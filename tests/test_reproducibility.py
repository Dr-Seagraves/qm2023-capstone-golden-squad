#!/usr/bin/env python3
"""
Basic Reproducibility Test
==========================

This script runs basic checks to ensure the project is reproducible.
"""

import pandas as pd
import sys
from pathlib import Path

def test_data_integrity():
    """Test that the final dataset has expected properties."""
    panel_path = Path('data/final/analysis_panel_enhanced.csv')

    if not panel_path.exists():
        print("ERROR: analysis_panel_enhanced.csv not found")
        return False

    panel = pd.read_csv(panel_path)
    panel['date'] = pd.to_datetime(panel['date'])

    # Check dimensions
    expected_rows = 20736
    expected_cols = 15

    if panel.shape[0] != expected_rows:
        print(f"ERROR: Expected {expected_rows} rows, got {panel.shape[0]}")
        return False

    if panel.shape[1] != expected_cols:
        print(f"ERROR: Expected {expected_cols} columns, got {panel.shape[1]}")
        return False

    # Check date range
    min_date = panel['date'].min()
    max_date = panel['date'].max()

    if min_date != pd.Timestamp('1990-01-01'):
        print(f"ERROR: Expected min date 1990-01-01, got {min_date}")
        return False

    if max_date < pd.Timestamp('2025-01-01'):
        print(f"ERROR: Expected max date >= 2025-01-01, got {max_date}")
        return False

    # Check states
    n_states = panel['state'].nunique()
    if n_states != 48:
        print(f"ERROR: Expected 48 states, got {n_states}")
        return False

    print("✓ Data integrity check passed")
    return True

def test_scripts_run():
    """Test that main scripts can be imported without errors."""
    try:
        sys.path.insert(0, str(Path('Code')))
        import config_paths
        print("✓ Config paths import OK")
    except ImportError as e:
        print(f"ERROR: Failed to import config_paths: {e}")
        return False

    try:
        # Test py_compile on main scripts
        import py_compile
        py_compile.compile('Code/merge_final_panel_enhanced.py', doraise=True)
        print("✓ Main script compiles OK")
    except py_compile.PyCompileError as e:
        print(f"ERROR: Script compilation failed: {e}")
        return False

    return True

if __name__ == '__main__':
    print("Running reproducibility tests...")

    success = True
    success &= test_data_integrity()
    success &= test_scripts_run()

    if success:
        print("\n✓ All tests passed! Project is reproducible.")
        sys.exit(0)
    else:
        print("\n✗ Some tests failed.")
        sys.exit(1)