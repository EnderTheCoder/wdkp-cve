"""
@Time: 2024/5/22 0:00
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: util.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from prettytable import PrettyTable


def dict_to_table(data):
    table = None
    for row in data:
        row = dict(row)
        if table is None:
            table = PrettyTable(row.keys())
        table.add_row(row.values())
    return table
