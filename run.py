#!/usr/bin/env python3
"""
Quick launcher for Batch Image Rotator
This script provides a simple way to run the application with error handling.
"""

import sys
import os
import subprocess
import importlib.util

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = {
        'PIL': 'Pillow',
        'numpy': 'numpy',
        'tkinter': 'tkinter (built-in)'
    }
    
    missing_packages = []
    
    for package, display_name in required_packages.items():
        try:
            if package == 'PIL':
                import PIL
            elif package == 'numpy':
                import numpy
            elif package == 'tkinter':
                import tkinter
        except ImportError:
            missing_packages.append(display_name)
    
    # Check optional tkinterdnd2
    try:
        import tkinterdnd2
        print("✅ Drag and drop support available")
    except ImportError:
        print("⚠️  tkinterdnd2 not installed - drag and drop will not work")
        print("   Install with: pip install tkinterdnd2")
    
    if missing_packages:
        print("❌ Missing required packages:")
        for package in missing_packages:
            print(f"   - {package}")
        print("\nInstall missing packages with:")
        print("   pip install -r requirements.txt")
        return False
    
    return True

def install_dependencies():
    """Install dependencies if needed"""
    print("Installing dependencies...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install dependencies")
        return False

def main():
    """Main launcher function"""
    print("🚀 Batch Image Rotator Launcher")
    print("=" * 40)
    
    # Check if requirements file exists
    if not os.path.exists("requirements.txt"):
        print("❌ requirements.txt not found")
        print("Please ensure you're running this from the project directory")
        return
    
    # Check dependencies
    if not check_dependencies():
        response = input("\nWould you like to install missing dependencies? (y/n): ").lower()
        if response in ['y', 'yes']:
            if not install_dependencies():
                print("Please install dependencies manually and try again")
                return
        else:
            print("Please install dependencies manually and try again")
            return
    
    # Check if main application exists
    if not os.path.exists("batch_image_rotator.py"):
        print("❌ batch_image_rotator.py not found")
        print("Please ensure you're running this from the project directory")
        return
    
    print("\n🎉 Starting Batch Image Rotator...")
    print("=" * 40)
    
    # Import and run the application
    try:
        from batch_image_rotator import main as app_main
        app_main()
    except Exception as e:
        print(f"❌ Error starting application: {e}")
        print("\nTry running directly with: python batch_image_rotator.py")

if __name__ == "__main__":
    main() 