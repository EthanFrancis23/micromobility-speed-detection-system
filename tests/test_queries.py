from pathlib import Path
from src.database import (
    get_events_by_location,
    get_events_above_speed,
    get_events_above_threshold,
    get_all_events
)

TEST_DB = Path("tests/test_events.db")

print("\n=== ALL EVENTS ===")
for e in get_all_events(TEST_DB):
    print(e)

print("\n=== VIOLATIONS ===")
for e in get_events_above_threshold(TEST_DB):
    print(e)

print("\n=== SPEED >= 15 ===")
for e in get_events_above_speed(15, TEST_DB):
    print(e)

print("\n=== LOCATION: TEST B ===")
for e in get_events_by_location("Test B", TEST_DB):
    print(e)