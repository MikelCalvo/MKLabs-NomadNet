#!/usr/bin/env python3

import json
import os
import time
from typing import List, Dict, Any

# Base directory of the project (one level above "pages")
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")
LOG_FILE = os.path.join(DATA_DIR, "visits.json")


def _ensure_data_dir() -> None:
    try:
        os.makedirs(DATA_DIR, exist_ok=True)
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
    _ensure_data_dir()

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


