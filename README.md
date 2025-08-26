# The Slammer: Automated Mugshot Photo Booth

An interactive photo booth that simulates a classic police mugshot experience. Participants step into the themed booth, have their picture taken, and receive a digitally processed photo automatically placed into a branded template.

## Project Overview

**The Slammer** is designed for events like school functions, parties, or fundraisers where participants can create fun, professional-looking "mugshot" photos with custom branding and fake charges.

## Key Features

- **Professional Image Capture**: Supports DSLR/mirrorless cameras (Sony a6400, Canon 90D)
- **Live Preview**: Real-time camera feed for perfect positioning
- **Automated Processing**: One-click capture, template overlay, and saving
- **Customizable Templates**: Easy branding with school logos, event names, fake charges
- **Operator Friendly**: Simple interface requiring minimal training
- **Fast Processing**: Under 10 seconds from capture to saved image

## Quick Start

1. **Hardware Setup**: Connect camera, lighting, and display
2. **Install Dependencies**: `pip install -r requirements.txt`
3. **Configure Settings**: Edit `config/settings.json`
4. **Run Application**: `python src/main.py`

## Project Structure

```
JAIL_BOOTH/
├── src/                    # Source code
├── templates/              # Mugshot templates
├── output/                 # Generated photos
├── config/                 # Configuration files
├── docs/                   # Documentation
├── tests/                  # Test scripts
├── assets/                 # Images, fonts, etc.
└── requirements.txt        # Python dependencies
```

## Hardware Requirements

- DSLR/Mirrorless Camera (Sony a6400, Canon 90D, etc.)
- USB HDMI Capture Card
- Laptop/Computer (Windows/Mac/Linux)
- Tripod and Lighting Equipment
- HDMI Cables and Power Supplies

## Software Requirements

- Python 3.8+
- OpenCV
- Pillow (PIL)
- Tkinter (usually included with Python)
- Camera-specific drivers

## Documentation

- [Hardware Setup Guide](docs/hardware_setup.md)
- [Operator Manual](docs/operator_manual.md)
- [Configuration Guide](docs/configuration.md)
- [Troubleshooting](docs/troubleshooting.md)

## Success Criteria

- ✅ **Reliability**: Runs without crashing for 2-3 hours
- ✅ **Speed**: Under 10 seconds per photo
- ✅ **Usability**: 5-minute volunteer training
- ✅ **Quality**: Professional, well-aligned photos

## License

This project is designed for educational and event use. Please respect camera manufacturer guidelines and participant privacy.
