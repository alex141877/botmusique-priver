import subprocess
import sys
import os
import platform

def install():
    """Install FFmpeg on Replit"""
    print("🔧 Installing FFmpeg...")
    
    try:
        # Check if we're on Replit (Linux environment)
        if platform.system() != 'Linux':
            print("⚠️ This installation script is designed for Linux/Replit environments")
            return False
        
        # Method 1: Try installing via package manager
        print("📦 Attempting to install FFmpeg via apt...")
        try:
            # Update package list
            subprocess.run(['apt', 'update'], check=True, capture_output=True)
            # Install FFmpeg
            subprocess.run(['apt', 'install', '-y', 'ffmpeg'], check=True, capture_output=True)
            print("✅ FFmpeg installed successfully via apt")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ apt installation failed, trying alternative method...")
        
        # Method 2: Try installing via nix (Replit's package manager)
        print("📦 Attempting to install FFmpeg via nix...")
        try:
            subprocess.run(['nix-env', '-iA', 'nixpkgs.ffmpeg'], check=True, capture_output=True)
            print("✅ FFmpeg installed successfully via nix")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ nix installation failed, trying conda...")
        
        # Method 3: Try conda if available
        print("📦 Attempting to install FFmpeg via conda...")
        try:
            subprocess.run(['conda', 'install', '-c', 'conda-forge', 'ffmpeg', '-y'], 
                          check=True, capture_output=True)
            print("✅ FFmpeg installed successfully via conda")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("❌ conda installation failed")
        
        # Method 4: Download static binary as last resort
        print("📦 Attempting to download FFmpeg static binary...")
        try:
            # Create a local bin directory
            bin_dir = os.path.expanduser("~/bin")
            os.makedirs(bin_dir, exist_ok=True)
            
            # Download FFmpeg static binary
            import urllib.request
            import tarfile
            
            # URL for static FFmpeg binary (Linux x64)
            ffmpeg_url = "https://johnvansickle.com/ffmpeg/builds/ffmpeg-git-amd64-static.tar.xz"
            ffmpeg_tar = os.path.join(bin_dir, "ffmpeg.tar.xz")
            
            print("⬇️ Downloading FFmpeg static binary...")
            urllib.request.urlretrieve(ffmpeg_url, ffmpeg_tar)
            
            print("📦 Extracting FFmpeg...")
            with tarfile.open(ffmpeg_tar, 'r:xz') as tar:
                # Extract to temporary directory
                temp_dir = os.path.join(bin_dir, "temp_ffmpeg")
                tar.extractall(temp_dir)
                
                # Find the ffmpeg binary and copy to bin
                for root, dirs, files in os.walk(temp_dir):
                    if 'ffmpeg' in files:
                        ffmpeg_src = os.path.join(root, 'ffmpeg')
                        ffmpeg_dst = os.path.join(bin_dir, 'ffmpeg')
                        
                        import shutil
                        shutil.copy2(ffmpeg_src, ffmpeg_dst)
                        os.chmod(ffmpeg_dst, 0o755)
                        break
                
                # Cleanup
                shutil.rmtree(temp_dir)
                os.remove(ffmpeg_tar)
            
            # Add bin directory to PATH
            current_path = os.environ.get('PATH', '')
            if bin_dir not in current_path:
                os.environ['PATH'] = f"{bin_dir}:{current_path}"
            
            print("✅ FFmpeg static binary installed successfully")
            return True
            
        except Exception as e:
            print(f"❌ Static binary installation failed: {e}")
        
        # Method 5: Replit-specific installation
        print("📦 Trying Replit-specific installation...")
        try:
            # Create replit.nix file for FFmpeg
            nix_config = '''{ pkgs }: {
    deps = [
        pkgs.ffmpeg
        pkgs.python3
        pkgs.python3Packages.pip
    ];
}'''
            
            with open('replit.nix', 'w') as f:
                f.write(nix_config)
            
            print("📝 Created replit.nix configuration")
            print("⚠️ Please restart your Replit to apply FFmpeg installation")
            print("   or manually run: nix-shell")
            
            return True
            
        except Exception as e:
            print(f"❌ Replit-specific installation failed: {e}")
        
        print("❌ All FFmpeg installation methods failed")
        print("📝 Manual installation required:")
        print("   1. Add 'pkgs.ffmpeg' to your replit.nix file")
        print("   2. Restart your Replit")
        print("   3. Or install manually with: apt install ffmpeg")
        
        return False
        
    except Exception as e:
        print(f"❌ FFmpeg installation error: {e}")
        return False

def verify_installation():
    """Verify that FFmpeg is properly installed"""
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True, 
                              check=True)
        
        # Extract version info
        version_line = result.stdout.split('\n')[0]
        print(f"✅ FFmpeg verification successful: {version_line}")
        return True
        
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ FFmpeg verification failed - not found or not working")
        return False

if __name__ == "__main__":
    print("🎵 FFmpeg Installation Script for Discord Music Bot")
    print("=" * 50)
    
    # Check if FFmpeg is already installed
    if verify_installation():
        print("✅ FFmpeg is already installed and working!")
        sys.exit(0)
    
    # Install FFmpeg
    if install():
        print("\n" + "=" * 50)
        print("🔄 Verifying installation...")
        
        if verify_installation():
            print("🎉 FFmpeg installation completed successfully!")
        else:
            print("⚠️ Installation may have succeeded but verification failed")
            print("   Try restarting your application or Replit environment")
    else:
        print("❌ FFmpeg installation failed!")
        sys.exit(1)
