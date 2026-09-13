"""Unit tests for models/ — pure logic, no database involved.

These test the classes in isolation, the way your class diagram describes
them: Challenge, Session, Score.
"""

from datetime import datetime

from models.challenge import Challenge, ResponseOption
from models.score import Score
from models.session import Session


def _make_challenge(correct_option_id=2):
    return Challenge(
        challenge_id=1,
        description="Test question?",
        correct_option_id=correct_option_id,
        feedback_correct="You got it right.",
        feedback_incorrect="That wasn't it.",
        options=[ResponseOption(1, "Option A"), ResponseOption(2, "Option B")],
    )


class TestChallenge:
    def test_evaluate_response_true_for_correct_option(self):
        challenge = _make_challenge(correct_option_id=2)
        assert challenge.evaluate_response(2) is True

    def test_evaluate_response_false_for_wrong_option(self):
        challenge = _make_challenge(correct_option_id=2)
        assert challenge.evaluate_response(1) is False

    def test_feedback_for_returns_correct_message_when_right(self):
        challenge = _make_challenge(correct_option_id=2)
        assert challenge.feedback_for(2) == "You got it right."

    def test_feedback_for_returns_incorrect_message_when_wrong(self):
        challenge = _make_challenge(correct_option_id=2)
        assert challenge.feedback_for(1) == "That wasn't it."

    def test_defaults_to_generic_scenario_with_no_display_data(self):
        challenge = _make_challenge()
        assert challenge.scenario_type == "generic"
        assert challenge.display_data == {}


class TestSession:
    def test_starts_in_idle_state(self):
        session = Session()
        assert session.state == "idle"

    def test_full_state_lifecycle(self):
        session = Session()
        session.start()
        assert session.state == "playing"
        session.pause()
        assert session.state == "paused"
        session.resume()
        assert session.state == "playing"
        session.exit()
        assert session.state == "idle"

    def test_pause_is_a_no_op_when_not_playing(self):
        session = Session()  # still idle
        session.pause()
        assert session.state == "idle"

    def test_resume_is_a_no_op_when_not_paused(self):
        session = Session()
        session.start()  # now playing, not paused
        session.resume()
        assert session.state == "playing"

    def test_add_points_accumulates_across_calls(self):
        session = Session()
        session.add_points(10)
        session.add_points(10)
        session.add_points(0)
        assert session.total_score == 20

    def test_each_session_gets_a_unique_id(self):
        assert Session().session_id != Session().session_id


class TestScore:
    def test_recorded_at_defaults_to_now_if_not_given(self):
        score = Score(session_id="abc", challenge_id=1, points=10)
        assert isinstance(score.recorded_at, datetime)
