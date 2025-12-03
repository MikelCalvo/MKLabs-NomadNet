#!/usr/bin/env python3

import json
import os
import sys
import time
from typing import Any, Dict, List

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config_loader import get_config


config = get_config()
logo_color = config.get("ui", "logo_color", default="`F00a")
color_reset = config.get("ui", "color_reset", default="`f")
topbar_divider = config.get("ui", "topbar_divider", default="-━")


def get_storage_dir() -> str:
    return config.expand_path("nomadnet", "storage_path")


def get_log_file() -> str:
    return config.expand_path("analytics", "log_file")


def ensure_storage_dir() -> None:
    storage_dir = get_storage_dir()
    try:
        os.makedirs(storage_dir, exist_ok=True)
    except OSError:
        pass


def load_visits() -> List[Dict[str, Any]]:
    log_file = get_log_file()
    try:
        with open(log_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                return data
    except (FileNotFoundError, json.JSONDecodeError, OSError):
        pass
    return []


def save_visits(entries: List[Dict[str, Any]]) -> None:
    log_file = get_log_file()
    try:
        with open(log_file, "w", encoding="utf-8") as f:
            json.dump(entries, f, ensure_ascii=False, indent=2)
    except OSError:
        pass


def register_visit(page: str) -> int:
    ensure_storage_dir()

    entries = load_visits()
    entries.append(
        {
            "timestamp": int(time.time()),
            "file": page,
        }
    )
    save_visits(entries)

    return sum(1 for entry in entries if entry.get("file") == page)


def get_footer(page: str) -> str:
    visits = register_visit(page)

    return (
        f"{logo_color}\n"
        f"{topbar_divider}\n"
        f"{color_reset}\n"
        f"`lVisits to this page (`!{page}`!): {visits}\n"
    )
