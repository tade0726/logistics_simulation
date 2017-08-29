import os, time, csv
from pymysql import connect
from odo import odo



class Mysql(object):


    @property
    def connect(self):
        return connect(host='10.0.149.62',
                       user='root',
                       passwd='root123',
                       db='hangzhouhubqa_v3')

def creat_ge(files):

    while True:
        l = []
        x = 1
        for i, v in enumerate(files):
            l.append(v)
            x += 1
            if x == 1000000:
                break
        yield l
project_path = os.path.dirname(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
)

file_path_dict = {
        'o_machine_table': os.path.join(
            project_path, r'simpy_lib\hangzhou_simpy\out\machine_table.csv'),
        'o_path_table': os.path.join(
            project_path, r'simpy_lib\hangzhou_simpy\out\path_table.csv'),
        'o_pipeline_table': os.path.join(
            project_path, r'simpy_lib\hangzhou_simpy\out\pipeline_table.csv'),
        'o_truck_table': os.path.join(
            project_path, r'simpy_lib\hangzhou_simpy\out\truck_table.csv'),
                      }

for table, file_path in file_path_dict.items():
    c = time.time()
    files = csv.reader(open(file_path))
    columns = ''
    lenth = 0
    x = 1
    for i, v in enumerate(files):
        if i == 0:
            columns = ', '.join(v)
            lenth = len(v)
            break
    conn = Mysql().connect
    with conn as cursor:
        for item in creat_ge(files):
            if item != []:
                cursor.executemany(
                    "insert into {} ({}) values "
                    "(%s".format(table, columns) + ', %s' * (lenth - 1) + ')', item)
                x+=1000000
                print("已插入： ", x)
            else:
                break
    print(time.time()-c)

# project_path = os.path.dirname(
#     os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# )
#
# file_path = os.path.join(
#             project_path, r'simpy_lib\hangzhou_simpy\out\machine_table.csv')
#
# t = odo(file_path, 'mysql+pymysql://root:root123@10.0.149.62/hangzhouhubqa_v3::o_machine_table')