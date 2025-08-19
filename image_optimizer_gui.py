import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from PIL import Image, ImageTk
import threading
from pathlib import Path

class ImageOptimizerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Optimizer - Offline Compression Tool")
        self.root.geometry("800x600")
        
        # Variables
        self.input_files = []
        self.output_folder = tk.StringVar()
        self.target_size = tk.StringVar(value="200")
        self.quality = tk.StringVar(value="85")
        self.max_width = tk.StringVar()
        self.max_height = tk.StringVar()
        self.output_format = tk.StringVar(value="JPEG")
        self.aspect_ratio = tk.StringVar()
        
        self.setup_gui()
    
    def setup_gui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Title
        title_label = ttk.Label(main_frame, text="🖼️ Image Optimizer", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # File selection
        ttk.Label(main_frame, text="Select Images:").grid(row=1, column=0, sticky=tk.W, pady=5)
        
        file_frame = ttk.Frame(main_frame)
        file_frame.grid(row=1, column=1, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        ttk.Button(file_frame, text="Browse Files", 
                  command=self.select_files).pack(side=tk.LEFT, padx=(0, 10))
        ttk.Button(file_frame, text="Browse Folder", 
                  command=self.select_folder).pack(side=tk.LEFT)
        
        # Selected files display
        self.files_listbox = tk.Listbox(main_frame, height=6)
        self.files_listbox.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), 
                               pady=(5, 15))
        
        # Output folder
        ttk.Label(main_frame, text="Output Folder:").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_folder, width=40).grid(
            row=3, column=1, sticky=(tk.W, tk.E), pady=5)
        ttk.Button(main_frame, text="Browse", 
                  command=self.select_output_folder).grid(row=3, column=2, padx=(5, 0), pady=5)
        
        # Compression settings
        settings_frame = ttk.LabelFrame(main_frame, text="Compression Settings", padding="10")
        settings_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        
        # Target size
        ttk.Label(settings_frame, text="Target Size (KB):").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(settings_frame, textvariable=self.target_size, width=15).grid(
            row=0, column=1, sticky=tk.W, pady=2, padx=(5, 20))
        
        # Quality
        ttk.Label(settings_frame, text="Quality (1-100):").grid(row=0, column=2, sticky=tk.W, pady=2)
        ttk.Entry(settings_frame, textvariable=self.quality, width=15).grid(
            row=0, column=3, sticky=tk.W, pady=2, padx=(5, 0))
        
        # Format
        ttk.Label(settings_frame, text="Output Format:").grid(row=1, column=0, sticky=tk.W, pady=2)
        format_combo = ttk.Combobox(settings_frame, textvariable=self.output_format, 
                                   values=["JPEG", "PNG", "WEBP", "AVIF"], width=12)
        format_combo.grid(row=1, column=1, sticky=tk.W, pady=2, padx=(5, 20))
        format_combo.state(['readonly'])
        
        # Resize settings
        resize_frame = ttk.LabelFrame(main_frame, text="Resize Settings (Optional)", padding="10")
        resize_frame.grid(row=5, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        
        # Max dimensions
        ttk.Label(resize_frame, text="Max Width:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Entry(resize_frame, textvariable=self.max_width, width=15).grid(
            row=0, column=1, sticky=tk.W, pady=2, padx=(5, 20))
        
        ttk.Label(resize_frame, text="Max Height:").grid(row=0, column=2, sticky=tk.W, pady=2)
        ttk.Entry(resize_frame, textvariable=self.max_height, width=15).grid(
            row=0, column=3, sticky=tk.W, pady=2, padx=(5, 0))
        
        # Aspect ratio
        ttk.Label(resize_frame, text="Aspect Ratio:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Entry(resize_frame, textvariable=self.aspect_ratio, width=15).grid(
            row=1, column=1, sticky=tk.W, pady=2, padx=(5, 5))
        ttk.Label(resize_frame, text="(e.g., 16:9, 4:3, 1:1)").grid(
            row=1, column=2, columnspan=2, sticky=tk.W, pady=2)
        
        # Progress and buttons
        self.progress = ttk.Progressbar(main_frame, mode='indeterminate')
        self.progress.grid(row=6, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=15)
        
        button_frame = ttk.Frame(main_frame)
        button_frame.grid(row=7, column=0, columnspan=3, pady=10)
        
        self.optimize_button = ttk.Button(button_frame, text="🚀 Optimize Images", 
                                         command=self.start_optimization)
        self.optimize_button.pack(side=tk.LEFT, padx=(0, 10))
        
        ttk.Button(button_frame, text="Clear All", 
                  command=self.clear_all).pack(side=tk.LEFT)
        
        # Results area
        self.results_text = tk.Text(main_frame, height=8, wrap=tk.WORD)
        self.results_text.grid(row=8, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(15, 0))
        
        # Scrollbar for results
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.results_text.yview)
        scrollbar.grid(row=8, column=3, sticky=(tk.N, tk.S))
        self.results_text.configure(yscrollcommand=scrollbar.set)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(8, weight=1)
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.webp *.bmp *.tiff"),
                ("All files", "*.*")
            ]
        )
        if files:
            self.input_files.extend(files)
            self.update_files_display()
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="Select Folder with Images")
        if folder:
            # Find all image files in folder
            image_extensions = ['.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff']
            folder_path = Path(folder)
            
            for ext in image_extensions:
                self.input_files.extend(str(f) for f in folder_path.glob(f"*{ext}"))
                self.input_files.extend(str(f) for f in folder_path.glob(f"*{ext.upper()}"))
            
            self.update_files_display()
    
    def select_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def update_files_display(self):
        self.files_listbox.delete(0, tk.END)
        for file in self.input_files:
            filename = os.path.basename(file)
            size_kb = os.path.getsize(file) / 1024
            self.files_listbox.insert(tk.END, f"{filename} ({size_kb:.1f} KB)")
    
    def clear_all(self):
        self.input_files.clear()
        self.files_listbox.delete(0, tk.END)
        self.results_text.delete(1.0, tk.END)
    
    def start_optimization(self):
        if not self.input_files:
            messagebox.showwarning("No Files", "Please select images to optimize!")
            return
        
        # Disable button and start progress
        self.optimize_button.config(state='disabled')
        self.progress.start()
        self.results_text.delete(1.0, tk.END)
        
        # Run optimization in separate thread
        thread = threading.Thread(target=self.run_optimization)
        thread.daemon = True
        thread.start()
    
    def run_optimization(self):
        try:
            optimizer = ImageOptimizer()
            
            # Prepare parameters
            target_kb = float(self.target_size.get()) if self.target_size.get() else None
            quality = int(self.quality.get()) if self.quality.get() else 85
            max_w = int(self.max_width.get()) if self.max_width.get() else None
            max_h = int(self.max_height.get()) if self.max_height.get() else None
            
            aspect_ratio = None
            if self.aspect_ratio.get():
                try:
                    w, h = map(int, self.aspect_ratio.get().split(':'))
                    aspect_ratio = (w, h)
                except:
                    self.log_result("❌ Invalid aspect ratio format!")
                    return
            
            # Process each file
            successful = 0
            total_original_size = 0
            total_final_size = 0
            
            for i, input_file in enumerate(self.input_files):
                self.log_result(f"\n📸 Processing {i+1}/{len(self.input_files)}: {os.path.basename(input_file)}")
                
                # Determine output path
                if self.output_folder.get():
                    output_dir = Path(self.output_folder.get())
                else:
                    output_dir = Path(input_file).parent / "optimized"
                
                output_dir.mkdir(exist_ok=True)
                
                input_name = Path(input_file).stem
                ext = optimizer.get_extension_for_format(self.output_format.get())
                output_file = output_dir / f"{input_name}_optimized{ext}"
                
                original_size = optimizer.get_file_size_kb(input_file)
                total_original_size += original_size
                
                result = optimizer.optimize_image(
                    input_path=input_file,
                    output_path=str(output_file),
                    target_size_kb=target_kb,
                    quality=quality,
                    max_width=max_w,
                    max_height=max_h,
                    output_format=self.output_format.get(),
                    aspect_ratio=aspect_ratio
                )
                
                if result:
                    final_size = optimizer.get_file_size_kb(result)
                    total_final_size += final_size
                    compression = (1 - final_size/original_size) * 100
                    
                    self.log_result(f"✅ {original_size:.1f} KB → {final_size:.1f} KB ({compression:.1f}% reduction)")
                    successful += 1
                else:
                    self.log_result("❌ Failed to optimize")
            
            # Summary
            total_compression = (1 - total_final_size/total_original_size) * 100 if total_original_size > 0 else 0
            self.log_result(f"\n🎉 Optimization Complete!")
            self.log_result(f"Successfully processed: {successful}/{len(self.input_files)} images")
            self.log_result(f"Total size reduction: {total_original_size:.1f} KB → {total_final_size:.1f} KB")
            self.log_result(f"Overall compression: {total_compression:.1f}%")
            
        except Exception as e:
            self.log_result(f"❌ Error: {str(e)}")
        finally:
            # Re-enable button and stop progress
            self.root.after(0, self.finish_optimization)
    
    def log_result(self, message):
        """Thread-safe logging to results text widget"""
        def update_text():
            self.results_text.insert(tk.END, message + "\n")
            self.results_text.see(tk.END)
            self.root.update_idletasks()
        
        self.root.after(0, update_text)
    
    def finish_optimization(self):
        self.progress.stop()
        self.optimize_button.config(state='normal')

# Same ImageOptimizer class from the previous script
class ImageOptimizer:
    def __init__(self):
        self.supported_formats = {
            'JPEG': ['.jpg', '.jpeg'],
            'PNG': ['.png'],
            'WEBP': ['.webp'],
            'AVIF': ['.avif']
        }
    
    def get_file_size_kb(self, filepath):
        return os.path.getsize(filepath) / 1024
    
    def optimize_image(self, input_path, output_path=None, target_size_kb=None, 
                      quality=85, max_width=None, max_height=None, 
                      output_format=None, aspect_ratio=None):
        try:
            with Image.open(input_path) as img:
                # Convert to RGB if necessary
                if img.mode in ('RGBA', 'LA', 'P'):
                    if output_format in ['JPEG']:
                        background = Image.new('RGB', img.size, (255, 255, 255))
                        if img.mode == 'P':
                            img = img.convert('RGBA')
                        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                        img = background
                    else:
                        img = img.convert('RGBA')
                elif img.mode != 'RGB':
                    img = img.convert('RGB')
                
                # Apply aspect ratio if specified
                if aspect_ratio:
                    img = self.change_aspect_ratio(img, aspect_ratio)
                
                # Resize if max dimensions specified
                if max_width or max_height:
                    img = self.resize_image(img, max_width, max_height)
                
                # Determine output format and path
                if not output_format:
                    output_format = 'JPEG'
                
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
                
                return str(output_path)
                
        except Exception as e:
            return None
    
    def change_aspect_ratio(self, img, aspect_ratio):
        target_width, target_height = aspect_ratio
        target_ratio = target_width / target_height
        current_ratio = img.width / img.height
        
        if current_ratio > target_ratio:
            new_width = int(img.height * target_ratio)
            left = (img.width - new_width) // 2
            img = img.crop((left, 0, left + new_width, img.height))
        elif current_ratio < target_ratio:
            new_height = int(img.width / target_ratio)
            top = (img.height - new_height) // 2
            img = img.crop((0, top, img.width, top + new_height))
        
        return img
    
    def resize_image(self, img, max_width=None, max_height=None):
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
        quality = 95
        min_quality = 10
        
        while quality >= min_quality:
            self.save_with_quality(img, output_path, quality, output_format)
            current_size_kb = self.get_file_size_kb(output_path)
            
            if current_size_kb <= target_kb:
                return
            
            quality -= 5
        
        # If still too large, try progressive resizing
        scale_factor = 0.9
        temp_img = img.copy()
        
        while scale_factor >= 0.3:
            new_size = (int(temp_img.width * scale_factor), int(temp_img.height * scale_factor))
            resized_img = temp_img.resize(new_size, Image.Resampling.LANCZOS)
            
            self.save_with_quality(resized_img, output_path, max(quality, 20), output_format)
            current_size_kb = self.get_file_size_kb(output_path)
            
            if current_size_kb <= target_kb:
                return
            
            scale_factor -= 0.1
    
    def save_with_quality(self, img, output_path, quality, output_format):
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
                'method': 6
            }
        elif output_format == 'AVIF':
            save_kwargs = {
                'format': 'AVIF',
                'quality': quality,
                'optimize': True
            }
        
        img.save(output_path, **save_kwargs)
    
    def get_extension_for_format(self, format_name):
        extensions = {
            'JPEG': '.jpg',
            'PNG': '.png',
            'WEBP': '.webp',
            'AVIF': '.avif'
        }
        return extensions.get(format_name, '.jpg')

def main():
    root = tk.Tk()
    app = ImageOptimizerGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()