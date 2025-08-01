#!/usr/bin/env python3
"""
Get IP address from Pico W
"""
import serial
import time
import sys

def get_pico_ip(device_port='/dev/tty.usbmodem1201', baud_rate=115200):
    """Get IP address from connected Pico W"""
    try:
        s = serial.Serial(device_port, baud_rate, timeout=2)
        
        # Clear any existing output
        s.write(b'\r\n')
        time.sleep(0.5)
        
        # Send network check commands
        s.write(b'try:\r\n')
        s.write(b'    import network\r\n')
        s.write(b'    wlan = network.WLAN(network.STA_IF)\r\n')
        s.write(b'    if wlan.isconnected():\r\n')
        s.write(b'        ip_info = wlan.ifconfig()\r\n')
        s.write(b'        print(f"IP_ADDRESS: {ip_info[0]}")\r\n')
        s.write(b'        print(f"Netmask: {ip_info[1]}")\r\n')
        s.write(b'        print(f"Gateway: {ip_info[2]}")\r\n')
        s.write(b'        print(f"DNS: {ip_info[3]}")\r\n')
        s.write(b'    else:\r\n')
        s.write(b'        print("ERROR: Not connected to WiFi")\r\n')
        s.write(b'except Exception as e:\r\n')
        s.write(b'    print(f"ERROR: {e}")\r\n')
        s.write(b'\r\n')
        
        time.sleep(1)
        
        # Read responses
        found_ip = False
        ip_address = None
        
        for i in range(10):
            line = s.readline().decode().strip()
            if line and not line.startswith('>>>'):
                print(line)
                if line.startswith('IP_ADDRESS:'):
                    ip_address = line.split(': ')[1]
                    print(f'\033[0;32m🌐 Your Pico W is at: http://{ip_address}\033[0m')
                    found_ip = True
            time.sleep(0.2)
        
        if not found_ip:
            print('\033[0;33m⚠️  Could not determine IP address\033[0m')
            
        s.close()
        return ip_address
        
    except Exception as e:
        print(f"Error connecting to device: {e}")
        return None

if __name__ == "__main__":
    device_port = sys.argv[1] if len(sys.argv) > 1 else '/dev/tty.usbmodem1201'
    get_pico_ip(device_port) 