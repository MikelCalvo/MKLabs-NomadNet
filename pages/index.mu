#!/usr/bin/env python3

TEMPLATE_MAIN = """                                                                     
                                                                     
`c ██████   ██████ █████   ████ █████                 █████            
`c`F00a░░`f██████ ██████ `F00a░░`f███   ███`F00a░`f `F00a░░`f███                 `F00a░░`f███             
`c `F00a░`f███`F00a░`f█████`F00a░`f███  `F00a░`f███  ███    `F00a░`f███         ██████   `F00a░`f███████   █████ 
`c `F00a░`f███`F00a░░`f███ `F00a░`f███  `F00a░`f███████     `F00a░`f███        `F00a░░░░░`f███  `F00a░`f███`F00a░░`f███ ███`F00a░░`f  
`c `F00a░`f███ `F00a░░░`f  `F00a░`f███  `F00a░`f███`F00a░░`f███    `F00a░`f███         ███████  `F00a░`f███ `F00a░`f███`F00a░░`f█████ 
`c `F00a░`f███      `F00a░`f███  `F00a░`f███ `F00a░░`f███   `F00a░`f███      █ ███`F00a░░`f███  `F00a░`f███ `F00a░`f███ `F00a░░░░`f███
`c █████     █████ █████ `F00a░░`f████ ███████████`F00a░░`f████████ ████████  ██████ 
`c`F00a░░░░░`f     `F00a░░░░░`f `F00a░░░░░`f   `F00a░░░░`f `F00a░░░░░░░░░░░`f  `F00a░░░░░░░░`f `F00a░░░░░░░░`f  `F00a░░░░░░`f  
                                                                     
                                                                     
`F00a
-━
`f
`c<`_`!`[HOME`3c81447dff85b425c79ca5a97ff75f75:/page/index.mu]`!`_> <`!`[OPERATOR INFO`3c81447dff85b425c79ca5a97ff75f75:/page/operator.mu]`!> <`!`[STATUS`3c81447dff85b425c79ca5a97ff75f75:/page/status.mu]`!> <`!`[SOURCE`3c81447dff85b425c79ca5a97ff75f75:/page/source.mu]`!>`
`F00a
-━
`f

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
"""

tpl = TEMPLATE_MAIN
print(tpl)
