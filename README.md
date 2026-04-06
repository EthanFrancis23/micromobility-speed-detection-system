# Raspberry Pi Speed Radar Monitoring System

A real-time speed detection system using a Raspberry Pi and the Speed Radar Click (MIKROE-5869) sensor. This project captures speed data, detects threshold violations, and integrates with a camera and display for monitoring and future dashboard analytics.

---

## Project Overview

This system is designed to:

- Detect object speed using a radar sensor
- Determine direction (approaching or receding)
- Capture images when speed exceeds a threshold
- Display results on an I2C LCD
- Store events for future dashboard visualization

The long-term goal is to deploy this as a sidewalk micromobility monitoring system.

---

## Hardware Components

- Raspberry Pi 5
- Speed Radar Click (MIKROE-5869)
- USB-C connection (sensor to Pi)
- I2C LCD 1602 display (PCF8574, address 0x27)
- Camera module (CSI or USB)
- Power supply

---

## How It Works

1. Radar sensor sends serial data via /dev/ttyUSB0
2. Python reads and parses radar output
3. System determines:
   - Speed (mph)
   - Direction
   - Detection status
4. If speed exceeds threshold:
   - Capture image
   - Store event
5. Display speed and status on LCD

---

## Project Structure

Speed-Radar-Click-Sensor-Implementation/

├── src/  
│   ├── main.py            # Entry point  
│   ├── radar.py           # Radar sensor interface  
│   ├── parser.py          # Parses raw radar data  
│   ├── camera.py          # Image capture logic  
│   ├── display.py         # LCD output  
│   └── models.py          # SpeedEvent model  

├── tests/  
│   └── test_radar.py      # Radar testing script  

├── images/                # Captured images  
├── data/                  # Stored event data (future DB)  
├── requirements.txt       # Raspberry Pi runtime dependencies  
├── requirements-dev.txt   # Windows development dependencies  
└── README.md  

---

## Installation

Clone the repository:

git clone <your-repo-url>  
cd Speed-Radar-Click-Sensor-Implementation  

---

## Environment Setup

Raspberry Pi (Production Environment):

python3 -m venv .venv  
source .venv/bin/activate  
pip install -r requirements.txt  

Windows (Development Environment):

python -m venv .venv  
.\.venv\Scripts\Activate  
python -m pip install -r requirements-dev.txt  

---

## Running the Project

python -m src.main  

Expected output:

Detected: True  
Direction: Approaching  
Speed: 12.5 mph  
Magnitude: -34 dB  

---

## Speed Event Model

SpeedEvent {  
    id: int  
    timestamp: datetime  
    speed_mph: float  
    threshold_value: float  
    image_path: string  
    location: string  
}  

Notes:
- Only threshold violations should generate full events with images  
- Normal detections can be logged optionally without images  

---

## Camera Integration

Captures image when:

speed_mph >= threshold_value  

Images are saved to:

/images/<timestamp>.jpg  

---

## LCD Output

Displays:
- Current speed  
- Detection status  

Future improvements:
- Alert message when threshold exceeded  
- Direction indicator  

---

## Testing

Run radar test:

python src/test_radar.py  

Expected:
- Raw sensor responses  
- Parsed values (speed, direction, magnitude)  

---

## Sensor Communication

The radar communicates using serial commands such as:

- F01, F00  
- R00, R01, R02  
- C00  

Parsed output includes:
- Detection (True or False)  
- Speed bin converted to MPH  
- Direction  
- Signal strength  

References:
https://libstock.mikroe.com/projects/view/5409/speed-radar-click  
https://www.mikroe.com/speed-radar-click  

---

## Dependency Management

This project uses two dependency files to support different environments:

requirements.txt (Raspberry Pi):
Contains full runtime dependencies, including hardware-specific libraries such as:
- picamera2  
- RPi.GPIO  
- lgpio  

These packages are required for deployment but are not compatible with Windows.

requirements-dev.txt (Windows):
Contains development-safe dependencies such as:
- pyserial  
- smbus2  
- RPLCD  
- numpy  
- opencv-python  

This allows development and testing without requiring Raspberry Pi hardware.

---

## Roadmap

Phase 1: Event System  
- Define SpeedEvent schema  
- Store mock events  
- Add database (SQLite or PostgreSQL)  

Phase 2: Detection Logic  
- Real-time radar parsing  
- Speed calculation  
- Improve detection reliability  

Phase 3: Camera Integration  
- Capture on threshold  
- Fix orientation issues  
- Optimize capture timing  

Phase 4: Dashboard  
- Backend API (FastAPI)  
- Event storage and retrieval  
- Image viewer UI  

Phase 5: Deployment  
- Weatherproof enclosure  
- Power system design  
- Multi-sensor network  

---

## Known Issues

- Camera images may appear upside down  
- Occasional "no data received" from radar  
- LCD refresh timing could be improved  
- Detection latency for fast-moving objects  

---

## Future Improvements

- Multi-location support  
- Real-time web dashboard  
- Cloud storage integration  
- Speed violation alerts (LED or buzzer)  
- AI-based object classification  

---

## Author

Built as part of a smart city initiative and ongoing IoT development work.