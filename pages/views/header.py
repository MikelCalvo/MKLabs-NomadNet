#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from utils.config_loader import get_config


config = get_config()
logo_color = config.get("ui", "logo_color", default="`F00a")
color_reset = config.get("ui", "color_reset", default="`f")

TEMPLATE_MAIN = """                                                                     
                                                                     
`c ██████   ██████ █████   ████ █████                 █████            
`c░░██████ ██████ ░░███   ███░ ░░███                 ░░███             
`c ░███░█████░███  ░███  ███    ░███         ██████   ░███████   █████ 
`c ░███░░███ ░███  ░███████     ░███        ░░░░░███  ░███░░███ ███░░  
`c ░███ ░░░  ░███  ░███░░███    ░███         ███████  ░███ ░███░░█████ 
`c ░███      ░███  ░███ ░░███   ░███      █ ███░░███  ░███ ░███ ░░░░███
`c █████     █████ █████ ░░████ ███████████░░████████ ████████  ██████ 
`c░░░░░     ░░░░░ ░░░░░   ░░░░ ░░░░░░░░░░░  ░░░░░░░░ ░░░░░░░░  ░░░░░░  
                                                                     
                                                                     
"""


def get_header() -> str:
    return TEMPLATE_MAIN.replace("░", f"{logo_color}░{color_reset}")
