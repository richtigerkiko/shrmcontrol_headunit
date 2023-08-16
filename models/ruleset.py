from dataclasses import dataclass
from click import UUID

@dataclass
class Rule:
    id: UUID
    measurement_type: None
    lower_threshold: int
    upper_threshold: int
    lower_critical: int
    upper_critical: int
    force_on: bool
    force_off: bool

@dataclass
class RuleSet:
    id: UUID
    name: str
    rules: list[Rule]