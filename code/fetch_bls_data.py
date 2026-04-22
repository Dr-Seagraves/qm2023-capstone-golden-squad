"""
Fetch Supplementary Data from BLS API
======================================

This script fetches 10 supplementary economic variables from the BLS API
using the provided API key via direct requests.
"""

import os
import requests
import pandas as pd
from pathlib import Path

# Import config
from config_paths import RAW_DATA_DIR

def fetch_bls_series(series_id, name, api_key, start_year=1990, end_year=2025):
    """Fetch a series from BLS API using requests."""
    url = 'https://api.bls.gov/publicAPI/v2/timeseries/data/'
    headers = {'Content-type': 'application/json'}
    data = {
        "seriesid": [series_id],
        "startyear": str(start_year),
        "endyear": str(end_year),
        "registrationkey": api_key
    }
    
    print(f"Fetching {name} ({series_id})...")
    try:
        response = requests.post(url, json=data, headers=headers)
        response.raise_for_status()
        json_data = response.json()
        
        if json_data['status'] != 'REQUEST_SUCCEEDED':
            print(f"  ✗ API Error: {json_data.get('message', 'Unknown error')}")
            return None
        
        series_data = json_data['Results']['series'][0]['data']
        records = []
        for item in series_data:
            year = int(item['year'])
            period = item['period']
            if period.startswith('M'):
                month = int(period[1:])
                date = f"{year}-{month:02d}-01"
                value = float(item['value'])
                records.append({'date': date, 'value': value})
        
        df = pd.DataFrame(records)
        df['date'] = pd.to_datetime(df['date'])
        df = df.sort_values('date').reset_index(drop=True)
        df = df.rename(columns={'value': name.lower().replace(' ', '_')})
        print(f"  ✓ Fetched {len(df)} observations")
        return df
    except Exception as e:
        print(f"  ✗ Failed: {e}")
        return None

def main():
    # Get BLS API key from environment
    api_key = os.getenv('BLS_API_KEY')
    if not api_key:
        print("ERROR: BLS_API_KEY environment variable not set!")
        print("Please set it with: export BLS_API_KEY=your_key_here")
        print("Or add it to your .env file")
        return 1
    
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    
    series = [
        ('CUUR0000SA0', 'cpi'),
        ('CES0000000001', 'total_nonfarm_employment'),
        ('LNS11000000', 'civilian_labor_force'),
        ('CES0500000001', 'total_private_employment'),
        ('CES3000000001', 'manufacturing_employment'),
        ('CES2000000001', 'construction_employment'),
        ('CES0500000003', 'average_hourly_earnings'),
        ('JTS000000000000000JOL', 'job_openings'),
        ('JTS000000000000000QUR', 'quits_rate'),
        ('LNS12000000', 'employment_level')
    ]
    
    for series_id, name in series:
        df = fetch_bls_series(series_id, name, api_key)
        if df is not None:
            filename = f"{name}.csv"
            filepath = RAW_DATA_DIR / filename
            df.to_csv(filepath, index=False)
            print(f"  ✓ Saved to {filepath}")
    
    print("\nBLS data fetch complete!")

if __name__ == '__main__':
    main()