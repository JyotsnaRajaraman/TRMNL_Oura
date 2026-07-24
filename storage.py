import json
from pathlib import Path

TOKEN_FILE = Path("tokens.json")


def load_tokens():
    if not TOKEN_FILE.exists():
        return None

    with open(TOKEN_FILE) as f:
        return json.load(f)


def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f, indent=2)
