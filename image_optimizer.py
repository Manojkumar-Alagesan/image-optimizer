import os
import sys
from PIL import Image, ImageOps
import argparse
from pathlib import Path

class ImageOptimizer:
    def __init__(self):
        self.supported_formats = {
            'JPEG': ['.jpg', '.jpeg'],
            'PNG': ['.png'],
            'WEBP': ['.webp'],
            'AVIF': ['.avif']
        }
    
    def get_file_size_kb(self, filepath):
        """Get file size in KB"""
        return os.path.getsize(filepath) / 1024
    
    def optimize_image(self, input_path, output_path=None, target_size_kb=None, 
                      quality=85, max_width=None, max_height=None, 
                      output_format=None, aspect_ratio=None):
        """
        Optimize image with multiple compression techniques
        
        Args:
            input_path: Path to input image
            output_path: Path for output (optional)
            target_size_kb: Target file size in KB
            quality: JPEG/WEBP quality (1-100)
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            output_format: Output format (JPEG, PNG, WEBP, AVIF)
            aspect_ratio: Tuple (width, height) for aspect ratio
        """
        try:
            # Open and process image
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    if output_format in ['JPEG']:
                        # Create white background for JPEG
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    else:
                        img = img.convert('RGBA')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                original_size = img.size
                print(f"Original size: {original_size[0]}x{original_size[1]}")
                
                # Apply aspect ratio if specified
                if aspect_ratio:
                    img = self.change_aspect_ratio(img, aspect_ratio)
                    print(f"Aspect ratio changed to {aspect_ratio[0]}:{aspect_ratio[1]}")
                
                # Resize if max dimensions specified
                if max_width or max_height:
                    img = self.resize_image(img, max_width, max_height)
                    print(f"Resized to: {img.size[0]}x{img.size[1]}")
                
                # Determine output format and path
                if not output_format:
                    output_format = 'JPEG'  # Default to JPEG for best compression
                
                if not output_path:
                    input_stem = Path(input_path).stem
                    input_dir = Path(input_path).parent
                    ext = self.get_extension_for_format(output_format)
                    output_path = input_dir / f"{input_stem}_optimized{ext}"
                
                # Optimize based on target size
                if target_size_kb:
                    self.compress_to_target_size(img, output_path, target_size_kb, output_format)
                else:
                    self.save_with_quality(img, output_path, quality, output_format)
                
                # Report results
                final_size_kb = self.get_file_size_kb(output_path)
                compression_ratio = (1 - final_size_kb / self.get_file_size_kb(input_path)) * 100
                
                print(f"✅ Optimization complete!")
                print(f"Input: {input_path}")
                print(f"Output: {output_path}")
                print(f"Original size: {self.get_file_size_kb(input_path):.1f} KB")
                print(f"Final size: {final_size_kb:.1f} KB")
                print(f"Compression: {compression_ratio:.1f}% reduction")
                
                return str(output_path)
                
        except Exception as e:
            print(f"❌ Error processing {input_path}: {str(e)}")
            return None
    
    def change_aspect_ratio(self, img, aspect_ratio):
        """Change image aspect ratio by cropping"""
        target_width, target_height = aspect_ratio
        target_ratio = target_width / target_height
        current_ratio = img.width / img.height
        
        if current_ratio > target_ratio:
            # Image is too wide, crop width
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        elif current_ratio < target_ratio:
            # Image is too tall, crop height
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))
        
        return img
    
    def resize_image(self, img, max_width=None, max_height=None):
        """Resize image while maintaining aspect ratio"""
        width, height = img.size
        
        if max_width and width > max_width:
            ratio = max_width / width
            height = int(height * ratio)
            width = max_width
        
        if max_height and height > max_height:
            ratio = max_height / height
            width = int(width * ratio)
            height = max_height
        
        return img.resize((width, height), Image.Resampling.LANCZOS)
    
    def compress_to_target_size(self, img, output_path, target_kb, output_format):
        """Compress image to target file size"""
        quality = 95
        min_quality = 10
        
        while quality >= min_quality:
            self.save_with_quality(img, output_path, quality, output_format)
            current_size_kb = self.get_file_size_kb(output_path)
            
            if current_size_kb <= target_kb:
                print(f"Target size achieved at quality {quality}")
                return
            
            quality -= 5
        
        # If still too large, try progressive resizing
        print("Quality reduction not enough, trying size reduction...")
        scale_factor = 0.9
        temp_img = img.copy()
        
        while scale_factor >= 0.3:
            new_size = (int(temp_img.width * scale_factor), int(temp_img.height * scale_factor))
            resized_img = temp_img.resize(new_size, Image.Resampling.LANCZOS)
            
            self.save_with_quality(resized_img, output_path, max(quality, 20), output_format)
            current_size_kb = self.get_file_size_kb(output_path)
            
            if current_size_kb <= target_kb:
                print(f"Target size achieved with {scale_factor:.1%} scaling")
                return
            
            scale_factor -= 0.1
        
        print(f"⚠️  Could not reach target size. Final size: {current_size_kb:.1f} KB")
    
    def save_with_quality(self, img, output_path, quality, output_format):
        """Save image with specified quality and format"""
        save_kwargs = {}
        
        if output_format == 'JPEG':
            save_kwargs = {
                'format': 'JPEG',
                'quality': quality,
                'optimize': True,
                'progressive': True
            }
        elif output_format == 'PNG':
            save_kwargs = {
                'format': 'PNG',
                'optimize': True
            }
        elif output_format == 'WEBP':
            save_kwargs = {
                'format': 'WEBP',
                'quality': quality,
                'optimize': True,
                'method': 6  # Highest compression method
            }
        elif output_format == 'AVIF':
            save_kwargs = {
                'format': 'AVIF',
                'quality': quality,
                'optimize': True
            }
        
        img.save(output_path, **save_kwargs)
    
    def get_extension_for_format(self, format_name):
        """Get file extension for format"""
        extensions = {
            'JPEG': '.jpg',
            'PNG': '.png',
            'WEBP': '.webp',
            'AVIF': '.avif'
        }
        return extensions.get(format_name, '.jpg')
    
    def batch_optimize(self, input_folder, output_folder=None, **kwargs):
        """Optimize all images in a folder"""
        input_path = Path(input_folder)
        if not output_folder:
            output_folder = input_path / "optimized"
        
        output_path = Path(output_folder)
        output_path.mkdir(exist_ok=True)
        
        # Find all image files
        image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff']
        image_files = []
        
        for ext in image_extensions:
            image_files.extend(input_path.glob(f"*{ext}"))
            image_files.extend(input_path.glob(f"*{ext.upper()}"))
        
        if not image_files:
            print("No image files found in the specified folder.")
            return
        
        print(f"Found {len(image_files)} image(s) to optimize...")
        
        successful = 0
        for img_file in image_files:
            print(f"\n📸 Processing: {img_file.name}")
            output_file = output_path / img_file.name
            
            result = self.optimize_image(
                input_path=str(img_file),
                output_path=str(output_file),
                **kwargs
            )
            
            if result:
                successful += 1
        
        print(f"\n🎉 Batch optimization complete!")
        print(f"Successfully optimized: {successful}/{len(image_files)} images")
        print(f"Output folder: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Offline Image Optimizer")
    parser.add_argument("input", help="Input image file or folder")
    parser.add_argument("-o", "--output", help="Output path")
    parser.add_argument("-t", "--target-size", type=float, help="Target size in KB")
    parser.add_argument("-q", "--quality", type=int, default=85, help="Quality (1-100)")
    parser.add_argument("-w", "--max-width", type=int, help="Maximum width in pixels")
    parser.add_argument("-h", "--max-height", type=int, help="Maximum height in pixels")
    parser.add_argument("-f", "--format", choices=['JPEG', 'PNG', 'WEBP', 'AVIF'], 
                       default='JPEG', help="Output format")
    parser.add_argument("-ar", "--aspect-ratio", help="Aspect ratio as 'width:height' (e.g., '16:9')")
    parser.add_argument("-b", "--batch", action="store_true", help="Batch process folder")
    
    args = parser.parse_args()
    
    # Parse aspect ratio
    aspect_ratio = None
    if args.aspect_ratio:
        try:
            w, h = map(int, args.aspect_ratio.split(':'))
            aspect_ratio = (w, h)
        except:
            print("❌ Invalid aspect ratio format. Use 'width:height' (e.g., '16:9')")
            return
    
    optimizer = ImageOptimizer()
    
    if args.batch or os.path.isdir(args.input):
        optimizer.batch_optimize(
            input_folder=args.input,
            output_folder=args.output,
            target_size_kb=args.target_size,
            quality=args.quality,
            max_width=args.max_width,
            max_height=args.max_height,
            output_format=args.format,
            aspect_ratio=aspect_ratio
        )
    else:
        optimizer.optimize_image(
            input_path=args.input,
            output_path=args.output,
            target_size_kb=args.target_size,
            quality=args.quality,
            max_width=args.max_width,
            max_height=args.max_height,
            output_format=args.format,
            aspect_ratio=aspect_ratio
        )

if __name__ == "__main__":
    # Example usage if run directly
    if len(sys.argv) == 1:
        print("🖼️  Image Optimizer - Offline Compression Tool")
        print("\nExample usage:")
        print("python image_optimizer.py image.jpg -t 200 -f WEBP")
        print("python image_optimizer.py photos/ -b -t 300 -w 1920")
        print("\nFor help: python image_optimizer.py -h")
        
        # Interactive mode
        while True:
            print("\n" + "="*50)
            input_path = input("Enter image path (or 'quit' to exit): ").strip()
            
            if input_path.lower() == 'quit':
                break
                
            if not os.path.exists(input_path):
                print("❌ File not found!")
                continue
            
            print(f"Original size: {ImageOptimizer().get_file_size_kb(input_path):.1f} KB")
            
            target_kb = input("Target size in KB (press Enter to skip): ").strip()
            target_kb = float(target_kb) if target_kb else None
            
            format_choice = input("Output format (JPEG/PNG/WEBP/AVIF) [JPEG]: ").strip().upper()
            if not format_choice:
                format_choice = 'JPEG'
            
            optimizer = ImageOptimizer()
            result = optimizer.optimize_image(
                input_path=input_path,
                target_size_kb=target_kb,
                output_format=format_choice
            )
            
            if result:
                print(f"✅ Saved to: {result}")
    else:
        main()