"""Entry point.

Run this file. It opens a database connection (creating and seeding the
SQLite database on first run), then launches the game window.
"""

from database.db import get_connection
from ui.main_window import GameWindow


def main():
    conn = get_connection()
    app = GameWindow(conn)
    app.mainloop()
    conn.close()


if __name__ == "__main__":
    main()
