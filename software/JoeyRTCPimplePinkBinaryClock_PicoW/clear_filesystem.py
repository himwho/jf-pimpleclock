#!/usr/bin/env python3
"""
Script to clear the problematic main.py file from Pico W
"""
import serial
import time
import sys

def clear_main_py(port='/dev/tty.usbmodem101', baud=115200):
    """Try to interrupt running program and remove main.py"""
    try:
        print("🔧 Connecting to Pico W...")
        s = serial.Serial(port, baud, timeout=2)
        
        print("⏹️  Sending interrupt signals...")
        # Send multiple interrupt signals to break out of running program
        for i in range(15):
            s.write(b'\x03')  # Ctrl+C
            time.sleep(0.1)
        
        print("🔄 Attempting soft reset...")
        s.write(b'\x04')  # Ctrl+D (soft reset)
        time.sleep(2)
        
        print("💻 Trying to enter raw REPL...")
        s.write(b'\x01')  # Ctrl+A (raw REPL)
        time.sleep(1)
        
        # Clear any pending data
        s.read(s.in_waiting or 0)
        
        print("🗑️  Attempting to remove main.py...")
        commands = [
            b'import os\r\n',
            b'try:\r\n',
            b'    os.remove("main.py")\r\n',
            b'    print("main.py removed")\r\n',
            b'except:\r\n',
            b'    print("main.py not found or could not remove")\r\n',
            b'\r\n'
        ]
        
        for cmd in commands:
            s.write(cmd)
            time.sleep(0.2)
        
        time.sleep(2)
        response = s.read(s.in_waiting or 0)
        print("📄 Response:", repr(response))
        
        # Try to get to normal REPL
        s.write(b'\x02')  # Ctrl+B (exit raw REPL)
        time.sleep(1)
        
        s.close()
        print("✅ Filesystem clear attempt completed")
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    print("🧹 Clearing problematic files from Pico W...")
    if clear_main_py():
        print("🎉 Ready to upload fresh files!")
        print("💻 Run: make upload")
    else:
        print("⚠️  Could not clear filesystem automatically")
        print("🔄 You may need to do another manual reset") 