# Troubleshooting Guide
## The IMAGE JAIL PHOTOBOOTH

This guide helps diagnose and resolve common issues with The Slammer photo booth system.

## Quick Diagnostic Checklist

### Before Event (System Check)
- [ ] Power: All equipment has stable power supply
- [ ] Connections: All cables secure and functional
- [ ] Software: Application launches without errors
- [ ] Camera: Live preview shows clear image
- [ ] Storage: Adequate disk space available
- [ ] Templates: All templates load correctly
- [ ] Output: Test photos save successfully

### During Event (Performance Check)
- [ ] Speed: Capture-to-save under 10 seconds
- [ ] Quality: Images are well-exposed and sharp
- [ ] Stability: No crashes or freezes
- [ ] Storage: Monitor remaining disk space
- [ ] Temperature: Equipment not overheating

## Common Issues and Solutions

### Camera Connection Issues

**Problem: "Camera: Disconnected" error**

*Symptoms:*
- Red camera status indicator
- No preview image
- Application shows camera connection error

*Solutions:*
1. **Check physical connections:**
   - Verify USB cable is firmly connected
   - Try different USB port (use USB 3.0 if available)
   - Check HDMI connections for capture cards
   - Ensure camera is powered on

2. **Restart sequence:**
   - Close The Slammer application
   - Turn camera off and on
   - Restart application
   - Check camera status

3. **Driver issues:**
   - Open Device Manager (Windows)
   - Look for camera under "Cameras" or "Imaging devices"
   - Update drivers if yellow warning appears
   - Uninstall and reinstall camera drivers

4. **Alternative cameras:**
   - Try built-in webcam as backup
   - Change `camera_index` in settings.json
   - Test with different camera if available

**Problem: Camera connects but poor image quality**

*Solutions:*
1. **Clean lens:** Use proper lens cleaning cloth
2. **Check focus:** Manually focus camera if needed
3. **Lighting:** Adjust booth lighting intensity
4. **Settings:** Review camera exposure settings
5. **Position:** Verify camera angle and distance

### Software Issues

**Problem: Application won't start**

*Error messages to look for:*
```
ModuleNotFoundError: No module named 'cv2'
ImportError: No module named 'PIL'
```

*Solutions:*
1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Python path issues:**
   - Verify Python 3.8+ is installed
   - Check that pip installed packages correctly
   - Try running from command line to see full error

3. **Permission issues:**
   - Run as administrator (Windows)
   - Check file permissions
   - Verify write access to output directory

**Problem: Application crashes during operation**

*Solutions:*
1. **Memory issues:**
   - Close other applications
   - Check available RAM
   - Restart computer if needed

2. **Storage full:**
   - Check disk space
   - Clean temporary files
   - Use different output directory

3. **Check logs:**
   - Look for error messages in console
   - Enable debug mode in settings
   - Check system event logs

### Image Processing Issues

**Problem: Photos not saving**

*Symptoms:*
- Capture appears to work but no file created
- Error message about file permissions
- Images save to wrong location

*Solutions:*
1. **Check output directory:**
   - Verify directory exists
   - Check write permissions
   - Try different output location

2. **File naming conflicts:**
   - Check for duplicate filenames
   - Verify timestamp generation
   - Clear output directory if needed

3. **Disk space:**
   - Ensure adequate free space (>1GB recommended)
   - Monitor space during event
   - Set up automatic cleanup if needed

**Problem: Template overlay not working**

*Solutions:*
1. **Template files:**
   - Verify template JSON files exist
   - Check file format and syntax
   - Reset to default template

2. **Configuration:**
   - Check school name and event details
   - Verify template directory path
   - Reload templates in application

### Performance Issues

**Problem: Slow capture (>10 seconds)**

*Causes and solutions:*
1. **Computer performance:**
   - Close unnecessary applications
   - Check CPU and memory usage
   - Disable antivirus real-time scanning temporarily
   - Use Task Manager to identify resource hogs

2. **USB bandwidth:**
   - Use USB 3.0 ports for camera
   - Avoid USB hubs if possible
   - Disconnect other USB devices

3. **Image processing:**
   - Reduce image quality setting
   - Disable denoising if enabled
   - Lower capture resolution

**Problem: Preview lag or stuttering**

*Solutions:*
1. **Reduce preview quality:**
   - Lower preview resolution in settings
   - Decrease preview frame rate
   - Use smaller preview window

2. **Graphics performance:**
   - Update graphics drivers
   - Close other graphics-intensive applications
   - Use integrated graphics if dedicated GPU is having issues

### Hardware-Specific Issues

**Problem: DSLR camera not recognized**

*For Canon cameras:*
1. Install Canon EOS Utility software
2. Set camera to "PC Connect" mode
3. Verify USB cable supports data transfer
4. Try different USB ports

*For Sony cameras:*
1. Install Sony Imaging Edge software
2. Enable "PC Remote" mode on camera
3. Check USB connection type (some require specific cables)
4. Update camera firmware if needed

**Problem: HDMI capture card issues**

*Solutions:*
1. **Driver installation:**
   - Install capture card drivers
   - Verify device appears in Device Manager
   - Try different USB 3.0 port

2. **HDMI signal:**
   - Check HDMI cable quality
   - Verify camera HDMI output is enabled
   - Try different HDMI resolution on camera

3. **Compatibility:**
   - Ensure capture card supports camera's HDMI format
   - Check refresh rate compatibility
   - Try different HDMI cable

### Event-Day Emergency Procedures

**Total System Failure:**

*Backup Plan 1: Smartphone Backup*
1. Use high-quality smartphone camera
2. Create manual template in PowerPoint/Google Slides
3. Take photos and add to template later
4. Maintain same props and positioning

*Backup Plan 2: Manual Operation*
1. Use any available camera
2. Save images without template processing
3. Apply templates later using image editing software
4. Document participant names for proper attribution

**Partial System Issues:**

*Camera works, software fails:*
1. Use camera's built-in timer function
2. Save images to camera memory card
3. Process with templates after event

*Software works, camera fails:*
1. Switch to backup camera immediately
2. Adjust settings for new camera
3. Continue with lower quality if necessary

## Preventive Maintenance

### Daily Checks
- Clean camera lens before each event
- Check all cable connections
- Verify adequate storage space
- Test capture functionality
- Update system clock for accurate timestamps

### Weekly Maintenance
- Update camera drivers
- Clear temporary files
- Check for software updates
- Test backup equipment
- Review event logs for patterns

### Monthly Tasks
- Full equipment inspection
- Clean computer internals if needed
- Update operating system
- Backup configuration files
- Review and update documentation

## Diagnostic Tools

### Built-in Diagnostics

*System Information:*
- Check camera info in application
- Review configuration validation
- Monitor performance counters

*Log Files:*
- Enable debug logging
- Check console output for errors
- Review system event logs

### External Tools

*Windows:*
- Device Manager for hardware issues
- Task Manager for performance monitoring
- Event Viewer for system errors

*Camera Testing:*
- Windows Camera app
- OBS Studio for capture card testing
- Manufacturer's camera software

### Contact Information

**Technical Support:**
- Email: [support@yourorganization.com]
- Phone: [your phone number]
- Hours: [support hours]

**Emergency Contacts:**
- Event Coordinator: [contact info]
- IT Support: [contact info]
- Backup Technical Person: [contact info]

**Documentation:**
- Setup Guide: `docs/hardware_setup.md`
- Operator Manual: `docs/operator_manual.md`
- Configuration Guide: `docs/configuration.md`

## Frequently Asked Questions

**Q: Can I use a regular webcam instead of a DSLR?**
A: Yes, but image quality will be lower. USB webcams work fine for casual events.

**Q: How much disk space do I need?**
A: Plan for 2-5MB per photo. For 500 photos, allocate at least 5GB of free space.

**Q: Can I run this on a Mac?**
A: Yes, the software is cross-platform. Install Python and the required packages.

**Q: What if participants don't like their photo?**
A: The system allows immediate retakes. Just click capture again.

**Q: Can I customize the mugshot templates?**
A: Yes, see the Configuration Guide for details on creating custom templates.

**Q: How do I transfer photos after the event?**
A: Copy the entire output folder to a USB drive or cloud storage.

Remember: When troubleshooting during an event, prioritize getting the system working quickly over perfect image quality. You can always improve settings between events.
