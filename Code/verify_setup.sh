#!/bin/bash
# Project Setup Verification Script
# This script verifies that all components are set up correctly

echo "═══════════════════════════════════════════════════════════════════════════"
echo "QM 2023 CAPSTONE PROJECT - SETUP VERIFICATION"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to check file existence
check_file() {
    if [ -f "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1"
        return 1
    fi
}

# Function to check directory existence
check_dir() {
    if [ -d "$1" ]; then
        echo -e "${GREEN}✓${NC} $1"
        return 0
    else
        echo -e "${RED}✗${NC} $1"
        return 1
    fi
}

echo "1. CHECKING DIRECTORY STRUCTURE"
echo "───────────────────────────────────────────────────────────────────────────"
check_dir "code"
check_dir "data"
check_dir "data/raw"
check_dir "data/processed"
check_dir "data/final"
check_dir "results"
check_dir "results/figures"
check_dir "results/tables"
check_dir "results/reports"
echo ""

echo "2. CHECKING MAIN SCRIPTS"
echo "───────────────────────────────────────────────────────────────────────────"
check_file "Code/config_paths.py"
check_file "Code/fetch_data.py"
check_file "Code/merge_final_panel_enhanced.py"
echo ""

echo "3. CHECKING CONFIGURATION FILES"
echo "───────────────────────────────────────────────────────────────────────────"
check_file "requirements.txt"
check_file ".env.example"
echo ""

echo "4. CHECKING DOCUMENTATION"
echo "───────────────────────────────────────────────────────────────────────────"
check_file "README.md"
check_file "docs/SETUP_GUIDE.md"
check_file "docs/QUICKSTART.md"
echo ""

echo "5. CHECKING PYTHON ENVIRONMENT"
echo "───────────────────────────────────────────────────────────────────────────"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓${NC} Python found: $PYTHON_VERSION"
else
    echo -e "${RED}✗${NC} Python not found"
fi

if command -v pip3 &> /dev/null; then
    echo -e "${GREEN}✓${NC} pip found"
else
    echo -e "${RED}✗${NC} pip not found"
fi
echo ""

echo "6. CHECKING API KEYS"
echo "───────────────────────────────────────────────────────────────────────────"
if [ -n "$FRED_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} FRED_API_KEY environment variable set (${#FRED_API_KEY} chars)"
else
    echo -e "${YELLOW}⚠${NC} FRED_API_KEY environment variable not set"
    if [ -f ".env" ]; then
        echo -e "${YELLOW}  Hint: Source .env file with: export \$(cat .env | xargs)${NC}"
    else
        echo -e "${YELLOW}  Hint: Create .env file from .env.example${NC}"
    fi
fi

if [ -n "$BLS_API_KEY" ]; then
    echo -e "${GREEN}✓${NC} BLS_API_KEY environment variable set (${#BLS_API_KEY} chars)"
else
    echo -e "${YELLOW}⚠${NC} BLS_API_KEY environment variable not set"
    if [ -f ".env" ]; then
        echo -e "${YELLOW}  Hint: Source .env file with: export \$(cat .env | xargs)${NC}"
    else
        echo -e "${YELLOW}  Hint: Create .env file from .env.example${NC}"
    fi
fi
echo ""

echo "═══════════════════════════════════════════════════════════════════════════"
echo "NEXT STEPS:"
echo "═══════════════════════════════════════════════════════════════════════════"
echo ""
echo "1. If you haven't already, get your API keys:"
echo "   → FRED: https://fred.stlouisfed.org/docs/api/api_key.html"
echo "   → BLS: https://www.bls.gov/developers/"
echo ""
echo "2. Set your API keys:"
echo "   → export FRED_API_KEY=your_fred_key_here"
echo "   → export BLS_API_KEY=your_bls_key_here"
echo "   OR edit .env and run: export \$(cat .env | xargs)"
echo ""
echo "3. Fetch data from FRED:"
echo "   → python Code/fetch_data.py"
echo ""
echo "4. Fetch supplementary data from BLS (optional):"
echo "   → python Code/fetch_bls_data.py"
echo ""
echo "5. Create analysis panel:"
echo "   → python Code/merge_final_panel_enhanced.py"
echo ""
echo "5. Check your data in data/final/analysis_panel_enhanced.csv"
echo ""
echo "For more information, see docs/QUICKSTART.md or docs/SETUP_GUIDE.md"
echo "═══════════════════════════════════════════════════════════════════════════"
