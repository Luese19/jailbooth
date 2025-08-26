# Installation Guide
## The Slammer: Automated Mugshot Photo Booth

This guide covers the complete installation and setup process for The Slammer photo booth system.

## System Requirements

### Minimum Requirements
- **Operating System**: Windows 10, macOS 10.14, or Linux (Ubuntu 18.04+)
- **Processor**: Intel i5 or AMD equivalent (2.5GHz+)
- **Memory**: 8GB RAM
- **Storage**: 10GB free space (more for event photos)
- **USB**: 2+ USB 3.0 ports
- **Display**: 1920x1080 resolution

### Recommended Requirements
- **Processor**: Intel i7 or AMD equivalent (3.0GHz+)
- **Memory**: 16GB RAM
- **Storage**: SSD with 50GB+ free space
- **Graphics**: Dedicated graphics card
- **USB**: 4+ USB 3.0 ports
- **Display**: 4K resolution or dual monitors

## Software Installation

### Step 1: Install Python

**Windows:**
1. Download Python 3.8+ from [python.org](https://python.org)
2. Run installer and check "Add Python to PATH"
3. Select "Install for all users"
4. Verify installation: Open Command Prompt, type `python --version`

**macOS:**
1. Install Homebrew: `/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"`
2. Install Python: `brew install python3`
3. Verify installation: `python3 --version`

**Linux (Ubuntu/Debian):**
```bash
sudo apt update
sudo apt install python3 python3-pip python3-venv
```

### Step 2: Download The Slammer

**Option A: Download ZIP**
1. Download the project ZIP file
2. Extract to desired location (e.g., `C:\JAIL_BOOTH` or `~/JAIL_BOOTH`)

**Option B: Git Clone**
```bash
git clone [repository-url] JAIL_BOOTH
cd JAIL_BOOTH
```

### Step 3: Automatic Installation

**Windows:**
1. Open File Explorer and navigate to the JAIL_BOOTH folder
2. Double-click `start.bat`
3. Follow the prompts

**macOS/Linux:**
1. Open Terminal and navigate to the JAIL_BOOTH folder
2. Make script executable: `chmod +x start.sh`
3. Run: `./start.sh`

### Step 4: Manual Installation (if automatic fails)

1. **Open terminal/command prompt in project directory**

2. **Create virtual environment:**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Test installation:**
   ```bash
   python tests/quick_test.py
   ```

5. **Run application:**
   ```bash
   python src/main.py
   ```

## Hardware Setup

### Camera Setup

**For DSLR/Mirrorless Cameras:**
1. Install camera manufacturer software:
   - Canon: EOS Utility
   - Sony: Imaging Edge
   - Nikon: Camera Control Pro
2. Connect camera via USB cable
3. Set camera to appropriate mode (PC Connect/Tethering)

**For HDMI Capture:**
1. Install capture card drivers (if required)
2. Connect camera HDMI output to capture card
3. Connect capture card to computer via USB 3.0
4. Test in OBS or Windows Camera app

**For USB Webcams:**
1. Connect webcam to USB 3.0 port
2. Install drivers if prompted
3. Test in Windows Camera app or equivalent

### Initial Configuration

1. **Launch The Slammer application**
2. **Check camera connection** (should show green status)
3. **Configure basic settings:**
   - Click "Settings" button
   - Enter school name and event details
   - Select appropriate template
   - Set output directory
4. **Test capture functionality** with volunteer

## Troubleshooting Installation

### Python Issues

**"Python not found" error:**
- Ensure Python is in system PATH
- Try `python3` instead of `python`
- Reinstall Python with "Add to PATH" checked

**Permission errors:**
- Run as administrator (Windows)
- Use `sudo` for package installation (Linux)
- Check file permissions

### Dependency Issues

**OpenCV installation fails:**
```bash
# Try alternative installation
pip install opencv-python-headless
```

**Pillow installation fails:**
```bash
# Install system dependencies first (Linux)
sudo apt install libjpeg-dev zlib1g-dev
pip install Pillow
```

**Missing tkinter:**
```bash
# Linux only
sudo apt install python3-tk
```

### Camera Issues

**Camera not detected:**
1. Check USB connections
2. Try different USB ports
3. Install camera drivers
4. Test with other camera software
5. Check Device Manager (Windows)

**Poor performance:**
1. Use USB 3.0 ports
2. Close other applications
3. Update graphics drivers
4. Lower camera resolution

## Network Installation (Multiple Computers)

### Shared Configuration

1. **Install on primary computer** following standard process
2. **Share configuration files:**
   - Copy `config/settings.json` to other computers
   - Share template files if customized
3. **Create network output folder** for centralized photo storage

### Event-Specific Setup

1. **Pre-event preparation:**
   - Test all computers with same configuration
   - Ensure network connectivity for shared storage
   - Prepare backup configurations

2. **Day-of-event:**
   - Start all computers from shared configuration
   - Monitor shared storage space
   - Have local backup storage ready

## Security Considerations

### Data Protection
- Use dedicated computer for photo booth
- Disable unnecessary network services
- Use local storage for sensitive events
- Plan for secure photo transfer

### Privacy Compliance
- Inform participants about photo usage
- Implement photo deletion procedures
- Follow institutional privacy policies
- Consider parental consent for minors

## Performance Optimization

### Hardware Optimization
- Use SSD storage for faster saves
- Ensure adequate cooling for extended operation
- Use dedicated graphics for better performance
- Connect cameras to fastest USB ports

### Software Optimization
- Close unnecessary applications
- Disable automatic updates during events
- Use performance power plan
- Monitor system resources

## Backup and Recovery

### Pre-Event Backup
- Copy entire JAIL_BOOTH folder to external drive
- Test backup on different computer
- Document hardware serial numbers
- Prepare emergency contact list

### During Event
- Monitor storage space regularly
- Create periodic photo backups
- Keep spare equipment ready
- Document any issues for later review

## Update and Maintenance

### Regular Updates
- Check for software updates monthly
- Update camera drivers as needed
- Review configuration files
- Test system after updates

### Seasonal Maintenance
- Clean equipment thoroughly
- Update event-specific configurations
- Review and update documentation
- Train new operators

## Support Resources

### Documentation
- Hardware Setup Guide: `docs/hardware_setup.md`
- Operator Manual: `docs/operator_manual.md`
- Configuration Guide: `docs/configuration.md`
- Troubleshooting Guide: `docs/troubleshooting.md`

### Testing Tools
- Quick Test: `python tests/quick_test.py`
- Full System Test: `python tests/system_test.py`
- Performance Benchmark: Run system test with benchmarks

### Contact Information
- Technical Support: [your-support-email]
- Documentation: Available in `docs/` folder
- Issue Tracking: [if using issue tracker]

## Post-Installation Checklist

- [ ] Python 3.8+ installed and working
- [ ] All dependencies installed successfully
- [ ] Camera detected and functional
- [ ] Templates loading correctly
- [ ] Output directory writable
- [ ] Test photos capture and save
- [ ] Performance meets requirements (<10s capture-to-save)
- [ ] Documentation reviewed
- [ ] Operator training completed
- [ ] Backup procedures tested

**Congratulations!** Your Slammer photo booth system is ready for deployment. Remember to test thoroughly before each event and have backup plans ready.
