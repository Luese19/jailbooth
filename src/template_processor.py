"""
Template Processor Module
Handles loading and applying mugshot templates to captured images.
"""

import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path
import json
from typing import Optional, Dict, Any, Tuple
import logging


class TemplateProcessor:
    """Processes images with mugshot templates."""
    
    def __init__(self, config):
        self.config = config
        self.template_dir = Path(config.get('template_directory', 'templates'))
        self.templates = {}
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load available templates
        self.load_templates()
        
    def load_templates(self):
        """Load all available templates from the templates directory."""
        try:
            if not self.template_dir.exists():
                self.template_dir.mkdir(parents=True, exist_ok=True)
                self.create_default_templates()
                
            # Load template configurations
            for template_file in self.template_dir.glob("*.json"):
                template_name = template_file.stem
                try:
                    with open(template_file, 'r', encoding='utf-8') as f:
                        template_config = json.load(f)
                    self.templates[template_name] = template_config
                    self.logger.info(f"Loaded template: {template_name}")
                except Exception as e:
                    self.logger.error(f"Failed to load template {template_name}: {e}")
                    
        except Exception as e:
            self.logger.error(f"Failed to load templates: {e}")
            
    def create_default_templates(self):
        """Create default template configurations."""
        # Default template
        default_template = {
            "name": "Default Mugshot",
            "description": "Basic mugshot template",
            "image_position": {
                "x": 100,
                "y": 150,
                "width": 400,
                "height": 500
            },
            "background": {
                "color": [240, 240, 240],
                "image": None
            },
            "text_elements": [
                {
                    "type": "title",
                    "text": "COUNTY JAIL",
                    "position": [300, 50],
                    "font_size": 36,
                    "color": [0, 0, 0],
                    "font_weight": "bold"
                },
                {
                    "type": "charge",
                    "text": "CAFETERIA BANDIT",
                    "position": [300, 700],
                    "font_size": 24,
                    "color": [200, 0, 0],
                    "font_weight": "normal"
                },
                {
                    "type": "date",
                    "text": "{event_date}",
                    "position": [300, 750],
                    "font_size": 18,
                    "color": [0, 0, 0],
                    "font_weight": "normal"
                },
                {
                    "type": "school",
                    "text": "{school_name}",
                    "position": [300, 800],
                    "font_size": 20,
                    "color": [50, 50, 150],
                    "font_weight": "bold"
                }
            ],
            "decorative_elements": [
                {
                    "type": "height_chart",
                    "position": [50, 150],
                    "height": 500
                },
                {
                    "type": "border",
                    "width": 5,
                    "color": [0, 0, 0]
                }
            ],
            "final_size": [600, 850]
        }
        
        # School template
        school_template = {
            "name": "School Event",
            "description": "School-themed mugshot template",
            "image_position": {
                "x": 100,
                "y": 150,
                "width": 400,
                "height": 500
            },
            "background": {
                "color": [250, 250, 250],
                "image": None
            },
            "text_elements": [
                {
                    "type": "title",
                    "text": "{school_name}",
                    "position": [300, 30],
                    "font_size": 32,
                    "color": [0, 50, 100],
                    "font_weight": "bold"
                },
                {
                    "type": "subtitle",
                    "text": "DETENTION CENTER",
                    "position": [300, 70],
                    "font_size": 24,
                    "color": [150, 0, 0],
                    "font_weight": "bold"
                },
                {
                    "type": "charge",
                    "text": "HOMEWORK AVOIDER",
                    "position": [300, 700],
                    "font_size": 22,
                    "color": [180, 0, 0],
                    "font_weight": "normal"
                },
                {
                    "type": "event",
                    "text": "{event_name}",
                    "position": [300, 740],
                    "font_size": 18,
                    "color": [0, 0, 0],
                    "font_weight": "normal"
                },
                {
                    "type": "date",
                    "text": "{event_date}",
                    "position": [300, 770],
                    "font_size": 16,
                    "color": [100, 100, 100],
                    "font_weight": "normal"
                }
            ],
            "decorative_elements": [
                {
                    "type": "height_chart",
                    "position": [50, 150],
                    "height": 500
                },
                {
                    "type": "school_logo",
                    "position": [500, 30],
                    "size": [80, 80]
                }
            ],
            "final_size": [600, 850]
        }
        
        # Party template
        party_template = {
            "name": "Party Mugshot",
            "description": "Fun party-themed template",
            "image_position": {
                "x": 100,
                "y": 150,
                "width": 400,
                "height": 500
            },
            "background": {
                "color": [255, 240, 200],
                "image": None
            },
            "text_elements": [
                {
                    "type": "title",
                    "text": "PARTY POLICE",
                    "position": [300, 50],
                    "font_size": 36,
                    "color": [255, 100, 50],
                    "font_weight": "bold"
                },
                {
                    "type": "charge",
                    "text": "EXCESSIVE FUN",
                    "position": [300, 700],
                    "font_size": 24,
                    "color": [200, 50, 150],
                    "font_weight": "normal"
                },
                {
                    "type": "date",
                    "text": "{event_date}",
                    "position": [300, 750],
                    "font_size": 18,
                    "color": [100, 50, 200],
                    "font_weight": "normal"
                }
            ],
            "decorative_elements": [
                {
                    "type": "height_chart",
                    "position": [50, 150],
                    "height": 500
                },
                {
                    "type": "party_border",
                    "width": 8,
                    "color": [255, 100, 50]
                }
            ],
            "final_size": [600, 850]
        }
        
        # Save templates
        templates = {
            "default": default_template,
            "school": school_template,
            "party": party_template
        }
        
        for name, template in templates.items():
            template_file = self.template_dir / f"{name}.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template, f, indent=4)
                
        self.logger.info("Default templates created")
        
    def process_image(self, image: np.ndarray, template_name: str) -> Optional[np.ndarray]:
        """
        Process an image with the specified template.
        
        Args:
            image: Input image as numpy array
            template_name: Name of template to apply
            
        Returns:
            Processed image or None if processing fails
        """
        try:
            if template_name not in self.templates:
                self.logger.error(f"Template not found: {template_name}")
                return None
                
            template = self.templates[template_name]
            
            # Create base canvas
            final_size = template["final_size"]
            canvas = self._create_canvas(template)
            
            # Handle dual photo templates
            if template.get("dual_photo", False) and "image_positions" in template:
                # Place photos in different orientations for front/side view
                for img_pos in template["image_positions"]:
                    # Create different processing for front vs side view
                    if img_pos.get("name") == "side_view":
                        # For side view, we can flip the image horizontally to simulate profile
                        side_image = cv2.flip(image, 1)  # Horizontal flip
                        processed_photo = self._process_photo_for_position(side_image, img_pos)
                    else:
                        # For front view, use original image
                        processed_photo = self._process_photo_for_position(image, img_pos)
                    
                    canvas = self._place_photo_at_position(canvas, processed_photo, img_pos)
                    
                    # Position labels removed per user request
                    # canvas = self._add_position_label(canvas, img_pos)
            else:
                # Single photo template (legacy)
                processed_photo = self._process_photo(image, template)
                canvas = self._place_photo(canvas, processed_photo, template)
                
            # Add text elements
            canvas = self._add_text_elements(canvas, template)
            
            # Add decorative elements
            canvas = self._add_decorative_elements(canvas, template)
            
            return canvas
            
        except Exception as e:
            self.logger.error(f"Failed to process image with template {template_name}: {e}")
            return None

    def process_dual_images(self, front_image: np.ndarray, side_image: np.ndarray, template_name: str) -> Optional[np.ndarray]:
        """
        Process two separate images with a dual photo template.
        
        Args:
            front_image: Image for the front view position
            side_image: Image for the side view position
            template_name: Name of template to apply (must be a dual photo template)
            
        Returns:
            Processed image or None if processing fails
        """
        try:
            if template_name not in self.templates:
                self.logger.error(f"Template not found: {template_name}")
                return None
                
            template = self.templates[template_name]
            
            # Verify this is a dual photo template
            if not template.get("dual_photo", False) or "image_positions" not in template:
                self.logger.error(f"Template {template_name} is not a dual photo template")
                return None
                
            # Create base canvas
            final_size = template["final_size"]
            canvas = self._create_canvas(template)
            
            # Process each position with the corresponding image
            for img_pos in template["image_positions"]:
                if img_pos.get("name") == "side_view":
                    # Use the second image for side view
                    processed_photo = self._process_photo_for_position(side_image, img_pos)
                else:
                    # Use the first image for front view (or any other position)
                    processed_photo = self._process_photo_for_position(front_image, img_pos)
                
                canvas = self._place_photo_at_position(canvas, processed_photo, img_pos)
            
            # Add text elements
            canvas = self._add_text_elements(canvas, template)
            
            # Add decorative elements
            canvas = self._add_decorative_elements(canvas, template)
            
            return canvas
            
        except Exception as e:
            self.logger.error(f"Failed to process dual images with template {template_name}: {e}")
            return None
            
    def _create_canvas(self, template: Dict[str, Any]) -> np.ndarray:
        """Create the base canvas for the template."""
        final_size = template["final_size"]
        background = template["background"]
        
        # Create canvas with background color
        canvas = np.full(
            (final_size[1], final_size[0], 3),
            background["color"],
            dtype=np.uint8
        )
        
        # If background image is specified, load and apply it
        if background.get("image"):
            bg_path = self.template_dir / background["image"]
            if bg_path.exists():
                bg_image = cv2.imread(str(bg_path))
                if bg_image is not None:
                    # final_size is [width, height], cv2.resize expects (width, height)
                    bg_resized = cv2.resize(bg_image, (final_size[0], final_size[1]))
                    canvas = bg_resized
                    
        return canvas
        
    def _process_photo(self, image: np.ndarray, template: Dict[str, Any]) -> np.ndarray:
        """Process the captured photo to fit the template."""
        image_pos = template["image_position"]
        target_size = (image_pos["width"], image_pos["height"])
        
        # Resize image to fit the designated area
        processed = cv2.resize(image, target_size)
        
        # Apply any photo-specific effects
        # (contrast, brightness adjustments can be added here)
        
        return processed
        
    def _place_photo(self, canvas: np.ndarray, photo: np.ndarray, template: Dict[str, Any]) -> np.ndarray:
        """Place the processed photo on the canvas."""
        image_pos = template["image_position"]
        
        x, y = image_pos["x"], image_pos["y"]
        h, w = photo.shape[:2]
        
        # Ensure placement is within canvas bounds
        if y + h <= canvas.shape[0] and x + w <= canvas.shape[1]:
            canvas[y:y+h, x:x+w] = photo
            
        return canvas
        
    def _process_photo_for_position(self, image: np.ndarray, image_pos: Dict[str, Any]) -> np.ndarray:
        """Process the captured photo for a specific position with proper alignment."""
        target_width = image_pos["width"]
        target_height = image_pos["height"]
        
        # Get original dimensions
        orig_height, orig_width = image.shape[:2]
        
        # Calculate scaling factors to maintain aspect ratio
        scale_x = target_width / orig_width
        scale_y = target_height / orig_height
        
        # Use the larger scale to ensure the image fills the area (crop if needed)
        scale = max(scale_x, scale_y)
        
        # Calculate new dimensions
        new_width = int(orig_width * scale)
        new_height = int(orig_height * scale)
        
        # Resize the image
        resized = cv2.resize(image, (new_width, new_height))
        
        # Create target canvas
        result = np.zeros((target_height, target_width, 3), dtype=np.uint8)
        result.fill(255)  # White background
        
        # Calculate centering offsets
        offset_x = (target_width - new_width) // 2
        offset_y = (target_height - new_height) // 2
        
        # Calculate crop boundaries if image is larger than target
        start_x = max(0, -offset_x)
        start_y = max(0, -offset_y)
        end_x = min(new_width, start_x + target_width)
        end_y = min(new_height, start_y + target_height)
        
        # Calculate placement boundaries on target canvas
        place_x = max(0, offset_x)
        place_y = max(0, offset_y)
        place_end_x = place_x + (end_x - start_x)
        place_end_y = place_y + (end_y - start_y)
        
        # Place the cropped/resized image onto the target canvas
        result[place_y:place_end_y, place_x:place_end_x] = resized[start_y:end_y, start_x:end_x]
        
        return result
        
    def _place_photo_at_position(self, canvas: np.ndarray, photo: np.ndarray, image_pos: Dict[str, Any]) -> np.ndarray:
        """Place the processed photo at a specific position on the canvas."""
        x, y = image_pos["x"], image_pos["y"]
        h, w = photo.shape[:2]
        
        # Ensure placement is within canvas bounds
        if y + h <= canvas.shape[0] and x + w <= canvas.shape[1]:
            canvas[y:y+h, x:x+w] = photo
            
        return canvas
    
    def _add_position_label(self, canvas: np.ndarray, image_pos: Dict[str, Any]) -> np.ndarray:
        """Add a label to identify the photo position (front/side view)."""
        try:
            position_name = image_pos.get("name", "")
            if position_name:
                # Convert position name to display text
                if position_name == "front_view":
                    label_text = "FRONT"
                elif position_name == "side_view":
                    label_text = "SIDE"
                else:
                    label_text = position_name.upper()
                
                # Position the label above the photo
                x = image_pos["x"]
                y = image_pos["y"] - 30  # 30 pixels above the photo
                
                # Make sure label is within canvas bounds
                if y > 20:
                    cv2.putText(canvas, label_text, (x, y), 
                              cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
        except Exception as e:
            self.logger.warning(f"Failed to add position label: {e}")
            
        return canvas
    
    def _add_text_elements(self, canvas: np.ndarray, template: Dict[str, Any]) -> np.ndarray:
        """Add text elements to the canvas."""
        # Convert to PIL for better text rendering
        pil_image = Image.fromarray(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_image)
        
        for text_element in template.get("text_elements", []):
            self._add_text_element(draw, text_element)
            
        # Convert back to OpenCV format
        canvas = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        return canvas
        
    def _add_text_element(self, draw: ImageDraw.Draw, element: Dict[str, Any]): # type: ignore
        """Add a single text element."""
        try:
            # Get text with variable substitution
            text = self._substitute_variables(element["text"])
            
            # Get font
            font_size = element.get("font_size", 20)
            font_weight = element.get("font_weight", "normal")
            
            try:
                # Try to load a system font
                if font_weight == "bold":
                    font = ImageFont.truetype("arial.ttf", font_size)
                else:
                    font = ImageFont.truetype("arial.ttf", font_size)
            except:
                # Fallback to default font
                font = ImageFont.load_default()
                
            # Get position and color
            position = tuple(element["position"])
            color = tuple(element["color"])
            
            # Draw text
            draw.text(position, text, font=font, fill=color)
            
        except Exception as e:
            self.logger.warning(f"Failed to add text element: {e}")
            
    def _substitute_variables(self, text: str) -> str:
        """Substitute template variables with actual values."""
        substitutions = {
            "{school_name}": self.config.get("school_name", "Your School"),
            "{event_name}": self.config.get("event_name", "Photo Booth Event"),
            "{event_date}": self.config.get("event_date", "2025-08-24")
        }
        
        for variable, value in substitutions.items():
            text = text.replace(variable, value)
            
        return text
        
    def _add_decorative_elements(self, canvas: np.ndarray, template: Dict[str, Any]) -> np.ndarray:
        """Add decorative elements to the canvas."""
        for element in template.get("decorative_elements", []):
            if element["type"] == "height_chart":
                canvas = self._add_height_chart(canvas, element)
            elif element["type"] == "border":
                canvas = self._add_border(canvas, element)
            elif element["type"] == "divider_line":
                canvas = self._add_divider_line(canvas, element)
                
        return canvas
        
    def _add_height_chart(self, canvas: np.ndarray, element: Dict[str, Any]) -> np.ndarray:
        """Add a height chart element."""
        try:
            x, y = element["position"]
            height = element["height"]
            
            # Draw height marks
            for i in range(0, height, 50):  # Every 50 pixels
                mark_y = y + i
                cv2.line(canvas, (x, mark_y), (x + 30, mark_y), (0, 0, 0), 2)
                
                # Add height labels (simplified)
                if i % 100 == 0:  # Every 100 pixels
                    cv2.putText(
                        canvas,
                        f"{i//10}",  # Simplified height marking
                        (x - 25, mark_y + 5),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 0, 0),
                        1
                    )
                    
        except Exception as e:
            self.logger.warning(f"Failed to add height chart: {e}")
            
        return canvas
        
    def _add_border(self, canvas: np.ndarray, element: Dict[str, Any]) -> np.ndarray:
        """Add a border element."""
        try:
            width = element.get("width", 5)
            color = tuple(element.get("color", [0, 0, 0]))
            
            h, w = canvas.shape[:2]
            
            # Draw border
            cv2.rectangle(canvas, (0, 0), (w-1, h-1), color, width)
            
        except Exception as e:
            self.logger.warning(f"Failed to add border: {e}")
            
        return canvas
        
    def _add_divider_line(self, canvas: np.ndarray, element: Dict[str, Any]) -> np.ndarray:
        """Add a divider line element."""
        try:
            start = tuple(element.get("start", [0, 0]))
            end = tuple(element.get("end", [100, 100]))
            width = element.get("width", 2)
            color = tuple(element.get("color", [150, 150, 150]))
            
            # Draw line
            cv2.line(canvas, start, end, color, width)
            
        except Exception as e:
            self.logger.warning(f"Failed to add divider line: {e}")
            
        return canvas
        
    def get_available_templates(self) -> Dict[str, str]:
        """Get list of available templates."""
        return {
            name: template.get("description", "No description")
            for name, template in self.templates.items()
        }
        
    def add_custom_template(self, name: str, template_config: Dict[str, Any]) -> bool:
        """Add a custom template."""
        try:
            template_file = self.template_dir / f"{name}.json"
            with open(template_file, 'w', encoding='utf-8') as f:
                json.dump(template_config, f, indent=4)
                
            self.templates[name] = template_config
            self.logger.info(f"Custom template added: {name}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to add custom template: {e}")
            return False


# Example usage and testing
if __name__ == "__main__":
    from config_manager import ConfigManager
    import numpy as np
    
    # Test template processor
    config = ConfigManager()
    processor = TemplateProcessor(config)
    
    print("Available templates:", processor.get_available_templates())
    
    # Create a test image
    test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
    
    # Process with default template
    result = processor.process_image(test_image, "default")
    if result is not None:
        print(f"Template processing successful: {result.shape}")
    else:
        print("Template processing failed")
