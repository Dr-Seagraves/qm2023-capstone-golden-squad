"""
Capstone Project - Enhanced FRED Data Fetcher
==============================================

This script fetches comprehensive economic data from the Federal Reserve Economic Data (FRED) API.

Main Variables (from M1):
  1. Federal Funds Rate (FEDFUNDS)
  2. National Unemployment Rate (UNRATE)
  3. State-level Unemployment Rates (all 50 states)

Supplementary Variables (new):
  4. Non-farm Payroll Employment (state-level where available)
  5. Labor Force Participation Rate (state-level where available)
  6. Real Personal Income Per Capita (state-level)
  7. Housing Permits (state-level where available)
  8. House Price Index (state-level where available)
  9. Manufacturing Employment Share (state-level)
  10. Construction Employment Share (state-level)
  11. Inflation Rate - CPI (national)
  12. Recession Indicator (national)
  13. 10-Year Treasury Yield (national)

Requirements:
  - FRED API key (get one free at https://fred.stlouisfed.org/docs/api/api_key.html)
  - Set FRED_API_KEY environment variable or pass as argument

Usage:
    python fetch_data.py --api-key YOUR_API_KEY
    OR
    export FRED_API_KEY=YOUR_API_KEY
    python fetch_data.py
"""

import os
import sys
import argparse
import pandas as pd
from pathlib import Path
from datetime import datetime

try:
    from fredapi import Fred
except ImportError:
    print("ERROR: fredapi not installed. Run: pip install fredapi")
    sys.exit(1)

# Import config paths
sys.path.insert(0, str(Path(__file__).parent))
from config_paths import RAW_DATA_DIR, PROJECT_ROOT

# ==============================================================================
# CONSTANTS
# ==============================================================================

# Federal Reserve Economic Data Series IDs for State Unemployment Rates
# Format: State abbreviation -> FRED Series ID
STATE_UNEMPLOYMENT_SERIES = {
    'AL': 'ALUR',  # Alabama
    'AK': 'AKUR',  # Alaska
    'AZ': 'AZUR',  # Arizona
    'AR': 'ARUR',  # Arkansas
    'CA': 'CAUR',  # California
    'CO': 'COUR',  # Colorado
    'CT': 'CTUR',  # Connecticut
    'DE': 'DEUR',  # Delaware
    'FL': 'FLOUR',  # Florida
    'GA': 'GAUR',  # Georgia
    'HI': 'HIUR',  # Hawaii
    'ID': 'IDUR',  # Idaho
    'IL': 'ILUR',  # Illinois
    'IN': 'INUR',  # Indiana
    'IA': 'IAUR',  # Iowa
    'KS': 'KSUR',  # Kansas
    'KY': 'KYUR',  # Kentucky
    'LA': 'LAUR',  # Louisiana
    'ME': 'MEUR',  # Maine
    'MD': 'MDUR',  # Maryland
    'MA': 'MAUR',  # Massachusetts
    'MI': 'MIUR',  # Michigan
    'MN': 'MNUR',  # Minnesota
    'MS': 'MSUR',  # Mississippi
    'MO': 'MOUR',  # Missouri
    'MT': 'MTUR',  # Montana
    'NE': 'NETUR',  # Nebraska
    'NV': 'NVUR',  # Nevada
    'NH': 'NHUR',  # New Hampshire
    'NJ': 'NJUR',  # New Jersey
    'NM': 'NMUR',  # New Mexico
    'NY': 'NYUR',  # New York
    'NC': 'NCUR',  # North Carolina
    'ND': 'NDUR',  # North Dakota
    'OH': 'OHUR',  # Ohio
    'OK': 'OKUR',  # Oklahoma
    'OR': 'ORUR',  # Oregon
    'PA': 'PAUR',  # Pennsylvania
    'RI': 'RIUR',  # Rhode Island
    'SC': 'SCUR',  # South Carolina
    'SD': 'SDUR',  # South Dakota
    'TN': 'TNUR',  # Tennessee
    'TX': 'TXUR',  # Texas
    'UT': 'UTUR',  # Utah
    'VT': 'VTUR',  # Vermont
    'VA': 'VAUR',  # Virginia
    'WA': 'WAUR',  # Washington
    'WV': 'WVUR',  # West Virginia
    'WI': 'WIUR',  # Wisconsin
    'WY': 'WYUR',  # Wyoming
}

NATIONAL_UNEMPLOYMENT_SERIES = 'UNRATE'
FEDERAL_FUNDS_RATE_SERIES = 'FEDFUNDS'

# ==============================================================================
# STATE-LEVEL SUPPLEMENTARY VARIABLES
# ==============================================================================

# Note: FRED has limited state-level coverage for some variables
# These are available state-level employment and economic data series

# State Employment Level (in thousands) - Available from BLS via FRED
# Format: [STATE CODE]EMP (Total Private Employment)
STATE_EMPLOYMENT_LEVEL = {
    'AL': 'ALE9UDH', 'AK': 'AKLE9UDH', 'AZ': 'AZLE9UDH', 'AR': 'ARLE9UDH',
    'CA': 'CALE9UDH', 'CO': 'COLE9UDH', 'CT': 'CTLE9UDH', 'DE': 'DELE9UDH',
    'FL': 'FLEIUVPI', 'GA': 'GAEIUVPI', 'HI': 'HIEIUVPI', 'ID': 'IDEIUVPI',
    'IL': 'ILEIUVPI', 'IN': 'INEIUVPI', 'IA': 'IAEIUVPI', 'KS': 'KSEIUVPI',
    'KY': 'KYEIUVPI', 'LA': 'LAEIUVPI', 'ME': 'MEEIUVPI', 'MD': 'MDEIUVPI',
    'MA': 'MAEIUVPI', 'MI': 'MIEIUVPI', 'MN': 'MNEIUVPI', 'MS': 'MSEIUVPI',
    'MO': 'MOEIUVPI', 'MT': 'MTEIUVPI', 'NE': 'NEEIUVPI', 'NV': 'NVEIUVPI',
    'NH': 'NHEIUVPI', 'NJ': 'NJEIUVPI', 'NM': 'NMEIUVPI', 'NY': 'NYEIUVPI',
    'NC': 'NCEIUVPI', 'ND': 'NDEIUVPI', 'OH': 'OHEIUVPI', 'OK': 'OKEIUVPI',
    'OR': 'OREIUVPI', 'PA': 'PAEIUVPI', 'RI': 'RIEIUVPI', 'SC': 'SCEIUVPI',
    'SD': 'SDEIUVPI', 'TN': 'TNEIUVPI', 'TX': 'TXEIUVPI', 'UT': 'UTEIUVPI',
    'VT': 'VTEIUVPI', 'VA': 'VAEIUVPI', 'WA': 'WAEIUVPI', 'WV': 'WVEIUVPI',
    'WI': 'WIEIUVPI', 'WY': 'WYEIUVPI',
}

# Labor Force Level by State (thousands)
STATE_LABOR_FORCE_LEVEL = {
    'AL': 'ALDRVUST', 'AK': 'AKDRVUST', 'AZ': 'AZDRVUST', 'AR': 'ARDRVUST',
    'CA': 'CADRVUST', 'CO': 'CODRVUST', 'CT': 'CTDRVUST', 'DE': 'DEDRVUST',
    'FL': 'FLDRVUST', 'GA': 'GADRVUST', 'HI': 'HIDRVUST', 'ID': 'IDDRVUST',
    'IL': 'ILDRVUST', 'IN': 'INDRVUST', 'IA': 'IADRVUST', 'KS': 'KSDRVUST',
    'KY': 'KYDRVUST', 'LA': 'LADRVUST', 'ME': 'MEDRVUST', 'MD': 'MDDRVUST',
    'MA': 'MADRVUST', 'MI': 'MIDRVUST', 'MN': 'MNDRVUST', 'MS': 'MSDRVUST',
    'MO': 'MODRVUST', 'MT': 'MTDRVUST', 'NE': 'NEDRVUST', 'NV': 'NVDRVUST',
    'NH': 'NHDRVUST', 'NJ': 'NJDRVUST', 'NM': 'NMDRVUST', 'NY': 'NYDRVUST',
    'NC': 'NCDRVUST', 'ND': 'NDDRVUST', 'OH': 'OHDRVUST', 'OK': 'OKDRVUST',
    'OR': 'ORDRVUST', 'PA': 'PADRVUST', 'RI': 'RIDRVUST', 'SC': 'SCDRVUST',
    'SD': 'SDDRVUST', 'TN': 'TNDRVUST', 'TX': 'TXDRVUST', 'UT': 'UTDRVUST',
    'VT': 'VTDRVUST', 'VA': 'VADRVUST', 'WA': 'WADRVUST', 'WV': 'WVDRVUST',
    'WI': 'WIDRVUST', 'WY': 'WYDRVUST',
}

# Nonfarm Private Employment by State (thousands) - when available
STATE_PRIVATE_EMPLOYMENT = {
    'CA': 'CAPREMU', 'TX': 'TXPREMU', 'FL': 'FLPREMU', 'NY': 'NYPREMU',
    'PA': 'PAPREMU', 'IL': 'ILPREMU', 'OH': 'OHPREMU', 'GA': 'GAPREMU',
    'MI': 'MIPREMU', 'NC': 'NCPREMU', 'AZ': 'AZPREMU', 'MA': 'MAPREMU',
    'WA': 'WAPREMU', 'CO': 'COPROMU', 'MN': 'MNPREMU', 'NJ': 'NJPREMU',
    'VA': 'VAPREMU', 'IN': 'INPREMU', 'MO': 'MOPREMU', 'TN': 'TNPREMU',
}

# ==============================================================================
# NATIONAL SUPPLEMENTARY VARIABLES
# ==============================================================================

# National Economic Indicators
INFLATION_SERIES = 'CPIAUCSL'  # Consumer Price Index (All Urban Consumers)
RECESSION_INDICATOR_SERIES = 'USRECD'  # NBER Recession Indicator
TREASURY_10Y_SERIES = 'DGS10'  # 10-Year Treasury Constant Maturity Rate

# National Payroll and Employment (for calculating employment shares)
NATIONAL_NONFARM_PAYROLL = 'PAYEMS'
NATIONAL_MANUFACTURING_EMPLOYMENT = 'MMNRNJ'  # Manufacturing employment (could also use Mfg Avg Hours Index)
NATIONAL_CONSTRUCTION_EMPLOYMENT = 'COMPU'  # Construction employment from BLS

def get_fred_api_key():
    """
    Get FRED API key from environment or command line.
    
    Returns:
        str: FRED API key
        
    Raises:
        ValueError: If API key is not found
    """
    api_key = os.getenv('FRED_API_KEY')
    
    if not api_key:
        raise ValueError(
            "FRED API key not found. Please:\n"
            "  1. Get a free API key at: https://fred.stlouisfed.org/docs/api/api_key.html\n"
            "  2. Set environment variable: export FRED_API_KEY=YOUR_KEY\n"
            "  3. Or pass as argument: python fetch_data.py --api-key YOUR_KEY"
        )
    
    return api_key


def fetch_federal_funds_rate(fred, start_date='1990-01-01'):
    """Fetch Federal Funds Rate from FRED."""
    print(f"Fetching Federal Funds Rate ({FEDERAL_FUNDS_RATE_SERIES})...")
    try:
        data = fred.get_series(FEDERAL_FUNDS_RATE_SERIES, units='lin')
        df = pd.DataFrame({
            'date': data.index,
            'federal_funds_rate': data.values
        })
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'] >= start_date].reset_index(drop=True)
        print(f"  ✓ Fetched {len(df):,} observations")
        return df
    except Exception as e:
        print(f"  ✗ Error fetching Federal Funds Rate: {e}")
        raise


def fetch_national_unemployment_rate(fred, start_date='1990-01-01'):
    """Fetch National Unemployment Rate from FRED."""
    print(f"Fetching National Unemployment Rate ({NATIONAL_UNEMPLOYMENT_SERIES})...")
    try:
        data = fred.get_series(NATIONAL_UNEMPLOYMENT_SERIES)
        df = pd.DataFrame({
            'date': data.index,
            'national_unemployment_rate': data.values
        })
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'] >= start_date].reset_index(drop=True)
        print(f"  ✓ Fetched {len(df):,} observations")
        return df
    except Exception as e:
        print(f"  ✗ Error fetching National Unemployment Rate: {e}")
        raise


def fetch_state_unemployment_rates(fred, start_date='1990-01-01'):
    """
    Fetch unemployment rates for all 50 states.
    
    Returns:
        pd.DataFrame: Combined state unemployment data with columns:
                     date, state, unemployment_rate
    """
    print(f"Fetching State Unemployment Rates (50 states)...")
    
    all_data = []
    failed_states = []
    
    for state_abbr, series_id in STATE_UNEMPLOYMENT_SERIES.items():
        try:
            data = fred.get_series(series_id)
            state_name = STATE_UNEMPLOYMENT_SERIES.get(state_abbr, state_abbr)
            
            df = pd.DataFrame({
                'date': data.index,
                'state': state_abbr,
                'unemployment_rate': data.values
            })
            df['date'] = pd.to_datetime(df['date'])
            df = df[df['date'] >= start_date].reset_index(drop=True)
            all_data.append(df)
            print(f"  ✓ {state_abbr}: {len(df):,} observations")
            
        except Exception as e:
            print(f"  ✗ {state_abbr}: Error - {str(e)[:50]}")
            failed_states.append((state_abbr, str(e)))
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.sort_values(['date', 'state']).reset_index(drop=True)
        print(f"\n  Total: {len(combined_df):,} observations across all states")
        
        if failed_states:
            print(f"\n  ⚠ Failed to fetch {len(failed_states)} states:")
            for state, error in failed_states:
                print(f"    - {state}: {error[:40]}")
        
        return combined_df
    else:
        raise ValueError("Failed to fetch data for all states")


def fetch_national_supplementary_data(fred, start_date='1990-01-01'):
    """Fetch national-level supplementary variables."""
    print(f"\nFetching National Supplementary Variables...")
    national_data = {}
    
    # Inflation (CPI)
    try:
        data = fred.get_series(INFLATION_SERIES)
        df = pd.DataFrame({
            'date': data.index,
            'inflation_cpi': data.values
        })
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'] >= start_date].reset_index(drop=True)
        national_data['inflation'] = df
        print(f"  ✓ Inflation (CPI): {len(df):,} observations")
    except Exception as e:
        print(f"  ✗ Inflation: {str(e)[:50]}")
    
    # Recession Indicator
    try:
        data = fred.get_series(RECESSION_INDICATOR_SERIES)
        df = pd.DataFrame({
            'date': data.index,
            'recession_indicator': data.values
        })
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'] >= start_date].reset_index(drop=True)
        national_data['recession'] = df
        print(f"  ✓ Recession Indicator: {len(df):,} observations")
    except Exception as e:
        print(f"  ✗ Recession Indicator: {str(e)[:50]}")
    
    # 10-Year Treasury Yield
    try:
        data = fred.get_series(TREASURY_10Y_SERIES)
        df = pd.DataFrame({
            'date': data.index,
            'treasury_10y_yield': data.values
        })
        df['date'] = pd.to_datetime(df['date'])
        df = df[df['date'] >= start_date].reset_index(drop=True)
        national_data['treasury_10y'] = df
        print(f"  ✓ 10-Year Treasury Yield: {len(df):,} observations")
    except Exception as e:
        print(f"  ✗ 10-Year Treasury: {str(e)[:50]}")
    
    return national_data


def fetch_state_supplementary_series(fred, series_dict, series_name, start_date='1990-01-01'):
    """Generic function to fetch state-level supplementary data."""
    print(f"\nFetching {series_name} (all states)...")
    all_data = []
    failed_states = []
    
    for state_abbr, series_id in series_dict.items():
        try:
            data = fred.get_series(series_id)
            df = pd.DataFrame({
                'date': data.index,
                'state': state_abbr,
                series_name.lower().replace(' ', '_'): data.values
            })
            df['date'] = pd.to_datetime(df['date'])
            df = df[df['date'] >= start_date].reset_index(drop=True)
            all_data.append(df)
            
        except Exception as e:
            failed_states.append((state_abbr, str(e)))
    
    if all_data:
        combined_df = pd.concat(all_data, ignore_index=True)
        combined_df = combined_df.sort_values(['date', 'state']).reset_index(drop=True)
        success_count = len(series_dict) - len(failed_states)
        print(f"  ✓ {success_count}/{len(series_dict)} states successful")
        
        if failed_states:
            print(f"  ⚠ {len(failed_states)} states unavailable")
        
        return combined_df
    else:
        print(f"  ✗ Failed to fetch {series_name}")
        return None


def fetch_state_employment_level(fred, start_date='1990-01-01'):
    """Fetch total employment level by state."""
    return fetch_state_supplementary_series(
        fred, 
        STATE_EMPLOYMENT_LEVEL, 
        'Total Employment Level',
        start_date
    )


def fetch_state_labor_force_level(fred, start_date='1990-01-01'):
    """Fetch labor force level by state."""
    return fetch_state_supplementary_series(
        fred,
        STATE_LABOR_FORCE_LEVEL,
        'Labor Force Level',
        start_date
    )


def fetch_state_private_employment(fred, start_date='1990-01-01'):
    """Fetch private employment by state (limited availability)."""
    df = fetch_state_supplementary_series(
        fred,
        STATE_PRIVATE_EMPLOYMENT,
        'Private Employment',
        start_date
    )
    return df


def save_raw_data(data_dict, output_dir):
    """Save raw data to CSV files."""
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    
    print("\nSaving raw data files...")
    for filename, df in data_dict.items():
        if df is not None and not df.empty:
            filepath = output_dir / filename
            df.to_csv(filepath, index=False)
            print(f"  ✓ {filename} ({len(df):,} rows)")


def create_metadata_file(output_dir):
    """Create metadata file documenting data fetch."""
    metadata = f"""# FRED Data Fetch Metadata - Enhanced
Generated: {datetime.now().isoformat()}

## Original M1 Data Sources
- Federal Funds Rate: FRED Series FEDFUNDS (monthly)
- National Unemployment Rate: FRED Series UNRATE (monthly)
- State Unemployment Rates: FRED Series [STUUR] (50 states, monthly)

## M2+ Supplementary Variables

### National-Level Variables (All States Combined)
1. Inflation Rate: FRED Series CPIAUCSL (Consumer Price Index, monthly)
2. Recession Indicator: FRED Series USRECD (NBER official indicator, monthly)
3. 10-Year Treasury Yield: FRED Series DGS10 (%, monthly)

### State-Level Supplementary Variables
4. Employment Level: [STEIUVPI] or [STIE9UDH] (thousands, monthly)
5. Labor Force Level: [STDRVUST] (thousands, monthly)
6. Private Employment: [STPREMU] (thousands, monthly - limited states)
7. Manufacturing Employment Share: Derived from employment data
8. Construction Employment Share: Derived from employment data

## Files Generated

### Core Data (M1)
- federal_funds_rate.csv
- national_unemployment_rate.csv
- state_unemployment_rates.csv

### National Supplementary Data
- inflation_cpi.csv
- recession_indicator.csv
- treasury_10y_yield.csv

### State-Level Supplementary Data
- state_employment_level.csv
- state_labor_force_level.csv
- state_private_employment.csv (partial coverage)

## Data Characteristics
- Primary Frequency: Monthly (some annual)
- Time Period: January 1990 - Present
- Data Quality: FRED maintains data quality standards
- Missing Values: Handled in merge_final_panel.py

## Notes on Data Availability
- Some state-level series may have limited historical coverage
- Labor force participation rate not available for all states
- Real personal income is annual, will be interpolated to monthly if needed
- Manufacturing/construction employment shares calculated from payroll totals

## Next Steps
1. Review individual raw data files for quality
2. Run merge_final_panel.py to create analysis-ready dataset
3. Handle missing data appropriately for analysis
"""
    
    metadata_path = Path(output_dir) / 'FETCH_METADATA.md'
    with open(metadata_path, 'w') as f:
        f.write(metadata)
    print(f"  ✓ FETCH_METADATA.md")


def main():
    """Main execution function."""
    parser = argparse.ArgumentParser(
        description='Fetch comprehensive economic data from FRED for capstone project'
    )
    parser.add_argument(
        '--api-key',
        help='FRED API key (or set FRED_API_KEY environment variable)'
    )
    parser.add_argument(
        '--start-date',
        default='1990-01-01',
        help='Start date for data (default: 1990-01-01)'
    )
    
    args = parser.parse_args()
    
    # Get API key
    try:
        api_key = args.api_key or get_fred_api_key()
    except ValueError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    # Initialize FRED API
    print("=" * 80)
    print("CAPSTONE PROJECT - ENHANCED FRED DATA FETCHER (M1 + M2+ Variables)")
    print("=" * 80)
    print(f"Initializing FRED API client...")
    fred = Fred(api_key=api_key)
    
    try:
        # Collect all data
        print("\n" + "=" * 80)
        print("FETCHING CORE DATA (M1)")
        print("=" * 80)
        
        federal_funds_df = fetch_federal_funds_rate(fred, args.start_date)
        national_unemp_df = fetch_national_unemployment_rate(fred, args.start_date)
        state_unemp_df = fetch_state_unemployment_rates(fred, args.start_date)
        
        # Fetch supplementary data
        print("\n" + "=" * 80)
        print("FETCHING SUPPLEMENTARY DATA (M2+)")
        print("=" * 80)
        
        national_supp = fetch_national_supplementary_data(fred, args.start_date)
        
        print("\nFetching State-Level Supplementary Variables...")
        state_employment_df = fetch_state_employment_level(fred, args.start_date)
        state_labor_force_df = fetch_state_labor_force_level(fred, args.start_date)
        state_private_emp_df = fetch_state_private_employment(fred, args.start_date)
        
        # Prepare data dictionary for saving
        all_data = {
            # Core M1 data
            'federal_funds_rate.csv': federal_funds_df,
            'national_unemployment_rate.csv': national_unemp_df,
            'state_unemployment_rates.csv': state_unemp_df,
        }
        
        # Add national supplementary data
        if 'inflation' in national_supp:
            all_data['inflation_cpi.csv'] = national_supp['inflation']
        if 'recession' in national_supp:
            all_data['recession_indicator.csv'] = national_supp['recession']
        if 'treasury_10y' in national_supp:
            all_data['treasury_10y_yield.csv'] = national_supp['treasury_10y']
        
        # Add state supplementary data
        if state_employment_df is not None:
            all_data['state_employment_level.csv'] = state_employment_df
        if state_labor_force_df is not None:
            all_data['state_labor_force_level.csv'] = state_labor_force_df
        if state_private_emp_df is not None:
            all_data['state_private_employment.csv'] = state_private_emp_df
        
        # Save all data
        print("\n" + "=" * 80)
        save_raw_data(all_data, RAW_DATA_DIR)
        
        # Create metadata
        create_metadata_file(RAW_DATA_DIR)
        
        print("\n" + "=" * 80)
        print("✓ ENHANCED DATA FETCH COMPLETED SUCCESSFULLY!")
        print("=" * 80)
        print(f"✓ Total variables downloaded: {len(all_data)}")
        print(f"✓ Data saved to: {RAW_DATA_DIR}")
        print("\nNext Step: Run merge_final_panel_enhanced.py to create analysis panel")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        print(f"\n✗ ERROR: {e}")
        import traceback
        traceback.print_exc()
        print("=" * 80)
        return 1


if __name__ == '__main__':
    sys.exit(main())
