"""Checks for every notebook in this folder: valid nbformat, compiling code, Codespaces-ready."""

from pathlib import Path

import nbformat
import pytest
from conftest import NOTEBOOKS_DIR
from IPython.core.inputtransformer2 import TransformerManager

NOTEBOOKS = sorted(NOTEBOOKS_DIR.glob("*.ipynb"))


def read(path: Path) -> nbformat.NotebookNode:
    return nbformat.read(path, as_version=4)


def test_there_are_notebooks() -> None:
    assert NOTEBOOKS, f"no .ipynb files in {NOTEBOOKS_DIR}"


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_is_valid_nbformat(path: Path) -> None:
    nbformat.validate(read(path))


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_code_cells_compile(path: Path) -> None:
    """Every code cell must be valid IPython once task placeholders (`...`) are filled in."""
    transformer = TransformerManager()
    for index, cell in enumerate(read(path).cells):
        if cell.cell_type != "code":
            continue
        # Lab placeholders may stand anywhere (`OpenAI...`, `... = "..."`), so compile them as a
        # name; a stray `..` still fails.
        source = transformer.transform_cell(cell.source.replace("...", "_"))
        compile(source, f"{path.name}[cell {index}]", "exec")


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_has_no_stored_outputs(path: Path) -> None:
    """Notebooks are committed without outputs to keep diffs readable."""
    for index, cell in enumerate(read(path).cells):
        if cell.cell_type == "code":
            assert not cell.outputs, f"{path.name}[cell {index}] has stored outputs"
            assert cell.execution_count is None, (
                f"{path.name}[cell {index}] has an execution count"
            )


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_runs_in_codespaces(path: Path) -> None:
    """No Colab-only APIs, no package installs (dependencies come from pyproject.toml), and the
    dev container's kernel preselected so VS Code does not ask."""
    notebook = read(path)
    assert notebook.metadata.kernelspec.name == "notebooks"
    assert "colab" not in notebook.metadata
    for index, cell in enumerate(notebook.cells):
        if cell.cell_type != "code":
            continue
        where = f"{path.name}[cell {index}]"
        assert "google.colab" not in cell.source, f"{where} uses google.colab"
        assert "pip install" not in cell.source, (
            f"{where} installs packages; add them to pyproject.toml"
        )
