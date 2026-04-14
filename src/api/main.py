from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from src.database import create_table
from src.database import (
    get_all_events,
    get_events_above_speed,
    get_events_above_threshold,
    get_events_by_location,
)

app = FastAPI(title="Micromobility Speed Detection System")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

BASE_DIR = Path(__file__).resolve().parent.parent.parent
DB_PATH = BASE_DIR / "data" / "events.db"
FRONTEND_DIR = BASE_DIR / "frontend"
CAPTURES_DIR = BASE_DIR / "data" / "captures"

create_table(DB_PATH)

# Serve frontend files like script.js
app.mount("/frontend", StaticFiles(directory=FRONTEND_DIR), name="frontend")

# Serve captured images
app.mount("/captures", StaticFiles(directory=CAPTURES_DIR), name="captures")


def serialize_event(event):
    image_url = None
    if event.image_path:
        image_name = Path(event.image_path).name
        image_url = f"/captures/{image_name}"

    return {
        "id": event.id,
        "timestamp": event.timestamp.isoformat(),
        "speed_mph": event.speed_mph,
        "threshold_value": event.threshold_value,
        "image_path": image_url,
        "location": event.location,
    }


@app.get("/")
def serve_dashboard():
    return FileResponse(FRONTEND_DIR / "index.html")


@app.get("/events")
def read_all_events():
    events = get_all_events(DB_PATH)
    return [serialize_event(event) for event in events]


@app.get("/events/violations")
def read_violations():
    events = get_events_above_threshold(DB_PATH)
    return [serialize_event(event) for event in events]


@app.get("/events/speed/{min_speed}")
def read_events_above_speed(min_speed: float):
    events = get_events_above_speed(min_speed, DB_PATH)
    return [serialize_event(event) for event in events]


@app.get("/events/location/{location}")
def read_events_by_location(location: str):
    events = get_events_by_location(location, DB_PATH)
    return [serialize_event(event) for event in events]