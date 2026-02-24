# Quick Reference Card

## Project: Federal Funds Rate vs Unemployment Rate (50 States)

### 📋 One-Time Setup (First Time Only)

```bash
# 1. Get API key (free)
# Visit: https://fred.stlouisfed.org/docs/api/api_key.html

# 2. Create .env file with your key
cp .env.example .env
# Edit .env: replace 'your_api_key_here_replace_this' with your actual key

# 3. Verify setup
python code/config_paths.py
```

---

## 🚀 Run Analysis Pipeline (Every Time)

### Step 1: Fetch Data (10-15 minutes)
```bash
python code/fetch_data.py
```
**Output**: Raw data files in `data/raw/`
- federal_funds_rate.csv (408 observations)
- national_unemployment_rate.csv (408 observations)  
- state_unemployment_rates.csv (20,400 observations)

### Step 2: Create Analysis Panel (1 minute)
```bash
python code/merge_final_panel.py
```
**Output**: Analysis-ready files in `data/final/`
- analysis_panel.csv (20,400 observations) ← **Use this for analysis!**
- M1_data_quality_report.md

---

## 📊 Your Main Dataset

**File**: `data/final/analysis_panel.csv`

**Structure**:
| date | state | unemployment_rate | national_unemployment_rate | federal_funds_rate |
|------|-------|---|---|---|
| 1990-01-01 | AL | 6.17 | 5.3 | 5.86 |
| 1990-01-01 | AK | 8.47 | 5.3 | 5.86 |
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
