"""
Pimple Pink Binary Clock - MicroPython Version
A binary clock with NeoPixel display and web interface
"""

import network
import socket
import time
import machine
import neopixel
import ntptime
from machine import Pin, RTC
import _thread
import gc

# Import configuration
try:
    from config import *
except ImportError:
    # Fallback configuration if config.py is missing
    WIFI_SSID = "sistersweetheart"
    WIFI_PASSWORD = "sabrinacunningham"
    NEOPIXEL_PIN = 2
    NUM_PIXELS = 10
    TIMEZONE_OFFSET = -8
    NTP_SERVER = "pool.ntp.org"
    DEFAULT_BRIGHTNESS = 50
    DEFAULT_MODE = "binary"
    COLORS = {
        'off': (0, 0, 0),
        'on': (255, 20, 147),
        'dim': (50, 5, 30),
        'accent': (0, 255, 25)
    }

# Hardware setup
np = neopixel.NeoPixel(Pin(NEOPIXEL_PIN), NUM_PIXELS)
rtc = RTC()
onboard_led = Pin("LED", Pin.OUT)

# Global state
current_time = None
display_mode = DEFAULT_MODE
brightness = DEFAULT_BRIGHTNESS
wifi_connected = False
web_server_running = False

class BinaryClock:
    def __init__(self):
        self.display_buffer = [(0, 0, 0)] * NUM_PIXELS
        self.last_update = 0
        
    def clear_display(self):
        """Clear all pixels"""
        for i in range(NUM_PIXELS):
            np[i] = COLORS['off']
        np.write()
        
    def display_binary_time(self, hours, minutes, seconds):
        """Display time in binary format - Arduino style"""
        self.clear_display()
        
        # Convert to 12-hour format like Arduino
        display_hours = hours
        if display_hours > 12:
            display_hours = display_hours % 12
        if display_hours == 0:
            display_hours = 12
            
        # Hours (0-11) - first 4 pixels (pixels 0-3)
        for h in range(4):
            if (display_hours >> h) & 1:  # Check bit h
                color = COLORS['on']
                if brightness < 100:
                    color = tuple(int(c * brightness / 100) for c in color)
                np[h] = color
            else:
                np[h] = COLORS['off']
        
        # Minutes (0-59) - next 6 pixels (pixels 4-9)
        for m in range(6):
            if (minutes >> m) & 1:  # Check bit m
                color = COLORS['on']
                if brightness < 100:
                    color = tuple(int(c * brightness / 100) for c in color)
                np[m + 4] = color
            else:
                np[m + 4] = COLORS['off']
                
        np.write()
                    
    def display_rainbow(self):
        """Display a rainbow pattern"""
        for i in range(NUM_PIXELS):
            hue = (i * 360 // NUM_PIXELS + time.ticks_ms() // 50) % 360
            rgb = self.hsv_to_rgb(hue, 100, brightness)
            np[i] = rgb
        np.write()
        
    def hsv_to_rgb(self, h, s, v):
        """Convert HSV to RGB"""
        h = h / 360.0
        s = s / 100.0
        v = v / 100.0
        
        i = int(h * 6.0)
        f = (h * 6.0) - i
        p = v * (1.0 - s)
        q = v * (1.0 - s * f)
        t = v * (1.0 - s * (1.0 - f))
        
        i = i % 6
        if i == 0:
            r, g, b = v, t, p
        elif i == 1:
            r, g, b = q, v, p
        elif i == 2:
            r, g, b = p, v, t
        elif i == 3:
            r, g, b = p, q, v
        elif i == 4:
            r, g, b = t, p, v
        elif i == 5:
            r, g, b = v, p, q
            
        return (int(r * 255), int(g * 255), int(b * 255))

# Initialize clock
clock = BinaryClock()

def connect_wifi():
    """Connect to WiFi network"""
    global wifi_connected
    
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    
    if not wlan.isconnected():
        print(f"Connecting to WiFi: {WIFI_SSID}")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        
        timeout = 10
        while timeout > 0 and not wlan.isconnected():
            print("Waiting for WiFi connection...")
            onboard_led.toggle()
            time.sleep(1)
            timeout -= 1
            
    if wlan.isconnected():
        wifi_connected = True
        onboard_led.on()
        network_info = wlan.ifconfig()
        print(f"WiFi connected! IP: {network_info[0]}")
        return network_info[0]
    else:
        wifi_connected = False
        onboard_led.off()
        print("WiFi connection failed")
        return None

def sync_time():
    """Synchronize time with NTP server"""
    global current_time
    
    if wifi_connected:
        try:
            print("Syncing time with NTP...")
            ntptime.settime()
            
            # Adjust for timezone
            current_time = time.localtime(time.time() + TIMEZONE_OFFSET * 3600)
            rtc.datetime((
                current_time[0],  # year
                current_time[1],  # month
                current_time[2],  # day
                current_time[6],  # weekday
                current_time[3],  # hour
                current_time[4],  # minute
                current_time[5],  # second
                0                 # subsecond
            ))
            print(f"Time synced: {current_time[3]:02d}:{current_time[4]:02d}:{current_time[5]:02d}")
            return True
        except Exception as e:
            print(f"NTP sync failed: {e}")
            return False
    return False

def get_current_time():
    """Get current time from RTC"""
    dt = rtc.datetime()
    return (dt[4], dt[5], dt[6])  # hour, minute, second

def webpage(ip_address):
    """Generate the web interface HTML"""
    current_time = get_current_time()
    time_str = f"{current_time[0]:02d}:{current_time[1]:02d}:{current_time[2]:02d}"
    
    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>🕐 Pimple Pink Binary Clock</title>
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body {{
                background: #000;
                color: #00ff19;
                font-family: 'Courier New', monospace;
                padding: 20px;
                margin: 0;
            }}
            .header {{
                text-align: center;
                border: 2px solid #00ff19;
                padding: 20px;
                margin-bottom: 20px;
                background: rgba(0, 255, 25, 0.1);
            }}
            .status {{
                border: 1px solid #00ff19;
                padding: 15px;
                margin: 10px 0;
                background: rgba(0, 255, 25, 0.05);
            }}
            .controls {{
                display: flex;
                flex-wrap: wrap;
                gap: 10px;
                margin: 20px 0;
            }}
            button {{
                background: #000;
                color: #00ff19;
                border: 2px solid #00ff19;
                padding: 10px 20px;
                font-family: inherit;
                cursor: pointer;
                transition: all 0.3s;
            }}
            button:hover {{
                background: #00ff19;
                color: #000;
            }}
            .time-display {{
                font-size: 2em;
                text-align: center;
                margin: 20px 0;
                color: #ff1493;
            }}
            .grid {{
                display: grid;
                grid-template-columns: repeat(5, 30px);
                grid-gap: 2px;
                justify-content: center;
                margin: 20px 0;
            }}
            .pixel {{
                width: 30px;
                height: 30px;
                border: 1px solid #333;
                background: #111;
            }}
            .pixel.on {{
                background: #ff1493;
                box-shadow: 0 0 10px #ff1493;
            }}
            .slider-container {{
                margin: 20px 0;
            }}
            .slider {{
                width: 100%;
                background: #333;
                outline: none;
            }}
        </style>
        <script>
            function updateClock() {{
                fetch('/status')
                    .then(response => response.json())
                    .then(data => {{
                        document.getElementById('time').textContent = data.time;
                        document.getElementById('uptime').textContent = data.uptime;
                        // Update pixel grid if needed
                    }})
                    .catch(err => console.log('Update failed:', err));
            }}
            
            setInterval(updateClock, 1000);
            
            function sendCommand(cmd) {{
                fetch('/' + cmd)
                    .then(() => updateClock())
                    .catch(err => console.log('Command failed:', err));
            }}
        </script>
    </head>
    <body>
        <div class="header">
            <h1>🕐 Pimple Pink Binary Clock</h1>
            <p>IoT Binary Clock Control Panel</p>
        </div>
        
        <div class="time-display" id="time">
            {time_str}
        </div>
        
        <div class="status">
            <h2>System Status</h2>
            <p>✅ WiFi: Connected ({ip_address})</p>
            <p>🕒 Current Time: <span id="time">{time_str}</span></p>
            <p>⏱️ Uptime: <span id="uptime">{time.ticks_ms() // 1000}s</span></p>
            <p>🎨 Display Mode: {display_mode}</p>
            <p>💡 Brightness: {brightness}%</p>
        </div>
        
        <div class="controls">
            <button onclick="sendCommand('mode/binary')">Binary Mode</button>
            <button onclick="sendCommand('mode/rainbow')">Rainbow Mode</button>
            <button onclick="sendCommand('brightness/up')">Brighter</button>
            <button onclick="sendCommand('brightness/down')">Dimmer</button>
            <button onclick="sendCommand('sync')">Sync Time</button>
            <button onclick="sendCommand('clear')">Clear Display</button>
        </div>
        
        <div class="slider-container">
            <label for="brightness">Brightness: {brightness}%</label>
            <input type="range" id="brightness" class="slider" min="10" max="100" value="{brightness}"
                   onchange="sendCommand('brightness/' + this.value)">
        </div>
        
        <div class="status">
            <h3>Binary Time Explanation</h3>
            <p>• Top 2 rows: Hours (0-23) in binary</p>
            <p>• Middle 2 rows: Minutes (0-59) in binary</p>
            <p>• Bottom center: Seconds indicator (blinks)</p>
            <p>• Pink pixels = 1, Dark pixels = 0</p>
        </div>
    </body>
    </html>
    """
    return html

def handle_request(client_socket):
    """Handle incoming HTTP requests - based on working test_web.py"""
    global display_mode, brightness
    
    try:
        request = client_socket.recv(1024).decode()
        print(f"Request: {request.split()[0:2] if request else 'Empty'}")
        
        if 'GET /' in request and not any(x in request for x in ['/mode/', '/brightness/', '/sync', '/clear']):
            # Main page
            wlan = network.WLAN(network.STA_IF)
            ip = wlan.ifconfig()[0] if wlan.isconnected() else "Unknown"
            response_body = webpage(ip)
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_body}"
            
        elif 'GET /mode/' in request:
            # Change display mode
            if '/mode/binary' in request:
                display_mode = 'binary'
            elif '/mode/rainbow' in request:
                display_mode = 'rainbow'
            response_body = f"Mode changed to {display_mode}"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{response_body}"
            
        elif 'GET /brightness/' in request:
            # Change brightness
            if '/brightness/up' in request:
                brightness = min(100, brightness + 10)
            elif '/brightness/down' in request:
                brightness = max(10, brightness - 10)
            else:
                # Try to parse specific brightness value
                try:
                    parts = request.split('/')
                    for i, part in enumerate(parts):
                        if part == 'brightness' and i + 1 < len(parts):
                            brightness = max(10, min(100, int(parts[i + 1].split()[0])))
                            break
                except:
                    pass
            response_body = f"Brightness set to {brightness}%"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{response_body}"
            
        elif 'GET /sync' in request:
            # Sync time
            if sync_time():
                response_body = "Time synchronized"
            else:
                response_body = "Time sync failed"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{response_body}"
            
        elif 'GET /clear' in request:
            # Clear display
            clock.clear_display()
            response_body = "Display cleared"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{response_body}"
            
        else:
            # 404 Not Found
            response_body = "Not Found"
            response = f"HTTP/1.1 404 Not Found\r\nContent-Type: text/plain\r\n\r\n{response_body}"
            
        client_socket.send(response.encode())
        
    except Exception as e:
        print(f"Request handling error: {e}")
        
    finally:
        client_socket.close()

def web_server():
    """Run the web server - based on working test_web.py"""
    global web_server_running
    
    try:
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 80))
        server_socket.listen(1)
        
        wlan = network.WLAN(network.STA_IF)
        ip = wlan.ifconfig()[0] if wlan.isconnected() else "Unknown"
        print(f"🌐 Web server running on http://{ip}")
        web_server_running = True
        
        while True:
            try:
                client_socket, addr = server_socket.accept()
                print(f"📡 Connection from {addr}")
                handle_request(client_socket)
                
            except KeyboardInterrupt:
                print("\n⏹️  Stopping web server...")
                break
                
            except Exception as e:
                print(f"Connection error: {e}")
                
    except Exception as e:
        print(f"Server error: {e}")
        web_server_running = False
        
    finally:
        try:
            server_socket.close()
        except:
            pass

def clock_update():
    """Update the clock display"""
    while True:
        try:
            current_time = get_current_time()
            
            if display_mode == "binary":
                clock.display_binary_time(current_time[0], current_time[1], current_time[2])
            elif display_mode == "rainbow":
                clock.display_rainbow()
                
            # Heartbeat
            if time.ticks_ms() % 2000 < 100:
                onboard_led.toggle()
                
        except Exception as e:
            print(f"Clock update error: {e}")
            
        time.sleep(1)

def main():
    """Main application loop"""
    print("🕐 Pimple Pink Binary Clock Starting...")
    
    # Initialize display
    clock.clear_display()
    
    # Connect to WiFi
    ip = connect_wifi()
    if ip:
        # Sync time
        sync_time()
        
        print("Starting clock and web server...")
        
        # Start web server in separate thread
        try:
            _thread.start_new_thread(web_server, ())
            print("Web server thread started")
        except Exception as e:
            print(f"Failed to start web server thread: {e}")
        
        # Run clock update in main thread
        clock_update()
        
    else:
        print("WiFi connection failed, running in offline mode")
        # Just run the clock
        clock_update()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("Shutting down...")
        clock.clear_display()
    except Exception as e:
        print(f"Fatal error: {e}")
        clock.clear_display()
    finally:
        machine.reset() 