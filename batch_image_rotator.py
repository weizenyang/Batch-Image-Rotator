import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
from PIL import Image, ImageTk
import numpy as np
from pathlib import Path

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

class BatchImageRotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Image Rotator")
        self.root.geometry("800x600")
        
        # Current batch of images
        self.current_batch = []
        self.rotation_angle = tk.DoubleVar(value=0.0)
        self.processing = False
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Batch Image Rotator", 
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=3, pady=(0, 20))
        
        # Drop zone
        self.setup_drop_zone(main_frame)
        
        # Controls
        self.setup_controls(main_frame)
        
        # Image list
        self.setup_image_list(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
        
    def setup_drop_zone(self, parent):
        # Drop zone frame
        drop_frame = ttk.LabelFrame(parent, text="Drop Images Here", padding="20")
        drop_frame.grid(row=1, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Drop zone
        self.drop_zone = tk.Label(drop_frame, text="Drag and drop images here\n(or click to browse)", 
                                 bg="lightgray", fg="darkgray", 
                                 font=("Arial", 12), height=4,
                                 relief=tk.SUNKEN, cursor="hand2")
        self.drop_zone.pack(fill=tk.BOTH, expand=True)
        
        # Bind click event
        self.drop_zone.bind("<Button-1>", self.browse_files)
        
        # Setup drag and drop if available
        if DND_AVAILABLE:
            self.drop_zone.drop_target_register(DND_FILES)
            self.drop_zone.dnd_bind('<<Drop>>', self.on_drop)
        else:
            self.drop_zone.config(text="Drag and drop not available\nClick to browse files")
            
    def setup_controls(self, parent):
        # Controls frame
        controls_frame = ttk.LabelFrame(parent, text="Rotation Controls", padding="10")
        controls_frame.grid(row=2, column=0, columnspan=3, sticky=(tk.W, tk.E), pady=(0, 20))
        
        # Rotation angle
        ttk.Label(controls_frame, text="Rotation Angle (degrees):").grid(row=0, column=0, sticky=tk.W)
        
        angle_frame = ttk.Frame(controls_frame)
        angle_frame.grid(row=0, column=1, sticky=(tk.W, tk.E), padx=(10, 0))
        
        self.angle_scale = ttk.Scale(angle_frame, from_=-180, to=180, 
                                   variable=self.rotation_angle, orient=tk.HORIZONTAL)
        self.angle_scale.grid(row=0, column=0, sticky=(tk.W, tk.E))
        
        self.angle_entry = ttk.Entry(angle_frame, textvariable=self.rotation_angle, width=10)
        self.angle_entry.grid(row=0, column=1, padx=(10, 0))
        
        angle_frame.columnconfigure(0, weight=1)
        
        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        self.process_button = ttk.Button(button_frame, text="Process Batch", 
                                       command=self.process_batch)
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear Batch", 
                                     command=self.clear_batch)
        self.clear_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.preview_button = ttk.Button(button_frame, text="Preview First Image", 
                                       command=self.preview_rotation)
        self.preview_button.pack(side=tk.LEFT)
        
        controls_frame.columnconfigure(1, weight=1)
        
    def setup_image_list(self, parent):
        # Image list frame
        list_frame = ttk.LabelFrame(parent, text="Current Batch", padding="10")
        list_frame.grid(row=3, column=0, columnspan=3, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 20))
        
        # Treeview for image list
        self.image_tree = ttk.Treeview(list_frame, columns=('path', 'size', 'format'), show='headings')
        self.image_tree.heading('path', text='File Path')
        self.image_tree.heading('size', text='Size')
        self.image_tree.heading('format', text='Format')
        
        # Configure column widths
        self.image_tree.column('path', width=400)
        self.image_tree.column('size', width=100)
        self.image_tree.column('format', width=80)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.image_tree.yview)
        self.image_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.image_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
    def setup_status_bar(self, parent):
        # Status frame
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=4, column=0, columnspan=3, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        self.progress_bar = ttk.Progressbar(status_frame, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 0))
        
    def on_drop(self, event):
        """Handle dropped files"""
        files = self.root.tk.splitlist(event.data)
        self.add_files(files)
        
    def browse_files(self, event=None):
        """Browse for files"""
        filetypes = [
            ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.tif *.webp"),
            ("All files", "*.*")
        ]
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=filetypes
        )
        if files:
            self.add_files(files)
            
    def add_files(self, files):
        """Add files to current batch"""
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.tif', '.webp'}
        added_count = 0
        
        for file_path in files:
            if os.path.isfile(file_path):
                ext = Path(file_path).suffix.lower()
                if ext in valid_extensions:
                    try:
                        # Get image info
                        with Image.open(file_path) as img:
                            size = f"{img.size[0]}x{img.size[1]}"
                            format_str = img.format or "Unknown"
                            
                        # Add to list if not already present
                        if file_path not in [item[0] for item in self.current_batch]:
                            self.current_batch.append((file_path, size, format_str))
                            self.image_tree.insert('', 'end', values=(file_path, size, format_str))
                            added_count += 1
                            
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
                        
        self.update_status(f"Added {added_count} images. Total: {len(self.current_batch)}")
        
    def clear_batch(self):
        """Clear current batch"""
        self.current_batch.clear()
        for item in self.image_tree.get_children():
            self.image_tree.delete(item)
        self.update_status("Batch cleared")
        
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
    def rotate_equirectangular(self, image, angle_degrees):
        """Rotate an equirectangular image"""
        if angle_degrees == 0:
            return image
            
        # Convert to numpy array
        img_array = np.array(image)
        height, width = img_array.shape[:2]
        
        # Calculate pixel shift for horizontal rotation
        angle_radians = np.radians(angle_degrees)
        shift_pixels = int((angle_radians / (2 * np.pi)) * width)
        
        # Roll the image horizontally
        if len(img_array.shape) == 3:  # Color image
            rotated_array = np.roll(img_array, shift_pixels, axis=1)
        else:  # Grayscale image
            rotated_array = np.roll(img_array, shift_pixels, axis=1)
            
        # Convert back to PIL Image
        return Image.fromarray(rotated_array)
        
    def preview_rotation(self):
        """Preview rotation on first image"""
        if not self.current_batch:
            messagebox.showwarning("No Images", "Please add images to the batch first.")
            return
            
        try:
            first_image_path = self.current_batch[0][0]
            with Image.open(first_image_path) as img:
                # Resize for preview
                img.thumbnail((400, 200), Image.Resampling.LANCZOS)
                
                # Apply rotation
                rotated_img = self.rotate_equirectangular(img, self.rotation_angle.get())
                
                # Show preview window
                self.show_preview_window(img, rotated_img)
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to preview image: {str(e)}")
            
    def show_preview_window(self, original, rotated):
        """Show preview window"""
        preview_window = tk.Toplevel(self.root)
        preview_window.title("Rotation Preview")
        preview_window.geometry("850x450")
        
        # Original image
        original_frame = ttk.LabelFrame(preview_window, text="Original", padding="10")
        original_frame.grid(row=0, column=0, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        original_tk = ImageTk.PhotoImage(original)
        original_label = ttk.Label(original_frame, image=original_tk)
        original_label.image = original_tk  # Keep a reference
        original_label.pack()
        
        # Rotated image
        rotated_frame = ttk.LabelFrame(preview_window, text=f"Rotated ({self.rotation_angle.get():.1f}°)", padding="10")
        rotated_frame.grid(row=0, column=1, padx=10, pady=10, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        rotated_tk = ImageTk.PhotoImage(rotated)
        rotated_label = ttk.Label(rotated_frame, image=rotated_tk)
        rotated_label.image = rotated_tk  # Keep a reference
        rotated_label.pack()
        
        # Close button
        close_button = ttk.Button(preview_window, text="Close", command=preview_window.destroy)
        close_button.grid(row=1, column=0, columnspan=2, pady=10)
        
    def process_batch(self):
        """Process the current batch"""
        if not self.current_batch:
            messagebox.showwarning("No Images", "Please add images to the batch first.")
            return
            
        if self.processing:
            return
            
        # Ask for output directory
        output_dir = filedialog.askdirectory(title="Select Output Directory")
        if not output_dir:
            return
            
        # Start processing in separate thread
        self.processing = True
        self.process_button.config(state='disabled')
        self.progress_bar.config(maximum=len(self.current_batch))
        
        thread = threading.Thread(target=self._process_batch_thread, args=(output_dir,))
        thread.daemon = True
        thread.start()
        
    def _process_batch_thread(self, output_dir):
        """Process batch in separate thread"""
        try:
            angle = self.rotation_angle.get()
            processed_count = 0
            
            for i, (file_path, _, _) in enumerate(self.current_batch):
                try:
                    # Update progress
                    self.root.after(0, self.update_status, f"Processing: {os.path.basename(file_path)}")
                    self.root.after(0, self.progress_bar.config, {'value': i})
                    
                    # Open and process image
                    with Image.open(file_path) as img:
                        # Rotate image
                        rotated_img = self.rotate_equirectangular(img, angle)
                        
                        # Generate output filename
                        input_path = Path(file_path)
                        output_filename = f"{input_path.stem}_rotated_{angle:.1f}deg{input_path.suffix}"
                        output_path = Path(output_dir) / output_filename
                        
                        # Save with same format and quality
                        save_kwargs = {}
                        if img.format == 'JPEG':
                            save_kwargs['quality'] = 95
                            save_kwargs['optimize'] = True
                        elif img.format == 'PNG':
                            save_kwargs['optimize'] = True
                            
                        rotated_img.save(output_path, **save_kwargs)
                        processed_count += 1
                        
                except Exception as e:
                    print(f"Error processing {file_path}: {e}")
                    
            # Update UI on completion
            self.root.after(0, self.progress_bar.config, {'value': len(self.current_batch)})
            self.root.after(0, self.update_status, f"Completed! Processed {processed_count} images")
            self.root.after(0, messagebox.showinfo, "Complete", 
                          f"Successfully processed {processed_count} images\nOutput directory: {output_dir}")
            
        except Exception as e:
            self.root.after(0, messagebox.showerror, "Error", f"Processing failed: {str(e)}")
            
        finally:
            # Re-enable UI
            self.root.after(0, self.process_button.config, {'state': 'normal'})
            self.root.after(0, self.progress_bar.config, {'value': 0})
            self.processing = False

def main():
    # Create root window
    if DND_AVAILABLE:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
        
    # Create application
    app = BatchImageRotator(root)
    
    # Start main loop
    root.mainloop()

if __name__ == "__main__":
    main() 