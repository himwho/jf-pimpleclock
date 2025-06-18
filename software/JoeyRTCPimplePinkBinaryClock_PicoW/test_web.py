"""
Simple web server test for Pimple Pink Binary Clock
"""
import network
import socket
import time
from machine import Pin

# Configuration
WIFI_SSID = "sistersweetheart"
WIFI_PASSWORD = "sabrinacunningham"

# Hardware
onboard_led = Pin("LED", Pin.OUT)

def connect_wifi():
    """Connect to WiFi"""
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
        onboard_led.on()
        network_info = wlan.ifconfig()
        print(f"✅ WiFi connected! IP: {network_info[0]}")
        return network_info[0]
    else:
        onboard_led.off()
        print("❌ WiFi connection failed")
        return None

def simple_webpage():
    """Generate a simple test webpage"""
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Pimple Pink Clock Test</title>
        <style>
            body { 
                font-family: Arial, sans-serif; 
                background: #1a1a1a; 
                color: #ff1493; 
                text-align: center;
                padding: 20px;
            }
            .container { 
                max-width: 600px; 
                margin: 0 auto; 
                background: #2a2a2a; 
                padding: 30px; 
                border-radius: 10px;
                border: 2px solid #ff1493;
            }
            h1 { color: #ff1493; }
            button { 
                background: #ff1493; 
                color: white; 
                border: none; 
                padding: 10px 20px; 
                margin: 5px; 
                border-radius: 5px; 
                cursor: pointer;
                font-size: 16px;
            }
            button:hover { background: #e91e63; }
            .status { 
                background: #333; 
                padding: 15px; 
                border-radius: 5px; 
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🕐 Pimple Pink Binary Clock</h1>
            <h2>✅ Web Server Test Successful!</h2>
            
            <div class="status">
                <p><strong>Status:</strong> Web server is running correctly</p>
                <p><strong>Time:</strong> <span id="time">Loading...</span></p>
            </div>
            
            <div>
                <button onclick="testLEDs()">Test LEDs</button>
                <button onclick="testTime()">Test Time</button>
                <button onclick="location.reload()">Refresh</button>
            </div>
            
            <div id="result" style="margin-top: 20px;"></div>
        </div>
        
        <script>
            function updateTime() {
                const now = new Date();
                document.getElementById('time').textContent = now.toLocaleTimeString();
            }
            
            function testLEDs() {
                document.getElementById('result').innerHTML = 
                    '<p style="color: #00ff19;">🎨 LED test command sent!</p>';
                fetch('/test-leds');
            }
            
            function testTime() {
                document.getElementById('result').innerHTML = 
                    '<p style="color: #00ff19;">🕐 Time sync command sent!</p>';
                fetch('/test-time');
            }
            
            // Update time every second
            setInterval(updateTime, 1000);
            updateTime();
        </script>
    </body>
    </html>
    """
    return html

def handle_request(client_socket):
    """Handle incoming HTTP requests"""
    try:
        request = client_socket.recv(1024).decode()
        print(f"Request: {request.split()[0:2] if request else 'Empty'}")
        
        if 'GET /' in request:
            # Main page
            response_body = simple_webpage()
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n{response_body}"
            
        elif 'GET /test-leds' in request:
            # LED test endpoint
            print("🎨 LED test requested")
            response_body = "LED test triggered"
            response = f"HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\n{response_body}"
            
        elif 'GET /test-time' in request:
            # Time test endpoint
            print("🕐 Time test requested")
            response_body = "Time sync triggered"
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

def run_web_server(ip_address):
    """Run the simple web server"""
    try:
        # Create socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind(('0.0.0.0', 80))
        server_socket.listen(1)
        
        print(f"🌐 Web server running on http://{ip_address}")
        print("🔗 Open this URL in your web browser to test!")
        print("⏹️  Press Ctrl+C to stop")
        
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
        
    finally:
        try:
            server_socket.close()
        except:
            pass

def main():
    """Main test function"""
    print("🌐 Pimple Pink Binary Clock - Web Server Test")
    print("=" * 50)
    
    # Connect to WiFi
    ip_address = connect_wifi()
    
    if ip_address:
        print(f"✅ Ready to test web interface!")
        print(f"🔗 URL: http://{ip_address}")
        time.sleep(2)
        
        # Start web server
        run_web_server(ip_address)
        
    else:
        print("❌ Cannot start web server without WiFi connection")
        print("🔧 Check your WiFi credentials in the script")

if __name__ == "__main__":
    main() 