#!/usr/bin/env python3

import json
import os
import time
from typing import List, Dict, Any

# NomadNet storage path for analytics
STORAGE_DIR = os.path.expanduser("~/.nomadnetwork/storage")
LOG_FILE = os.path.join(STORAGE_DIR, "pages_analytics.json")


def _ensure_storage_dir() -> None:
    try:
        os.makedirs(STORAGE_DIR, exist_ok=True)
    except OSError:
        pass


def _load_visits() -> List[Dict[str, Any]]:
    try:
        with open(LOG_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return []


def _save_visits(entries: List[Dict[str, Any]]) -> None:
    try:
        with open(LOG_FILE, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except OSError:
        # If we can't write, just ignore persistence errors.
        pass


def _register_visit(page: str) -> int:
    _ensure_storage_dir()

    entries = _load_visits()
    entries.append(
        {
            "timestamp": int(time.time()),
            "file": page,
        }
    )
    _save_visits(entries)

    return sum(1 for e in entries if e.get("file") == page)


def get_footer(page: str) -> str:
    visits = _register_visit(page)

    return (
        "`F00a\n"
        "-━\n"
        "`f\n"
        f"`lVisits to this page (`!{page}`!): {visits}\n"
    )


