# Quick Reference Card

## Project: Federal Funds Rate vs Unemployment Rate (50 States)

### 📋 One-Time Setup (First Time Only)

```bash
# 1. Get API key (free)
# Visit: https://fred.stlouisfed.org/docs/api/api_key.html

# 2. Create .env file with your keys
cp .env.example .env
# Edit .env: replace the placeholder keys with your actual keys:
# - FRED_API_KEY=your_actual_fred_key
# - BLS_API_KEY=your_actual_bls_key

# 3. Verify setup
python Code/config_paths.py
```

---

## 🚀 Run Analysis Pipeline (Every Time)

### Step 1: Fetch Core Data from FRED (10-15 minutes)
```bash
python Code/fetch_data.py
```
**Output**: Raw data files in `data/raw/`
- federal_funds_rate.csv (433 observations)
- national_unemployment_rate.csv (433 observations)  
- state_unemployment_rates.csv (20,736 observations)

### Step 2: Fetch Supplementary Data from BLS (Optional, 2-3 minutes)
```bash
python Code/fetch_bls_data.py
```
**Output**: Additional raw data files in `data/raw/`
- cpi.csv, total_nonfarm_employment.csv, etc.

### Step 3: Create Analysis Panel (1 minute)
```bash
python Code/merge_final_panel_enhanced.py
```
**Output**: Analysis-ready files in `data/final/`
- analysis_panel_enhanced.csv (20,736 observations) ← **Use this for analysis!**
- M2_enhanced_data_quality_report.md

---

## 📊 Your Main Dataset

**File**: `data/final/analysis_panel_enhanced.csv`

**Structure**:
| date | state | unemployment_rate | national_unemployment_rate | federal_funds_rate | inflation_cpi | recession_indicator | treasury_10y_yield | ... |
|------|-------|---|---|---|---|---|---|---|---|
| 1990-01-01 | AL | 6.17 | 5.3 | 5.86 | 127.5 | 0 | NaN | ... |
| 1990-01-01 | AK | 8.47 | 5.3 | 5.86 | 127.5 | 0 | NaN | ... |
| ... | ... | ... | ... | ... |

**Stats**:
- 20,400 observations (50 states × ~408 months)
- Time period: Jan 1990 - Present
- All values in percentages (%)
- Balanced panel (all states have same time period)

---

## 💻 Use in Python

```python
import pandas as pd

# Load data
panel = pd.read_csv('data/final/analysis_panel.csv')
panel['date'] = pd.to_datetime(panel['date'])

# Quick analysis
print(panel.describe())
print(panel.groupby('state')['unemployment_rate'].mean())

# Regression example
from statsmodels.formula.api import ols
model = ols('unemployment_rate ~ federal_funds_rate', data=panel).fit()
print(model.summary())
```

---

## 📁 Directory Reference

| Directory | Contains | Use For |
|-----------|----------|---------|
| `data/raw/` | Original FRED data | Reference only |
| `data/processed/` | Intermediate outputs | Quality control |
| `data/final/` | Analysis-ready data | **Your analysis** |
| `results/figures/` | Empty (for your plots) | Save visualizations here |
| `results/tables/` | Empty (for your tables) | Save regression tables here |
| `results/reports/` | Empty (for memos) | Save milestone reports here |

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not found" | Set `export FRED_API_KEY=your_key` |
| "Connection error" | Check internet, retry in 5 minutes |
| "Missing module" | Run `pip install -r requirements.txt` |
| "File not found" | Verify you ran fetch_data.py AND merge_final_panel.py |

---

## 📚 Full Documentation

See **SETUP_GUIDE.md** for:
- Detailed installation steps
- Extended troubleshooting
- Data format specifications
- Analysis examples

---

## 🔗 Data Sources

- **FRED API**: https://fred.stlouisfed.org/docs/api/
- **Federal Funds Rate**: https://fred.stlouisfed.org/series/FEDFUNDS
- **Unemployment Rate**: https://fred.stlouisfed.org/series/UNRATE

**Status**: ✓ Ready to use | Last updated: 2/24/2026
