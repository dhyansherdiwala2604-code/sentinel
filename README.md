# SENTINEL — Setup Instructions

## First-time setup
```bash
python3 -m venv venv
source venv/bin/activate       # Windows: venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

Then open http://127.0.0.1:5000 in your browser.

## What each file does
- `app.py` — Flask routes (report form, submit, dashboard, helplines)
- `database.py` — SQLite setup and queries (no identity fields, by design)
- `trie_engine.py` — Trie-based keyword matcher (your DSA piece)
- `risk_engine.py` — weighted risk scoring via dot product (your linear algebra piece)
- `keywords.json` — starter keyword dictionary; expand this with your team
- `templates/` — the three pages (report form, dashboard, helplines)
- `static/style.css` — styling

## Before your demo
- Edit `templates/helplines.html` and fill in your actual campus counselling cell contact.
- Expand `keywords.json` with more terms as a team — keep the weight scale consistent (1-2 mild, 3-4 concerning, 5+ urgent).
- Submit a few test reports so your dashboard isn't empty when judges look at it.
- Everything has already been tested end-to-end (form → Trie → risk score → SQLite → dashboard) and works out of the box.
