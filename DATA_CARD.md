# Synthetic data card

## Intended use

This dataset supports the three published FPWM Lab notebooks. It is
a transparent computational fixture for studying diagnostics, evaluation
partitions, simple baselines, and reproducibility. It is not a representation
of an operating field or a reservoir simulation.

## Contents

| Property | Value |
| --- | --- |
| Sites | 24 fictional identities, `S00`–`S23` |
| Periods | 36 synthetic monthly indices, 0–35 |
| Rows | 864 site-period pairs |
| Observed targets | 801 (92.71%) |
| Missing targets | 63 (7.29%) |
| Coordinates | Normalized `x_norm` and `y_norm` in [0, 1] |
| Target | `pressure_su`, measured only in synthetic units |

The generator exposes its spatial, temporal, seasonal, perturbation, and site
components. Target missingness combines a recorded random draw with short gaps
for two fictional sites. The component columns are audit evidence and must not
be used as prediction features because they reveal the constructed answer.

## Provenance and reproducibility

Notebook 01 generates the data from seed `20261031`; later notebooks add graph,
partition, and baseline artifacts. The source is independent clean-room work.
No private data, operational geometry, model weights, or reference outputs are
included.

The committed CSVs are deterministic for the qualified environments. Tests
verify their identities and core invariants, while the notebooks retain the
actual generation assumptions and inspection outputs.

## Limitations

- The spatial surface and perturbation were selected for diagnostic variety,
  not physical fidelity.
- Missingness is only partly random.
- Normalized proximity does not imply subsurface communication.
- The five-site spatial holdout is a boundary test, not a representative field
  deployment sample.
- Results must not be generalized to real assets or operational decisions.
