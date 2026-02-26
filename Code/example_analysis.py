"""
Example Analysis Script
=======================

This script demonstrates how to use the analysis_panel.csv dataset
for exploratory analysis and basic regressions.

Run after:
  1. python code/fetch_data.py
  2. python code/merge_final_panel.py
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import sys

# Add code directory to path for imports
sys.path.insert(0, str(Path(__file__).parent / 'code'))
from config_paths import FINAL_DATA_DIR, FIGURES_DIR

# ==============================================================================
# LOAD DATA
# ==============================================================================

def load_analysis_panel():
    """Load the analysis-ready panel dataset."""
    panel_path = FINAL_DATA_DIR / 'analysis_panel_enhanced.csv'
    
    if not panel_path.exists():
        print(f"ERROR: {panel_path} not found!")
        print("Please run:")
        print("  1. python code/fetch_data.py")
        print("  2. python code/merge_final_panel.py")
        sys.exit(1)
    
    panel = pd.read_csv(panel_path)
    panel['date'] = pd.to_datetime(panel['date'])
    return panel


# ==============================================================================
# EXPLORATORY ANALYSIS
# ==============================================================================

def explore_data(panel):
    """Print basic data exploration."""
    print("=" * 70)
    print("DATASET OVERVIEW")
    print("=" * 70)
    print(f"\nShape: {panel.shape[0]:,} observations × {panel.shape[1]} variables")
    print(f"\nVariables:\n{panel.dtypes}")
    print(f"\nNumber of states: {panel['state'].nunique()}")
    print(f"Time period: {panel['date'].min().date()} to {panel['date'].max().date()}")
    print(f"Number of time periods: {panel['date'].nunique()}")
    
    print("\n" + "=" * 70)
    print("MISSING VALUES")
    print("=" * 70)
    print(panel.isnull().sum())
    
    print("\n" + "=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    print(panel.describe())
    
    return panel


def state_summary(panel):
    """Summary statistics by state."""
    print("\n" + "=" * 70)
    print("STATE-LEVEL UNEMPLOYMENT SUMMARY")
    print("=" * 70)
    
    state_stats = panel.groupby('state')['unemployment_rate'].agg([
        ('Mean', 'mean'),
        ('Std Dev', 'std'),
        ('Min', 'min'),
        ('Max', 'max')
    ]).round(2)
    
    state_stats = state_stats.sort_values('Mean', ascending=False)
    print("\nTop 15 states with highest average unemployment:")
    print(state_stats.head(15))
    
    print("\nTop 15 states with lowest average unemployment:")
    print(state_stats.tail(15))
    
    return state_stats


def correlation_analysis(panel):
    """Analyze correlations between variables."""
    print("\n" + "=" * 70)
    print("CORRELATION ANALYSIS")
    print("=" * 70)
    
    # Drop date and state columns for correlation
    numeric_data = panel[['unemployment_rate', 'national_unemployment_rate', 'federal_funds_rate']]
    corr_matrix = numeric_data.corr()
    
    print("\nCorrelation Matrix:")
    print(corr_matrix.round(3))
    
    # Aggregate to national level for cleaner correlation
    national_data = panel.drop_duplicates(subset=['date'])
    corr_national = national_data[['unemployment_rate', 'national_unemployment_rate', 'federal_funds_rate']].corr()
    
    print("\nCorrelation at National Aggregate Level:")
    print(corr_national.round(3))
    
    return corr_matrix


# ==============================================================================
# VISUALIZATIONS
# ==============================================================================

def plot_time_series(panel):
    """Create time series plots."""
    # Get national level data
    national = panel.drop_duplicates(subset=['date']).sort_values('date')
    
    fig, ax = plt.subplots(figsize=(14, 6))
    ax2 = ax.twinx()
    
    # Plot both variables with different y-axes
    line1 = ax.plot(national['date'], national['federal_funds_rate'], 
                    color='blue', linewidth=2, label='Federal Funds Rate')
    line2 = ax2.plot(national['date'], national['national_unemployment_rate'],
                     color='red', linewidth=2, label='National Unemployment Rate')
    
    ax.set_xlabel('Date', fontsize=12)
    ax.set_ylabel('Federal Funds Rate (%)', color='blue', fontsize=12)
    ax2.set_ylabel('Unemployment Rate (%)', color='red', fontsize=12)
    ax.tick_params(axis='y', labelcolor='blue')
    ax2.tick_params(axis='y', labelcolor='red')
    
    ax.grid(True, alpha=0.3)
    ax.set_title('Federal Funds Rate vs National Unemployment Rate Over Time', fontsize=14, fontweight='bold')
    
    # Combine legends
    lines = line1 + line2
    labels = [l.get_label() for l in lines]
    ax.legend(lines, labels, loc='upper left')
    
    plt.tight_layout()
    fig_path = FIGURES_DIR / 'time_series_trends.png'
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    print(f"\n✓ Saved: {fig_path.name}")
    return fig


def plot_state_distribution(panel):
    """Plot distribution of state unemployment rates."""
    fig, axes = plt.subplots(1, 2, figsize=(14, 5))
    
    # Histogram
    axes[0].hist(panel['unemployment_rate'], bins=50, color='steelblue', edgecolor='black', alpha=0.7)
    axes[0].set_xlabel('Unemployment Rate (%)', fontsize=11)
    axes[0].set_ylabel('Frequency', fontsize=11)
    axes[0].set_title('Distribution of State Unemployment Rates', fontsize=12, fontweight='bold')
    axes[0].grid(True, alpha=0.3)
    
    # Box plot by state
    state_order = panel.groupby('state')['unemployment_rate'].mean().sort_values(ascending=False).index
    sns.boxplot(data=panel, y='state', x='unemployment_rate', order=state_order, ax=axes[1])
    axes[1].set_xlabel('Unemployment Rate (%)', fontsize=11)
    axes[1].set_ylabel('State', fontsize=11)
    axes[1].set_title('Unemployment Rate Distribution by State', fontsize=12, fontweight='bold')
    
    plt.tight_layout()
    fig_path = FIGURES_DIR / 'state_unemployment_distribution.png'
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {fig_path.name}")
    return fig


def plot_scatter(panel):
    """Create scatter plot of unemployment vs federal funds rate."""
    # Sample data to avoid overplotting
    sample = panel.sample(n=min(5000, len(panel)), random_state=42)
    
    fig, ax = plt.subplots(figsize=(10, 7))
    scatter = ax.scatter(sample['federal_funds_rate'], sample['unemployment_rate'], 
                        c=sample['date'].astype(int), cmap='viridis', alpha=0.5, s=20)
    
    ax.set_xlabel('Federal Funds Rate (%)', fontsize=12)
    ax.set_ylabel('State Unemployment Rate (%)', fontsize=12)
    ax.set_title('Relationship: Federal Funds Rate vs State Unemployment Rate', 
                 fontsize=13, fontweight='bold')
    ax.grid(True, alpha=0.3)
    
    cbar = plt.colorbar(scatter, ax=ax)
    cbar.set_label('Time (days since epoch)', fontsize=11)
    
    # Add trend line
    sample_clean = sample.dropna(subset=['federal_funds_rate', 'unemployment_rate'])
    if len(sample_clean) > 1:
        z = np.polyfit(sample_clean['federal_funds_rate'], sample_clean['unemployment_rate'], 1)
        p = np.poly1d(z)
        x_trend = np.linspace(sample_clean['federal_funds_rate'].min(), sample_clean['federal_funds_rate'].max(), 100)
        ax.plot(x_trend, p(x_trend), "r--", linewidth=2, label=f'Trend line (slope={z[0]:.4f})')
        ax.legend()
    
    plt.tight_layout()
    fig_path = FIGURES_DIR / 'scatter_unemployment_vs_fedfunds.png'
    plt.savefig(fig_path, dpi=300, bbox_inches='tight')
    print(f"✓ Saved: {fig_path.name}")
    return fig


# ==============================================================================
# REGRESSION ANALYSIS
# ==============================================================================

def simple_regression(panel):
    """Run simple regression: unemployment_rate ~ federal_funds_rate."""
    from statsmodels.formula.api import ols
    
    print("\n" + "=" * 70)
    print("SIMPLE REGRESSION: Unemployment Rate ~ Federal Funds Rate")
    print("=" * 70)
    
    model = ols('unemployment_rate ~ federal_funds_rate', data=panel).fit()
    print(model.summary())
    
    return model


def fixed_effects_regression(panel):
    """Run fixed effects regression (by state)."""
    from statsmodels.formula.api import ols
    
    print("\n" + "=" * 70)
    print("FIXED EFFECTS REGRESSION: With State Dummies")
    print("=" * 70)
    
    # Note: This will have many coefficients (one per state)
    # In practice, use statsmodels.regression.linear_model.PanelOLS for panel data
    model = ols('unemployment_rate ~ federal_funds_rate + C(state)', data=panel).fit()
    print(model.summary())
    
    return model


# ==============================================================================
# MAIN EXECUTION
# ==============================================================================

def main():
    """Run all analyses."""
    print("\n" + "=" * 70)
    print("CAPSTONE PROJECT - EXAMPLE ANALYSIS")
    print("=" * 70 + "\n")
    
    # Load data
    print("Loading analysis panel...")
    panel = load_analysis_panel()
    print(f"✓ Loaded {len(panel):,} observations")
    
    # Exploratory analysis
    explore_data(panel)
    state_summary(panel)
    correlation_analysis(panel)
    
    # Create visualizations
    print("\n" + "=" * 70)
    print("CREATING VISUALIZATIONS")
    print("=" * 70)
    
    plot_time_series(panel)
    plot_state_distribution(panel)
    plot_scatter(panel)
    
    # Run regressions
    print("\n" + "=" * 70)
    print("RUNNING REGRESSIONS")
    print("=" * 70)
    
    simple_regression(panel)
    fixed_effects_regression(panel)
    
    print("\n" + "=" * 70)
    print("✓ ANALYSIS COMPLETE")
    print("=" * 70)
    print(f"Outputs saved to: {FIGURES_DIR}")
    print("\nNext steps:")
    print("1. Review the visualizations in results/figures/")
    print("2. Examine regression results above")
    print("3. Modify this script for your specific analysis")
    print("4. Create publication-ready tables and figures")
    print("=" * 70 + "\n")


if __name__ == '__main__':
    main()
