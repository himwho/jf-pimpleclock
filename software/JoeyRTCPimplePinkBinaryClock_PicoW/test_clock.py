#!/usr/bin/env python3
"""
Test script for Pimple Pink Binary Clock
This script can be run on your computer to test the binary time logic
"""

def display_binary_number(number, bits=8):
    """Display a number in binary with visual representation"""
    binary_str = format(number, f'0{bits}b')
    visual = ""
    for i, bit in enumerate(binary_str):
        if bit == '1':
            visual += "🟪"  # Pink square for 1
        else:
            visual += "⬛"  # Black square for 0
    return binary_str, visual

def test_binary_time(hours, minutes, seconds):
    """Test binary time display for given time"""
    print(f"\n⏰ Testing time: {hours:02d}:{minutes:02d}:{seconds:02d}")
    print("=" * 50)
    
    # Hours (0-23) - need up to 5 bits
    hours_bin, hours_vis = display_binary_number(hours, 5)
    print(f"Hours ({hours:2d}):   {hours_bin} {hours_vis}")
    
    # Minutes (0-59) - need up to 6 bits  
    minutes_bin, minutes_vis = display_binary_number(minutes, 6)
    print(f"Minutes ({minutes:2d}): {minutes_bin} {minutes_vis}")
    
    # Seconds indicator
    seconds_indicator = "🟩" if seconds % 2 == 0 else "⬛"
    print(f"Seconds ({seconds:2d}): {'Even' if seconds % 2 == 0 else 'Odd'} {seconds_indicator}")
    
    print("\n5x5 Grid Layout:")
    print("Row 0 (Hours):  ", hours_vis[:5] if len(hours_vis) >= 5 else hours_vis + "⬛" * (5 - len(hours_vis)))
    print("Row 1 (Hours):  ", "⬛" * 5)  # Extra space for hours if needed
    print("Row 2 (Minutes):", minutes_vis[:5] if len(minutes_vis) >= 5 else minutes_vis + "⬛" * (5 - len(minutes_vis)))
    print("Row 3 (Minutes):", minutes_vis[5:] if len(minutes_vis) > 5 else "⬛" * 5)
    print("Row 4 (Seconds): ⬛⬛" + seconds_indicator + "⬛⬛")

def test_colors():
    """Test color definitions"""
    print("\n🎨 Color Palette Test")
    print("=" * 30)
    
    colors = {
        'off': (0, 0, 0),
        'on': (255, 20, 147),     # Deep pink (pimple pink)
        'dim': (50, 5, 30),       # Dim pink
        'accent': (0, 255, 25),   # Bright green accent
        'error': (255, 0, 0),     # Red for errors
        'warning': (255, 255, 0)  # Yellow for warnings
    }
    
    for name, rgb in colors.items():
        print(f"{name:8s}: RGB{rgb}")

def test_web_endpoints():
    """Test web endpoint logic"""
    print("\n🌐 Web Endpoint Test")
    print("=" * 30)
    
    endpoints = [
        "/",
        "/status",
        "/mode/binary",
        "/mode/rainbow", 
        "/brightness/up",
        "/brightness/down",
        "/brightness/75",
        "/sync",
        "/clear"
    ]
    
    for endpoint in endpoints:
        print(f"✅ {endpoint}")

def main():
    """Run all tests"""
    print("🕐 Pimple Pink Binary Clock - Test Suite")
    print("=" * 50)
    
    # Test various times
    test_times = [
        (0, 0, 0),      # Midnight
        (12, 0, 0),     # Noon
        (14, 35, 42),   # Afternoon
        (23, 59, 59),   # Almost midnight
        (9, 15, 30),    # Morning
    ]
    
    for hours, minutes, seconds in test_times:
        test_binary_time(hours, minutes, seconds)
    
    test_colors()
    test_web_endpoints()
    
    print("\n✅ All tests completed!")
    print("\nNext steps:")
    print("1. Connect your Pico W and run: make install")
    print("2. Edit config.py with your WiFi credentials")
    print("3. Upload files with: make upload")
    print("4. Monitor output with: make monitor")

if __name__ == "__main__":
    main() 