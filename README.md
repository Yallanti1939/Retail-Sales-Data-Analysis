# Retail Sales Analysis and Reporting for a Retail Chain

This project analyzes retail transaction data with Python, SQL, Excel, and an
optional Streamlit dashboard. It cleans raw CSV records, creates sales and time
features, generates exploratory analysis tables, exports charts, builds an Excel
dashboard, and produces PDF and PowerPoint report artifacts.

## Project Structure

```text
Retail_Sales_Project/
  data/
    transaction_data.csv
    cleaned_transaction_data.csv
  notebooks/
    data_cleaning.ipynb
    analysis.ipynb
    visualization.ipynb
  sql/
    create_database.sql
    create_tables.sql
    analysis_queries.sql
  src/
    data_loader.py
    data_cleaning.py
    feature_engineering.py
    analysis.py
    visualization.py
    database.py
  dashboard/
    app.py
  reports/
    charts/
    dashboard.xlsx
    final_report.pdf
  presentation/
    project_presentation.pptx
  main.py
  requirements.txt
```

## Dataset Columns

The pipeline expects these business columns:

- `TransactionID`
- `TransactionTime`
- `ItemCode`
- `ItemDescription`
- `NumberOfItemsPurchased`
- `CostPerItem`
- `Country`

The included CSV uses `TransactionId`; the loader normalizes it to
`TransactionID`.

## Setup

Use Python 3.12.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

## Run the Full Pipeline

```powershell
python main.py
```

Outputs:

- `data/cleaned_transaction_data.csv`
- `data/cleaned_retail_data.csv`
- `reports/charts/*.png`
- `reports/business_insights.txt`
- `reports/dashboard.xlsx`
- `reports/insights_report.pdf`
- `reports/final_report.pdf`
- `presentation/project_presentation.pptx`

To also create the MySQL table and insert the cleaned data, configure the
database environment variables first and run:

```powershell
python main.py --load-mysql
```

## Run the Streamlit Dashboard

```powershell
streamlit run dashboard/app.py
```

Dashboard pages:

- Overview
- Product Analysis
- Country Analysis
- Sales Trends
- Business Insights

## MySQL Usage

Create the database and table:

```sql
SOURCE sql/create_database.sql;
SOURCE sql/create_tables.sql;
```

The Python database module reads these environment variables:

- `MYSQL_HOST`
- `MYSQL_PORT`
- `MYSQL_USER`
- `MYSQL_PASSWORD`
- `MYSQL_DATABASE`

Default database name is `RetailSalesDB`.

## Analysis Covered

- Total revenue
- Total transactions
- Total countries
- Total products
- Average order value
- Monthly and quarterly sales
- Country-wise revenue
- Product-wise revenue
- Top 10 products and countries
- Peak shopping hours
- Revenue distribution
- Item purchase frequency
- Business insights and trend summary

## Notes

The existing `venv` in this workspace may not be portable. For reproducible
execution, create a fresh Python 3.12 virtual environment and install from
`requirements.txt`.

To initialize this as a GitHub repository:

```powershell
git init
git add .
git commit -m "Initial retail sales analysis project"
```
