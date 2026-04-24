"""
Download Missing Raw Data from FRED
====================================

This script downloads the missing supplementary raw data files from FRED
using direct CSV downloads, bypassing the API.

Missing files:
- state_employment_level.csv
- state_labor_force_level.csv
- state_private_employment.csv

National supplementary are already present.
"""

import requests
import pandas as pd
from pathlib import Path
import time

# Import config
from config_paths import RAW_DATA_DIR

def download_csv(series_id, start_date='1990-01-01'):
    """Download CSV for a series from FRED."""
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={series_id}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        # Parse CSV
        from io import StringIO
        df = pd.read_csv(StringIO(response.text))
        df['DATE'] = pd.to_datetime(df['DATE'])
        df = df[df['DATE'] >= start_date]
        df = df.rename(columns={'DATE': 'date', 'VALUE': 'value'})
        return df
    except Exception as e:
        print(f"Failed to download {series_id}: {e}")
        return None

def download_national_supplementary():
    """Download national supplementary data (if missing)."""
    series = {
        'inflation_cpi.csv': 'CPIAUCSL',
        'recession_indicator.csv': 'USRECD',
        'treasury_10y_yield.csv': 'DGS10'
    }
    for filename, series_id in series.items():
        filepath = RAW_DATA_DIR / filename
        if not filepath.exists():
            print(f"Downloading {filename}...")
            df = download_csv(series_id)
            if df is not None:
                df.to_csv(filepath, index=False)
                print(f"Saved {filepath}")
            time.sleep(1)  # Rate limit

def download_state_data(filename, series_dict):
    """Download and combine state-level data."""
    filepath = RAW_DATA_DIR / filename
    if filepath.exists():
        print(f"{filename} already exists, skipping.")
        return
    
    all_data = []
    for state, series_id in series_dict.items():
        print(f"Downloading {state} for {filename}...")
        df = download_csv(series_id)
        if df is not None:
            df['state'] = state
            df = df[['date', 'state', 'value']]
            df = df.rename(columns={'value': filename.replace('state_', '').replace('.csv', '').replace('_', ' ')})
            all_data.append(df)
        time.sleep(1)  # Rate limit
    
    if all_data:
        combined = pd.concat(all_data, ignore_index=True)
        combined = combined.sort_values(['date', 'state']).reset_index(drop=True)
        combined.to_csv(filepath, index=False)
        print(f"Saved {filepath}")

def main():
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    # Download national if missing
    download_national_supplementary()
    
    # Import the series dicts
    from fetch_data import STATE_EMPLOYMENT_LEVEL, STATE_LABOR_FORCE_LEVEL, STATE_PRIVATE_EMPLOYMENT
    
    # Download state data
    download_state_data('state_employment_level.csv', STATE_EMPLOYMENT_LEVEL)
    download_state_data('state_labor_force_level.csv', STATE_LABOR_FORCE_LEVEL)
    download_state_data('state_private_employment.csv', STATE_PRIVATE_EMPLOYMENT)
    
    print("Download complete!")

if __name__ == '__main__':
    main()