# SENTINEL — Setup Instructions

## First-time setup

python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py

Then open http://127.0.0.1:5000 in your browser.

## What each file does

- `app.py` — Flask routes (report form, submit, dashboard, helplines)
- `database.py` — SQLite setup and queries (no identity fields, by design)
- `trie_engine.py` — Trie-based keyword matcher (your DSA piece) + phrase-level scan for multi-word crisis language
- `risk_engine.py` — weighted risk scoring via dot product (your linear algebra piece)
- `keywords.json` — 81 single-word terms across substance / distress / distribution
- `phrases.json` — multi-word escalation phrases (e.g. "no way out") the Trie alone can't catch
- `templates/` — the three pages (report form, dashboard, helplines)
- `static/style.css` — styling

## Before your demo

- Keyword and phrase dictionaries expanded and reviewed for false-positive risk — done.
- Edit `templates/helplines.html` and fill in your actual campus counselling cell contact.
- Submit a few test reports (mix of mild/concerning/urgent language) so your dashboard isn't empty when judges look at it.
- Everything has been tested end-to-end (form → Trie + phrase scan → risk score → SQLite → dashboard) and works out of the box.
