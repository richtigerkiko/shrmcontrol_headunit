
from dataclasses import dataclass
import datetime
from enum import Enum


class MeasurementType(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    CO2 = "co2"
    WATERLEVEL = "water_level"
    PICTURE = "picture"

@dataclass
class Measurement:
    timestamp: datetime
    measurement_type: MeasurementType
    value: float
    unit: str  # unitsysmbol like °C, %, ppm, ...
