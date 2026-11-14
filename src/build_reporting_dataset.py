
from pathlib import Path
import pandas as pd

# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "retail_classified.parquet"
)

OUTPUT_DIR = BASE_DIR / "data" / "processed"


def build_reporting_dataset():

    # Load classified transaction data
    df = pd.read_parquet(INPUT_FILE)

    print(f"Loaded {len(df):,} classified records")

    # Create reporting date fields
    df["ReportingDate"] = pd.to_datetime(
        df["InvoiceDate"], errors="coerce"
    )

    df["Year"] = df["ReportingDate"].dt.year
    df["Month"] = df["ReportingDate"].dt.month
    df["YearMonth"] = (
        df["ReportingDate"]
        .dt.strftime("%Y-%m")
    )

    # Calculate line amount for all records
    df["LineAmount"] = (
        df["Quantity"] * df["Price"]
    )

    # Mark positive sales candidates
    df["IsPositiveSale"] = (
        df["TransactionType"]
        == "Positive Sales Candidate"
    )

    # Mark identified customers
    df["HasCustomerID"] = df["Customer ID"].notna()

    # Define reporting scenario
    df["ReportingScenario"] = "Review Required"

    df.loc[
        df["IsPositiveSale"],
        "ReportingScenario"
    ] = "Gross Sales Candidate"

    # Validate that records were preserved
    assert len(df) == 1_067_371

    OUTPUT_DIR.mkdir(
        parents=True, exist_ok=True
    )

    output_file = (
        OUTPUT_DIR / "retail_reporting.parquet"
    )

    df.to_parquet(
        output_file,
        index=False
    )

    print("\nReporting dataset created successfully!")
    print(f"Output: {output_file}")
    print(f"Total records: {len(df):,}")

    print("\nReporting scenarios:")
    print(df["ReportingScenario"].value_counts())


if __name__ == "__main__":
    build_reporting_dataset()
