from dataclasses import dataclass
from enum import IntEnum

class AlarmType(IntEnum):
    Info = 0
    Warning = 1
    Critical = 2


@dataclass 
class Alarm:
    AlarmType: AlarmType
    Message: str
    