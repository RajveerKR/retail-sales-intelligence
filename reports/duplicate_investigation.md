
# Duplicate Transaction Investigation

## Retail Sales Intelligence Project

### Objective

Assess the potential financial impact of exact
duplicate-looking transaction records before
deciding whether to remove them.

## Dataset

Source: UCI Online Retail II

Analysis scope: Positive sales candidates

## Investigation Results

| Metric | Result |
|---|---:|
| Sales candidate records | 1,041,670 |
| Extra duplicate occurrences | 33,757 |
| Invoices with duplicate groups | 5,086 |
| Baseline candidate revenue | £20,972,594.57 |
| Revenue from extra duplicates | £496,334.12 |
| Deduplicated scenario revenue | £20,476,260.45 |
| Potential revenue difference | 2.37% |

## Key Findings

Exact duplicate-looking invoice lines were identified
across 5,086 invoices.

Removing extra duplicate occurrences would reduce
the analysed revenue total by approximately 2.37%.

However, identical invoice lines are not necessarily
data-entry errors. They may represent legitimate
repeated transactions.

## Recommended Treatment

1. Preserve original transaction records.
2. Flag duplicate-looking records.
3. Retain duplicates in the baseline scenario.
4. Create a separate deduplicated sensitivity scenario.
5. Avoid claiming financial overstatement without
   further evidence.

## Limitations

- No original transaction-line identifier is available.
- Duplicate records cannot be conclusively classified
  as erroneous using these fields alone.
- Cancellation and return reconciliation is pending.
- Revenue calculations represent sales candidates,
  not final audited net revenue.

## Conclusion

Duplicate investigation completed.

The project will retain the original transaction
records and separately report the potential financial
impact of deduplication.
