
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

SALES_FILE = (
    BASE_DIR / "data" / "processed"
    / "sales_candidates.csv"
)

# Load sales candidates
df = pd.read_csv(
    SALES_FILE,
    dtype={"Invoice": "string", "StockCode": "string"},
    low_memory=False
)

# Define duplicate comparison columns
duplicate_columns = [
    "Invoice",
    "StockCode",
    "Description",
    "Quantity",
    "InvoiceDate",
    "Price",
    "Customer ID",
    "Country"
]

# Identify extra duplicate occurrences
df["IsExtraDuplicate"] = df.duplicated(
    subset=duplicate_columns,
    keep="first"
)

# Identify all rows belonging to duplicate groups
df["InDuplicateGroup"] = df.duplicated(
    subset=duplicate_columns,
    keep=False
)

duplicate_rows = df[df["IsExtraDuplicate"]]

# Calculate revenue impact
total_revenue = df["LineRevenue"].sum()

duplicate_revenue = duplicate_rows["LineRevenue"].sum()

revenue_without_duplicates = (
    total_revenue - duplicate_revenue
)

print("\nDUPLICATE INVESTIGATION")
print("-" * 45)

print(f"Total sales candidate rows: {len(df):,}")

print(
    f"Extra duplicate occurrences: "
    f"{df['IsExtraDuplicate'].sum():,}"
)

print(
    f"Invoices containing duplicate groups: "
    f"{df.loc[df['InDuplicateGroup'], 'Invoice'].nunique():,}"
)

print(f"\nRevenue with duplicates: £{total_revenue:,.2f}")

print(
    f"Revenue from extra duplicate occurrences: "
    f"£{duplicate_revenue:,.2f}"
)

print(
    f"Revenue without extra duplicates: "
    f"£{revenue_without_duplicates:,.2f}"
)

print(
    f"Potential revenue impact: "
    f"{duplicate_revenue / total_revenue * 100:.2f}%"
)

# Save sample evidence for investigation
REPORT_DIR = BASE_DIR / "reports"
REPORT_DIR.mkdir(exist_ok=True)

duplicate_rows.head(100).to_csv(
    REPORT_DIR / "duplicate_samples.csv",
    index=False
)

print("\nDuplicate investigation completed.")
