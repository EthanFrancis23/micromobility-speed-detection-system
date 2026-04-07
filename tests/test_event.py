from pathlib import Path
from datetime import datetime
from src.models.speed_event_model import SpeedEvent
from src.database import create_table, insert_event, get_all_events

TEST_DB = Path("tests/test_events.db")


def main():
    create_table(TEST_DB)

    events = [
        SpeedEvent(1, datetime.now(), 12.4, 15.0, None, "Test A"),
        SpeedEvent(2, datetime.now(), 18.7, 15.0, "img2.jpg", "Test B"),
        SpeedEvent(3, datetime.now(), 16.2, 20.0, None, "Test C"),
        SpeedEvent(4, datetime.now(), 22.5, 20.0, "img4.jpg", "Test D"),
    ]

    for event in events:
        insert_event(event, TEST_DB)

    saved = get_all_events(TEST_DB)

    for e in saved:
        print(e)


if __name__ == "__main__":
    main()