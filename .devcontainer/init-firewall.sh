#!/bin/bash

# YOLO Project Firewall Initialization Script
# This script configures a restrictive firewall that only allows necessary connections
# for YOLO development: GitHub, PyPI, PyTorch, npm, Anthropic APIs, and VSCode services

set -e

echo "🔒 Initializing firewall for YOLO development environment..."

# Save existing Docker DNS rules
DOCKER_DNS_RULES=$(iptables-save | grep "DOCKER_OUTPUT.*dport 53" || true)

# Flush all existing rules and chains
echo "🗑️  Flushing existing firewall rules..."
iptables -F
iptables -X
iptables -t nat -F
iptables -t nat -X
iptables -t mangle -F
iptables -t mangle -X

# Restore Docker DNS rules
if [ -n "$DOCKER_DNS_RULES" ]; then
    echo "$DOCKER_DNS_RULES" | while IFS= read -r rule; do
        iptables-restore <<< "$rule" 2>/dev/null || true
    done
fi

# Destroy existing ipsets
ipset destroy allowed-ips 2>/dev/null || true
ipset destroy allowed-domains 2>/dev/null || true

# Create ipsets for allowed IPs and domains
ipset create allowed-ips hash:net
ipset create allowed-domains hash:ip

# Allow localhost
echo "✅ Allowing localhost..."
iptables -A OUTPUT -d 127.0.0.0/8 -j ACCEPT
iptables -A INPUT -s 127.0.0.0/8 -j ACCEPT

# Allow DNS
echo "✅ Allowing DNS (port 53)..."
iptables -A OUTPUT -p udp --dport 53 -j ACCEPT
iptables -A OUTPUT -p tcp --dport 53 -j ACCEPT

# Allow SSH
echo "✅ Allowing SSH (port 22)..."
iptables -A OUTPUT -p tcp --dport 22 -j ACCEPT

# Function to add CIDR to allowed list
add_cidr() {
    local cidr=$1
    # Validate CIDR format
    if [[ $cidr =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}/[0-9]{1,2}$ ]]; then
        ipset add allowed-ips "$cidr" 2>/dev/null || echo "⚠️  Failed to add $cidr"
    fi
}

# Function to resolve domain and add IPs
resolve_and_add() {
    local domain=$1
    echo "  Resolving $domain..."

    # Get all IPs for the domain
    local ips=$(dig +short "$domain" A | grep -E '^[0-9.]+$' || true)

    if [ -n "$ips" ]; then
        while IFS= read -r ip; do
            if [[ $ip =~ ^[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}$ ]]; then
                ipset add allowed-domains "$ip" 2>/dev/null || echo "⚠️  Failed to add $ip ($domain)"
            fi
        done <<< "$ips"
    else
        echo "⚠️  Failed to resolve $domain"
    fi
}

# Fetch and add GitHub IP ranges
echo "🐙 Fetching GitHub IP ranges..."
GITHUB_IPS=$(curl -s https://api.github.com/meta | grep -oP '(?<="git": \[)[^\]]+' | tr -d '",' || true)

if [ -n "$GITHUB_IPS" ]; then
    for cidr in $GITHUB_IPS; do
        add_cidr "$cidr"
    done
    echo "✅ Added GitHub IP ranges"
else
    echo "⚠️  Failed to fetch GitHub IPs"
fi

# Fetch and add GitHub Actions IP ranges
echo "⚙️  Fetching GitHub Actions IP ranges..."
ACTIONS_IPS=$(curl -s https://api.github.com/meta | grep -oP '(?<="actions": \[)[^\]]+' | tr -d '",' || true)

if [ -n "$ACTIONS_IPS" ]; then
    for cidr in $ACTIONS_IPS; do
        add_cidr "$cidr"
    done
    echo "✅ Added GitHub Actions IP ranges"
fi

# Add Python Package Index (PyPI) domains
echo "🐍 Resolving Python Package Index (PyPI) domains..."
resolve_and_add "pypi.org"
resolve_and_add "files.pythonhosted.org"
resolve_and_add "pypi.python.org"

# Add PyTorch domains
echo "🔥 Resolving PyTorch domains..."
resolve_and_add "pytorch.org"
resolve_and_add "download.pytorch.org"

# Add npm registry
echo "📦 Resolving npm registry..."
resolve_and_add "registry.npmjs.org"

# Add Anthropic API domains
echo "🤖 Resolving Anthropic API domains..."
resolve_and_add "api.anthropic.com"
resolve_and_add "claude.ai"

# Add Sentry (error tracking)
echo "📊 Resolving Sentry..."
resolve_and_add "sentry.io"

# Add VSCode services
echo "💻 Resolving VSCode services..."
resolve_and_add "vscode.dev"
resolve_and_add "marketplace.visualstudio.com"
resolve_and_add "update.code.visualstudio.com"

# Add Ultralytics domains (YOLO)
echo "🎯 Resolving Ultralytics/YOLO domains..."
resolve_and_add "ultralytics.com"
resolve_and_add "github.com"

# Add Docker Hub (for container operations)
echo "🐳 Resolving Docker Hub..."
resolve_and_add "hub.docker.com"
resolve_and_add "registry-1.docker.io"

# Add common CDN domains
echo "🌐 Resolving CDN domains..."
resolve_and_add "cdn.jsdelivr.net"
resolve_and_add "unpkg.com"

# Detect and allow host network (for Docker)
HOST_GATEWAY=$(ip route | grep default | awk '{print $3}')
if [ -n "$HOST_GATEWAY" ]; then
    echo "🏠 Allowing host network gateway: $HOST_GATEWAY"
    HOST_NETWORK=$(ip route | grep "$HOST_GATEWAY" | grep -v default | awk '{print $1}' | head -1)
    if [ -n "$HOST_NETWORK" ]; then
        ipset add allowed-ips "$HOST_NETWORK" 2>/dev/null || true
    fi
fi

# Set default policy to DROP
echo "🚫 Setting default DROP policy..."
iptables -P INPUT DROP
iptables -P OUTPUT DROP
iptables -P FORWARD DROP

# Allow established connections
echo "🔗 Allowing established connections..."
iptables -A INPUT -m state --state ESTABLISHED,RELATED -j ACCEPT
iptables -A OUTPUT -m state --state ESTABLISHED,RELATED -j ACCEPT

# Allow traffic to allowed IPs and domains
echo "✅ Allowing traffic to approved destinations..."
iptables -A OUTPUT -m set --match-set allowed-ips dst -j ACCEPT
iptables -A OUTPUT -m set --match-set allowed-domains dst -j ACCEPT
iptables -A INPUT -m set --match-set allowed-ips src -j ACCEPT
iptables -A INPUT -m set --match-set allowed-domains src -j ACCEPT

# Allow HTTPS (443) and HTTP (80) to allowed destinations
iptables -I OUTPUT 1 -p tcp --dport 443 -m set --match-set allowed-ips dst -j ACCEPT
iptables -I OUTPUT 1 -p tcp --dport 443 -m set --match-set allowed-domains dst -j ACCEPT
iptables -I OUTPUT 1 -p tcp --dport 80 -m set --match-set allowed-ips dst -j ACCEPT
iptables -I OUTPUT 1 -p tcp --dport 80 -m set --match-set allowed-domains dst -j ACCEPT

# Verify firewall is working
echo ""
echo "🧪 Testing firewall configuration..."

# Test that blocked domain is unreachable
if timeout 2 curl -s http://example.com > /dev/null 2>&1; then
    echo "❌ Warning: example.com is reachable (should be blocked)"
else
    echo "✅ Verified: example.com is blocked"
fi

# Test that allowed domain is reachable
if timeout 5 curl -s https://api.github.com > /dev/null 2>&1; then
    echo "✅ Verified: api.github.com is accessible"
else
    echo "⚠️  Warning: api.github.com is not accessible"
fi

# Test PyPI access
if timeout 5 curl -s https://pypi.org > /dev/null 2>&1; then
    echo "✅ Verified: pypi.org is accessible"
else
    echo "⚠️  Warning: pypi.org is not accessible"
fi

echo ""
echo "✅ Firewall initialization complete!"
echo ""
echo "📋 Firewall Summary:"
echo "   - Allowed: GitHub, PyPI, PyTorch, npm, Anthropic APIs"
echo "   - Allowed: Docker Hub, VSCode services, Ultralytics"
echo "   - Allowed: localhost, DNS (53), SSH (22)"
echo "   - Default: All other traffic blocked"
echo ""
