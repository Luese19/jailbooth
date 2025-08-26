"""
The Slammer: Automated Mugshot Photo Booth
Main Application Entry Point

This is the primary application file that coordinates all components of the photo booth system.
It handles the GUI, camera interface, image processing, and file management.
"""

import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import cv2
import numpy as np
import threading
import time
from datetime import datetime
import json
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox
import cv2
import numpy as np
import threading
import time
from datetime import datetime
import json
from pathlib import Path

# Add src directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from camera_manager import CameraManager
from template_processor import TemplateProcessor
from image_processor import ImageProcessor
from config_manager import ConfigManager


class SlammerPhotoBoothApp:
    """Main application class for The Slammer photo booth system."""
    
    def __init__(self):
        self.root = tk.Tk()
        self.setup_window()
        
        # Load configuration
        self.config = ConfigManager()
        
        # Initialize components
        self.camera_manager = None
        self.template_processor = TemplateProcessor(self.config)
        self.image_processor = ImageProcessor()
        
        # State variables
        self.is_running = False
        self.preview_running = False
        self.capture_count = 0
        self.dual_capture_state = "ready"  # "ready", "waiting_for_second", "processing"
        self.first_image = None
        
        # Setup GUI
        self.setup_gui()
        
        # Initialize camera
        self.initialize_camera()
        
    def setup_window(self):
        """Configure the main application window."""
        self.root.title("Image Jail Booth - Automated Mugshot Photo Booth")
        self.root.geometry("1200x800")
        self.root.configure(bg='#1a1a1a')
        
        # Make window fullscreen capable
        self.root.attributes('-topmost', False)
        
        # Handle window closing
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def setup_gui(self):
        """Setup the graphical user interface."""
        # Main container
        main_frame = tk.Frame(self.root, bg='#1a1a1a')
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            main_frame, 
            text="IMAGE JAIL BOOTH", 
            font=("Arial", 24, "bold"),
            fg='#ffffff',
            bg='#1a1a1a'
        )
        title_label.pack(pady=(0, 20))
        
        # Create two columns
        content_frame = tk.Frame(main_frame, bg='#1a1a1a')
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left column - Camera preview
        self.setup_preview_panel(content_frame)
        
        # Right column - Controls
        self.setup_control_panel(content_frame)
        
        # Bottom status bar
        self.setup_status_bar(main_frame)
        
    def setup_preview_panel(self, parent):
        """Setup the camera preview panel."""
        preview_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        preview_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Preview title
        preview_title = tk.Label(
            preview_frame,
            text="LIVE PREVIEW",
            font=("Arial", 16, "bold"),
            fg='#ffffff',
            bg='#2a2a2a'
        )
        preview_title.pack(pady=10)
        
        # Camera preview canvas
        self.preview_canvas = tk.Canvas(
            preview_frame,
            bg='#000000',
            width=640,
            height=480
        )
        self.preview_canvas.pack(pady=10, padx=10, fill=tk.BOTH, expand=True)
        
        # Preview controls
        preview_controls = tk.Frame(preview_frame, bg='#2a2a2a')
        preview_controls.pack(pady=10)
        
        self.preview_button = tk.Button(
            preview_controls,
            text="Start Preview",
            command=self.toggle_preview,
            font=("Arial", 12),
            bg='#4CAF50',
            fg='white',
            relief=tk.RAISED,
            bd=2
        )
        self.preview_button.pack(side=tk.LEFT, padx=5)
        
    def setup_control_panel(self, parent):
        """Setup the control panel."""
        control_frame = tk.Frame(parent, bg='#2a2a2a', relief=tk.RAISED, bd=2)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=(10, 0))
        control_frame.config(width=300)
        
        # Control title
        control_title = tk.Label(
            control_frame,
            text="CONTROLS",
            font=("Arial", 16, "bold"),
            fg='#ffffff',
            bg='#2a2a2a'
        )
        control_title.pack(pady=10)
        
        # Capture section
        capture_section = tk.LabelFrame(
            control_frame,
            text="Capture",
            font=("Arial", 12, "bold"),
            fg='#ffffff',
            bg='#2a2a2a'
        )
        capture_section.pack(fill=tk.X, padx=10, pady=10)
        
        # Large capture button
        self.capture_button = tk.Button(
            capture_section,
            text="📸 CAPTURE MUGSHOT",
            command=self.capture_photo,
            font=("Arial", 14, "bold"),
            bg='#ff6b35',
            fg='white',
            height=3,
            relief=tk.RAISED,
            bd=3
        )
        self.capture_button.pack(fill=tk.X, padx=10, pady=10)
        
        # Stats section
        stats_section = tk.LabelFrame(
            control_frame,
            text="Statistics",
            font=("Arial", 12, "bold"),
            fg='#ffffff',
            bg='#2a2a2a'
        )
        stats_section.pack(fill=tk.X, padx=10, pady=10)
        
        self.stats_label = tk.Label(
            stats_section,
            text="Photos Captured: 0",
            font=("Arial", 11),
            fg='#ffffff',
            bg='#2a2a2a'
        )
        self.stats_label.pack(pady=5)
        
        # Settings section
        settings_section = tk.LabelFrame(
            control_frame,
            text="Settings",
            font=("Arial", 12, "bold"),
            fg='#ffffff',
            bg='#2a2a2a'
        )
        settings_section.pack(fill=tk.X, padx=10, pady=10)
        
        # Template selection
        tk.Label(
            settings_section,
            text="Template:",
            font=("Arial", 10),
            fg='#ffffff',
            bg='#2a2a2a'
        ).pack(anchor=tk.W, padx=5)
        
        # Get available templates
        available_templates = list(self.template_processor.templates.keys())
        default_template = self.config.get('default_template', 'dual_photo')
        
        self.template_var = tk.StringVar(value=default_template)
        self.template_combo = ttk.Combobox(
            settings_section,
            textvariable=self.template_var,
            values=available_templates,
            state="readonly"
        )
        self.template_combo.pack(fill=tk.X, padx=5, pady=5)
        
        # Action buttons
        action_frame = tk.Frame(settings_section, bg='#2a2a2a')
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        tk.Button(
            action_frame,
            text="Settings",
            command=self.open_settings,
            font=("Arial", 10),
            bg='#666666',
            fg='white'
        ).pack(side=tk.LEFT, padx=(0, 5))
        
        tk.Button(
            action_frame,
            text="Output Folder",
            command=self.open_output_folder,
            font=("Arial", 10),
            bg='#666666',
            fg='white'
        ).pack(side=tk.RIGHT)
        
    def setup_status_bar(self, parent):
        """Setup the status bar."""
        status_frame = tk.Frame(parent, bg='#333333', relief=tk.SUNKEN, bd=1)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.status_label = tk.Label(
            status_frame,
            text="Ready - Please connect camera and start preview",
            font=("Arial", 10),
            fg='#ffffff',
            bg='#333333'
        )
        self.status_label.pack(side=tk.LEFT, padx=5, pady=2)
        
        # Camera status indicator
        self.camera_status = tk.Label(
            status_frame,
            text="* Camera: Disconnected",
            font=("Arial", 10),
            fg='#ff4444',
            bg='#333333'
        )
        self.camera_status.pack(side=tk.RIGHT, padx=5, pady=2)
        
    def initialize_camera(self):
        """Initialize the camera manager."""
        try:
            self.camera_manager = CameraManager(self.config)
            if self.camera_manager.initialize():
                self.camera_status.config(text="* Camera: Connected", fg='#44ff44')
                self.status_label.config(text="Camera connected - Ready to start preview")
            else:
                self.camera_status.config(text="* Camera: Error", fg='#ff4444')
                self.status_label.config(text="Camera connection failed - Check hardware")
        except Exception as e:
            messagebox.showerror("Camera Error", f"Failed to initialize camera: {str(e)}")
            
    def toggle_preview(self):
        """Toggle camera preview on/off."""
        if not self.preview_running:
            self.start_preview()
        else:
            self.stop_preview()
            
    def start_preview(self):
        """Start the camera preview."""
        if not self.camera_manager or not self.camera_manager.is_connected():
            messagebox.showerror("Error", "Camera not connected")
            return
            
        self.preview_running = True
        self.preview_button.config(text="Stop Preview", bg='#f44336')
        self.status_label.config(text="Preview active - Ready to capture")
        
        # Start preview thread
        self.preview_thread = threading.Thread(target=self.preview_loop, daemon=True)
        self.preview_thread.start()
        
    def stop_preview(self):
        """Stop the camera preview."""
        self.preview_running = False
        self.preview_button.config(text="Start Preview", bg='#4CAF50')
        self.status_label.config(text="Preview stopped")
        
    def preview_loop(self):
        """Main preview loop running in separate thread."""
        from PIL import Image, ImageTk
        
        # Store canvas dimensions to avoid recalculating
        last_canvas_width = 0
        last_canvas_height = 0
        preview_image_id = None
        
        while self.preview_running:
            try:
                frame = self.camera_manager.get_frame() # type: ignore
                if frame is not None:
                    # Get canvas dimensions
                    canvas_width = self.preview_canvas.winfo_width()
                    canvas_height = self.preview_canvas.winfo_height()
                    
                    # Only proceed if canvas has valid dimensions
                    if canvas_width > 1 and canvas_height > 1:
                        # Check if canvas size changed
                        size_changed = (canvas_width != last_canvas_width or 
                                      canvas_height != last_canvas_height)
                        
                        if size_changed:
                            last_canvas_width = canvas_width
                            last_canvas_height = canvas_height
                            # Clear canvas only when size changes
                            self.preview_canvas.delete("all")
                            preview_image_id = None
                        
                        # Resize frame to fit canvas
                        frame_resized = cv2.resize(frame, (canvas_width, canvas_height))
                        
                        # Convert to PhotoImage
                        frame_rgb = cv2.cvtColor(frame_resized, cv2.COLOR_BGR2RGB)
                        pil_image = Image.fromarray(frame_rgb)
                        photo = ImageTk.PhotoImage(pil_image)
                        
                        # Update or create image on canvas
                        if preview_image_id is None:
                            # Create new image
                            preview_image_id = self.preview_canvas.create_image(
                                canvas_width//2, canvas_height//2, 
                                image=photo, 
                                anchor=tk.CENTER
                            )
                        else:
                            # Update existing image
                            self.preview_canvas.itemconfig(preview_image_id, image=photo)
                        
                        # Keep reference to prevent garbage collection
                        self.preview_canvas.image = photo  # pyright: ignore[reportAttributeAccessIssue]
                        
                # Reduced frame rate to prevent blinking (20 FPS instead of 30)
                time.sleep(1/20)
                
            except Exception as e:
                print(f"Preview error: {e}")
                time.sleep(0.1)
                
    def capture_photo(self):
        """Capture and process a photo."""
        if not self.camera_manager or not self.camera_manager.is_connected():
            messagebox.showerror("Error", "Camera not connected")
            return
            
        try:
            template_name = self.template_var.get()
            template = self.template_processor.templates.get(template_name)
            
            # Check if this is a dual photo template
            if template and template.get("dual_photo", False):
                self.handle_dual_capture()
            else:
                self.capture_single_photo()
                
        except Exception as e:
            messagebox.showerror("Capture Error", f"Failed to capture photo: {str(e)}")
            self.status_label.config(text="Capture failed - Try again")
            self.reset_dual_capture_state()
            
        finally:
            if self.dual_capture_state == "ready":
                self.capture_button.config(state=tk.NORMAL)
                
    def handle_dual_capture(self):
        """Handle the dual capture state machine."""
        if self.dual_capture_state == "ready":
            # First click - capture front view
            self.capture_first_shot()
        elif self.dual_capture_state == "waiting_for_second":
            # Second click - capture side view and process
            self.capture_second_shot()
            
    def capture_first_shot(self):
        """Capture the first shot (front view) for dual photos."""
        if not self.camera_manager:
            raise Exception("Camera manager not initialized")
            
        self.status_label.config(text="Capturing front view...")
        self.capture_button.config(state=tk.DISABLED)
        
        # Capture first image
        self.first_image = self.camera_manager.capture_image()
        if self.first_image is None:
            raise Exception("Failed to capture front view image")
            
        # Update state for second shot
        self.dual_capture_state = "waiting_for_second"
        self.status_label.config(text="Front captured! Turn to side view and click again")
        self.capture_button.config(text="📸 CAPTURE SIDE VIEW", state=tk.NORMAL)
        
    def capture_second_shot(self):
        """Capture the second shot (side view) and process both."""
        if not self.camera_manager:
            raise Exception("Camera manager not initialized")
            
        if self.first_image is None:
            raise Exception("First image not found")
            
        self.status_label.config(text="Capturing side view...")
        self.capture_button.config(state=tk.DISABLED)
        
        # Capture second image
        side_image = self.camera_manager.capture_image()
        if side_image is None:
            raise Exception("Failed to capture side view image")
            
        # Process both images
        self.status_label.config(text="Processing dual images...")
        processed_image = self.template_processor.process_dual_images(
            self.first_image, 
            side_image, 
            self.template_var.get()
        )
        
        if processed_image is None:
            raise Exception("Failed to process images with dual template")
        
        # Save and display
        self.save_and_display_photo(processed_image)
        
        # Reset state
        self.reset_dual_capture_state()
        
    def reset_dual_capture_state(self):
        """Reset the dual capture state to ready."""
        self.dual_capture_state = "ready"
        self.first_image = None
        self.capture_button.config(text="📸 CAPTURE MUGSHOT", state=tk.NORMAL)
            
    def capture_single_photo(self):
        """Capture and process a single photo."""
        if not self.camera_manager:
            raise Exception("Camera manager not initialized")
            
        self.status_label.config(text="Capturing photo...")
        self.capture_button.config(state=tk.DISABLED)
        
        # Capture image
        captured_image = self.camera_manager.capture_image()
        if captured_image is None:
            raise Exception("Failed to capture image")
            
        # Process with template
        processed_image = self.template_processor.process_image(
            captured_image, 
            self.template_var.get()
        )
        
        if processed_image is None:
            raise Exception("Failed to process image with template")
        
        # Save image
        self.save_and_display_photo(processed_image)
        
    def save_and_display_photo(self, processed_image):
        """Save the processed image and display it."""
        # Save image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"Mugshot_{timestamp}_{self.capture_count:03d}.jpg"
        output_path = Path(self.config.get('output_directory', 'output')) / filename
        
        self.image_processor.save_image(processed_image, str(output_path))
        
        # Update stats
        self.capture_count += 1
        self.stats_label.config(text=f"Photos Captured: {self.capture_count}")
        
        self.status_label.config(text=f"Photo saved: {filename}")
        
        # Show the captured photo
        self.show_captured_photo(processed_image)
            
    def show_captured_photo(self, image: np.ndarray):
        """Display the captured photo in a popup window."""
        try:
            import tkinter as tk
            from PIL import Image, ImageTk
            
            # Create popup window
            popup = tk.Toplevel(self.root)
            popup.title("Captured Photo")
            popup.geometry("600x800")
            popup.configure(bg='black')
            
            # Convert image for display
            # Resize for display while maintaining aspect ratio
            height, width = image.shape[:2]
            max_display_width = 550
            max_display_height = 750
            
            scale = min(max_display_width/width, max_display_height/height)
            new_width = int(width * scale)
            new_height = int(height * scale)
            
            display_image = cv2.resize(image, (new_width, new_height))
            display_image_rgb = cv2.cvtColor(display_image, cv2.COLOR_BGR2RGB)
            
            # Convert to PIL and then to PhotoImage
            pil_image = Image.fromarray(display_image_rgb)
            photo = ImageTk.PhotoImage(pil_image)
            
            # Create label to display image
            label = tk.Label(popup, image=photo, bg='black')
            label.pack(expand=True)
            
            # Keep a reference to prevent garbage collection
            label.image = photo # type: ignore
            
            # Add close button
            close_button = tk.Button(
                popup, 
                text="Close", 
                command=popup.destroy,
                font=("Arial", 12),
                bg='#ff6b35',
                fg='white'
            )
            close_button.pack(pady=10)
            
            # Auto-close after 5 seconds
            popup.after(5000, popup.destroy)
            
        except Exception as e:
            print(f"Error displaying captured photo: {e}")
            
    def open_settings(self):
        """Open comprehensive settings dialog."""
        settings_window = SettingsDialog(self.root, self.config)
        
        # If settings were changed, update the application
        if settings_window.settings_changed:
            self.update_from_settings()
            
    def update_from_settings(self):
        """Update application components when settings change."""
        try:
            # Update template processor
            self.template_processor = TemplateProcessor(self.config)
            
            # Update template dropdown
            self.update_template_dropdown()
            
            # Restart camera if camera settings changed
            if self.camera_manager:
                self.camera_manager.cleanup()
                time.sleep(0.5)  # Give time for cleanup
                self.camera_manager = CameraManager(self.config)
                
            messagebox.showinfo("Settings", "Settings updated successfully!")
            
        except Exception as e:
            messagebox.showerror("Settings Error", f"Error updating settings: {e}")
            
    def update_template_dropdown(self):
        """Update the template dropdown with available templates."""
        try:
            templates_dict = self.template_processor.get_available_templates()
            if templates_dict:
                template_names = list(templates_dict.keys())
                self.template_var.set('')  # Clear current selection
                self.template_combo['values'] = template_names
                
                # Set default template
                default_template = self.config.get('default_template', 'dual_photo')
                if default_template in template_names:
                    self.template_var.set(default_template)
                elif template_names:
                    self.template_var.set(template_names[0])
        except Exception as e:
            print(f"Error updating template dropdown: {e}")
        
    def open_output_folder(self):
        """Open the output folder."""
        output_dir = self.config.get('output_directory', 'output')
        if os.path.exists(output_dir):
            os.startfile(output_dir)
        else:
            messagebox.showwarning("Warning", "Output directory does not exist")
            
    def on_closing(self):
        """Handle application closing."""
        self.preview_running = False
        if self.camera_manager:
            self.camera_manager.cleanup()
        self.root.destroy()
        
    def run(self):
        """Start the application."""
        self.root.mainloop()


class SettingsDialog:
    """Comprehensive settings dialog for the photo booth."""
    
    def __init__(self, parent, config):
        """Initialize the settings dialog."""
        self.parent = parent
        self.config = config
        self.settings_changed = False
        
        # Create the dialog window
        self.window = tk.Toplevel(parent)
        self.window.title("Photo Booth Settings")
        self.window.geometry("600x500")
        self.window.configure(bg='#2a2a2a')
        self.window.resizable(True, True)
        
        # Make dialog modal
        self.window.transient(parent)
        self.window.grab_set()
        
        # Center the window
        self.center_window()
        
        # Store original values for comparison
        self.original_values = {}
        
        # Create the interface
        self.create_widgets()
        
        # Load current settings
        self.load_current_settings()
        
    def center_window(self):
        """Center the settings window on the parent."""
        self.window.update_idletasks()
        x = (self.parent.winfo_x() + (self.parent.winfo_width() // 2) - 
             (self.window.winfo_width() // 2))
        y = (self.parent.winfo_y() + (self.parent.winfo_height() // 2) - 
             (self.window.winfo_height() // 2))
        self.window.geometry(f"+{x}+{y}")
        
    def create_widgets(self):
        """Create the settings interface."""
        # Create notebook for tabs
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TNotebook', background='#2a2a2a')
        style.configure('TNotebook.Tab', background='#3a3a3a', foreground='white')
        
        self.notebook = ttk.Notebook(self.window)
        self.notebook.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Create tabs
        self.create_camera_tab()
        self.create_capture_tab()
        self.create_template_tab()
        self.create_output_tab()
        self.create_interface_tab()
        
        # Create buttons frame
        button_frame = tk.Frame(self.window, bg='#2a2a2a')
        button_frame.pack(fill=tk.X, padx=10, pady=(0, 10))
        
        # Buttons
        tk.Button(
            button_frame,
            text="Cancel",
            command=self.cancel,
            bg='#555555',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=10
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(
            button_frame,
            text="Apply",
            command=self.apply_settings,
            bg='#0066cc',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=10
        ).pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(
            button_frame,
            text="Reset to Defaults",
            command=self.reset_defaults,
            bg='#cc6600',
            fg='white',
            font=('Arial', 10, 'bold'),
            width=15
        ).pack(side=tk.LEFT)
        
    def create_camera_tab(self):
        """Create camera settings tab."""
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Camera")
        
        # Camera source
        self.create_setting_row(frame, "Camera Index:", "camera_index", "spinbox", (0, 10))
        
        # Resolution
        res_frame = tk.Frame(frame, bg='#2a2a2a')
        res_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(res_frame, text="Resolution:", bg='#2a2a2a', fg='white', font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.resolution_var = tk.StringVar()
        resolutions = ["1920x1080", "1280x720", "640x480", "Custom"]
        self.resolution_combo = ttk.Combobox(res_frame, textvariable=self.resolution_var, 
                                           values=resolutions, state="readonly", width=15)
        self.resolution_combo.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Frame rate
        self.create_setting_row(frame, "Frame Rate (FPS):", "camera_fps", "spinbox", (15, 60))
        
        # Image enhancement
        tk.Label(frame, text="Image Enhancement", bg='#2a2a2a', fg='#cccccc', 
                font=('Arial', 11, 'bold')).pack(pady=(15, 5))
        
        self.create_setting_row(frame, "Brightness:", "image_brightness", "scale", (-50, 50))
        self.create_setting_row(frame, "Contrast:", "image_contrast", "scale", (0.5, 2.0))
        self.create_setting_row(frame, "Noise Reduction:", "apply_denoising", "checkbox")
        
    def create_capture_tab(self):
        """Create capture settings tab."""
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Capture")
        
        self.create_setting_row(frame, "Countdown Timer (sec):", "capture_countdown", "spinbox", (0, 10))
        self.create_setting_row(frame, "Auto Save:", "auto_save", "checkbox")
        self.create_setting_row(frame, "Show Last Photo:", "show_last_photo", "checkbox")
        self.create_setting_row(frame, "Enable Sound:", "enable_sound", "checkbox")
        self.create_setting_row(frame, "Flash Enabled:", "flash_enabled", "checkbox")
        
    def create_template_tab(self):
        """Create template settings tab."""
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Templates")
        
        # Default template
        temp_frame = tk.Frame(frame, bg='#2a2a2a')
        temp_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(temp_frame, text="Default Template:", bg='#2a2a2a', fg='white', 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.template_var = tk.StringVar()
        self.template_combo = ttk.Combobox(temp_frame, textvariable=self.template_var, 
                                         state="readonly", width=20)
        self.template_combo.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Event information
        tk.Label(frame, text="Event Information", bg='#2a2a2a', fg='#cccccc', 
                font=('Arial', 11, 'bold')).pack(pady=(15, 5))
        
        self.create_setting_row(frame, "School/Organization:", "school_name", "entry")
        self.create_setting_row(frame, "Event Name:", "event_name", "entry")
        self.create_setting_row(frame, "Event Date:", "event_date", "entry")
        
    def create_output_tab(self):
        """Create output settings tab."""
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Output")
        
        # Output directory with browse button
        dir_frame = tk.Frame(frame, bg='#2a2a2a')
        dir_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(dir_frame, text="Output Directory:", bg='#2a2a2a', fg='white', 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.output_dir_var = tk.StringVar()
        self.output_dir_entry = tk.Entry(dir_frame, textvariable=self.output_dir_var, 
                                       bg='#3a3a3a', fg='white', width=25)
        self.output_dir_entry.pack(side=tk.RIGHT, padx=(5, 0))
        
        tk.Button(dir_frame, text="Browse", command=self.browse_output_dir,
                 bg='#555555', fg='white', font=('Arial', 8)).pack(side=tk.RIGHT)
        
        # File format
        format_frame = tk.Frame(frame, bg='#2a2a2a')
        format_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(format_frame, text="Image Format:", bg='#2a2a2a', fg='white', 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.format_var = tk.StringVar()
        formats = ["jpg", "png", "bmp"]
        self.format_combo = ttk.Combobox(format_frame, textvariable=self.format_var, 
                                       values=formats, state="readonly", width=10)
        self.format_combo.pack(side=tk.RIGHT, padx=(0, 10))
        
        self.create_setting_row(frame, "Image Quality (%):", "image_quality", "scale", (50, 100))
        self.create_setting_row(frame, "Filename Prefix:", "filename_prefix", "entry")
        self.create_setting_row(frame, "Include Timestamp:", "include_timestamp", "checkbox")
        
    def create_interface_tab(self):
        """Create interface settings tab."""
        frame = tk.Frame(self.notebook, bg='#2a2a2a')
        self.notebook.add(frame, text="Interface")
        
        self.create_setting_row(frame, "Fullscreen Mode:", "fullscreen_mode", "checkbox")
        
        # Preview size
        prev_frame = tk.Frame(frame, bg='#2a2a2a')
        prev_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(prev_frame, text="Preview Size:", bg='#2a2a2a', fg='white', 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.preview_size_var = tk.StringVar()
        preview_sizes = ["320x240", "640x480", "800x600", "1024x768"]
        self.preview_combo = ttk.Combobox(prev_frame, textvariable=self.preview_size_var, 
                                        values=preview_sizes, state="readonly", width=15)
        self.preview_combo.pack(side=tk.RIGHT, padx=(0, 10))
        
        # UI Theme
        theme_frame = tk.Frame(frame, bg='#2a2a2a')
        theme_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(theme_frame, text="UI Theme:", bg='#2a2a2a', fg='white', 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        self.theme_var = tk.StringVar()
        themes = ["dark", "light"]
        self.theme_combo = ttk.Combobox(theme_frame, textvariable=self.theme_var, 
                                      values=themes, state="readonly", width=10)
        self.theme_combo.pack(side=tk.RIGHT, padx=(0, 10))
        
        # Debug mode
        self.create_setting_row(frame, "Debug Mode:", "debug_mode", "checkbox")
        
    def create_setting_row(self, parent, label_text, config_key, widget_type, widget_range=None):
        """Create a settings row with label and input widget."""
        row_frame = tk.Frame(parent, bg='#2a2a2a')
        row_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Label
        tk.Label(row_frame, text=label_text, bg='#2a2a2a', fg='white', 
                font=('Arial', 10)).pack(side=tk.LEFT)
        
        # Store the variable for later access
        if not hasattr(self, 'setting_vars'):
            self.setting_vars = {}
        
        # Create appropriate widget
        var = None
        if widget_type == "entry":
            var = tk.StringVar()
            widget = tk.Entry(row_frame, textvariable=var, bg='#3a3a3a', fg='white', width=20)
            widget.pack(side=tk.RIGHT, padx=(0, 10))
            
        elif widget_type == "spinbox" and widget_range is not None:
            var = tk.StringVar()
            widget = tk.Spinbox(row_frame, textvariable=var, from_=widget_range[0], 
                              to=widget_range[1], bg='#3a3a3a', fg='white', width=10)
            widget.pack(side=tk.RIGHT, padx=(0, 10))
            
        elif widget_type == "scale" and widget_range is not None:
            var = tk.DoubleVar()
            widget = tk.Scale(row_frame, variable=var, from_=widget_range[0], 
                            to=widget_range[1], orient=tk.HORIZONTAL, bg='#3a3a3a', 
                            fg='white', length=150, resolution=0.1 if widget_range[1] <= 5 else 1)
            widget.pack(side=tk.RIGHT, padx=(0, 10))
            
        elif widget_type == "checkbox":
            var = tk.BooleanVar()
            widget = tk.Checkbutton(row_frame, variable=var, bg='#2a2a2a', fg='white',
                                  selectcolor='#3a3a3a', activebackground='#2a2a2a')
            widget.pack(side=tk.RIGHT, padx=(0, 10))
        
        if var is not None:
            self.setting_vars[config_key] = var
        
    def browse_output_dir(self):
        """Browse for output directory."""
        directory = filedialog.askdirectory(title="Select Output Directory")
        if directory:
            self.output_dir_var.set(directory)
            
    def load_current_settings(self):
        """Load current settings into the dialog."""
        try:
            # Load templates for dropdown
            from template_processor import TemplateProcessor
            tp = TemplateProcessor(self.config)
            templates_dict = tp.get_available_templates()
            if templates_dict:
                template_names = list(templates_dict.keys())
                self.template_combo['values'] = template_names
            
            # Load resolution
            resolution = self.config.get('camera_resolution', [1920, 1080])
            res_str = f"{resolution[0]}x{resolution[1]}"
            if res_str in self.resolution_combo['values']:
                self.resolution_var.set(res_str)
            else:
                self.resolution_var.set("Custom")
            
            # Load preview size
            preview_size = self.config.get('preview_size', [640, 480])
            prev_str = f"{preview_size[0]}x{preview_size[1]}"
            if prev_str in self.preview_combo['values']:
                self.preview_size_var.set(prev_str)
            else:
                self.preview_size_var.set("640x480")
            
            # Load other settings
            for key, var in self.setting_vars.items():
                value = self.config.get(key)
                if value is not None:
                    var.set(value)
                    self.original_values[key] = value
            
            # Load special settings
            self.output_dir_var.set(self.config.get('output_directory', 'output'))
            self.format_var.set(self.config.get('image_format', 'jpg'))
            self.template_var.set(self.config.get('default_template', 'dual_photo'))
            self.theme_var.set(self.config.get('ui_theme', 'dark'))
            
        except Exception as e:
            print(f"Error loading settings: {e}")
            
    def apply_settings(self):
        """Apply the changed settings."""
        try:
            changes_made = False
            
            # Check regular settings
            for key, var in self.setting_vars.items():
                new_value = var.get()
                if key not in self.original_values or self.original_values[key] != new_value:
                    self.config.set(key, new_value)
                    changes_made = True
            
            # Check special settings
            special_settings = {
                'output_directory': self.output_dir_var.get(),
                'image_format': self.format_var.get(),
                'default_template': self.template_var.get(),
                'ui_theme': self.theme_var.get()
            }
            
            for key, value in special_settings.items():
                if self.config.get(key) != value:
                    self.config.set(key, value)
                    changes_made = True
            
            # Handle resolution
            res_str = self.resolution_var.get()
            if res_str != "Custom":
                width, height = map(int, res_str.split('x'))
                if self.config.get('camera_resolution') != [width, height]:
                    self.config.set('camera_resolution', [width, height])
                    changes_made = True
            
            # Handle preview size
            prev_str = self.preview_size_var.get()
            width, height = map(int, prev_str.split('x'))
            if self.config.get('preview_size') != [width, height]:
                self.config.set('preview_size', [width, height])
                changes_made = True
            
            if changes_made:
                self.config.save_config()
                self.settings_changed = True
                
            self.window.destroy()
            
        except Exception as e:
            messagebox.showerror("Settings Error", f"Error saving settings: {e}")
            
    def reset_defaults(self):
        """Reset all settings to defaults."""
        if messagebox.askyesno("Reset Settings", "Reset all settings to defaults?"):
            self.config.reset_to_defaults()
            self.load_current_settings()
            
    def cancel(self):
        """Cancel settings dialog."""
        self.window.destroy()


def main():
    """Main entry point."""
    try:
        app = SlammerPhotoBoothApp()
        app.run()
    except Exception as e:
        print(f"Fatal error: {e}")
        messagebox.showerror("Fatal Error", f"Application failed to start: {str(e)}")


if __name__ == "__main__":
    main()
