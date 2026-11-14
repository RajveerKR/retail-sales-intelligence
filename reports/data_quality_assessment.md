
# Retail Sales Intelligence
## Data Quality Assessment Report

**Project:** Retail Sales Intelligence & Data Quality Analytics  
**Dataset:** UCI Online Retail II  
**Tools:** Python, Pandas, NumPy  
**Status:** Initial profiling and classification completed

---

## 1. Business Objective

Assess the quality of historical retail transaction data
before using it for SQL analysis and Power BI reporting.

The analysis focuses on missing values, duplicate records,
transaction cancellations, invalid prices, and data
reliability.

## 2. Dataset Overview

| Metric | Result |
|---|---:|
| Total records | 1,067,371 |
| Original columns | 8 |
| Source worksheets | 2 |
| Period | December 2009 - December 2011 |

Original fields:

Invoice, StockCode, Description, Quantity, InvoiceDate,
Price, Customer ID, Country.

## 3. Initial Data Quality Findings

| Issue | Records |
|---|---:|
| Missing Customer IDs | 243,007 |
| Missing descriptions | 4,382 |
| Extra exact duplicate occurrences | 34,335 |
| Negative quantities | 22,950 |
| Zero quantities | 0 |
| Zero prices | 6,202 |
| Negative prices | 5 |

Note: These issue categories overlap.

## 4. Transaction Classification

A Python-based classification process assigned every
record to one mutually exclusive category.

| Category | Records |
|---|---:|
| Positive Sales Candidate | 1,041,670 |
| Cancelled Invoice - Negative Quantity | 19,493 |
| Negative Quantity - Investigation Required | 3,457 |
| Zero Price Transaction | 2,745 |
| Negative Price - Investigation Required | 5 |
| Other Cancelled Invoice | 1 |

**Total classified:** 1,067,371 records.

Classification counts depend on rule priority.
Individual records may have multiple quality issues.

## 5. Positive Sales Quality Assessment

Further investigation of positive sales candidates found:

| Metric | Result |
|---|---:|
| Positive sales candidate rows | 1,041,670 |
| Missing Customer IDs | 236,121 |
| Missing descriptions | 0 |
| Extra duplicate occurrences | 33,757 |
| Unique invoices | 40,077 |

These are candidate sales, not verified net sales.

## 6. Key Business Findings

### Missing Customer Information

Some positive sales have missing Customer IDs.

Decision:
- Retain eligible records for aggregate sales analysis.
- Exclude unidentified customers from analyses requiring
  customer identity.
- Report customer-data completeness separately.

### Negative Quantities

Negative quantities are not always customer returns.

Examples in the dataset include descriptions such as
"lost", "damages", and "short".

Decision:
- Separate cancellations from other negative quantities.
- Investigate stock adjustments independently.
- Do not automatically treat every negative value as a return.

### Duplicate Records

Identical-looking transaction lines may represent
legitimate repeated purchases or recording errors.

Decision:
- Preserve the original records.
- Flag potential duplicates.
- Compare reporting scenarios with and without them.
- Do not automatically remove duplicate-looking records.

### Zero and Negative Prices

Price anomalies require investigation.

Decision:
- Exclude non-positive prices from positive sales
  candidate calculations.
- Preserve the excluded records for audit purposes.

## 7. Duplicate Revenue Sensitivity

| Metric | Result |
|---|---:|
| Extra duplicate occurrences | 33,757 |
| Invoices containing duplicate groups | 5,086 |
| Baseline candidate revenue | GBP 20,972,594.57 |
| Revenue from extra occurrences | GBP 496,334.12 |
| Deduplicated scenario revenue | GBP 20,476,260.45 |
| Potential difference | 2.37% |

The difference is a sensitivity estimate, not proof
that reported revenue was overstated.

## 8. Validation

The Python pipeline successfully:

- Processed 1,067,371 records.
- Reconciled transaction classification counts.
- Generated intermediate Parquet and CSV outputs.
- Passed five automated data quality tests.

## 9. Current Limitations

- Exact duplicates cannot be proven erroneous without
  additional source-system information.
- Returns and cancellations are not fully reconciled.
- Aggregate candidate revenue is not audited net revenue.
- Customer-level analysis is limited by missing IDs.
- Dataset values represent historical transactions.

## 10. Next Steps

1. Prepare reporting-ready transaction tables.
2. Develop SQL tables and analytical queries.
3. Create validated business KPI definitions.
4. Build a Power BI sales performance dashboard.
5. Test and document dashboard results.
6. Publish the final project portfolio.

---

**Data Source:** UCI Machine Learning Repository,
Online Retail II.

https://archive.ics.uci.edu/dataset/502/online+retail+ii

**Project Type:** Independent practical portfolio project.
