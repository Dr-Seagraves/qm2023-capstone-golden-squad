# Capstone Project Setup Guide

## Overview

This project compares federal interest rates (Federal Funds Rate) with unemployment rates across all 50 US states. Data is sourced from the Federal Reserve Economic Data (FRED) database via the official FRED API.

## Prerequisites

- Python 3.8+ (3.11.2 recommended)
- FRED API key (free to obtain)
- Internet connection for data download

## Step 1: Get Your FRED API Key

1. Visit: https://fred.stlouisfed.org/docs/api/api_key.html
2. Click "Request API Key" and sign up (free account)
3. You'll receive your 32-character API key via email
4. Save this key somewhere safe

## Step 2: Set Up Your Environment

### Option A: Using Environment Variable (Recommended)

Create a `.env` file in the project root with your API key:

```bash
cd /workspaces/qm2023-capstone-golden-squad
cp .env.example .env
# Edit .env and replace 'your_api_key_here' with your actual key
```

Then run:

```bash
export FRED_API_KEY=$(grep FRED_API_KEY .env | cut -d'=' -f2)
```

### Option B: Command Line Argument

Pass your API key directly when running the script:

```bash
python code/fetch_data.py --api-key YOUR_API_KEY_HERE
```

### Option C: System Environment Variable

```bash
export FRED_API_KEY=YOUR_API_KEY_HERE
```

## Step 3: Fetch Data from FRED

Run the data fetching script:

```bash
python code/fetch_data.py
```

**What this does:**
- Fetches Federal Funds Rate (FEDFUNDS) - monthly from 1990-present
- Fetches National Unemployment Rate (UNRATE) - monthly from 1990-present  
- Fetches Unemployment Rates for all 50 states - monthly from 1990-present
- Saves raw data as CSV files to `data/raw/`

**Expected output:**
```
======================================================================
CAPSTONE PROJECT - FRED DATA FETCHER
======================================================================
Initializing FRED API client...

======================================================================
Fetching Federal Funds Rate (FEDFUNDS)...
  ✓ Fetched 408 observations

Fetching National Unemployment Rate (UNRATE)...
  ✓ Fetched 408 observations

Fetching State Unemployment Rates (50 states)...
  ✓ AL: 408 observations
  ✓ AK: 408 observations
  ...
  ✓ WY: 408 observations

Saving raw data files...
  ✓ federal_funds_rate.csv (408 rows)
  ✓ national_unemployment_rate.csv (408 rows)
  ✓ state_unemployment_rates.csv (20,400 rows)
  ✓ FETCH_METADATA.md

======================================================================
✓ Data fetch completed successfully!
✓ Data saved to: .../data/raw
======================================================================
```

## Step 4: Merge Data Into Analysis Panel

After fetching data, create the analysis-ready panel:

```bash
python code/merge_final_panel.py
```

**What this does:**
- Merges federal funds rate with state unemployment data
- Creates a balanced panel structure
- Validates data quality
- Generates quality report
- Saves final dataset to `data/final/analysis_panel.csv`

**Expected output:**
```
======================================================================
CAPSTONE PROJECT - MERGE DATA INTO ANALYSIS PANEL
======================================================================

Loading raw data files...
  ✓ federal_funds_rate.csv: 408 rows
  ✓ national_unemployment_rate.csv: 408 rows
  ✓ state_unemployment_rates.csv: 20,400 rows

Creating analysis panel...
  Date range: 1990-01-01 to 2026-02-01
  Panel shape: 20,400 observations × 5 variables
  States: 50
  Date range: 1990-01-01 to 2026-02-01

======================================================================
✓ Panel merge completed successfully!
✓ Data saved to: .../data/final
✓ Ready for analysis with 20,400 observations
======================================================================

First 10 observations of analysis panel:
       date state  unemployment_rate  national_unemployment_rate  federal_funds_rate
 1990-01-01    AL              6.17                        5.3                5.86
 1990-01-01    AK              8.47                        5.3                5.86
 1990-01-01    AZ              5.36                        5.3                5.86
 1990-01-01    AR              6.75                        5.3                5.86
 1990-01-01    CA              5.91                        5.3                5.86
 ...
```

## Project Structure

After running the scripts, your directory structure will be:

```
qm2023-capstone-golden-squad/
├── code/
│   ├── config_paths.py           # Centralized path configuration
│   ├── fetch_data.py             # FRED data fetcher (NEW)
│   ├── merge_final_panel.py      # Data merger (NEW)
│   └── ...
├── data/
│   ├── raw/
│   │   ├── federal_funds_rate.csv           # Federal Funds Rate data
│   │   ├── national_unemployment_rate.csv   # National unemployment
│   │   ├── state_unemployment_rates.csv     # All 50 states
│   │   └── FETCH_METADATA.md                # Data fetch documentation
│   ├── processed/
│   │   └── panel_processed.csv              # Intermediate panel
│   └── final/
│       ├── analysis_panel.csv               # Analysis-ready panel
│       └── M1_data_quality_report.md        # Data quality report
├── results/
│   ├── figures/                  # Your visualizations go here
│   ├── tables/                   # Regression tables go here
│   └── reports/                  # Milestone reports go here
└── ...
```

## Data Format

### analysis_panel.csv

The final analysis-ready dataset has the following structure:

```
date,state,unemployment_rate,national_unemployment_rate,federal_funds_rate
1990-01-01,AL,6.17,5.3,5.86
1990-01-01,AK,8.47,5.3,5.86
...
```

**Variables:**
- `date`: Year-Month (YYYY-MM-DD format)
- `state`: US state abbreviation (AL, AK, AZ, ..., WY)
- `unemployment_rate`: State-level unemployment rate (%)
- `national_unemployment_rate`: National unemployment rate (%)
- `federal_funds_rate`: Federal Funds Rate (%)

**Panel Characteristics:**
- **Observations:** 20,400 (50 states × 408 months)
- **Time Period:** January 1990 - Present
- **Frequency:** Monthly
- **Type:** Balanced panel (all states have equal observations)

## Troubleshooting

### Issue: "FRED API key not found"

**Solution:** 
1. Make sure you've obtained a free key at https://fred.stlouisfed.org/docs/api/api_key.html
2. Set the environment variable: `export FRED_API_KEY=your_key_here`
3. Or use the command-line argument: `python code/fetch_data.py --api-key YOUR_KEY`

### Issue: "Connection error" or timeout

**Solution:**
- Check your internet connection
- FRED API might be temporarily unavailable
- Wait a few minutes and try again
- The script has built-in retries, so large datasets may take 5-10 minutes to fetch

### Issue: Some states have fewer observations

**Possible cause:** FRED might not have historical data for all states going back to 1990.

**Solution:**
- Check `FETCH_METADATA.md` in `data/raw/` for details
- The merge process automatically handles this by only using the overlapping date range

### Issue: "Missing module" errors

**Solution:**
```bash
# Reinstall dependencies
pip install -r requirements.txt
```

## Next Steps for Your Capstone

After the data is ready in `data/final/analysis_panel.csv`:

1. **Exploratory Data Analysis (EDA)**
   - Create visualizations for trends over time
   - Examine state-level heterogeneity
   - Check correlation between variables

2. **Econometric Analysis**
   - Fixed effects panel regression
   - Dynamic panel models (if appropriate)
   - Event study analysis

3. **Reporting**
   - Create summary statistics tables
   - Generate regression tables
   - Write interpretation of results

Example analysis in Python:

```python
import pandas as pd
from pathlib import Path

# Load the analysis panel
panel = pd.read_csv('data/final/analysis_panel.csv')
panel['date'] = pd.to_datetime(panel['date'])

# Summary statistics by state
print(panel.groupby('state')['unemployment_rate'].describe())

# Correlation analysis
print(panel[['unemployment_rate', 'federal_funds_rate']].corr())

# Time series plot visualization
import matplotlib.pyplot as plt
panel_national = panel.drop_duplicates(subset=['date'])
fig, ax = plt.subplots(figsize=(12, 6))
ax.plot(panel_national['date'], panel_national['federal_funds_rate'], label='Federal Funds Rate')
ax.set_xlabel('Date')
ax.set_ylabel('Rate (%)')
ax.legend()
plt.savefig('results/figures/federal_funds_trend.png', dpi=300, bbox_inches='tight')
```

## Additional Resources

- **FRED Data Explorer:** https://fred.stlouisfed.org/
- **FRED API Documentation:** https://fred.stlouisfed.org/docs/api/
- **About Federal Funds Rate:** https://fred.stlouisfed.org/series/FEDFUNDS
- **About Unemployment Data:** https://fred.stlouisfed.org/series/UNRATE

## Questions or Issues?

If you encounter any problems:
1. Check the troubleshooting section above
2. Review the metadata files (FETCH_METADATA.md, M1_data_quality_report.md)
3. Check console output for specific error messages
4. Ensure your FRED API key is valid and you have internet access
