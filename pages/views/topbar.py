#!/usr/bin/env python3

LINKS = [
    ("HOME", "index"),
    ("OPERATOR INFO", "operator"),
    ("STATUS", "status"),
    ("SOURCE", "source"),
]


def _build_link(label: str, page: str, current: str) -> str:
    base = f"`!`[{label}`3c81447dff85b425c79ca5a97ff75f75:/page/{page}.mu]`!`"
    if page == current:
        return f"<`_{base}_>"
    return f"<{base}\>"


def get_topbar(current: str) -> str:
    links = " ".join(_build_link(label, page, current) for label, page in LINKS)
    return (
        "`F00a\n"
        "-━\n"
        "`f\n"
        f"`c{links}\n"
        "`F00a\n"
        "-━\n"
        "`f"
    )
