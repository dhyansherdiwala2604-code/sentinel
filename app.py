from flask import Flask, render_template, request

from database import init_db, insert_report, get_all_reports, get_stats
from trie_engine import build_trie_from_json, load_phrases, scan_phrases
from risk_engine import compute_risk_score, dominant_category

app = Flask(__name__)
trie = build_trie_from_json()
phrases = load_phrases()


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


@app.route("/dashboard")
def dashboard():
    reports = get_all_reports()
    by_block, by_category = get_stats()
    return render_template(
        "dashboard.html", reports=reports, by_block=by_block, by_category=by_category
    )


@app.route("/helplines")
def helplines():
    return render_template("helplines.html")


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
