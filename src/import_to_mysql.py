import pandas as pd
from sqlalchemy import create_engine

# Load CSV
df = pd.read_csv("data/transaction_data.csv")

# Create TotalSales column
df["TotalSales"] = (
    df["NumberOfItemsPurchased"] *
    df["CostPerItem"]
)

# Connect to MySQL
engine = create_engine(
    "mysql+pymysql://root:Saiteja1939@localhost/RetailSalesDB"
)

# Import data
df.to_sql(
    "transactions",
    con=engine,
    if_exists="replace",
    index=False,
    chunksize=10000
)

print("Data imported successfully!")