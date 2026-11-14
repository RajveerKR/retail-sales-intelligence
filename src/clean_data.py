
from pathlib import Path
import pandas as pd
import numpy as np

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
RAW_FILE = BASE_DIR / "data" / "raw" / "online_retail_II.xlsx"
OUTPUT_DIR = BASE_DIR / "data" / "processed"


def load_data():
    """Load both historical retail datasets."""
    sheets = pd.read_excel(RAW_FILE, sheet_name=None)

    df = pd.concat(
        sheets.values(),
        ignore_index=True
    )

    print(f"Loaded {len(df):,} raw records")
    return df


def prepare_data(df):
    """Standardise fields without deleting source records."""
    result = df.copy()

    # Standardise identifiers
    result["Invoice"] = (
        result["Invoice"].astype("string").str.strip()
    )
    result["StockCode"] = (
        result["StockCode"].astype("string").str.strip()
    )

    # Normalise text fields
    result["Description"] = (
        result["Description"].astype("string").str.strip()
    )
    result["Country"] = (
        result["Country"].astype("string").str.strip()
    )

    # Validate numeric and date fields
    result["Quantity"] = pd.to_numeric(
        result["Quantity"], errors="coerce"
    )
    result["Price"] = pd.to_numeric(
        result["Price"], errors="coerce"
    )
    result["InvoiceDate"] = pd.to_datetime(
        result["InvoiceDate"], errors="coerce"
    )

    # Customer IDs remain missing when unknown
    result["Customer ID"] = pd.to_numeric(
        result["Customer ID"], errors="coerce"
    ).astype("Int64")

    return result


def classify_transactions(df):
    """Assign mutually exclusive analysis categories."""
    result = df.copy()

    cancelled = (
        result["Invoice"]
        .str.upper()
        .str.startswith("C")
        .fillna(False)
    )

    quantity = result["Quantity"]
    price = result["Price"]

    conditions = [
        cancelled & (quantity < 0),
        cancelled,
        (quantity < 0) & ~cancelled,
        price < 0,
        price == 0,
        (quantity > 0) & (price > 0)
    ]

    categories = [
        "Cancelled Invoice - Negative Quantity",
        "Other Cancelled Invoice",
        "Negative Quantity - Investigation Required",
        "Negative Price - Investigation Required",
        "Zero Price Transaction",
        "Positive Sales Candidate"
    ]

    result["TransactionType"] = np.select(
        conditions,
        categories,
        default="Other - Investigation Required"
    )

    # Flags preserve information about overlapping issues
    result["IsCancelled"] = cancelled
    result["MissingCustomerID"] = result["Customer ID"].isna()
    result["MissingDescription"] = result["Description"].isna()
    result["IsDuplicateCandidate"] = result.duplicated(
        subset=[
            "Invoice", "StockCode", "Description",
            "Quantity", "InvoiceDate", "Price",
            "Customer ID", "Country"
        ],
        keep=False
    )

    return result


def save_outputs(df):
    """Save audit data and sales candidates."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    audit_file = OUTPUT_DIR / "retail_classified.parquet"
    sales_file = OUTPUT_DIR / "sales_candidates.csv"

    df.to_parquet(audit_file, index=False)

    sales = df[
        df["TransactionType"] == "Positive Sales Candidate"
    ].copy()

    sales["LineRevenue"] = (
        sales["Quantity"] * sales["Price"]
    )

    sales.to_csv(sales_file, index=False)

    print(f"Audit file: {audit_file}")
    print(f"Sales file: {sales_file}")
    print(f"Sales candidate rows: {len(sales):,}")


def main():
    raw = load_data()
    prepared = prepare_data(raw)
    classified = classify_transactions(prepared)

    print("\nTransaction classification:")
    print(classified["TransactionType"].value_counts())

    assert len(raw) == len(classified), (
        "Record count changed during preparation!"
    )

    save_outputs(classified)
    print("\nPipeline completed successfully.")


if __name__ == "__main__":
    main()
