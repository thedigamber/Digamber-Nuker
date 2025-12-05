#!/usr/bin/env bash
# build.sh - FFMPEG install for Render

echo "🔧 Installing FFMPEG for Discord voice..."

# Update package list
apt-get update

# Install FFMPEG
apt-get install -y ffmpeg

# Verify installation
ffmpeg -version

echo "<a:emoji_1:1430081383757512785> FFMPEG installed successfully!"
