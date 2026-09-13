"""Module model class, matching the class diagram."""

from dataclasses import dataclass


@dataclass
class Module:
    module_id: int
    name: str
    type: str
