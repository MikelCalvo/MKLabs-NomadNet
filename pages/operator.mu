#!/usr/bin/env python3
import os
from views.header import get_header

TEMPLATE_MAIN = """{header}
`F00a
-━
`f
`c<`!`[HOME`3c81447dff85b425c79ca5a97ff75f75:/page/index.mu]`!> <`_`!`[OPERATOR INFO`3c81447dff85b425c79ca5a97ff75f75:/page/operator.mu]`!`_> <`!`[STATUS`3c81447dff85b425c79ca5a97ff75f75:/page/status.mu]`!> <`!`[SOURCE`3c81447dff85b425c79ca5a97ff75f75:/page/source.mu]`!>`
`F00a
-━
`f

`lI'm Mikel Calvo, a software developer from the Basque Country.
You can check out my personal website at `!www.mikelcalvo.net`!
You can also shoot me a message at: `!lxmf@704a9988aacb09b811740d8eedf5e705`!
"""

FILE = os.path.splitext(os.path.basename(__file__))[0]

tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
print(tpl)