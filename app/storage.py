import json
from pathlib import Path


DATA_PATH = Path("data/preferences.json")


def load_preferences() -> dict:
    if not DATA_PATH.exists():
        return {}
    return json.loads(DATA_PATH.read_text(encoding="utf-8"))


def save_preferences(preferences: dict) -> None:
    DATA_PATH.parent.mkdir(parents=True, exist_ok=True)
    DATA_PATH.write_text(json.dumps(preferences, ensure_ascii=False, indent=2), encoding="utf-8")
