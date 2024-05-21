"""
@Time: 2024/5/21 11:11
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: user_request.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from request import EncryptedRequest


class UserInfoRequest(EncryptedRequest):
    def __init__(self, username):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': 'top 1 *',
            'tablename': 'JYAC_HYT.dbo.user_info nolock',
            'OrderBy': 'userid desc',
            'strwhere': f"and userzt=0 and userdlzh='{username}'"
        })


class GetProfileRequest(EncryptedRequest):
    def __init__(self):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': 'top 10 *',
            'tablename': '[WDHL_USER_LSGJ].[dbo].HIS_USER_969231 nolock',
        })
