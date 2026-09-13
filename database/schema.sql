-- Structure only. This is safe to run on every launch: CREATE TABLE IF NOT EXISTS
-- means it never touches tables that already exist, so it never duplicates data.

CREATE TABLE IF NOT EXISTS modules (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS challenges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    correct_option_id INTEGER,
    feedback_correct TEXT,
    feedback_incorrect TEXT,
    scenario_type TEXT NOT NULL DEFAULT 'generic',
    display_data TEXT,
    FOREIGN KEY (module_id) REFERENCES modules(id)
);

CREATE TABLE IF NOT EXISTS response_options (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    challenge_id INTEGER NOT NULL,
    text TEXT NOT NULL,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
);

CREATE TABLE IF NOT EXISTS scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    challenge_id INTEGER NOT NULL,
    points INTEGER NOT NULL,
    recorded_at TEXT NOT NULL,
    FOREIGN KEY (challenge_id) REFERENCES challenges(id)
);

CREATE TABLE IF NOT EXISTS tips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    module_id INTEGER NOT NULL,
    tip_text TEXT NOT NULL,
    FOREIGN KEY (module_id) REFERENCES modules(id)
);
