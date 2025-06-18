# Changelog

## Version 2.0 - Web Interface Edition

### 🌐 **Major New Feature: Web Interface**

- **Built-in Web Server**: TCP-based HTTP server running on port 80
- **Real-time Monitoring**: View system status, uptime, and current LED state
- **Pimple Pink Theme**: Beautiful dark interface with signature #00ff19 color
- **Mobile-Friendly**: Responsive design works on phones, tablets, and desktops
- **Auto-Refresh**: Page updates every 5 seconds automatically
- **JSON API**: RESTful endpoint at `/status` for developers
- **WiFi Integration**: Automatic connection using `.env` credentials

### 🛠️ **Build System Improvements**

- **WiFi Credential Validation**: Build process checks for configured WiFi settings
- **Enhanced Makefile**: Added `web-info` and `web-test` commands
- **Better Documentation**: Comprehensive web interface guide
- **Cleaner Architecture**: Separated web server into dedicated module

### 📱 **Web Interface Features**

**Main Dashboard (`/`):**
- System uptime display
- WiFi connection status
- Current LED number indicator
- Visual LED pattern representation
- Auto-refreshing every 5 seconds

**JSON API (`/status`):**
```json
{
  "uptime": 1234,
  "wifi": "Connected",
  "led": 5,
  "status": "running"
}
```

### 🔧 **Technical Details**

- **Protocol**: HTTP/1.1 over TCP
- **Port**: 80 (standard HTTP)
- **Memory**: Optimized for Pico W's limited RAM
- **Performance**: Non-blocking server with connection pooling
- **Compatibility**: Works with all modern browsers

### 📚 **Documentation**

- **WEB_INTERFACE.md**: Complete web interface guide
- **Updated README.md**: Added web interface section
- **Enhanced Makefile help**: New web-related commands

### 🚀 **Getting Started**

```bash
# 1. Configure WiFi
nano .env

# 2. Build with web interface
make build

# 3. Flash to Pico W
make flash

# 4. Monitor for IP address
make monitor

# 5. Visit web interface
# Open browser to IP shown in serial output
```

### 🎯 **What's Next**

Future enhancements could include:
- Interactive LED controls via web interface
- Time setting through web UI
- Brightness adjustment controls
- Color customization options
- WebSocket for real-time updates
- Settings persistence
- Mobile app integration

---

## Version 1.0 - Initial Release

### ✨ **Core Features**

- **Raspberry Pi Pico W Support**: Native C/C++ implementation
- **NeoPixel LEDs**: WS2812 support with PIO
- **DS3231 RTC**: I2C real-time clock integration
- **Button Controls**: Debounced button handling
- **DFPlayer Audio**: Serial audio module support
- **Pimple Pink Theme**: Signature #00ff19 color scheme
- **Multiple Build Options**: Arduino IDE, C/C++ SDK, MicroPython

### 🔌 **Hardware Support**

- 10 NeoPixel LEDs for binary time display
- 4 buttons for user interaction
- DS3231 RTC for accurate timekeeping
- DFPlayer Mini for audio feedback
- Proper pin mapping for custom PCB

### 🛠️ **Build System**

- Comprehensive Makefile with 20+ commands
- Cross-platform support (Linux, macOS, Windows)
- Automatic dependency management
- Multiple build configurations
- Easy flashing and monitoring

---

*Joey's Pimple Pink Binary Clock - Making time beautiful, one LED at a time! 🌸* 