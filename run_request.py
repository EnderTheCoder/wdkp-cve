"""
@Time: 2024/5/21 13:24
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: run_request.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import json
import random

from request import EncryptedRequest, JsonInsertRequest, DeleteRequest
from util import offset_time
from copy import deepcopy

class GetUserRunRequest(EncryptedRequest):
    def __init__(self, userid: float):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': '* ',
            'tablename': 'JYAC_HYT.dbo.Yd_CdPb nolock',
            'strwhere': f"and yhid='{userid}' and qssj > '2024-02-01'"
        })


class InsertRunRequest(JsonInsertRequest):
    def __init__(self, json_val, user_id: int, random_offset=False, time_offset=None):
        json_val = deepcopy(json_val)
        if random_offset:
            json_val['pbbs'] += random.randrange(50, 200)
            json_val['gls'] += random.randrange(50, 200)
            json_val['hdgls'] = json_val['gls']
            json_val['hdgls'] = json_val['gls']
            json_val['kcal'] += json_val['kcal'] * random.random() * 0.1
            json_val['khkcal'] = json_val['kcal']
            json_val['jssj'] = offset_time(json_val['jssj'], random.randrange(0, 200))
            json_val['khjssj'] = offset_time(json_val['khjssj'], random.randrange(0, 200))
        if isinstance(json_val, str):
            with open(json_val) as f:
                super().__init__(dict(json.load(f)), 'JYAC_HYT.dbo.Yd_CdPb ', {"yhid": user_id}, ('id',),
                                 ['qssj', 'jssj', 'khjssj'], time_offset)
        elif isinstance(json_val, dict):
            super().__init__(json_val, 'JYAC_HYT.dbo.Yd_CdPb ', {"yhid": user_id}, ('id',), ['qssj', 'jssj', 'khjssj'],
                             time_offset)
        else:
            raise Exception('Unsupported param type')


class DeleteRunRequest(DeleteRequest):
    def __init__(self, run_id: id):
        super().__init__("JYAC_HYT.dbo.Yd_CdPb ", f"and id = {run_id}")


class GetRunSectionRequest(EncryptedRequest):
    def __init__(self, run_id: id):
        super().__init__({
            'uuid': 'wdrunandroid_0',
            'cols': '* ',
            'tablename': 'JYAC_HYT.dbo.Yd_CdPb_Section',
            'strwhere': f"and pbid={run_id}"
        })


class InsertRunSectionRequest(JsonInsertRequest):
    def __init__(self, json_val, run_id: int, offset: int):
        json_val = deepcopy(json_val)
        if isinstance(json_val, str):
            with open(json_val) as f:
                super().__init__(dict(json.load(f)), 'JYAC_HYT.dbo.Yd_CdPb_Section', {"pbid": run_id}, ('id',),
                                 ['rtime'], offset)
        elif isinstance(json_val, dict):
            super().__init__(json_val, 'JYAC_HYT.dbo.Yd_CdPb_Section', {"pbid": run_id}, ('id',), ['rtime'], offset)
        else:
            raise Exception('Unsupported param type')


class DeleteRunSectionRequest(DeleteRequest):
    def __init__(self, run_id: int):
        super().__init__("JYAC_HYT.dbo.Yd_CdPb_Section", f"and pbid = {run_id}")


class GetLocationRequest(EncryptedRequest):
    def __init__(self, user_id: float, begin_time: str, end_time: str):
        super().__init__({
            'uuid': 'wdrunandroid_0',
            'cols': '* ',
            'tablename': f'[WDHL_USER_LSGJ].[dbo].HIS_USER_{int(user_id)}',
            'strwhere': f" and sj between '{begin_time}' and '{end_time}'"
        })


class DeleteLocationRequest(DeleteRequest):
    def __init__(self, user_id: float, begin_time: str, end_time: str):
        super().__init__(f'[WDHL_USER_LSGJ].[dbo].HIS_USER_{int(user_id)}',
                         f" and sj between '{begin_time}' and '{end_time}'")


class InsertLocationRequest(JsonInsertRequest):
    def __init__(self, json_val, user_id: float, offset: int):
        json_val = deepcopy(json_val)
        table_name = f'[WDHL_USER_LSGJ].[dbo].HIS_USER_{int(user_id)}'
        if isinstance(json_val, str):
            with open(json_val) as f:
                super().__init__(dict(json.load(f)), table_name, {"cjh": int(user_id)}, ('lsdwid',), ['sj'], offset)
        elif isinstance(json_val, dict):
            super().__init__(json_val, table_name, {"cjh": int(user_id)}, ('lsdwid',), ['sj'], offset)
        else:
            raise Exception('Unsupported param type')
