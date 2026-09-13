"""Shared pytest fixtures.

This file lives at the project root (not inside tests/) so that pytest adds
the project root to sys.path automatically — that's what makes imports like
`from models.challenge import Challenge` work from inside the test files.
"""

import sqlite3
from pathlib import Path

import pytest

ROOT = Path(__file__).parent
SCHEMA_PATH = ROOT / "database" / "schema.sql"
SEED_PATH = ROOT / "database" / "seed.sql"


@pytest.fixture
def db_conn():
    """A fresh, in-memory database seeded exactly like a real first launch,
    completely separate from your real database/game.db save file. Nothing
    a test does here can ever affect your actual game progress."""
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    conn.executescript(SCHEMA_PATH.read_text(encoding="utf-8"))
    conn.executescript(SEED_PATH.read_text(encoding="utf-8"))
    conn.commit()
    yield conn
    conn.close()
