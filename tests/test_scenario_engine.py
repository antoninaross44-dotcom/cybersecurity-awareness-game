"""Tests for ScenarioEngine — the component your sequence diagram calls
'Scenario engine'. Uses the db_conn fixture from conftest.py, which seeds a
throwaway in-memory copy of your real database schema and seed data.
"""

from logic.scenario_engine import ScenarioEngine


def test_get_all_modules_returns_all_three(db_conn):
    se = ScenarioEngine(db_conn)
    modules = se.get_all_modules()
    names = {m.name for m in modules}

    assert len(modules) == 3
    assert names == {
        "Password & Account Security",
        "Phishing & Social Engineering",
        "Quizzes & Decision Challenges",
    }


def test_every_module_has_four_challenges(db_conn):
    se = ScenarioEngine(db_conn)
    for module in se.get_all_modules():
        challenges = se.get_challenges_for_module(module.module_id)
        assert len(challenges) == 4, f"{module.name} should have 4 challenges, has {len(challenges)}"


def test_password_module_challenges_use_generic_display(db_conn):
    se = ScenarioEngine(db_conn)
    for challenge in se.get_challenges_for_module(1):
        assert challenge.scenario_type == "generic"
        assert challenge.display_data == {}


def test_phishing_module_has_one_of_each_realistic_scenario_type(db_conn):
    se = ScenarioEngine(db_conn)
    expected_types = {"email", "sms", "phone_call", "login_page"}

    seen_types = set()
    for challenge in se.get_challenges_for_module(2):
        assert challenge.scenario_type in expected_types
        assert challenge.display_data, f"challenge {challenge.challenge_id} has empty display_data"
        seen_types.add(challenge.scenario_type)

    assert seen_types == expected_types


def test_email_scenario_has_the_fields_the_renderer_needs(db_conn):
    """If this breaks, the email mockup in the UI will silently show blanks."""
    se = ScenarioEngine(db_conn)
    email_challenges = [
        c for c in se.get_challenges_for_module(2) if c.scenario_type == "email"
    ]
    assert len(email_challenges) == 1

    data = email_challenges[0].display_data
    for key in ("from_name", "from_address", "subject", "body"):
        assert key in data, f"email display_data missing '{key}'"


def test_login_page_scenario_has_the_fields_the_renderer_needs(db_conn):
    se = ScenarioEngine(db_conn)
    login_challenges = [
        c for c in se.get_challenges_for_module(2) if c.scenario_type == "login_page"
    ]
    assert len(login_challenges) == 1

    data = login_challenges[0].display_data
    for key in ("url", "page_title", "logo_text"):
        assert key in data, f"login_page display_data missing '{key}'"


def test_every_challenge_has_at_least_two_options(db_conn):
    se = ScenarioEngine(db_conn)
    for module in se.get_all_modules():
        for challenge in se.get_challenges_for_module(module.module_id):
            assert len(challenge.options) >= 2, (
                f"challenge {challenge.challenge_id} has fewer than 2 options"
            )


def test_every_module_has_at_least_one_tip(db_conn):
    """FR19 needs at least one tip per module to show a recommendation."""
    se = ScenarioEngine(db_conn)
    for module in se.get_all_modules():
        tips = se.get_tips_for_module(module.module_id)
        assert len(tips) > 0, f"'{module.name}' has no tips for FR19 recommendations"
