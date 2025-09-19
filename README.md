# 🖼️ Image Optimizer - Mac Silicon Standalone App

**Compress images without limits. No 400KB restrictions. No subscriptions. Complete offline control.**

🎯 Why This Tool?

Online image compressors limit you to 400KB and require payment for smaller sizes. This tool gives you complete control:

- ✅ **No size limits** - Compress to 50KB, 100KB, or any target size
- ✅ **No upload delays** - Process locally, instantly
- ✅ **Batch processing** - Handle hundreds of images at once
- ✅ **Privacy first** - Your images never leave your computer
- ✅ **Advanced formats** - WEBP, AVIF, and more
- ✅ **Free forever** - No subscriptions or hidden costs
- ✅ **Native Mac Silicon** - Optimized for M1/M2/M3 performance

## 🚀 Quick Start

### Option 1: Standalone Mac App (Recommended)
1. **Download** the app from the releases or build it yourself
2. **Copy** `ImageOptimizer.app` to your Applications folder
3. **Right-click** → Open (first time only to bypass Gatekeeper)
4. **Drag & drop** images or use the browse buttons

### Option 2: Python Development Version
```bash
# Install dependencies
pip install -r requirements.txt

# Run GUI
python image_optimizer_gui.py

# Command line usage
python image_optimizer.py photo.jpg -t 200 -f WEBP
```

## 📦 Installation

### For Regular Users - ZERO Setup Required! 🎉

**The standalone app includes everything - no downloads, no Python, no technical setup!**

1. Get `ImageOptimizer.app` (self-contained, ~38MB)
2. Copy to your Applications folder:
   ```bash
   cp -r ImageOptimizer.app /Applications/
   ```
3. **First launch:** Right-click → Open (bypasses security)
4. **Done!** The app works immediately

**✅ What's Included in the App:**
- Complete Python runtime
- Image processing libraries
- GUI framework (tkinter)
- All dependencies
- **Nothing else to install!**

**System Requirements:**
- macOS 10.15+ (Catalina or later)
- Any Mac (optimized for Apple Silicon M1/M2/M3)
- ~40MB free disk space
- **No Python installation needed**
- **No technical knowledge required**

### For Developers Only

**⚠️ Only needed if you want to modify the code or build from source**

**Build from source:**
```bash
# First install Python + tkinter
brew install python-tk

# Clone the repository
git clone https://github.com/yourusername/image-optimizer.git
cd image-optimizer

# Build standalone app
./build_mac.sh

# Your app will be in dist/ImageOptimizer.app
```

**Development setup:**
```bash
# Install Python dependencies
pip install -r requirements.txt

# Run development GUI (requires Python)
python image_optimizer_gui.py
```

**Developer Requirements:**
- Python 3.7+ with tkinter support
- Homebrew (for easy Python-tk installation)
- PyInstaller (included in requirements.txt)

## 🎯 Features

### Compression Options
- **Target file size** - Specify exact KB size
- **Quality control** - Fine-tune compression level (1-100)
- **Smart scaling** - Automatic size reduction when needed
- **Format conversion** - JPEG, PNG, WEBP, AVIF

### Image Processing
- **Batch processing** - Process entire folders at once
- **Aspect ratio changes** - 16:9, 4:3, 1:1, custom ratios
- **Smart resizing** - Maintain quality while reducing size
- **Progressive JPEG** - Better web loading

### Formats Supported
- **Input**: JPG, PNG, WEBP, BMP, TIFF
- **Output**: JPEG, PNG, WEBP, AVIF

### Error Handling
- **Smart validation** - Catches invalid inputs before processing
- **Detailed error messages** - Know exactly what went wrong
- **File-by-file results** - See which images succeeded/failed
- **Recovery suggestions** - Get actionable advice for fixing issues

## 💡 Use Cases

### For Websites
- **Hero images**: Target 150-200KB
- **Thumbnails**: Target 50-100KB
- **WEBP format**: 25-35% smaller than JPEG
- **Batch optimize**: Process entire image folders

### For Social Media
- **Instagram**: 1080x1080 (1:1 ratio)
- **Facebook**: 1200x630 (1.91:1 ratio)
- **Twitter**: 1200x675 (16:9 ratio)

### For Email/Sharing
- **Target**: 200-500KB max
- **Format**: JPEG for photos
- **Max width**: 1200px

## 🔧 Advanced Usage

### GUI Interface
1. **Select images** - Browse files or entire folders
2. **Set parameters** - Target size, quality, dimensions
3. **Choose format** - JPEG, PNG, WEBP, or AVIF
4. **Process** - Click "Optimize Images" and watch progress
5. **Review results** - See detailed compression stats

### Command Line Options (Development)
```bash
-t, --target-size    Target size in KB (e.g., -t 200)
-q, --quality        Quality 1-100 (e.g., -q 85)
-w, --max-width      Maximum width in pixels
-h, --max-height     Maximum height in pixels
-f, --format         Output format (JPEG, PNG, WEBP, AVIF)
-ar, --aspect-ratio  Aspect ratio (e.g., -ar 16:9)
-b, --batch          Batch process folder
```

### Examples
```bash
# Web optimization
python image_optimizer.py photos/ -b -t 150 -f WEBP -w 1920

# Social media (Instagram)
python image_optimizer.py photo.jpg -ar 1:1 -t 200 -f JPEG

# Extreme compression
python image_optimizer.py image.jpg -t 50 -f WEBP
```

## 🏗️ Technical Details

### Architecture
- **Native Mac app** - Built with PyInstaller for macOS
- **Apple Silicon optimized** - Native ARM64 performance
- **Modular design** - Easy to extend and modify
- **Error handling** - Robust processing with detailed feedback
- **Memory efficient** - Processes large batches without issues

### Dependencies
- **Core**: Pillow (PIL) for image processing
- **GUI**: tkinter (native macOS support)
- **Packaging**: PyInstaller for standalone app creation
- **Format support**: pillow-avif-plugin for AVIF format

### Performance
- **Speed**: ~1-3 seconds per image (depends on size/quality)
- **Memory**: Efficient processing of large image batches
- **Quality**: Advanced compression algorithms maintain visual quality

## 🆘 Troubleshooting

### App Won't Open
**"App can't be opened because it is from an unidentified developer"**
```bash
# Remove quarantine flag
xattr -cr /Applications/ImageOptimizer.app

# Then right-click → Open
```

### Performance Issues
**App seems slow on first launch**
- First launch takes longer as macOS scans the app
- Subsequent launches will be much faster

**Large images taking too long**
- Reduce target quality (try 60-80)
- Use WEBP format for better compression
- Reduce image dimensions first

### Common Error Messages
**"Target size too small"**
- Increase target KB size
- Try WEBP format for better compression
- Reduce image dimensions

**"Invalid image format"**
- File may be corrupted
- Ensure it's a supported format (JPG, PNG, WEBP, BMP, TIFF)

**"Permission denied"**
- Check file permissions
- Try copying images to Desktop first

## 📊 Performance Comparison

### Standalone App vs. Online Tools
| Feature | This App | Online Tools |
|---------|----------|--------------|
| Size Limit | None | 400KB+ (paid) |
| Batch Processing | ✅ Unlimited | ❌ Limited |
| Privacy | ✅ Local only | ❌ Upload required |
| Speed | ✅ Instant | ❌ Upload/download |
| Cost | ✅ Free forever | ❌ Subscription |
| Formats | ✅ 4+ formats | ❌ Limited |
| Mac Native | ✅ Apple Silicon | ❌ Web-based |

### Benchmark Results
- **Compression**: Typically 60-80% size reduction
- **Quality**: Maintains visual quality at target sizes
- **Batch**: Can process 100+ images efficiently
- **Memory**: ~50-100MB RAM usage for typical batches

## 🔮 Future Roadmap

### Planned Features
- [ ] **AI-powered optimization** - Smart compression based on image content
- [ ] **Background removal** - Automatic subject isolation
- [ ] **Watermark addition** - Batch watermarking
- [ ] **HEIC support** - Apple's modern format
- [ ] **Video compression** - Extend to video files
- [ ] **Shortcuts integration** - macOS Shortcuts support

## 📄 License

MIT License - Free to use, modify, and distribute.

## 🙏 Acknowledgments

- Built with Python and Pillow
- Native macOS integration with tkinter
- Optimized for Apple Silicon performance
- Created for photographers, designers, and content creators

## 📞 Support

- **Issues**: Report bugs via GitHub Issues
- **Mac-specific help**: Check README_MAC.md
- **Questions**: Check the documentation first
- **Feature requests**: Open a GitHub Issue with enhancement label

---

**⭐ Star this repository if it helped you optimize images on your Mac!**

## 🛠️ Building the App

For developers who want to build the standalone app:

```bash
# Prerequisites
# - macOS 10.15+
# - Python 3.7+ with tkinter support
# - Homebrew (recommended)

# Install Python with tkinter
brew install python-tk

# Clone and build
git clone https://github.com/yourusername/image-optimizer.git
cd image-optimizer
./build_mac.sh

# Your standalone app will be in dist/ImageOptimizer.app
```

The build process creates a fully self-contained macOS application that doesn't require Python to be installed on the target machine.