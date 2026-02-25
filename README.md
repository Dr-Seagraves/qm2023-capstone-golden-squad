[![Review Assignment Due Date](https://classroom.github.com/assets/deadline-readme-button-22041afd0340ce965d47ae6ef1cefeee28c7c493a6346c4f15d667ab976d596c.svg)](https://classroom.github.com/a/gp9US0IQ)
[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=22639587&assignment_repo_type=AssignmentRepo)
# QM 2023 Capstone Project

Semester-long capstone for Statistics II: Data Analytics.

## Research Question

**How do interest rates (Federal Funds Rate) affect unemployment rates across the United States over time?**

We analyze the relationship between the national Federal Funds Rate and unemployment rates across all 50 states to identify whether interest rate policy correlates with state-level employment dynamics. While not directly linked, interest rates affect investment, consumer spending, and borrowing costs, which influence unemployment rates.

## Preliminary Hypothesis

**Hypothesis**: Higher federal funds rates will be associated with lower unemployment rates, but this relationship may vary across states and economic conditions.

**Rationale**:
- **Monetary Policy Theory**: The Federal Reserve increases interest rates to combat inflation and cool down an overheating economy, which typically occurs during periods of low unemployment
- **Phillips Curve**: Suggests an inverse relationship between inflation (controlled by interest rates) and unemployment
- **State-Level Variation**: Economic conditions, industry composition, and regional factors may cause the relationship to differ across states
- **Time-Varying Effects**: The relationship may be stronger during certain economic periods (e.g., recessions vs. expansions)

**Expected Findings**:
- Negative correlation between federal funds rate and unemployment rate
- Stronger effects in manufacturing-heavy states
- Weaker effects during recession periods
- Potential lag effects (1-6 months) in unemployment response

## Quick Start

### 1. Get Your FRED API Key (5 minutes)
- Visit: [https://fred.stlouisfed.org/docs/api/api_key.html](https://fred.stlouisfed.org/docs/api/api_key.html)
- Click "Request API Key" and sign up (free account)
- Save your 32-character key

### 2. Get Your BLS API Key (5 minutes)
- Visit: [https://www.bls.gov/developers/](https://www.bls.gov/developers/)
- Click "Request a Key" and fill out the form (free account)
- Save your API key (typically 32 characters)

### 3. Set Your API Keys
```bash
# Option A: Create .env file
cp .env.example .env
# Edit .env and replace the placeholder keys with your actual keys:
# - FRED_API_KEY=your_actual_fred_key
# - BLS_API_KEY=your_actual_bls_key

# Option B: Export as environment variables
export FRED_API_KEY=YOUR_FRED_API_KEY_HERE
export BLS_API_KEY=YOUR_BLS_API_KEY_HERE
```

### 4. Fetch Data from FRED
```bash
python code/fetch_data.py
```
This downloads Federal Funds Rate and unemployment data for all 50 states.

### 5. Fetch Supplementary Data from BLS (Optional)
```bash
python Code/fetch_bls_data.py
```
This downloads additional economic indicators from the Bureau of Labor Statistics API.

### 6. Create Analysis Panel
```bash
python code/merge_final_panel_enhanced.py
```
This merges raw FRED data into an analysis-ready panel dataset stored in `data/final/analysis_panel_enhanced.csv`.

**Total time:** ~10-15 minutes depending on internet speed

---

## Project Structure

```
qm2023-capstone-golden-squad/
├── Code/                           # Main Python scripts
│   ├── config_paths.py            # Centralized path configuration
│   ├── fetch_data.py              # Download data from FRED API
│   ├── fetch_bls_data.py          # Download supplementary data from BLS API
│   ├── merge_final_panel_enhanced.py # Create enhanced analysis-ready panel
│   ├── example_analysis.py        # Example analysis and visualization
│   ├── add_supplementary_variables.py # Supplementary variable calculations
│   ├── verify_setup.sh            # Setup verification script
│   └── __pycache__/               # Python bytecode cache
├── data/
│   ├── raw/                       # Original API data (CSVs)
│   │   ├── federal_funds_rate.csv
│   │   ├── national_unemployment_rate.csv
│   │   ├── state_unemployment_rates.csv
│   │   ├── inflation_cpi.csv
│   │   ├── recession_indicator.csv
│   │   ├── treasury_10y_yield.csv
│   │   ├── total_nonfarm_employment.csv
│   │   ├── civilian_labor_force.csv
│   │   ├── manufacturing_employment.csv
│   │   └── FETCH_METADATA.md
│   ├── processed/                 # Intermediate outputs
│   │   └── panel_enhanced.csv
│   └── final/                     # Analysis-ready output
│       ├── analysis_panel_enhanced.csv # Main dataset (20,736 observations)
│       ├── enhanced_panel_data_dictionary.md
│       └── M1_enhanced_data_quality_report.md
├── results/
│   ├── figures/                   # Generated visualizations
│   │   ├── time_series_trends.png
│   │   ├── state_unemployment_distribution.png
│   │   └── scatter_unemployment_vs_fedfunds.png
│   ├── tables/                    # Regression tables
│   └── reports/                   # Milestone memos and reports
├── docs/                          # Documentation
│   ├── START_HERE.md             # Step-by-step setup guide
│   ├── QUICKSTART.md             # Quick reference guide
│   ├── SETUP_GUIDE.md            # Detailed setup and troubleshooting
│   ├── SUPPLEMENTARY_VARIABLES_GUIDE.md
│   ├── SUPPLEMENTARY_VARIABLES_IMPLEMENTATION.md
│   ├── PROJECT_COMPLETION_STATUS.md
│   └── PROJECT_FILES_SUMMARY.md
├── tests/                         # Test suite
│   └── test_reproducibility.py    # Reproducibility verification
├── AI_Chat_Logs/                  # Development logs
├── AI_AUDIT_APPENDIX.md          # AI assistance documentation
├── .env                          # Environment variables (API keys)
├── .env.example                  # Environment template
├── requirements.txt              # Python dependencies
└── README.md                     # This file
```

## Data Sources

All data is sourced directly from official government APIs:

### Federal Reserve Economic Data (FRED) API
- **Federal Funds Rate**: FEDFUNDS series
  - Monthly average of daily rates
  - Primary credit rate (discount window)
  
- **National Unemployment Rate**: UNRATE series
  - Monthly civilian unemployment rate (seasonally adjusted)
  
- **State Unemployment Rates**: Individual state series (ALUR, AKUR, AZUR, ..., WYUR)
  - Monthly unemployment rates for all 50 states
  - Seasonally adjusted

- **Inflation (CPI)**: CPIAUCSL series
  - Consumer Price Index for All Urban Consumers

- **Recession Indicator**: USRECD series
  - NBER official recession indicator (0/1)

- **10-Year Treasury Yield**: DGS10 series
  - 10-year Treasury constant maturity rate

### Bureau of Labor Statistics (BLS) API
- **Total Nonfarm Employment**: CES0000000001
  - Total nonfarm payroll employment

- **Civilian Labor Force**: LNS11000000
  - Civilian labor force level

- **Manufacturing Employment**: CES3000000001
  - Manufacturing sector employment

- **Construction Employment**: CES2000000001
  - Construction sector employment

- **Job Openings**: JTS000000000000000JOL
  - Job openings level

- **Quits Rate**: JTS000000000000000QUR
  - Quits rate

**Time Period**: January 1990 - December 2025 (monthly observations)

## Analysis Panel

The final dataset `data/final/analysis_panel_enhanced.csv` has:

- **20,736 observations** (48 states × ~433 months)
- **15 variables**:
  - `date`: Year-Month (YYYY-MM-DD)
  - `state`: State abbreviation (AL, AK, AZ, ... WY)
  - `unemployment_rate`: State unemployment rate (%)
  - `national_unemployment_rate`: US unemployment rate (%)
  - `federal_funds_rate`: Federal Funds Rate (%)
  - `inflation_cpi`: Consumer Price Index
  - `recession_indicator`: NBER recession flag (0/1)
  - `treasury_10y_yield`: 10-year Treasury yield
  - `total_nonfarm_employment`: Total nonfarm employment
  - `civilian_labor_force`: Civilian labor force
  - `total_private_employment`: Total private employment
  - `manufacturing_employment`: Manufacturing employment
  - `cpi`: Consumer Price Index (alternative)
  - `year`: Year
  - `month`: Month

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

# Load the enhanced analysis panel
panel = pd.read_csv('data/final/analysis_panel_enhanced.csv')
panel['date'] = pd.to_datetime(panel['date'])

# Summary statistics by state
print(panel.groupby('state')['unemployment_rate'].describe())

# Correlation analysis
key_vars = ['unemployment_rate', 'federal_funds_rate', 'inflation_cpi', 'recession_indicator']
print(panel[key_vars].corr())

# Time series plot
import matplotlib.pyplot as plt
national = panel.drop_duplicates(subset=['date']).sort_values('date')
plt.figure(figsize=(14, 6))
plt.plot(national['date'], national['federal_funds_rate'], label='Federal Funds Rate')
plt.plot(national['date'], national['national_unemployment_rate'], label='National Unemployment')
plt.xlabel('Date')
plt.ylabel('Rate (%)')
plt.title('Federal Funds Rate vs National Unemployment (1990-2025)')
plt.legend()
plt.savefig('results/figures/trends.png', dpi=300, bbox_inches='tight')
```

## Project Status

### ✅ **M1 Deliverables (Data Quality & Panel Construction) - COMPLETED**
- ✓ Data fetched from official FRED and BLS APIs (48 states + federal/national data)
- ✓ Raw data saved to `data/raw/` with metadata
- ✓ Enhanced analysis panel created in `data/final/analysis_panel_enhanced.csv`
- ✓ Data quality report: `M1_enhanced_data_quality_report.md`
- ✓ Supplementary variables implemented (15 total variables)

### ✅ **Setup & Reproducibility - VERIFIED**
- ✓ Automated setup verification script (`Code/verify_setup.sh`)
- ✓ Reproducibility testing (`tests/test_reproducibility.py`)
- ✓ Complete documentation suite
- ✓ Environment configuration with API keys

## Documentation

### Setup & Getting Started
- **[docs/START_HERE.md](docs/START_HERE.md)** — Step-by-step setup checklist
- **[docs/QUICKSTART.md](docs/QUICKSTART.md)** — Quick reference guide
- **[docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md)** — Detailed setup instructions and troubleshooting

### Data & Methodology
- **[data/final/enhanced_panel_data_dictionary.md](data/final/enhanced_panel_data_dictionary.md)** — Complete variable definitions
- **[M1_enhanced_data_quality_report.md](M1_enhanced_data_quality_report.md)** — Data quality assessment
- **[docs/SUPPLEMENTARY_VARIABLES_GUIDE.md](docs/SUPPLEMENTARY_VARIABLES_GUIDE.md)** — Supplementary variables documentation
- **[docs/SUPPLEMENTARY_VARIABLES_IMPLEMENTATION.md](docs/SUPPLEMENTARY_VARIABLES_IMPLEMENTATION.md)** — Implementation details

### Project Management
- **[docs/PROJECT_COMPLETION_STATUS.md](docs/PROJECT_COMPLETION_STATUS.md)** — Current project status
- **[docs/PROJECT_FILES_SUMMARY.md](docs/PROJECT_FILES_SUMMARY.md)** — File inventory and descriptions
- **[AI_AUDIT_APPENDIX.md](AI_AUDIT_APPENDIX.md)** — AI assistance documentation

## Dependencies

All Python dependencies are listed in `requirements.txt`:
- pandas, numpy: Data manipulation
- fredapi: FRED API access
- matplotlib, seaborn: Visualization
- statsmodels, scikit-learn: Statistical analysis
- jupyter: Interactive notebooks

Install with: `pip install -r requirements.txt`

## FAQ

**Q: Do I need API keys?**  
A: Yes, you need both FRED and BLS API keys. Both are free and take about 2 minutes each to obtain.

**Q: How long does data fetch take?**  
A: FRED data: 5-10 minutes. BLS data: 2-3 minutes. Total setup: ~15-20 minutes.

**Q: Can I use different date ranges?**  
A: Yes, modify the `start_date` parameter in the fetch scripts. Default is 1990-01-01.

**Q: What if some states are missing data?**  
A: The merge script automatically uses the overlapping date range for all states (1990-2025).

**Q: Can I modify the analysis?**  
A: Yes! The scripts are well-documented and designed to be extended. See `Code/example_analysis.py` for examples.

**Q: What statistical methods are you using?**  
A: Panel data regression (Fixed Effects, Random Effects), time series analysis, and hypothesis testing.

**Q: How do I run the analysis?**  
A: After setup, run `python Code/example_analysis.py` to generate exploratory analysis and visualizations.

## Troubleshooting

For detailed troubleshooting, see [docs/SETUP_GUIDE.md](docs/SETUP_GUIDE.md).

**Common Issues:**
- **"API key not found"**: Set both `FRED_API_KEY` and `BLS_API_KEY` environment variables or add them to `.env` file
- **Connection errors**: Check internet connection, wait a moment, and retry
- **"Missing module"**: Run `pip install -r requirements.txt`
- **"File not found"**: Ensure you've run all setup steps in order
- **BLS API limits**: The free BLS API has rate limits; the script handles this automatically

**Verification Script:**
```bash
bash Code/verify_setup.sh
```
This checks your entire setup and provides specific guidance for any issues.

## Team

**Golden Squad** - QM 2023 Capstone Project

- **Trenton Diveley** 
- **Henry Simon** 
- **Rylan Leathers** 

*University of Tulsa - Data Analytics 2023-01*

## Resources

### Data Sources
- [Federal Reserve Economic Data (FRED)](https://fred.stlouisfed.org/)
- [FRED API Documentation](https://fred.stlouisfed.org/docs/api/)
- [Bureau of Labor Statistics (BLS)](https://www.bls.gov/)
- [BLS API Documentation](https://www.bls.gov/developers/)

### Economic Indicators
- [About Federal Funds Rate](https://fred.stlouisfed.org/series/FEDFUNDS)
- [About Unemployment Rate](https://fred.stlouisfed.org/series/UNRATE)
- [About CPI Inflation](https://fred.stlouisfed.org/series/CPIAUCSL)
- [NBER Recession Indicators](https://fred.stlouisfed.org/series/USRECD)

### Academic References
- Phillips Curve Theory
- Monetary Policy Transmission Mechanisms
- Panel Data Econometrics
- Time Series Analysis in Macroeconomics

## Contact Information


📧 For questions or concerns, contact via UTulsa Microsoft Teams or university email

---

**"Reign 'Cane"** 