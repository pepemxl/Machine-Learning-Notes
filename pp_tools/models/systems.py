from dataclasses import dataclass


@dataclass
class Version:
    name: str
    description: str
    version: str
    major: int
    minor: int
    patch: int