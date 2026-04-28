# Raspberry Pi Speed Radar Monitoring System

A real-time speed detection system for Raspberry Pi using the Speed Radar Click (MIKROE-5869), Pi camera, and I2C LCD. The system reads radar data, converts it into speed readings, captures burst images for threshold violations, stores events in SQLite, and serves a dashboard/API with FastAPI.

---

## Features

- Read radar target packets over serial (`/dev/ttyUSB0`)
- Parse detection state, direction, speed bin, and magnitude
- Convert speed bins to mph using configurable factor
- Show live status/speed/alerts on 16x2 I2C LCD
- Capture burst image frames when speed threshold is exceeded
- Store violation events with image paths in SQLite
- View events and image galleries in a browser dashboard

---

## Hardware Components

- Raspberry Pi 5
- Speed Radar Click (MIKROE-5869)
- I2C LCD 1602 (PCF8574, default address `0x27`)
- Raspberry Pi camera (Picamera2/libcamera compatible)
- USB serial connection for radar (`/dev/ttyUSB0`)

> Note: hardware assumptions (serial port, I2C address, thresholds) are currently defined in `src/config/settings.py`.

---

## Repository Structure

```text
micromobility-speed-detection-system/
├── frontend/
│   ├── index.html
│   ├── script.js
│   └── style.css
├── src/
│   ├── main.py                      # Sensor loop entrypoint
│   ├── database.py                  # SQLite access helpers
│   ├── config/settings.py           # Runtime settings/constants
│   ├── radar/
│   │   ├── radar.py                 # Serial radar interface
│   │   └── parser.py                # C00 parser + conversion
│   ├── camera/capture.py            # Picamera2 capture helpers
│   ├── display/lcd_display.py       # LCD output wrapper
│   ├── logic/violation_handler.py   # Event creation/persistence
│   └── api/
│       ├── main.py                  # FastAPI app
│       ├── routes/events.py         # /events endpoint
│       └── schemas/event.py         # API response schema
├── tests/
├── requirements.txt
└── README.md
```

---

## Installation

### 1) Clone repository

```bash
git clone <your-repo-url>
cd micromobility-speed-detection-system
```

### 2) Create and activate virtual environment

Linux/macOS (including Raspberry Pi OS):

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3) Install dependencies

```bash
pip install -r requirements.txt
```

---

## Configuration

Runtime configuration lives in `src/config/settings.py`:

- radar serial settings (`SERIAL_PORT`, `BAUD_RATE`, `SERIAL_TIMEOUT`)
- LCD settings (`LCD_I2C_ADDRESS`, `LCD_COLS`, `LCD_ROWS`)
- threshold/cooldown settings
- storage paths (`data/events.db`, `data/captures`)

---

## Running the Project

### A) Hardware monitoring loop (radar + LCD + camera)

```bash
python -m src.main
```

### B) API + dashboard (FastAPI)

```bash
uvicorn src.api.main:app --host 0.0.0.0 --port 8000 --reload
```

Then open:

- Dashboard UI: `http://<pi-ip>:8000/`
- Events API: `http://<pi-ip>:8000/events`

---

## Data Model

Stored event fields:

- `id`
- `timestamp`
- `speed_mph`
- `threshold_value`
- `image_paths` (list of relative capture paths)
- `location`

---

## Testing

Run tests with:

```bash
pytest -q
```

Current tests include parser/database/integration scaffolding and utility scripts under `tests/`.

---

## Sensor Commands

The radar interface uses commands such as:

- `$F01` (device type)
- `$F00` (firmware)
- `$C00` (target data)

---

## Notes and Limitations

- Speed conversion factor (`BIN_TO_MPH_FACTOR`) is currently provisional and should be calibrated per deployment.
- Camera and LCD libraries require compatible Raspberry Pi hardware/runtime.
- Captured images are served by the API from `/captures`.
