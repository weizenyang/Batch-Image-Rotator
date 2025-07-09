#!/usr/bin/env python3
"""
Build script for creating executables from the Batch Image Rotator application.
This script uses PyInstaller to create standalone executables for Mac and Windows.
"""

import os
import sys
import subprocess
import platform
from pathlib import Path

def install_requirements():
    """Install required packages"""
    print("Installing requirements...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
    subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])

def build_executable(use_universal2=False):
    """Build executable using PyInstaller"""
    print("Building executable...")
    
    # Get the current platform
    system = platform.system()
    
    # Common PyInstaller options
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",  # Create a single executable file
        "--windowed",  # Don't show console window
        "--name", "BatchImageRotator",
        "--add-data", "requirements.txt:.",
        "batch_image_rotator.py"
    ]
    
    # Add icon if available
    if system == "Windows" and os.path.exists("icon.ico"):
        cmd.extend(["--icon", "icon.ico"])
    elif system == "Darwin" and os.path.exists("icon.icns"):
        cmd.extend(["--icon", "icon.icns"])
    
    # Platform-specific options
    if system == "Darwin":  # macOS
        cmd.extend(["--osx-bundle-identifier", "com.example.batchimagerotator"])
        
        # Only add universal2 if requested and supported
        if use_universal2:
            cmd.extend(["--target-arch", "universal2"])
    
    # Add hidden imports for better compatibility
    cmd.extend([
        "--hidden-import", "PIL._tkinter_finder",
        "--hidden-import", "tkinter",
        "--hidden-import", "tkinter.ttk",
        "--hidden-import", "tkinter.filedialog",
        "--hidden-import", "tkinter.messagebox",
        "--hidden-import", "numpy",
        "--hidden-import", "PIL",
        "--hidden-import", "PIL.Image",
        "--hidden-import", "PIL.ImageTk"
    ])
    
    # Try to include tkinterdnd2 if available
    try:
        import tkinterdnd2
        cmd.extend(["--hidden-import", "tkinterdnd2"])
    except ImportError:
        pass
    
    try:
        print(f"Running PyInstaller with command: {' '.join(cmd)}")
        subprocess.check_call(cmd)
        print(f"✅ Build successful! Executable created in the 'dist' folder.")
        
        # Show output location
        if system == "Windows":
            print("📁 Executable: dist/BatchImageRotator.exe")
        elif system == "Darwin":
            print("📁 Executable: dist/BatchImageRotator")
        else:
            print("📁 Executable: dist/BatchImageRotator")
            
    except subprocess.CalledProcessError as e:
        print(f"❌ Build failed: {e}")
        return False
    
    return True

def clean_build():
    """Clean build artifacts"""
    print("Cleaning build artifacts...")
    
    import shutil
    
    # Remove build directories
    for dir_name in ["build", "dist", "__pycache__"]:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"Removed {dir_name}")
    
    # Remove .spec file
    spec_file = "BatchImageRotator.spec"
    if os.path.exists(spec_file):
        os.remove(spec_file)
        print(f"Removed {spec_file}")

def main():
    """Main build function"""
    print("🚀 Building Batch Image Rotator...")
    print(f"Platform: {platform.system()} {platform.machine()}")
    
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
        return
    
    try:
        # Install requirements
        install_requirements()
        
        # Try building executable
        success = False
        
        # On macOS, first try with universal2, then fallback to regular build
        if platform.system() == "Darwin":
            print("\n🎯 Attempting universal2 build for macOS...")
            success = build_executable(use_universal2=True)
            
            if not success:
                print("\n⚠️  Universal2 build failed, falling back to regular build...")
                clean_build()  # Clean failed build
                success = build_executable(use_universal2=False)
        else:
            # For other platforms, just do regular build
            success = build_executable(use_universal2=False)
        
        if success:
            print("\n🎉 Build completed successfully!")
            print("\nTo run the application:")
            if platform.system() == "Windows":
                print("  ./dist/BatchImageRotator.exe")
            else:
                print("  ./dist/BatchImageRotator")
        else:
            print("\n❌ Build failed!")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Build failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 