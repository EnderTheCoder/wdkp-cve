"""
@Time: 2024/5/22 0:00
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: util.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from datetime import datetime

from prettytable import PrettyTable


def dict_to_table(data):
    table = None
    for row in data:
        row = dict(row)
        if table is None:
            table = PrettyTable(row.keys())
        table.add_row(row.values())
    return table


time_format = "%Y-%m-%d %H:%M:%S"


def sql_time_to_timestamp(sql_time: str):
    datetime_obj = datetime.strptime(sql_time, time_format)
    return int(datetime_obj.timestamp())


def offset_time(sql_time: str, _offset_timestamp: int):
    return datetime.fromtimestamp(sql_time_to_timestamp(sql_time) + _offset_timestamp).strftime(time_format)

def timestamp_to_sql_time(timestamp: int):
    datetime_obj = datetime.fromtimestamp(timestamp)
    return datetime_obj.strftime(time_format)