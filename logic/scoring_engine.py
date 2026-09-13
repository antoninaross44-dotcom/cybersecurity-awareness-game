"""Scoring engine — application logic layer.

Evaluates a submitted response and records the resulting score.
This is the component your sequence diagram calls 'Scoring engine'.
"""

from datetime import datetime

from models.challenge import Challenge
from models.score import Score

POINTS_CORRECT = 10
POINTS_INCORRECT = 0


class ScoringEngine:
    def __init__(self, conn):
        self.conn = conn

    def evaluate_and_record(self, session_id: str, challenge: Challenge, selected_option_id: int) -> Score:
        is_correct = challenge.evaluate_response(selected_option_id)
        points = POINTS_CORRECT if is_correct else POINTS_INCORRECT

        score = Score(session_id=session_id, challenge_id=challenge.challenge_id, points=points)

        self.conn.execute(
            "INSERT INTO scores (session_id, challenge_id, points, recorded_at) VALUES (?, ?, ?, ?)",
            (score.session_id, score.challenge_id, score.points, score.recorded_at.isoformat()),
        )
        self.conn.commit()

        return score

    def get_module_performance(self, session_id: str, module_id: int) -> tuple:
        """Return (correct_count, total_answered) for this module, within
        this session only. Used for FR19 (personalised recommendations) —
        a module the user hasn't played yet in this session returns (0, 0).
        """
        row = self.conn.execute(
            """
            SELECT
                COUNT(*) AS total,
                SUM(CASE WHEN scores.points > 0 THEN 1 ELSE 0 END) AS correct
            FROM scores
            JOIN challenges ON challenges.id = scores.challenge_id
            WHERE scores.session_id = ? AND challenges.module_id = ?
            """,
            (session_id, module_id),
        ).fetchone()

        total = row["total"] or 0
        correct = row["correct"] or 0
        return correct, total
