# Synthetic experiment results

All values below come from the executed synthetic notebooks. The protocols have
different information boundaries and answer different questions.

## Baseline scorecard

| Protocol | Domain | Baseline | n | MAE | RMSE | Bias |
| --- | --- | --- | ---: | ---: | ---: | ---: |
| Chronological prediction | Periods 28–35; observed test rows | Per-site linear trend | 178 | 0.225458 | 0.269812 | -0.065418 |
| Chronological prediction | Periods 28–35; observed test rows | Per-site persistence | 178 | 0.320228 | 0.395955 | -0.261640 |
| Chronological prediction | Periods 28–35; observed test rows | Global mean | 178 | 0.602560 | 0.802759 | 0.402273 |
| Same-period spatial interpolation | Five eastern-boundary sites; all periods | Distance-weighted KNN, k=5 | 157 | 0.649611 | 0.876292 | 0.586843 |

Chronological rows predict later periods using only periods 0–27. The spatial
row predicts withheld sites from other sites observed in the same period. Its
error is therefore interpolation evidence, not forecasting evidence.

## Controlled measurement-noise sensitivity

One standardized random draw is reused at every scale, so the injected
perturbations differ only by multiplication and have pairwise correlation 1.0.

| Noise scale | Response standard deviation | 5th percentile | 95th percentile |
| ---: | ---: | ---: | ---: |
| 0.08 | 0.780191 | 10.179462 | 12.785987 |
| 0.16 | 0.789857 | 10.142154 | 12.772923 |
| 0.32 | 0.832609 | 10.116363 | 12.843064 |

The full response spread increases as the controlled noise scale rises, but
only modestly because the held-fixed latent components already contribute most
of the variation. The experiment does not estimate real measurement noise.

## Spatial neighbour sensitivity

| Neighbours | n | MAE | RMSE | Bias |
| ---: | ---: | ---: | ---: | ---: |
| 3 | 157 | 0.666393 | 0.896828 | 0.635001 |
| 5 | 157 | 0.649611 | 0.876292 | 0.586843 |
| 8 | 157 | 0.667782 | 0.891687 | 0.576098 |

Errors are close across these three choices; that supports limited local
stability for this synthetic holdout only. KNN remains a distance-based
interpolator, and neighbour-value spread remains descriptive rather than a
calibrated uncertainty interval.
