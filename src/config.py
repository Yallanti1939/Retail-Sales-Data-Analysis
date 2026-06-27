"""Central project configuration for paths and database defaults."""

from __future__ import annotations

from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA_DIR = PROJECT_ROOT / "data"
REPORTS_DIR = PROJECT_ROOT / "reports"
CHARTS_DIR = REPORTS_DIR / "charts"
PRESENTATION_DIR = PROJECT_ROOT / "presentation"

RAW_DATA_PATH = DATA_DIR / "transaction_data.csv"
RAW_RETAIL_DATA_PATH = DATA_DIR / "retail_data.csv"
CLEANED_TRANSACTION_DATA_PATH = DATA_DIR / "cleaned_transaction_data.csv"
CLEANED_RETAIL_DATA_PATH = DATA_DIR / "cleaned_retail_data.csv"
BUSINESS_INSIGHTS_PATH = REPORTS_DIR / "business_insights.txt"
EXCEL_DASHBOARD_PATH = REPORTS_DIR / "dashboard.xlsx"
INSIGHTS_REPORT_PATH = REPORTS_DIR / "insights_report.pdf"
FINAL_REPORT_PATH = REPORTS_DIR / "final_report.pdf"
PRESENTATION_PATH = PRESENTATION_DIR / "project_presentation.pptx"

DATABASE_NAME = "RetailSalesDB"

