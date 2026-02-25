# Supplementary Variables Implementation Guide

## Successfully Fetched Variables (from FRED)

### M1 Core Variables
1. **Federal Funds Rate** - FEDFUNDS (national, monthly)
2. **National Unemployment Rate** - UNRATE (national, monthly)
3. **State Unemployment Rates** - [ST]UR (50 states, monthly, 48 available)

### M2+ Supplementary Variables (Successfully Fetched)
4. **Inflation Rate** - CPIAUCSL (Consumer Price Index, monthly)
5. **Recession Indicator** - USRECD (NBER official recession dates, monthly binary)
6. **10-Year Treasury Yield** - DGS10 (%, monthly)

---

## Additional Supplementary Variables (Derived or Calculated)

### 7. Manufacturing Employment Share
**Source**: BLS via FRED
**Method**: 
- Calculate as: (Manufacturing Employment / Total Non-farm Employment) × 100
- Can use national-level data: MMNRNJ / PAYEMS
- Or source from individual state BLS reports

**Implementation**:
```python
# National manufacturing employment share
mfg_employment = fred.get_series('MMNRNJ')  # Manufacturing employment
total_employment = fred.get_series('PAYEMS')  # Total non-farm payroll
mfg_share = (mfg_employment / total_employment) * 100
```

### 8. Construction Employment Share
**Source**: BLS via FRED
**Method**: 
- Calculate as: (Construction Employment / Total Non-farm Employment) × 100
- Use: COMPU / PAYEMS at national level

**Implementation**:
```python
construction_employment = fred.get_series('COMPU')  # Construction employment
construction_share = (construction_employment / total_employment) * 100
```

### 9. State Labor Force Participation Rate
**Source**: BLS Labor Force Statistics
**Formula**: (Labor Force / Civilian Non-institutional Population) × 100
**Availability**: Limited in FRED for state level
**Alternative**: Use national CIVPART from FRED for all states as proxy

```python
# National labor force participation rate
lfpr = fred.get_series('CIVPART')  # %
```

### 10. Real Personal Income Per Capita Growth Rate
**Source**: BEA via FRED
**Notes**: 
- Annual data, need to interpolate to monthly
- Series: A229RX0 (National) or state-specific codes

```python
# National real personal income
real_income = fred.get_series('A229RX0')  # Chained 2012 dollars
# Calculate YoY growth rate
income_growth = real_income.pct_change(12) * 100
```

---

## FRED Series Codes Reference

| Variable | National FRED Code | Type | Frequency |
|----------|-------------------|------|-----------|
| Federal Funds Rate | FEDFUNDS | % | Monthly |
| Unemployment Rate | UNRATE | % | Monthly |
| CPI Inflation | CPIAUCSL | Index | Monthly |
| Recession Indicator | USRECD | 0/1 Binary | Monthly |
| 10-Year Treasury | DGS10 | % | Monthly |
| Nonfarm Payroll | PAYEMS | Thousands | Monthly |
| Manufacturing Emp | MMNRNJ | Thousands | Monthly |
| Construction Emp | COMPU | Thousands | Monthly |
| Labor Force Part | CIVPART | % | Monthly |
| Real Personal Inc | A229RX0 | 2012 $ | Annual |

---

## Updated Implementation Plan

### Phase 1: Current Analysis Panel (✓ Complete)
- Core M1 variables: Unemployment, Federal Funds Rate
- Supplementary: Inflation, Recession Indicator, Treasury Yield

### Phase 2: Enhanced Panel (Recommended)
1. Add manufacturing/construction employment shares (national or derived)
2. Calculate income growth rates from available data
3. Add lagged variables for econometric analysis
4. Calculate volatility/standard deviation over rolling windows

### Phase 3: Advanced Analysis (Optional)
1. Source state-level employment data from BLS directly
2. Calculate state-specific labor force participation
3. Add regional indicators
4. Implement leading/coinciding indicators

---

## How to Add Supplementary Variables to Your Analysis

### Simple Approach: Use National Aggregates
```python
import pandas as pd
from fredapi import Fred

fred = Fred(api_key='YOUR_API_KEY')

# Load your existing panel
panel = pd.read_csv('data/final/analysis_panel.csv')
panel['date'] = pd.to_datetime(panel['date'])

# Add manufacturing employment share
mfg = fred.get_series('MMNRNJ')  # Manufacturing
total = fred.get_series('PAYEMS')  # Total
emp_share = (mfg / total) * 100

# Merge into panel
emp_share_df = pd.DataFrame({
    'date': emp_share.index,
    'manufacturing_share': emp_share.values
})
emp_share_df['date'] = pd.to_datetime(emp_share_df['date'])

panel = panel.merge(emp_share_df, on='date', how='left')

# Save updated panel
panel.to_csv('data/final/analysis_panel_enhanced.csv', index=False)
```

### Moderate Approach: Calculate Derived Variables
```python
# Add growth rates
panel['federal_funds_lagged'] = panel.groupby('state')['federal_funds_rate'].shift(1)
panel['unemployment_change'] = panel.groupby('state')['unemployment_rate'].diff()

# Add rolling averages for volatility
panel['unemployment_volatility'] = (
    panel.groupby('state')['unemployment_rate']
    .rolling(window=12)
    .std()
    .reset_index(drop=True)
)

# Save
panel.to_csv('data/final/analysis_panel_enhanced.csv', index=False)
```

---

## Next Steps for Your Capstone

1. **Use Current Panel**: `analysis_panel.csv` is ready with core + 3 supplementary variables
2. **Add Employment Shares**: Run the code snippets above to add manufacturing/construction
3. **Calculate Growth Rates**: Create year-over-year changes and growth metrics
4. **Econometric Analysis**: Run panel regressions with these variables
5. **Document References**: Cite BLS and FRED as data sources

---

## Troubleshooting

**Problem**: "Series does not exist" for state-level employment
**Solution**: Use national-level aggregates replicated to all states in the panel

**Problem**: "Date mismatch" when merging new variables
**Solution**: Ensure both dataframes use same date format (datetime, YYYY-MM-DD)

**Problem**: "Annual data not matching monthly"
**Solution**: Use `pandas.DataFrame.asfreq('MS').interpolate()` for interpolation

---

## Resources

- **FRED API**: https://fred.stlouisfed.org/docs/api/
- **FRED Browse**: https://fred.stlouisfed.org/
- **BLS Data Tools**: https://www.bls.gov/data/
- **Bureau of Economic Analysis**: https://www.bea.gov/

