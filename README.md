# AutoClicker

A simple GUI autoclicker application that allows you to record and playback mouse clicks with global keyboard shortcuts.

## Features
- Record mouse clicks with exact timing
- Playback recorded clicks with precise timing
- Global keyboard shortcuts (works even when window is not focused)
- Configurable playback interval in seconds
- System tray application with always-on-top window
- Cross-platform support (Windows/Linux)

## Requirements
- Python 3.10 or higher
- python3-tk 3.10.6-7
- X11 display server (Wayland is not supported)

## Installation

### Linux
1. Clone or download this repository
2. Make the install script executable:
```bash
chmod +x install.sh
```
3. Run the installation script with sudo:
```bash
sudo ./install.sh
```

This will:
- Install required dependencies
- Build the application
- Install it system-wide
- Create a desktop menu entry

After installation, you can:
- Launch AutoClicker from your applications menu
- Run it from terminal with command `autoclicker`

### Manual Installation
If you prefer to install dependencies manually:

1. Install required system packages:
```bash
sudo apt-get update
sudo apt-get install -y python3-pip python3-tk=3.10.6-7
```

2. Install Python dependencies:
```bash
pip3 install -r requirements.txt
```

3. Build the executable:
```bash
pyinstaller autoclicker.spec
```

## Usage
1. Launch the AutoClicker application
2. Use the following keyboard shortcuts:
   - F8: Start/Stop recording clicks
   - F9: Start/Stop playback
3. Set your desired playback interval in seconds
4. The window will stay on top for easy access

### Playback Interval
- Enter the interval in seconds between playback sequences
- Minimum interval is 0.1 seconds
- Default interval is 540 seconds (9 minutes)
- Changes take effect on the next playback cycle

## Notes
- The application requires X11 on Linux systems
- Global keyboard shortcuts work without root privileges
- Recorded clicks are stored in memory until the program is closed
- Each recorded sequence maintains the exact timing between clicks

## Troubleshooting

### Linux
If the global shortcuts don't work:
1. Make sure you're running X11 (not Wayland)
2. Check if python3-tk is installed with the correct version:
```bash
sudo apt-get install -y python3-tk=3.10.6-7
```
3. Verify you have necessary permissions for input devices

### Common Issues
- If the application doesn't appear in the menu after installation, try logging out and back in
- If keyboard shortcuts don't work, make sure no other application is using F8/F9
- If you get tkinter errors, make sure you have the correct python3-tk version installed 