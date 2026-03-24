"""

Camera capture module.
Takes a photo when the configured speed threshold is exceeded and saves it with a timestamp.

"""

from pathlib import Path
from datetime import datetime
import time

from picamera2 import Picamera2

from src.config.settings import CAPTURE_DIR

class CameraCapture:
    def __init__(self) -> None:
        self.capture_dir = Path(CAPTURE_DIR)
        self.capture_dir.mkdir(parents=True, exist_ok=True)
        self.camera = Picamera2()


    def capture_image(self, prefix: str ="capture") -> Path:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%s")
        file_path = self.capture_dir / f"{prefix}_{timestamp}.jpg"

        config = self.camera.create_still_configuration()
        self.camera.configure(config)
        self.camera.start()
        time.sleep(2)
        self.camera.capture_file(str(file_path))
        self.camera.stop()

        return file_path