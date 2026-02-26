# 🚀 START HERE - Quick Action Plan

## ⏱️ Total Time Required: ~20 minutes
- FRED API Key: 2 minutes
- Environment setup: 2 minutes  
- First data fetch: 10 minutes
- Data merge: 1 minute
- Verification: 5 minutes

---

## 📋 YOUR CHECKLIST (Do These Steps In Order)

### Step 1: Get Your Free FRED API Key ⏰ 2 min
```
1. Go to: https://fred.stlouisfed.org/docs/api/api_key.html
2. Click "Request API Key"
3. Create free account (auto-filled from GitHub probably)
4. Check your email for your 32-character API key
5. Save it somewhere (you'll use it in 5 minutes)
```

**Status**: ☐ Done

---

### Step 2: Get Your Free BLS API Key ⏰ 2 min
```
1. Go to: https://www.bls.gov/developers/
2. Click "Request a Key"
3. Fill out the form and submit
4. Check your email for your API key
5. Save it somewhere (you'll use it in 5 minutes)
```

**Status**: ☐ Done

---

### Step 3: Set Your API Keys ⏰ 1 min
Pick ONE method:

**Method A: Edit .env file** (Recommended)
```bash
# In project root (where README.md is):
# 1. Make sure you're in the right directory:
cd /workspaces/qm2023-capstone-golden-squad

# 2. Look at the template:
cat .env.example

# 3. Edit the file (click on .env.example in VS Code, change it, save as .env)
# Replace the placeholder keys with your actual keys:
# - FRED_API_KEY=your_actual_fred_key
# - BLS_API_KEY=your_actual_bls_key

# 4. Then run:
export $(cat .env | xargs)
```

**Method B: Set environment variables directly**
```bash
export FRED_API_KEY=your_actual_fred_api_key_here
export BLS_API_KEY=your_actual_bls_api_key_here
```

**Status**: ☐ Done

---

### Step 3: Download Data from FRED ⏰ 10 min
```bash
# Make sure you're in the project root:
cd /workspaces/qm2023-capstone-golden-squad

# Run the data fetcher:
python code/fetch_data.py
```

**What you'll see**:
- Progress bars for each of 50 states
- Files being saved to `data/raw/`
- Confirmation message at the end

**What gets created**:
- `data/raw/federal_funds_rate.csv`
- `data/raw/national_unemployment_rate.csv`
- `data/raw/state_unemployment_rates.csv`
- `data/raw/FETCH_METADATA.md`

**Status**: ☐ Done

---

### Step 4: Create Your Analysis Dataset ⏰ 1 min
```bash
# Still in project root:
python code/merge_final_panel.py
```

**What you'll see**:
- Loading messages
- Merge progress
- Quality report generation
- Summary of 20,400 observations

**What gets created**:
- `data/final/analysis_panel.csv` ← **📊 YOUR MAIN DATASET**
- `data/final/M1_data_quality_report.md`
- `data/processed/panel_processed.csv`

**Status**: ☐ Done

---

### Step 5: Verify Everything Works ⏰ 2 min
```bash
# Check the setup:
bash verify_setup.sh

# Should see green checkmarks (✓) for everything
```

**Status**: ☐ Done

---

### Step 6: Load Your Data 🎉 (Optional - see it in action)
```bash
# See your data in action:
python example_analysis.py
```

**This will**:
- Print data summary statistics
- Show correlations
- Create 3 publication-ready plots
- Run basic regressions
- Save PNG files to `results/figures/`

**Status**: ☐ Done

---

## 📊 Now You Have Your Data!

**Location**: `data/final/analysis_panel.csv`

**Structure** (20,400 rows × 5 columns):
```
date               state  unemployment_rate  national_unemployment_rate  federal_funds_rate
2026-02-01         AL     3.45              3.9                       4.75
2026-02-01         AK     4.12              3.9                       4.75
...
```

**Ready to use for**:
- Time series analysis
- Panel regressions  
- Correlation studies
- Visualization
- Hypothesis testing

---

## 🎓 Next: Analyze Your Data

```python
import pandas as pd

# Load your data
panel = pd.read_csv('data/final/analysis_panel.csv')
panel['date'] = pd.to_datetime(panel['date'])

# Quick analysis
print(panel.describe())
print(panel.groupby('state')['unemployment_rate'].mean())

# Regression
from statsmodels.formula.api import ols
model = ols('unemployment_rate ~ federal_funds_rate', data=panel).fit()
print(model.summary())
```

---

## ⚠️ Troubleshooting

| Problem | Solution |
|---------|----------|
| "API key not found" | Did you run `export FRED_API_KEY=...`? Check Step 2 |
| "Connection error" | Check internet. FRED might be slow. Wait 5 min & retry |
| "FileNotFoundError" | Did you run fetch_data.py first? Check Step 3 |
| "Module not found" | Python dependencies. Run: `pip install -r requirements.txt` |
| Still stuck? | Read SETUP_GUIDE.md for detailed troubleshooting |

---

## 📚 Documentation Files

| File | When to Read |
|------|---|
| **QUICKSTART.md** | 2-minute reference while working |
| **SETUP_GUIDE.md** | Detailed setup & troubleshooting |
| **PROJECT_FILES_SUMMARY.md** | Details about what was created |
| **README.md** | Project overview |

---

## ✅ Verification Checklist

After completing all steps:

- [ ] FRED API key obtained
- [ ] FRED_API_KEY environment variable set  
- [ ] `python code/fetch_data.py` completed successfully
- [ ] `python code/merge_final_panel.py` completed successfully
- [ ] `data/final/analysis_panel.csv` file exists (20,400+ rows)
- [ ] `bash verify_setup.sh` shows all green checkmarks
- [ ] Can load data in Python without errors
- [ ] Ready to start your analysis

---

## 🎯 You Are Now Ready To:

✅ Analyze how Federal Funds Rate affects unemployment  
✅ Run state-level regressions  
✅ Create visualizations  
✅ Test your research hypotheses  
✅ Complete your capstone project  

---

**Questions?** 
- Quick questions → see QUICKSTART.md
- Setup problems → see SETUP_GUIDE.md  
- Details about files → see PROJECT_FILES_SUMMARY.md

**Good luck with your capstone! 🎓**
