# Field Pressure World Model

A notebook-first study of spatial and temporal prediction on a deliberately
fictional pressure-like field.

The point is not to present a finished model. It is to make the research trail
visible: inspect the observations, change one assumption, look at the result,
and record what the evidence does—and does not—support.

Everything here is synthetic. Coordinates are normalized, values use synthetic
units, and site identifiers do not refer to real assets.

## The study

Read the notebooks in order:

1. [Synthetic field investigation](notebooks/01_synthetic_field_investigation.ipynb) — constructs the fictional observations, diagnoses missingness, and tests measurement-noise sensitivity.
2. [Spatial and temporal analysis](notebooks/02_spatial_temporal_analysis.ipynb) — examines distances, graph connectivity, chronological leakage, and a disjoint spatial holdout.
3. [Evaluation and experimental diagnostics](notebooks/03_evaluation_and_diagnostics.ipynb) — evaluates transparent temporal baselines and same-period spatial interpolation.

The working assumptions are intentionally modest:

- a smooth synthetic surface, temporal drift, seasonality, site offsets, and one localized perturbation create enough structure for diagnostics;
- normalized distance can define a computational neighbourhood, but does not establish physical communication;
- periods 0–27 may train a chronological baseline and periods 28–35 test later-period prediction;
- five eastern-boundary sites may be withheld to study same-period spatial interpolation.

![Synthetic pressure-like snapshots at three periods](docs/images/synthetic_field_snapshots.png)

The shared colour scale above comes from the complete synthetic response range.
No observations are clipped.

![Selected computational graph with node degree colouring](docs/images/computational_graph.png)

Node colour is graph degree. The graph is a modelling choice over normalized
coordinates—not a map of subsurface connectivity.

## Results

The two evaluation protocols answer different questions and should not be
treated as one leaderboard.

| Protocol | Domain | Baseline | n | MAE | RMSE | Bias |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Chronological prediction | Periods 28–35; observed test rows | Per-site linear trend | 178 | 0.225458 | 0.269812 | -0.065418 |
| Chronological prediction | Periods 28–35; observed test rows | Per-site persistence | 178 | 0.320228 | 0.395955 | -0.261640 |
| Chronological prediction | Periods 28–35; observed test rows | Global mean | 178 | 0.602560 | 0.802759 | 0.402273 |
| Same-period spatial interpolation | Five eastern-boundary sites; all periods | Distance-weighted KNN, k=5 | 157 | 0.649611 | 0.876292 | 0.586843 |

The temporal trend is the strongest chronological reference on this synthetic
split. The spatial result is harder and measures interpolation at held-out
boundary sites using observations from the same period; it is not a forecast.
See [RESULTS.md](RESULTS.md) for the controlled noise and neighbour-count
sensitivity tables.

These experiments establish that the synthetic generator is reproducible, the
evaluation partitions are explicit, and simple assumptions produce measurable
and diagnosable errors. They do **not** establish geological realism, causal
behaviour, reservoir communication, calibrated uncertainty, operational
forecasting performance, or the quality of any private model.

## Data

The generated corpus contains 24 fictional sites across 36 periods: 864 rows,
of which 801 have an observed target. Generator components remain in the table
so every synthetic value can be audited. Read the compact [synthetic data card](DATA_CARD.md)
before reusing the artifacts.

## Reproduce the study

Python 3.10 or newer is supported by the current CI matrix.

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\python.exe -m pip install --upgrade pip
.\.venv\Scripts\python.exe -m pip install -r requirements.txt -r requirements-dev.txt
.\.venv\Scripts\python.exe -m jupyter lab
```

Open the notebooks from `notebooks/` and run them in numeric order.

For a clean headless execution that leaves the committed notebooks untouched:

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

```bash
.venv/bin/python tools/run_notebooks.py --output-dir build/executed
```

The notebooks regenerate `data/generated/` from the recorded seed. Validate the
research contracts afterward:

```powershell
.\.venv\Scripts\python.exe -m pytest -q
.\.venv\Scripts\python.exe -m ruff check tools tests
```

## References

Presentation and reproducible-research structure were informed by the
[Liquid AI cookbook](https://github.com/Liquid4All/cookbook), its
[wind-turbine inspection example](https://github.com/Liquid4All/cookbook/tree/main/examples/wind-turbine-inspection),
and the [Data Engineering Handbook](https://github.com/DataExpert-io/data-engineer-handbook).
The implementation uses [NumPy](https://numpy.org/),
[pandas](https://pandas.pydata.org/), [SciPy](https://scipy.org/),
[NetworkX](https://networkx.org/), [Matplotlib](https://matplotlib.org/), and
[scikit-learn](https://scikit-learn.org/).

## License

An authored-code license has not been selected. The private repository is open
for owner review, but public redistribution and release remain blocked until
that decision is recorded.
