"""
@Time: 2024/5/21 13:24
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: run_request.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import json

from request import EncryptedRequest, JsonInsertRequest, DeleteRequest


class GetUserRunRequest(EncryptedRequest):
    def __init__(self, userid: float):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': '* ',
            'tablename': 'JYAC_HYT.dbo.Yd_CdPb nolock',
            'strwhere': f"and yhid='{userid}' and qssj > '2024-02-01'"
        })


class InsertRunRequest(JsonInsertRequest):
    def __init__(self, json_val, user_id: int):
        if isinstance(json_val, str):
            with open(json_val) as f:
                super().__init__(dict(json.load(f)), 'JYAC_HYT.dbo.Yd_CdPb ', {"yhid": user_id}, ('id',))
        elif isinstance(json_val, dict):
            super().__init__(json_val, 'JYAC_HYT.dbo.Yd_CdPb ', {"yhid": user_id}, ('id',))
        else:
            raise Exception('Unsupported param type')
        self.time_fields = ['qssj', 'jssj', 'khjssj']


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
    def __init__(self, json_val, run_id: int):
        if isinstance(json_val, str):
            with open(json_val) as f:
                super().__init__(dict(json.load(f)), 'JYAC_HYT.dbo.Yd_CdPb_Section', {"pbid": run_id}, ('id',))
        elif isinstance(json_val, dict):
            super().__init__(json_val, 'JYAC_HYT.dbo.Yd_CdPb_Section', {"pbid": run_id}, ('id',))
        else:
            raise Exception('Unsupported param type')
        self.time_fields = ['rtime']


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
    def __init__(self, json_val, user_id: float):
        table_name = f'[WDHL_USER_LSGJ].[dbo].HIS_USER_{int(user_id)}'
        if isinstance(json_val, str):
            with open(json_val) as f:
                super().__init__(dict(json.load(f)), table_name, {"cjh": int(user_id)}, ('lsdwid',))
        elif isinstance(json_val, dict):
            super().__init__(json_val, table_name, {"cjh": int(user_id)}, ('lsdwid',))
        else:
            raise Exception('Unsupported param type')
        self.time_fields = ['sj']
