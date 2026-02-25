# FRED Data Fetch Metadata - Enhanced
Generated: 2026-02-25T19:17:00.314530

## Original M1 Data Sources
- Federal Funds Rate: FRED Series FEDFUNDS (monthly)
- National Unemployment Rate: FRED Series UNRATE (monthly)
- State Unemployment Rates: FRED Series [STUUR] (50 states, monthly)

## M2+ Supplementary Variables

### National-Level Variables (All States Combined)
1. Inflation Rate: FRED Series CPIAUCSL (Consumer Price Index, monthly)
2. Recession Indicator: FRED Series USRECD (NBER official indicator, monthly)
3. 10-Year Treasury Yield: FRED Series DGS10 (%, monthly)

### State-Level Supplementary Variables
4. Employment Level: [STEIUVPI] or [STIE9UDH] (thousands, monthly)
5. Labor Force Level: [STDRVUST] (thousands, monthly)
6. Private Employment: [STPREMU] (thousands, monthly - limited states)
7. Manufacturing Employment Share: Derived from employment data
8. Construction Employment Share: Derived from employment data

## Files Generated

### Core Data (M1)
- federal_funds_rate.csv
- national_unemployment_rate.csv
- state_unemployment_rates.csv

### National Supplementary Data
- inflation_cpi.csv
- recession_indicator.csv
- treasury_10y_yield.csv

### State-Level Supplementary Data
- state_employment_level.csv
- state_labor_force_level.csv
- state_private_employment.csv (partial coverage)

## Data Characteristics
- Primary Frequency: Monthly (some annual)
- Time Period: January 1990 - Present
- Data Quality: FRED maintains data quality standards
- Missing Values: Handled in merge_final_panel.py

## Notes on Data Availability
- Some state-level series may have limited historical coverage
- Labor force participation rate not available for all states
- Real personal income is annual, will be interpolated to monthly if needed
- Manufacturing/construction employment shares calculated from payroll totals

## Next Steps
1. Review individual raw data files for quality
2. Run merge_final_panel.py to create analysis-ready dataset
3. Handle missing data appropriately for analysis
