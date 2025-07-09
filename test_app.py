#!/usr/bin/env python3
"""
Test script for the Batch Image Rotator application.
This script creates sample images and tests the core functionality.
"""

import os
import sys
import tempfile
import shutil
from pathlib import Path
from PIL import Image
import numpy as np

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from batch_image_rotator import BatchImageRotator

def create_test_image(width=1024, height=512, filename="test_equirectangular.jpg"):
    """Create a test equirectangular image"""
    # Create a gradient pattern that's easy to see when rotated
    img_array = np.zeros((height, width, 3), dtype=np.uint8)
    
    # Create horizontal gradient
    for x in range(width):
        color_val = int((x / width) * 255)
        img_array[:, x] = [color_val, 128, 255 - color_val]
    
    # Add vertical stripes for rotation visibility
    for x in range(0, width, width // 8):
        img_array[:, x:x+20] = [255, 255, 255]
    
    # Create PIL image and save
    img = Image.fromarray(img_array)
    img.save(filename, quality=90)
    return filename

def test_rotation_function():
    """Test the rotation function directly"""
    print("Testing rotation function...")
    
    # Create temporary test image
    with tempfile.NamedTemporaryFile(suffix='.jpg', delete=False) as tmp:
        test_image = create_test_image(filename=tmp.name)
    
    try:
        # Create a mock app instance to test rotation
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        app = BatchImageRotator(root)
        
        # Test rotation
        with Image.open(test_image) as img:
            print(f"Original image size: {img.size}")
            
            # Test different rotation angles
            angles = [0, 45, 90, 180, -90]
            for angle in angles:
                rotated = app.rotate_equirectangular(img, angle)
                print(f"Rotation {angle}°: {rotated.size} (should be same as original)")
                
                # Save test result
                output_file = f"test_output_{angle}deg.jpg"
                rotated.save(output_file)
                print(f"Saved: {output_file}")
        
        root.destroy()
        print("✅ Rotation function test passed!")
        
    except Exception as e:
        print(f"❌ Rotation function test failed: {e}")
    finally:
        # Clean up
        if os.path.exists(test_image):
            os.unlink(test_image)

def test_image_formats():
    """Test different image formats"""
    print("\nTesting image formats...")
    
    formats = [
        ("JPEG", ".jpg"),
        ("PNG", ".png"),
        ("BMP", ".bmp"),
        ("TIFF", ".tiff")
    ]
    
    temp_dir = tempfile.mkdtemp()
    
    try:
        for format_name, ext in formats:
            filename = os.path.join(temp_dir, f"test{ext}")
            
            # Create test image
            img_array = np.random.randint(0, 255, (256, 512, 3), dtype=np.uint8)
            img = Image.fromarray(img_array)
            
            # Save in format
            if format_name == "JPEG":
                img.save(filename, format_name, quality=90)
            else:
                img.save(filename, format_name)
            
            # Test loading
            with Image.open(filename) as loaded_img:
                print(f"✅ {format_name} format: {loaded_img.size}, {loaded_img.mode}")
                
    except Exception as e:
        print(f"❌ Image format test failed: {e}")
    finally:
        shutil.rmtree(temp_dir)

def create_sample_images():
    """Create sample images for testing"""
    print("\nCreating sample images...")
    
    # Create sample directory
    sample_dir = Path("sample_images")
    sample_dir.mkdir(exist_ok=True)
    
    # Create different sized test images
    sizes = [
        (1024, 512, "small_panorama.jpg"),
        (2048, 1024, "medium_panorama.jpg"),
        (4096, 2048, "large_panorama.jpg")
    ]
    
    for width, height, filename in sizes:
        filepath = sample_dir / filename
        if not filepath.exists():
            create_test_image(width, height, str(filepath))
            print(f"Created: {filepath}")
    
    print(f"✅ Sample images created in {sample_dir}")

def main():
    """Main test function"""
    print("🧪 Testing Batch Image Rotator...")
    
    # Test core functionality
    test_rotation_function()
    test_image_formats()
    create_sample_images()
    
    print("\n🎉 All tests completed!")
    print("\nTo test the GUI:")
    print("1. Run: python batch_image_rotator.py")
    print("2. Drag the sample images from 'sample_images/' folder")
    print("3. Set rotation angle and click 'Preview First Image'")
    print("4. Process the batch to test full functionality")

if __name__ == "__main__":
    main() 