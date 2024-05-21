"""
@Time: 2024/5/21 13:24
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: run_request.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import json

from request import EncryptedRequest, JsonInsertRequest


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
