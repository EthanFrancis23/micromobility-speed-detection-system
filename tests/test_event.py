from datetime import datetime
from src.models.speed_event_model import SpeedEvent

event1 = SpeedEvent(
    id=1, 
    timestamp=datetime.now(),
    speed_mph=12.5,
    threshold_value=15.0,
    image_path=None,
    location="Test Location"
)

print(event1)