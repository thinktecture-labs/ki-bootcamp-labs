"""Initial test for the "Embeddings & Vector DB" lab (Colab export of F95_Vector_DB_Lab).

The structural tests run everywhere. The live test runs what participants are expected to
build (bge-m3 via OVH AI Endpoints into an in-memory Qdrant collection, then the lab's
queries) and is skipped unless OVH_API_KEY is set; it catches a removed model or a changed
API before the workshop does.
"""

import ast
import os

import nbformat
import pytest
from conftest import NOTEBOOKS_DIR
from IPython.core.inputtransformer2 import TransformerManager

NOTEBOOK = NOTEBOOKS_DIR / "02-embeddings-vector-db-lab.ipynb"
OVH_BASE_URL = "https://oai.endpoints.kepler.ai.cloud.ovh.net/v1"
EMBEDDING_MODEL = "bge-m3"
COLAB_SECRET_NAME = "OVH_AI_ENDPOINTS_ACCESS_TOKEN"

QUERY_RUSSIAN_EMBASSY = (
    "Which movie is about a device in the Russian embassy? "
    "Who is the main actor and when was it released?"
)
QUERY_NO_BOND_MOVIE = "A young man comes to Bel Air"
QUERY_ROGER_MOORE = "List all movies with Roger Moore as main actor"

needs_ovh = pytest.mark.skipif(
    not os.environ.get("OVH_API_KEY"),
    reason="OVH_API_KEY not set – live check against OVH AI Endpoints skipped",
)


@pytest.fixture(scope="module")
def code() -> list[str]:
    notebook = nbformat.read(NOTEBOOK, as_version=4)
    return [cell.source for cell in notebook.cells if cell.cell_type == "code"]


@pytest.fixture(scope="module")
def docs_movies(code: list[str]) -> list[str]:
    """The demo-data cell assigns a list of strings to `docs_movies`; read it without
    executing notebook code."""
    transformer = (
        TransformerManager()
    )  # turns `!pip …` into Python so every cell parses
    for source in code:
        for node in ast.parse(transformer.transform_cell(source)).body:
            if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "docs_movies" for t in node.targets
            ):
                return ast.literal_eval(node.value)
    pytest.fail("no `docs_movies = [...]` cell found")


def test_lab_keeps_its_task_placeholders(code: list[str]) -> None:
    """The lab version must stay a lab: participants fill in the `...` after "Task:" hints."""
    source = "\n".join(code)
    assert source.count("Task:") >= 8
    assert source.count("...") >= 6
    assert 'model="..."' in source and 'base_url="..."' in source


def test_lab_uses_the_workshop_stack(code: list[str]) -> None:
    install_cell = code[0]
    assert "pip" in install_cell and "install" in install_cell
    for package in ("langchain", "langchain_openai", "langchain_qdrant"):
        assert package in install_cell, f"{package} missing from the install cell"
    source = "\n".join(code)
    assert "from langchain_openai import OpenAIEmbeddings" in source
    assert "from langchain_qdrant import QdrantVectorStore" in source
    assert 'collection_name="movies"' in source


def test_lab_reads_the_ovh_token_from_colab_secrets(code: list[str]) -> None:
    """Participants store the token under this name in Colab (🔑 Secrets); keep README in sync."""
    source = "\n".join(code)
    assert "from google.colab import userdata" in source
    assert f'userdata.get("{COLAB_SECRET_NAME}")' in source


def test_demo_data_are_the_bond_movies(docs_movies: list[str]) -> None:
    assert len(docs_movies) == 17  # Dr. No (1962) … GoldenEye (1995)
    assert all(doc.startswith("Filmnummer:") for doc in docs_movies)
    assert any("From Russia With Love" in doc for doc in docs_movies)
    assert sum("Hauptdarsteller: Roger Moore" in doc for doc in docs_movies) == 7


@needs_ovh
def test_solution_path_against_ovh(docs_movies: list[str]) -> None:
    from langchain_openai import OpenAIEmbeddings
    from langchain_qdrant import QdrantVectorStore
    from pydantic import SecretStr

    embeddings = OpenAIEmbeddings(
        model=EMBEDDING_MODEL,
        base_url=OVH_BASE_URL,
        api_key=SecretStr(os.environ["OVH_API_KEY"]),
    )
    store = QdrantVectorStore.from_texts(
        docs_movies,
        embeddings,
        location=":memory:",
        collection_name="movies",
        force_recreate=True,
    )

    # Q1: pure similarity search finds "From Russia With Love" (Lector in the Russian consulate)
    found = store.similarity_search(QUERY_RUSSIAN_EMBASSY, k=1)
    assert "From Russia With Love" in found[0].page_content

    # A query about a movie that is not in the collection still returns the nearest neighbour,
    # but with a clearly lower score – that is what the score_threshold task is about.
    (_, best_match_score), *_ = store.similarity_search_with_score(
        QUERY_RUSSIAN_EMBASSY, k=1
    )
    (_, no_match_score), *_ = store.similarity_search_with_score(
        QUERY_NO_BOND_MOVIE, k=1
    )
    assert no_match_score < best_match_score
    assert not store.similarity_search_with_score(
        QUERY_NO_BOND_MOVIE, score_threshold=0.9
    )

    # Q3: the first hits for the Roger Moore query are Roger Moore movies
    roger_moore = store.similarity_search(QUERY_ROGER_MOORE, k=3)
    assert all("Roger Moore" in doc.page_content for doc in roger_moore)
