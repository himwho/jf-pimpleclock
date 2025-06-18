# Web Interface Guide

## Joey's Pimple Pink Binary Clock - Web Interface

The Pico W firmware now includes a built-in web interface that allows you to monitor your binary clock remotely!

### 🌐 Accessing the Web Interface

1. **Flash the firmware** to your Pico W using `make flash`
2. **Connect to WiFi** - The device will automatically connect using credentials from your `.env` file
3. **Find the IP address** - Check the serial monitor for the IP address (usually something like `192.168.1.xxx`)
4. **Open in browser** - Visit `http://[IP_ADDRESS]` in any web browser

### 📱 Features

- **Real-time Status**: Shows uptime, WiFi connection status, and current LED
- **Auto-refresh**: Page updates every 5 seconds automatically
- **Mobile-friendly**: Works on phones, tablets, and desktops
- **Pimple Pink Theme**: Beautiful dark theme with signature #00ff19 color
- **JSON API**: Visit `/status` for JSON data

### 🔧 Setup Instructions

1. **Configure WiFi**:
   ```bash
   # Edit your WiFi credentials
   nano .env
   ```

2. **Build and Flash**:
   ```bash
   make build
   make flash
   ```

3. **Monitor Serial Output**:
   ```bash
   make monitor
   ```
   Look for output like:
   ```
   =====================================
   Joey's Pimple Pink Binary Clock v2.0
   =====================================
   Connecting to WiFi 'YourNetwork'...
   Connected to WiFi!
   IP Address: 192.168.1.123
   Web server started successfully!
   Visit: http://192.168.1.123
   =====================================
   ```

### 🌸 Web Interface Preview

The web interface shows:
- **System Status**: Uptime, WiFi status, current LED number
- **LED Display**: Visual representation of the LED pattern
- **Auto-refresh**: Updates every 5 seconds
- **Responsive Design**: Works on all devices

### 🔌 API Endpoints

- `GET /` - Main web interface (HTML)
- `GET /status` - JSON status data

Example JSON response:
```json
{
  "uptime": 1234,
  "wifi": "Connected", 
  "led": 5,
  "status": "running"
}
```

### 🐛 Troubleshooting

**Web interface not loading?**
- Check serial monitor for IP address
- Ensure device and computer are on same network
- Try refreshing the page
- Check WiFi credentials in `.env` file

**Can't connect to WiFi?**
- Verify WiFi credentials in `.env` file
- Check that network supports 2.4GHz (Pico W doesn't support 5GHz)
- Try restarting the device

**LED patterns not updating?**
- Web interface updates every 5 seconds
- Check that NeoPixel LEDs are properly connected
- Monitor serial output for errors

### 💡 Next Steps

This is a basic web interface. Future enhancements could include:
- Interactive LED controls
- Time setting via web interface
- Brightness adjustment
- Color customization
- Settings persistence
- Real-time WebSocket updates

Enjoy your web-enabled Pimple Pink Binary Clock! 🌸 