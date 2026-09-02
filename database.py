import sqlite3
from datetime import date, timedelta

DB_PATH = "sentinel.db"
HIGH_RISK_THRESHOLD = 6.0


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


def get_time_slot_stats():
    conn = get_db()
    rows = conn.execute(
        "SELECT time_slot, COUNT(*) as n FROM reports GROUP BY time_slot"
    ).fetchall()
    conn.close()
    return rows


def get_summary_stats():
    """High-level numbers for the top-of-dashboard cards."""
    conn = get_db()
    total = conn.execute("SELECT COUNT(*) as n FROM reports").fetchone()["n"]
    high_risk = conn.execute(
        "SELECT COUNT(*) as n FROM reports WHERE risk_score >= ?",
        (HIGH_RISK_THRESHOLD,),
    ).fetchone()["n"]
    last_7_days = conn.execute(
        "SELECT COUNT(*) as n FROM reports WHERE created_at >= datetime('now', '-7 days')"
    ).fetchone()["n"]
    avg_row = conn.execute("SELECT AVG(risk_score) as avg FROM reports").fetchone()
    avg_score = round(avg_row["avg"], 1) if avg_row["avg"] is not None else 0.0
    conn.close()
    return {
        "total": total,
        "high_risk": high_risk,
        "last_7_days": last_7_days,
        "avg_score": avg_score,
    }


def get_daily_counts(days=14):
    """Zero-filled day-by-day counts for the trend line — last `days` days."""
    conn = get_db()
    rows = conn.execute(
        """
        SELECT strftime('%Y-%m-%d', created_at) as day, COUNT(*) as n
        FROM reports
        WHERE created_at >= datetime('now', ?)
        GROUP BY day
        """,
        (f"-{days} days",),
    ).fetchall()
    conn.close()

    counts = {r["day"]: r["n"] for r in rows}
    today = date.today()
    labels, values = [], []
    for i in range(days - 1, -1, -1):
        d = today - timedelta(days=i)
        labels.append(d.strftime("%d %b"))
        values.append(counts.get(d.isoformat(), 0))
    return labels, values
