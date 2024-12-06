"""
@Time: 2024/12/7 1:30
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: parse_profile.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""

import json

from prettytable import PrettyTable

data = json.loads(input('输入json数据：'))
data = data['data']['rows']
table = PrettyTable(['id', '姓名', '电话', '学号', '性别', '当前已跑', '专业', '民族'])
for i in data:
    table.add_row([
        i['id'], i['oname'], i['userlxdh'], i['onumber'], i['osex'], i['khgls'], i['proname'], i['userzb']
    ])
print(table)
