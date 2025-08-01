"""
Test binary time display logic for Pimple Pink Binary Clock
"""
import time
import machine
import neopixel
from machine import Pin

# Configuration matching the schematic
NEOPIXEL_PIN = 2
NUM_PIXELS = 10

# Colors
PINK = (255, 20, 147)  # Pimple Pink
OFF = (0, 0, 0)

# Initialize NeoPixels
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)
onboard_led = Pin("LED", Pin.OUT)

def clear_display():
    """Clear all pixels"""
    for i in range(NUM_PIXELS):
        np[i] = OFF
    np.write()

def display_binary_time(hours, minutes):
    """Display time in binary format - Arduino style"""
    clear_display()
    
    # Convert to 12-hour format like Arduino
    display_hours = hours
    if display_hours > 12:
        display_hours = display_hours % 12
    if display_hours == 0:
        display_hours = 12
        
    print(f"Time: {hours:02d}:{minutes:02d} -> Display: {display_hours} hours, {minutes} minutes")
    
    # Hours (0-11) - first 4 pixels (pixels 0-3)
    print(f"Hours {display_hours} = {display_hours:04b}")
    for h in range(4):
        if (display_hours >> h) & 1:  # Check bit h
            np[h] = PINK
            print(f"  Pixel {h}: ON")
        else:
            np[h] = OFF
            print(f"  Pixel {h}: OFF")
    
    # Minutes (0-59) - next 6 pixels (pixels 4-9)
    print(f"Minutes {minutes} = {minutes:06b}")
    for m in range(6):
        if (minutes >> m) & 1:  # Check bit m
            np[m + 4] = PINK
            print(f"  Pixel {m + 4}: ON")
        else:
            np[m + 4] = OFF
            print(f"  Pixel {m + 4}: OFF")
            
    np.write()

def test_times():
    """Test various times"""
    test_cases = [
        (12, 0),   # Noon
        (1, 15),   # 1:15
        (3, 30),   # 3:30
        (6, 45),   # 6:45
        (9, 59),   # 9:59
        (0, 0),    # Midnight (should show as 12:00)
        (13, 30),  # 1:30 PM (should show as 1:30)
        (23, 45),  # 11:45 PM (should show as 11:45)
    ]
    
    for hours, minutes in test_cases:
        print(f"\n{'='*40}")
        print(f"Testing {hours:02d}:{minutes:02d}")
        print('='*40)
        
        display_binary_time(hours, minutes)
        
        # Show which pixels are lit
        lit_pixels = []
        for i in range(NUM_PIXELS):
            if np[i] == PINK:
                lit_pixels.append(i)
        
        print(f"Lit pixels: {lit_pixels}")
        
        # Heartbeat
        onboard_led.on()
        time.sleep(2)
        onboard_led.off()
        time.sleep(1)

def demo_sequence():
    """Demo sequence showing time progression"""
    print("\n🎨 Demo: Time progression")
    
    for minute in range(0, 60, 5):  # Every 5 minutes
        display_binary_time(3, minute)  # 3 o'clock
        print(f"3:{minute:02d}")
        time.sleep(0.5)
    
    clear_display()

def main():
    """Run binary time tests"""
    print("🕐 Pimple Pink Binary Clock - Time Display Test")
    print("Hardware: 10 NeoPixels on pin 2")
    print("Layout: Pixels 0-3 = Hours, Pixels 4-9 = Minutes")
    print("="*50)
    
    try:
        # Test specific times
        test_times()
        
        # Demo sequence
        demo_sequence()
        
        print("\n✅ Binary time test complete!")
        print("💡 Check that the lit pixels match the binary representation")
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        clear_display()

if __name__ == "__main__":
    main() 