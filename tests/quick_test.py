"""
Quick Test Script
Simple test to verify basic functionality before an event.
"""

import sys
import os
import time
from pathlib import Path

# Add src directory to path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_imports():
    """Test that all required modules can be imported."""
    print("Testing imports...")
    
    try:
        import cv2
        print("✓ OpenCV imported")
    except ImportError:
        print("✗ OpenCV not available - install with: pip install opencv-python")
        return False
        
    try:
        from PIL import Image
        print("✓ Pillow imported")
    except ImportError:
        print("✗ Pillow not available - install with: pip install Pillow")
        return False
        
    try:
        import numpy as np
        print("✓ NumPy imported")
    except ImportError:
        print("✗ NumPy not available - install with: pip install numpy")
        return False
        
    try:
        import tkinter as tk
        print("✓ Tkinter imported")
    except ImportError:
        print("✗ Tkinter not available - usually included with Python")
        return False
        
    return True

def test_application_modules():
    """Test that application modules can be imported."""
    print("\nTesting application modules...")
    
    try:
        from config_manager import ConfigManager
        print("✓ ConfigManager imported")
    except ImportError as e:
        print(f"✗ ConfigManager import failed: {e}")
        return False
        
    try:
        from camera_manager import CameraManager
        print("✓ CameraManager imported")
    except ImportError as e:
        print(f"✗ CameraManager import failed: {e}")
        return False
        
    try:
        from template_processor import TemplateProcessor
        print("✓ TemplateProcessor imported")
    except ImportError as e:
        print(f"✗ TemplateProcessor import failed: {e}")
        return False
        
    try:
        from image_processor import ImageProcessor
        print("✓ ImageProcessor imported")
    except ImportError as e:
        print(f"✗ ImageProcessor import failed: {e}")
        return False
        
    return True

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        from config_manager import ConfigManager
        config = ConfigManager()
        
        # Test basic settings
        camera_index = config.get('camera_index')
        school_name = config.get('school_name')
        output_dir = config.get('output_directory')
        
        print(f"✓ Camera index: {camera_index}")
        print(f"✓ School name: {school_name}")
        print(f"✓ Output directory: {output_dir}")
        
        # Test validation
        errors = config.validate_config()
        if errors:
            print("⚠ Configuration warnings:")
            for key, error in errors.items():
                print(f"  - {key}: {error}")
        else:
            print("✓ Configuration validation passed")
            
        return True
        
    except Exception as e:
        print(f"✗ Configuration test failed: {e}")
        return False

def test_directories():
    """Test that required directories exist."""
    print("\nTesting directory structure...")
    
    project_root = Path(__file__).parent.parent
    required_dirs = ['src', 'templates', 'config', 'output']
    
    all_exist = True
    for dir_name in required_dirs:
        dir_path = project_root / dir_name
        if dir_path.exists():
            print(f"✓ {dir_name}/ directory exists")
        else:
            print(f"✗ {dir_name}/ directory missing")
            all_exist = False
            
    return all_exist

def test_camera_detection():
    """Test camera detection."""
    print("\nTesting camera detection...")
    
    try:
        from camera_manager import CameraManager
        from config_manager import ConfigManager
        
        config = ConfigManager()
        camera_manager = CameraManager(config)
        
        if camera_manager.initialize():
            print("✓ Camera detected and initialized")
            
            # Get camera info
            info = camera_manager.get_camera_info()
            print(f"✓ Camera type: {info.get('type', 'Unknown')}")
            
            # Test frame capture
            frame = camera_manager.get_frame()
            if frame is not None:
                print(f"✓ Frame captured: {frame.shape}")
            else:
                print("⚠ Frame capture returned None")
                
            camera_manager.cleanup()
            return True
        else:
            print("⚠ No camera detected (this is normal if no camera is connected)")
            return False
            
    except Exception as e:
        print(f"✗ Camera test failed: {e}")
        return False

def test_templates():
    """Test template loading."""
    print("\nTesting templates...")
    
    try:
        from template_processor import TemplateProcessor
        from config_manager import ConfigManager
        
        config = ConfigManager()
        processor = TemplateProcessor(config)
        
        templates = processor.get_available_templates()
        
        if templates:
            print(f"✓ {len(templates)} templates loaded:")
            for name, description in templates.items():
                print(f"  - {name}: {description}")
        else:
            print("⚠ No templates found")
            
        return len(templates) > 0
        
    except Exception as e:
        print(f"✗ Template test failed: {e}")
        return False

def test_output_directory():
    """Test output directory access."""
    print("\nTesting output directory...")
    
    try:
        from config_manager import ConfigManager
        from image_processor import ImageProcessor
        import numpy as np
        
        config = ConfigManager()
        processor = ImageProcessor()
        
        output_dir = Path(config.get('output_directory', 'output'))
        
        # Create output directory if it doesn't exist
        output_dir.mkdir(exist_ok=True)
        print(f"✓ Output directory: {output_dir}")
        
        # Test write access
        test_image = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
        test_file = output_dir / "write_test.jpg"
        
        if processor.save_image(test_image, str(test_file)):
            print("✓ Write access confirmed")
            
            # Clean up test file
            if test_file.exists():
                test_file.unlink()
                
            return True
        else:
            print("✗ Cannot write to output directory")
            return False
            
    except Exception as e:
        print(f"✗ Output directory test failed: {e}")
        return False

def main():
    """Run quick tests."""
    print("The Slammer Photo Booth - Quick Test")
    print("="*40)
    
    tests = [
        ("Imports", test_imports),
        ("Application Modules", test_application_modules),
        ("Configuration", test_configuration),
        ("Directories", test_directories),
        ("Templates", test_templates),
        ("Output Directory", test_output_directory),
        ("Camera Detection", test_camera_detection),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n--- {test_name} ---")
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
    
    print("\n" + "="*40)
    print(f"RESULTS: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! System is ready for use.")
    elif passed >= total - 1:
        print("⚠ Almost ready - check any warnings above.")
    else:
        print("❌ System needs attention - check failed tests.")
        
    print("\nNext steps:")
    if passed == total:
        print("1. Run the main application: python src/main.py")
        print("2. Test with a volunteer before the event")
    else:
        print("1. Fix any failed tests")
        print("2. Install missing dependencies")
        print("3. Check hardware connections")
        
    return passed == total

if __name__ == "__main__":
    main()
