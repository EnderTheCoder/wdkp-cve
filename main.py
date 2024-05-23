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
from user_request import UserInfoRequest
from run_request import GetUserRunRequest, InsertRunRequest, DeleteRunRequest, GetRunSectionRequest, \
    DeleteRunSectionRequest, InsertRunSectionRequest, GetLocationRequest, InsertLocationRequest, DeleteLocationRequest
from prettytable import PrettyTable

if not os.path.exists('data'):
    os.mkdir('data')
phone = input("手机号码: ")
if len(phone) != 11 or phone[0] != '1' or not phone.isdigit():
    raise Exception("Invalid phone number format")
req = UserInfoRequest(phone)
res = req.send()
if len(res['data']) > 0:
    print("用户名: ", res['data'][0]['username'])
    print("密码: ", res['data'][0]['userdlmm'])
    print("用户id: ", res['data'][0]['userid'])
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
        run_section_path = user_path + '/run_section'
        run_location_path = user_path + '/run_location'
        if not os.path.exists(run_path):
            os.mkdir(run_path)
        if not os.path.exists(run_section_path):
            os.mkdir(run_section_path)
        if not os.path.exists(run_location_path):
            os.mkdir(run_location_path)
        section_req = GetRunSectionRequest(run_data['id'])
        section_req.send()
        print('跑步数据详情：')
        section_req.print_table()
        location_req = GetLocationRequest(user_id, run_data['qssj'], run_data['jssj'])
        location_req.send()
        print(f'含有位置记录点{len(location_req.data())}个')
        # location_req.print_table()
        if input('\t是否确认写入[y/N]') == 'y':
            section_req.save_data(f'data/{phone}/run_section/{run_data["id"]}.json')
            location_req.save_data(f'data/{phone}/run_location/{run_data["id"]}.json')
            export_path = f'data/{phone}/run/{run_data["id"]}.json'
            with open(export_path, 'w') as f:
                json.dump(run_data, f)
                print("文件被导出到：", export_path)
        else:
            print('写入取消')
    if option == 2:
        run_data_id = int(input("输入数据编号"))
        if input("\t是否确认删除[y/N]") == 'y':
            req = DeleteRunRequest(run_records[run_data_id]['id'])
            res = req.send()
            DeleteRunSectionRequest(run_records[run_data_id]['id']).send()
            DeleteLocationRequest(user_id, run_records[run_data_id]['qssj'], run_records[run_data_id]['jssj']).send()
            print('删除成功')
        else:
            print('删除取消')
        pass
    if option == 3:
        phones = []
        phone_table = PrettyTable(['编号', '手机号码'])
        i = 0
        for dir_name in os.listdir("data/"):
            if os.path.exists(f'data/{dir_name}/run'):
                phones.append(dir_name)
                phone_table.add_row([i, dir_name])
                i += 1
        print("具有缓存数据的账号列表：")
        print(phone_table)
        target_phone = phones[int(input('输入来源数据手机号码编号：'))]
        if not os.path.exists(f"data/{target_phone}"):
            raise FileExistsError("Target phone dir does not exists.")
        run_path = f"data/{target_phone}/run"
        i = 0
        target_records = []
        table = PrettyTable(
            ['编号', '跑步id', '原始里程数（米）', '考核里程数（米）', '跑步步数', '开始时间', '是否有效'])
        for json_file_name in os.listdir(run_path):
            with open(f'{run_path}/{json_file_name}') as f:
                record = json.load(f)
                if record['isquestion'] == 0:
                    is_question = '是'
                else:
                    is_question = '否'
                table.add_row(
                    [i, record['id'], record['gls'], record['khgls'], record['pbbs'], record['qssj'], is_question])
                target_records.append(record)
                i += 1
        print(table)
        run_option = int(input("输入目标数据编号："))
        target_record = target_records[run_option]
        req = InsertRunRequest(target_record, user_id)
        req.send()
        print('跑步数据写入成功')
        with open(f"data/{target_phone}/run_section/{target_record['id']}.json") as f:
            sections = list(json.load(f))
            for section in sections:
                InsertRunSectionRequest(dict(section), req.data_id()).send()
        print('跑步区段数据写入成功')
        with open(f"data/{target_phone}/run_location/{target_record['id']}.json") as f:
            locations = list(json.load(f))
            for location in locations:
                InsertLocationRequest(dict(location), user_id).send()
        print('位置关键点数据写入成功')
        print("插入成功")
        pass
    if option == 0:
        print('主程序退出')
        exit(0)
        pass
