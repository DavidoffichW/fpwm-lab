from __future__ import annotations

import hashlib
from pathlib import Path

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_generated_observations_are_fully_synthetic_and_bounded() -> None:
    observations = pd.read_csv(ROOT / "data" / "generated" / "observations.csv")
    assert observations["site_id"].str.fullmatch(r"S\d{2}").all()
    assert observations["x_norm"].between(0, 1).all()
    assert observations["y_norm"].between(0, 1).all()
    assert observations["pressure_su"].notna().mean() > 0.85
    assert observations.duplicated(["site_id", "period"]).sum() == 0


def test_chronological_split_has_exact_later_period_semantics() -> None:
    partitions = pd.read_csv(ROOT / "data" / "generated" / "partitions.csv")
    chronological = partitions.dropna(subset=["chronological_role"])
    train = chronological[chronological["chronological_role"] == "train"]
    test = chronological[chronological["chronological_role"] == "test"]
    assert set(train["period"]) == set(range(28))
    assert set(test["period"]) == set(range(28, 36))
    assert test["period"].nunique() == 8
    assert train["period"].max() < test["period"].min()


def test_spatial_holdout_is_disjoint_by_site() -> None:
    partitions = pd.read_csv(ROOT / "data" / "generated" / "partitions.csv")
    spatial = partitions.dropna(subset=["spatial_role"])
    train_sites = set(spatial.loc[spatial["spatial_role"] == "train", "site_id"])
    test_sites = set(spatial.loc[spatial["spatial_role"] == "test", "site_id"])
    assert train_sites.isdisjoint(test_sites)
    assert len(train_sites) == 19
    assert len(test_sites) == 5
    assert set(spatial["period"]) == set(range(36))


def test_noise_sensitivity_reuses_one_standardized_draw() -> None:
    sensitivity = pd.read_csv(ROOT / "data" / "generated" / "noise_sensitivity.csv")
    assert sensitivity["noise_scale"].tolist() == [0.08, 0.16, 0.32]
    assert sensitivity["noise_sample_id"].nunique() == 1
    assert sensitivity["response_std"].is_monotonic_increasing

    notebook = (ROOT / "notebooks" / "01_synthetic_field_investigation.ipynb").read_text(encoding="utf-8")
    assert notebook.count("standard_normal") == 1
    assert "scale * standard_noise" in notebook


def test_global_mean_metrics_match_an_independent_calculation() -> None:
    observations = pd.read_csv(ROOT / "data" / "generated" / "observations.csv")
    partitions = pd.read_csv(ROOT / "data" / "generated" / "partitions.csv")
    data = observations.merge(
        partitions.drop(columns="pressure_su"), on=["site_id", "period"], validate="one_to_one"
    )
    train = data.query("chronological_role == 'train'")["pressure_su"].dropna()
    test = data.query("chronological_role == 'test'")["pressure_su"].dropna()
    residual = test - train.mean()

    scorecard = pd.read_csv(ROOT / "data" / "generated" / "baseline_metrics.csv")
    observed = scorecard.query("baseline == 'global mean'").iloc[0]
    assert observed["protocol"] == "chronological prediction"
    assert observed["n"] == len(test) == 178
    assert np.isclose(observed["mae"], residual.abs().mean())
    assert np.isclose(observed["rmse"], np.sqrt(np.mean(residual**2)))
    assert np.isclose(observed["bias"], residual.mean())


def test_generated_artifact_identities() -> None:
    expected = {
        "baseline_metrics.csv": "389de071338a1771650f04922c601ef9e6c2ddbb2b46d3a066835f53acfb506f",
        "graph_edges.csv": "cf64e8a0d23de93a1f4d448dcd40281c138b392f749b09bac7162ec4ce3196a8",
        "knn_sensitivity.csv": "a71614adecf95372ae7e1862f49daf51ea699b4962202c49e3600a696e3cc3e9",
        "noise_sensitivity.csv": "789a17dd24f5924f759fd356aff64f2ce45f7a61c90e6e25081262a4524c8704",
        "observations.csv": "ec06b923683a56714abdc2527253f140f4f8cedcd9190463695082f8a0ea2c5f",
        "partitions.csv": "5cf5f4a856a85507608637cf7b1bc00bd76dc591deb195ed0c987fe151f1e894",
        "sites.csv": "0a0fc6fd28c1a4aad253cdea685fe003d9dc6851ef6bab9440a52a41b5f749ff",
    }
    for name, expected_hash in expected.items():
        payload = (ROOT / "data" / "generated" / name).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_hash, name
