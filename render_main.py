#!/usr/bin/env python3
"""
Main entry point for Render deployment
Automatically detects environment (Render vs Replit) and adapts accordingly
"""

import os
import sys
import threading
import time

def detect_environment():
    """Detect if running on Render or Replit"""
    if os.getenv('RENDER'):
        return 'render'
    elif os.getenv('REPLIT_DB_URL') or os.path.exists('/home/runner'):
        return 'replit'
    else:
        return 'unknown'

def install_ffmpeg_for_environment():
    """Install FFmpeg based on detected environment"""
    env = detect_environment()
    
    if env == 'render':
        print("🌍 Detected Render environment")
        from render_install import install_ffmpeg_render, check_ffmpeg
        if not check_ffmpeg():
            install_ffmpeg_render()
    elif env == 'replit':
        print("🌍 Detected Replit environment")
        try:
            from install_ffmpeg import install_ffmpeg
            install_ffmpeg()
        except ImportError:
            print("⚠️ install_ffmpeg module not found")
    else:
        print("🌍 Unknown environment, attempting basic FFmpeg check")
        import subprocess
        try:
            subprocess.run(['ffmpeg', '-version'], check=True, capture_output=True)
            print("FFmpeg already available")
        except:
            print("⚠️ FFmpeg not found - some features may not work")

def get_port():
    """Get port based on environment"""
    env = detect_environment()
    
    if env == 'render':
        # Render provides PORT environment variable
        return int(os.getenv('PORT', 5000))
    else:
        # Replit and others use 5000
        return 5000

def start_keep_alive_server():
    """Start the Flask keep-alive server"""
    from keep_alive import app
    port = get_port()
    host = '0.0.0.0'
    
    print(f"🌐 Starting keep-alive server on {host}:{port}")
    app.run(host=host, port=port, debug=False)

def start_discord_bot():
    """Start the Discord bot"""
    print("🤖 Starting Discord bot...")
    
    # Import and run the main function from main.py
    from main import main as run_bot
    run_bot()

if __name__ == "__main__":
    print("🚀 Starting Discord Music Bot...")
    
    # Install FFmpeg first
    install_ffmpeg_for_environment()
    
    # Start Flask server in background thread
    flask_thread = threading.Thread(target=start_keep_alive_server, daemon=True)
    flask_thread.start()
    
    # Give Flask a moment to start
    time.sleep(2)
    
    # Start Discord bot (this will block)
    start_discord_bot()