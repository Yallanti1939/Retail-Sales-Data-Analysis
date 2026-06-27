"""MySQL database utilities for the retail sales project."""

from __future__ import annotations

import os
from dataclasses import dataclass

import pandas as pd
from sqlalchemy import URL, create_engine, text
from sqlalchemy.engine import Engine


@dataclass(frozen=True)
class DatabaseConfig:
    """Database connection configuration loaded from environment variables."""

    host: str = os.getenv("MYSQL_HOST", "localhost")
    port: int = int(os.getenv("MYSQL_PORT", "3306"))
    user: str = os.getenv("MYSQL_USER", "root")
    password: str = os.getenv("MYSQL_PASSWORD", "")
    database: str = os.getenv("MYSQL_DATABASE", "RetailSalesDB")


def create_mysql_engine(config: DatabaseConfig | None = None) -> Engine:
    """Create a SQLAlchemy engine for MySQL."""
    cfg = config or DatabaseConfig()
    url = URL.create(
        "mysql+pymysql",
        username=cfg.user,
        password=cfg.password,
        host=cfg.host,
        port=cfg.port,
        database=cfg.database,
    )
    return create_engine(url, pool_pre_ping=True)


def initialize_database(engine: Engine) -> None:
    """Create the transactions table if it does not already exist."""
    ddl = """
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
    """
    with engine.begin() as connection:
        connection.execute(text(ddl))


def insert_transactions(df: pd.DataFrame, engine: Engine) -> None:
    """Insert cleaned transaction data into MySQL."""
    columns = [
        "TransactionID",
        "TransactionTime",
        "ItemCode",
        "ItemDescription",
        "NumberOfItemsPurchased",
        "CostPerItem",
        "Country",
        "TotalSales",
        "Year",
        "Month",
        "Quarter",
        "Day",
        "Hour",
    ]
    df[columns].to_sql(
        "transactions",
        con=engine,
        if_exists="append",
        index=False,
        chunksize=5000,
    )
