# Batch Image Rotator

A streamlined, high-performance Python application for batch rotating equirectangular images with multi-core processing and drag-and-drop functionality.

## Features

- **Multi-Core Processing**: Automatically scales to use all CPU cores for maximum speed
- **Drag and Drop**: Simply drag image files into the application
- **Batch Processing**: Process multiple images simultaneously
- **Equirectangular Rotation**: Specialized rotation for 360° panoramic images
- **Format Preservation**: Maintains original image format and quality
- **Original Naming**: Keeps original filenames (no prefixes/suffixes)
- **Streamlined UI**: Clean, minimal interface focused on essential operations
- **Cross-Platform**: Works on Mac and Windows
- **Fast Startup**: Built with tkinter for quick launching

## Supported Image Formats

- JPEG (.jpg, .jpeg)
- PNG (.png)
- BMP (.bmp)
- TIFF (.tiff, .tif)
- WebP (.webp)

## Installation

### Option 1: Run from Source

1. **Clone or download this repository**

2. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   python3 batch_image_rotator.py
   ```

### Option 2: Build Executable

1. **Install dependencies and build**:
   ```bash
   python3 build_app.py
   ```

2. **Run the executable**:
   - **Windows**: `./dist/BatchImageRotator.exe`
   - **Mac**: `./dist/BatchImageRotator`

## Usage

### Basic Workflow

1. **Add Images**: 
   - Drag and drop image files into the drop zone, or
   - Click the drop zone to browse and select files

2. **Set Rotation**:
   - Enter rotation angle in degrees (-180° to 180°)
   - Positive values rotate clockwise, negative values rotate counterclockwise

3. **Process Batch**:
   - Click "Process Batch"
   - Select an output directory
   - Processing will use all available CPU cores for maximum speed

### Understanding Equirectangular Rotation

Equirectangular images (360° panoramas) are rotated horizontally by shifting pixels rather than traditional rotation. This maintains the proper projection for VR/360° viewing.

- **0°**: No rotation
- **90°**: Rotates view 90° to the right
- **-90°**: Rotates view 90° to the left
- **180°**: Rotates view 180° (flips horizontally)

### Output

- Processed images are saved with their **original filenames**
- Original format and quality are preserved
- Example: `panorama.jpg` → `panorama.jpg` (in output directory)

## Performance

- **Multi-Core Processing**: Automatically uses all CPU cores
- **Parallel Processing**: Multiple images processed simultaneously
- **Memory Efficient**: Each worker processes images independently
- **Progress Tracking**: Real-time progress updates during processing

## System Requirements

- **Python**: 3.7 or higher
- **Operating System**: macOS 10.14+ or Windows 10+
- **Memory**: 512MB RAM (more for large images)
- **Storage**: Sufficient space for input and output images

## Dependencies

- **Pillow**: Image processing
- **NumPy**: Array operations for rotation
- **tkinterdnd2**: Drag and drop functionality (optional)

## Building for Distribution

### Prerequisites

```bash
pip install pyinstaller
```

### Build Commands

```bash
# Build executable
python3 build_app.py

# Clean build artifacts
python3 build_app.py clean
```

### Platform-Specific Notes

#### macOS
- Creates ARM64 native binary for Apple Silicon
- Falls back gracefully from universal build if needed
- App bundle created in `dist/` folder

#### Windows
- Creates single .exe file
- No additional runtime required
- Executable created in `dist/` folder

## Troubleshooting

### Common Issues

1. **"Drag and drop not available"**
   - Install tkinterdnd2: `pip install tkinterdnd2`
   - You can still use the browse button

2. **Processing seems slow**
   - Application automatically uses all CPU cores
   - Large images take more time
   - Check available RAM and close other applications

3. **Build fails**
   - Ensure all dependencies are installed
   - Try cleaning build artifacts: `python3 build_app.py clean`

### Performance Tips

- **More CPU cores = faster processing**
- **Use SSD storage** for faster file I/O
- **Close other applications** to free up CPU and memory
- **Process images in smaller batches** if running out of memory

## What's New

### v2.0 Optimizations

- ✅ **Multi-core processing** with automatic CPU detection
- ✅ **Streamlined UI** with essential controls only
- ✅ **Original filenames** preserved (no prefixes/suffixes)
- ✅ **Faster processing** with parallel workers
- ✅ **Real-time progress** tracking
- ✅ **Smaller window size** for better screen utilization

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions, please create an issue in the project repository. 