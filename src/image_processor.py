"""
Image Processor Module
Handles image processing operations including saving, format conversion, and optimization.
"""

import cv2
import numpy as np
from PIL import Image, ImageEnhance
from pathlib import Path
import logging
from typing import Optional, Tuple, Dict, Any


class ImageProcessor:
    """Handles image processing and file operations."""
    
    def __init__(self):
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
    def save_image(self, image: np.ndarray, output_path: str, quality: int = 95) -> bool:
        """
        Save image to file with specified quality.
        
        Args:
            image: Image as numpy array
            output_path: Path to save the image
            quality: JPEG quality (1-100)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            output_file = Path(output_path)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Get file extension
            extension = output_file.suffix.lower()
            
            if extension in ['.jpg', '.jpeg']:
                # Save as JPEG with quality setting
                cv2.imwrite(str(output_file), image, [cv2.IMWRITE_JPEG_QUALITY, quality])
            elif extension == '.png':
                # Save as PNG with compression
                cv2.imwrite(str(output_file), image, [cv2.IMWRITE_PNG_COMPRESSION, 6])
            else:
                # Default save
                cv2.imwrite(str(output_file), image)
                
            self.logger.info(f"Image saved: {output_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to save image: {e}")
            return False
            
    def resize_image(self, image: np.ndarray, target_size: Tuple[int, int], 
                    maintain_aspect: bool = True) -> np.ndarray:
        """
        Resize image to target size.
        
        Args:
            image: Input image
            target_size: Target (width, height)
            maintain_aspect: Whether to maintain aspect ratio
            
        Returns:
            Resized image
        """
        try:
            if maintain_aspect:
                # Calculate aspect ratio
                h, w = image.shape[:2]
                target_w, target_h = target_size
                
                # Calculate scaling factor
                scale = min(target_w / w, target_h / h)
                
                # Calculate new dimensions
                new_w = int(w * scale)
                new_h = int(h * scale)
                
                # Resize image
                resized = cv2.resize(image, (new_w, new_h), interpolation=cv2.INTER_LANCZOS4)
                
                # Create canvas and center the image
                canvas = np.zeros((target_h, target_w, 3), dtype=np.uint8)
                
                # Calculate position to center the image
                y_offset = (target_h - new_h) // 2
                x_offset = (target_w - new_w) // 2
                
                canvas[y_offset:y_offset+new_h, x_offset:x_offset+new_w] = resized
                
                return canvas
            else:
                # Direct resize without maintaining aspect ratio
                return cv2.resize(image, target_size, interpolation=cv2.INTER_LANCZOS4)
                
        except Exception as e:
            self.logger.error(f"Failed to resize image: {e}")
            return image
            
    def enhance_image(self, image: np.ndarray, config: Optional[Dict[str, Any]] = None) -> np.ndarray:
        """
        Apply image enhancements.
        
        Args:
            image: Input image
            config: Enhancement configuration
            
        Returns:
            Enhanced image
        """
        try:
            if config is None:
                config = {}
                
            enhanced = image.copy()
            
            # Brightness and contrast adjustment
            alpha = config.get('contrast', 1.0)  # Contrast control (1.0-3.0)
            beta = config.get('brightness', 0)   # Brightness control (0-100)
            
            if alpha != 1.0 or beta != 0:
                enhanced = cv2.convertScaleAbs(enhanced, alpha=alpha, beta=beta)
                
            # Saturation adjustment using PIL
            if config.get('saturation', 1.0) != 1.0:
                # Convert to PIL for saturation adjustment
                pil_image = Image.fromarray(cv2.cvtColor(enhanced, cv2.COLOR_BGR2RGB))
                enhancer = ImageEnhance.Color(pil_image)
                pil_image = enhancer.enhance(config.get('saturation', 1.0))
                enhanced = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
                
            # Sharpening
            if config.get('sharpen', False):
                kernel = np.array([[-1,-1,-1],
                                 [-1, 9,-1],
                                 [-1,-1,-1]])
                enhanced = cv2.filter2D(enhanced, -1, kernel)
                
            # Noise reduction
            if config.get('denoise', False):
                enhanced = cv2.fastNlMeansDenoisingColored(enhanced, None, 10, 10, 7, 21)
                
            return enhanced
            
        except Exception as e:
            self.logger.error(f"Failed to enhance image: {e}")
            return image
            
    def crop_image(self, image: np.ndarray, crop_box: Tuple[int, int, int, int]) -> np.ndarray:
        """
        Crop image to specified rectangle.
        
        Args:
            image: Input image
            crop_box: (x, y, width, height)
            
        Returns:
            Cropped image
        """
        try:
            x, y, w, h = crop_box
            
            # Ensure crop box is within image bounds
            img_h, img_w = image.shape[:2]
            x = max(0, min(x, img_w))
            y = max(0, min(y, img_h))
            w = min(w, img_w - x)
            h = min(h, img_h - y)
            
            return image[y:y+h, x:x+w]
            
        except Exception as e:
            self.logger.error(f"Failed to crop image: {e}")
            return image
            
    def rotate_image(self, image: np.ndarray, angle: float) -> np.ndarray:
        """
        Rotate image by specified angle.
        
        Args:
            image: Input image
            angle: Rotation angle in degrees
            
        Returns:
            Rotated image
        """
        try:
            h, w = image.shape[:2]
            center = (w // 2, h // 2)
            
            # Get rotation matrix
            matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
            
            # Calculate new dimensions
            cos = np.abs(matrix[0, 0])
            sin = np.abs(matrix[0, 1])
            
            new_w = int((h * sin) + (w * cos))
            new_h = int((h * cos) + (w * sin))
            
            # Adjust rotation matrix for new center
            matrix[0, 2] += (new_w / 2) - center[0]
            matrix[1, 2] += (new_h / 2) - center[1]
            
            # Perform rotation
            rotated = cv2.warpAffine(image, matrix, (new_w, new_h))
            
            return rotated
            
        except Exception as e:
            self.logger.error(f"Failed to rotate image: {e}")
            return image
            
    def flip_image(self, image: np.ndarray, horizontal: bool = True) -> np.ndarray:
        """
        Flip image horizontally or vertically.
        
        Args:
            image: Input image
            horizontal: If True, flip horizontally, else vertically
            
        Returns:
            Flipped image
        """
        try:
            if horizontal:
                return cv2.flip(image, 1)  # Horizontal flip
            else:
                return cv2.flip(image, 0)  # Vertical flip
                
        except Exception as e:
            self.logger.error(f"Failed to flip image: {e}")
            return image
            
    def convert_format(self, image: np.ndarray, target_format: str) -> Optional[np.ndarray]:
        """
        Convert image color format.
        
        Args:
            image: Input image
            target_format: Target format ('BGR', 'RGB', 'GRAY', 'HSV')
            
        Returns:
            Converted image or None if conversion fails
        """
        try:
            if target_format.upper() == 'RGB':
                return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            elif target_format.upper() == 'GRAY':
                return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            elif target_format.upper() == 'HSV':
                return cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            elif target_format.upper() == 'BGR':
                return image  # Already in BGR
            else:
                self.logger.warning(f"Unsupported format: {target_format}")
                return image
                
        except Exception as e:
            self.logger.error(f"Failed to convert image format: {e}")
            return None
            
    def get_image_info(self, image: np.ndarray) -> Dict[str, Any]:
        """
        Get information about an image.
        
        Args:
            image: Input image
            
        Returns:
            Dictionary with image information
        """
        try:
            info = {
                'shape': image.shape,
                'dtype': str(image.dtype),
                'size': image.size,
                'channels': len(image.shape) if len(image.shape) <= 3 else image.shape[2]
            }
            
            if len(image.shape) >= 2:
                info['height'] = image.shape[0]
                info['width'] = image.shape[1]
                
            if len(image.shape) == 3:
                info['channels'] = image.shape[2]
            else:
                info['channels'] = 1
                
            return info
            
        except Exception as e:
            self.logger.error(f"Failed to get image info: {e}")
            return {}
            
    def create_thumbnail(self, image: np.ndarray, max_size: Tuple[int, int] = (200, 200)) -> np.ndarray:
        """
        Create a thumbnail of the image.
        
        Args:
            image: Input image
            max_size: Maximum size for thumbnail
            
        Returns:
            Thumbnail image
        """
        try:
            return self.resize_image(image, max_size, maintain_aspect=True)
            
        except Exception as e:
            self.logger.error(f"Failed to create thumbnail: {e}")
            return image
            
    def apply_filter(self, image: np.ndarray, filter_type: str) -> np.ndarray:
        """
        Apply various filters to the image.
        
        Args:
            image: Input image
            filter_type: Type of filter to apply
            
        Returns:
            Filtered image
        """
        try:
            if filter_type == 'blur':
                return cv2.GaussianBlur(image, (15, 15), 0)
            elif filter_type == 'sharpen':
                kernel = np.array([[-1,-1,-1],
                                 [-1, 9,-1],
                                 [-1,-1,-1]])
                return cv2.filter2D(image, -1, kernel)
            elif filter_type == 'edge':
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
                edges = cv2.Canny(gray, 100, 200)
                return cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
            elif filter_type == 'emboss':
                kernel = np.array([[-2, -1, 0],
                                 [-1,  1, 1],
                                 [ 0,  1, 2]])
                return cv2.filter2D(image, -1, kernel)
            else:
                self.logger.warning(f"Unknown filter type: {filter_type}")
                return image
                
        except Exception as e:
            self.logger.error(f"Failed to apply filter: {e}")
            return image
            
    def validate_image(self, image: np.ndarray) -> bool:
        """
        Validate that image is in correct format.
        
        Args:
            image: Image to validate
            
        Returns:
            True if valid, False otherwise
        """
        try:
            if image is None:
                return False
                
            if not isinstance(image, np.ndarray):
                return False
                
            if len(image.shape) not in [2, 3]:
                return False
                
            if len(image.shape) == 3 and image.shape[2] not in [1, 3, 4]:
                return False
                
            return True
            
        except Exception:
            return False


# Example usage and testing
if __name__ == "__main__":
    # Test image processor
    processor = ImageProcessor()
    
    # Create a test image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    print("Image info:", processor.get_image_info(test_image))
    print("Image valid:", processor.validate_image(test_image))
    
    # Test resize
    resized = processor.resize_image(test_image, (320, 240))
    print("Resized shape:", resized.shape)
    
    # Test enhancement
    enhanced = processor.enhance_image(test_image, {'contrast': 1.2, 'brightness': 10})
    print("Enhanced shape:", enhanced.shape)
