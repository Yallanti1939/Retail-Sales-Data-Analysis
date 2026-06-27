"""Data cleaning routines for retail transaction records."""

from __future__ import annotations

import pandas as pd

from src.data_loader import validate_columns


NUMERIC_COLUMNS = ["NumberOfItemsPurchased", "CostPerItem"]


def _parse_transaction_time(series: pd.Series) -> pd.Series:
    """Parse transaction timestamps that include timezone abbreviations."""
    cleaned = series.astype(str).str.replace(r"\sIST\s", " ", regex=True)
    return pd.to_datetime(cleaned, errors="coerce")


def remove_outliers_iqr(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Remove extreme values using the interquartile-range rule."""
    q1 = df[column].quantile(0.25)
    q3 = df[column].quantile(0.75)
    iqr = q3 - q1
    lower = q1 - 1.5 * iqr
    upper = q3 + 1.5 * iqr
    return df[(df[column] >= lower) & (df[column] <= upper)]


def remove_outliers_zscore(
    df: pd.DataFrame,
    column: str,
    threshold: float = 3.0,
) -> pd.DataFrame:
    """Remove values outside the z-score threshold."""
    standard_deviation = df[column].std()
    if standard_deviation == 0 or pd.isna(standard_deviation):
        return df
    z_scores = (df[column] - df[column].mean()) / standard_deviation
    return df[z_scores.abs() <= threshold]


def clean_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Clean raw retail transactions and return valid records only."""
    validate_columns(df)
    cleaned = df.copy()

    cleaned = cleaned.drop_duplicates()
    cleaned["TransactionTime"] = _parse_transaction_time(cleaned["TransactionTime"])

    for column in NUMERIC_COLUMNS:
        cleaned[column] = pd.to_numeric(cleaned[column], errors="coerce")

    cleaned["ItemDescription"] = cleaned["ItemDescription"].fillna("Unknown")
    cleaned["Country"] = cleaned["Country"].fillna("Unknown")

    cleaned = cleaned.dropna(
        subset=[
            "TransactionID",
            "TransactionTime",
            "ItemCode",
            "NumberOfItemsPurchased",
            "CostPerItem",
        ]
    )

    cleaned = cleaned[
        (cleaned["NumberOfItemsPurchased"] > 0) & (cleaned["CostPerItem"] > 0)
    ]

    for column in NUMERIC_COLUMNS:
        cleaned = remove_outliers_iqr(cleaned, column)
        cleaned = remove_outliers_zscore(cleaned, column)

    return cleaned.reset_index(drop=True)

