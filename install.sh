#!/bin/bash

# Check if running with sudo
if [ "$EUID" -ne 0 ]
  then echo "Please run with sudo"
  exit
fi

# Install required packages
apt-get update
apt-get install -y python3-pip python3-tk=3.10.6-7

# Install Python dependencies
pip3 install -r requirements.txt

# Build the application
pyinstaller autoclicker.spec

# Copy the executable to /usr/local/bin
cp dist/autoclicker /usr/local/bin/
chmod +x /usr/local/bin/autoclicker

# Install desktop entry
cp autoclicker.desktop /usr/share/applications/

echo "Installation complete! You can now find AutoClicker in your applications menu or run it from terminal with 'autoclicker'" 