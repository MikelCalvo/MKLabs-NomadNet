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

`lThis is an experimental website.
More stuff will be added in the future.

Meanwhile, you can connect your Sideband/Meshchat/... to me via TCP:

`!Host =`! {tcp_host}
`!Port =`! {tcp_port}

Or paste the following in your ~/.reticulum/config file:

`Fccc`B333

[[MKLabs```Fccc`B333]]
    type = TCPClientInterface
    interface_enabled = yes
    target_host = {tcp_host}
    target_port = {tcp_port}

`b`f

Public Propagation Node Address: `!{propagation_node}`!

{footer}
"""

FILE = os.path.splitext(os.path.basename(__file__))[0]

tpl = TEMPLATE_MAIN
tpl = tpl.replace("{self}", FILE)
tpl = tpl.replace("{header}", get_header())
tpl = tpl.replace("{topbar}", get_topbar(FILE))
tpl = tpl.replace("{tcp_host}", config.get("reticulum", "tcp_host", default=""))
tpl = tpl.replace("{tcp_port}", str(config.get("reticulum", "tcp_port", default="")))
tpl = tpl.replace("{propagation_node}", config.get("reticulum", "propagation_node", default=""))
tpl = tpl.replace("{footer}", get_footer(FILE))
print(tpl)
