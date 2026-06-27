"""Chart generation for reports and dashboards."""

from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from src.analysis import (
    country_revenue,
    hourly_transactions,
    item_purchase_frequency,
    monthly_sales,
    product_revenue,
    quarterly_sales,
)


sns.set_theme(style="whitegrid")


def _save_current_figure(output_path: Path) -> None:
    """Save and close the active Matplotlib figure."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    plt.tight_layout()
    plt.savefig(output_path, dpi=160, bbox_inches="tight")
    plt.close()


def create_all_charts(df: pd.DataFrame, charts_dir: str | Path) -> list[Path]:
    """Create all requested chart images and return their paths."""
    output_dir = Path(charts_dir)
    chart_paths: list[Path] = []

    monthly = monthly_sales(df)
    plt.figure(figsize=(11, 5))
    sns.lineplot(data=monthly, x="YearMonth", y="TotalSales", marker="o")
    plt.title("Monthly Sales Trend")
    plt.xticks(rotation=45, ha="right")
    path = output_dir / "monthly_sales_trend.png"
    _save_current_figure(path)
    chart_paths.append(path)

    top_products = product_revenue(df).head(10)
    plt.figure(figsize=(11, 6))
    sns.barplot(data=top_products, y="ItemDescription", x="TotalSales")
    plt.title("Top Products by Revenue")
    path = output_dir / "top_products.png"
    _save_current_figure(path)
    chart_paths.append(path)

    top_countries = country_revenue(df).head(10)
    plt.figure(figsize=(10, 5))
    sns.barplot(data=top_countries, x="TotalSales", y="Country")
    plt.title("Top Countries by Revenue")
    path = output_dir / "country_revenue.png"
    _save_current_figure(path)
    chart_paths.append(path)

    plt.figure(figsize=(8, 8))
    plt.pie(
        top_countries["TotalSales"],
        labels=top_countries["Country"],
        autopct="%1.1f%%",
        startangle=140,
    )
    plt.title("Country Revenue Distribution")
    path = output_dir / "country_distribution.png"
    _save_current_figure(path)
    chart_paths.append(path)

    plt.figure(figsize=(9, 5))
    sns.histplot(df["TotalSales"], bins=50, kde=True)
    plt.title("Revenue Distribution")
    path = output_dir / "revenue_distribution.png"
    _save_current_figure(path)
    chart_paths.append(path)

    plt.figure(figsize=(8, 5))
    sns.boxplot(x=df["TotalSales"])
    plt.title("Total Sales Outlier Check")
    path = output_dir / "outliers_boxplot.png"
    _save_current_figure(path)
    chart_paths.append(path)

    numeric = df[["NumberOfItemsPurchased", "CostPerItem", "TotalSales", "Hour"]]
    plt.figure(figsize=(7, 5))
    sns.heatmap(numeric.corr(), annot=True, cmap="crest", fmt=".2f")
    plt.title("Correlation Matrix")
    path = output_dir / "correlation_heatmap.png"
    _save_current_figure(path)
    chart_paths.append(path)

    quarterly = quarterly_sales(df)
    quarterly["Period"] = quarterly["Year"].astype(str) + " Q" + quarterly[
        "Quarter"
    ].astype(str)
    plt.figure(figsize=(10, 5))
    plt.fill_between(quarterly["Period"], quarterly["TotalSales"], alpha=0.35)
    sns.lineplot(data=quarterly, x="Period", y="TotalSales", marker="o")
    plt.title("Quarterly Sales Area Trend")
    plt.xticks(rotation=45, ha="right")
    path = output_dir / "quarterly_sales_area.png"
    _save_current_figure(path)
    chart_paths.append(path)

    hours = hourly_transactions(df)
    plt.figure(figsize=(10, 5))
    sns.barplot(data=hours, x="Hour", y="Transactions")
    plt.title("Hourly Transactions")
    path = output_dir / "hourly_transactions.png"
    _save_current_figure(path)
    chart_paths.append(path)

    top_items = item_purchase_frequency(df).head(10)
    plt.figure(figsize=(11, 6))
    sns.barplot(data=top_items, y="ItemDescription", x="NumberOfItemsPurchased")
    plt.title("Top Purchased Items")
    path = output_dir / "top_purchased_items.png"
    _save_current_figure(path)
    chart_paths.append(path)

    return chart_paths

