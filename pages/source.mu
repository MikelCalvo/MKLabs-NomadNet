#!/usr/bin/env python3
import os
from views.header import get_header

TEMPLATE_MAIN = """{header}
`F00a
-━
`f
`c<`!`[HOME`3c81447dff85b425c79ca5a97ff75f75:/page/index.mu]`!> <`!`[OPERATOR INFO`3c81447dff85b425c79ca5a97ff75f75:/page/operator.mu]`!> <`!`[STATUS`3c81447dff85b425c79ca5a97ff75f75:/page/status.mu]`!> <`_`!`[SOURCE`3c81447dff85b425c79ca5a97ff75f75:/page/source.mu]`!`_>`
`F00a
-━
`f

`lThe source code of this website is available at:
`!`_https://github.com/MikelCalvo/MKLabs-NomadNet`_`!

Feel free to make any pull requests or use the code as you wish.
Let me know if you do something cool with it.
"""

FILE = os.path.splitext(os.path.basename(__file__))[0]

tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
print(tpl)