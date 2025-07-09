import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import threading
import multiprocessing
from concurrent.futures import ProcessPoolExecutor, as_completed
from PIL import Image, ImageTk
import numpy as np
from pathlib import Path

try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    DND_AVAILABLE = True
except ImportError:
    DND_AVAILABLE = False

def rotate_equirectangular_worker(args):
    """Worker function for processing images in parallel"""
    file_path, angle, output_dir = args
    
    try:
        with Image.open(file_path) as img:
            # Rotate image
            if angle != 0:
                # Convert to numpy array
                img_array = np.array(img)
                height, width = img_array.shape[:2]
                
                # Calculate pixel shift for horizontal rotation
                angle_radians = np.radians(angle)
                shift_pixels = int((angle_radians / (2 * np.pi)) * width)
                
                # Roll the image horizontally
                if len(img_array.shape) == 3:  # Color image
                    rotated_array = np.roll(img_array, shift_pixels, axis=1)
                else:  # Grayscale image
                    rotated_array = np.roll(img_array, shift_pixels, axis=1)
                    
                # Convert back to PIL Image
                rotated_img = Image.fromarray(rotated_array)
            else:
                rotated_img = img.copy()
            
            # Generate output filename (no prefix/suffix)
            input_path = Path(file_path)
            output_path = Path(output_dir) / input_path.name
            
            # Save with same format and quality
            save_kwargs = {}
            if img.format == 'JPEG':
                save_kwargs['quality'] = 95
                save_kwargs['optimize'] = True
            elif img.format == 'PNG':
                save_kwargs['optimize'] = True
                
            rotated_img.save(output_path, **save_kwargs)
            return True, file_path
            
    except Exception as e:
        return False, f"Error processing {file_path}: {e}"

class BatchImageRotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Batch Image Rotator")
        self.root.geometry("600x400")
        
        # Current batch of images
        self.current_batch = []
        self.rotation_angle = tk.DoubleVar(value=0.0)
        self.processing = False
        self.num_workers = multiprocessing.cpu_count()
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Drop zone
        self.setup_drop_zone(main_frame)
        
        # Image list
        self.setup_image_list(main_frame)
        
        # Controls
        self.setup_controls(main_frame)
        
        # Status bar
        self.setup_status_bar(main_frame)
        
    def setup_drop_zone(self, parent):
        # Drop zone
        self.drop_zone = tk.Label(parent, text="Drop images here or click to browse", 
                                 bg="lightgray", fg="darkgray", 
                                 font=("Arial", 12), height=3,
                                 relief=tk.SUNKEN, cursor="hand2")
        self.drop_zone.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Bind click event
        self.drop_zone.bind("<Button-1>", self.browse_files)
        
        # Setup drag and drop if available
        if DND_AVAILABLE:
            self.drop_zone.drop_target_register(DND_FILES)
            self.drop_zone.dnd_bind('<<Drop>>', self.on_drop)
        else:
            self.drop_zone.config(text="Click to browse files")
            
    def setup_image_list(self, parent):
        # Image list frame
        list_frame = ttk.Frame(parent)
        list_frame.grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        
        # Treeview for image list
        self.image_tree = ttk.Treeview(list_frame, columns=('count',), show='headings')
        self.image_tree.heading('count', text=f'Images ({len(self.current_batch)})')
        self.image_tree.column('count', width=500)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.image_tree.yview)
        self.image_tree.configure(yscrollcommand=scrollbar.set)
        
        # Grid layout
        self.image_tree.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)
        
    def setup_controls(self, parent):
        # Controls frame
        controls_frame = ttk.Frame(parent)
        controls_frame.grid(row=2, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Rotation angle
        ttk.Label(controls_frame, text="Rotation (degrees):").grid(row=0, column=0, sticky=tk.W)
        
        self.angle_entry = ttk.Entry(controls_frame, textvariable=self.rotation_angle, width=10)
        self.angle_entry.grid(row=0, column=1, padx=(10, 0))
        
        # Buttons
        button_frame = ttk.Frame(controls_frame)
        button_frame.grid(row=0, column=2, padx=(20, 0))
        
        self.process_button = ttk.Button(button_frame, text="Process Batch", 
                                       command=self.process_batch)
        self.process_button.pack(side=tk.LEFT, padx=(0, 10))
        
        self.clear_button = ttk.Button(button_frame, text="Clear", 
                                     command=self.clear_batch)
        self.clear_button.pack(side=tk.LEFT)
        
        controls_frame.columnconfigure(2, weight=1)
        
    def setup_status_bar(self, parent):
        # Status frame
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=3, column=0, sticky=(tk.W, tk.E))
        
        self.status_label = ttk.Label(status_frame, text="Ready")
        self.status_label.pack(side=tk.LEFT)
        
        # Show number of workers
        worker_label = ttk.Label(status_frame, text=f"Workers: {self.num_workers}")
        worker_label.pack(side=tk.RIGHT)
        
        self.progress_bar = ttk.Progressbar(status_frame, mode='determinate')
        self.progress_bar.pack(side=tk.RIGHT, padx=(10, 10))
        
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
                        # Add to list if not already present
                        if file_path not in self.current_batch:
                            self.current_batch.append(file_path)
                            self.image_tree.insert('', 'end', values=(os.path.basename(file_path),))
                            added_count += 1
                            
                    except Exception as e:
                        print(f"Error processing {file_path}: {e}")
                        
        # Update header
        self.image_tree.heading('count', text=f'Images ({len(self.current_batch)})')
        self.update_status(f"Added {added_count} images")
        
    def clear_batch(self):
        """Clear current batch"""
        self.current_batch.clear()
        for item in self.image_tree.get_children():
            self.image_tree.delete(item)
        self.image_tree.heading('count', text='Images (0)')
        self.update_status("Cleared")
        
    def update_status(self, message):
        """Update status bar"""
        self.status_label.config(text=message)
        self.root.update_idletasks()
        
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
        """Process batch using multiple workers"""
        try:
            angle = self.rotation_angle.get()
            total_files = len(self.current_batch)
            
            # Prepare arguments for worker processes
            work_args = [(file_path, angle, output_dir) for file_path in self.current_batch]
            
            processed_count = 0
            failed_count = 0
            
            # Use ProcessPoolExecutor for parallel processing
            with ProcessPoolExecutor(max_workers=self.num_workers) as executor:
                # Submit all tasks
                future_to_file = {executor.submit(rotate_equirectangular_worker, args): args[0] 
                                 for args in work_args}
                
                # Process completed tasks
                for future in as_completed(future_to_file):
                    try:
                        success, result = future.result()
                        if success:
                            processed_count += 1
                        else:
                            failed_count += 1
                            print(result)  # Log error
                            
                        # Update progress
                        progress = processed_count + failed_count
                        self.root.after(0, self.progress_bar.config, {'value': progress})
                        self.root.after(0, self.update_status, f"Processing: {progress}/{total_files}")
                        
                    except Exception as e:
                        failed_count += 1
                        print(f"Worker error: {e}")
            
            # Update UI on completion
            self.root.after(0, self.update_status, f"Complete: {processed_count} processed, {failed_count} failed")
            if failed_count == 0:
                self.root.after(0, messagebox.showinfo, "Complete", 
                              f"Successfully processed {processed_count} images")
            else:
                self.root.after(0, messagebox.showwarning, "Complete", 
                              f"Processed {processed_count} images, {failed_count} failed")
            
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