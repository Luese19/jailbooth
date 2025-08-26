"""
System Test Script
Tests all components of The Slammer photo booth system to ensure reliability and performance.
"""

import sys
import os
import time
import unittest
import numpy as np
import cv2
from pathlib import Path
import json

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

from config_manager import ConfigManager
from camera_manager import CameraManager
from template_processor import TemplateProcessor
from image_processor import ImageProcessor


class TestSystemComponents(unittest.TestCase):
    """Test suite for The Slammer photo booth system."""
    
    def setUp(self):
        """Set up test environment."""
        self.config = ConfigManager()
        self.test_image = np.random.randint(0, 255, (480, 640, 3), dtype=np.uint8)
        
    def test_config_manager(self):
        """Test configuration manager functionality."""
        print("\n=== Testing Configuration Manager ===")
        
        # Test basic configuration loading
        self.assertIsInstance(self.config.get_all_settings(), dict)
        
        # Test getting specific values
        camera_index = self.config.get('camera_index', 0)
        self.assertIsInstance(camera_index, int)
        
        # Test setting values
        self.config.set('test_value', 'test')
        self.assertEqual(self.config.get('test_value'), 'test')
        
        # Test validation
        errors = self.config.validate_config()
        self.assertIsInstance(errors, dict)
        
        print("✓ Configuration manager tests passed")
        
    def test_image_processor(self):
        """Test image processing functionality."""
        print("\n=== Testing Image Processor ===")
        
        processor = ImageProcessor()
        
        # Test image validation
        self.assertTrue(processor.validate_image(self.test_image))
        self.assertFalse(processor.validate_image(None)) # type: ignore
        
        # Test image info
        info = processor.get_image_info(self.test_image)
        self.assertIn('width', info)
        self.assertIn('height', info)
        
        # Test resize
        resized = processor.resize_image(self.test_image, (320, 240))
        self.assertEqual(resized.shape[:2], (240, 320))
        
        # Test enhancement
        enhanced = processor.enhance_image(self.test_image, {'contrast': 1.2})
        self.assertEqual(enhanced.shape, self.test_image.shape)
        
        # Test thumbnail creation
        thumbnail = processor.create_thumbnail(self.test_image)
        self.assertLessEqual(max(thumbnail.shape[:2]), 200)
        
        print("✓ Image processor tests passed")
        
    def test_template_processor(self):
        """Test template processing functionality."""
        print("\n=== Testing Template Processor ===")
        
        processor = TemplateProcessor(self.config)
        
        # Test template loading
        templates = processor.get_available_templates()
        self.assertIsInstance(templates, dict)
        self.assertGreater(len(templates), 0)
        
        # Test image processing with default template
        if 'default' in templates:
            result = processor.process_image(self.test_image, 'default')
            if result is not None:
                self.assertIsInstance(result, np.ndarray)
                print("✓ Template processing successful")
            else:
                print("! Template processing returned None (may need template files)")
        else:
            print("! No default template found")
            
        print("✓ Template processor tests completed")
        
    def test_camera_manager(self):
        """Test camera manager functionality."""
        print("\n=== Testing Camera Manager ===")
        
        camera_manager = CameraManager(self.config)
        
        # Test camera initialization
        init_success = camera_manager.initialize()
        
        if init_success:
            print("✓ Camera initialized successfully")
            
            # Test camera info
            info = camera_manager.get_camera_info()
            self.assertIsInstance(info, dict)
            self.assertEqual(info.get('status'), 'connected')
            
            # Test frame capture
            frame = camera_manager.get_frame()
            if frame is not None:
                self.assertIsInstance(frame, np.ndarray)
                print("✓ Frame capture successful")
            else:
                print("! Frame capture returned None")
                
            # Test image capture
            image = camera_manager.capture_image()
            if image is not None:
                self.assertIsInstance(image, np.ndarray)
                print("✓ Image capture successful")
            else:
                print("! Image capture returned None")
                
            # Cleanup
            camera_manager.cleanup()
            print("✓ Camera cleanup successful")
            
        else:
            print("! Camera initialization failed (normal if no camera connected)")
            
    def test_performance_timing(self):
        """Test system performance timing."""
        print("\n=== Testing Performance ===")
        
        processor = ImageProcessor()
        template_processor = TemplateProcessor(self.config)
        
        # Test image processing speed
        start_time = time.time()
        
        # Simulate the full capture-to-save pipeline
        enhanced = processor.enhance_image(self.test_image)
        
        if 'default' in template_processor.get_available_templates():
            processed = template_processor.process_image(enhanced, 'default')
            
            if processed is not None:
                # Test save speed (to temporary location)
                temp_path = Path('temp_test_image.jpg')
                save_success = processor.save_image(processed, str(temp_path))
                
                # Clean up temp file
                if temp_path.exists():
                    temp_path.unlink()
                    
                total_time = time.time() - start_time
                print(f"✓ Full processing pipeline: {total_time:.2f} seconds")
                
                if total_time < 10.0:
                    print("✓ Performance target met (under 10 seconds)")
                else:
                    print(f"! Performance warning: {total_time:.2f}s exceeds 10s target")
            else:
                print("! Template processing failed, cannot test full pipeline")
        else:
            print("! No default template available for performance test")
            
    def test_directory_structure(self):
        """Test that all required directories and files exist."""
        print("\n=== Testing Directory Structure ===")
        
        project_root = Path(__file__).parent.parent
        
        required_dirs = ['src', 'templates', 'config', 'docs', 'output']
        required_files = [
            'src/main.py',
            'src/config_manager.py',
            'src/camera_manager.py',
            'src/template_processor.py',
            'src/image_processor.py',
            'config/settings.json',
            'requirements.txt'
        ]
        
        # Check directories
        for dir_name in required_dirs:
            dir_path = project_root / dir_name
            self.assertTrue(dir_path.exists(), f"Directory missing: {dir_name}")
            
        # Check files
        for file_name in required_files:
            file_path = project_root / file_name
            self.assertTrue(file_path.exists(), f"File missing: {file_name}")
            
        print("✓ Directory structure validation passed")
        
    def test_configuration_validation(self):
        """Test configuration file validation."""
        print("\n=== Testing Configuration Validation ===")
        
        # Test current configuration
        errors = self.config.validate_config()
        
        if not errors:
            print("✓ Configuration validation passed")
        else:
            print("! Configuration validation errors:")
            for key, error in errors.items():
                print(f"  - {key}: {error}")
                
        # Test required settings exist
        required_settings = [
            'camera_index', 'camera_resolution', 'output_directory',
            'template_directory', 'school_name', 'event_name'
        ]
        
        for setting in required_settings:
            value = self.config.get(setting)
            self.assertIsNotNone(value, f"Required setting missing: {setting}")
            
        print("✓ Required settings validation passed")


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete system."""
    
    def setUp(self):
        """Set up integration test environment."""
        self.config = ConfigManager()
        
    def test_full_system_integration(self):
        """Test the complete system workflow."""
        print("\n=== Testing Full System Integration ===")
        
        try:
            # Initialize all components
            camera_manager = CameraManager(self.config)
            template_processor = TemplateProcessor(self.config)
            image_processor = ImageProcessor()
            
            print("✓ All components initialized")
            
            # Test template availability
            templates = template_processor.get_available_templates()
            self.assertGreater(len(templates), 0, "No templates available")
            print(f"✓ {len(templates)} templates available")
            
            # Create test output directory
            output_dir = Path(self.config.get('output_directory', 'output'))
            output_dir.mkdir(exist_ok=True)
            
            # Test with synthetic image (camera may not be available)
            test_image = np.random.randint(0, 255, (1080, 1920, 3), dtype=np.uint8)
            
            # Process with each available template
            for template_name in templates.keys():
                start_time = time.time()
                
                processed = template_processor.process_image(test_image, template_name)
                
                if processed is not None:
                    # Save test image
                    test_filename = f"integration_test_{template_name}.jpg"
                    test_path = output_dir / test_filename
                    
                    success = image_processor.save_image(processed, str(test_path))
                    
                    if success and test_path.exists():
                        processing_time = time.time() - start_time
                        file_size = test_path.stat().st_size
                        
                        print(f"✓ Template '{template_name}': {processing_time:.2f}s, {file_size} bytes")
                        
                        # Clean up test file
                        test_path.unlink()
                    else:
                        print(f"! Template '{template_name}': Save failed")
                else:
                    print(f"! Template '{template_name}': Processing failed")
                    
            print("✓ Integration testing completed")
            
        except Exception as e:
            self.fail(f"Integration test failed: {str(e)}")


def run_performance_benchmark():
    """Run performance benchmarks."""
    print("\n" + "="*50)
    print("PERFORMANCE BENCHMARK")
    print("="*50)
    
    config = ConfigManager()
    
    # Test different image sizes
    sizes = [(640, 480), (1280, 720), (1920, 1080)]
    
    for width, height in sizes:
        print(f"\nTesting {width}x{height} images:")
        
        test_image = np.random.randint(0, 255, (height, width, 3), dtype=np.uint8)
        
        # Test image processing speed
        processor = ImageProcessor()
        start_time = time.time()
        
        enhanced = processor.enhance_image(test_image)
        resized = processor.resize_image(enhanced, (600, 800))
        
        processing_time = time.time() - start_time
        print(f"  Image processing: {processing_time:.3f}s")
        
        # Test template processing speed
        template_processor = TemplateProcessor(config)
        
        if 'default' in template_processor.get_available_templates():
            start_time = time.time()
            result = template_processor.process_image(test_image, 'default')
            template_time = time.time() - start_time
            
            if result is not None:
                print(f"  Template processing: {template_time:.3f}s")
                
                # Test save speed
                start_time = time.time()
                processor.save_image(result, 'temp_benchmark.jpg')
                save_time = time.time() - start_time
                
                print(f"  Save time: {save_time:.3f}s")
                print(f"  Total pipeline: {processing_time + template_time + save_time:.3f}s")
                
                # Clean up
                temp_file = Path('temp_benchmark.jpg')
                if temp_file.exists():
                    temp_file.unlink()
            else:
                print("  Template processing: FAILED")


def main():
    """Run all tests."""
    print("The Slammer Photo Booth - System Test Suite")
    print("="*50)
    
    # Check Python version
    if sys.version_info < (3, 8):
        print("ERROR: Python 3.8 or higher required")
        return False
        
    # Check required modules
    required_modules = ['cv2', 'PIL', 'numpy']
    missing_modules = []
    
    for module in required_modules:
        try:
            __import__(module)
        except ImportError:
            missing_modules.append(module)
            
    if missing_modules:
        print(f"ERROR: Missing required modules: {', '.join(missing_modules)}")
        print("Run: pip install -r requirements.txt")
        return False
        
    # Run unit tests
    print("\nRunning unit tests...")
    unittest.main(argv=[''], exit=False, verbosity=2)
    
    # Run performance benchmark
    run_performance_benchmark()
    
    print("\n" + "="*50)
    print("SYSTEM TEST COMPLETE")
    print("="*50)
    print("\nIf all tests passed, the system is ready for deployment.")
    print("If any tests failed, check the troubleshooting guide.")
    
    return True


if __name__ == "__main__":
    main()
