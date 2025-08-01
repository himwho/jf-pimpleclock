#!/usr/bin/env python3
"""
Run test scripts on Pico W
"""
import serial
import time
import sys

def run_test(test_file, device_port='/dev/tty.usbmodem1201', baud_rate=115200):
    """Run a test script on the Pico W"""
    try:
        s = serial.Serial(device_port, baud_rate, timeout=2)
        
        # Stop any running program and clear
        s.write(b'\r\n\x03\r\n')
        time.sleep(1)
        
        # Run the test
        print(f'Running {test_file}...')
        s.write(f'exec(open("{test_file}").read())\r\n'.encode())
        time.sleep(3)
        
        # Read output
        print(f'{test_file} output:')
        print('-' * 40)
        
        try:
            for i in range(50):  # Read for up to 25 seconds
                line = s.readline().decode().strip()
                if line and not line.startswith('>>>'):
                    print(line)
                    
                    # Highlight important messages
                    if any(word in line.lower() for word in ['web server', 'running on http', 'ip:', 'error', 'wifi connected']):
                        if 'error' in line.lower():
                            print('🔴 ERROR detected above')
                        elif any(word in line.lower() for word in ['web server', 'running on http']):
                            print('✅ Web server started!')
                        elif 'wifi connected' in line.lower():
                            print('✅ WiFi connected!')
                            
                time.sleep(0.5)
        except KeyboardInterrupt:
            print('\n⏹️  Test stopped by user')
            s.write(b'\x03')
            
        s.close()
        
    except Exception as e:
        print(f"Error running test: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_test.py <test_file> [device_port]")
        print("Examples:")
        print("  python run_test.py test_leds.py")
        print("  python run_test.py test_web.py") 
        print("  python run_test.py test_binary_time.py")
        print("  python run_test.py main.py")
        sys.exit(1)
        
    test_file = sys.argv[1]
    device_port = sys.argv[2] if len(sys.argv) > 2 else '/dev/tty.usbmodem1201'
    
    run_test(test_file, device_port) 