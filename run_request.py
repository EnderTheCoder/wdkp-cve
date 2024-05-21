"""
@Time: 2024/5/21 13:24
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: run_request.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from request import EncryptedRequest


class GetUserRunRequest(EncryptedRequest):
    def __init__(self, userid: float):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': '* ',
            'tablename': 'JYAC_HYT.dbo.Yd_CdPb nolock',
            'strwhere': f"and yhid='{userid}' and qssj > '2024-02-01'"
        })

