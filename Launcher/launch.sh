#!/bin/bash

# FTM-2077 LINUX/MAC LAUNCHER
# Usage: ./launch.sh

# Colors
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}"
echo "========================================="
echo "   FTM-2077 // OMEGA SYSTEM INITIATED    "
echo "========================================="
echo -e "${NC}"

# 1. Check Python
if ! command -v python3 &> /dev/null
then
    echo -e "${RED}[ERROR] Python3 could not be found.${NC}"
    exit 1
fi

# 2. Install Dependencies
echo -e "${GREEN}[*] INSTALLING NEURAL DEPENDENCIES...${NC}"
python3 -m pip install -r requirements.txt

# 3. Run Setup Script
echo -e "${GREEN}[*] CHECKING FILE INTEGRITY...${NC}"
if [ -f "setup_omega.py" ]; then
    python3 setup_omega.py
else
    echo -e "${RED}[WARN] setup_omega.py not found. Skipping structure check.${NC}"
fi

# 4. Open Frontend (Detect OS)
echo -e "${GREEN}[*] OPENING VISUAL INTERFACE...${NC}"
if [[ "$OSTYPE" == "darwin"* ]]; then
    open frontend/index.html # Mac
else
    xdg-open frontend/index.html # Linux
fi

# 5. Start Server
echo -e "${CYAN}"
echo "-----------------------------------------"
echo " SYSTEM ONLINE @ http://localhost:8000"
echo " Press CTRL+C to Shutdown"
echo "-----------------------------------------"
echo -e "${NC}"

# Run Uvicorn
uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
