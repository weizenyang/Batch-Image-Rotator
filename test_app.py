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

from batch_image_rotator import rotate_equirectangular_worker

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
    
    # Create temporary output directory
    output_dir = tempfile.mkdtemp()
    
    try:
        # Test different rotation angles
        angles = [0, 45, 90, 180, -90]
        for angle in angles:
            args = (test_image, angle, output_dir)
            success, result = rotate_equirectangular_worker(args)
            
            if success:
                print(f"✅ Rotation {angle}° successful")
                # Check output file exists
                output_file = Path(output_dir) / Path(test_image).name
                if output_file.exists():
                    print(f"   Output file created: {output_file}")
                else:
                    print(f"   ❌ Output file not found: {output_file}")
            else:
                print(f"❌ Rotation {angle}° failed: {result}")
                return False
        
        print("✅ Rotation function test passed!")
        return True
        
    except Exception as e:
        print(f"❌ Rotation function test failed: {e}")
        return False
    finally:
        # Clean up
        if os.path.exists(test_image):
            os.unlink(test_image)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

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
    output_dir = tempfile.mkdtemp()
    
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
            
            # Test processing
            args = (filename, 90, output_dir)
            success, result = rotate_equirectangular_worker(args)
            
            if success:
                print(f"✅ {format_name} format processed successfully")
            else:
                print(f"❌ {format_name} format failed: {result}")
                
    except Exception as e:
        print(f"❌ Image format test failed: {e}")
    finally:
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        if os.path.exists(output_dir):
            shutil.rmtree(output_dir)

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

def test_multicore_info():
    """Test multicore detection"""
    print("\nTesting multicore detection...")
    
    try:
        import multiprocessing
        num_cores = multiprocessing.cpu_count()
        print(f"✅ Detected {num_cores} CPU cores")
        print(f"   Application will use {num_cores} parallel workers")
        
        # Test ProcessPoolExecutor
        from concurrent.futures import ProcessPoolExecutor
        with ProcessPoolExecutor(max_workers=num_cores) as executor:
            print(f"✅ ProcessPoolExecutor with {num_cores} workers initialized successfully")
            
    except Exception as e:
        print(f"❌ Multicore test failed: {e}")

def main():
    """Main test function"""
    print("🧪 Testing Batch Image Rotator v2.0...")
    print("=" * 50)
    
    # Test core functionality
    success = test_rotation_function()
    if not success:
        print("\n❌ Core rotation test failed!")
        return
    
    test_image_formats()
    test_multicore_info()
    create_sample_images()
    
    print("\n" + "=" * 50)
    print("🎉 All tests completed!")
    print("\nTo test the GUI:")
    print("1. Run: python3 batch_image_rotator.py")
    print("2. Drag the sample images from 'sample_images/' folder")
    print("3. Set rotation angle and click 'Process Batch'")
    print("4. Select output directory and watch multi-core processing!")
    print(f"\nYour system has {multiprocessing.cpu_count()} CPU cores for parallel processing.")

if __name__ == "__main__":
    import multiprocessing
    main() 