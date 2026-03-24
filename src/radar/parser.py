"""

Radar response parsing utilities.

Converts raw radar command responses to structured Python data that is usable by the LCD, threshold logic, camera trigger, and dashboard.

"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from src.config.settings import BIN_TO_MPH_FACTOR

@dataclass
class RadarReading:
    detected: bool
    direction: str
    speed_bin: int
    speed_mph: float
    magnitude_db: int
    raw_response: str


def _clean_response(raw_response: str) -> str:
    """
    Normalizing raw radar response into readable string.

    Examples or raw data:
        '@001;076;067'
        '001;076,067'
        '@C00;001;076;067'

    """

    text = raw_response.strip()

    if text.startswith("@"):
        text= text[1:]

    return text.strip()
