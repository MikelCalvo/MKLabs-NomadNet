#!/usr/bin/env python3

import os
import time
import subprocess
from views.header import get_header

# Date/time format for formatting on the screen.
DATE_TIME_FORMAT = "%Y-%m-%d %H:%M:%S"

TEMPLATE_MAIN = """{header}
`F00a
-━
`f
`c<`!`[HOME`3c81447dff85b425c79ca5a97ff75f75:/page/index.mu]`!`> <`!`[OPERATOR INFO`3c81447dff85b425c79ca5a97ff75f75:/page/operator.mu]`!> <`_`!`[STATUS`3c81447dff85b425c79ca5a97ff75f75:/page/status.mu]`!`_> <`!`[SOURCE`3c81447dff85b425c79ca5a97ff75f75:/page/source.mu]`!>`
`F00a
-━
`f

Latest Update: {date_time}`c

{entrys}

"""

FILE = os.path.splitext(os.path.basename(__file__))[0]

tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
tpl = tpl.replace("{date_time}", time.strftime(DATE_TIME_FORMAT, time.localtime(time.time())))
tpl = tpl.replace("{entrys}", subprocess.getoutput("/home/mk/.local/bin/rnstatus -t").strip())
print(tpl)
