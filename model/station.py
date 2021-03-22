from dataclasses import dataclass

@dataclass
class ConfigStation:
    code: str
    platform: str

@dataclass
class Station:
    name: str
    code: str