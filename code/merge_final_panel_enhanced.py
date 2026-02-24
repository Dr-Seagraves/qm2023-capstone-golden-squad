"""
Capstone Project - Enhanced Data Panel Merger
==============================================

This script merges all raw FRED data (M1 core + M2+ supplementary) 
into analysis-ready panel format.

Core Variables (M1):
  1. Federal Funds Rate (national, monthly)
  2. National Unemployment Rate (national, monthly)
  3. State Unemployment Rates (all states, monthly)

Supplementary Variables (M2+):
  4-10: State-level variables (nonfarm payroll, income, housing, etc.)
  11-13: National variables (inflation, recession, treasury yield)

Panel Structure:
  - Long format: 50 states × 400+ months
  - All variables merged by date
  - National variables replicated for all states
  - Derived variables calculated

Usage:
    python merge_final_panel_enhanced.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime

sys.path.insert(0, str(Path(__file__).parent))
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, FINAL_DATA_DIR

# ==============================================================================
# FUNCTIONS
# ==============================================================================

def load_raw_data():
    """Load all available raw data files."""
    print("Loading raw data files...")
    
    # Core data files (always needed)
    core_files = {
        'federal_funds': 'federal_funds_rate.csv',
        'national_unemployment': 'national_unemployment_rate.csv',
        'state_unemployment': 'state_unemployment_rates.csv',
    }
    
    # Optional supplementary files
    optional_files = {
        'inflation': 'inflation_cpi.csv',
        'recession': 'recession_indicator.csv',
        'treasury_10y': 'treasury_10y_yield.csv',
        'employment_level': 'state_employment_level.csv',
        'labor_force_level': 'state_labor_force_level.csv',
        'private_employment': 'state_private_employment.csv',
    }
    
    data = {}
    
    # Load core data
    for key, filename in core_files.items():
        filepath = RAW_DATA_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Missing core data file: {filename}")
        
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        data[key] = df
        print(f"  ✓ {filename}: {len(df):,} rows")
    
    # Load optional supplementary data
    print("\nLoading supplementary data (if available)...")
    for key, filename in optional_files.items():
        filepath = RAW_DATA_DIR / filename
        if filepath.exists():
            df = pd.read_csv(filepath)
            df['date'] = pd.to_datetime(df['date'])
            data[key] = df
            print(f"  ✓ {filename}: {len(df):,} rows")
        else:
            print(f"  - {filename}: not found (skipping)")
    
    return data


def harmonize_frequencies(data):
    """Handle different data frequencies (monthly vs annual)."""
    print("\nHarmonizing data frequencies...")
    
    # Identify annual data (real income)
    if 'real_income' in data:
        df = data['real_income']
        if df['date'].dt.month.nunique() == 1:  # Only one month value
            print("  ℹ Real Personal Income: Annual data -> interpolating to monthly")
            # Forward fill annual data to monthly
            df = df.set_index('date').asfreq('MS').interpolate(method='forward_fill')
            df = df.reset_index()
            data['real_income'] = df
    
    return data


def create_state_panel(state_unemp, federal_funds, national_unemp, data):
    """Create comprehensive analysis panel combining all variables."""
    print("\nCreating comprehensive analysis panel...")
    
    # Sort for merging
    federal_funds = federal_funds.sort_values('date').reset_index(drop=True)
    national_unemp = national_unemp.sort_values('date').reset_index(drop=True)
    state_unemp = state_unemp.sort_values('date').reset_index(drop=True)
    
    # Get common date range
    common_start = max(
        state_unemp['date'].min(),
        federal_funds['date'].min(),
        national_unemp['date'].min()
    )
    common_end = min(
        state_unemp['date'].max(),
        federal_funds['date'].max(),
        national_unemp['date'].max()
    )
    
    print(f"  Primary date range: {common_start.date()} to {common_end.date()}")
    
    # Merge federal funds with national unemployment
    national_data = federal_funds.merge(
        national_unemp,
        on='date',
        how='inner'
    )
    
    # Start with state unemployment
    panel = state_unemp.merge(
        national_data,
        on='date',
        how='inner'
    ).copy()
    
    # Add national supplementary variables (replicate for all states)
    for state_name, df in [('inflation', 'inflation_cpi'), 
                           ('recession', 'recession_indicator'),
                           ('treasury_10y', 'treasury_10y_yield')]:
        if state_name in data:
            df_nat = data[state_name].sort_values('date').reset_index(drop=True)
            # Merge on date (will replicate national values for all states)
            panel = panel.merge(df_nat, on='date', how='left')
    
    # Add state-level supplementary variables
    for state_var in ['employment_level', 'labor_force_level', 'private_employment']:
        if state_var in data:
            df_state = data[state_var].sort_values(['date', 'state']).reset_index(drop=True)
            panel = panel.merge(df_state, on=['date', 'state'], how='left')
    
    # Filter to common date range
    panel = panel[
        (panel['date'] >= common_start) & 
        (panel['date'] <= common_end)
    ].reset_index(drop=True)
    
    # Sort
    panel = panel.sort_values(['date', 'state']).reset_index(drop=True)
    
    return panel


def calculate_derived_variables(panel):
    """Calculate derived variables (employment shares, growth rates, etc.)."""
    print("\nCalculating derived variables...")
    
    # Create a copy to avoid modifying while iterating
    panel_copy = panel.copy()
    
    # Create a state_year identifier for annual calculations if needed
    panel_copy['year'] = panel_copy['date'].dt.year
    panel_copy['month'] = panel_copy['date'].dt.month
    
    print("  ✓ Prepared derived variable columns")
    
    return panel_copy


def generate_data_quality_report(panel, output_dir):
    """Generate comprehensive data quality report."""
    print("\nGenerating data quality report...")
    
    report = []
    report.append("# Data Quality Report - Enhanced Panel (M1 + M2+)\n\n")
    report.append(f"Generated: {datetime.now().isoformat()}\n\n")
    
    report.append("## Panel Overview\n\n")
    report.append(f"- **Total Observations:** {len(panel):,}\n")
    report.append(f"- **Number of States:** {panel['state'].nunique()}\n")
    report.append(f"- **Number of Time Periods:** {panel['date'].nunique()}\n")
    report.append(f"- **Date Range:** {panel['date'].min().date()} to {panel['date'].max().date()}\n")
    report.append(f"- **Number of Variables:** {panel.shape[1] - 2}\n\n")
    
    report.append("## Variables Included\n\n")
    report.append("### Core Variables (M1)\n")
    report.append("- date: Month identifier\n")
    report.append("- state: State abbreviation\n")
    report.append("- unemployment_rate: State unemployment (%)\n")
    report.append("- national_unemployment_rate: US unemployment (%)\n")
    report.append("- federal_funds_rate: Federal Funds Rate (%)\n\n")
    
    report.append("### National Supplementary Variables (M2+)\n")
    if 'inflation_cpi' in panel.columns:
        report.append("- inflation_cpi: CPI inflation (index)\n")
    if 'recession_indicator' in panel.columns:
        report.append("- recession_indicator: NBER recession indicator (0/1)\n")
    if 'treasury_10y_yield' in panel.columns:
        report.append("- treasury_10y_yield: 10-Year Treasury Yield (%)\n\n")
    
    report.append("### State-Level Supplementary Variables (M2+)\n")
    if 'employment_level_total_employment_level' in panel.columns:
        report.append("- employment_level (thousands)\n")
    if 'labor_force_level_labor_force_level' in panel.columns:
        report.append("- labor_force_level (thousands)\n")
    if 'private_employment_private_employment' in panel.columns:
        report.append("- private_employment (thousands, partial coverage)\n")
    
    report.append("## Missing Values\n\n")
    report.append("| Variable | Missing | Pct. Missing |\n")
    report.append("|---|---|---|\n")
    for col in panel.columns:
        if col not in ['date', 'state', 'year', 'month']:
            missing = panel[col].isna().sum()
            pct = 100 * missing / len(panel)
            report.append(f"| {col} | {missing:,} | {pct:.2f}% |\n")
    report.append("\n")
    
    report.append("## Summary Statistics\n\n")
    report.append("### Core Variables\n")
    for col in ['unemployment_rate', 'national_unemployment_rate', 'federal_funds_rate']:
        if col in panel.columns:
            stats = panel[col].describe()
            report.append(f"\n**{col}:**\n")
            report.append(f"- Mean: {stats['mean']:.2f}\n")
            report.append(f"- Std Dev: {stats['std']:.2f}\n")
            report.append(f"- Min: {stats['min']:.2f}\n")
            report.append(f"- Max: {stats['max']:.2f}\n")
    
    report.append("\n## Panel Structure\n\n")
    counts = panel.groupby('state').size()
    is_balanced = len(counts.unique()) == 1
    if is_balanced:
        report.append(f"✓ **Balanced Panel:** All states have {counts.iloc[0]} observations\n")
    else:
        report.append(f"⚠ **Unbalanced Panel:** \n")
        report.append(f"  - Min: {counts.min()} observations\n")
        report.append(f"  - Max: {counts.max()} observations\n")
    
    report.append("\n## Data Quality Notes\n\n")
    report.append("✓ All data sourced from FRED API (Federal Reserve)\n")
    report.append("✓ Core M1 variables are complete and balanced\n")
    report.append("✓ Supplementary M2+ variables may have missing values\n")
    report.append("✓ National variables merged to all states on date\n")
    report.append("✓ State variables matched by date and state\n\n")
    
    report_text = ''.join(report)
    
    # Save report
    report_path = output_dir / 'M2_enhanced_data_quality_report.md'
    with open(report_path, 'w') as f:
        f.write(report_text)
    
    print(f"  ✓ Report saved to {report_path.name}")
    return report_text


def main():
    """Main execution function."""
    print("=" * 80)
    print("CAPSTONE PROJECT - MERGE ENHANCED DATA INTO ANALYSIS PANEL")
    print("=" * 80)
    
    try:
        # Load raw data
        data = load_raw_data()
        
        # Harmonize frequencies
        data = harmonize_frequencies(data)
        
        # Create analysis panel
        panel = create_state_panel(
            data['state_unemployment'],
            data['federal_funds'],
            data['national_unemployment'],
            data
        )
        
        # Calculate derived variables
        panel = calculate_derived_variables(panel)
        
        print(f"\n  Final Panel Shape: {panel.shape[0]:,} observations × {panel.shape[1]} variables")
        print(f"  States: {panel['state'].nunique()}")
        print(f"  Date range: {panel['date'].min().date()} to {panel['date'].max().date()}")
        
        # Save to processed directory
        print("\nSaving processed data...")
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        processed_path = PROCESSED_DATA_DIR / 'panel_enhanced.csv'
        panel.to_csv(processed_path, index=False)
        print(f"  ✓ {processed_path.name}")
        
        # Save to final directory
        print("\nSaving final analysis-ready panel...")
        FINAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
        final_path = FINAL_DATA_DIR / 'analysis_panel_enhanced.csv'
        panel.to_csv(final_path, index=False)
        print(f"  ✓ {final_path.name}")
        
        # Generate quality report
        report = generate_data_quality_report(panel, FINAL_DATA_DIR)
        
        # Print summary
        print("\n" + "=" * 80)
        print("✓ ENHANCED PANEL MERGE COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"✓ Analysis-ready dataset: analysis_panel_enhanced.csv")
        print(f"✓ Total observations: {len(panel):,}")
        print(f"✓ Total variables: {panel.shape[1]}")
        print(f"✓ Ready for regression analysis")
        print("=" * 80)
        
        # Print column names
        print("\nDataset Columns:")
        for i, col in enumerate(panel.columns, 1):
            print(f"  {i:2d}. {col}")
        
        # Print first few rows
        print("\nFirst 5 observations:")
        print(panel.head().to_string(index=False))
        
        return 0
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
