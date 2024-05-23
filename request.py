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
from util import dict_to_table


class UnparsableRequestException(Exception):
    def __init__(self, code, message):
        self.message = f"Request could not be parsed by remote sql gate, code:{code}, message:{message}"
        self.message = message


class EncryptedRequest:
    def __init__(self, data_dict: dict, url: str = 'http://wd.wdhl365.com:7700/App/Query'):
        self.data_dict = data_dict
        for key, value in self.data_dict.items():
            self.data_dict[key] = secret_util.encrypt(f'"{value}"')
        self.url = url
        self.time = str(int(time.time()))
        self.md5_sign = self.sign()
        self.response = None

    def sign(self):
        s = self.time + json.dumps(self.data_dict).replace(" ", "")
        sorted_s = list(s)
        sorted_s.sort()
        s = ""
        for i in sorted_s:
            s += i
        return hashlib.md5(s.encode('utf-8')).hexdigest()

    def save_data(self, path, index: int = None):
        with open(path, 'w') as f:
            if index is None:
                json.dump(self.response['data'], f)
            else:
                json.dump(self.response['data'][index], f)

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
        self.response = response.json()
        return self.response

    def print_table(self):
        print(dict_to_table(self.response['data']))


class InsertRequest(EncryptedRequest):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict, 'http://wd.wdhl365.com:7702/App/InsertID')

    def data_id(self):
        return self.response['data']


class JsonInsertRequest(InsertRequest):
    def __init__(self, obj: dict, table_name: str, modify_fields: dict = None, remove_fields: tuple[str] = ()):
        data = {"SetCols": "", "tablename": table_name, "SetValue": ""}

        def sqlize(val):
            if isinstance(val, str):
                return f"'{val}'"
            if val is None:
                return "null"
            return str(val)

        for k, v in obj.items():
            if k not in remove_fields:
                data['SetCols'] += k + ", "

                if modify_fields is not None and k in modify_fields.keys():
                    data['SetValue'] += sqlize(modify_fields[k]) + ", "
                else:
                    data['SetValue'] += sqlize(v) + ", "
        data['SetCols'] = data['SetCols'][:-2]
        data['SetValue'] = data['SetValue'][:-2]
        super().__init__(data)


class DeleteRequest(EncryptedRequest):
    def __init__(self, table_name: str, condition: str):
        super().__init__({"tablename": table_name, "strwhere": condition}, "http://wd.wdhl365.com:7700/App/Delete")
