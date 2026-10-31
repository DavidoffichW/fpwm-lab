from __future__ import annotations

from pathlib import Path

import pandas as pd

ROOT = Path(__file__).resolve().parents[1]


def test_generated_observations_are_fully_synthetic_and_bounded() -> None:
    observations = pd.read_csv(ROOT / "data" / "generated" / "observations.csv")
    assert observations["site_id"].str.fullmatch(r"S\d{2}").all()
    assert observations["x_norm"].between(0, 1).all()
    assert observations["y_norm"].between(0, 1).all()
    assert observations["pressure_su"].notna().mean() > 0.85
    assert observations.duplicated(["site_id", "period"]).sum() == 0


def test_evaluation_partitions_are_disjoint() -> None:
    partitions = pd.read_csv(ROOT / "data" / "generated" / "partitions.csv")
    chronological = partitions.dropna(subset=["chronological_role"])
    train = chronological[chronological["chronological_role"] == "train"]
    test = chronological[chronological["chronological_role"] == "test"]
    assert train["period"].max() < test["period"].min()

    spatial = partitions.dropna(subset=["spatial_role"])
    train_sites = set(spatial.loc[spatial["spatial_role"] == "train", "site_id"])
    test_sites = set(spatial.loc[spatial["spatial_role"] == "test", "site_id"])
    assert train_sites.isdisjoint(test_sites)
