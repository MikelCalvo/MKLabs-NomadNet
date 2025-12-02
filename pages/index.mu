#!/usr/bin/env python3
import os
from views.topbar import get_topbar
from views.header import get_header
from views.footer import get_footer


TEMPLATE_MAIN = """{header}
{topbar}

`lThis is an experimental website.
More stuff will be added in the future.

Meanwhile, you can connect your Sideband/Meshchat/... to me via TCP:

`!Host =`! lab.mikelcalvo.net
`!Port =`! 4242

Or paste the following in your ~/.reticulum/config file:

`Fccc`B333

[[MKLabs```Fccc`B333]]
    type = TCPClientInterface
    interface_enabled = yes
    target_host = lab.mikelcalvo.net
    target_port = 4242

`b`f

Public Propagation Node Address: `!5381d942a5ed27f3e48452b7f57f6108`!

{footer}
"""

FILE = os.path.splitext(os.path.basename(__file__))[0]

tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
tpl = tpl.replace("{topbar}", get_topbar(FILE))
tpl = tpl.replace("{footer}", get_footer(FILE))
print(tpl)
