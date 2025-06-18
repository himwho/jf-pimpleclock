# 🕐 Pimple Pink Binary Clock - MicroPython Edition

A beautiful binary clock with NeoPixel display and web interface, now powered by **MicroPython** for maximum simplicity and ease of development!

![Pimple Pink Binary Clock](https://img.shields.io/badge/Pico%20W-MicroPython-green)
![Status](https://img.shields.io/badge/Status-Active-brightgreen)
![License](https://img.shields.io/badge/License-MIT-blue)

## ✨ Features

- **🎨 Pimple Pink Theme**: Beautiful deep pink (#ff1493) LEDs with bright green (#00ff19) accents
- **⏰ Binary Time Display**: Shows hours, minutes, and seconds in binary on a 5x5 NeoPixel grid
- **🌐 Web Interface**: Real-time web dashboard for control and monitoring
- **📡 WiFi Connected**: Automatic NTP time synchronization
- **🌈 Multiple Modes**: Binary time display and rainbow animation modes
- **💡 Brightness Control**: Adjustable LED brightness via web interface
- **📱 Mobile Friendly**: Responsive web interface works on phones and tablets
- **🔄 Real-time Updates**: Live time updates via AJAX
- **⚙️ Easy Configuration**: Simple Python configuration file

## 🚀 Quick Start

### Prerequisites

- Raspberry Pi Pico W
- 25 NeoPixel LEDs (WS2812B) arranged in 5x5 grid
- Python 3.7+ on your computer
- USB cable for programming

### Installation

1. **Install dependencies:**
   ```bash
   make deps
   ```

2. **Flash MicroPython and upload code:**
   ```bash
   make install
   ```

3. **Configure WiFi:**
   ```bash
   make config
   ```
   Edit `config.py` with your WiFi credentials and timezone.

4. **Monitor startup:**
   ```bash
   make monitor
   ```
   Look for the IP address in the output.

5. **Access web interface:**
   Open the IP address in your browser!

## 🔧 Hardware Setup

### Wiring

```
Pico W Pin 16 (GPIO16) → NeoPixel Data In
Pico W 3V3 (Pin 36)    → NeoPixel VCC
Pico W GND (Pin 38)    → NeoPixel GND
```

### NeoPixel Grid Layout

```
[0 ] [1 ] [2 ] [3 ] [4 ]   ← Hours (binary)
[5 ] [6 ] [7 ] [8 ] [9 ]   ← Hours (binary)
[10] [11] [12] [13] [14]   ← Minutes (binary)
[15] [16] [17] [18] [19]   ← Minutes (binary)
[20] [21] [22] [23] [24]   ← Seconds indicator
```

## ⚙️ Configuration

Edit `config.py` to customize your clock:

```python
# WiFi Settings
WIFI_SSID = "YourWiFiNetwork"
WIFI_PASSWORD = "YourPassword"

# Time Settings
TIMEZONE_OFFSET = -8  # PST = -8, EST = -5, GMT = 0

# Hardware
NEOPIXEL_PIN = 16
NUM_PIXELS = 25

# Display
DEFAULT_BRIGHTNESS = 50  # 10-100%
DEFAULT_MODE = "binary"  # "binary" or "rainbow"
```

## 🌐 Web Interface

The web interface provides:

- **Real-time clock display** with auto-updates
- **Mode switching** between binary and rainbow modes
- **Brightness control** with slider and buttons
- **Time synchronization** button
- **System status** monitoring
- **Mobile-responsive design** with Pimple Pink theme

### Available Endpoints

- `/` - Main dashboard
- `/status` - JSON status API
- `/mode/binary` - Switch to binary mode
- `/mode/rainbow` - Switch to rainbow mode
- `/brightness/up` - Increase brightness
- `/brightness/down` - Decrease brightness
- `/brightness/50` - Set specific brightness
- `/sync` - Sync time with NTP
- `/clear` - Clear display

## 🛠️ Development

### Makefile Commands

```bash
make help           # Show all available commands
make deps           # Install Python dependencies
make flash          # Flash MicroPython firmware
make upload         # Upload Python files to Pico W
make config         # Edit configuration
make monitor        # Monitor serial output
make test           # Test connectivity
make reset          # Reset the Pico W
make backup         # Backup files from Pico W
make status         # Show project status
make clean          # Clean temporary files
make lint           # Check code style
make format         # Format code with black
```

### File Structure

```
├── main.py                 # Main MicroPython application
├── config.py              # Configuration settings
├── install_micropython.py # Installation helper script
├── Makefile               # Development workflow
└── README.md              # This file
```

### Binary Time Format

The binary clock displays time using a 5x5 grid of NeoPixels:

- **Hours (0-23)**: Top 2 rows (10 bits)
- **Minutes (0-59)**: Middle 2 rows (10 bits)  
- **Seconds**: Bottom center pixel blinks every second

Each bit represents a power of 2, read from right to left:
- `1` = Pink pixel (LED on)
- `0` = Dark pixel (LED off)

Example: 14:35:42
- Hours (14) = `0000001110` binary
- Minutes (35) = `0000100011` binary
- Seconds (42) = Even, so center pixel is ON

## 🎨 Customization

### Colors

Modify colors in `config.py`:

```python
COLORS = {
    'off': (0, 0, 0),           # Black (off)
    'on': (255, 20, 147),       # Deep pink (pimple pink)
    'dim': (50, 5, 30),         # Dim pink
    'accent': (0, 255, 25),     # Bright green accent
    'error': (255, 0, 0),       # Red for errors
    'warning': (255, 255, 0)    # Yellow for warnings
}
```

### Display Modes

Add new display modes by extending the `BinaryClock` class:

```python
def display_custom_mode(self):
    # Your custom display logic here
    pass
```

## 🐛 Troubleshooting

### Common Issues

1. **WiFi won't connect**
   - Check SSID and password in `config.py`
   - Ensure 2.4GHz network (Pico W doesn't support 5GHz)
   - Check signal strength

2. **Upload fails**
   - Try `make reset` first
   - Check USB connection
   - Verify device port in Makefile

3. **NeoPixels don't light up**
   - Check wiring connections
   - Verify power supply (NeoPixels need 3.3V or 5V)
   - Check `NEOPIXEL_PIN` setting in config

4. **Time is wrong**
   - Set correct `TIMEZONE_OFFSET` in config
   - Use `/sync` endpoint to force NTP sync
   - Check internet connection

### Debug Mode

Enable debug output in `config.py`:

```python
DEBUG = True
SERIAL_DEBUG = True
```

Then monitor serial output:
```bash
make monitor
```

## 📱 Mobile App (Future)

A companion mobile app is planned with features:
- Remote control and monitoring
- Custom color themes
- Alarm and timer functions
- Multiple clock management

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- [ ] Additional display modes (analog, digital, etc.)
- [ ] Sound/buzzer integration for alarms
- [ ] Weather display integration
- [ ] Home Assistant integration
- [ ] Battery power optimization
- [ ] Custom web themes

## 📄 License

MIT License - see LICENSE file for details.

## 🙏 Acknowledgments

- **MicroPython Team** for the excellent Python implementation
- **Raspberry Pi Foundation** for the Pico W
- **Adafruit** for NeoPixel libraries and inspiration
- **Random Nerd Tutorials** for MicroPython web server examples

---

**Why MicroPython?**

We switched from C++ to MicroPython because:
- ✅ **10x simpler** web server implementation
- ✅ **No complex build system** or lwIP configuration
- ✅ **Faster development** with instant file uploads
- ✅ **Better debugging** with Python REPL
- ✅ **Easier customization** for users
- ✅ **Dynamic updates** without recompilation

The result is a much more maintainable and user-friendly binary clock! 🎉 