"""Business insight generation and export utilities."""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.analysis import calculate_kpis, generate_business_insights
from src.utils import format_currency, write_lines


def build_insight_report_lines(df: pd.DataFrame) -> list[str]:
    """Build a text-ready business insight report."""
    kpis = calculate_kpis(df)
    lines = [
        "Retail Sales Business Insights",
        "",
        f"Total Revenue: {format_currency(float(kpis['total_revenue']))}",
        f"Total Transactions: {int(kpis['total_transactions']):,}",
        f"Total Products: {int(kpis['total_products']):,}",
        f"Total Countries: {int(kpis['total_countries']):,}",
        f"Average Order Value: {format_currency(float(kpis['average_order_value']))}",
        "",
        "Key Insights:",
    ]
    lines.extend(f"- {insight}" for insight in generate_business_insights(df))
    return lines


def export_business_insights(df: pd.DataFrame, output_path: str | Path) -> Path:
    """Export business insights to a plain text report."""
    return write_lines(output_path, build_insight_report_lines(df))

