
from dataclasses import dataclass
import datetime
from enum import IntEnum


class MeasurementType(IntEnum):
    TEMPERATURE = 0
    HUMIDITY = 1
    CO2 = 2
    WATERLEVEL = 3
    PICTURE = 4

@dataclass
class Measurement:
    timestamp: datetime
    measurement_type: MeasurementType
    value: float
    unit: str  # unitsysmbol like °C, %, ppm, ...
