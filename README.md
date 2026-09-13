# Cybersecurity Awareness Game — Day-1 Prototype

This is the smallest possible version of the whole system, working end to
end: one password-security scenario, one correct/incorrect branch, a score
that updates in SQLite. It is deliberately ugly. Its only job is to prove
that every layer in your architecture diagram actually talks to the next.

## What's here

```
cybersecurity_game/
├── main.py                    # entry point — run this
├── database/
│   ├── schema.sql              # tables from your class diagram, seeded with 1 scenario
│   └── db.py                   # connects to SQLite, runs schema.sql on first launch
├── models/
│   ├── session.py               # Session class (FR1: start/pause/resume/exit)
│   ├── challenge.py             # Challenge + ResponseOption classes
│   └── score.py                 # Score class
├── logic/
│   ├── scenario_engine.py       # loads challenges — your sequence diagram's "Scenario engine"
│   └── scoring_engine.py        # evaluates responses, records scores — "Scoring engine"
└── ui/
    └── main_window.py           # tkinter window — thin on purpose, swap for PyQt6 later
```

## Requirements

- Python 3.10 or later (check with `python --version` or `python3 --version`)
- Nothing else — `tkinter` and `sqlite3` both ship with standard Python, so
  there is no `pip install` step for this first slice.

## How to run it

Open a terminal in this folder, then:

**Windows:**
```
python main.py
```

**macOS / Linux:**
```
python3 main.py
```

A window should open with one password-security question and two buttons.
Click either one — you'll see feedback appear and the score update. That's
the entire loop working: UI → Scenario engine → Scoring engine → SQLite →
back to UI.

A file called `database/game.db` will be created automatically the first
time you run it. If you ever want to reset to a clean database, just delete
`database/game.db` and run the app again — it rebuilds itself from
`schema.sql`.

## Put this under version control now

Before you add anything else, turn this into a Git repository so your
commit history becomes the evidence of Agile iteration you'll reference
in your appendix:

```
git init
git add .
git commit -m "Initial vertical slice: one scenario, full loop working"
```

Then create an empty repository on GitHub and push:

```
git remote add origin <your-repo-url>
git branch -M main
git push -u origin main
```

## Running the test suite

This project includes an automated test suite (32 tests) covering the model
classes, the scenario engine, the scoring engine, and the seed data itself.
Install pytest once:

```
pip install pytest
```

Then, from inside this folder, run:

```
pytest
```

You should see all tests pass. This is your 4.4.3 (Evaluation and Testing
Techniques) evidence for Chapter Four — you can screenshot the output for
your appendix.

The `tests/test_data_integrity.py` file is worth understanding: it checks
your *content* (seed.sql), not just your code. If you add more scenarios
later, run `pytest` again before trusting them — it will catch things like
a `correct_option_id` that accidentally points at the wrong option.

## What to do next (in order)

1. Get this running and click through it once. Confirm it works before
   changing anything.
2. Add 3–4 more password scenarios to `schema.sql` (copy the `INSERT`
   pattern) so the password module feels like a real module, not one
   question.
3. Add a "Next scenario" flow to `main_window.py` so the user can move
   through several scenarios instead of the window ending after one click.
4. Only once the password module feels complete, start Sprint 2 on your
   Gantt chart: the phishing/social-engineering module. Reuse
   `ScenarioEngine` and `ScoringEngine` as-is — you shouldn't need to touch
   them, only add new challenges and a way to select which module to play.
5. Swap `ui/main_window.py` for a PyQt6 version once the underlying logic
   is proven and you want a more polished interface (addresses NFR1/NFR2).
