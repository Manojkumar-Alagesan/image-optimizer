# 🍎 Mac Silicon Standalone App

## Building the Standalone Application

To create a standalone Mac application that doesn't require Python installation:

### Prerequisites
- macOS 10.15+ (Catalina or later)
- Python 3.7+ installed
- Apple Silicon Mac (M1/M2/M3) for native performance

### Build Steps

1. **Run the build script:**
   ```bash
   ./build_mac.sh
   ```

2. **Install the app:**
   ```bash
   # Copy to Applications folder
   cp -r dist/ImageOptimizer.app /Applications/
   ```

3. **First launch:**
   - Right-click on ImageOptimizer.app → Open
   - Click "Open" when macOS asks about running an unsigned app
   - Subsequent launches can use double-click

### Manual Build (Alternative)

If you prefer manual control:

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Build the app
pyinstaller image_optimizer.spec

# Your app will be in dist/ImageOptimizer.app
```

## App Features

✅ **Native Mac Silicon performance** - Built specifically for Apple Silicon
✅ **No Python required** - Runs on any Mac without Python installation
✅ **Retina display optimized** - High DPI support enabled
✅ **macOS integrated** - Follows Mac design guidelines
✅ **Secure** - App sandbox compatible

## Distribution

The resulting `.app` file can be:
- Shared with other Mac users
- Distributed via email/cloud storage
- Uploaded to app stores (with proper signing)

## Troubleshooting

**"App can't be opened because it is from an unidentified developer"**
- Right-click → Open instead of double-clicking
- Go to System Preferences → Security & Privacy → Allow app

**App seems slow on first launch**
- First launch takes longer as macOS scans the app
- Subsequent launches will be faster

**"App is damaged" error**
- This happens if the app was downloaded and quarantined
- Run: `xattr -cr /Applications/ImageOptimizer.app`

## File Size

Expected app size: ~60-80MB (includes Python runtime and all dependencies)

## Compatibility

- **Minimum macOS:** 10.15 (Catalina)
- **Optimized for:** Apple Silicon (M1/M2/M3)
- **Also runs on:** Intel Macs (via Rosetta if needed)