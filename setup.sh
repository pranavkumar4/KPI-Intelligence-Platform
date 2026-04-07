#!/bin/bash

# KPI Intelligence Platform - Deployment Script
# This script sets up and runs the application

set -e

echo "========================================="
echo "KPI Intelligence Platform Setup"
echo "========================================="
echo ""

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3.11 or higher.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo -e "${GREEN}✅ Python version: $PYTHON_VERSION${NC}"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}❌ pip3 is not installed.${NC}"
    exit 1
fi

echo -e "${GREEN}✅ pip3 is installed${NC}"
echo ""

# Create virtual environment
echo -e "${YELLOW}📦 Creating virtual environment...${NC}"
if [ ! -d "venv" ]; then
    python3 -m venv venv
    echo -e "${GREEN}✅ Virtual environment created${NC}"
else
    echo -e "${GREEN}✅ Virtual environment already exists${NC}"
fi

# Activate virtual environment
echo -e "${YELLOW}🔄 Activating virtual environment...${NC}"
source venv/bin/activate

# Upgrade pip
echo -e "${YELLOW}⬆️  Upgrading pip...${NC}"
pip install --upgrade pip

# Install requirements
echo -e "${YELLOW}📥 Installing dependencies...${NC}"
pip install -r requirements.txt

echo -e "${GREEN}✅ All dependencies installed${NC}"
echo ""

# Create necessary directories
echo -e "${YELLOW}📁 Creating directories...${NC}"
mkdir -p data logs

# Generate sample data
echo -e "${YELLOW}🎲 Generating sample data...${NC}"
python generate_sample_data.py

echo ""
echo -e "${GREEN}=========================================${NC}"
echo -e "${GREEN}✅ Setup Complete!${NC}"
echo -e "${GREEN}=========================================${NC}"
echo ""
echo -e "${YELLOW}To start the application:${NC}"
echo "  streamlit run app.py"
echo ""
echo -e "${YELLOW}Or use Docker:${NC}"
echo "  docker-compose up -d"
echo ""
echo -e "${YELLOW}Access the application at:${NC}"
echo "  http://localhost:8501"
echo ""
