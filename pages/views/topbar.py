#!/usr/bin/env python3

import os
import sys
from typing import List, Tuple

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config_loader import get_config


config = get_config()
node_hash = config.get("nomadnet", "node_hash", default="")
logo_color = config.get("ui", "logo_color", default="`F00a")
color_reset = config.get("ui", "color_reset", default="`f")
topbar_divider = config.get("ui", "topbar_divider", default="-━")


def get_navigation_links() -> List[Tuple[str, str]]:
    links_config = config.get("topbar", "links", default=[])
    return [(link["label"], link["page"]) for link in links_config]


def build_link(label: str, page: str, current: str) -> str:
    base = f"`!`[{label}`{node_hash}:/page/{page}.mu]`!`"
    if page == current:
        return f"<`_{base}_>"
    return f"<{base}\>"


def get_topbar(current: str) -> str:
    links = get_navigation_links()
    links_html = " ".join(build_link(label, page, current) for label, page in links)
    
    return (
        f"{logo_color}\n"
        f"{topbar_divider}\n"
        f"{color_reset}\n"
        f"`c{links_html}\n"
        f"{logo_color}\n"
        f"{topbar_divider}\n"
        f"{color_reset}"
    )
