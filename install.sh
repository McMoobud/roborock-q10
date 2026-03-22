#!/bin/bash
# Roborock Q10 S5+ Custom Component Installer
#
# This script copies the unmodified core Roborock integration files
# into the custom component directory alongside the Q10-patched files.
#
# Usage: Run from the root of this repo
#   ./install.sh /path/to/ha/config
#
# Example:
#   ./install.sh /config

set -e

HA_CONFIG="${1:-/config}"
CORE_DIR="$HA_CONFIG/homeassistant/components/roborock"
CUSTOM_DIR="$HA_CONFIG/custom_components/roborock"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

if [ ! -d "$CORE_DIR" ]; then
    echo "Error: Core Roborock integration not found at $CORE_DIR"
    echo "Make sure Home Assistant is installed and the Roborock integration exists."
    exit 1
fi

echo "Installing Roborock Q10 custom component..."

# Create custom component directory
mkdir -p "$CUSTOM_DIR"

# Copy ALL files from core integration first
echo "Copying core integration files from $CORE_DIR..."
cp -r "$CORE_DIR/"* "$CUSTOM_DIR/"

# Overlay Q10-patched files from this repo
echo "Applying Q10 patches..."
cp -r "$REPO_DIR/custom_components/roborock/"* "$CUSTOM_DIR/"

echo ""
echo "Done! Restart Home Assistant to activate."
echo "Custom component installed at: $CUSTOM_DIR"
