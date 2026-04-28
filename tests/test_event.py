from src.database import create_table
from src.logic.violation_handler import ViolationHandler


def main() -> None:
    create_table()
    handler = ViolationHandler(threshold_mph=15.0, location="Bench Test")
    event = handler.save_event(18.7, image_paths=[])
    print(event)


if __name__ == "__main__":
    main()
