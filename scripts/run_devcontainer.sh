#!/bin/bash

# YOLO Project DevContainer Launcher for macOS/Linux
# This script automates the DevContainer setup and launches Claude Code

set -e

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color

# Output functions
print_success() {
    echo -e "${GREEN}✓ $1${NC}"
}

print_error() {
    echo -e "${RED}✗ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠ $1${NC}"
}

print_info() {
    echo -e "${CYAN}ℹ $1${NC}"
}

# Usage information
usage() {
    cat << EOF
YOLO Project DevContainer Launcher

Usage: $0 [OPTIONS]

Options:
    -b, --backend BACKEND   Container backend to use (docker or podman)
                            Default: docker
    -s, --skip-claude      Skip launching Claude Code after container starts
    -h, --help             Show this help message

Examples:
    $0                              # Use Docker (default)
    $0 --backend docker             # Explicitly use Docker
    $0 --backend podman             # Use Podman
    $0 --skip-claude                # Start without Claude Code

Requirements:
    - Docker Desktop or Podman
    - Dev Container CLI (npm install -g @devcontainers/cli)
    - Project must have .devcontainer configuration

EOF
    exit 0
}

# Parse arguments
BACKEND="docker"
SKIP_CLAUDE=false

while [[ $# -gt 0 ]]; do
    case $1 in
        -b|--backend)
            BACKEND="$2"
            if [[ "$BACKEND" != "docker" && "$BACKEND" != "podman" ]]; then
                print_error "Invalid backend: $BACKEND (must be 'docker' or 'podman')"
                exit 1
            fi
            shift 2
            ;;
        -s|--skip-claude)
            SKIP_CLAUDE=true
            shift
            ;;
        -h|--help)
            usage
            ;;
        *)
            print_error "Unknown option: $1"
            usage
            ;;
    esac
done

# Banner
echo ""
echo -e "${MAGENTA}╔════════════════════════════════════════╗${NC}"
echo -e "${MAGENTA}║   YOLO Project DevContainer Launcher   ║${NC}"
echo -e "${MAGENTA}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if running from project root
if [ ! -d ".devcontainer" ]; then
    print_error "Cannot find .devcontainer directory!"
    print_info "Please run this script from the project root directory."
    exit 1
fi

print_success "Found .devcontainer configuration"

# Check for devcontainer CLI
print_info "Checking prerequisites..."

if ! command -v devcontainer &> /dev/null; then
    print_error "DevContainer CLI not found!"
    print_info "Install with: npm install -g @devcontainers/cli"
    exit 1
fi

print_success "DevContainer CLI found"

# Backend-specific setup
case $BACKEND in
    docker)
        print_info "Using Docker as container backend"

        if ! command -v docker &> /dev/null; then
            print_error "Docker not found!"
            print_info "Install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
            exit 1
        fi

        print_success "Docker found"

        # Check if Docker is running
        print_info "Checking Docker status..."
        if ! docker info > /dev/null 2>&1; then
            print_error "Docker is not running!"
            print_info "Please start Docker Desktop and try again."
            exit 1
        fi

        print_success "Docker is running"
        ;;

    podman)
        print_info "Using Podman as container backend"

        if ! command -v podman &> /dev/null; then
            print_error "Podman not found!"
            print_info "Install Podman from: https://podman.io/getting-started/installation"
            exit 1
        fi

        print_success "Podman found"

        # Initialize Podman machine if needed (macOS only)
        if [[ "$OSTYPE" == "darwin"* ]]; then
            print_info "Checking Podman machine..."

            if ! podman machine list | grep -q "claudeVM"; then
                print_info "Creating Podman machine 'claudeVM'..."
                podman machine init claudeVM
                print_success "Podman machine created"
            fi

            # Start machine if not running
            if ! podman machine list | grep "claudeVM" | grep -q "running"; then
                print_info "Starting Podman machine..."
                podman machine start claudeVM
                print_success "Podman machine started"
            else
                print_success "Podman machine is running"
            fi

            # Set as default connection
            podman system connection default claudeVM
        fi
        ;;
esac

# Build and start DevContainer
echo ""
print_info "Starting DevContainer..."
print_warning "This may take 5-10 minutes on first run..."
echo ""

if ! devcontainer up --workspace-folder .; then
    print_error "Failed to start DevContainer"
    exit 1
fi

print_success "DevContainer is running"

# Get container ID
print_info "Finding container ID..."

WORKSPACE_PATH=$(pwd)
CONTAINER_ID=$(docker ps --filter "label=devcontainer.local_folder=$WORKSPACE_PATH" --format "{{.ID}}" | head -1)

if [ -z "$CONTAINER_ID" ]; then
    print_error "Failed to find container ID"
    print_info "Container may not have started correctly"
    exit 1
fi

print_success "Found container: $CONTAINER_ID"

# Launch Claude Code if not skipped
if [ "$SKIP_CLAUDE" = false ]; then
    echo ""
    print_info "Launching Claude Code..."
    echo ""

    docker exec -it "$CONTAINER_ID" claude || print_warning "Claude Code exited with error"
fi

# Launch interactive shell
echo ""
print_info "Launching interactive shell (zsh)..."
print_info "Type 'exit' to stop the container"
echo ""

docker exec -it "$CONTAINER_ID" zsh

# Cleanup message
echo ""
print_info "DevContainer session ended"
print_info "To stop the container: docker stop $CONTAINER_ID"
print_info "To remove the container: devcontainer down --workspace-folder ."
echo ""
