"""Exploratory analysis and insight generation."""

from __future__ import annotations

import pandas as pd


def calculate_kpis(df: pd.DataFrame) -> dict[str, float | int]:
    """Calculate high-level business KPIs."""
    total_revenue = float(df["TotalSales"].sum())
    total_transactions = int(df["TransactionID"].nunique())
    return {
        "total_revenue": total_revenue,
        "total_transactions": total_transactions,
        "total_countries": int(df["Country"].nunique()),
        "total_products": int(df["ItemCode"].nunique()),
        "average_order_value": (
            total_revenue / total_transactions if total_transactions else 0.0
        ),
    }


def monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Return monthly revenue trend."""
    monthly = (
        df.assign(YearMonth=df["TransactionTime"].dt.to_period("M").astype(str))
        .groupby("YearMonth", as_index=False)["TotalSales"]
        .sum()
        .sort_values("YearMonth")
    )
    return monthly


def quarterly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """Return quarterly revenue by year and quarter."""
    return (
        df.groupby(["Year", "Quarter"], as_index=False)["TotalSales"]
        .sum()
        .sort_values(["Year", "Quarter"])
    )


def country_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Return revenue by country."""
    return (
        df.groupby("Country", as_index=False)["TotalSales"]
        .sum()
        .sort_values("TotalSales", ascending=False)
    )


def product_revenue(df: pd.DataFrame) -> pd.DataFrame:
    """Return revenue by product."""
    return (
        df.groupby(["ItemCode", "ItemDescription"], as_index=False)["TotalSales"]
        .sum()
        .sort_values("TotalSales", ascending=False)
    )


def hourly_transactions(df: pd.DataFrame) -> pd.DataFrame:
    """Return transaction count by shopping hour."""
    return (
        df.groupby("Hour", as_index=False)["TransactionID"]
        .nunique()
        .rename(columns={"TransactionID": "Transactions"})
        .sort_values("Hour")
    )


def item_purchase_frequency(df: pd.DataFrame) -> pd.DataFrame:
    """Return total purchased units by item."""
    return (
        df.groupby(["ItemCode", "ItemDescription"], as_index=False)[
            "NumberOfItemsPurchased"
        ]
        .sum()
        .sort_values("NumberOfItemsPurchased", ascending=False)
    )


def build_analysis_tables(df: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build all tabular outputs needed by reports and dashboards."""
    tables = {
        "monthly_sales": monthly_sales(df),
        "quarterly_sales": quarterly_sales(df),
        "country_revenue": country_revenue(df),
        "product_revenue": product_revenue(df),
        "top_10_products": product_revenue(df).head(10),
        "top_10_countries": country_revenue(df).head(10),
        "hourly_transactions": hourly_transactions(df),
        "item_purchase_frequency": item_purchase_frequency(df),
    }
    return tables


def generate_business_insights(df: pd.DataFrame) -> list[str]:
    """Generate concise business insights from analyzed data."""
    kpis = calculate_kpis(df)
    countries = country_revenue(df)
    products = product_revenue(df)
    monthly = monthly_sales(df)
    hours = hourly_transactions(df)
    quarterly = quarterly_sales(df)

    best_country = countries.iloc[0]
    best_product = products.iloc[0]
    best_month = monthly.loc[monthly["TotalSales"].idxmax()]
    peak_hour = hours.loc[hours["Transactions"].idxmax()]
    best_quarter = quarterly.loc[quarterly["TotalSales"].idxmax()]

    return [
        (
            f"Highest revenue country is {best_country['Country']} with "
            f"{best_country['TotalSales']:,.2f} in sales."
        ),
        (
            f"Highest selling product by revenue is "
            f"{best_product['ItemDescription']} ({best_product['ItemCode']})."
        ),
        f"Best sales month is {best_month['YearMonth']}.",
        f"Peak shopping hour is {int(peak_hour['Hour']):02d}:00.",
        f"Average transaction value is {kpis['average_order_value']:,.2f}.",
        (
            f"Strongest seasonal quarter is Q{int(best_quarter['Quarter'])} "
            f"{int(best_quarter['Year'])}."
        ),
        "Track country and product concentration to manage inventory and campaigns.",
    ]

