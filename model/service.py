import datetime
from dataclasses import dataclass

@dataclass
class Service:
    serviceUid: str
    runDate: datetime.date
    departureTime: str
    destination: str
    expectedTime: str