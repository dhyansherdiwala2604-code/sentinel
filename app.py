import os
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session

from database import (
    init_db,
    insert_report,
    get_all_reports,
    get_stats,
    get_time_slot_stats,
    get_summary_stats,
    get_daily_counts,
)
from trie_engine import build_trie_from_json, load_phrases, scan_phrases
from risk_engine import compute_risk_score, dominant_category

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "sentinel2026")

trie = build_trie_from_json()
phrases = load_phrases()


def counsellor_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("is_counsellor"):
            return redirect(url_for("dashboard_login"))
        return view(*args, **kwargs)
    return wrapped


@app.route("/")
def report_form():
    return render_template("report.html")


@app.route("/submit", methods=["POST"])
def submit():
    text = request.form.get("concern", "").strip()
    block = request.form.get("hostel_block", "unspecified")
    time_slot = request.form.get("time_slot", "unspecified")

    matches = trie.scan(text) + scan_phrases(text, phrases)
    score, freq = compute_risk_score(matches)
    category = dominant_category(freq)

    insert_report(text, block, time_slot, score, category)
    return render_template("report.html", submitted=True)


@app.route("/dashboard-login", methods=["GET", "POST"])
def dashboard_login():
    if request.method == "POST":
        if request.form.get("password") == DASHBOARD_PASSWORD:
            session["is_counsellor"] = True
            return redirect(url_for("dashboard"))
        return render_template("dashboard_login.html", error=True)
    return render_template("dashboard_login.html", error=False)


@app.route("/dashboard")
@counsellor_required
def dashboard():
    reports = get_all_reports()
    summary = get_summary_stats()

    by_block, by_category = get_stats()
    by_time_slot = get_time_slot_stats()
    daily_labels, daily_values = get_daily_counts()

    block_labels = [r["hostel_block"] or "Unspecified" for r in by_block]
    block_values = [r["n"] for r in by_block]

    category_labels = [r["category"] or "none" for r in by_category]
    category_values = [r["n"] for r in by_category]

    time_slot_labels = [r["time_slot"] or "Unspecified" for r in by_time_slot]
    time_slot_values = [r["n"] for r in by_time_slot]

    return render_template(
        "dashboard.html",
        reports=reports,
        summary=summary,
        block_labels=block_labels,
        block_values=block_values,
        category_labels=category_labels,
        category_values=category_values,
        time_slot_labels=time_slot_labels,
        time_slot_values=time_slot_values,
        daily_labels=daily_labels,
        daily_values=daily_values,
    )


@app.route("/logout")
def logout():
    session.pop("is_counsellor", None)
    return redirect(url_for("report_form"))


@app.route("/helplines")
def helplines():
    return render_template("helplines.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
