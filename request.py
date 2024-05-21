"""
@Time: 2024/5/21 11:12
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: request.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import hashlib
import json
import time

import requests

from secret import secret_util


class UnparsableRequestException(Exception):
    def __init__(self, code, message):
        self.message = f"Request could not be parsed by remote sql gate, code:{code}, message:{message}"


class EncryptedRequest:
    def __init__(self, data_dict: dict, url: str = 'http://wd.wdhl365.com:7700/App/Query'):
        self.data_dict = data_dict
        for key, value in self.data_dict.items():
            self.data_dict[key] = secret_util.encrypt(f'"{value}"')
        self.url = url
        self.time = str(int(time.time()))
        self.md5_sign = self.sign()

    def sign(self):
        s = self.time + json.dumps(self.data_dict).replace(" ", "")
        sorted_s = list(s)
        sorted_s.sort()
        s = ""
        for i in sorted_s:
            s += i
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    def send(self):
        response = requests.post(self.url, data=json.dumps(self.data_dict).replace(' ', ''),
                                 headers={
                                     'Content-Type': 'application/json;charset=UTF-8',
                                     'appId': 'WdRunAndroid',
                                     'timeStamp': self.time,
                                     'signature': self.md5_sign,
                                     'tokenSign': 'e4edd60967ae7c5bfc087194c0971da7'
                                 })
        if response.status_code != 200:
            raise UnparsableRequestException(response.status_code, response.json())
        return response.json()
