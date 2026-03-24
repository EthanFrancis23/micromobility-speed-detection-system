"""

Entry point for application. 
Starts the radar, LCD, and camera services. Then runs the main monitoring loop. 

"""

# Currently only testing LCD startup and idle messages

import time

from src.display.lcd_display import LCDDisplay
from src.camera.capture import CameraCapture
from src.radar.radar import RadarSensor

def send_and_print(radar: RadarSensor, cmd: str) -> None:
    radar.write_bytes(cmd.encode("ascii"))
    time.sleep(0.2)
    raw = radar.read_bytes(128)
    if raw:
        print(f"{cmd.strip()} -> {raw!r}")
    else:
        print(f"{cmd.strip()} -> No Response")



def main() -> None:
    lcd = LCDDisplay()
    radar = RadarSensor()

    try: 
        lcd.show_startup()
        time.sleep(1)

        lcd.write_lines("Connecting...", "Radar UUSB")
        radar.connect()
        time.sleep(1)

        lcd.write_lines("Radar Connected", "Check Terminal")

        # Basic identification
        send_and_print(radar, "$F01\r")
        send_and_print(radar, "$F00\r")

        # Poll repeatedly while moving your hand in front of radar
        for _ in range(20):
            send_and_print(radar, "$R00\r")
            send_and_print(radar, "$R01\r")
            send_and_print(radar, "$R02\r")
            send_and_print(radar, "$C00\r")
            time.sleep(0.5)

        lcd.write_lines("Radar Test Done", "Check Terminal")
        time.sleep(2)
        lcd.show_idle()

    except Exception as exc:
        print(f"Radar test error: {exc}")
        lcd.write_lines("Radar Error", str(exc)[:16])
        time.sleep(3)


    finally:
        radar.disconnect()

        # camera = CameraCapture()
        # image_path = camera.capture_image(prefix="test")

        # lcd.write_lines("Image Saved", image_path.name[:16])
        # time.sleep(3)

        # lcd.show_idle()


if __name__ == "__main__":
    main()