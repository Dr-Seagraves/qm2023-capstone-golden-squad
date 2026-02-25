[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22639587&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Research Question

**How do interest rates (Federal Funds Rate) affect unemployment rates across the United States over time?**

We analyze the relationship between the national Federal Funds Rate and unemployment rates across all 50 states to identify whether interest rate policy correlates with state-level employment dynamics. While not directly linked, interest rates affect investment, consumer spending, and borrowing costs, which influence unemployment rates.

## Quick Start

### 1. Get Your FRED API Key (5 minutes)
- Visit: [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
- Click "Request API Key" and sign up (free account)
- Save your 32-character key

### 2. Set Your API Key
```bash
# Option A: Create .env file
cp .env.example .env
# Edit .env and replace 'your_api_key_here_replace_this' with your actual key

# Option B: Export as environment variable
export FRED_API_KEY=YOUR_API_KEY_HERE
```

### 3. Fetch Data from FRED
```bash
python code/fetch_data.py
```
This downloads Federal Funds Rate and unemployment data for all 50 states.

### 4. Create Analysis Panel
```bash
python code/merge_final_panel.py
```
This merges raw FRED data into an analysis-ready panel dataset stored in `data/final/analysis_panel.csv`.

**Total time:** ~10-15 minutes depending on internet speed

---

## Project Structure

```
qm2023-capstone-golden-squad/
├── code/
│   ├── config_paths.py              # Centralized path configuration
│   ├── fetch_data.py                # Download data from FRED API
│   ├── merge_final_panel.py         # Create analysis-ready panel
│   ├── fetch_data copy*.py          # (Previous attempts - can be deleted)
│   └── requirements.txt
├── data/
│   ├── raw/                         # Original FRED data (CSVs)
│   │   ├── federal_funds_rate.csv
│   │   ├── national_unemployment_rate.csv
│   │   ├── state_unemployment_rates.csv
│   │   └── FETCH_METADATA.md
│   ├── processed/                   # Intermediate outputs
│   │   └── panel_processed.csv
│   └── final/                       # Analysis-ready M1 output
│       ├── analysis_panel.csv       # Main dataset (20,400 observations)
│       └── M1_data_quality_report.md
├── results/
│   ├── figures/                     # Visualizations go here
│   ├── tables/                      # Regression tables go here
│   └── reports/                     # Milestone memos go here
├── tests/                           # Autograding test suite
├── SETUP_GUIDE.md                   # Detailed setup and troubleshooting
├── README.md                        # This file
└── requirements.txt                 # Python dependencies
```

## Data Source

All data is sourced directly from the **Federal Reserve Economic Data (FRED)** API:

- **Federal Funds Rate**: FEDFUNDS series
  - Monthly average of daily rates
  - Primary credit rate (discount window)
  
- **National Unemployment Rate**: UNRATE series
  - Monthly civilian unemployment rate (seasonally adjusted)
  
- **State Unemployment Rates**: Individual state series (ALUR, AKUR, AZUR, ..., WYUR)
  - Monthly unemployment rates for all 50 states
  - Seasonally adjusted

**Time Period**: January 1990 - Present (monthly observations)

## Analysis Panel

The final dataset `data/final/analysis_panel.csv` has:

- **20,400 observations** (50 states × ~408 months)
- **5 variables**:
  - `date`: Year-Month (YYYY-MM-DD)
  - `state`: State abbreviation (AL, AK, AZ, ... WY)
  - `unemployment_rate`: State unemployment rate (%)
  - `national_unemployment_rate`: US unemployment rate (%)
  - `federal_funds_rate`: Federal Funds Rate (%)

- **Panel Type**: Balanced (all states have equal observations)
- **Format**: Long format (one row per state-month)

## **Supplementary Variables**

- **inflation_cpi**: Consumer Price Index (CPIAUCSL) — national monthly inflation index, replicated across states.
- **recession_indicator**: NBER recession flag (USRECD) — monthly binary indicator (0/1).
- **treasury_10y_yield**: 10-year Treasury yield (DGS10) — monthly yield series.
- **labor_force_participation_rate**: Labor force participation (CIVPART) — national participation rate replicated across states.
- **manufacturing_employment_share**: Manufacturing employment share — (MMNRNJ / PAYEMS) × 100, derived and merged by date.
- **construction_employment_share**: Construction employment share — derived from construction employment / total payroll (where available).
- **unemployment_yoy_change**: Year-over-year change in state unemployment — lag(12) difference.
- **fed_rate_change**: Monthly first difference of federal funds rate.
- **unemployment_lagged_1mo**: One-month lag of state unemployment — useful for dynamic models.
- **unemployment_volatility_12mo**: 12-month rolling standard deviation of unemployment rate — volatility measure.

For implementation details and the full variable reference, see [SUPPLEMENTARY_VARIABLES_IMPLEMENTATION.md](SUPPLEMENTARY_VARIABLES_IMPLEMENTATION.md) and [SUPPLEMENTARY_VARIABLES_GUIDE.md](SUPPLEMENTARY_VARIABLES_GUIDE.md). The enhanced panel and documentation are available at [data/final/analysis_panel_enhanced.csv](data/final/analysis_panel_enhanced.csv) and [data/final/enhanced_panel_data_dictionary.md](data/final/enhanced_panel_data_dictionary.md). The script used to generate these variables is [code/add_supplementary_variables.py](code/add_supplementary_variables.py).

## Usage Example

```python
import pandas as pd

# Load the analysis panel
panel = pd.read_csv('data/final/analysis_panel.csv')
panel['date'] = pd.to_datetime(panel['date'])

# Summary statistics
print(panel.groupby('state')['unemployment_rate'].describe())

# Correlation
print(panel[['unemployment_rate', 'federal_funds_rate']].corr())

# Time series plot
import matplotlib.pyplot as plt
national = panel.drop_duplicates(subset=['date'])
plt.figure(figsize=(14, 6))
plt.plot(national['date'], national['federal_funds_rate'], label='Federal Funds Rate')
plt.plot(national['date'], national['national_unemployment_rate'], label='Unemployment Rate')
plt.xlabel('Date')
plt.ylabel('Rate (%)')
plt.legend()
plt.savefig('results/figures/trends.png', dpi=300)
```

## Project Components

### M1 Deliverables (Data Quality & Panel Construction)
- ✓ Data fetched from official FRED API (50 states + federal rate)
- ✓ Raw data saved to `data/raw/` with metadata
- ✓ Analysis panel created in `data/final/`
- ✓ Data quality report: `data/final/M1_data_quality_report.md`

### Verification

To verify your setup is working:

```bash
python code/config_paths.py
```

This will display all paths and confirm they exist.

## Documentation

- **[SETUP_GUIDE.md](SETUP_GUIDE.md)** — Detailed setup instructions, troubleshooting, and examples
- **data/final/M1_data_quality_report.md** — Data quality report (generated after running merge script)
- **data/raw/FETCH_METADATA.md** — Data fetch documentation (generated after running fetch script)

## Dependencies

All Python dependencies are listed in `requirements.txt`:
- pandas, numpy: Data manipulation
- fredapi: FRED API access
- matplotlib, seaborn: Visualization
- statsmodels, scikit-learn: Statistical analysis
- jupyter: Interactive notebooks

Install with: `pip install -r requirements.txt`

## FAQ

**Q: Do I need a FRED API key?**
A: Yes, but it's free and takes 2 minutes to get.

**Q: How long does data fetch take?**
A: 5-10 minutes depending on internet speed and FRED server response.

**Q: Can I use different date ranges?**
A: Yes, use `--start-date` argument: `python code/fetch_data.py --start-date 2000-01-01`

**Q: What if some states are missing data?**
A: The merge script automatically uses the overlapping date range for all states.

**Q: Can I modify the scripts?**
A: Yes! They're well-documented and designed to be extended.

## Troubleshooting

For detailed troubleshooting, see [SETUP_GUIDE.md](SETUP_GUIDE.md).

Common issues:
- **"API key not found"**: Set `FRED_API_KEY` environment variable or use `--api-key` argument
- **Connection errors**: Check internet, wait a moment, and retry
- **"Missing module"**: Run `pip install -r requirements.txt`

## Team

Golden Squad - QM 2023 Capstone Project

## Resources

- [FRED Database](https://fred.stlouisfed.org/)
- [FRED API Documentation](https://fred.stlouisfed.org/docs/api/)
- [About Federal Funds Rate](https://fred.stlouisfed.org/series/FEDFUNDS)
- [About Unemployment Rate](https://fred.stlouisfed.org/series/UNRATE)

## Contact Information
If you have questions, please contact Trenton Diveley, Henry Simon, or Rylan Leathers through UTULSA Microsoft Teams or UTULSA email.

Reign 'Cane