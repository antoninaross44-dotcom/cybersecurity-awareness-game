"""Challenge and ResponseOption model classes, matching the class diagram."""

from dataclasses import dataclass, field


@dataclass
class ResponseOption:
    option_id: int
    text: str


@dataclass
class Challenge:
    challenge_id: int
    description: str
    correct_option_id: int
    feedback_correct: str
    feedback_incorrect: str
    options: list = field(default_factory=list)  # list[ResponseOption]
    scenario_type: str = "generic"  # generic | email | sms | phone_call | login_page
    display_data: dict = field(default_factory=dict)  # realistic content for the mockup

    def evaluate_response(self, selected_option_id: int) -> bool:
        """Return True if the selected option is the correct one."""
        return selected_option_id == self.correct_option_id

    def feedback_for(self, selected_option_id: int) -> str:
        return self.feedback_correct if self.evaluate_response(selected_option_id) else self.feedback_incorrect
