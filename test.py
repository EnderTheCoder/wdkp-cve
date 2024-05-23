"""
@Time: 2024/5/22 12:20
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: test.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from run_request import GetLocationRequest
req = GetLocationRequest(954532.0, '2024-01-01', '2024-05-01')
res = req.send()
req.print_table()
