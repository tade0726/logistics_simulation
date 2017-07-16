# -*- coding: utf-8 -*-

"""
作者：Ted
日期：
说明：

处理与数据库的交互

data will be store into dictionary

"""

import pandas as pd
from sqlalchemy import create_engine
from os.path import realpath, join, split
from collections import defaultdict

class MySQLConfig:

    HOST = ""
    USER = ""
    PASS = ""
    DB = ""
    CHARSET = 'utf8'

    engine = create_engine(
        f'mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}?charset={CHARSET}',
        isolation_level="READ UNCOMMITTED", )


class SaveConfig:

    DATA_DIR = join( split(split(split(realpath(__file__))[0])[0])[0], 'data')
    DATA_FILE = 'tables.csv'
    DATA_PATH = join(DATA_DIR, DATA_FILE)


def load_from_local(table_name: str):
    """本地读取数据，数据格式为csv"""
    table = pd.read_csv(join(SaveConfig.DATA_DIR, f"{table_name}.csv"))
    return table


def load_from_mysql(table_name: str):
    """读取远程mysql数据表"""
    table = pd.read_sql_table(con=MySQLConfig.engine, table_name=f"{table_name}")
    return table


def get_trucks(is_test: bool=False, is_local: bool=False):
    """
    返回货车数据，字典形式：
        key 为 （货车编号， 到达时间，货车货物路径类型（LL／LA..））
        value 为 一个货车的 packages 数据表
    """
    table_name = "i_od_parcel_landside"
    if is_local:
        table = load_from_local(table_name)
    else:
        table = load_from_mysql(table_name)
    if is_test:
        table = table.head(1000)
    # add path_type: LL/LA/AL/AA
    table['path_type'] = table['origin_type'] + table['dest_type']
    # 'plate_num' 是货车／飞机／的编号
    return dict(list(table.groupby(['plate_num', 'arrive_time', 'path_type'])))


def get_ulds(is_test: bool=False, is_local: bool=False):
    """
    返回uld数据，字典形式：
        key 为 （货车编号， 到达时间，货车货物路径类型（LL／LA..））
        value 为 一个uld的 packages 数据表
    """
    table_name = "i_od_parcel_airside"
    if is_local:
        table = load_from_local(table_name)
    else:
        table = load_from_mysql(table_name)
    if is_test:
        table = table.head(1000)
    # add path_type: LL/LA/AL/AA
    table['path_type'] = table['origin_type'] + table['dest_type']
    # 'plate_num' 是货车／飞机／的编号
    return dict(list(table.groupby(['uld_num', 'arrive_time', 'path_type'])))


def get_unload_setting(is_local: bool=False):
    """
    返回字典形式：
        unload port 和 truck 类型（LL， LA， AL ，AA） 的映射
    examples:
        {'r1_1': ['LL'], 'r3_1': ['LL', 'LA']}
    """

    table_name = "i_unload_setting"

    if is_local:
        table = load_from_local(table_name)
    else:
        table = load_from_mysql(table_name)

    # add truck type: LL/LA/AL/AA
    table['truck_type'] = table['origin_type'] + table['dest_type']

    table_dict = defaultdict(list)
    for _, row in table.iterrows():
        table_dict[row['equipment_port']].append(row['truck_type'])
    return table_dict


def get_reload_setting(is_local: bool=False):
    """
    返回字典形式：
        dest_code 和 reload port 类型的映射
    examples:
        { "571J": [c1_1, ], }
    """

    table_name = "i_reload_setting"

    if is_local:
        table = load_from_local(table_name)
    else:
        table = load_from_mysql(table_name)

    table_dict = defaultdict(list)
    for _, row in table.iterrows():
        table_dict[row['dest_code']].append(row['equipment_port'])
    return table_dict


def get_resource_limit(is_local: bool=False):
    """返回资源表，包含了单个资源处理时间"""
    table_name1 = "i_resource_limit"
    table_name2 = "i_equipment_resource"
    table_name3 = "i_equipment_io"

    if is_local:
        table1 = load_from_local(table_name1)
        table2 = load_from_local(table_name2)
        table3 = load_from_local(table_name3)
    else:
        table1 = load_from_mysql(table_name1)
        table2 = load_from_mysql(table_name2)
        table3 = load_from_mysql(table_name3)

    table = table1.merge(table2[['resource_id', 'equipment_id']], how='left', on='resource_id')\
                .merge(table3[['equipment_id', 'process_time']], how='left', on='equipment_id')

    return table


def get_pipelines(is_local: bool=False):

    """返回队列的表， 包含了每个队列对应的功能区域和传送时间"""

    table_name = "i_queue_io"

    if is_local:
        table = load_from_local(table_name)
    else:
        table = load_from_mysql(table_name)

    machine_dict = \
    {'LM': 'presort',
     'LS': 'secondary_sort',
     'SE': 'security',
     'AM': 'presort',
     'AS': 'secondary_sort',
     'MS': 'small_sort',}

    table = table[['equipment_port_last', 'equipment_port_next', 'sorter_zone', 'process_time', 'queue_id']]
    table['machine_type'] = table['sorter_zone'].apply(lambda x: x[:2]).replace(machine_dict)
    return table


def get_queue_io(is_local: bool):
    """返回 io 对: [(r1_1,  m1_1), (r1_3, m2_3), ]"""
    table = get_pipelines(is_local)
    io_list = []
    for _, row in table.iterrows():
        io_list.append((row['equipment_port_last'], row['equipment_port_next']))

    return io_list


if __name__ == '__main__':

    test1 = get_unload_setting(is_local=True)
    test2 = get_resource_limit(is_local=True)
    test3 = get_pipelines(is_local=True)
    test4 = get_queue_io(is_local=True)
    test5 = get_reload_setting(is_local=True)

    # this a test
    with open('tools.py.txt', 'at') as file:
        for obj in [test1, test2, test3, test4, test5]:
            file.writelines(obj.__str__() + "\n")
            file.writelines("\n" + "=" * 60 + "\n")
