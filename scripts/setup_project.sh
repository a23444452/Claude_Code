#!/bin/bash

# YOLO Project Setup Script
# Initializes the project structure and installs dependencies

set -e

# Color codes
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
echo -e "${MAGENTA}╔═══════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║   YOLO Project Setup Script       ║${NC}"
echo -e "${MAGENTA}╚═══════════════════════════════════╝${NC}"
echo ""

# Check Python version
print_step "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found!"
    print_info "Please install Python 3.10 or later"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
print_success "Python $PYTHON_VERSION found"

# Check pip
if ! command -v pip3 &> /dev/null; then
    print_error "pip not found!"
    exit 1
fi

print_success "pip found"

# Create directory structure
print_step "Creating project directories..."

mkdir -p dataset/{images,labels}/{train,val,test}
mkdir -p models
mkdir -p runs
mkdir -p logs
mkdir -p config
mkdir -p src/{api,training,data,utils}
mkdir -p tests
mkdir -p analysis
mkdir -p monitoring
mkdir -p optimization
mkdir -p security

print_success "Project directories created"

# Create __init__.py files
print_step "Creating Python package files..."

touch src/__init__.py
touch src/api/__init__.py
touch src/training/__init__.py
touch src/data/__init__.py
touch src/utils/__init__.py
touch tests/__init__.py

print_success "Package files created"

# Create .env from example if not exists
if [ ! -f .env ]; then
    print_step "Creating .env file..."
    if [ -f .devcontainer/.env.example ]; then
        cp .devcontainer/.env.example .env
        print_success ".env file created from example"
        print_warning "Please edit .env to add your API keys and configuration"
    else
        print_warning ".env.example not found, skipping"
    fi
else
    print_info ".env file already exists"
fi

# Create config example if not exists
if [ ! -f config/data.example.yaml ] && [ -f config/data.example.yaml ]; then
    print_info "config/data.example.yaml already exists"
elif [ -f config/data.example.yaml ]; then
    print_success "config/data.example.yaml found"
else
    print_warning "config/data.example.yaml not found"
fi

# Install Python dependencies
print_step "Installing Python dependencies..."

if [ -f requirements.txt ]; then
    print_info "Installing from requirements.txt..."
    pip3 install -r requirements.txt
    print_success "Dependencies installed"
else
    print_warning "requirements.txt not found"
    print_info "Installing essential packages..."

    # Install essential packages
    pip3 install \
        ultralytics \
        fastapi \
        uvicorn \
        python-multipart \
        pillow \
        opencv-python \
        numpy \
        torch \
        torchvision

    print_success "Essential packages installed"
fi

# Download default YOLO model if not exists
print_step "Checking for YOLO model..."

if [ ! -f yolo11n.pt ]; then
    print_info "Downloading YOLO11n model..."

    python3 << 'EOF'
from ultralytics import YOLO
import os

# This will download the model if not present
model = YOLO('yolo11n.pt')
print(f"Model downloaded: {os.path.exists('yolo11n.pt')}")
EOF

    if [ -f yolo11n.pt ]; then
        print_success "YOLO11n model downloaded"
    else
        print_warning "Failed to download model, will be downloaded on first use"
    fi
else
    print_info "YOLO11n model already exists"
fi

# Initialize git if not already initialized
if [ ! -d .git ]; then
    print_step "Initializing git repository..."
    git init
    print_success "Git repository initialized"

    if [ -f .gitignore ]; then
        print_info ".gitignore already exists"
    fi
else
    print_info "Git repository already initialized"
fi

# Set up git hooks (optional)
if [ -d .git ]; then
    print_step "Setting up git hooks..."

    # Create pre-commit hook
    cat > .git/hooks/pre-commit << 'EOF'
#!/bin/bash
# Pre-commit hook to prevent committing large files

# Check for .pt files
if git diff --cached --name-only | grep -q '\.pt$'; then
    echo "Error: Attempting to commit .pt model files"
    echo "Model files should not be committed to git"
    exit 1
fi

# Check for large files (>10MB)
for file in $(git diff --cached --name-only); do
    if [ -f "$file" ]; then
        size=$(stat -f%z "$file" 2>/dev/null || stat -c%s "$file" 2>/dev/null)
        if [ "$size" -gt 10485760 ]; then
            echo "Error: File $file is larger than 10MB"
            exit 1
        fi
    fi
done

exit 0
EOF

    chmod +x .git/hooks/pre-commit
    print_success "Git pre-commit hook installed"
fi

# Create sample Python files if they don't exist
print_step "Creating sample files..."

# Create sample training script
if [ ! -f src/training/train.py ]; then
    cat > src/training/train.py << 'EOF'
"""
YOLO Training Script
"""

from ultralytics import YOLO


def train_model(
    data_config: str = "config/data.yaml",
    model: str = "yolo11n.pt",
    epochs: int = 100,
    batch: int = 16,
    imgsz: int = 640,
    device: str = "cpu",
):
    """
    Train YOLO model

    Args:
        data_config: Path to data configuration YAML
        model: Model to use (yolo11n, yolo11s, etc.)
        epochs: Number of training epochs
        batch: Batch size
        imgsz: Image size
        device: Device to use (cpu, mps, cuda, 0, etc.)
    """
    # Load model
    model = YOLO(model)

    # Train
    results = model.train(
        data=data_config,
        epochs=epochs,
        batch=batch,
        imgsz=imgsz,
        device=device,
    )

    return results


if __name__ == "__main__":
    train_model()
EOF
    print_success "Created src/training/train.py"
fi

# Create sample API file
if [ ! -f src/api/main.py ]; then
    cat > src/api/main.py << 'EOF'
"""
YOLO FastAPI Application
"""

from fastapi import FastAPI, File, UploadFile
from ultralytics import YOLO
import io
from PIL import Image

app = FastAPI(title="YOLO Object Detection API")

# Load model
model = YOLO("yolo11n.pt")


@app.get("/")
async def root():
    return {"message": "YOLO API is running"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


@app.post("/predict")
async def predict(file: UploadFile = File(...), conf_threshold: float = 0.25):
    """
    Predict objects in uploaded image
    """
    # Read image
    contents = await file.read()
    image = Image.open(io.BytesIO(contents))

    # Predict
    results = model.predict(image, conf=conf_threshold)

    # Format results
    detections = []
    for r in results:
        for box in r.boxes:
            detections.append({
                "class": int(box.cls[0]),
                "class_name": model.names[int(box.cls[0])],
                "confidence": float(box.conf[0]),
                "bbox": box.xyxy[0].tolist(),
            })

    return {
        "success": True,
        "detections": detections,
        "detection_count": len(detections),
    }
EOF
    print_success "Created src/api/main.py"
fi

# Create sample test file
if [ ! -f tests/test_model.py ]; then
    cat > tests/test_model.py << 'EOF'
"""
YOLO Model Tests
"""

import pytest
from ultralytics import YOLO


def test_model_load():
    """Test that model loads successfully"""
    model = YOLO("yolo11n.pt")
    assert model is not None


def test_model_predict():
    """Test that model can make predictions"""
    model = YOLO("yolo11n.pt")
    # Create a dummy image
    import numpy as np
    dummy_image = np.zeros((640, 640, 3), dtype=np.uint8)

    results = model.predict(dummy_image)
    assert results is not None
EOF
    print_success "Created tests/test_model.py"
fi

# Summary
echo ""
echo -e "${MAGENTA}═══════════════════════════════════${NC}"
echo -e "${GREEN}✅ Project setup complete!${NC}"
echo -e "${MAGENTA}═══════════════════════════════════${NC}"
echo ""

print_info "Next steps:"
echo "  1. Review and edit .env file with your configuration"
echo "  2. Create config/data.yaml for your dataset"
echo "  3. Add your dataset to dataset/ directory"
echo "  4. Run training: python src/training/train.py"
echo "  5. Start API: uvicorn src.api.main:app --reload"
echo ""

print_info "Useful commands:"
echo "  - Test installation: pytest tests/"
echo "  - Format code: black src/"
echo "  - Check style: flake8 src/"
echo "  - Run API: /start-services"
echo "  - Train model: /train"
echo ""

print_success "Happy coding! 🚀"
echo ""
