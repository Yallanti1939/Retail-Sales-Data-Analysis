-- Business analysis queries for RetailSalesDB.
USE RetailSalesDB;

-- 1. Total revenue.
SELECT SUM(TotalSales) AS total_revenue
FROM transactions;

-- 2. Total transactions.
SELECT COUNT(DISTINCT TransactionID) AS total_transactions
FROM transactions;

-- 3. Total countries.
SELECT COUNT(DISTINCT Country) AS total_countries
FROM transactions;

-- 4. Total products.
SELECT COUNT(DISTINCT ItemCode) AS total_products
FROM transactions;

-- 5. Average order value.
SELECT SUM(TotalSales) / COUNT(DISTINCT TransactionID) AS average_order_value
FROM transactions;

-- 6. Monthly sales.
SELECT Year, Month, SUM(TotalSales) AS revenue
FROM transactions
GROUP BY Year, Month
ORDER BY Year, Month;

-- 7. Quarterly sales.
SELECT Year, Quarter, SUM(TotalSales) AS revenue
FROM transactions
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

-- 8. Country-wise revenue.
SELECT Country, SUM(TotalSales) AS revenue
FROM transactions
GROUP BY Country
ORDER BY revenue DESC;

-- 9. Product-wise revenue.
SELECT ItemCode, ItemDescription, SUM(TotalSales) AS revenue
FROM transactions
GROUP BY ItemCode, ItemDescription
ORDER BY revenue DESC;

-- 10. Top 10 products.
SELECT ItemCode, ItemDescription, SUM(TotalSales) AS revenue
FROM transactions
GROUP BY ItemCode, ItemDescription
ORDER BY revenue DESC
LIMIT 10;

-- 11. Top 10 countries.
SELECT Country, SUM(TotalSales) AS revenue
FROM transactions
GROUP BY Country
ORDER BY revenue DESC
LIMIT 10;

-- 12. Peak shopping hours.
SELECT Hour, COUNT(DISTINCT TransactionID) AS transactions
FROM transactions
GROUP BY Hour
ORDER BY transactions DESC;

-- 13. Revenue distribution buckets.
SELECT
    CASE
        WHEN TotalSales < 25 THEN 'Under 25'
        WHEN TotalSales < 100 THEN '25 to 99'
        WHEN TotalSales < 500 THEN '100 to 499'
        ELSE '500+'
    END AS revenue_bucket,
    COUNT(*) AS transaction_lines
FROM transactions
GROUP BY revenue_bucket
ORDER BY transaction_lines DESC;

-- 14. Item purchase frequency.
SELECT ItemCode, ItemDescription, SUM(NumberOfItemsPurchased) AS units_sold
FROM transactions
GROUP BY ItemCode, ItemDescription
ORDER BY units_sold DESC;

