from pathlib import Path

from src.database import (
    get_all_events,
    get_events_above_speed,
    get_events_above_threshold,
    get_events_by_location,
)

TEST_DB = Path("tests/test_events.db")


def main() -> None:
    print("\n=== ALL EVENTS ===")
    for event in get_all_events(TEST_DB):
        print(event)

    print("\n=== VIOLATIONS ===")
    for event in get_events_above_threshold(TEST_DB):
        print(event)

    print("\n=== SPEED >= 15 ===")
    for event in get_events_above_speed(15, TEST_DB):
        print(event)

    print("\n=== LOCATION: TEST B ===")
    for event in get_events_by_location("Test B", TEST_DB):
        print(event)


if __name__ == "__main__":
    main()
