
from pathlib import Path
import pandas as pd
import numpy as np

BASE_DIR = Path(__file__).resolve().parent.parent

INPUT_FILE = (
    BASE_DIR / "data" / "processed"
    / "retail_reporting.parquet"
)


def run_tests():
    assert INPUT_FILE.exists(), "Reporting dataset missing"

    df = pd.read_parquet(INPUT_FILE)

    # Test 1: All original records retained
    assert len(df) == 1_067_371
    print("PASS: All original records preserved")

    # Test 2: Reporting scenarios reconcile
    counts = df["ReportingScenario"].value_counts()

    assert counts["Gross Sales Candidate"] == 1_041_670
    assert counts["Review Required"] == 25_701

    print("PASS: Reporting scenarios reconcile")

    # Test 3: Reporting dates are valid
    assert df["ReportingDate"].notna().all()
    assert df["Year"].notna().all()
    assert df["Month"].between(1, 12).all()

    print("PASS: Reporting dates validated")

    # Test 4: Line amount calculation
    expected = df["Quantity"] * df["Price"]

    assert np.allclose(
        df["LineAmount"],
        expected,
        equal_nan=True
    )

    print("PASS: Line amounts validated")

    # Test 5: Positive sales flags agree with scenarios
    positive = df["IsPositiveSale"]

    assert (
        df.loc[positive, "ReportingScenario"]
        == "Gross Sales Candidate"
    ).all()

    assert (
        df.loc[positive, "Quantity"] > 0
    ).all()

    assert (
        df.loc[positive, "Price"] > 0
    ).all()

    print("PASS: Positive sales flags validated")

    print("\nALL REPORTING DATASET TESTS PASSED")


if __name__ == "__main__":
    run_tests()
