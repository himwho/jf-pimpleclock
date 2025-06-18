#!/usr/bin/env python3
"""
Simple script to check if Pico W is in bootloader mode
"""
import os
import sys
import time

def check_bootloader():
    """Check if RPI-RP2 drive is mounted (bootloader mode)"""
    # Common mount points for macOS
    mount_points = [
        '/Volumes/RPI-RP2',
        '/Volumes/RPI-RP2 1',  # Sometimes gets numbered
    ]
    
    for mount_point in mount_points:
        if os.path.exists(mount_point):
            print(f"✅ Found Pico W in bootloader mode at: {mount_point}")
            return True
    
    # Check if any RPI-RP2 volumes exist
    volumes_dir = '/Volumes'
    if os.path.exists(volumes_dir):
        for item in os.listdir(volumes_dir):
            if 'RPI-RP2' in item:
                print(f"✅ Found Pico W in bootloader mode at: /Volumes/{item}")
                return True
    
    print("❌ Pico W not found in bootloader mode")
    print("💡 Make sure to:")
    print("   1. Disconnect USB cable")
    print("   2. Hold BOOTSEL button")
    print("   3. Reconnect USB while holding BOOTSEL")
    print("   4. Release BOOTSEL button")
    return False

if __name__ == "__main__":
    print("🔍 Checking for Pico W in bootloader mode...")
    if check_bootloader():
        print("🎉 Ready for firmware flash!")
        print("💻 Run: make flash")
    else:
        print("⏳ Waiting for bootloader mode...")
        # Wait and check again
        for i in range(10):
            time.sleep(1)
            if check_bootloader():
                print("🎉 Ready for firmware flash!")
                print("💻 Run: make flash")
                sys.exit(0)
        print("⚠️  Still not in bootloader mode. Please try the manual reset again.") 