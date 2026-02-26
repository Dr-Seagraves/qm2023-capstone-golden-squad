# Enhanced Analysis Panel - Final Data Dictionary

Generated: 2026-02-24T23:22:23.082230

## Panel Summary

- **Observations:** 20,736
- **States:** 48
- **Time Period:** 1990-01-01 to 2025-12-01
- **Variables:** 15

## All Variables in Panel

| # | Variable | Type | Description |
|---|----------|------|-------------|
| 1 | date | Date | YYYY-MM-DD format |
| 2 | state | State | State abbreviation (AL-WY) |
| 3 | unemployment_rate | Unemployment Rate | State unemployment (%) |
| 4 | national_unemployment_rate | National Unemployment | US unemployment (%) |
| 5 | federal_funds_rate | Federal Funds Rate | Target rate (%) |
| 6 | manufacturing_employment_share | Mfg Employment Share | Mfg as % of total |
| 7 | labor_force_participation_rate | Labor Force Participation | Participation rate (%) |
| 8 | inflation_cpi | Inflation | CPI index |
| 9 | recession_indicator | Recession Indicator | NBER recession (0/1) |
| 10 | treasury_10y_yield | 10-Year Treasury | Yield (%) |
| 11 | unemployment_yoy_change | Unemployment YoY Change | Change from prior year (pp) |
| 12 | fed_rate_change | Fed Rate Change | Monthly change (pp) |
| 13 | unemployment_lagged_1mo | Unemployment Lagged | Previous month (%) |
| 14 | fed_rate_lagged_1mo | Fed Rate Lagged | Previous month (%) |
| 15 | unemployment_volatility_12mo | Unemployment Volatility | 12-month rolling std dev |

## Data Quality Summary

| Variable | Missing | % Missing | Min | Mean | Max |
|----------|---------|-----------|-----|------|-----|
| unemployment_rate | 48 | 0.2% | 1.70 | 5.29 | 30.50 |
| national_unemployment_rate | 48 | 0.2% | 3.40 | 5.68 | 14.80 |
| federal_funds_rate | 0 | 0.0% | 0.05 | 2.88 | 8.29 |
| manufacturing_employment_share | 19,776 | 95.4% | 0.00 | 0.00 | 0.00 |
| labor_force_participation_rate | 48 | 0.2% | 60.10 | 64.87 | 67.30 |
| inflation_cpi | 48 | 0.2% | 127.50 | 209.99 | 326.03 |
| recession_indicator | 0 | 0.0% | 0.00 | 0.08 | 1.00 |
| treasury_10y_yield | 7,440 | 35.9% | 0.62 | 4.22 | 9.08 |
| unemployment_yoy_change | 672 | 3.2% | -22.90 | -0.04 | 26.40 |
| fed_rate_change | 1 | 0.0% | -0.96 | -0.00 | 0.70 |
| unemployment_lagged_1mo | 96 | 0.5% | 1.70 | 5.30 | 30.50 |
| fed_rate_lagged_1mo | 1 | 0.0% | 0.05 | 2.88 | 8.29 |
| unemployment_volatility_12mo | 48 | 0.2% | 0.00 | 0.35 | 9.56 |

## Econometric Ready

✓ Panel structure: Long format (state-month observations)
✓ Balanced time dimension: All states have same dates
✓ Lagged variables: Available for dynamic analysis
✓ National regressors: Federal funds, inflation, recession
✓ State-time heterogeneity: Ready for fixed effects

