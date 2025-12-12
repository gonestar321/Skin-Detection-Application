#!/bin/bash
# Build script for Render deployment
# This script ensures Git LFS files are properly downloaded

echo "=== Starting Build ==="

# Install Git LFS
echo "Installing Git LFS..."
curl -s https://packagecloud.io/install/repositories/github/git-lfs/script.deb.sh | bash
apt-get install -y git-lfs
git lfs install

# Pull LFS files
echo "Pulling LFS files..."
git lfs pull

# Verify model files
echo "Verifying model files..."
ls -lh models/

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

echo "=== Build Complete ==="
