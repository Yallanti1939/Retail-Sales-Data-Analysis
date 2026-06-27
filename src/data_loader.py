"""Utilities for loading and profiling retail transaction data."""

from __future__ import annotations

from pathlib import Path

import pandas as pd


EXPECTED_COLUMNS = [
    "TransactionID",
    "TransactionTime",
    "ItemCode",
    "ItemDescription",
    "NumberOfItemsPurchased",
    "CostPerItem",
    "Country",
]


def load_csv(file_path: str | Path) -> pd.DataFrame:
    """Load transaction CSV data and normalize known column names."""
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"CSV file not found: {path}")

    df = pd.read_csv(path)
    if "TransactionId" in df.columns and "TransactionID" not in df.columns:
        df = df.rename(columns={"TransactionId": "TransactionID"})
    return df


def profile_dataframe(df: pd.DataFrame) -> dict[str, object]:
    """Return basic profile outputs for collection-stage reporting."""
    return {
        "head": df.head(),
        "tail": df.tail(),
        "shape": df.shape,
        "info": df.dtypes.astype(str).to_dict(),
        "describe": df.describe(include="all"),
    }


def validate_columns(df: pd.DataFrame) -> None:
    """Raise a clear error when required project columns are missing."""
    missing = [column for column in EXPECTED_COLUMNS if column not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

