# M1 Data Quality Report
Generated: 2026-02-24T23:10:01.656757

## Panel Overview
- **Total Observations:** 20,736
- **Number of States:** 48
- **Number of Time Periods:** 432
- **Date Range:** 1990-01-01 to 2025-12-01
- **Variables:** date, state, unemployment_rate, national_unemployment_rate, federal_funds_rate

## Missing Values

| Variable | Missing | Pct. Missing |
|---|---|---|
| unemployment_rate | 48 | 0.23% |
| national_unemployment_rate | 48 | 0.23% |
| federal_funds_rate | 0 | 0.00% |

## Summary Statistics

### Unemployment Rate (State-Level)
- **Mean:** 5.29%
- **Std Dev:** 1.98%
- **Min:** 1.70% (Date: 2023-05-01)
- **Max:** 30.50% (Date: 2020-04-01)

### National Unemployment Rate
- **Mean:** 5.68%
- **Std Dev:** 1.74%
- **Min:** 3.40%
- **Max:** 14.80%

### Federal Funds Rate
- **Mean:** 2.88%
- **Std Dev:** 2.34%
- **Min:** 0.05%
- **Max:** 8.29%

## Panel Structure Verification

✓ **Balanced Panel:** All states have same number of observations
  - Observations per state: 432

## Data Quality Notes

✓ Data sourced directly from FRED API (Federal Reserve)
✓ Unemployment rates are monthly averages in percentages
✓ Federal Funds Rate is primary credit rate, monthly average
✓ No data imputation; missing values removed at merge stage
