"""
Configuration Manager Module
Handles loading and managing configuration settings for the photo booth.
"""

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional
import logging


class ConfigManager:
    """Manages configuration settings for the photo booth system."""
    
    def __init__(self, config_file: Optional[str] = None):
        """
        Initialize configuration manager.
        
        Args:
            config_file: Path to configuration file. If None, uses default location.
        """
        if config_file is None:
            # Default configuration file location
            project_root = Path(__file__).parent.parent
            self.config_file = project_root / "config" / "settings.json"
        else:
            self.config_file = Path(config_file)
        self.config_data = {}
        self.default_config = self._get_default_config()
        
        # Setup logging
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)
        
        # Load configuration
        self.load_config()
        
    def _get_default_config(self) -> Dict[str, Any]:
        """Get default configuration values."""
        return {
            # Camera settings
            "camera_index": 0,
            "camera_resolution": [1920, 1080],
            "camera_fps": 30,
            "image_contrast": 1.1,
            "image_brightness": 10,
            "apply_denoising": True,
            
            # Template settings
            "default_template": "dual_photo",
            "template_directory": "templates",
            "school_name": "Your School Name",
            "event_name": "Photo Booth Event",
            "event_date": "2025-08-24",
            
            # Output settings
            "output_directory": "output",
            "image_format": "jpg",
            "image_quality": 95,
            "filename_prefix": "Mugshot",
            "include_timestamp": True,
            
            # Display settings
            "fullscreen_mode": False,
            "preview_size": [640, 480],
            "ui_theme": "dark",
            
            # Booth settings
            "capture_countdown": 3,
            "auto_save": True,
            "show_last_photo": True,
            "enable_sound": True,
            
            # Hardware settings
            "use_external_trigger": False,
            "trigger_pin": None,
            "flash_enabled": False,
            
            # Advanced settings
            "debug_mode": False,
            "log_level": "INFO",
            "max_retries": 3,
            "timeout_seconds": 30
        }
        
    def load_config(self):
        """Load configuration from file, create with defaults if not found."""
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    loaded_config = json.load(f)
                    
                # Merge with defaults (defaults for missing keys)
                self.config_data = {**self.default_config, **loaded_config}
                self.logger.info(f"Configuration loaded from {self.config_file}")
                
            else:
                # Create default configuration file
                self.config_data = self.default_config.copy()
                self.save_config()
                self.logger.info(f"Default configuration created at {self.config_file}")
                
        except Exception as e:
            self.logger.error(f"Failed to load configuration: {e}")
            self.config_data = self.default_config.copy()
            
    def save_config(self):
        """Save current configuration to file."""
        try:
            # Ensure config directory exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
                
            self.logger.info(f"Configuration saved to {self.config_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to save configuration: {e}")
            
    def get(self, key: str, default_value: Any = None) -> Any:
        """
        Get configuration value by key.
        
        Args:
            key: Configuration key
            default_value: Value to return if key not found
            
        Returns:
            Configuration value or default_value
        """
        return self.config_data.get(key, default_value)
        
    def set(self, key: str, value: Any):
        """
        Set configuration value.
        
        Args:
            key: Configuration key
            value: Value to set
        """
        self.config_data[key] = value
        
    def update(self, config_dict: Dict[str, Any]):
        """
        Update multiple configuration values.
        
        Args:
            config_dict: Dictionary of key-value pairs to update
        """
        self.config_data.update(config_dict)
        
    def get_camera_config(self) -> Dict[str, Any]:
        """Get camera-specific configuration."""
        return {
            "camera_index": self.get("camera_index"),
            "camera_resolution": tuple(self.get("camera_resolution")),
            "camera_fps": self.get("camera_fps"),
            "image_contrast": self.get("image_contrast"),
            "image_brightness": self.get("image_brightness"),
            "apply_denoising": self.get("apply_denoising")
        }
        
    def get_template_config(self) -> Dict[str, Any]:
        """Get template-specific configuration."""
        return {
            "default_template": self.get("default_template"),
            "template_directory": self.get("template_directory"),
            "school_name": self.get("school_name"),
            "event_name": self.get("event_name"),
            "event_date": self.get("event_date")
        }
        
    def get_output_config(self) -> Dict[str, Any]:
        """Get output-specific configuration."""
        return {
            "output_directory": self.get("output_directory"),
            "image_format": self.get("image_format"),
            "image_quality": self.get("image_quality"),
            "filename_prefix": self.get("filename_prefix"),
            "include_timestamp": self.get("include_timestamp")
        }
        
    def validate_config(self) -> Dict[str, str]:
        """
        Validate configuration values.
        
        Returns:
            Dictionary of validation errors (empty if all valid)
        """
        errors = {}
        
        # Validate camera settings
        camera_index = self.get("camera_index")
        if not isinstance(camera_index, int) or camera_index < 0:
            errors["camera_index"] = "Must be a non-negative integer"
            
        resolution = self.get("camera_resolution")
        if not isinstance(resolution, list) or len(resolution) != 2:
            errors["camera_resolution"] = "Must be a list of two integers [width, height]"
            
        # Validate paths
        template_dir = self.get("template_directory")
        if not template_dir:
            errors["template_directory"] = "Template directory cannot be empty"
            
        output_dir = self.get("output_directory")
        if not output_dir:
            errors["output_directory"] = "Output directory cannot be empty"
            
        # Validate image quality
        quality = self.get("image_quality")
        if not isinstance(quality, int) or quality < 1 or quality > 100:
            errors["image_quality"] = "Image quality must be between 1 and 100"
            
        return errors
        
    def reset_to_defaults(self):
        """Reset configuration to default values."""
        self.config_data = self.default_config.copy()
        self.logger.info("Configuration reset to defaults")
        
    def export_config(self, export_path: str):
        """
        Export current configuration to a file.
        
        Args:
            export_path: Path to export file
        """
        try:
            export_file = Path(export_path)
            export_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(export_file, 'w', encoding='utf-8') as f:
                json.dump(self.config_data, f, indent=4, ensure_ascii=False)
                
            self.logger.info(f"Configuration exported to {export_file}")
            
        except Exception as e:
            self.logger.error(f"Failed to export configuration: {e}")
            
    def import_config(self, import_path: str) -> bool:
        """
        Import configuration from a file.
        
        Args:
            import_path: Path to import file
            
        Returns:
            True if successful, False otherwise
        """
        try:
            import_file = Path(import_path)
            if not import_file.exists():
                self.logger.error(f"Import file does not exist: {import_file}")
                return False
                
            with open(import_file, 'r', encoding='utf-8') as f:
                imported_config = json.load(f)
                
            # Validate imported configuration
            temp_config = {**self.default_config, **imported_config}
            
            # If validation passes, update current config
            self.config_data = temp_config
            self.logger.info(f"Configuration imported from {import_file}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to import configuration: {e}")
            return False
            
    def get_all_settings(self) -> Dict[str, Any]:
        """Get all configuration settings."""
        return self.config_data.copy()
        
    def __str__(self) -> str:
        """String representation of configuration."""
        return f"ConfigManager(file={self.config_file}, settings={len(self.config_data)})"
        
    def __repr__(self) -> str:
        """Detailed string representation."""
        return f"ConfigManager(config_file='{self.config_file}', config_data={self.config_data})"


# Example usage and testing
if __name__ == "__main__":
    # Test configuration manager
    config = ConfigManager()
    
    print("Configuration loaded:")
    print(f"Camera index: {config.get('camera_index')}")
    print(f"Resolution: {config.get('camera_resolution')}")
    print(f"School name: {config.get('school_name')}")
    
    # Test validation
    errors = config.validate_config()
    if errors:
        print("Validation errors:", errors)
    else:
        print("Configuration is valid")
        
    # Test setting values
    config.set('school_name', 'Test School')
    print(f"Updated school name: {config.get('school_name')}")
    
    # Save configuration
    config.save_config()
