# Pimple Pink Binary Clock - MicroPython Makefile
# This Makefile helps with MicroPython development workflow

.PHONY: help install flash upload config test clean monitor deps lint format test-leds test-web test-binary test-main ip get-ip

# Configuration
PYTHON := python3
PIP := pip3
DEVICE_PORT := /dev/tty.usbmodem1201
BAUD_RATE := 115200

# Files to upload to Pico W
UPLOAD_FILES := main.py config.py
TEST_FILES := test_leds.py test_web.py test_binary_time.py

# MicroPython firmware
FIRMWARE_URL := https://micropython.org/resources/firmware/RPI_PICO_W-20250415-v1.25.0.uf2
FIRMWARE_FILE := micropython-firmware-pico-w-290622.uf2

# Colors for output
RED := \033[0;31m
GREEN := \033[0;32m
YELLOW := \033[0;33m
BLUE := \033[0;34m
PURPLE := \033[0;35m
CYAN := \033[0;36m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(CYAN)🕐 Pimple Pink Binary Clock - MicroPython Development$(NC)"
	@echo "$(CYAN)================================================$(NC)"
	@echo ""
	@echo "$(GREEN)Available targets:$(NC)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(YELLOW)%-15s$(NC) %s\n", $$1, $$2}' $(MAKEFILE_LIST)
	@echo ""
	@echo "$(GREEN)Quick start:$(NC)"
	@echo "  1. make deps           # Install dependencies"
	@echo "  3. make monitor        # Monitor serial output"
	@echo "  4. make install        # Install full binary clock"

deps: ## Install Python dependencies
	@echo "$(BLUE)Installing Python dependencies...$(NC)"
	$(PIP) install pyserial adafruit-ampy black flake8
	@echo "$(GREEN)✅ Dependencies installed$(NC)"

download-firmware: ## Download MicroPython firmware
	@echo "$(BLUE)Downloading MicroPython firmware...$(NC)"
	@if [ ! -f $(FIRMWARE_FILE) ]; then \
		curl -L -o $(FIRMWARE_FILE) $(FIRMWARE_URL) || \
		wget -O $(FIRMWARE_FILE) $(FIRMWARE_URL) || \
		$(PYTHON) -c "import urllib.request; urllib.request.urlretrieve('$(FIRMWARE_URL)', '$(FIRMWARE_FILE)')"; \
	else \
		echo "$(GREEN)✅ Firmware already downloaded$(NC)"; \
	fi

flash: download-firmware ## Flash MicroPython firmware to Pico W
	@echo "$(PURPLE)🔧 Flashing MicroPython firmware...$(NC)"
	@echo "$(YELLOW)1. Hold the BOOTSEL button on your Pico W$(NC)"
	@echo "$(YELLOW)2. Connect the Pico W to your computer via USB$(NC)"
	@echo "$(YELLOW)3. Release the BOOTSEL button$(NC)"
	@echo "$(YELLOW)4. The Pico should appear as a USB drive named 'RPI-RP2'$(NC)"
	@echo ""
	@read -p "Press Enter when the Pico W is connected in BOOTSEL mode..."
	@echo "$(BLUE)Looking for Pico drive...$(NC)"
	@if [ -d "/Volumes/RPI-RP2" ]; then \
		cp $(FIRMWARE_FILE) /Volumes/RPI-RP2/; \
		echo "$(GREEN)✅ Firmware flashed (macOS)$(NC)"; \
	elif [ -d "/media/*/RPI-RP2" ]; then \
		cp $(FIRMWARE_FILE) /media/*/RPI-RP2/; \
		echo "$(GREEN)✅ Firmware flashed (Linux)$(NC)"; \
	else \
		echo "$(RED)❌ Cannot find Pico drive. Please copy $(FIRMWARE_FILE) manually to the RPI-RP2 drive$(NC)"; \
	fi
	@echo "$(GREEN)The Pico W should automatically reboot with MicroPython$(NC)"

upload-manual: ## Manual upload with detailed debugging
	@echo "$(BLUE)📁 Manual upload with debugging...$(NC)"
	@echo "$(YELLOW)Device port: $(DEVICE_PORT)$(NC)"
	@echo "$(YELLOW)Testing basic connection...$(NC)"
	@$(PYTHON) -c "import serial; s=serial.Serial('$(DEVICE_PORT)', $(BAUD_RATE), timeout=3); print('Connected:', s.is_open); s.write(b'\\r\\n'); import time; time.sleep(1); response=s.read(1000); print('Response:', repr(response)); s.close()"
	@echo ""
	@echo "$(YELLOW)Stopping running programs...$(NC)"
	@$(PYTHON) -c "import serial; s=serial.Serial('$(DEVICE_PORT)', $(BAUD_RATE), timeout=1); s.write(b'\\x03\\x03\\x04'); s.close()" 2>/dev/null || true
	@sleep 2
	@echo "$(YELLOW)Testing REPL after interrupt...$(NC)"
	@$(PYTHON) -c "import serial; s=serial.Serial('$(DEVICE_PORT)', $(BAUD_RATE), timeout=3); s.write(b'\\r\\n'); import time; time.sleep(1); response=s.read(1000); print('REPL Response:', repr(response)); s.close()"
	@echo ""
	@echo "$(YELLOW)Trying ampy upload...$(NC)"
	@ampy -p $(DEVICE_PORT) put main.py || echo "$(RED)Upload failed$(NC)"

upload: ## Upload Python files to Pico W
	@echo "$(BLUE)📁 Uploading files to Pico W...$(NC)"
	@if [ ! -c $(DEVICE_PORT) ]; then \
		echo "$(YELLOW)⚠️  Device not found at $(DEVICE_PORT)$(NC)"; \
		echo "$(YELLOW)Available devices:$(NC)"; \
		ls /dev/tty* | grep -E "(ACM|USB|usbmodem)" || echo "No USB devices found"; \
		echo "$(YELLOW)Update DEVICE_PORT in Makefile or set it: make upload DEVICE_PORT=/dev/ttyUSB0$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Stopping any running programs...$(NC)"
	@$(PYTHON) -c "import serial; s=serial.Serial('$(DEVICE_PORT)', $(BAUD_RATE), timeout=1); s.write(b'\\x03\\x03\\x04'); s.close()" || true
	@sleep 2
	@for file in $(UPLOAD_FILES); do \
		if [ -f $$file ]; then \
			echo "$(BLUE)Uploading $$file...$(NC)"; \
			uploaded=false; \
			for attempt in 1 2 3; do \
				if ampy -p $(DEVICE_PORT) put $$file; then \
					echo "$(GREEN)✅ Uploaded $$file with ampy$(NC)"; \
					uploaded=true; \
					break; \
				elif command -v mpremote >/dev/null 2>&1 && mpremote connect $(DEVICE_PORT) cp $$file :$$file; then \
					echo "$(GREEN)✅ Uploaded $$file with mpremote$(NC)"; \
					uploaded=true; \
					break; \
				else \
					echo "$(YELLOW)⚠️  Upload attempt $$attempt failed, retrying...$(NC)"; \
					sleep 2; \
				fi; \
			done; \
			if [ "$$uploaded" = "false" ]; then \
				echo "$(RED)❌ Failed to upload $$file after 3 attempts$(NC)"; \
				echo "$(YELLOW)Try manually: ampy -p $(DEVICE_PORT) put $$file$(NC)"; \
				exit 1; \
			fi; \
		else \
			echo "$(RED)❌ File not found: $$file$(NC)"; \
			exit 1; \
		fi; \
	done
	@echo "$(GREEN)🎉 All files uploaded!$(NC)"

install: ## Complete installation (flash + upload + config)
	@echo "$(GREEN)🎉 Installation starting...$(NC)"
	@echo ""
	@echo "$(GREEN)Step 1: Flashing MicroPython firmware$(NC)"
	@$(MAKE) flash
	@echo ""
	@echo "$(GREEN)Step 2: Waiting for device to reboot...$(NC)"
	@echo "$(YELLOW)Waiting 10 seconds for Pico W to reboot and reconnect...$(NC)"
	@sleep 10
	@echo "$(BLUE)Checking if device is ready...$(NC)"
	@for i in 1 2 3; do \
		if [ -c $(DEVICE_PORT) ]; then \
			echo "$(GREEN)✅ Device found at $(DEVICE_PORT)$(NC)"; \
			break; \
		else \
			echo "$(YELLOW)⏳ Waiting for device (attempt $$i/3)...$(NC)"; \
			sleep 5; \
		fi; \
	done
	@if [ ! -c $(DEVICE_PORT) ]; then \
		echo "$(RED)❌ Device not found. Available devices:$(NC)"; \
		ls /dev/tty* | grep -E "(ACM|USB|usbmodem)" || echo "No USB devices found"; \
		echo "$(YELLOW)You may need to update DEVICE_PORT in Makefile$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Testing MicroPython REPL connection...$(NC)"
	@for i in 1 2 3 4 5; do \
		if $(PYTHON) -c "import serial; s=serial.Serial('$(DEVICE_PORT)', $(BAUD_RATE), timeout=2); s.write(b'\\r\\n'); response=s.read(100); s.close(); exit(0 if b'>>>' in response else 1)" 2>/dev/null; then \
			echo "$(GREEN)✅ MicroPython REPL is ready$(NC)"; \
			break; \
		else \
			echo "$(YELLOW)⏳ Waiting for MicroPython REPL (attempt $$i/5)...$(NC)"; \
			sleep 3; \
		fi; \
	done
	@echo ""
	@echo "$(GREEN)Step 3: Uploading Python files$(NC)"
	@$(MAKE) upload
	@echo ""
	@echo "$(GREEN)🎉 Installation complete!$(NC)"
	@echo ""
	@echo "$(GREEN)Next steps:$(NC)"
	@echo "  1. Edit config.py with your WiFi credentials (already done!)"
	@echo "  2. Connect your NeoPixel strip to pin 16"
	@echo "  3. Reset the Pico W to start the clock: make reset"
	@echo "  4. Check serial output for IP address: make monitor"
	@echo "  5. Open the IP address in your web browser"

config: ## Edit configuration file
	@echo "$(BLUE)⚙️  Opening configuration file...$(NC)"
	@if command -v code >/dev/null 2>&1; then \
		code config.py; \
	elif command -v nano >/dev/null 2>&1; then \
		nano config.py; \
	elif command -v vim >/dev/null 2>&1; then \
		vim config.py; \
	else \
		echo "$(YELLOW)Please edit config.py with your preferred editor$(NC)"; \
		echo "$(YELLOW)Set your WiFi credentials and timezone$(NC)"; \
	fi

monitor: ## Monitor serial output from Pico W
	@echo "$(BLUE)📺 Monitoring serial output from $(DEVICE_PORT)...$(NC)"
	@echo "$(YELLOW)Press Ctrl+C to exit$(NC)"
	@if command -v screen >/dev/null 2>&1; then \
		screen $(DEVICE_PORT) $(BAUD_RATE); \
	elif command -v minicom >/dev/null 2>&1; then \
		minicom -D $(DEVICE_PORT) -b $(BAUD_RATE); \
	elif $(PYTHON) -c "import serial" 2>/dev/null; then \
		$(PYTHON) -c "import serial; s=serial.Serial('$(DEVICE_PORT)', $(BAUD_RATE)); \
		print('Connected to $(DEVICE_PORT)'); \
		try: \
			while True: print(s.readline().decode().strip()) \
		except KeyboardInterrupt: \
			s.close()"; \
	else \
		echo "$(RED)❌ No serial monitor available. Install screen, minicom, or pyserial$(NC)"; \
	fi

check-bootloader: ## Check if Pico W is in bootloader mode
	@$(PYTHON) check_bootloader.py

clear-filesystem: ## Clear problematic files from Pico W
	@$(PYTHON) clear_filesystem.py

reset: ## Reset the Pico W (or guide manual reset if needed)
	@echo "$(BLUE)🔄 Resetting Pico W...$(NC)"
	@if [ -c $(DEVICE_PORT) ]; then \
		if $(PYTHON) -c "import serial; s=serial.Serial('$(DEVICE_PORT)', $(BAUD_RATE), timeout=2); s.write(b'\x03\x04'); s.close()" 2>/dev/null; then \
			echo "$(GREEN)✅ Reset signal sent$(NC)"; \
		else \
			echo "$(RED)❌ Device not responding - Manual reset required$(NC)"; \
			echo ""; \
			echo "$(YELLOW)Please follow these steps:$(NC)"; \
			echo "$(BLUE)1. Disconnect the USB cable from your Pico W$(NC)"; \
			echo "$(BLUE)2. Hold down the BOOTSEL button on the Pico W$(NC)"; \
			echo "$(BLUE)3. While holding BOOTSEL, reconnect the USB cable$(NC)"; \
			echo "$(BLUE)4. Release the BOOTSEL button$(NC)"; \
			echo "$(BLUE)5. The Pico W should appear as a USB drive$(NC)"; \
			echo ""; \
			echo "$(GREEN)Then run: make flash$(NC)"; \
			echo "$(GREEN)Followed by: make upload$(NC)"; \
		fi; \
	else \
		echo "$(RED)❌ Device not found at $(DEVICE_PORT)$(NC)"; \
		echo "$(YELLOW)Available devices:$(NC)"; \
		ls /dev/tty* | grep -E "(ACM|USB|usbmodem)" || echo "No USB devices found"; \
	fi

upload-tests: ## Upload test files to Pico W
	@echo "$(BLUE)📁 Uploading test files to $(DEVICE_PORT)...$(NC)"
	@uploaded_count=0; \
	total_files=0; \
	for file in $(TEST_FILES); do \
		if [ -f $$file ]; then \
			total_files=$$((total_files + 1)); \
			echo "$(BLUE)Uploading $$file...$(NC)"; \
			if ampy -p $(DEVICE_PORT) put $$file; then \
				echo "$(GREEN)✅ Uploaded $$file$(NC)"; \
				uploaded_count=$$((uploaded_count + 1)); \
			elif command -v mpremote >/dev/null 2>&1 && mpremote connect $(DEVICE_PORT) cp $$file :$$file; then \
				echo "$(GREEN)✅ Uploaded $$file with mpremote$(NC)"; \
				uploaded_count=$$((uploaded_count + 1)); \
			else \
				echo "$(RED)❌ Failed to upload $$file$(NC)"; \
			fi; \
		else \
			echo "$(RED)❌ File not found: $$file$(NC)"; \
		fi; \
	done; \
	if [ $$uploaded_count -eq $$total_files ] && [ $$total_files -gt 0 ]; then \
		echo "$(GREEN)✅ All $$uploaded_count test files uploaded successfully!$(NC)"; \
		echo "$(GREEN)Available tests:$(NC)"; \
		echo "  - test_leds.py: Test NeoPixel hardware"; \
		echo "  - test_web.py: Test web server"; \
		echo "  - test_binary_time.py: Test binary time display"; \
	elif [ $$uploaded_count -gt 0 ]; then \
		echo "$(YELLOW)⚠️  Partial upload: $$uploaded_count/$$total_files files uploaded$(NC)"; \
		exit 1; \
	else \
		echo "$(RED)❌ No files were uploaded successfully$(NC)"; \
		echo "$(YELLOW)Try: make reset && make upload-tests$(NC)"; \
		exit 1; \
	fi

test: ## Run basic connectivity test
	@echo "$(BLUE)🧪 Testing Pico W connectivity...$(NC)"
	@if [ -c $(DEVICE_PORT) ]; then \
		echo "$(GREEN)✅ Device found at $(DEVICE_PORT)$(NC)"; \
		$(PYTHON) -c "import serial; s=serial.Serial('$(DEVICE_PORT)', $(BAUD_RATE), timeout=1); \
		s.write(b'print(\"Hello from Pico W!\")\r\n'); \
		response = s.read(100); \
		s.close(); \
		print('Response:', response.decode() if response else 'No response')"; \
	else \
		echo "$(RED)❌ Device not found at $(DEVICE_PORT)$(NC)"; \
		echo "$(YELLOW)Available devices:$(NC)"; \
		ls /dev/tty* | grep -E "(ACM|USB|usbmodem)" || echo "No USB devices found"; \
	fi

lint: ## Check code style
	@echo "$(BLUE)🔍 Checking code style...$(NC)"
	@if command -v flake8 >/dev/null 2>&1; then \
		flake8 *.py --max-line-length=88 --ignore=E203,W503; \
		echo "$(GREEN)✅ Linting complete$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  flake8 not found. Install with: pip install flake8$(NC)"; \
	fi

format: ## Format code with black
	@echo "$(BLUE)🎨 Formatting code...$(NC)"
	@if command -v black >/dev/null 2>&1; then \
		black *.py; \
		echo "$(GREEN)✅ Code formatted$(NC)"; \
	else \
		echo "$(YELLOW)⚠️  black not found. Install with: pip install black$(NC)"; \
	fi

clean: ## Clean build artifacts and temporary files
	@echo "$(BLUE)🧹 Cleaning up...$(NC)"
	rm -f $(FIRMWARE_FILE)
	rm -f *.pyc
	rm -rf __pycache__
	rm -rf .pytest_cache
	@echo "$(GREEN)✅ Cleanup complete$(NC)"

backup: ## Backup current files from Pico W
	@echo "$(BLUE)💾 Backing up files from Pico W...$(NC)"
	@mkdir -p backup
	@for file in $(UPLOAD_FILES); do \
		echo "$(BLUE)Backing up $$file...$(NC)"; \
		ampy -p $(DEVICE_PORT) get $$file backup/$$file 2>/dev/null || \
		echo "$(YELLOW)⚠️  Could not backup $$file$(NC)"; \
	done
	@echo "$(GREEN)✅ Backup complete (check backup/ directory)$(NC)"

status: ## Show project status
	@echo "$(CYAN)🕐 Pimple Pink Binary Clock - Status$(NC)"
	@echo "$(CYAN)================================$(NC)"
	@echo ""
	@echo "$(GREEN)Files:$(NC)"
	@for file in $(UPLOAD_FILES); do \
		if [ -f $$file ]; then \
			echo "  $(GREEN)✅ $$file$(NC)"; \
		else \
			echo "  $(RED)❌ $$file$(NC)"; \
		fi; \
	done
	@echo ""
	@echo "$(GREEN)Firmware:$(NC)"
	@if [ -f $(FIRMWARE_FILE) ]; then \
		echo "  $(GREEN)✅ $(FIRMWARE_FILE)$(NC)"; \
	else \
		echo "  $(YELLOW)⚠️  $(FIRMWARE_FILE) (not downloaded)$(NC)"; \
	fi
	@echo ""
	@echo "$(GREEN)Device:$(NC)"
	@if [ -c $(DEVICE_PORT) ]; then \
		echo "  $(GREEN)✅ $(DEVICE_PORT)$(NC)"; \
	else \
		echo "  $(RED)❌ $(DEVICE_PORT) (not found)$(NC)"; \
	fi
	@echo ""
	@echo "$(GREEN)Dependencies:$(NC)"
	@$(PYTHON) -c "import serial" 2>/dev/null && echo "  $(GREEN)✅ pyserial$(NC)" || echo "  $(RED)❌ pyserial$(NC)"
	@command -v ampy >/dev/null 2>&1 && echo "  $(GREEN)✅ ampy$(NC)" || echo "  $(RED)❌ ampy$(NC)"

test-leds: ## Run LED test script
	@echo "$(BLUE)🎨 Running LED test...$(NC)"
	@$(PYTHON) run_test.py test_leds.py $(DEVICE_PORT)

test-web: ## Run web server test
	@echo "$(BLUE)🌐 Running web server test...$(NC)"
	@$(PYTHON) run_test.py test_web.py $(DEVICE_PORT)
	@echo "$(YELLOW)Note: Web server will keep running. Use make reset to stop.$(NC)"

test-binary: ## Run binary time display test
	@echo "$(BLUE)⏰ Running binary time test...$(NC)"
	@$(PYTHON) run_test.py test_binary_time.py $(DEVICE_PORT)

test-main: ## Run main binary clock program
	@echo "$(BLUE)🕐 Running main binary clock...$(NC)"
	@$(PYTHON) run_test.py main.py $(DEVICE_PORT)
	@echo "$(YELLOW)Note: Main program will keep running. Use make reset to stop.$(NC)"

ip: ## Get Pico W IP address
	@echo "$(BLUE)🔍 Getting Pico W IP address...$(NC)"
	@$(PYTHON) get_ip.py $(DEVICE_PORT)

get-ip: ip ## Alias for ip command

# Default target
.DEFAULT_GOAL := help 