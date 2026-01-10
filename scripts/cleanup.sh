#!/bin/bash

# YOLO Project Cleanup Script
# Cleans up temporary files, caches, and generated outputs

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
echo -e "${MAGENTA}║   YOLO Project Cleanup Script      ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════╝${NC}"
echo ""

# Parse arguments
AGGRESSIVE=false
DRY_RUN=false
KEEP_MODELS=true

while [[ $# -gt 0 ]]; do
    case $1 in
        --aggressive)
            AGGRESSIVE=true
            shift
            ;;
        --dry-run)
            DRY_RUN=true
            shift
            ;;
        --remove-models)
            KEEP_MODELS=false
            shift
            ;;
        -h|--help)
            echo "Usage: $0 [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --aggressive      Remove logs and plugin outputs"
            echo "  --dry-run        Show what would be deleted without deleting"
            echo "  --remove-models  Also remove downloaded models (dangerous!)"
            echo "  -h, --help       Show this help message"
            echo ""
            echo "Examples:"
            echo "  $0                    # Basic cleanup"
            echo "  $0 --dry-run          # Preview cleanup"
            echo "  $0 --aggressive       # Deep cleanup"
            exit 0
            ;;
        *)
            print_error "Unknown option: $1"
            exit 1
            ;;
    esac
done

if [ "$DRY_RUN" = true ]; then
    print_warning "DRY RUN MODE - No files will be deleted"
    echo ""
fi

# Function to remove files/directories
cleanup_path() {
    local path=$1
    local description=$2

    if [ -e "$path" ]; then
        if [ "$DRY_RUN" = true ]; then
            print_info "Would remove: $path ($description)"
        else
            rm -rf "$path"
            print_success "Removed: $path ($description)"
        fi
    fi
}

# Calculate sizes before cleanup
print_step "Calculating current disk usage..."

if command -v du &> /dev/null; then
    BEFORE_SIZE=0

    for dir in __pycache__ .pytest_cache .mypy_cache runs logs analysis monitoring optimization security; do
        if [ -d "$dir" ]; then
            SIZE=$(du -sh "$dir" 2>/dev/null | cut -f1 || echo "0")
            echo "  $dir: $SIZE"
            BEFORE_NUM=$(du -sk "$dir" 2>/dev/null | cut -f1 || echo "0")
            BEFORE_SIZE=$((BEFORE_SIZE + BEFORE_NUM))
        fi
    done

    echo ""
fi

# Python cache cleanup
print_step "Cleaning Python cache files..."

find . -type d -name "__pycache__" -exec bash -c "
    if [ \"$DRY_RUN\" = true ]; then
        echo \"  Would remove: {}\"
    else
        rm -rf \"{}\"
    fi
" \;

find . -type f -name "*.pyc" -o -name "*.pyo" -exec bash -c "
    if [ \"$DRY_RUN\" = true ]; then
        echo \"  Would remove: {}\"
    else
        rm -f \"{}\"
    fi
" \;

if [ "$DRY_RUN" = false ]; then
    print_success "Python cache cleaned"
fi

# Pytest cache
print_step "Cleaning pytest cache..."
cleanup_path ".pytest_cache" "pytest cache"
cleanup_path ".coverage" "coverage data"
cleanup_path "htmlcov" "coverage HTML report"

# Mypy cache
print_step "Cleaning mypy cache..."
cleanup_path ".mypy_cache" "mypy cache"

# YOLO training outputs
print_step "Cleaning training outputs..."

if [ -d "runs" ]; then
    RUN_COUNT=$(find runs -mindepth 1 -maxdepth 3 -type d | wc -l)
    print_info "Found $RUN_COUNT training run directories"

    if [ "$DRY_RUN" = true ]; then
        print_info "Would remove: runs/ directory"
    else
        read -p "Remove all training runs? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            rm -rf runs
            print_success "Removed training runs"
        else
            print_info "Kept training runs"
        fi
    fi
fi

# Plugin outputs (if aggressive)
if [ "$AGGRESSIVE" = true ]; then
    print_step "Cleaning plugin outputs (aggressive mode)..."

    cleanup_path "analysis" "dataset analysis results"
    cleanup_path "monitoring" "training monitoring data"
    cleanup_path "optimization" "optimization reports"
    cleanup_path "security" "security scan results"
fi

# Logs (if aggressive)
if [ "$AGGRESSIVE" = true ]; then
    print_step "Cleaning logs (aggressive mode)..."

    cleanup_path "logs" "application logs"

    # Clean individual log files in root
    find . -maxdepth 1 -type f -name "*.log" -exec bash -c "
        if [ \"$DRY_RUN\" = true ]; then
            echo \"  Would remove: {}\"
        else
            rm -f \"{}\"
        fi
    " \;
fi

# Temporary files
print_step "Cleaning temporary files..."

cleanup_path "tmp" "temporary directory"
cleanup_path "temp" "temp directory"

find . -type f -name "*.tmp" -o -name "*~" -exec bash -c "
    if [ \"$DRY_RUN\" = true ]; then
        echo \"  Would remove: {}\"
    else
        rm -f \"{}\"
    fi
" \;

if [ "$DRY_RUN" = false ]; then
    print_success "Temporary files cleaned"
fi

# DS_Store files (macOS)
if [[ "$OSTYPE" == "darwin"* ]]; then
    print_step "Cleaning .DS_Store files..."

    find . -type f -name ".DS_Store" -exec bash -c "
        if [ \"$DRY_RUN\" = true ]; then
            echo \"  Would remove: {}\"
        else
            rm -f \"{}\"
        fi
    " \;

    if [ "$DRY_RUN" = false ]; then
        print_success ".DS_Store files cleaned"
    fi
fi

# Models (only if explicitly requested)
if [ "$KEEP_MODELS" = false ]; then
    print_warning "Model removal requested!"

    if [ "$DRY_RUN" = true ]; then
        print_info "Would remove: *.pt files (YOLO models)"
    else
        read -p "Are you SURE you want to remove all model files? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            find . -type f -name "*.pt" -exec rm -f {} \;
            print_warning "Removed all .pt model files"
        else
            print_info "Kept model files"
        fi
    fi
fi

# Docker cleanup (optional)
if command -v docker &> /dev/null; then
    print_step "Docker cleanup available..."

    if [ "$DRY_RUN" = true ]; then
        print_info "Run 'docker system prune' to clean Docker cache"
    else
        read -p "Run Docker cleanup? [y/N]: " -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            docker system prune -f
            print_success "Docker cache cleaned"
        fi
    fi
fi

# Calculate size after cleanup
if [ "$DRY_RUN" = false ] && command -v du &> /dev/null; then
    echo ""
    print_step "Calculating disk space saved..."

    AFTER_SIZE=0
    for dir in __pycache__ .pytest_cache .mypy_cache runs logs analysis monitoring optimization security; do
        if [ -d "$dir" ]; then
            AFTER_NUM=$(du -sk "$dir" 2>/dev/null | cut -f1 || echo "0")
            AFTER_SIZE=$((AFTER_SIZE + AFTER_NUM))
        fi
    done

    SAVED=$((BEFORE_SIZE - AFTER_SIZE))
    SAVED_MB=$((SAVED / 1024))

    if [ $SAVED_MB -gt 0 ]; then
        print_success "Disk space saved: ${SAVED_MB}MB"
    fi
fi

# Summary
echo ""
echo -e "${MAGENTA}═════════════════════════════════${NC}"
if [ "$DRY_RUN" = true ]; then
    echo -e "${YELLOW}📋 Dry run complete${NC}"
else
    echo -e "${GREEN}✅ Cleanup complete!${NC}"
fi
echo -e "${MAGENTA}═════════════════════════════════${NC}"
echo ""

if [ "$DRY_RUN" = false ]; then
    print_info "Project cleaned successfully"
    echo ""
    print_info "To clean more aggressively:"
    echo "  $0 --aggressive"
    echo ""
fi
