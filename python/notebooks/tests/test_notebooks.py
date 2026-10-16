"""Structural checks for every notebook in this folder: valid nbformat, Python that compiles."""

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
    """Every code cell must be valid IPython: `%pip` / `!pip` lines are transformed first,
    task placeholders (`...`) are valid Python, a stray `..` is not."""
    transformer = TransformerManager()
    for index, cell in enumerate(read(path).cells):
        if cell.cell_type != "code":
            continue
        source = transformer.transform_cell(cell.source)
        compile(source, f"{path.name}[cell {index}]", "exec")


@pytest.mark.parametrize("path", NOTEBOOKS, ids=lambda p: p.name)
def test_notebook_has_no_stored_outputs(path: Path) -> None:
    """Notebooks are committed clean (Colab export → outputs cleared) to keep diffs readable."""
    for index, cell in enumerate(read(path).cells):
        if cell.cell_type == "code":
            assert not cell.outputs, f"{path.name}[cell {index}] has stored outputs"
            assert cell.execution_count is None, (
                f"{path.name}[cell {index}] has an execution count"
            )
