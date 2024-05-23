"""
@Time: 2024/5/22 12:20
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from run_request import GetRunSectionRequest
req = GetRunSectionRequest(6813304.0)
res = req.send()
req.print_table()
