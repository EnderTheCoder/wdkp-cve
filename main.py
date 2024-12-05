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
import random

from tqdm import tqdm

import util
from request import UnparsableRequestException
from util import sql_time_to_timestamp
from user_request import UserInfoRequest
from run_request import GetUserRunRequest, InsertRunRequest, DeleteRunRequest, GetRunSectionRequest, \
    DeleteRunSectionRequest, InsertRunSectionRequest, GetLocationRequest, InsertLocationRequest, DeleteLocationRequest
from prettytable import PrettyTable

phone_serial = None
app_version = None
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
    table = PrettyTable(
        ['编号', '跑步id', '原始里程数（米）', '考核里程数（米）', '跑步步数', '开始时间', '是否有效', '序列号', '版本号'])
    run_records = res['data']
    i = 0
    for record in run_records:
        if record['isquestion'] == 0:
            total_run_kilo += record['khgls']
        if record['isquestion'] == 0:
            is_question = 'YES'
        else:
            is_question = 'NO'

        table.add_row(
            [i, record['id'], record['gls'], record['khgls'], record['pbbs'], record['qssj'], is_question,
             record['phoneno'], record['version']])
        i += 1
    print(f"找到共计{len(res['data'])}条记录，合法总里程数{total_run_kilo}米")
    print(table)
    print('当前设置的app版本号：', app_version)
    print('当前设置的手机序列号：', phone_serial)
    print("*执行操作：")
    print("\t1. 下载数据")
    print("\t2. 删除数据")
    print("\t3. 插入数据")
    print("\t4. 设置手机序列号")
    print("\t5. 设置APP版本")
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
            ['编号', '跑步id', '原始里程数（米）', '考核里程数（米）', '跑步步数', '开始时间', '是否有效', '序列号',
             '版本号'])
        for json_file_name in os.listdir(run_path):
            with open(f'{run_path}/{json_file_name}') as f:
                record = json.load(f)
                if record['isquestion'] == 0:
                    is_question = 'YES'
                else:
                    is_question = 'NO'
                table.add_row(
                    [i, record['id'], record['gls'], record['khgls'], record['pbbs'], record['qssj'], is_question,
                     record['phoneno'], record['version']])
                target_records.append(record)
                i += 1
        print(table)
        run_option = int(input("输入目标数据编号："))
        target_record = target_records[run_option]
        target_time_head = input('输入开始跑步日期，格式YYYY-MM-DD：')
        target_time_tail = input("输入跑步时间，格式hh:mm:ss（默认随机八点钟）：")

        if app_version is not None:
            target_record['version'] = app_version
        if phone_serial is not None:
            target_record['phoneno'] = phone_serial
        req_list = []
        dup = input('重复天数（默认1，不得小于1）：')
        if dup == '':
            print('使用默认值：1')
            dup = 1
        else:
            dup = int(dup)

        pbar = tqdm(range(dup))
        for run_idx in pbar:
            flag_random_time_tail = False
            if target_time_tail == '':
                flag_random_time_tail = True
                target_time_tail = f'08:{random.randrange(0, 30)}:{random.randrange(0, 59)}'
            target_time_full = target_time_head+' ' + target_time_tail
            target_timestamp = sql_time_to_timestamp(target_time_full) + run_idx * 24 * 60 * 60
            base_timestamp = sql_time_to_timestamp(target_record['qssj'])
            timestamp_offset = target_timestamp - base_timestamp
            pbar.set_description('写入跑步数据')
            run_req = InsertRunRequest(target_record, user_id, True, timestamp_offset)
            run_req.send()
            with open(f"data/{target_phone}/run_section/{target_record['id']}.json") as f:
                sections = list(json.load(f))
                for s_idx, section in enumerate(sections):
                    if s_idx == len(sections) - 1:
                        section['rtime'] = util.offset_time(section['rtime'], random.randrange(0, 60 * 5))
                    pbar.set_description(f'写入跑步区段数据{s_idx + 1}/{len(sections)}')
                    InsertRunSectionRequest(dict(section), run_req.data_id(), timestamp_offset).send()
            with open(f"data/{target_phone}/run_location/{target_record['id']}.json") as f:
                locations = list(json.load(f))
                for l_idx, location in enumerate(locations):
                    fail_cnt = 0
                    try:
                        pbar.set_description(f'写入位置关键点数据{l_idx + 1}/{len(locations)}')
                        InsertLocationRequest(dict(location), user_id, timestamp_offset).send()
                    except UnparsableRequestException:
                        fail_cnt += 1
                        print('警告：一项位置关键点数据写入失败')
                        if fail_cnt >= 5:
                            print('错误：失败超过5次，终止写入')
                            break
            if flag_random_time_tail:
                target_time_tail = ''
    if option == 4:
        phone_serial = input("输入手机序列号：")
    if option == 5:
        app_version = input("输入app版本号（苹果手机的型号包含在版本号中，示例：iPhone15,4|17.4.1|1.71）：")
    if option == 0:
        print('主程序退出')
        exit(0)
