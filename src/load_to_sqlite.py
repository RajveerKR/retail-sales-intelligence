
from pathlib import Path
import sqlite3
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "retail_reporting.parquet"
)

DATABASE_FILE = (
    BASE_DIR / "data" / "processed"
    / "retail_analytics.db"
)


def load_to_database():
    """Load reporting data into SQLite."""

    if not INPUT_FILE.exists():
        raise FileNotFoundError(
            f"Reporting dataset not found: {INPUT_FILE}"
        )

    # Load the validated reporting dataset
    df = pd.read_parquet(INPUT_FILE)

    print(f"Loaded {len(df):,} reporting records")

    # Prepare SQLite-compatible data types
    df["ReportingDate"] = pd.to_datetime(
        df["ReportingDate"], errors="coerce"
    ).dt.strftime("%Y-%m-%d %H:%M:%S")

    df["InvoiceDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    ).dt.strftime("%Y-%m-%d %H:%M:%S")

    # Store identifiers as strings
    df["Invoice"] = df["Invoice"].astype("string")
    df["StockCode"] = df["StockCode"].astype("string")
    df["Customer ID"] = df["Customer ID"].astype("string")

    # Convert pandas extension types for SQLite
    for col in df.select_dtypes(include=["boolean"]).columns:
        df[col] = df[col].astype("Int64")

    # Replace remaining pandas missing values with SQL NULL
    df = df.astype(object).where(pd.notna(df), None)

    DATABASE_FILE.parent.mkdir(
        parents=True, exist_ok=True
    )

    # Create database and load table
    with sqlite3.connect(DATABASE_FILE) as conn:
        df.to_sql(
            "retail_transactions",
            conn,
            if_exists="replace",
            index=False,
            chunksize=10000
        )

        # Create indexes for common analytical queries
        conn.execute(
            "CREATE INDEX idx_invoice "
            "ON retail_transactions (Invoice)"
        )

        conn.execute(
            "CREATE INDEX idx_yearmonth "
            "ON retail_transactions (YearMonth)"
        )

        conn.execute(
            'CREATE INDEX idx_customer '
            'ON retail_transactions ("Customer ID")'
        )

        count = conn.execute(
            "SELECT COUNT(*) FROM retail_transactions"
        ).fetchone()[0]

    assert count == len(df), "Database row count mismatch"

    print("\nSQLite database created successfully!")
    print(f"Database: {DATABASE_FILE}")
    print(f"Table: retail_transactions")
    print(f"Rows inserted: {count:,}")


if __name__ == "__main__":
    load_to_database()
