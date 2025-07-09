# Batch Image Rotator

A cross-platform Python application for batch rotating equirectangular images with drag-and-drop functionality.

## Features

- **Drag and Drop**: Simply drag image files into the application
- **Batch Processing**: Process multiple images at once
- **Equirectangular Rotation**: Specialized rotation for 360° panoramic images
- **Format Preservation**: Maintains original image format and quality
- **Preview Function**: Preview rotation before processing
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
   python batch_image_rotator.py
   ```

### Option 2: Build Executable

1. **Install dependencies and build**:
   ```bash
   python build_app.py
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
   - Use the slider or enter a specific angle (-180° to 180°)
   - Positive values rotate clockwise, negative values rotate counterclockwise

3. **Preview** (optional):
   - Click "Preview First Image" to see how the rotation will look

4. **Process Batch**:
   - Click "Process Batch"
   - Select an output directory
   - Wait for processing to complete

### Understanding Equirectangular Rotation

Equirectangular images (360° panoramas) are rotated horizontally by shifting pixels rather than traditional rotation. This maintains the proper projection for VR/360° viewing.

- **0°**: No rotation
- **90°**: Rotates view 90° to the right
- **-90°**: Rotates view 90° to the left
- **180°**: Rotates view 180° (flips horizontally)

### Output

- Processed images are saved with the suffix `_rotated_[angle]deg`
- Original format and quality are preserved
- Example: `panorama.jpg` → `panorama_rotated_45.0deg.jpg`

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
python build_app.py

# Clean build artifacts
python build_app.py clean
```

### Platform-Specific Notes

#### macOS
- Creates universal binary supporting both Intel and Apple Silicon
- May require code signing for distribution
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

2. **"Failed to preview image"**
   - Ensure the image file is not corrupted
   - Check if the image format is supported

3. **Build fails**
   - Ensure all dependencies are installed
   - Try cleaning build artifacts: `python build_app.py clean`

4. **Slow processing**
   - Large images take more time
   - Processing happens in background thread

### Performance Tips

- For very large images, consider resizing before rotation
- Close other applications to free up memory
- Use SSD storage for faster file I/O

## License

This project is open source. Feel free to modify and distribute.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## Support

For issues or questions, please create an issue in the project repository. 