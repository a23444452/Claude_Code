# YOLO Project DevContainer Launcher for Windows
# This script automates the DevContainer setup and launches Claude Code

<#
.SYNOPSIS
    Launches the YOLO Project development container with Claude Code

.DESCRIPTION
    This script checks prerequisites, starts the DevContainer, and launches
    Claude Code CLI with an interactive shell for YOLO development.

.PARAMETER Backend
    Container backend to use: 'docker' (default) or 'podman'

.PARAMETER SkipClaude
    Skip launching Claude Code after container starts

.EXAMPLE
    .\run_devcontainer.ps1 -Backend docker
    .\run_devcontainer.ps1 -Backend podman
    .\run_devcontainer.ps1 -SkipClaude

.NOTES
    Requires:
    - Docker Desktop or Podman
    - Dev Container CLI (npm install -g @devcontainers/cli)
    - Project must have .devcontainer configuration

    Author: YOLO Project Team
#>

[CmdletBinding()]
param(
    [Parameter()]
    [ValidateSet('docker', 'podman')]
    [string]$Backend = 'docker',

    [Parameter()]
    [switch]$SkipClaude
)

# Color output functions
function Write-ColorOutput {
    param(
        [string]$Message,
        [string]$Color = 'White'
    )
    Write-Host $Message -ForegroundColor $Color
}

function Write-Success {
    param([string]$Message)
    Write-ColorOutput "✓ $Message" -Color Green
}

function Write-Error {
    param([string]$Message)
    Write-ColorOutput "✗ $Message" -Color Red
}

function Write-Warning {
    param([string]$Message)
    Write-ColorOutput "⚠ $Message" -Color Yellow
}

function Write-Info {
    param([string]$Message)
    Write-ColorOutput "ℹ $Message" -Color Cyan
}

# Banner
Write-Host ""
Write-ColorOutput "╔════════════════════════════════════════╗" -Color Magenta
Write-ColorOutput "║   YOLO Project DevContainer Launcher   ║" -Color Magenta
Write-ColorOutput "╚════════════════════════════════════════╝" -Color Magenta
Write-Host ""

# Check if running from project root
if (-not (Test-Path ".devcontainer")) {
    Write-Error "Cannot find .devcontainer directory!"
    Write-Info "Please run this script from the project root directory."
    exit 1
}

Write-Success "Found .devcontainer configuration"

# Check for devcontainer CLI
Write-Info "Checking prerequisites..."

if (-not (Get-Command devcontainer -ErrorAction SilentlyContinue)) {
    Write-Error "DevContainer CLI not found!"
    Write-Info "Install with: npm install -g @devcontainers/cli"
    exit 1
}

Write-Success "DevContainer CLI found"

# Backend-specific setup
switch ($Backend) {
    'docker' {
        Write-Info "Using Docker as container backend"

        if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
            Write-Error "Docker not found!"
            Write-Info "Install Docker Desktop from: https://www.docker.com/products/docker-desktop/"
            exit 1
        }

        Write-Success "Docker found"

        # Check if Docker is running
        Write-Info "Checking Docker status..."
        try {
            $dockerInfo = docker info 2>&1
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Docker is not running!"
                Write-Info "Please start Docker Desktop and try again."
                exit 1
            }
            Write-Success "Docker is running"
        }
        catch {
            Write-Error "Failed to connect to Docker"
            exit 1
        }
    }
    'podman' {
        Write-Info "Using Podman as container backend"

        if (-not (Get-Command podman -ErrorAction SilentlyContinue)) {
            Write-Error "Podman not found!"
            Write-Info "Install Podman from: https://podman.io/getting-started/installation"
            exit 1
        }

        Write-Success "Podman found"

        # Initialize Podman machine if needed
        Write-Info "Checking Podman machine..."
        $machines = podman machine list --format json | ConvertFrom-Json

        $claudeVM = $machines | Where-Object { $_.Name -eq "claudeVM" }

        if (-not $claudeVM) {
            Write-Info "Creating Podman machine 'claudeVM'..."
            podman machine init claudeVM
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Failed to create Podman machine"
                exit 1
            }
            Write-Success "Podman machine created"
        }

        # Start machine if not running
        if ($claudeVM.Running -ne $true) {
            Write-Info "Starting Podman machine..."
            podman machine start claudeVM
            if ($LASTEXITCODE -ne 0) {
                Write-Error "Failed to start Podman machine"
                exit 1
            }
            Write-Success "Podman machine started"
        }
        else {
            Write-Success "Podman machine is running"
        }

        # Set as default connection
        podman system connection default claudeVM
    }
}

# Build and start DevContainer
Write-Host ""
Write-Info "Starting DevContainer..."
Write-Warning "This may take 5-10 minutes on first run..."
Write-Host ""

devcontainer up --workspace-folder .

if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to start DevContainer"
    exit 1
}

Write-Success "DevContainer is running"

# Get container ID
Write-Info "Finding container ID..."

$containerId = docker ps --filter "label=devcontainer.local_folder=$((Get-Location).Path.Replace('\', '/'))" --format "{{.ID}}" | Select-Object -First 1

if (-not $containerId) {
    Write-Error "Failed to find container ID"
    Write-Info "Container may not have started correctly"
    exit 1
}

Write-Success "Found container: $containerId"

# Launch Claude Code if not skipped
if (-not $SkipClaude) {
    Write-Host ""
    Write-Info "Launching Claude Code..."
    Write-Host ""

    docker exec -it $containerId claude

    if ($LASTEXITCODE -ne 0) {
        Write-Warning "Claude Code exited with error"
    }
}

# Launch interactive shell
Write-Host ""
Write-Info "Launching interactive shell (zsh)..."
Write-Info "Type 'exit' to stop the container"
Write-Host ""

docker exec -it $containerId zsh

# Cleanup message
Write-Host ""
Write-Info "DevContainer session ended"
Write-Info "To stop the container: docker stop $containerId"
Write-Info "To remove the container: devcontainer down --workspace-folder ."
Write-Host ""
