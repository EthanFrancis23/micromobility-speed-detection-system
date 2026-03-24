"""

Radar device interface.
Opens UART connection, sends commands to the Speed Radar Click, and receives sensor data. 

"""

from __future__ import annotations

import serial

from src.config.settings import SERIAL_PORT,BAUD_RATE, SERIAL_TIMEOUT

class RadarSensor:
    def __init__(self):
        self.serial_port = SERIAL_PORT
        self.baud_rate = BAUD_RATE
        self.timeout = SERIAL_TIMEOUT
        self.connection: serial.Serial | None = None

    
    def connect(self) -> None:
        self.connection = serial.Serial(
            port=self.serial_port,
            baudrate=self.baud_rate,
            timeout=self.timeout,
        )

    def disconnect(self) -> None:
        if self.connection and self.conection.is_open:
            self.connection.close()

    def is_connected(self) -> Bool:
        return self.connection is not None and self.connection.is_open

    def read_lines(self) -> bytes:
        if not self.is_connectd():
            raise RuntimeError("Radar serial connection is not open.")
        return self.connection.readline()

    def read_bytes(self,size: int = 64) -> bytes:
        if not self.is_connected():
            raise RuntimeError("Radar serial connection i not open.")
        return self.connection.read(size)

    def write_bytes(self, data: bytes) -> None:
        if not self.is_connected():
            raise RuntimeError("Radar serial connection is not open.")
        self.connection.write(data)
