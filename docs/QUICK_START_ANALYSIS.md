# Quick Start: Using the Enhanced Analysis Panel

**File:** `data/final/analysis_panel_enhanced.csv`  
**Ready to use for:** Econometric regression analysis, time series modeling, panel estimation

---

## Quick Load & Explore

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Load the enhanced panel
df = pd.read_csv('data/final/analysis_panel_enhanced.csv')

# Basic info
print(df.info())
print(df.describe())

# Check for missing values
print(df.isnull().sum())

# Plot unemployment vs federal funds rate
plt.figure(figsize=(14, 6))
for state in df['state'].unique()[:5]:  # First 5 states
    state_data = df[df['state'] == state].sort_values('date')
    plt.plot(state_data['date'], state_data['unemployment_rate'], label=state, alpha=0.7)
plt.xlabel('Date')
plt.ylabel('Unemployment Rate (%)')
plt.legend()
plt.show()
```

---

## Structure

**Dimensions:** 20,736 rows × 15 columns

**Panel structure:**
- **48 states** (FL, NE missing): AL, AK, AZ, AR, CA, CO, CT, DE, GA, HI, ID, IL, IN, IA, KS, KY, LA, ME, MD, MA, MI, MN, MS, MO, MT, NV, NH, NJ, NM, NY, NC, ND, OH, OK, OR, PA, RI, SC, SD, TN, TX, UT, VT, VA, WA, WV, WI, WY
- **Time period:** January 1990 - December 2025 (36 years)
- **Frequency:** Monthly
- **Observations per state:** 432 months
- **Format:** Long format (one row per state-month combination)

---

## All Variables

### Unemployment Variables
```python
# Dependent variable (typical)
df['unemployment_rate']              # State unemployment (%)
df['unemployment_yoy_change']        # Year-over-year change
df['unemployment_lagged_1mo']        # Previous month's rate
df['unemployment_volatility_12mo']   # Volatility (12-month rolling SD)
df['national_unemployment_rate']     # National rate (same for all states)
```

### Federal Reserve Variables
```python
# Main regressor (typical)
df['federal_funds_rate']             # Fed target rate (%)
df['fed_rate_change']                # Monthly change in fed rate
df['fed_rate_lagged_1mo']            # Previous month's fed rate
```

### Macroeconomic Conditions
```python
# Common controls
df['inflation_cpi']                  # Consumer Price Index level
df['recession_indicator']            # NBER recession (0=expansion, 1=recession)
df['treasury_10y_yield']             # 10-year Treasury yield (%)
df['labor_force_participation_rate'] # Labor force participation (%)
```

### Employment Indicators
```python
# Supplementary employment data
df['manufacturing_employment_share'] # Manufacturing as % of total employment
```

### Time Identifier
```python
df['date']                           # YYYY-MM-DD format
df['state']                          # Two-letter state code
```

---

## Descriptive Statistics

```python
# Summary statistics
df.describe()

# By state
df.groupby('state')[['unemployment_rate', 'federal_funds_rate']].describe()

# By time period
df.groupby(df['date'].dt.year)[['unemployment_rate', 'federal_funds_rate']].mean()
```

**Expected ranges:**
- Unemployment: 2-15%
- Federal funds: 0-6%
- Inflation (CPI): 100-300 (index level)
- Treasury yield: 1-6%
- Recession: 0 or 1

---

## Common Analyses

### 1. **Simple Correlation Analysis**

```python
# Correlation matrix
correlation = df[['unemployment_rate', 'federal_funds_rate', 
                   'inflation_cpi', 'recession_indicator']].corr()
print(correlation)
```

### 2. **Basic OLS Regression**

```python
from statsmodels.formula.api import ols

# Pooled OLS (ignores state/time structure)
result = ols('unemployment_rate ~ federal_funds_rate + inflation_cpi', 
             data=df).fit()
print(result.summary())
```

### 3. **Fixed Effects Model (State Effects)**

```python
from statsmodels.formula.api import ols

# With state fixed effects
result = ols('unemployment_rate ~ federal_funds_rate + inflation_cpi + C(state)', 
             data=df).fit()
print(result.summary())
```

### 4. **Dynamic Panel Model (Lagged Dependent Variable)**

```python
# Remove state/time with missing dependent variable
df_clean = df.dropna(subset=['unemployment_rate', 'unemployment_lagged_1mo'])

# Regression with lagged dependent variable
result = ols('unemployment_rate ~ unemployment_lagged_1mo + federal_funds_rate', 
             data=df_clean).fit()
print(result.summary())
```

### 5. **Time Series Analysis by State**

```python
# Select one state
ca_data = df[df['state'] == 'CA'].sort_values('date').reset_index(drop=True)

# Plot
plt.figure(figsize=(14, 5))
plt.subplot(1, 2, 1)
plt.plot(ca_data['date'], ca_data['unemployment_rate'])
plt.title('California Unemployment Rate')
plt.xlabel('Date')
plt.ylabel('Unemployment (%)')

plt.subplot(1, 2, 2)
plt.plot(ca_data['date'], ca_data['federal_funds_rate'])
plt.title('Federal Funds Rate')
plt.xlabel('Date')
plt.ylabel('Fed Rate (%)')
plt.tight_layout()
plt.show()
```

### 6. **Recession Period Analysis**

```python
# Filter recession periods only
recession_periods = df[df['recession_indicator'] == 1]

# Average unemployment during recessions:
print(recession_periods.groupby('state')['unemployment_rate'].mean().describe())

# Compare expansion vs recession
df['period'] = df['recession_indicator'].map({0: 'Expansion', 1: 'Recession'})
print(df.groupby('period')[['unemployment_rate', 'federal_funds_rate']].mean())
```

### 7. **Impulse Response Analysis (Simple)**

```python
# Response of unemployment to federal funds rate shock
fig, axes = plt.subplots(2, 2, figsize=(14, 8))

for i, state in enumerate(['CA', 'NY', 'TX', 'FL']):
    ax = axes[i // 2, i % 2]
    state_data = df[df['state'] == state].sort_values('date')
    
    ax.scatter(state_data['fed_rate_change'], 
               state_data['unemployment_yoy_change'], 
               alpha=0.5, s=20)
    ax.set_xlabel('Fed Rate Change')
    ax.set_ylabel('Unemployment YoY Change')
    ax.set_title(f'{state}')
    
    # Add trend line
    z = np.polyfit(state_data['fed_rate_change'].dropna(), 
                   state_data['unemployment_yoy_change'].dropna(), 1)
    p = np.poly1d(z)
    ax.plot(state_data['fed_rate_change'].sort_values(), 
            p(state_data['fed_rate_change'].sort_values()), 
            "r--", alpha=0.8)

plt.tight_layout()
plt.show()
```

### 8. **Panel Regression with Year and State FE**

```python
# Add year and month
df['year'] = pd.to_datetime(df['date']).dt.year
df['month'] = pd.to_datetime(df['date']).dt.month

# Two-way fixed effects (within estimator)
result = ols('unemployment_rate ~ federal_funds_rate + inflation_cpi + C(state) + C(year)', 
             data=df).fit()
print(result.summary())

# Extract fixed effects
state_fe = result.params[result.params.index.str.startswith('C(state)')].sort_values()
print('State Fixed Effects:')
print(state_fe)
```

---

## Handling Missing Data

```python
# Check missing data rates
missing_rates = df.isnull().sum() / len(df) * 100
print(missing_rates[missing_rates > 0])

# Identify rows with key variables
key_vars = ['date', 'state', 'unemployment_rate', 'federal_funds_rate']
df_complete = df.dropna(subset=key_vars)
print(f"Complete cases: {len(df_complete)} / {len(df)} ({100*len(df_complete)/len(df):.1f}%)")

# For analysis, retain but be aware:
# - Treasury 10-year yield: ~64% coverage (not available before 1991)
# - Manufacturing share: ~5% coverage (limited payroll overlap)
# - These can be omitted from analysis if not critical
```

---

## Data Preparation for Regression

```python
# Create analysis dataset
df_analysis = df.copy()

# Select relevant variables
df_analysis = df_analysis[['date', 'state', 'unemployment_rate', 
                           'federal_funds_rate', 'inflation_cpi', 'recession_indicator']]

# Remove states with crucial missing values (if needed)
states_to_include = df_analysis.groupby('state')['unemployment_rate'].apply(
    lambda x: x.notna().sum() > 400  # At least 400 non-missing months
)
df_analysis = df_analysis[df_analysis['state'].isin(states_to_include[states_to_include].index)]

# Create time identifiers
df_analysis['year'] = pd.to_datetime(df_analysis['date']).dt.year
df_analysis['month'] = pd.to_datetime(df_analysis['date']).dt.month
df_analysis['year_month'] = pd.to_datetime(df_analysis['date']).dt.to_period('M')

# Sort for panel structure
df_analysis = df_analysis.sort_values(['state', 'date']).reset_index(drop=True)

print(df_analysis.head(10))
print(f"Shape: {df_analysis.shape}")
print(f"States: {df_analysis['state'].nunique()}")
```

---

## Exporting Results

```python
# Save subset for analysis
df_analysis.to_csv('data/final/analysis_subset.csv', index=False)

# Export regression results
from statsmodels.iolib.summary2 import summary_col

model1 = ols('unemployment_rate ~ federal_funds_rate', data=df).fit()
model2 = ols('unemployment_rate ~ federal_funds_rate + inflation_cpi', data=df).fit()
model3 = ols('unemployment_rate ~ federal_funds_rate + inflation_cpi + C(recession_indicator)', data=df).fit()

summary = summary_col([model1, model2, model3], 
                      names=['Model 1', 'Model 2', 'Model 3'])
print(summary)

# Save to file
with open('results/regression_results.txt', 'w') as f:
    f.write(str(summary))
```

---

## Useful Conversions

```python
# Convert date to datetime if needed
df['date'] = pd.to_datetime(df['date'])

# Extract time components
df['year'] = df['date'].dt.year
df['quarter'] = df['date'].dt.quarter
df['month'] = df['date'].dt.month
df['month_name'] = df['date'].dt.month_name()

# Create lagged variables at state-level (correct way for panel)
df = df.sort_values(['state', 'date'])
df['unemployment_lag1'] = df.groupby('state')['unemployment_rate'].shift(1)
df['unemployment_lag12'] = df.groupby('state')['unemployment_rate'].shift(12)  # 1 year

# Create differences
df['d_unemployment'] = df.groupby('state')['unemployment_rate'].diff()
df['d_fed_rate'] = df['federal_funds_rate'].diff()  # National, no groupby needed
```

---

## Relevant File Paths

```python
# Core files
analysis_panel = 'data/final/analysis_panel_enhanced.csv'
data_dictionary = 'data/final/enhanced_panel_data_dictionary.md'
implementation_guide = 'SUPPLEMENTARY_VARIABLES_IMPLEMENTATION.md'

# Results folder (for saving analysis outputs)
import os
os.makedirs('results/tables', exist_ok=True)
os.makedirs('results/figures', exist_ok=True)
os.makedirs('results/reports', exist_ok=True)
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Florida/Nebraska missing | These states don't have unemployment series in FRED; filter them out |
| Time series misaligned | Remember to `sort_values(['state', 'date'])` before creating lagged vars |
| Missing values in analysis | Use `.dropna(subset=['key_variables'])` before regression |
| Treasury yield mostly NaN | Treasury series sparse before 1991; can exclude if unnecessary |
| Manufacturing share NaN | Very limited data (~20 observations total); use inflation/recession instead |
| State effects not converging | Try centering variables or using within-group estimator |

---

## Next Steps

1. **Exploratory Analysis:** Load data and create descriptive plots
2. **Choose Specification:** Decide on fixed effects, dynamic lag structure
3. **Run Regressions:** Test core hypothesis (Fed rate → Unemployment)
4. **Robustness Checks:** Add controls, try different specifications
5. **Document Results:** Save tables, figures, and interpretation
6. **Present Findings:** Write up analysis with results tables

**Ready to analyze!** 🚀
