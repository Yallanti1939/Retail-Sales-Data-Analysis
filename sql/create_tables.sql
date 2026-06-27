-- Create the core transaction table for cleaned retail sales data.
USE RetailSalesDB;

CREATE TABLE IF NOT EXISTS transactions (
    TransactionID BIGINT,
    TransactionTime DATETIME,
    ItemCode VARCHAR(64),
    ItemDescription VARCHAR(255),
    NumberOfItemsPurchased INT,
    CostPerItem DECIMAL(12, 2),
    Country VARCHAR(100),
    TotalSales DECIMAL(14, 2),
    Year INT,
    Month INT,
    Quarter INT,
    Day INT,
    Hour INT
);

CREATE INDEX idx_transactions_time ON transactions (TransactionTime);
CREATE INDEX idx_transactions_country ON transactions (Country);
CREATE INDEX idx_transactions_item ON transactions (ItemCode);

