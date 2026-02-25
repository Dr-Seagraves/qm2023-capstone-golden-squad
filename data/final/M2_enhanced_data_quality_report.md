# Data Quality Report - Enhanced Panel (M1 + M2+)

Generated: 2026-02-25T19:34:30.228699

## Panel Overview

- **Total Observations:** 20,736
- **Number of States:** 48
- **Number of Time Periods:** 432
- **Date Range:** 1990-01-01 to 2025-12-01
- **Number of Variables:** 13

## Variables Included

### Core Variables (M1)
- date: Month identifier
- state: State abbreviation
- unemployment_rate: State unemployment (%)
- national_unemployment_rate: US unemployment (%)
- federal_funds_rate: Federal Funds Rate (%)

### National Supplementary Variables (M2+)
- inflation_cpi: CPI inflation (index)
- recession_indicator: NBER recession indicator (0/1)
- treasury_10y_yield: 10-Year Treasury Yield (%)

### State-Level Supplementary Variables (M2+)
## Missing Values

| Variable | Missing | Pct. Missing |
|---|---|---|
| unemployment_rate | 48 | 0.23% |
| federal_funds_rate | 0 | 0.00% |
| national_unemployment_rate | 48 | 0.23% |
| inflation_cpi | 48 | 0.23% |
| recession_indicator | 0 | 0.00% |
| treasury_10y_yield | 7,440 | 35.88% |
| total_nonfarm_employment | 9,216 | 44.44% |
| civilian_labor_force | 9,216 | 44.44% |
| total_private_employment | 9,216 | 44.44% |
| manufacturing_employment | 9,216 | 44.44% |
| cpi | 9,216 | 44.44% |

## Summary Statistics

### Core Variables

**unemployment_rate:**
- Mean: 5.29
- Std Dev: 1.98
- Min: 1.70
- Max: 30.50

**national_unemployment_rate:**
- Mean: 5.68
- Std Dev: 1.74
- Min: 3.40
- Max: 14.80

**federal_funds_rate:**
- Mean: 2.88
- Std Dev: 2.34
- Min: 0.05
- Max: 8.29

## Panel Structure

✓ **Balanced Panel:** All states have 432 observations

## Data Quality Notes

✓ All data sourced from FRED API (Federal Reserve)
✓ Core M1 variables are complete and balanced
✓ Supplementary M2+ variables may have missing values
✓ National variables merged to all states on date
✓ State variables matched by date and state

