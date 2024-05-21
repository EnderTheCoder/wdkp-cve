"""
@Time: 2024/5/21 11:14
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: main.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import time
from user_request import UserInfoRequest
from run_request import GetUserRunRequest
from prettytable import PrettyTable

req = UserInfoRequest(input("手机号码: "))
res = req.send()
if len(res['data']) > 0:
    print("用户名: ", res['data'][0]['username'])
    print("密码: ", res['data'][0]['userdlmm'])
    print("用户id: ", res['data'][0]['userid'])
    print("full data: ", res['data'][0])
    userid = res['data'][0]['userid']
else:
    raise Exception("User with given phone number not found")

req = GetUserRunRequest(userid)
res = req.send()
print(res['data'])
total_run_kilo = 0
table = PrettyTable(['跑步id', '原始里程数（米）', '考核里程数（米）', '跑步步数'])
for record in res['data']:
    total_run_kilo += record['khgls']
    table.add_row([record['id'], record['gls'], record['khgls'], record['pbbs']])
print(f"找到共计{len(res['data'])}条记录，总里程数{total_run_kilo}米")
print(table)