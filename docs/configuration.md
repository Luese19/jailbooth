# Configuration Guide
## The IMAGE JAIL PHOTOBOOTH

This guide explains how to configure The Slammer photo booth system for your specific event and hardware setup.

## Configuration File Location

The main configuration file is located at:
```
JAIL_BOOTH/config/settings.json
```

## Basic Configuration

### School and Event Information

Update these settings to customize your photo booth:

```json
{
    "school_name": "Your School Name",
    "event_name": "Spring Carnival Photo Booth",
    "event_date": "2025-08-24"
}
```

These values appear in the mugshot templates automatically.

### Camera Settings

```json
{
    "camera_index": 0,
    "camera_resolution": [1920, 1080],
    "camera_fps": 30,
    "image_contrast": 1.1,
    "image_brightness": 10,
    "apply_denoising": true
}
```

**Configuration Options:**
- `camera_index`: Which camera to use (0 = first camera, 1 = second, etc.)
- `camera_resolution`: [width, height] in pixels
- `camera_fps`: Frames per second for preview
- `image_contrast`: 1.0 = normal, >1.0 = more contrast
- `image_brightness`: 0 = normal, positive = brighter
- `apply_denoising`: true/false - reduces image noise

### Output Settings

```json
{
    "output_directory": "output",
    "image_format": "jpg",
    "image_quality": 95,
    "filename_prefix": "Mugshot",
    "include_timestamp": true
}
```

**File Naming:**
- Format: `{prefix}_{date}_{time}_{counter}.{format}`
- Example: `Mugshot_20250824_143052_001.jpg`

### Template Settings

```json
{
    "default_template": "school",
    "template_directory": "templates"
}
```

Available templates: `default`, `school`, `party`, `custom`

## Advanced Configuration

### Display Settings

```json
{
    "fullscreen_mode": false,
    "preview_size": [640, 480],
    "ui_theme": "dark"
}
```

### Booth Behavior

```json
{
    "capture_countdown": 3,
    "auto_save": true,
    "show_last_photo": true,
    "enable_sound": false
}
```

### Hardware Integration

```json
{
    "use_external_trigger": false,
    "trigger_pin": null,
    "flash_enabled": false
}
```

For external hardware triggers (buttons, sensors), contact technical support.

### Debug and Logging

```json
{
    "debug_mode": false,
    "log_level": "INFO",
    "max_retries": 3,
    "timeout_seconds": 30
}
```

Set `debug_mode` to `true` for troubleshooting.

## Template Customization

### Creating Custom Templates

1. Copy an existing template file from `templates/` folder
2. Rename it (e.g., `custom.json`)
3. Edit the template configuration:

```json
{
    "name": "Custom Template",
    "description": "My custom mugshot template",
    "image_position": {
        "x": 100,
        "y": 150,
        "width": 400,
        "height": 500
    },
    "background": {
        "color": [240, 240, 240],
        "image": null
    },
    "text_elements": [
        {
            "type": "title",
            "text": "MY CUSTOM TITLE",
            "position": [300, 50],
            "font_size": 36,
            "color": [0, 0, 0],
            "font_weight": "bold"
        }
    ],
    "final_size": [600, 850]
}
```

### Template Elements

**Image Position:**
- `x`, `y`: Top-left corner of photo area
- `width`, `height`: Size of photo area

**Text Elements:**
- `text`: Text to display (use `{school_name}`, `{event_name}`, `{event_date}` for variables)
- `position`: [x, y] coordinates
- `font_size`: Size in pixels
- `color`: [R, G, B] color values (0-255)

**Background:**
- `color`: [R, G, B] background color
- `image`: Optional background image file

## Camera-Specific Settings

### DSLR Cameras (via HDMI Capture)

```json
{
    "camera_index": 0,
    "camera_resolution": [1920, 1080],
    "camera_fps": 30
}
```

Ensure your HDMI capture card appears as camera index 0.

### USB Webcams

```json
{
    "camera_index": 0,
    "camera_resolution": [1280, 720],
    "camera_fps": 30
}
```

Lower resolution may be needed for USB bandwidth.

### Multiple Cameras

To use backup cameras:

```json
{
    "camera_index": 1,
    "backup_cameras": [0, 2, 3]
}
```

System will try backup cameras if primary fails.

## Performance Optimization

### For Slower Computers

```json
{
    "camera_resolution": [1280, 720],
    "camera_fps": 15,
    "preview_size": [480, 360],
    "apply_denoising": false
}
```

### For High-Performance Setup

```json
{
    "camera_resolution": [1920, 1080],
    "camera_fps": 60,
    "preview_size": [800, 600],
    "image_quality": 100
}
```

## Validation and Testing

### Configuration Validation

The system automatically validates settings on startup. Common issues:

**Invalid camera_index:**
```
Error: camera_index must be 0 or higher
```

**Invalid resolution:**
```
Error: camera_resolution must be [width, height]
```

**Missing directories:**
```
Error: template_directory does not exist
```

### Test Configuration

1. Save your configuration file
2. Restart The Slammer application
3. Check status messages for errors
4. Test camera connection and preview
5. Capture test images to verify settings

## Environment-Specific Configurations

### School Events

```json
{
    "school_name": "Lincoln High School",
    "event_name": "Homecoming Dance",
    "default_template": "school",
    "enable_sound": false,
    "capture_countdown": 3
}
```

### Party Events

```json
{
    "school_name": "Birthday Party",
    "event_name": "Sarah's Sweet 16",
    "default_template": "party",
    "enable_sound": true,
    "capture_countdown": 5
}
```

### Professional Events

```json
{
    "school_name": "Corporate Event",
    "event_name": "Annual Conference",
    "default_template": "default",
    "image_quality": 100,
    "capture_countdown": 0
}
```

## Backup and Recovery

### Backing Up Configuration

1. Copy `config/settings.json` to safe location
2. Copy entire `templates/` folder
3. Note any custom modifications

### Restoring Configuration

1. Replace `config/settings.json` with backup
2. Restart application
3. Verify all settings loaded correctly

### Factory Reset

1. Delete `config/settings.json`
2. Restart application
3. Default configuration will be created
4. Reconfigure for your event

## Troubleshooting Configuration Issues

### Configuration Not Loading
- Check file syntax (valid JSON)
- Verify file permissions
- Check for typos in settings names

### Settings Not Taking Effect
- Restart application after changes
- Check for validation errors in status bar
- Verify configuration file location

### Template Not Found
- Check template file exists in templates folder
- Verify template name matches file name
- Check template file format (JSON)

For advanced configuration needs or custom integrations, contact technical support.
