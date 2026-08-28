import sqlite3

DB_PATH = "sentinel.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            hostel_block TEXT,
            time_slot TEXT,
            risk_score REAL,
            category TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def insert_report(text, block, time_slot, risk_score, category):
    conn = get_db()
    conn.execute(
        "INSERT INTO reports (text, hostel_block, time_slot, risk_score, category) "
        "VALUES (?, ?, ?, ?, ?)",
        (text, block, time_slot, risk_score, category),
    )
    conn.commit()
    conn.close()


def get_all_reports():
    conn = get_db()
    rows = conn.execute(
        "SELECT * FROM reports ORDER BY risk_score DESC, created_at DESC"
    ).fetchall()
    conn.close()
    return rows


def get_stats():
    """Aggregate counts for the dashboard bars — no identity data involved."""
    conn = get_db()
    by_block = conn.execute(
        "SELECT hostel_block, COUNT(*) as n FROM reports GROUP BY hostel_block"
    ).fetchall()
    by_category = conn.execute(
        "SELECT category, COUNT(*) as n FROM reports GROUP BY category"
    ).fetchall()
    conn.close()
    return by_block, by_category
