"""
@Time: 2024/5/21 11:14
@Auth: EnderTheCoder
@Email: ggameinvader@gmail.com
@File: main.py
@IDE: PyCharm
@Motto：The only one true Legendary Grandmaster.
"""
import json
import os.path
import time
from user_request import UserInfoRequest
from run_request import GetUserRunRequest, InsertRunRequest
from prettytable import PrettyTable

phone = input("手机号码: ")
req = UserInfoRequest(phone)
res = req.send()
if len(res['data']) > 0:
    print("用户名: ", res['data'][0]['username'])
    print("密码: ", res['data'][0]['userdlmm'])
    print("用户id: ", res['data'][0]['userid'])
    print("full data: ", res['data'][0])
    user_id = res['data'][0]['userid']
else:
    raise Exception("User with given phone number not found")
user_path = f'data/{phone}'
if not os.path.exists(user_path):
    os.mkdir(user_path)
with open(user_path + f'/user.json', 'w') as f:
    json.dump(res['data'][0], f)
while True:
    req = GetUserRunRequest(user_id)
    res = req.send()
    print(res['data'])
    total_run_kilo = 0
    table = PrettyTable(['编号', '跑步id', '原始里程数（米）', '考核里程数（米）', '跑步步数', '开始时间', '是否有效'])
    run_records = res['data']
    i = 0
    for record in run_records:
        if record['isquestion'] == 0:
            total_run_kilo += record['khgls']
        if record['isquestion'] == 0:
            is_question = '是'
        else:
            is_question = '否'

        table.add_row(
            [i, record['id'], record['gls'], record['khgls'], record['pbbs'], record['qssj'], is_question])
        print(record)
        i += 1
    print(f"找到共计{len(res['data'])}条记录，合法总里程数{total_run_kilo}米")
    print(table)
    print("*执行操作：")
    print("\t1. 下载数据")
    print("\t2. 删除数据")
    print("\t3. 插入数据")
    print("\t0. 退出")
    option = int(input("输入选项："))
    if option == 1:
        run_data_id = int(input("输入数据编号"))
        run_data = run_records[run_data_id]
        run_path = user_path + '/run'
        if not os.path.exists(run_path):
            os.mkdir(run_path)
        export_path = f'data/{phone}/run/{user_id}-{run_data["id"]}-{run_data["qssj"]}.json'.replace(' ', '_')
        with open(export_path, 'w') as f:
            json.dump(run_data, f)
            print("文件被导出到：", export_path)
        pass
    if option == 2:
        pass
    if option == 3:
        target_phone = input('输入来源数据手机号码：')
        if not os.path.exists(f"data/{target_phone}"):
            raise FileExistsError("Target phone dir does not exists.")
        run_path = f"data/{target_phone}/run"
        i = 0
        target_records = []
        for json_file_name in os.listdir(run_path):
            table = PrettyTable(['编号', '跑步id', '原始里程数（米）', '考核里程数（米）', '跑步步数', '开始时间', '是否有效'])
            with open(f'{run_path}/{json_file_name}') as f:
                record = json.load(f)
                if record['isquestion'] == 0:
                    is_question = '是'
                else:
                    is_question = '否'
                table.add_row([i, record['id'], record['gls'], record['khgls'], record['pbbs'], record['qssj'], is_question])
                target_records.append(record)
                i += 1
        print(table)
        run_option = int(input("输入目标数据编号："))
        target_record = target_records[run_option]
        req = InsertRunRequest(target_record, user_id)
        res = req.send()
        pass
    if option == 0:
        exit(0)
        pass
