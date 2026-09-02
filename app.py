import os
import time
from functools import wraps

from flask import Flask, render_template, request, redirect, url_for, session

from database import init_db, insert_report, get_all_reports, get_stats
from trie_engine import build_trie_from_json, load_phrases, scan_phrases
from risk_engine import compute_risk_score, dominant_category

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev-secret-change-me")
DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "sentinel2026")
SUBMIT_COOLDOWN_SECONDS = 600  # 10 minutes between submissions, per browser session

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
    # Honeypot: real users never see or fill this hidden field. If it's
    # filled, it's almost certainly a bot — pretend success, discard silently.
    if request.form.get("website", "").strip():
        return render_template("report.html", submitted=True)

    # Anonymous cooldown: just a timestamp in this browser's own session,
    # no identity involved. Slows down rapid repeat submissions from one
    # browser without needing logins, CAPTCHAs, or IP tracking.
    last_submit = session.get("last_submit")
    now = time.time()
    if last_submit and (now - last_submit) < SUBMIT_COOLDOWN_SECONDS:
        wait_left = int(SUBMIT_COOLDOWN_SECONDS - (now - last_submit))
        return render_template("report.html", throttled=True, wait_left=wait_left)

    text = request.form.get("concern", "").strip()
    block = request.form.get("hostel_block", "unspecified")
    time_slot = request.form.get("time_slot", "unspecified")

    matches = trie.scan(text) + scan_phrases(text, phrases)
    score, freq = compute_risk_score(matches)
    category = dominant_category(freq)

    insert_report(text, block, time_slot, score, category)
    session["last_submit"] = now
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
    by_block, by_category = get_stats()
    return render_template(
        "dashboard.html", reports=reports, by_block=by_block, by_category=by_category
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
