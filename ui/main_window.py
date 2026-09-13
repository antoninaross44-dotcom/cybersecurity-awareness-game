"""Presentation layer.

Two screens inside one window: HomeScreen (lists modules — FR2, FR3) and
ModuleScreen (plays through one module's challenges, one at a time, with a
Next button — the same pattern used for every module, not just passwords).
The score shown is cumulative across the whole session (FR9), not per module.
"""

import tkinter as tk

from logic.scenario_engine import ScenarioEngine
from logic.scoring_engine import ScoringEngine
from models.session import Session
from ui.scenario_display import clear_and_render


class GameWindow(tk.Tk):
    """Root window. Owns the session and the shared engines, and swaps
    between screens (HomeScreen / ModuleScreen) inside a single container."""

    def __init__(self, conn):
        super().__init__()
        self.title("Cybersecurity Awareness Game — Prototype")
        self.geometry("600x600")
        self.resizable(False, False)

        self.conn = conn
        self.scenario_engine = ScenarioEngine(conn)
        self.scoring_engine = ScoringEngine(conn)

        self.session = Session()
        self.session.start()

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.show_home()

    def _clear_container(self):
        for widget in self.container.winfo_children():
            widget.destroy()

    def show_home(self):
        self._clear_container()
        HomeScreen(self.container, self)

    def start_module(self, module_id: int, module_name: str):
        self._clear_container()
        ModuleScreen(self.container, self, module_id, module_name)

    def show_recommendations(self):
        self._clear_container()
        RecommendationsScreen(self.container, self)


class HomeScreen(tk.Frame):
    """FR2: display available modules. FR3: let the user select one."""

    def __init__(self, parent, controller: GameWindow):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.controller = controller

        tk.Label(
            self, text="Cybersecurity Awareness Game",
            font=("Arial", 16, "bold")
        ).pack(pady=(30, 4))

        tk.Label(
            self, text=f"Total score: {controller.session.total_score}",
            font=("Arial", 11)
        ).pack(pady=(0, 25))

        tk.Label(self, text="Choose a module:", font=("Arial", 11)).pack(pady=(0, 10))

        modules = controller.scenario_engine.get_all_modules()
        for module in modules:
            row = tk.Frame(self)
            row.pack(pady=6, padx=60, fill="x")

            tk.Label(row, text=module.name, font=("Arial", 12), anchor="w").pack(side="left")

            tk.Button(
                row, text="Play", width=10,
                command=lambda mid=module.module_id, mname=module.name:
                    controller.start_module(mid, mname)
            ).pack(side="right")

        tk.Button(
            self, text="My Recommendations", command=controller.show_recommendations
        ).pack(pady=(25, 0))


class RecommendationsScreen(tk.Frame):
    """FR19: cybersecurity tips based on the modules the user performed
    poorly in, using performance from the CURRENT session only."""

    ACCURACY_THRESHOLD = 0.75  # below this, we show tips for that module

    def __init__(self, parent, controller: GameWindow):
        super().__init__(parent)
        self.pack(fill="both", expand=True)
        self.controller = controller

        top_row = tk.Frame(self)
        top_row.pack(fill="x", padx=20, pady=(16, 4))
        tk.Button(top_row, text="\u2190 Home", command=controller.show_home).pack(side="left")

        tk.Label(
            self, text="My Recommendations", font=("Arial", 16, "bold")
        ).pack(pady=(10, 4))

        tk.Label(
            self, text="Based on how you've played this session",
            font=("Arial", 10), fg="#555555"
        ).pack(pady=(0, 20))

        modules = controller.scenario_engine.get_all_modules()
        any_played = False

        for module in modules:
            correct, total = controller.scoring_engine.get_module_performance(
                controller.session.session_id, module.module_id
            )

            section = tk.Frame(self, highlightbackground="#dddddd", highlightthickness=1)
            section.pack(fill="x", padx=30, pady=8)

            tk.Label(
                section, text=module.name, font=("Arial", 12, "bold"), anchor="w"
            ).pack(fill="x", padx=12, pady=(10, 2))

            if total == 0:
                tk.Label(
                    section, text="Not played yet this session.",
                    font=("Arial", 10, "italic"), fg="#777777", anchor="w"
                ).pack(fill="x", padx=12, pady=(0, 10))
                continue

            any_played = True
            accuracy = correct / total
            tk.Label(
                section, text=f"{correct} / {total} correct ({accuracy:.0%})",
                font=("Arial", 10), anchor="w"
            ).pack(fill="x", padx=12, pady=(0, 6))

            if accuracy < self.ACCURACY_THRESHOLD:
                tips = controller.scenario_engine.get_tips_for_module(module.module_id)
                tk.Label(
                    section, text="Worth reviewing:", font=("Arial", 10, "bold"),
                    fg="#8a1f1f", anchor="w"
                ).pack(fill="x", padx=12, pady=(4, 2))
                for tip in tips:
                    tk.Label(
                        section, text=f"\u2022 {tip}", font=("Arial", 9),
                        wraplength=460, justify="left", anchor="w"
                    ).pack(fill="x", padx=20, pady=(0, 4))
                tk.Label(section, text="", height=1).pack()  # bottom spacing
            else:
                tk.Label(
                    section, text="Good work in this module.", font=("Arial", 10),
                    fg="#1f6b1f", anchor="w"
                ).pack(fill="x", padx=12, pady=(0, 10))

        if not any_played:
            tk.Label(
                self, text="Play at least one module to see personalised recommendations here.",
                font=("Arial", 10, "italic"), fg="#777777", wraplength=460
            ).pack(pady=20)


class ModuleScreen(tk.Frame):
    """Steps through every challenge in one module, one at a time, with a
    Next button, ending on a module-summary screen."""

    def __init__(self, parent, controller: GameWindow, module_id: int, module_name: str):
        super().__init__(parent)
        self.pack(fill="both", expand=True)

        self.controller = controller
        self.module_id = module_id
        self.module_name = module_name

        self.challenges = controller.scenario_engine.get_challenges_for_module(module_id)
        self.current_index = 0
        self.answered = False

        self._build_static_widgets()
        self._render_current_challenge()

    # ---- one-time widget setup -------------------------------------------------

    def _build_static_widgets(self):
        top_row = tk.Frame(self)
        top_row.pack(fill="x", padx=20, pady=(16, 4))

        tk.Button(
            top_row, text="\u2190 Modules", command=self.controller.show_home
        ).pack(side="left")

        self.score_label = tk.Label(top_row, text="", font=("Arial", 10, "bold"))
        self.score_label.pack(side="right")

        tk.Label(self, text=self.module_name, font=("Arial", 13, "bold")).pack(pady=(8, 0))

        self.progress_label = tk.Label(self, text="", font=("Arial", 10), fg="#555555")
        self.progress_label.pack(pady=(0, 10))

        self.mockup_frame = tk.Frame(self)
        self.mockup_frame.pack(fill="x", padx=20)

        self.question_label = tk.Label(
            self, text="", wraplength=510, font=("Arial", 12), justify="left"
        )
        self.question_label.pack(pady=(10, 15), padx=20, anchor="w")

        self.options_frame = tk.Frame(self)
        self.options_frame.pack(fill="x", padx=20)

        self.feedback_label = tk.Label(
            self, text="", wraplength=510, font=("Arial", 11),
            fg="#1a2b4c", justify="left"
        )
        self.feedback_label.pack(pady=15, padx=20, anchor="w")

        self.next_button = tk.Button(
            self, text="Next", width=16, state="disabled", command=self._go_to_next
        )
        self.next_button.pack(pady=10)

    # ---- per-challenge rendering -------------------------------------------------

    def _render_current_challenge(self):
        self.answered = False
        challenge = self.challenges[self.current_index]

        self.progress_label.config(
            text=f"Scenario {self.current_index + 1} of {len(self.challenges)}"
        )
        self.score_label.config(text=f"Score: {self.controller.session.total_score}")
        clear_and_render(self.mockup_frame, challenge)
        self.question_label.config(text=challenge.description)
        self.feedback_label.config(text="")
        self.next_button.config(state="disabled", text="Next")

        for widget in self.options_frame.winfo_children():
            widget.destroy()

        for option in challenge.options:
            btn = tk.Button(
                self.options_frame, text=option.text, width=56, anchor="w",
                wraplength=480, justify="left",
                command=lambda opt_id=option.option_id: self._handle_response(opt_id),
            )
            btn.pack(pady=4, fill="x")

    def _handle_response(self, selected_option_id: int):
        if self.answered:
            return
        self.answered = True

        challenge = self.challenges[self.current_index]

        score = self.controller.scoring_engine.evaluate_and_record(
            self.controller.session.session_id, challenge, selected_option_id
        )
        self.controller.session.add_points(score.points)

        is_correct = challenge.evaluate_response(selected_option_id)
        feedback_text = challenge.feedback_for(selected_option_id)
        prefix = "\u2713 Correct.  " if is_correct else "\u2717 Not quite.  "
        self.feedback_label.config(text=prefix + feedback_text)

        self.score_label.config(text=f"Score: {self.controller.session.total_score}")

        for widget in self.options_frame.winfo_children():
            widget.config(state="disabled")

        is_last = self.current_index == len(self.challenges) - 1
        self.next_button.config(state="normal", text="Finish" if is_last else "Next")

    def _go_to_next(self):
        if self.current_index < len(self.challenges) - 1:
            self.current_index += 1
            self._render_current_challenge()
        else:
            self._show_module_summary()

    # ---- end of module -------------------------------------------------

    def _show_module_summary(self):
        for widget in self.winfo_children():
            widget.destroy()

        tk.Label(self, text="Module complete", font=("Arial", 16, "bold")).pack(pady=(40, 10))

        tk.Label(
            self,
            text=f"{self.module_name}\n\nTotal score across all modules: {self.controller.session.total_score}",
            font=("Arial", 12), justify="center"
        ).pack(pady=10)

        tk.Button(
            self, text="Back to modules", width=18, command=self.controller.show_home
        ).pack(pady=20)
