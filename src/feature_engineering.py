"""Feature engineering for retail sales analysis."""

from __future__ import annotations

import pandas as pd


def add_sales_features(df: pd.DataFrame) -> pd.DataFrame:
    """Create sales, calendar, and shopping-behavior features."""
    featured = df.copy()
    featured["TotalSales"] = (
        featured["NumberOfItemsPurchased"] * featured["CostPerItem"]
    )
    featured["Year"] = featured["TransactionTime"].dt.year
    featured["Month"] = featured["TransactionTime"].dt.month
    featured["MonthName"] = featured["TransactionTime"].dt.month_name()
    featured["Quarter"] = featured["TransactionTime"].dt.quarter
    featured["Day"] = featured["TransactionTime"].dt.day
    featured["DayName"] = featured["TransactionTime"].dt.day_name()
    featured["Hour"] = featured["TransactionTime"].dt.hour
    featured["Week"] = featured["TransactionTime"].dt.isocalendar().week.astype(int)
    featured["WeekendFlag"] = featured["DayName"].isin(["Saturday", "Sunday"])
    return featured

