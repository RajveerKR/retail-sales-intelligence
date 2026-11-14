
from pathlib import Path
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

AUDIT_FILE = (
    BASE_DIR / "data" / "processed"
    / "retail_classified.parquet"
)

SALES_FILE = (
    BASE_DIR / "data" / "processed"
    / "sales_candidates.csv"
)

EXPECTED_ROWS = 1_067_371
EXPECTED_SALES_ROWS = 1_041_670

EXPECTED_CATEGORIES = {
    "Positive Sales Candidate": 1_041_670,
    "Cancelled Invoice - Negative Quantity": 19_493,
    "Negative Quantity - Investigation Required": 3_457,
    "Zero Price Transaction": 2_745,
    "Negative Price - Investigation Required": 5,
    "Other Cancelled Invoice": 1,
}


def run_tests():
    assert AUDIT_FILE.exists(), "Audit file missing"
    assert SALES_FILE.exists(), "Sales file missing"

    # Load processed datasets
    audit = pd.read_parquet(AUDIT_FILE)

    sales = pd.read_csv(
        SALES_FILE,
        dtype={"Invoice": "string"},
        low_memory=False
    )

    # Test 1: Check record counts
    assert len(audit) == EXPECTED_ROWS
    assert len(sales) == EXPECTED_SALES_ROWS

    print("PASS: Record counts match expected results")

    # Test 2: Check classification reconciliation
    actual_categories = (
        audit["TransactionType"]
        .value_counts()
        .to_dict()
    )

    assert actual_categories == EXPECTED_CATEGORIES

    print("PASS: Transaction classification reconciles")

    # Test 3: Check positive sales conditions
    assert (sales["Quantity"] > 0).all()
    assert (sales["Price"] > 0).all()

    assert (
        ~sales["IsCancelled"]
    ).all()

    print("PASS: Sales candidates meet basic conditions")

    # Test 4: Check calculated line revenue
    expected_revenue = (
        sales["Quantity"] * sales["Price"]
    )

    assert (
        (sales["LineRevenue"] - expected_revenue)
        .abs()
        .lt(0.000001)
        .all()
    )

    print("PASS: Line revenue calculations match")

    # Test 5: Check required numerical fields
    assert sales["Quantity"].notna().all()
    assert sales["Price"].notna().all()

    print("PASS: Required numerical fields are present")

    print("\nALL DATA QUALITY TESTS PASSED")


if __name__ == "__main__":
    run_tests()
