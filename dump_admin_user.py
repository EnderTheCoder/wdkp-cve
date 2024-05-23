"""
@Time: 2024/5/22 0:11
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: dump_admin_user.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
from sys_request import TestDumpTable, DumpRunAdminUser

# req = DumpBizAdminUser()
# req.send()
# req.save_data('sys/admin_user/biz_all.json')
# req.print_table()

req = DumpRunAdminUser()
req.send()
req.save_data('sys/admin_user/test_all_2.json')
req.print_table()
