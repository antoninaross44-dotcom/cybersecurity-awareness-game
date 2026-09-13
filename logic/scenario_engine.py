"""Scenario engine — application logic layer.

Responsible for loading challenges (and their response options) for a module.
This is the component your sequence diagram calls 'Scenario engine'.
"""

import json

from models.challenge import Challenge, ResponseOption
from models.module import Module


class ScenarioEngine:
    def __init__(self, conn):
        self.conn = conn

    def get_all_modules(self) -> list:
        """Return every module, in order. Used by the home screen (FR2)."""
        rows = self.conn.execute("SELECT id, name, type FROM modules ORDER BY id").fetchall()
        return [Module(module_id=r["id"], name=r["name"], type=r["type"]) for r in rows]

    def get_tips_for_module(self, module_id: int) -> list:
        """Return every tip for a module, in order. Used for FR19
        (personalised recommendations)."""
        rows = self.conn.execute(
            "SELECT tip_text FROM tips WHERE module_id = ? ORDER BY id", (module_id,)
        ).fetchall()
        return [row["tip_text"] for row in rows]

    def get_challenge(self, challenge_id: int) -> Challenge:
        row = self.conn.execute(
            "SELECT * FROM challenges WHERE id = ?", (challenge_id,)
        ).fetchone()

        option_rows = self.conn.execute(
            "SELECT * FROM response_options WHERE challenge_id = ?", (challenge_id,)
        ).fetchall()

        options = [ResponseOption(option_id=r["id"], text=r["text"]) for r in option_rows]

        raw_display_data = row["display_data"]
        display_data = json.loads(raw_display_data) if raw_display_data else {}

        return Challenge(
            challenge_id=row["id"],
            description=row["description"],
            correct_option_id=row["correct_option_id"],
            feedback_correct=row["feedback_correct"],
            feedback_incorrect=row["feedback_incorrect"],
            options=options,
            scenario_type=row["scenario_type"] or "generic",
            display_data=display_data,
        )

    def get_first_challenge_for_module(self, module_id: int) -> Challenge:
        row = self.conn.execute(
            "SELECT id FROM challenges WHERE module_id = ? ORDER BY id LIMIT 1", (module_id,)
        ).fetchone()
        return self.get_challenge(row["id"])

    def get_challenges_for_module(self, module_id: int) -> list:
        """Return every Challenge in a module, in order. Used to let the
        player move through a whole module rather than a single scenario."""
        rows = self.conn.execute(
            "SELECT id FROM challenges WHERE module_id = ? ORDER BY id", (module_id,)
        ).fetchall()
        return [self.get_challenge(row["id"]) for row in rows]
