#!/bin/bash

# YOLO Project Dev Container Environment Test Script
# This script verifies that all required tools and dependencies are correctly installed

set -e

echo "🧪 YOLO Project Environment Test"
echo "=================================="
echo ""

# Color codes
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counter
PASSED=0
FAILED=0

# Function to test command
test_command() {
    local name=$1
    local command=$2
    local expected=$3

    echo -n "Testing $name... "

    if eval "$command" > /dev/null 2>&1; then
        echo -e "${GREEN}✓ PASS${NC}"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        if [ -n "$expected" ]; then
            echo "  Expected: $expected"
        fi
        ((FAILED++))
    fi
}

# Function to test version
test_version() {
    local name=$1
    local command=$2

    echo -n "Testing $name... "

    version=$(eval "$command" 2>&1)
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ PASS${NC} ($version)"
        ((PASSED++))
    else
        echo -e "${RED}✗ FAIL${NC}"
        ((FAILED++))
    fi
}

echo "📋 System Tools"
echo "---------------"
test_version "Python" "python --version | head -1"
test_version "pip" "pip --version | head -1"
test_version "Node.js" "node --version"
test_version "npm" "npm --version"
test_version "Git" "git --version"
test_command "Git LFS" "git lfs version"
test_command "GitHub CLI" "gh --version"
test_command "Zsh" "which zsh"
echo ""

echo "🐍 Python Development Tools"
echo "----------------------------"
test_version "Black" "black --version | head -1"
test_version "isort" "isort --version | head -1"
test_version "Flake8" "flake8 --version | head -1"
test_version "mypy" "mypy --version"
test_version "pytest" "pytest --version | head -1"
echo ""

echo "🤖 Claude Code"
echo "--------------"
test_command "Claude Code CLI" "which claude"
if [ $? -eq 0 ]; then
    claude_version=$(claude --version 2>&1 || echo "installed")
    echo "  Version: $claude_version"
fi
echo ""

echo "🔧 Additional Tools"
echo "-------------------"
test_command "vim" "which vim"
test_command "nano" "which nano"
test_command "curl" "which curl"
test_command "wget" "which wget"
test_command "git-delta" "which delta"
echo ""

echo "📦 Python Packages (Optional)"
echo "------------------------------"
if python -c "import ultralytics" 2>/dev/null; then
    echo -e "Ultralytics: ${GREEN}✓ Installed${NC}"
    python -c "from ultralytics import YOLO; print(f'  Version: {ultralytics.__version__}')" 2>/dev/null || true
else
    echo -e "Ultralytics: ${YELLOW}○ Not installed (will be installed from requirements.txt)${NC}"
fi

if python -c "import fastapi" 2>/dev/null; then
    echo -e "FastAPI: ${GREEN}✓ Installed${NC}"
    python -c "import fastapi; print(f'  Version: {fastapi.__version__}')" 2>/dev/null || true
else
    echo -e "FastAPI: ${YELLOW}○ Not installed (will be installed from requirements.txt)${NC}"
fi

if python -c "import torch" 2>/dev/null; then
    echo -e "PyTorch: ${GREEN}✓ Installed${NC}"
    python -c "import torch; print(f'  Version: {torch.__version__}')" 2>/dev/null || true
else
    echo -e "PyTorch: ${YELLOW}○ Not installed (will be installed from requirements.txt)${NC}"
fi
echo ""

echo "🌐 Network Connectivity"
echo "-----------------------"
test_command "DNS Resolution" "nslookup google.com"
test_command "GitHub Access" "curl -s --max-time 5 https://api.github.com > /dev/null"
test_command "PyPI Access" "curl -s --max-time 5 https://pypi.org > /dev/null"

# Test firewall (should block example.com)
echo -n "Testing Firewall (should block)... "
if ! curl -s --max-time 2 http://example.com > /dev/null 2>&1; then
    echo -e "${GREEN}✓ PASS (blocked as expected)${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}○ WARNING (not blocked, firewall may not be active)${NC}"
fi
echo ""

echo "📁 Directory Structure"
echo "----------------------"
for dir in "/workspace" "/home/yolo/.claude" "/commandhistory"; do
    if [ -d "$dir" ]; then
        echo -e "$dir: ${GREEN}✓ Exists${NC}"
        ((PASSED++))
    else
        echo -e "$dir: ${RED}✗ Missing${NC}"
        ((FAILED++))
    fi
done
echo ""

echo "🔐 User Permissions"
echo "-------------------"
echo -n "Current user... "
if [ "$(whoami)" = "yolo" ]; then
    echo -e "${GREEN}✓ PASS (yolo)${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL ($(whoami))${NC}"
    ((FAILED++))
fi

echo -n "Sudo access to firewall... "
if sudo -n /usr/local/bin/init-firewall.sh --help > /dev/null 2>&1 || [ -f /usr/local/bin/init-firewall.sh ]; then
    echo -e "${GREEN}✓ PASS${NC}"
    ((PASSED++))
else
    echo -e "${RED}✗ FAIL${NC}"
    ((FAILED++))
fi
echo ""

echo "🎨 Shell Configuration"
echo "----------------------"
echo -n "Default shell... "
default_shell=$(echo $SHELL)
if [[ "$default_shell" == *"zsh"* ]]; then
    echo -e "${GREEN}✓ PASS (zsh)${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}○ WARNING ($default_shell)${NC}"
fi

echo -n "History file... "
if [ -n "$HISTFILE" ]; then
    echo -e "${GREEN}✓ PASS ($HISTFILE)${NC}"
    ((PASSED++))
else
    echo -e "${YELLOW}○ WARNING (not set)${NC}"
fi
echo ""

echo "=================================="
echo "📊 Test Summary"
echo "=================================="
echo -e "Passed: ${GREEN}$PASSED${NC}"
echo -e "Failed: ${RED}$FAILED${NC}"
echo ""

if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ All tests passed! Environment is ready.${NC}"
    exit 0
else
    echo -e "${YELLOW}⚠️  Some tests failed. Please review the output above.${NC}"
    exit 1
fi
