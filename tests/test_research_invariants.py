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
        "baseline_metrics.csv": "1038979d073bc704bd2c2174db200a2248756a2dd58cb23e2963944f21bb2cbc",
        "graph_edges.csv": "597d4cc2f5da938aa0371af36008f26c20d1b1ce26fe900078e889e7ffbce9b9",
        "knn_sensitivity.csv": "57008f9912d6b47d9966824e23d4d527bae3d5cc8ef4a912f297c37123ed0233",
        "noise_sensitivity.csv": "76493aa7033eaffe87c0a994b0f2130c542e3d868b27116d7c89456d5c6d3054",
        "observations.csv": "8b0486ae53162d4c1d66092fdf62f13e05afeffef42b8b00ec42b95ffe82746c",
        "partitions.csv": "3aaa377ecbb9c34fe3630850a44c187d558646914f56b32bafb5d14d14930498",
        "sites.csv": "7dc7a5871248b43530a8054c1ef35e9723c14489e6acdf50b1f5fce5ec8a741d",
    }
    for name, expected_hash in expected.items():
        payload = (ROOT / "data" / "generated" / name).read_bytes()
        assert hashlib.sha256(payload).hexdigest() == expected_hash, name
