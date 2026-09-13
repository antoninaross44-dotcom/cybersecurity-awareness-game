"""Database connection helper.

Creates the SQLite database file (if it doesn't exist yet), runs schema.sql
against it, and seeds it with starting data — but ONLY the first time the
database is created. This matters: schema.sql is safe to re-run every launch
(CREATE TABLE IF NOT EXISTS), but seed.sql is not — running its INSERTs twice
would duplicate every scenario. So seed.sql only runs when there was no
database file at all before this call.
"""

import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "game.db"
SCHEMA_PATH = Path(__file__).parent / "schema.sql"
SEED_PATH = Path(__file__).parent / "seed.sql"


def get_connection() -> sqlite3.Connection:
    """Return a SQLite connection, initialising the schema (and seed data
    on first run only) if needed."""
    is_new = not DB_PATH.exists()

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")

    # Structure: always safe to re-run.
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        conn.executescript(f.read())
    conn.commit()

    # Seed data: only run once, when the database is first created.
    if is_new:
        with open(SEED_PATH, "r", encoding="utf-8") as f:
            conn.executescript(f.read())
        conn.commit()

    return conn
