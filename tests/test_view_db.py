from pathlib import Path

from src.database import get_all_events

TEST_DB = Path("tests/test_events.db")


def main() -> None:
    events = get_all_events(TEST_DB)

    print("\n=== EVENTS IN DATABASE ===\n")

    for event in events:
        print(f"ID: {event.id}")
        print(f"Time: {event.timestamp}")
        print(f"Speed: {event.speed_mph} mph")
        print(f"Threshold: {event.threshold_value} mph")
        print(f"Images: {event.image_paths}")
        print(f"Location: {event.location}")
        print("-" * 30)


if __name__ == "__main__":
    main()
