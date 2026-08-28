import json


class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end = False
        self.weight = 0
        self.category = None


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, weight, category):
        node = self.root
        for ch in word.lower():
            node = node.children.setdefault(ch, TrieNode())
        node.is_end = True
        node.weight = weight
        node.category = category

    def scan(self, text):
        """Return list of (matched_word, weight, category) found in free text."""
        matches = []
        for raw_word in text.lower().split():
            clean = "".join(c for c in raw_word if c.isalnum())
            node = self.root
            found = True
            for ch in clean:
                if ch not in node.children:
                    found = False
                    break
                node = node.children[ch]
            if found and node.is_end:
                matches.append((clean, node.weight, node.category))
        return matches


def build_trie_from_json(path="keywords.json"):
    trie = Trie()
    with open(path) as f:
        data = json.load(f)
    for entry in data:
        trie.insert(entry["word"], entry["weight"], entry["category"])
    return trie
