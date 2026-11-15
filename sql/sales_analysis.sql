
-- Retail Sales Intelligence
-- Initial SQL Business Analysis
-- Source: UCI Online Retail II

-- 1. Check total records
SELECT COUNT(*) AS total_records
FROM retail_transactions;


-- 2. Check reporting classifications
SELECT
    ReportingScenario,
    COUNT(*) AS record_count
FROM retail_transactions
GROUP BY ReportingScenario
ORDER BY record_count DESC;


-- 3. Calculate gross sales-candidate revenue
SELECT
    ROUND(SUM(LineAmount), 2) AS gross_sales_candidate_revenue
FROM retail_transactions
WHERE ReportingScenario = 'Gross Sales Candidate';


-- 4. Monthly sales-candidate revenue
SELECT
    YearMonth,
    ROUND(SUM(LineAmount), 2) AS revenue,
    COUNT(DISTINCT Invoice) AS unique_invoices
FROM retail_transactions
WHERE ReportingScenario = 'Gross Sales Candidate'
GROUP BY YearMonth
ORDER BY YearMonth;


-- 5. Top 10 products by sales-candidate revenue
SELECT
    StockCode,
    Description,
    SUM(Quantity) AS units_sold,
    ROUND(SUM(LineAmount), 2) AS revenue
FROM retail_transactions
WHERE ReportingScenario = 'Gross Sales Candidate'
GROUP BY StockCode, Description
ORDER BY revenue DESC
LIMIT 10;


-- 6. Sales-candidate revenue by country
SELECT
    Country,
    COUNT(DISTINCT Invoice) AS invoice_count,
    ROUND(SUM(LineAmount), 2) AS revenue
FROM retail_transactions
WHERE ReportingScenario = 'Gross Sales Candidate'
GROUP BY Country
ORDER BY revenue DESC;


-- 7. Check dataset coverage and reporting dates
SELECT
    MIN(InvoiceDate) AS first_transaction,
    MAX(InvoiceDate) AS last_transaction,
    COUNT(DISTINCT Invoice) AS unique_invoices
FROM retail_transactions
WHERE ReportingScenario = 'Gross Sales Candidate';


-- 8. Investigate non-merchandise charges
SELECT
    StockCode,
    Description,
    COUNT(*) AS transaction_lines,
    ROUND(SUM(LineAmount), 2) AS total_amount
FROM retail_transactions
WHERE ReportingScenario = 'Gross Sales Candidate'
  AND (
      UPPER(Description) LIKE '%POSTAGE%'
      OR UPPER(Description) LIKE '%CARRIAGE%'
      OR UPPER(Description) LIKE '%MANUAL%'
      OR UPPER(Description) LIKE '%BANK CHARGES%'
      OR StockCode IN ('M', 'DOT', 'POST')
  )
GROUP BY StockCode, Description
ORDER BY total_amount DESC;


-- 9. Check duplicate sensitivity in sales data
SELECT
    COUNT(*) AS sales_candidate_rows,
    SUM(CASE WHEN IsDuplicateCandidate = 1
             THEN 1 ELSE 0 END) AS rows_in_duplicate_groups,
    ROUND(SUM(LineAmount), 2) AS baseline_revenue
FROM retail_transactions
WHERE ReportingScenario = 'Gross Sales Candidate';


-- 10. Revenue by business classification
SELECT
    ProductCategory,
    COUNT(*) AS transaction_lines,
    ROUND(SUM(LineAmount), 2) AS revenue
FROM retail_transactions
WHERE ReportingScenario = 'Gross Sales Candidate'
GROUP BY ProductCategory
ORDER BY revenue DESC;
