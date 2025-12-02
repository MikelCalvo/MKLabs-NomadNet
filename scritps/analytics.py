#!/usr/bin/env python3

import json
import os
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List


def _get_log_file() -> str:
    base_dir = os.path.dirname(os.path.abspath(__file__))  # .../MKLabs-NomadNet/scritps
    log_file = os.path.join(base_dir, "..", "pages", "data", "visits.json")
    return os.path.abspath(log_file)


def _load_visits(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        return []
    except (OSError, json.JSONDecodeError):
        return []

    if isinstance(data, list):
        return [e for e in data if isinstance(e, dict)]
    return []


def _format_ts(ts: int) -> str:
    try:
        return datetime.fromtimestamp(ts).strftime("%Y-%m-%d %H:%M:%S")
    except (OSError, OverflowError, ValueError, TypeError):
        return "-"


def print_summary(entries: List[Dict[str, Any]]) -> None:
    if not entries:
        print("No visit data yet (the JSON file is empty or does not exist).")
        return

    stats: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "first_ts": None, "last_ts": None}
    )

    all_timestamps: List[int] = []

    for e in entries:
        page = str(e.get("file", "desconocido"))
        ts = e.get("timestamp")
        if not isinstance(ts, int):
            try:
                ts = int(ts)
            except (TypeError, ValueError):
                ts = None

        stats[page]["count"] += 1

        if ts is not None:
            all_timestamps.append(ts)
            if stats[page]["first_ts"] is None or ts < stats[page]["first_ts"]:
                stats[page]["first_ts"] = ts
            if stats[page]["last_ts"] is None or ts > stats[page]["last_ts"]:
                stats[page]["last_ts"] = ts

    rows = sorted(
        [
            (
                page,
                data["count"],
                data["first_ts"],
                data["last_ts"],
            )
            for page, data in stats.items()
        ],
        key=lambda r: (-r[1], r[0]),
    )

    formatted_rows = []
    for page, count, first_ts, last_ts in rows:
        first_s = _format_ts(first_ts) if first_ts is not None else "-"
        last_s = _format_ts(last_ts) if last_ts is not None else "-"
        formatted_rows.append((page, count, first_s, last_s))

    header_page = "Page"
    header_visits = "Visits"
    header_first = "First visit"
    header_last = "Last visit"

    col_page_width = max(len(header_page), max(len(r[0]) for r in formatted_rows))
    col_visits_width = max(len(header_visits), max(len(str(r[1])) for r in formatted_rows))
    col_first_width = max(len(header_first), max(len(r[2]) for r in formatted_rows))
    col_last_width = max(len(header_last), max(len(r[3]) for r in formatted_rows))

    total_entries = len(entries)
    global_first = min(all_timestamps) if all_timestamps else None
    global_last = max(all_timestamps) if all_timestamps else None

    width = (
        col_page_width + col_visits_width + col_first_width + col_last_width + 8
    )
    divider = "=" * width

    print(divider)
    print("NomadNet visits summary".center(width))
    print(divider)

    header = (
        f"{header_page:<{col_page_width}}  "
        f"{header_visits:>{col_visits_width}}  "
        f"{header_first:<{col_first_width}}  "
        f"{header_last:<{col_last_width}}"
    )
    print(header)
    print("-" * len(header))

    for page, count, first_s, last_s in formatted_rows:
        print(
            f"{page:<{col_page_width}}  "
            f"{count:>{col_visits_width}}  "
            f"{first_s:<{col_first_width}}  "
            f"{last_s:<{col_last_width}}"
        )

    print("-" * len(header))
    print(f"Total records in log: {total_entries}")
    if global_first is not None and global_last is not None:
        print(
            f"Time range: {_format_ts(global_first)}  ->  {_format_ts(global_last)}"
        )
    print(divider)


def main() -> None:
    log_file = _get_log_file()
    entries = _load_visits(log_file)

    print_summary(entries)


if __name__ == "__main__":
    main()


