from datetime import datetime
import socket

from models.measurement import Measurement


class PostMeasurementObj:

    def __init__(self, measurements: list[Measurement]) -> None:
        self.timeStamp = datetime.now()
        self.headunitHostname = socket.gethostname()
        self.measurements = measurements
        pass
    