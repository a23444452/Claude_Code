#!/bin/bash

# YOLO Models Download Script
# Downloads official YOLO models for different use cases

set -e

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m'

print_success() { echo -e "${GREEN}✓ $1${NC}"; }
print_error() { echo -e "${RED}✗ $1${NC}"; }
print_warning() { echo -e "${YELLOW}⚠ $1${NC}"; }
print_info() { echo -e "${CYAN}ℹ $1${NC}"; }
print_step() { echo -e "${MAGENTA}▶ $1${NC}"; }

# Banner
echo ""
echo -e "${MAGENTA}╔════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║   YOLO Models Download Script      ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════╝${NC}"
echo ""

# Check Python and ultralytics
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found!"
    exit 1
fi

print_info "Checking ultralytics installation..."
if ! python3 -c "import ultralytics" 2>/dev/null; then
    print_error "Ultralytics not installed!"
    print_info "Install with: pip install ultralytics"
    exit 1
fi

print_success "Ultralytics found"

# Create models directory
mkdir -p models

# Model information
echo ""
print_info "YOLO11 Model Variants:"
echo ""
echo "  Model   Size    Parameters  mAP     Speed"
echo "  ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  n       6MB     2.6M       39.5%   1.5ms   (Fastest)"
echo "  s       22MB    9.4M       47.0%   2.3ms"
echo "  m       50MB    20.1M      51.5%   4.5ms   (Balanced)"
echo "  l       58MB    25.3M      53.4%   6.5ms"
echo "  x       138MB   56.9M      54.7%   10.6ms  (Most Accurate)"
echo ""

# Interactive selection or download all
if [ "$1" == "--all" ]; then
    MODELS=("n" "s" "m" "l" "x")
    print_info "Downloading all models..."
elif [ -n "$1" ]; then
    MODELS=("$@")
    print_info "Downloading selected models: ${MODELS[*]}"
else
    echo "Select models to download (space-separated, e.g., 'n s m' or 'all'):"
    read -p "Models [n]: " input

    if [ -z "$input" ]; then
        MODELS=("n")
    elif [ "$input" == "all" ]; then
        MODELS=("n" "s" "m" "l" "x")
    else
        MODELS=($input)
    fi
fi

# Download function
download_model() {
    local variant=$1
    local model_name="yolo11${variant}.pt"

    print_step "Downloading YOLO11${variant}..."

    python3 << EOF
from ultralytics import YOLO
import os

try:
    model = YOLO('yolo11${variant}.pt')
    print(f"✓ Downloaded: yolo11${variant}.pt")

    # Get file size
    if os.path.exists('yolo11${variant}.pt'):
        size = os.path.getsize('yolo11${variant}.pt')
        size_mb = size / (1024 * 1024)
        print(f"  Size: {size_mb:.1f} MB")

        # Move to models directory if not already there
        if not os.path.exists('models/yolo11${variant}.pt'):
            import shutil
            shutil.copy('yolo11${variant}.pt', 'models/yolo11${variant}.pt')
            print(f"  Copied to models/ directory")

except Exception as e:
    print(f"✗ Failed to download: {e}")
    exit(1)
EOF

    if [ $? -eq 0 ]; then
        print_success "YOLO11${variant} downloaded"
    else
        print_error "Failed to download YOLO11${variant}"
        return 1
    fi
}

# Download selected models
echo ""
for model in "${MODELS[@]}"; do
    # Validate model variant
    if [[ ! "$model" =~ ^[nsmlx]$ ]]; then
        print_warning "Invalid model variant: $model (must be n, s, m, l, or x)"
        continue
    fi

    download_model "$model"
    echo ""
done

# List downloaded models
print_step "Downloaded models:"
echo ""

if [ -d models ] && [ "$(ls -A models/*.pt 2>/dev/null)" ]; then
    ls -lh models/*.pt | awk '{print "  " $9 " (" $5 ")"}'
else
    print_warning "No models found in models/ directory"
fi

# Also check root directory
echo ""
if [ "$(ls -A *.pt 2>/dev/null)" ]; then
    print_info "Models in root directory:"
    ls -lh *.pt | awk '{print "  " $9 " (" $5 ")"}'
fi

# Summary
echo ""
echo -e "${MAGENTA}═════════════════════════════════${NC}"
echo -e "${GREEN}✅ Download complete!${NC}"
echo -e "${MAGENTA}═════════════════════════════════${NC}"
echo ""

print_info "Usage examples:"
echo "  - Training:   python src/training/train.py"
echo "  - Prediction: model = YOLO('models/yolo11n.pt')"
echo "  - API:        Specify model in src/api/main.py"
echo ""

print_info "Model selection guide:"
echo "  - Edge devices:     yolo11n"
echo "  - General use:      yolo11s or yolo11m"
echo "  - High accuracy:    yolo11l or yolo11x"
echo "  - Real-time (fast): yolo11n or yolo11s"
echo ""
