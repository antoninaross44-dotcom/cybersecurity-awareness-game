"""Tests for ScoringEngine — the component your sequence diagram calls
'Scoring engine'.
"""

from logic.scenario_engine import ScenarioEngine
from logic.scoring_engine import ScoringEngine


def test_correct_answer_awards_ten_points(db_conn):
    se = ScenarioEngine(db_conn)
    sc = ScoringEngine(db_conn)
    challenge = se.get_challenge(1)

    score = sc.evaluate_and_record("test-session", challenge, challenge.correct_option_id)

    assert score.points == 10


def test_incorrect_answer_awards_zero_points(db_conn):
    se = ScenarioEngine(db_conn)
    sc = ScoringEngine(db_conn)
    challenge = se.get_challenge(1)

    wrong_option_id = next(
        o.option_id for o in challenge.options if o.option_id != challenge.correct_option_id
    )
    score = sc.evaluate_and_record("test-session", challenge, wrong_option_id)

    assert score.points == 0


def test_score_is_actually_written_to_the_database(db_conn):
    se = ScenarioEngine(db_conn)
    sc = ScoringEngine(db_conn)
    challenge = se.get_challenge(1)

    sc.evaluate_and_record("session-xyz", challenge, challenge.correct_option_id)

    row = db_conn.execute(
        "SELECT * FROM scores WHERE session_id = ?", ("session-xyz",)
    ).fetchone()

    assert row is not None
    assert row["points"] == 10
    assert row["challenge_id"] == 1


def test_cumulative_score_across_all_three_modules(db_conn):
    """The same check we ran manually before adding this test suite —
    now it runs automatically every time, instead of by hand."""
    se = ScenarioEngine(db_conn)
    sc = ScoringEngine(db_conn)

    total = 0
    for module in se.get_all_modules():
        for challenge in se.get_challenges_for_module(module.module_id):
            score = sc.evaluate_and_record("full-playthrough", challenge, challenge.correct_option_id)
            total += score.points

    assert total == 120  # 3 modules x 4 challenges x 10 points, all correct


def test_module_performance_is_zero_zero_before_playing(db_conn):
    sc = ScoringEngine(db_conn)
    correct, total = sc.get_module_performance("unused-session", module_id=1)
    assert (correct, total) == (0, 0)


def test_module_performance_tracks_correct_and_incorrect_separately(db_conn):
    """FR19 depends on this being accurate: 1 right, 1 wrong should report
    exactly (1, 2), not (2, 2) or (0, 2)."""
    se = ScenarioEngine(db_conn)
    sc = ScoringEngine(db_conn)

    challenges = se.get_challenges_for_module(1)
    right_challenge = challenges[0]
    wrong_challenge = challenges[1]
    wrong_option = next(
        o.option_id for o in wrong_challenge.options
        if o.option_id != wrong_challenge.correct_option_id
    )

    sc.evaluate_and_record("perf-session", right_challenge, right_challenge.correct_option_id)
    sc.evaluate_and_record("perf-session", wrong_challenge, wrong_option)

    correct, total = sc.get_module_performance("perf-session", module_id=1)
    assert (correct, total) == (1, 2)


def test_module_performance_only_counts_the_given_session(db_conn):
    """Two different sessions playing the same module should not mix scores."""
    se = ScenarioEngine(db_conn)
    sc = ScoringEngine(db_conn)
    challenge = se.get_challenge(1)

    sc.evaluate_and_record("session-A", challenge, challenge.correct_option_id)

    correct_a, total_a = sc.get_module_performance("session-A", module_id=1)
    correct_b, total_b = sc.get_module_performance("session-B", module_id=1)

    assert (correct_a, total_a) == (1, 1)
    assert (correct_b, total_b) == (0, 0)
