from __future__ import annotations

import ast
from pathlib import Path

import nbformat

ROOT = Path(__file__).resolve().parents[1]
NOTEBOOKS = sorted((ROOT / "notebooks").glob("*.ipynb"))


def test_three_research_notebooks_are_present() -> None:
    assert [path.name[:2] for path in NOTEBOOKS] == ["01", "02", "03"]


def test_code_cells_remain_short_and_transparent() -> None:
    for path in NOTEBOOKS:
        notebook = nbformat.read(path, as_version=4)
        code_cells = [cell for cell in notebook.cells if cell.cell_type == "code"]
        lengths = [len(cell.source.splitlines()) for cell in code_cells]
        assert max(lengths) <= 30, path.name
        assert sum(lengths) / len(lengths) <= 12, path.name

        tree = ast.parse("\n\n".join(cell.source for cell in code_cells))
        assert not any(isinstance(node, ast.ClassDef) for node in ast.walk(tree))


def test_markdown_interpretation_is_substantive() -> None:
    required = {"question", "assumption", "evidence", "limitation"}
    for path in NOTEBOOKS:
        notebook = nbformat.read(path, as_version=4)
        markdown = "\n".join(
            cell.source.lower()
            for cell in notebook.cells
            if cell.cell_type == "markdown"
        )
        assert required <= {word for word in required if word in markdown}, path.name
        assert len(markdown.split()) >= 500, path.name


def test_private_reference_expression_is_absent() -> None:
    forbidden = ("hips_relocation", "c:\\users", "d:\\projects", "real field")
    for path in NOTEBOOKS:
        text = path.read_text(encoding="utf-8").lower()
        assert not any(term in text for term in forbidden), path.name
