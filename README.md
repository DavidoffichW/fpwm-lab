# Field Pressure World Model

A small, synthetic research workbench for asking spatial-temporal questions
about pressure-like observations. The notebooks emphasize inspection,
diagnostics, and interpretation rather than presenting a finished operational
model.

Everything in this repository is fictional. Coordinates are normalized,
pressure values use synthetic units, and site identifiers do not correspond to
real assets. The workbench is not a reservoir simulator, a forecasting service,
or evidence that geographic proximity implies physical communication.

## What is here

The notebooks are meant to be read and run in order:

1. `01_synthetic_field_investigation.ipynb` builds and examines a fictional
   observation set.
2. `02_spatial_temporal_analysis.ipynb` studies distance graphs, observation
   coverage, and leakage-resistant evaluation partitions.
3. `03_evaluation_and_diagnostics.ipynb` introduces simple baselines one at a
   time and examines their errors and sensitivity.

Calculations stay in short, visible cells. Markdown records the question,
assumptions, observations, and limitations around each experiment. A small
runner exists only to verify that the notebooks execute sequentially from clean
kernels; it does not hide the research workflow.

## Run the notebooks

Python 3.10 or newer is recommended.

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe -m jupyter lab
```

Open the three notebooks in `notebooks/` and run them in numeric order.

To execute the complete sequence without changing the committed notebooks:

```powershell
.\.venv\Scripts\python.exe .\tools\run_notebooks.py --output-dir .\build\executed
```

### macOS or Linux

```bash
python3 -m venv .venv
.venv/bin/python -m pip install --upgrade pip
.venv/bin/python -m pip install -r requirements.txt -r requirements-dev.txt
.venv/bin/python -m jupyter lab
```

For a headless sequential run:

```bash
.venv/bin/python tools/run_notebooks.py --output-dir build/executed
```

The first notebook writes compact synthetic CSV artifacts to
`data/generated/`. The later notebooks consume those artifacts. Re-running the
sequence with the recorded seed replaces them deterministically.

## Validate the workbench

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check tools tests
```

The tests check notebook structure, confidentiality boundaries, sequential
execution, deterministic synthetic artifacts, and core scientific invariants.

## Research boundary

The baselines are intentionally modest. In particular, nearest-neighbour
interpolation is reported as nearest-neighbour interpolation; adding independent
noise would not make it conditional sequential Gaussian simulation. Empirical
prediction spread is also not a calibrated uncertainty interval.

No private field data, operational assumptions, model weights, or training
code are included. Results describe this synthetic experiment only.

## License

An authored-code license has not yet been selected. The repository is suitable
for local review, but redistribution and public release remain blocked until
the owner records that decision.
