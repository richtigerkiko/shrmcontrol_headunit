
from dataclasses import dataclass
import datetime
from enum import Enum


class MeasurementType(Enum):
    TEMPERATURE = "temperature"
    HUMIDITY = "humidity"
    CO2 = "co2"
    WaterLevel = "water_level"
    Picture = "picture"

@dataclass
class Measurement:
    timestamp: datetime
    measurement_type: MeasurementType
    value: float
    unit: str  # unitsysmbol like °C, %, ppm, ...
