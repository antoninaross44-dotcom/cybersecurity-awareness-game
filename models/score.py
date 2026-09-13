"""Score model class, matching the class diagram."""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Score:
    session_id: str
    challenge_id: int
    points: int
    recorded_at: datetime = None

    def __post_init__(self):
        if self.recorded_at is None:
            self.recorded_at = datetime.now()
