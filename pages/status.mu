#!/usr/bin/env python3

import os
import shutil
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_loader import get_config
from views.header import get_header
from views.topbar import get_topbar
from views.footer import get_footer


config = get_config()
date_format = config.get("ui", "date_format", default="%Y-%m-%d %H:%M:%S")

TEMPLATE_MAIN = """{header}
{topbar}

Latest Update: {date_time}`c

{entries}

{footer}
"""

FILE = os.path.splitext(os.path.basename(__file__))[0]


def get_rnstatus_output() -> str:
    cmd = config.get("system", "rnstatus_command", default="rnstatus")
    args = config.get("system", "rnstatus_args", default=["-t"])
    
    cmd_expanded = os.path.expanduser(cmd)
    
    if os.path.isabs(cmd_expanded) or '/' in cmd:
        if os.path.isfile(cmd_expanded) and os.access(cmd_expanded, os.X_OK):
            cmd_path = cmd_expanded
        else:
            return f"Error: '{cmd}' not found or not executable"
    else:
        cmd_path = shutil.which(cmd)
        if not cmd_path:
            return f"Error: '{cmd}' command not found in PATH"
    
    try:
        result = subprocess.run(
            [cmd_path] + args,
            capture_output=True,
            text=True,
            timeout=10
        )
        return result.stdout.strip()
    except subprocess.TimeoutExpired:
        return "Error: rnstatus command timed out"
    except subprocess.CalledProcessError as e:
        return f"Error running rnstatus: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"


tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
tpl = tpl.replace("{topbar}", get_topbar(FILE))
tpl = tpl.replace("{date_time}", time.strftime(date_format, time.localtime(time.time())))
tpl = tpl.replace("{entries}", get_rnstatus_output())
tpl = tpl.replace("{footer}", get_footer(FILE))
print(tpl)
