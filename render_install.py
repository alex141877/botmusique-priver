#!/usr/bin/env python3
"""
FFmpeg installation script for Render deployment
Optimized for Ubuntu environment on Render
"""

import subprocess
import sys
import os

def install_ffmpeg_render():
    """Install FFmpeg on Render (Ubuntu environment)"""
    print("Installing FFmpeg for Render deployment...")
    
    try:
        # Update package list first
        subprocess.run(['sudo', 'apt-get', 'update'], check=True)
        
        # Install FFmpeg via apt-get (most reliable on Ubuntu)
        result = subprocess.run(
            ['sudo', 'apt-get', 'install', '-y', 'ffmpeg'],
            capture_output=True, text=True, check=True
        )
        
        # Verify installation
        version_result = subprocess.run(['ffmpeg', '-version'], capture_output=True, text=True)
        if version_result.returncode == 0:
            print("✅ FFmpeg installed successfully on Render!")
            return True
        else:
            print("❌ FFmpeg installation verification failed")
            return False
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install FFmpeg via apt-get: {e}")
        return False
    except FileNotFoundError:
        print("❌ apt-get not found - not running on Ubuntu")
        return False

def check_ffmpeg():
    """Check if FFmpeg is already installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], capture_output=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

if __name__ == "__main__":
    if check_ffmpeg():
        print("FFmpeg is already installed")
    else:
        if not install_ffmpeg_render():
            print("Failed to install FFmpeg - some audio features may not work")
            sys.exit(1)