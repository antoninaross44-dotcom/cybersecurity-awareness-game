"""Session model — tracks one play session (FR1: start/pause/resume/exit)."""

import uuid
from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Session:
    session_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    start_time: datetime = field(default_factory=datetime.now)
    total_score: int = 0
    state: str = "idle"  # idle | playing | paused | completed

    def start(self) -> None:
        self.state = "playing"

    def pause(self) -> None:
        if self.state == "playing":
            self.state = "paused"

    def resume(self) -> None:
        if self.state == "paused":
            self.state = "playing"

    def exit(self) -> None:
        self.state = "idle"

    def add_points(self, points: int) -> None:
        self.total_score += points
