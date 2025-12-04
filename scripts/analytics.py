#!/usr/bin/env python3

from __future__ import annotations

import json
import logging
import os
import sys
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
script_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(script_dir)

if os.path.basename(script_dir) == "scripts" and os.path.exists(os.path.join(parent_dir, "pages", "utils")):
    sys.path.insert(0, os.path.join(parent_dir, "pages"))
else:
    sys.path.insert(0, parent_dir)

from utils.config_loader import get_config

logging.basicConfig(
    level=logging.WARNING,
    format='%(levelname)s: %(message)s'
)
logger = logging.getLogger(__name__)


def get_log_file_path() -> str:
    config = get_config()
    return config.expand_path("analytics", "log_file")


def load_visits(path: str) -> List[Dict[str, Any]]:
    try:
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.debug(f"Analytics file not found: {path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"Invalid JSON in analytics file: {e}")
        return []
    except OSError as e:
        logger.error(f"Error reading analytics file: {e}")
        return []

    if isinstance(data, list):
        return [entry for entry in data if isinstance(entry, dict)]
    
    logger.warning("Analytics file does not contain a list")
    return []


def format_timestamp(timestamp: Optional[int]) -> str:
    if timestamp is None:
        return "-"
    
    config = get_config()
    date_format = config.get("ui", "date_format", default="%Y-%m-%d %H:%M:%S")
    
    try:
        return datetime.fromtimestamp(timestamp).strftime(date_format)
    except (OSError, OverflowError, ValueError, TypeError) as e:
        logger.debug(f"Invalid timestamp {timestamp}: {e}")
        return "-"


def calculate_statistics(
    entries: List[Dict[str, Any]]
) -> Tuple[Dict[str, Dict[str, Any]], List[int]]:
    stats: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"count": 0, "first_ts": None, "last_ts": None}
    )
    all_timestamps: List[int] = []

    for entry in entries:
        page = str(entry.get("file", "unknown"))
        timestamp = entry.get("timestamp")
        
        if not isinstance(timestamp, int):
            try:
                timestamp = int(timestamp)
            except (TypeError, ValueError):
                timestamp = None

        stats[page]["count"] += 1

        if timestamp is not None:
            all_timestamps.append(timestamp)
            
            if stats[page]["first_ts"] is None or timestamp < stats[page]["first_ts"]:
                stats[page]["first_ts"] = timestamp
            
            if stats[page]["last_ts"] is None or timestamp > stats[page]["last_ts"]:
                stats[page]["last_ts"] = timestamp

    return stats, all_timestamps


def format_statistics_table(
    stats: Dict[str, Dict[str, Any]],
    all_timestamps: List[int]
) -> List[str]:
    sorted_pages = sorted(
        [
            (
                page,
                data["count"],
                data["first_ts"],
                data["last_ts"],
            )
            for page, data in stats.items()
        ],
        key=lambda row: (-row[1], row[0]),
    )

    formatted_rows = [
        (
            page,
            count,
            format_timestamp(first_ts),
            format_timestamp(last_ts),
        )
        for page, count, first_ts, last_ts in sorted_pages
    ]

    header_page = "Page"
    header_visits = "Visits"
    header_first = "First visit"
    header_last = "Last visit"

    col_page_width = max(
        len(header_page),
        max((len(row[0]) for row in formatted_rows), default=0)
    )
    col_visits_width = max(
        len(header_visits),
        max((len(str(row[1])) for row in formatted_rows), default=0)
    )
    col_first_width = max(
        len(header_first),
        max((len(row[2]) for row in formatted_rows), default=0)
    )
    col_last_width = max(
        len(header_last),
        max((len(row[3]) for row in formatted_rows), default=0)
    )

    lines = []
    
    total_width = (
        col_page_width + col_visits_width + col_first_width + col_last_width + 8
    )
    thick_divider = "=" * total_width
    thin_divider = "-" * (
        col_page_width + col_visits_width + col_first_width + col_last_width + 6
    )

    lines.append(thick_divider)
    lines.append("NomadNet visits summary".center(total_width))
    lines.append(thick_divider)

    header_line = (
        f"{header_page:<{col_page_width}}  "
        f"{header_visits:>{col_visits_width}}  "
        f"{header_first:<{col_first_width}}  "
        f"{header_last:<{col_last_width}}"
    )
    lines.append(header_line)
    lines.append(thin_divider)

    for page, count, first_str, last_str in formatted_rows:
        lines.append(
            f"{page:<{col_page_width}}  "
            f"{count:>{col_visits_width}}  "
            f"{first_str:<{col_first_width}}  "
            f"{last_str:<{col_last_width}}"
        )

    lines.append(thin_divider)
    
    total_entries = sum(data["count"] for data in stats.values())
    lines.append(f"Total records in log: {total_entries}")
    
    if all_timestamps:
        global_first = min(all_timestamps)
        global_last = max(all_timestamps)
        lines.append(
            f"Time range: {format_timestamp(global_first)}  ->  "
            f"{format_timestamp(global_last)}"
        )
    
    lines.append(thick_divider)

    return lines


def print_summary(entries: List[Dict[str, Any]]) -> None:
    if not entries:
        print("No visit data yet (the JSON file is empty or does not exist).")
        return

    stats, all_timestamps = calculate_statistics(entries)
    table_lines = format_statistics_table(stats, all_timestamps)
    
    for line in table_lines:
        print(line)


def main() -> int:
    try:
        log_file = get_log_file_path()
        entries = load_visits(log_file)
        print_summary(entries)
        return 0
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1


if __name__ == "__main__":
    sys.exit(main())
