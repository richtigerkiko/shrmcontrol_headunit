from dataclasses import dataclass
import uuid
from dataclass_wizard import JSONWizard

@dataclass
class Rule(JSONWizard):
    id: uuid.UUID
    measurement_type: None
    lower_threshold: int
    upper_threshold: int
    lower_critical: int
    upper_critical: int
    force_on: bool
    force_off: bool

@dataclass
class RuleSet(JSONWizard):
    id: uuid.UUID
    name: str
    rules: list[Rule]
    
    
class FallbackRuleSet:
    def __init__(self):
        self.ruleset = RuleSet(
        id=uuid.uuid4(),
        name= "Backup",
        rules=[
            Rule(id=uuid.uuid4(), name="HUMIDITY", lower_critical=80, lower_threshold=90, upper_threshold=94, upper_critical=-1, force_on=False, force_off=False),
            Rule(id=uuid.uuid4(), name="CO2", lower_critical=-1, lower_threshold=450, upper_threshold=550, upper_critical=800, force_on=False, force_off=False),
            Rule(id=uuid.uuid4(), name="WATERLEVEL", lower_critical=10, lower_threshold=15, upper_threshold=-1, upper_critical=-1, force_on=False, force_off=False),
        ]
    )