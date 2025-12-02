#!/usr/bin/env python3

import os
import time
import subprocess
from views.header import get_header
from views.topbar import get_topbar

# Date/time format for formatting on the screen.
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

TEMPLATE_MAIN = """{header}
{topbar}

Latest Update: {date_time}`c

{entrys}

"""

FILE = os.path.splitext(os.path.basename(__file__))[0]

tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
tpl = tpl.replace("{topbar}", get_topbar(FILE))
tpl = tpl.replace("{date_time}", time.strftime(DATE_TIME_FORMAT, time.localtime(time.time())))
tpl = tpl.replace("{entrys}", subprocess.getoutput("/home/mk/.local/bin/rnstatus -t").strip())
print(tpl)
