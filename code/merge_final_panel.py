"""
Capstone Project - Data Panel Merger
====================================

This script merges raw FRED data into analysis-ready panel format.

It combines:
  1. Federal Funds Rate (national, monthly)
  2. National Unemployment Rate (national, monthly)
  3. State Unemployment Rates (all 50 states, monthly)

Into a clean panel structure for regression analysis.

Usage:
    python merge_final_panel.py
"""

import sys
from pathlib import Path
import pandas as pd
import numpy as np

sys.path.insert(0, str(Path(__file__).parent))
from config_paths import RAW_DATA_DIR, PROCESSED_DATA_DIR, FINAL_DATA_DIR

# ==============================================================================
# FUNCTIONS
# ==============================================================================

def load_raw_data():
    """Load all raw data files."""
    print("Loading raw data files...")
    
    files_to_load = {
        'federal_funds': 'federal_funds_rate.csv',
        'national_unemployment': 'national_unemployment_rate.csv',
        'state_unemployment': 'state_unemployment_rates.csv',
    }
    
    data = {}
    for key, filename in files_to_load.items():
        filepath = RAW_DATA_DIR / filename
        if not filepath.exists():
            raise FileNotFoundError(f"Missing raw data file: {filename}")
        
        df = pd.read_csv(filepath)
        df['date'] = pd.to_datetime(df['date'])
        data[key] = df
        print(f"  ✓ {filename}: {len(df):,} rows")
    
    return data


def create_state_panel(state_unemployment_df, federal_funds_df, national_unemployment_df):
    """
    Create analysis-ready panel combining state unemployment with federal rates.
    
    Parameters:
        state_unemployment_df: DataFrame with columns [date, state, unemployment_rate]
        federal_funds_df: DataFrame with columns [date, federal_funds_rate]
        national_unemployment_df: DataFrame with columns [date, national_unemployment_rate]
    
    Returns:
        Panel DataFrame with columns:
        [date, state, unemployment_rate, national_unemployment_rate, federal_funds_rate]
    """
    print("\nCreating analysis panel...")
    
    # Sort federal funds by date for merging
    federal_funds_df = federal_funds_df.sort_values('date').reset_index(drop=True)
    national_unemployment_df = national_unemployment_df.sort_values('date').reset_index(drop=True)
    state_unemployment_df = state_unemployment_df.sort_values('date').reset_index(drop=True)
    
    # Get the date range that all datasets have in common
    common_start = max(
        state_unemployment_df['date'].min(),
        federal_funds_df['date'].min(),
        national_unemployment_df['date'].min()
    )
    common_end = min(
        state_unemployment_df['date'].max(),
        federal_funds_df['date'].max(),
        national_unemployment_df['date'].max()
    )
    
    print(f"  Date range: {common_start.date()} to {common_end.date()}")
    
    # Merge federal funds with national unemployment
    national_data = federal_funds_df.merge(
        national_unemployment_df,
        on='date',
        how='inner'
    )
    
    # Merge with state unemployment
    # This creates state-level observations with national factors
    panel = state_unemployment_df.merge(
        national_data,
        on='date',
        how='inner'
    )
    
    # Filter to common date range (should already be in range, but just in case)
    panel = panel[
        (panel['date'] >= common_start) & 
        (panel['date'] <= common_end)
    ].reset_index(drop=True)
    
    # Reorder columns for clarity
    panel = panel[[
        'date',
        'state',
        'unemployment_rate',
        'national_unemployment_rate',
        'federal_funds_rate'
    ]]
    
    # Sort by date and state
    panel = panel.sort_values(['date', 'state']).reset_index(drop=True)
    
    print(f"  Panel shape: {panel.shape[0]:,} observations × {panel.shape[1]} variables")
    print(f"  States: {panel['state'].nunique()}")
    print(f"  Date range: {panel['date'].min().date()} to {panel['date'].max().date()}")
    
    return panel


def generate_data_quality_report(panel, output_dir):
    """Generate summary statistics and quality report."""
    print("\nGenerating data quality report...")
    
    report = []
    report.append("# M1 Data Quality Report\n")
    report.append(f"Generated: {pd.Timestamp.now().isoformat()}\n\n")
    
    report.append("## Panel Overview\n")
    report.append(f"- **Total Observations:** {len(panel):,}\n")
    report.append(f"- **Number of States:** {panel['state'].nunique()}\n")
    report.append(f"- **Number of Time Periods:** {panel['date'].nunique()}\n")
    report.append(f"- **Date Range:** {panel['date'].min().date()} to {panel['date'].max().date()}\n")
    report.append(f"- **Variables:** {', '.join(panel.columns.tolist())}\n\n")
    
    report.append("## Missing Values\n\n")
    report.append("| Variable | Missing | Pct. Missing |\n")
    report.append("|---|---|---|\n")
    for col in panel.columns:
        if col != 'date' and col != 'state':
            missing = panel[col].isna().sum()
            pct = 100 * missing / len(panel)
            report.append(f"| {col} | {missing} | {pct:.2f}% |\n")
    report.append("\n")
    
    report.append("## Summary Statistics\n\n")
    report.append("### Unemployment Rate (State-Level)\n")
    stats = panel['unemployment_rate'].describe()
    report.append(f"- **Mean:** {stats['mean']:.2f}%\n")
    report.append(f"- **Std Dev:** {stats['std']:.2f}%\n")
    report.append(f"- **Min:** {stats['min']:.2f}% (Date: {panel.loc[panel['unemployment_rate'].idxmin(), 'date'].date()})\n")
    report.append(f"- **Max:** {stats['max']:.2f}% (Date: {panel.loc[panel['unemployment_rate'].idxmax(), 'date'].date()})\n\n")
    
    report.append("### National Unemployment Rate\n")
    stats = panel['national_unemployment_rate'].describe()
    report.append(f"- **Mean:** {stats['mean']:.2f}%\n")
    report.append(f"- **Std Dev:** {stats['std']:.2f}%\n")
    report.append(f"- **Min:** {stats['min']:.2f}%\n")
    report.append(f"- **Max:** {stats['max']:.2f}%\n\n")
    
    report.append("### Federal Funds Rate\n")
    stats = panel['federal_funds_rate'].describe()
    report.append(f"- **Mean:** {stats['mean']:.2f}%\n")
    report.append(f"- **Std Dev:** {stats['std']:.2f}%\n")
    report.append(f"- **Min:** {stats['min']:.2f}%\n")
    report.append(f"- **Max:** {stats['max']:.2f}%\n\n")
    
    report.append("## Panel Structure Verification\n\n")
    
    # Check if balanced panel
    counts = panel.groupby('state').size()
    is_balanced = len(counts.unique()) == 1
    if is_balanced:
        report.append("✓ **Balanced Panel:** All states have same number of observations\n")
        report.append(f"  - Observations per state: {counts.iloc[0]}\n")
    else:
        report.append("⚠ **Unbalanced Panel:** States have different number of observations\n")
        report.append(f"  - Min: {counts.min()} observations\n")
        report.append(f"  - Max: {counts.max()} observations\n")
    
    report.append("\n## Data Quality Notes\n\n")
    report.append("✓ Data sourced directly from FRED API (Federal Reserve)\n")
    report.append("✓ Unemployment rates are monthly averages in percentages\n")
    report.append("✓ Federal Funds Rate is primary credit rate, monthly average\n")
    report.append("✓ No data imputation; missing values removed at merge stage\n")
    
    report_text = ''.join(report)
    
    # Save report
    report_path = output_dir / 'M1_data_quality_report.md'
    with open(report_path, 'w') as f:
        f.write(report_text)
    
    print(f"  ✓ Report saved to {report_path.name}")
    
    return report_text


def main():
    """Main execution function."""
    print("=" * 70)
    print("CAPSTONE PROJECT - MERGE DATA INTO ANALYSIS PANEL")
    print("=" * 70)
    
    try:
        # Load raw data
        data = load_raw_data()
        
        # Create analysis panel
        panel = create_state_panel(
            data['state_unemployment'],
            data['federal_funds'],
            data['national_unemployment']
        )
        
        # Save to processed directory (intermediate output)
        print("\nSaving processed data...")
        PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
        processed_path = PROCESSED_DATA_DIR / 'panel_processed.csv'
        panel.to_csv(processed_path, index=False)
        print(f"  ✓ {processed_path.name}")
        
        # Save to final directory (analysis-ready)
        print("\nSaving final analysis-ready panel...")
        FINAL_DATA_DIR.mkdir(parents=True, exist_ok=True)
        final_path = FINAL_DATA_DIR / 'analysis_panel.csv'
        panel.to_csv(final_path, index=False)
        print(f"  ✓ {final_path.name}")
        
        # Generate quality report
        report = generate_data_quality_report(panel, FINAL_DATA_DIR)
        
        # Print summary
        print("\n" + "=" * 70)
        print("✓ Panel merge completed successfully!")
        print(f"✓ Data saved to: {FINAL_DATA_DIR}")
        print(f"✓ Ready for analysis with {len(panel):,} observations")
        print("=" * 70)
        
        # Print first few rows
        print("\nFirst 10 observations of analysis panel:")
        print(panel.head(10).to_string(index=False))
        
        return 0
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
