"""Execute the research notebooks in order using fresh kernels."""

from __future__ import annotations

import argparse
import shutil
from pathlib import Path

import nbformat
from nbclient import NotebookClient

NOTEBOOKS = (
    "01_synthetic_field_investigation.ipynb",
    "02_spatial_temporal_analysis.ipynb",
    "03_evaluation_and_diagnostics.ipynb",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        required=True,
        help="Directory that receives executed notebook copies.",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]
    source_dir = root / "notebooks"
    output_dir = args.output_dir.resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    for name in NOTEBOOKS:
        source = source_dir / name
        destination = output_dir / name
        shutil.copy2(source, destination)
        with destination.open(encoding="utf-8") as handle:
            notebook = nbformat.read(handle, as_version=4)
        client = NotebookClient(
            notebook,
            timeout=600,
            kernel_name="python3",
            resources={"metadata": {"path": str(root)}},
        )
        client.execute()
        for cell in notebook.cells:
            cell.metadata.pop("execution", None)
        with destination.open("w", encoding="utf-8") as handle:
            nbformat.write(notebook, handle)
        print(f"executed {name}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
