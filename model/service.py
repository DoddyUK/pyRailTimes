from dataclasses import dataclass

@dataclass
class Service:
    departureTime: str
    destination: str
    expectedTime: str