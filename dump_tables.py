from sys_request import DumpTablesRequest, FetchTableRequest
from prettytable import PrettyTable
from util import dict_to_table
res = DumpTablesRequest().send()
table = dict_to_table(res['data'])
for table in res['data']:
    t_req = FetchTableRequest(table['name'])
    t_res = t_req.send()
    t_req.save_data(f'sys/tables/{table["name"]}.json')
    print(dict_to_table(t_res['data']))
print(table)
pass
