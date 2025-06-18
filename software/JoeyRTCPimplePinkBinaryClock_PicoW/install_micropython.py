#!/usr/bin/env python3
"""
MicroPython Installation Script for Pimple Pink Binary Clock
This script helps install MicroPython firmware and upload files to Pico W
"""

import os
import sys
import subprocess
import urllib.request
import shutil
from pathlib import Path

# MicroPython firmware URL for Pico W
MICROPYTHON_URL = "https://micropython.org/resources/firmware/RPI_PICO_W-20250415-v1.25.0.uf2"
FIRMWARE_FILE = "micropython-firmware-pico-w-290622.uf2"

def check_dependencies():
    """Check if required tools are installed"""
    print("Checking dependencies...")
    
    # Check for Python
    try:
        import serial
        print("✅ pyserial found")
    except ImportError:
        print("❌ pyserial not found. Install with: pip install pyserial")
        return False
    
    # Check for ampy (for file upload)
    try:
        result = subprocess.run(['ampy', '--help'], capture_output=True, text=True)
        print("✅ ampy found")
    except FileNotFoundError:
        print("❌ ampy not found. Install with: pip install adafruit-ampy")
        return False
    
    return True

def download_firmware():
    """Download MicroPython firmware"""
    if os.path.exists(FIRMWARE_FILE):
        print(f"✅ {FIRMWARE_FILE} already exists")
        return True
    
    print(f"Downloading MicroPython firmware from {MICROPYTHON_URL}")
    try:
        urllib.request.urlretrieve(MICROPYTHON_URL, FIRMWARE_FILE)
        print(f"✅ Downloaded {FIRMWARE_FILE}")
        return True
    except Exception as e:
        print(f"❌ Failed to download firmware: {e}")
        return False

def find_pico_drive():
    """Find the Pico drive when in BOOTSEL mode"""
    possible_paths = [
        "/Volumes/RPI-RP2",  # macOS
        "/media/*/RPI-RP2",  # Linux
        "D:\\",              # Windows (common)
        "E:\\",              # Windows (alternative)
        "F:\\",              # Windows (alternative)
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def flash_firmware():
    """Flash MicroPython firmware to Pico W"""
    print("\n🔧 Flashing MicroPython firmware...")
    print("1. Hold the BOOTSEL button on your Pico W")
    print("2. Connect the Pico W to your computer via USB")
    print("3. Release the BOOTSEL button")
    print("4. The Pico should appear as a USB drive named 'RPI-RP2'")
    
    input("Press Enter when the Pico W is connected in BOOTSEL mode...")
    
    pico_drive = find_pico_drive()
    if not pico_drive:
        print("❌ Cannot find Pico drive. Make sure it's connected in BOOTSEL mode.")
        return False
    
    print(f"Found Pico drive at: {pico_drive}")
    
    try:
        firmware_dest = os.path.join(pico_drive, FIRMWARE_FILE)
        shutil.copy2(FIRMWARE_FILE, firmware_dest)
        print("✅ Firmware copied to Pico W")
        print("The Pico W should automatically reboot with MicroPython")
        return True
    except Exception as e:
        print(f"❌ Failed to copy firmware: {e}")
        return False

def find_serial_port():
    """Find the serial port for the Pico W"""
    import serial.tools.list_ports
    
    ports = serial.tools.list_ports.comports()
    for port in ports:
        if "Pico" in port.description or "USB Serial" in port.description:
            return port.device
    
    # If no specific match, show all ports
    print("Available serial ports:")
    for i, port in enumerate(ports):
        print(f"{i}: {port.device} - {port.description}")
    
    if ports:
        try:
            choice = int(input("Select port number: "))
            return ports[choice].device
        except (ValueError, IndexError):
            print("Invalid selection")
    
    return None

def upload_files():
    """Upload Python files to Pico W"""
    print("\n📁 Uploading files to Pico W...")
    
    port = find_serial_port()
    if not port:
        print("❌ Cannot find Pico W serial port")
        return False
    
    print(f"Using serial port: {port}")
    
    files_to_upload = [
        "main.py",
        "config.py",
    ]
    
    for file in files_to_upload:
        if not os.path.exists(file):
            print(f"❌ File not found: {file}")
            continue
        
        try:
            cmd = ["ampy", "-p", port, "put", file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Uploaded {file}")
            else:
                print(f"❌ Failed to upload {file}: {result.stderr}")
        except Exception as e:
            print(f"❌ Error uploading {file}: {e}")
    
    return True

def setup_config():
    """Help user set up configuration"""
    print("\n⚙️  Configuration Setup")
    print("Edit config.py to set your WiFi credentials and preferences:")
    print("- WIFI_SSID: Your WiFi network name")
    print("- WIFI_PASSWORD: Your WiFi password")
    print("- TIMEZONE_OFFSET: Hours from UTC for your timezone")
    print("- NEOPIXEL_PIN: GPIO pin for NeoPixels (default: 16)")
    print("- NUM_PIXELS: Number of NeoPixels (default: 25 for 5x5 grid)")
    
    edit_now = input("Would you like to edit config.py now? (y/n): ").lower()
    if edit_now == 'y':
        # Try to open with default editor
        try:
            if sys.platform == "darwin":  # macOS
                subprocess.run(["open", "-t", "config.py"])
            elif sys.platform == "linux":  # Linux
                subprocess.run(["xdg-open", "config.py"])
            elif sys.platform == "win32":  # Windows
                subprocess.run(["notepad", "config.py"])
        except:
            print("Please manually edit config.py with your preferred text editor")

def main():
    """Main installation process"""
    print("🕐 Pimple Pink Binary Clock - MicroPython Setup")
    print("=" * 50)
    
    # Check dependencies
    if not check_dependencies():
        print("\n❌ Please install missing dependencies and try again")
        return
    
    # Download firmware
    if not download_firmware():
        return
    
    # Flash firmware
    if not flash_firmware():
        return
    
    print("\n⏳ Waiting for Pico W to reboot...")
    input("Press Enter when the Pico W has rebooted (LED should be solid/blinking)...")
    
    # Setup configuration
    setup_config()
    
    # Upload files
    if not upload_files():
        return
    
    print("\n🎉 Installation complete!")
    print("\nNext steps:")
    print("1. Edit config.py with your WiFi credentials")
    print("2. Connect your NeoPixel strip to pin 16 (or your configured pin)")
    print("3. Reset the Pico W to start the clock")
    print("4. Check the serial output for the IP address")
    print("5. Open the IP address in your web browser")
    
    print("\nTroubleshooting:")
    print("- If upload fails, try pressing Ctrl+C on the Pico W and retry")
    print("- Use Thonny IDE for easier file management and debugging")
    print("- Check serial output with: screen /dev/ttyACM0 115200 (Linux/macOS)")

if __name__ == "__main__":
    main() 