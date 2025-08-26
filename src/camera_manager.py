"""
Camera Manager Module
Handles camera initialization, live preview, and image capture for various camera types.
"""

import cv2
import numpy as np
import time
from typing import Optional, Tuple, Union, Any
import logging


class CameraManager:
    """Manages camera operations for the photo booth."""
    
    def __init__(self, config: Optional[Any] = None):
        self.config = config if config is not None else {}
        self.camera = None
        self.camera_type = None
        self.is_initialized = False
        
        # Camera settings with safe get method
        self.resolution = self._get_config('camera_resolution', (1920, 1080))
        self.fps = self._get_config('camera_fps', 30)
        self.camera_index = self._get_config('camera_index', 0)
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def _get_config(self, key: str, default: Any) -> Any:
        """Safely get configuration value with default."""
        if hasattr(self.config, 'get'):
            return self.config.get(key, default)
        elif isinstance(self.config, dict):
            return self.config.get(key, default)
        else:
            return default
        
    def initialize(self) -> bool:
        """
        Initialize camera connection.
        Tries multiple camera types and fallback options.
        """
        # Try different camera initialization methods
        camera_methods = [
            self._init_usb_camera,
            self._init_dslr_camera,
            self._init_webcam_fallback
        ]
        
        for method in camera_methods:
            try:
                if method():
                    self.is_initialized = True
                    self.logger.info(f"Camera initialized successfully: {self.camera_type}")
                    return True
            except Exception as e:
                self.logger.warning(f"Camera initialization method failed: {e}")
                continue
                
        self.logger.error("All camera initialization methods failed")
        return False
        
    def _init_usb_camera(self) -> bool:
        """Initialize USB/HDMI capture card camera."""
        try:
            # Try DirectShow backend for Windows
            self.camera = cv2.VideoCapture(self.camera_index, cv2.CAP_DSHOW)
            
            if not self.camera.isOpened():
                return False
                
            # Set camera properties
            self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, self.resolution[0])
            self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, self.resolution[1])
            self.camera.set(cv2.CAP_PROP_FPS, self.fps)
            
            # Test capture
            ret, frame = self.camera.read()
            if ret and frame is not None:
                self.camera_type = "USB/HDMI Capture"
                return True
                
            return False
            
        except Exception as e:
            self.logger.error(f"USB camera initialization failed: {e}")
            return False
            
    def _init_dslr_camera(self) -> bool:
        """Initialize DSLR camera via USB tethering."""
        try:
            # This would require camera-specific libraries
            # For now, we'll use a placeholder that could be extended
            
            # Example for gPhoto2 (would need python-gphoto2 installed)
            # try:
            #     import gphoto2 as gp
            #     camera = gp.Camera()
            #     camera.init()
            #     self.camera = camera
            #     self.camera_type = "DSLR (gPhoto2)"
            #     return True
            # except ImportError:
            #     pass
            
            # For now, return False to fall back to other methods
            return False
            
        except Exception as e:
            self.logger.error(f"DSLR camera initialization failed: {e}")
            return False
            
    def _init_webcam_fallback(self) -> bool:
        """Initialize standard webcam as fallback."""
        try:
            # Try different camera indices
            for index in range(3):
                self.camera = cv2.VideoCapture(index)
                if self.camera.isOpened():
                    # Test capture
                    ret, frame = self.camera.read()
                    if ret and frame is not None:
                        self.camera_type = f"Webcam (Index {index})"
                        self.camera_index = index
                        
                        # Set basic properties
                        self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
                        self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)
                        
                        return True
                    else:
                        self.camera.release()
                        
            return False
            
        except Exception as e:
            self.logger.error(f"Webcam fallback initialization failed: {e}")
            return False
            
    def is_connected(self) -> bool:
        """Check if camera is connected and working."""
        return self.is_initialized and self.camera is not None
        
    def get_frame(self) -> Optional[np.ndarray]:
        """
        Get current frame from camera for preview.
        Returns None if capture fails.
        """
        if not self.is_connected() or self.camera is None:
            return None
            
        try:
            frame = None
            # Read a couple of frames to get the latest one
            # This helps reduce lag and stuttering in preview
            for _ in range(2):
                ret, frame = self.camera.read()
                if not ret:
                    return None
                    
            if frame is not None:
                return frame
            return None
            
        except Exception as e:
            self.logger.error(f"Frame capture failed: {e}")
            return None
            
    def capture_image(self) -> Optional[np.ndarray]:
        """
        Capture high-quality image for processing.
        May use different settings than live preview.
        """
        if not self.is_connected() or self.camera is None:
            return None
            
        try:
            # For better quality, we might want to adjust camera settings
            # or capture multiple frames and select the best one
            
            # Capture a few frames to ensure camera is stable
            for _ in range(3):
                ret, frame = self.camera.read()
                if not ret:
                    continue
                time.sleep(0.1)
                
            # Capture the final frame
            ret, frame = self.camera.read()
            if ret and frame is not None:
                # Apply any post-processing for quality
                frame = self._enhance_image(frame)
                return frame
                
            return None
            
        except Exception as e:
            self.logger.error(f"Image capture failed: {e}")
            return None
            
    def _enhance_image(self, image: np.ndarray) -> np.ndarray:
        """Apply basic image enhancements."""
        try:
            # Convert to RGB for processing
            if len(image.shape) == 3 and image.shape[2] == 3:
                # Basic contrast and brightness adjustment
                alpha = self._get_config('image_contrast', 1.1)  # Contrast
                beta = self._get_config('image_brightness', 10)   # Brightness
                
                enhanced = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)
                
                # Optional: Apply denoising
                if self._get_config('apply_denoising', True):
                    enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
                    
                return enhanced
            
            return image
            
        except Exception as e:
            self.logger.warning(f"Image enhancement failed, using original: {e}")
            return image
            
    def get_camera_info(self) -> dict:
        """Get information about the current camera."""
        if not self.is_connected() or self.camera is None:
            return {"status": "disconnected"}
            
        try:
            info = {
                "status": "connected",
                "type": self.camera_type,
                "index": self.camera_index,
                "resolution": self.resolution,
                "fps": self.fps
            }
            
            # Get actual camera properties if available
            if hasattr(self.camera, 'get') and self.camera is not None:
                actual_width = self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
                actual_height = self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
                actual_fps = self.camera.get(cv2.CAP_PROP_FPS)
                
                info.update({
                    "actual_resolution": (int(actual_width), int(actual_height)),
                    "actual_fps": actual_fps
                })
                
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get camera info: {e}")
            return {"status": "error", "error": str(e)}
            
    def set_camera_setting(self, setting: str, value) -> bool:
        """Set a camera setting."""
        if not self.is_connected() or self.camera is None:
            return False
            
        try:
            setting_map = {
                'brightness': cv2.CAP_PROP_BRIGHTNESS,
                'contrast': cv2.CAP_PROP_CONTRAST,
                'saturation': cv2.CAP_PROP_SATURATION,
                'exposure': cv2.CAP_PROP_EXPOSURE,
                'gain': cv2.CAP_PROP_GAIN,
                'white_balance': cv2.CAP_PROP_WHITE_BALANCE_BLUE_U
            }
            
            if setting in setting_map and self.camera is not None:
                return self.camera.set(setting_map[setting], value)
                
            return False
            
        except Exception as e:
            self.logger.error(f"Failed to set camera setting {setting}: {e}")
            return False
            
    def cleanup(self):
        """Clean up camera resources."""
        try:
            if self.camera is not None:
                self.camera.release()
                self.camera = None
                
            self.is_initialized = False
            self.logger.info("Camera cleanup completed")
            
        except Exception as e:
            self.logger.error(f"Camera cleanup failed: {e}")


# Example usage and testing
if __name__ == "__main__":
    # Simple test of camera manager
    from config_manager import ConfigManager
    
    config = ConfigManager()
    camera_manager = CameraManager(config)
    
    if camera_manager.initialize():
        print("Camera initialized successfully!")
        print("Camera info:", camera_manager.get_camera_info())
        
        # Test frame capture
        frame = camera_manager.get_frame()
        if frame is not None:
            print(f"Frame captured: {frame.shape}")
            
        # Test image capture
        image = camera_manager.capture_image()
        if image is not None:
            print(f"Image captured: {image.shape}")
            
        camera_manager.cleanup()
    else:
        print("Failed to initialize camera")
