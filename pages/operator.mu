#!/usr/bin/env python3
import os
from views.topbar import get_topbar
from views.header import get_header
from views.footer import get_footer

TEMPLATE_MAIN = """{header}
{topbar}

`lI'm Mikel Calvo, a software developer from the Basque Country.
You can check out my personal website at `!www.mikelcalvo.net`!
You can also shoot me a message at: `!lxmf@704a9988aacb09b811740d8eedf5e705`!

{footer}
"""

FILE = os.path.splitext(os.path.basename(__file__))[0]

tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
tpl = tpl.replace("{topbar}", get_topbar(FILE))
tpl = tpl.replace("{footer}", get_footer(FILE))
print(tpl)