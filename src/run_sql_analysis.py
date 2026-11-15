
from pathlib import Path
import sqlite3
import pandas as pd

BASE_DIR = Path(__file__).resolve().parent.parent

DB_FILE = (
    BASE_DIR / "data" / "processed"
    / "retail_analytics.db"
)

SQL_FILE = BASE_DIR / "sql" / "sales_analysis.sql"

if not DB_FILE.exists():
    raise FileNotFoundError(
        "SQLite database missing. Run load_to_sqlite.py first."
    )

sql_text = SQL_FILE.read_text(encoding="utf-8")

# Split our SQL file into individual statements
queries = [
    query.strip()
    for query in sql_text.split(";")
    if query.strip()
]

with sqlite3.connect(DB_FILE) as conn:
    for i, query in enumerate(queries, start=1):
        result = pd.read_sql_query(query, conn)

        print(f"\n{'=' * 55}")
        print(f"QUERY {i}")
        print(f"{'=' * 55}")

        print(result.to_string(index=False, max_rows=15))
