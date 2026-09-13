"""Data integrity tests.

These don't test your code so much as your CONTENT — seed.sql. They exist
because every id in seed.sql (correct_option_id especially) was computed by
hand while writing it, and that's exactly the kind of thing that's easy to
get subtly wrong and hard to notice just by playing the app once.

If you add more scenarios later, run this file again before trusting them.
"""

from logic.scenario_engine import ScenarioEngine


def test_every_module_has_at_least_one_challenge(db_conn):
    se = ScenarioEngine(db_conn)
    for module in se.get_all_modules():
        challenges = se.get_challenges_for_module(module.module_id)
        assert len(challenges) > 0, f"'{module.name}' has no challenges at all"


def test_every_challenges_correct_option_id_belongs_to_itself(db_conn):
    """The most important test in this file. Catches a correct_option_id
    that was accidentally copied from a different challenge — the game
    would still run, but would silently mark every answer wrong (or right)
    for that scenario, and nothing in the UI would tell you."""
    se = ScenarioEngine(db_conn)
    for module in se.get_all_modules():
        for challenge in se.get_challenges_for_module(module.module_id):
            option_ids = [o.option_id for o in challenge.options]
            assert challenge.correct_option_id in option_ids, (
                f"Challenge {challenge.challenge_id} ('{challenge.description}') "
                f"has correct_option_id={challenge.correct_option_id}, but its own "
                f"options are {option_ids}. This scenario is currently unwinnable "
                f"or auto-correct."
            )


def test_no_challenge_has_duplicate_option_text(db_conn):
    se = ScenarioEngine(db_conn)
    for module in se.get_all_modules():
        for challenge in se.get_challenges_for_module(module.module_id):
            texts = [o.text for o in challenge.options]
            assert len(texts) == len(set(texts)), (
                f"Challenge {challenge.challenge_id} has two identical-looking options"
            )


def test_every_challenge_has_non_empty_feedback_for_both_outcomes(db_conn):
    se = ScenarioEngine(db_conn)
    for module in se.get_all_modules():
        for challenge in se.get_challenges_for_module(module.module_id):
            assert challenge.feedback_correct and challenge.feedback_correct.strip(), (
                f"Challenge {challenge.challenge_id} is missing 'correct' feedback text"
            )
            assert challenge.feedback_incorrect and challenge.feedback_incorrect.strip(), (
                f"Challenge {challenge.challenge_id} is missing 'incorrect' feedback text"
            )


def test_total_challenge_count_matches_expected_twelve(db_conn):
    """A simple tripwire: if this number ever changes unexpectedly, it means
    content was added or lost somewhere without anyone noticing."""
    se = ScenarioEngine(db_conn)
    total = sum(
        len(se.get_challenges_for_module(m.module_id)) for m in se.get_all_modules()
    )
    assert total == 12
