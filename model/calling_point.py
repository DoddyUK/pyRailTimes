from dataclasses import dataclass

@dataclass
class CallingPoint:
    description: str
    code: str
    arrival: str
    real_arrival: str