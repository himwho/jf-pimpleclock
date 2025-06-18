# Pimple Pink Binary Clock Configuration

# WiFi Settings
WIFI_SSID = "sistersweetheart"
WIFI_PASSWORD = "sabrinacunningham"

# Hardware Configuration
NEOPIXEL_PIN = 16
NUM_PIXELS = 25  # 5x5 grid

# Time Settings
TIMEZONE_OFFSET = -8  # Hours from UTC (PST = -8, EST = -5, GMT = 0)
NTP_SERVER = "pool.ntp.org"
UPDATE_INTERVAL = 3600  # Sync time every hour (seconds)

# Display Settings
DEFAULT_BRIGHTNESS = 50  # 10-100%
DEFAULT_MODE = "binary"  # "binary" or "rainbow"

# Colors (RGB values 0-255)
COLORS = {
    'off': (0, 0, 0),
    'on': (255, 20, 147),     # Deep pink (pimple pink)
    'dim': (50, 5, 30),       # Dim pink
    'accent': (0, 255, 25),   # Bright green accent
    'error': (255, 0, 0),     # Red for errors
    'warning': (255, 255, 0)  # Yellow for warnings
}

# Web Server Settings
WEB_PORT = 80
WEB_TIMEOUT = 30  # seconds

# Debug Settings
DEBUG = True
SERIAL_DEBUG = True 