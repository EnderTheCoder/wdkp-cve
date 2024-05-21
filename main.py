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

req = UserInfoRequest(input("phone number: "))
res = req.send()
if len(res['data']) > 0:
    print("username: ", res['data'][0]['username'])
    print("password: ", res['data'][0]['userdlmm'])
    print("id: ", res['data'][0]['userid'])
    print("full data: ", res['data'][0])
else:
    raise Exception("User with given phone number not found")