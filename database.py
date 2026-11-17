import sqlite3

DB = "recipes.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS favorites (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                image TEXT,
                category TEXT,
                area TEXT
            )
        """)


def add_favorite(id, name, image, category, area):
    with get_conn() as conn:
        conn.execute(
            "INSERT OR IGNORE INTO favorites VALUES (?, ?, ?, ?, ?)",
            (id, name, image, category, area),
        )


def remove_favorite(id):
    with get_conn() as conn:
        conn.execute("DELETE FROM favorites WHERE id = ?", (id,))


def get_favorites():
    with get_conn() as conn:
        return [dict(r) for r in conn.execute("SELECT * FROM favorites")]
