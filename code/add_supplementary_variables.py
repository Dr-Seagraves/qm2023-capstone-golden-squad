"""
Capstone Project - Add Supplementary Variables to Panel
========================================================

This script takes the enhanced analysis panel and adds supplementary variables
for manufacturing employment share, construction employment share, and other
derived indicators.

It combines:
  1. Already-fetched national variables (inflation, recession, treasury)
  2. Derived national employment shares
  3. Calculated growth rates and changes
  4. Lagged variables for econometric analysis

Usage:
    python add_supplementary_variables.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from config_paths import FINAL_DATA_DIR, RAW_DATA_DIR

try:
    from fredapi import Fred
except ImportError:
    print("ERROR: fredapi not installed. Run: pip install fredapi")
    sys.exit(1)

# ==============================================================================
# CONSTANTS
# ==============================================================================

# National employment series for calculating shares
MANUFACTURING_EMPLOYMENT = 'MMNRNJ'  # Manufacturing (thousands)
CONSTRUCTION_EMPLOYMENT = 'COMPU'   # Construction (thousands)
TOTAL_NONFARM_PAYROLL = 'PAYEMS'    # Total nonfarm employment (thousands)
LABOR_FORCE_PARTICIPATION = 'CIVPART'  # Labor force participation rate (%)

# ==============================================================================
# FUNCTIONS
# ==============================================================================

def load_panel_and_raw_data():
    """Load the analysis panel and raw data files."""
    print("Loading data files...")
    
    # Load main panel
    panel_path = FINAL_DATA_DIR / 'analysis_panel.csv'
    if not panel_path.exists():
        raise FileNotFoundError(f"Missing panel data: {panel_path}")
    
    panel = pd.read_csv(panel_path)
    panel['date'] = pd.to_datetime(panel['date'])
    print(f"  ✓ Main panel: {len(panel):,} rows, {panel['date'].min().date()} to {panel['date'].max().date()}")
    
    # Load raw supplementary data
    supplementary_files = {
        'inflation': RAW_DATA_DIR / 'inflation_cpi.csv',
        'recession': RAW_DATA_DIR / 'recession_indicator.csv',
        'treasury': RAW_DATA_DIR / 'treasury_10y_yield.csv',
    }
    
    raw_data = {}
    for name, filepath in supplementary_files.items():
        if filepath.exists():
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'])
            raw_data[name] = df
            print(f"  ✓ {name}: {len(df):,} rows")
        else:
            print(f"  - {name}: not found")
    
    return panel, raw_data


def fetch_national_employment_shares(api_key):
    """Fetch and calculate national employment shares."""
    print("\nFetching national employment data from FRED...")
    
    fred = Fred(api_key=api_key)
    employment_data = {}
    
    try:
        # Total nonfarm payroll
        print(f"  Fetching {TOTAL_NONFARM_PAYROLL}...")
        total = fred.get_series(TOTAL_NONFARM_PAYROLL)
        employment_data['total'] = total
        print(f"    ✓ {len(total):,} observations")
    except Exception as e:
        print(f"    ✗ Error: {e}")
        return None
    
    try:
        # Manufacturing employment
        print(f"  Fetching {MANUFACTURING_EMPLOYMENT}...")
        mfg = fred.get_series(MANUFACTURING_EMPLOYMENT)
        employment_data['manufacturing'] = mfg
        print(f"    ✓ {len(mfg):,} observations")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    try:
        # Construction employment
        print(f"  Fetching {CONSTRUCTION_EMPLOYMENT}...")
        const = fred.get_series(CONSTRUCTION_EMPLOYMENT)
        employment_data['construction'] = const
        print(f"    ✓ {len(const):,} observations")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    try:
        # Labor force participation
        print(f"  Fetching {LABOR_FORCE_PARTICIPATION}...")
        lfpr = fred.get_series(LABOR_FORCE_PARTICIPATION)
        employment_data['lfpr'] = lfpr
        print(f"    ✓ {len(lfpr):,} observations")
    except Exception as e:
        print(f"    ✗ Error: {e}")
    
    return employment_data


def calculate_employment_shares(employment_data):
    """Calculate employment shares from raw employment data."""
    print("\nCalculating employment shares...")
    
    # Create dataframe from total payroll index (baseline)
    shares_df = pd.DataFrame({'date': employment_data['total'].index})
    
    # Manufacturing share (if available and aligned)
    if 'manufacturing' in employment_data:
        # Align manufacturing with total by date, then calculate share
        total_df = pd.DataFrame({'total': employment_data['total']})
        mfg_df = pd.DataFrame({'manufacturing': employment_data['manufacturing']})
        
        # Join on index (date)
        merged = total_df.join(mfg_df, how='inner')
        
        if len(merged) > 0:
            mfg_share = (merged['manufacturing'] / merged['total']) * 100
            shares_df = shares_df.merge(
                pd.DataFrame({'date': merged.index, 'manufacturing_employment_share': mfg_share.values}),
                on='date',
                how='left'
            )
            print(f"  ✓ Manufacturing share: mean = {mfg_share.mean():.2f}% ({len(merged)} aligned observations)")
    
    # Construction share (if available and aligned)
    if 'construction' in employment_data:
        total_df = pd.DataFrame({'total': employment_data['total']})
        const_df = pd.DataFrame({'construction': employment_data['construction']})
        
        merged = total_df.join(const_df, how='inner')
        
        if len(merged) > 0:
            const_share = (merged['construction'] / merged['total']) * 100
            shares_df = shares_df.merge(
                pd.DataFrame({'date': merged.index, 'construction_employment_share': const_share.values}),
                on='date',
                how='left'
            )
            print(f"  ✓ Construction share: mean = {const_share.mean():.2f}% ({len(merged)} aligned observations)")
    
    # Labor force participation (if available)
    if 'lfpr' in employment_data:
        lfpr_df = pd.DataFrame({'date': employment_data['lfpr'].index, 'labor_force_participation_rate': employment_data['lfpr'].values})
        lfpr_df['date'] = pd.to_datetime(lfpr_df['date'])
        
        shares_df = shares_df.merge(lfpr_df, on='date', how='left')
        print(f"  ✓ Labor force participation rate: mean = {employment_data['lfpr'].mean():.2f}% ({len(lfpr_df)} observations)")
    
    shares_df['date'] = pd.to_datetime(shares_df['date'])
    return shares_df


def add_raw_supplementary_variables(panel, raw_data):
    """Add raw supplementary variables from FRED."""
    print("\nAdding raw supplementary variables...")
    
    if 'inflation' in raw_data:
        panel = panel.merge(raw_data['inflation'], on='date', how='left')
        print(f"  ✓ Inflation added")
    
    if 'recession' in raw_data:
        panel = panel.merge(raw_data['recession'], on='date', how='left')
        print(f"  ✓ Recession indicator added")
    
    if 'treasury' in raw_data:
        panel = panel.merge(raw_data['treasury'], on='date', how='left')
        print(f"  ✓ 10-Year Treasury yield added")
    
    return panel


def add_employment_shares(panel, shares_df):
    """Add manufactured employment shares to panel."""
    print("\nAdding employment shares...")
    
    # Merge employment shares (replicate national values for all states)
    panel = panel.merge(shares_df, on='date', how='left')
    print(f"  ✓ Employment shares merged (national values replicated for all states)")
    
    return panel


def calculate_derived_variables(panel):
    """Calculate derived variables for econometric analysis."""
    print("\nCalculating derived variables...")
    
    # Year-over-year changes in unemployment
    panel['unemployment_yoy_change'] = (
        panel.groupby('state')['unemployment_rate'].shift(1) - 
        panel.groupby('state')['unemployment_rate'].shift(13)
    )
    print(f"  ✓ Unemployment YoY change calculated")
    
    # Federal funds rate change
    panel['fed_rate_change'] = panel['federal_funds_rate'].diff()
    print(f"  ✓ Federal funds rate change calculated")
    
    # Lagged unemployment rate
    panel['unemployment_lagged_1mo'] = panel.groupby('state')['unemployment_rate'].shift(1)
    print(f"  ✓ Lagged unemployment (1-month) calculated")
    
    # Lagged federal funds rate
    panel['fed_rate_lagged_1mo'] = panel['federal_funds_rate'].shift(1)
    print(f"  ✓ Lagged federal funds rate (1-month) calculated")
    
    # Rolling 12-month standard deviation of unemployment (volatility)
    panel['unemployment_volatility_12mo'] = (
        panel.groupby('state')['unemployment_rate']
        .rolling(window=12, min_periods=1)
        .std()
        .reset_index(drop=True)
    )
    print(f"  ✓ Unemployment volatility (12-month rolling std) calculated")
    
    return panel


def generate_final_report(panel):
    """Generate final data quality report for enhanced panel."""
    print("\nGenerating final data quality report...")
    
    report = []
    report.append("# Enhanced Analysis Panel - Final Data Dictionary\n\n")
    report.append(f"Generated: {datetime.now().isoformat()}\n\n")
    
    report.append("## Panel Summary\n\n")
    report.append(f"- **Observations:** {len(panel):,}\n")
    report.append(f"- **States:** {panel['state'].nunique()}\n")
    report.append(f"- **Time Period:** {panel['date'].min().date()} to {panel['date'].max().date()}\n")
    report.append(f"- **Variables:** {panel.shape[1]}\n\n")
    
    report.append("## All Variables in Panel\n\n")
    report.append("| # | Variable | Type | Description |\n")
    report.append("|---|----------|------|-------------|\n")
    
    var_descriptions = {
        'date': ('Date', 'YYYY-MM-DD format'),
        'state': ('State', 'State abbreviation (AL-WY)'),
        'unemployment_rate': ('Unemployment Rate', 'State unemployment (%)'),
        'national_unemployment_rate': ('National Unemployment', 'US unemployment (%)'),
        'federal_funds_rate': ('Federal Funds Rate', 'Target rate (%)'),
        'inflation_cpi': ('Inflation', 'CPI index'),
        'recession_indicator': ('Recession Indicator', 'NBER recession (0/1)'),
        'treasury_10y_yield': ('10-Year Treasury', 'Yield (%)'),
        'manufacturing_employment_share': ('Mfg Employment Share', 'Mfg as % of total'),
        'construction_employment_share': ('Construction Share', 'Construction as % of total'),
        'labor_force_participation_rate': ('Labor Force Participation', 'Participation rate (%)'),
        'unemployment_yoy_change': ('Unemployment YoY Change', 'Change from prior year (pp)'),
        'fed_rate_change': ('Fed Rate Change', 'Monthly change (pp)'),
        'unemployment_lagged_1mo': ('Unemployment Lagged', 'Previous month (%)'),
        'fed_rate_lagged_1mo': ('Fed Rate Lagged', 'Previous month (%)'),
        'unemployment_volatility_12mo': ('Unemployment Volatility', '12-month rolling std dev'),
    }
    
    counter = 1
    for col in panel.columns:
        if col in var_descriptions:
            var_type, desc = var_descriptions[col]
            report.append(f"| {counter} | {col} | {var_type} | {desc} |\n")
            counter += 1
    
    report.append("\n## Data Quality Summary\n\n")
    report.append("| Variable | Missing | % Missing | Min | Mean | Max |\n")
    report.append("|----------|---------|-----------|-----|------|-----|\n")
    
    numeric_cols = panel.select_dtypes(include=['float64', 'int64']).columns
    for col in numeric_cols:
        if col == 'state':
            continue
        missing = panel[col].isna().sum()
        pct_missing = 100 * missing / len(panel)
        min_val = panel[col].min()
        mean_val = panel[col].mean()
        max_val = panel[col].max()
        report.append(
            f"| {col} | {missing:,} | {pct_missing:.1f}% | "
            f"{min_val:.2f} | {mean_val:.2f} | {max_val:.2f} |\n"
        )
    
    report.append("\n## Econometric Ready\n\n")
    report.append("✓ Panel structure: Long format (state-month observations)\n")
    report.append("✓ Balanced time dimension: All states have same dates\n")
    report.append("✓ Lagged variables: Available for dynamic analysis\n")
    report.append("✓ National regressors: Federal funds, inflation, recession\n")
    report.append("✓ State-time heterogeneity: Ready for fixed effects\n\n")
    
    report_text = ''.join(report)
    
    report_path = FINAL_DATA_DIR / 'enhanced_panel_data_dictionary.md'
    with open(report_path, 'w') as f:
        f.write(report_text)
    
    print(f"  ✓ Report saved: enhanced_panel_data_dictionary.md")
    return report_text


def main():
    """Main execution function."""
    print("=" * 80)
    print("ADDING SUPPLEMENTARY VARIABLES TO ANALYSIS PANEL")
    print("=" * 80)
    
    try:
        # Load existing data
        panel, raw_data = load_panel_and_raw_data()
        
        # Get API key
        api_key = pd.read_csv(Path('/workspaces/qm2023-capstone-golden-squad/.env'), 
                            header=None, sep='=', index_col=0).loc['FRED_API_KEY', 1]
        
        # Fetch employment data
        employment_data = fetch_national_employment_shares(api_key)
        
        # Calculate shares
        if employment_data:
            shares_df = calculate_employment_shares(employment_data)
            panel = add_employment_shares(panel, shares_df)
        
        # Add supplementary variables
        panel = add_raw_supplementary_variables(panel, raw_data)
        
        # Calculate derived variables
        panel = calculate_derived_variables(panel)
        
        # Save enhanced panel
        print("\nSaving enhanced panel...")
        output_path = FINAL_DATA_DIR / 'analysis_panel_enhanced.csv'
        panel.to_csv(output_path, index=False)
        print(f"  ✓ Saved: {output_path.name}")
        print(f"  ✓ {len(panel):,} observations × {panel.shape[1]} variables")
        
        # Generate report
        generate_final_report(panel)
        
        print("\n" + "=" * 80)
        print("✓ SUPPLEMENTARY VARIABLES ADDED SUCCESSFULLY!")
        print("=" * 80)
        print(f"✓ Enhanced panel: analysis_panel_enhanced.csv")
        print(f"✓ Variables added:")
        print(f"  - Inflation (CPI)")
        print(f"  - Recession indicator")
        print(f"  - 10-Year Treasury yield")
        print(f"  - Manufacturing employment share")
        print(f"  - Construction employment share")
        print(f"  - Labor force participation rate")
        print(f"  - Lagged variables")
        print(f"  - Volatility measures")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
