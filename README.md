
# 🛒 Retail Sales Intelligence & Data Quality Analytics

### End-to-End Data Analytics | Python | Pandas | SQL | Power BI

![Status](https://img.shields.io/badge/Status-In%20Progress-blue)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Pandas](https://img.shields.io/badge/Pandas-Data%20Processing-purple)
![SQL](https://img.shields.io/badge/SQL-Planned-orange)
![Power BI](https://img.shields.io/badge/Power%20BI-Planned-yellow)

---

## 📌 Project Overview

Retail Sales Intelligence is an independent, end-to-end
data analytics portfolio project designed to demonstrate
practical skills in data cleaning, data quality assessment,
Python automation, SQL analysis, and business intelligence.

The project uses historical retail transactions from the
UCI Machine Learning Repository.

The objective is to transform raw transactional data into
reliable, structured datasets that support accurate sales
reporting and business decision-making.

### 🎯 Business Objectives

- Identify and investigate data quality issues.
- Clean and standardise retail transaction records.
- Analyse missing values and duplicate transactions.
- Identify cancellations and stock adjustments.
- Evaluate the financial impact of duplicate records.
- Prepare reliable data for SQL and Power BI reporting.
- Develop interactive sales and customer dashboards.

---

## 📊 Dataset Information

**Dataset:** Online Retail II

**Source:** UCI Machine Learning Repository

**Period:** December 2009 – December 2011

**Records:** 1,067,371

**Original Columns:** 8

**Dataset Link:**

https://archive.ics.uci.edu/dataset/502/online+retail+ii

### Dataset Fields

| Column | Description |
|---|---|
| Invoice | Transaction invoice identifier |
| StockCode | Product identifier |
| Description | Product description |
| Quantity | Number of units |
| InvoiceDate | Transaction date and time |
| Price | Unit price |
| Customer ID | Customer identifier |
| Country | Customer country |

The original dataset is not included in this
repository. Download it from the official source.

---

## 🏗️ Project Architecture

```text
UCI Online Retail II
        |
        v
Raw Excel Files
        |
        v
Python / Pandas
        |
        v
Data Discovery & Profiling
        |
        v
Data Cleaning & Classification
        |
        v
Data Quality Validation
        |
        v
Processed CSV / Parquet
        |
        v
SQL Analytics (Planned)
        |
        v
Power BI Dashboard (Planned)
```

---

## 🔍 Data Quality Assessment

Initial profiling identified several issues in
the original retail dataset.

| Data Quality Issue | Records |
|---|---:|
| Total records | 1,067,371 |
| Missing Customer IDs | 243,007 |
| Missing descriptions | 4,382 |
| Extra duplicate occurrences | 34,335 |
| Negative quantities | 22,950 |
| Zero-price records | 6,202 |
| Negative-price records | 5 |

These categories may overlap.

### Key Findings

**Missing Customer IDs**

Approximately 22.8% of transaction lines have
missing customer identifiers.

These records are retained where appropriate
for aggregate sales analysis, while customer-level
analysis will account for missing identities.

**Negative Quantities**

Not all negative quantities indicate customer returns.

Some records appear to represent damaged stock,
shortages, or internal inventory adjustments.

**Duplicate Records**

Identical-looking transaction lines require
investigation before removal because some may
represent legitimate repeated purchases.

---

## 🧹 Transaction Classification

A reusable Python pipeline classifies transactions
into categories based on invoice identifiers,
quantities, and prices.

| Transaction Type | Records |
|---|---:|
| Positive Sales Candidate | 1,041,670 |
| Cancelled Invoice - Negative Quantity | 19,493 |
| Negative Quantity - Investigation Required | 3,457 |
| Zero Price Transaction | 2,745 |
| Negative Price - Investigation Required | 5 |
| Other Cancelled Invoice | 1 |

All 1,067,371 records were classified.

Classification rules are provisional and
support further investigation.

---

## 💷 Duplicate Revenue Investigation

A separate Python script investigated the
potential financial effect of extra duplicate
occurrences among positive sales candidates.

### Results

| Metric | Result |
|---|---:|
| Positive sales candidates | 1,041,670 |
| Extra duplicate occurrences | 33,757 |
| Invoices containing duplicate groups | 5,086 |
| Baseline candidate revenue | £20,972,594.57 |
| Deduplicated scenario revenue | £20,476,260.45 |
| Potential revenue difference | £496,334.12 |
| Potential difference (%) | 2.37% |

### Business Insight

Removing all extra exact duplicate-looking records
would reduce candidate revenue by approximately 2.37%.

However, these records have not been confirmed as
errors. They are preserved in the baseline data.

**Important:** These figures represent positive
sales-candidate revenue, not audited net revenue.

---

## 🛠️ Technology Stack

| Area | Technologies |
|---|---|
| Programming | Python 3.11 |
| Data Processing | Pandas, NumPy |
| Data Storage | CSV, Excel, Parquet |
| Data Quality | Python validation scripts |
| Development | VS Code, Jupyter Notebook |
| Version Control | Git, GitHub |
| Database Analytics | SQL — Planned |
| Visualisation | Power BI — Planned |

---

## 📁 Project Structure

```text
retail-sales-intelligence/
|
|-- data/
|   |-- raw/
|   |-- processed/
|
|-- notebooks/
|   |-- 01_data_discovery.ipynb
|
|-- src/
|   |-- clean_data.py
|   |-- analyse_duplicates.py
|
|-- tests/
|   |-- test_data_quality.py
|
|-- reports/
|   |-- data_quality_assessment.md
|   |-- duplicate_investigation.md
|
|-- sql/
|-- dashboard/
|-- screenshots/
|
|-- requirements.txt
|-- .gitignore
|-- README.md
```

Raw datasets and generated processed files
are excluded from GitHub.

---

## ⚙️ How to Run the Project

### 1. Clone the repository

```bash
git clone https://github.com/RajveerKR/retail-sales-intelligence.git

cd retail-sales-intelligence
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

On Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Download the dataset

Download Online Retail II from the UCI repository.

Place the Excel workbook at:

```text
data/raw/online_retail_II.xlsx
```

### 5. Run the data-processing pipeline

```bash
python src/clean_data.py
```

Expected generated files:

- `data/processed/retail_classified.parquet`
- `data/processed/sales_candidates.csv`

### 6. Run automated tests

```bash
python tests/test_data_quality.py
```

The initial five data-quality checks passed
during local development.

### 7. Run duplicate investigation

```bash
python src/analyse_duplicates.py
```

The script calculates duplicate statistics,
revenue sensitivity, and sample records
for further investigation.

---

## ✅ Project Progress

- [x] Project environment setup
- [x] Dataset acquisition
- [x] Data discovery and profiling
- [x] Missing value investigation
- [x] Transaction classification
- [x] Python processing pipeline
- [x] Initial data quality validation
- [x] Duplicate investigation
- [x] Duplicate revenue sensitivity analysis
- [ ] Final reporting dataset preparation
- [ ] SQL database and queries
- [ ] Power BI data modelling
- [ ] Interactive dashboard development
- [ ] Dashboard validation
- [ ] Final portfolio demonstration

---

## 🚀 Planned Dashboard Features

The completed Power BI dashboard is intended to include:

- Sales performance overview
- Monthly and yearly revenue trends
- Top-selling products
- Geographic sales analysis
- Customer behaviour analysis
- Cancellation and return analysis
- Data quality indicators

These dashboard features are planned and have
not yet been implemented.

---

## 📚 Data Source & Attribution

**Online Retail II Dataset**

UCI Machine Learning Repository

https://archive.ics.uci.edu/dataset/502/online+retail+ii

Dataset licence: CC BY 4.0.

This project is an independent educational and
professional portfolio demonstration.

---

## 👩‍💻 Author

**Rajveer Kaur**

Data Analytics | Python | SQL | Power BI | Cloud Engineering

GitHub:
https://github.com/RajveerKR

---

⭐ This project is actively being developed to
demonstrate practical data analytics, data engineering,
quality assurance, and business intelligence skills.
