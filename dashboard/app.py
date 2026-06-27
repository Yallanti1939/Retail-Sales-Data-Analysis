"""Streamlit dashboard for interactive retail sales analysis."""

from __future__ import annotations

from pathlib import Path
import sys

import pandas as pd
import plotly.express as px
import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.analysis import (
    build_analysis_tables,
    calculate_kpis,
    generate_business_insights,
)
from src.data_cleaning import clean_transactions
from src.data_loader import load_csv
from src.feature_engineering import add_sales_features


RAW_DATA = PROJECT_ROOT / "data" / "transaction_data.csv"
CLEAN_DATA = PROJECT_ROOT / "data" / "cleaned_transaction_data.csv"


@st.cache_data
def load_dashboard_data() -> pd.DataFrame:
    """Load cleaned data when available, otherwise clean the raw CSV."""
    if CLEAN_DATA.exists():
        df = pd.read_csv(CLEAN_DATA, parse_dates=["TransactionTime"])
    else:
        raw_df = load_csv(RAW_DATA)
        df = add_sales_features(clean_transactions(raw_df))
    return df


def apply_filters(df: pd.DataFrame) -> pd.DataFrame:
    """Apply sidebar country, product, and date filters."""
    st.sidebar.header("Filters")
    countries = sorted(df["Country"].dropna().unique())
    products = sorted(df["ItemDescription"].dropna().unique())

    selected_countries = st.sidebar.multiselect("Country", countries, default=countries)
    selected_products = st.sidebar.multiselect("Product", products)
    min_date = df["TransactionTime"].min().date()
    max_date = df["TransactionTime"].max().date()
    date_range = st.sidebar.date_input("Date Range", value=(min_date, max_date))

    filtered = df[df["Country"].isin(selected_countries)]
    if selected_products:
        filtered = filtered[filtered["ItemDescription"].isin(selected_products)]
    if len(date_range) == 2:
        start, end = date_range
        filtered = filtered[
            (filtered["TransactionTime"].dt.date >= start)
            & (filtered["TransactionTime"].dt.date <= end)
        ]
    return filtered


def render_overview(df: pd.DataFrame) -> None:
    """Render dashboard overview page."""
    kpis = calculate_kpis(df)
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Total Revenue", f"{kpis['total_revenue']:,.2f}")
    col2.metric("Transactions", f"{kpis['total_transactions']:,}")
    col3.metric("Countries", f"{kpis['total_countries']:,}")
    col4.metric("Products", f"{kpis['total_products']:,}")

    tables = build_analysis_tables(df)
    st.plotly_chart(
        px.line(tables["monthly_sales"], x="YearMonth", y="TotalSales", markers=True),
        use_container_width=True,
    )
    st.plotly_chart(
        px.bar(tables["top_10_countries"], x="TotalSales", y="Country", orientation="h"),
        use_container_width=True,
    )


def render_product_analysis(df: pd.DataFrame) -> None:
    """Render product analysis page."""
    tables = build_analysis_tables(df)
    st.plotly_chart(
        px.bar(
            tables["top_10_products"],
            x="TotalSales",
            y="ItemDescription",
            orientation="h",
        ),
        use_container_width=True,
    )
    st.dataframe(tables["product_revenue"], use_container_width=True)


def render_country_analysis(df: pd.DataFrame) -> None:
    """Render country analysis page."""
    tables = build_analysis_tables(df)
    st.plotly_chart(
        px.pie(tables["top_10_countries"], values="TotalSales", names="Country"),
        use_container_width=True,
    )
    st.dataframe(tables["country_revenue"], use_container_width=True)


def render_sales_trends(df: pd.DataFrame) -> None:
    """Render sales trends page."""
    tables = build_analysis_tables(df)
    st.plotly_chart(
        px.area(tables["quarterly_sales"], x="Quarter", y="TotalSales", color="Year"),
        use_container_width=True,
    )
    st.plotly_chart(
        px.bar(tables["hourly_transactions"], x="Hour", y="Transactions"),
        use_container_width=True,
    )


def render_business_insights(df: pd.DataFrame) -> None:
    """Render business insights page."""
    for insight in generate_business_insights(df):
        st.write(f"- {insight}")


def main() -> None:
    """Run the Streamlit dashboard."""
    st.set_page_config(page_title="Retail Sales Dashboard", layout="wide")
    st.title("Retail Sales Analysis Dashboard")
    data = load_dashboard_data()
    filtered_data = apply_filters(data)

    page = st.sidebar.radio(
        "Dashboard Pages",
        [
            "Overview",
            "Product Analysis",
            "Country Analysis",
            "Sales Trends",
            "Business Insights",
        ],
    )

    if filtered_data.empty:
        st.warning("No records match the selected filters.")
        return

    if page == "Overview":
        render_overview(filtered_data)
    elif page == "Product Analysis":
        render_product_analysis(filtered_data)
    elif page == "Country Analysis":
        render_country_analysis(filtered_data)
    elif page == "Sales Trends":
        render_sales_trends(filtered_data)
    else:
        render_business_insights(filtered_data)


if __name__ == "__main__":
    main()
