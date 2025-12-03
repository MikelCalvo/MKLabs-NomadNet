#!/usr/bin/env python3

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.config_loader import get_config
from views.topbar import get_topbar
from views.header import get_header
from views.footer import get_footer


config = get_config()

TEMPLATE_MAIN = """{header}
{topbar}

`l{operator_content}

{footer}
"""

FILE = os.path.splitext(os.path.basename(__file__))[0]

tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
tpl = tpl.replace("{topbar}", get_topbar(FILE))
tpl = tpl.replace("{operator_content}", config.get("operator", "content", default=""))
tpl = tpl.replace("{footer}", get_footer(FILE))
print(tpl)
