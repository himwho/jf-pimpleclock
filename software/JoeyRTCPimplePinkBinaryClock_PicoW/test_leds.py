"""
Simple LED test for Pimple Pink Binary Clock
"""
import time
import machine
import neopixel
from machine import Pin

# Configuration
NEOPIXEL_PIN = 2
NUM_PIXELS = 10

# Colors
PINK = (255, 20, 147)  # Pimple Pink
GREEN = (0, 255, 25)   # Accent Green
OFF = (0, 0, 0)

# Initialize NeoPixels
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)
onboard_led = Pin("LED", Pin.OUT)

def clear_all():
    """Clear all LEDs"""
    for i in range(NUM_PIXELS):
        np[i] = OFF
    np.write()

def test_individual_leds():
    """Test each LED individually"""
    print("🔍 Testing individual LEDs...")
    clear_all()
    
    for i in range(NUM_PIXELS):
        print(f"LED {i}")
        np[i] = PINK
        np.write()
        time.sleep(0.2)
        np[i] = OFF
        np.write()
        time.sleep(0.1)

def test_all_pink():
    """Test all LEDs pink"""
    print("💖 All LEDs pink...")
    for i in range(NUM_PIXELS):
        np[i] = PINK
    np.write()
    time.sleep(2)

def test_all_green():
    """Test all LEDs green"""
    print("💚 All LEDs green...")
    for i in range(NUM_PIXELS):
        np[i] = GREEN
    np.write()
    time.sleep(2)

def heartbeat_test():
    """Heartbeat pattern"""
    print("❤️  Heartbeat test...")
    for _ in range(NUM_PIXELS):
        # Pulse LED
        onboard_led.on()
        
        # Pulse LED
        np[0] = PINK
        np.write()
        time.sleep(0.1)
        
        onboard_led.off()
        np[0] = OFF
        np.write()
        time.sleep(0.4)

def main():
    """Run all LED tests"""
    print("🎨 Pimple Pink Binary Clock - LED Test")
    print("=" * 40)
    
    try:
        # Test sequence
        test_all_pink()
        clear_all()
        time.sleep(0.5)
        
        test_all_green()
        clear_all()
        time.sleep(0.5)
        
        test_individual_leds()
        clear_all()
        time.sleep(0.5)
        
        heartbeat_test()
        clear_all()
        
        print("✅ LED test complete!")
        print("💡 If you saw the LEDs light up, hardware is working!")
        print("🔧 If no LEDs lit up, check:")
        print("   - NeoPixel strip connected to pin 16")
        print("   - Power supply adequate for LEDs") 
        print("   - Ground connection")
        
    except Exception as e:
        print(f"❌ LED test error: {e}")
        clear_all()

if __name__ == "__main__":
    main() 