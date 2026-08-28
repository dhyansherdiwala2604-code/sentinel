CATEGORY_WEIGHTS = {
    "substance": 1.0,
    "distress": 1.5,      # weighted higher — mental-health urgency
    "distribution": 1.3,
}


def compute_risk_score(matches):
    """
    matches: list of (word, weight, category) from Trie.scan()
    Builds a per-category frequency vector, then dot-products it with
    CATEGORY_WEIGHTS to get a single severity score.
    """
    freq = {}
    for _, weight, category in matches:
        freq[category] = freq.get(category, 0) + weight

    raw_score = sum(freq.get(cat, 0) * w for cat, w in CATEGORY_WEIGHTS.items())
    normalized = min(round(raw_score / 3, 1), 10.0)
    return normalized, freq


def dominant_category(freq):
    if not freq:
        return "none"
    return max(freq, key=freq.get)
