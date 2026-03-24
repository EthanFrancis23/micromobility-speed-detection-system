"""

Entry point for application. 
Starts the radar, LCD, and camera services. Then runs the main monitoring loop. 

"""

# Currently only testing LCD startup and idle messages

import time

from src.display.lcd_display import LCDDisplay
from src.camera.capture import CameraCapture

def main() -> None:
    lcd = LCDDisplay()
    lcd.show_startup()
    time.sleep(2)


    lcd.write_lines("Testing Camera", "Say Cheese!")

    camera = CameraCapture()
    image_path = camera.capture_image(prefix="test")

    lcd.write_lines("Image Saved", image_path.name[:16])
    time.sleep(3)

    lcd.show_idle()


if __name__ == "__main__":
    main()