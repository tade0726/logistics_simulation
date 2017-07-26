# -*- coding: utf-8 -*-

"""
作者：Ted
日期：
说明：

处理与数据库的交互

data will be store into dictionary

"""

import pandas as pd
import logging
from src.config import *


def write_mysql(table_name: str, data: pd.DataFrame, ):
    """写入MySQl数据库, 表格如果存在, 则新增数据"""
    try:
        data.to_sql(name=f'o_{table_name}', con=RemoteMySQLConfig.engine, if_exists='append', index=0)
        logging.info(f"mysql write table {table_name} succeed!")
    except Exception as exc:
        logging.error(f"mysql write table {table_name} failed, error: {exc}.")
        raise Exception


def write_local(table_name: str, data: pd.DataFrame):
    """写入本地"""
    try:
        data.to_csv(join(SaveConfig.OUT_DIR, f"{table_name}.csv"), index=0)
        logging.info(f"csv write table {table_name} succeed!")
    except Exception as exc:
        logging.error(f"csv write table {table_name} failed, error: {exc}.")
        raise Exception


def load_from_local(table_name: str):
    """本地读取数据，数据格式为csv"""
    logging.info(msg=f"Reading local table {table_name}")
    table = pd.read_csv(join(SaveConfig.DATA_DIR, f"{table_name}.csv"))
    return table


def load_from_mysql(table_name: str):
    """读取远程mysql数据表"""
    logging.info(msg=f"Reading mysql table {table_name}")
    table = pd.read_sql_table(con=RemoteMySQLConfig.engine, table_name=f"{table_name}")
    return table


def get_trucks(is_test: bool=False, is_local: bool=False):
    """
    返回货车数据，字典形式：
        key 为 （货车编号， 到达时间，货车货物路径类型（L／A..））
        value 为 一个货车的 packages 数据表
    """
    table_name = "i_od_parcel_landside"
    if is_local:
        table = load_from_local(table_name)
    else:
        table = load_from_mysql(table_name)
    if is_test:
        table = table.head(100)

    # convert datetime to seconds

    table["arrive_time"] = (table["arrive_time"] - TimeConfig.ZERO_TIMESTAMP)\
        .apply(lambda x: x.total_seconds() if x.total_seconds() > 0 else 0)
    # 'plate_num' 是货车／飞机／的编号
    return dict(list(table.groupby(['plate_num', 'arrive_time', 'src_type'])))


def get_vehicles(is_land: bool, is_test: bool = False, is_local: bool = False,):
    """
    返回 uld 或者 truck 数据，字典形式：

    parcel_dict:
        key 为 （货车编号， 到达时间，货车货物路径类型（L／A..））
        value 为 一个uld的 packages 数据表

    small_dict:
        key 为 parcel_id
        value 为 一个small_bag的 packages 数据表
    """
    if is_land:
        table_parcel_n = "i_od_parcel_landside"
        table_small_n = "i_od_small_landside"
    else:
        table_parcel_n = "i_od_parcel_airside"
        table_small_n = "i_od_small_airside"

    if is_local:
        table_parcel = load_from_local(table_parcel_n)
        table_small = load_from_local(table_small_n)
    else:
        table_parcel = load_from_mysql(table_parcel_n)
        table_small = load_from_mysql(table_small_n)

    # take samples for test
    if is_test:
        table_parcel = table_parcel.head(1000)
        table_small = table_small.head(1000)

    if not is_land:
        # fixme: using parcel_id as plate_num, cos lack of plate_num for uld
        table_parcel["plate_num"] = table_parcel["parcel_id"]
        table_small["plate_num"] = table_small["parcel_id"]

    # 装换时间
    table_parcel["arrive_time"] = (table_parcel["arrive_time"] - TimeConfig.ZERO_TIMESTAMP) \
        .apply(lambda x: x.total_seconds() if x.total_seconds() > 0 else 0)

    table_small["arrive_time"] = (table_small["arrive_time"] - TimeConfig.ZERO_TIMESTAMP) \
        .apply(lambda x: x.total_seconds() if x.total_seconds() > 0 else 0)

    # 'plate_num' 是货车／飞机／的编号
    parcel_dict = dict(list(table_parcel.groupby(['plate_num', 'arrive_time', 'path_type', ])))
    small_dict = dict(list(table_small.groupby(['parcel_id'])))
    return parcel_dict, small_dict


def get_unload_setting(is_local: bool=False):
    """
    返回字典形式：
        unload port 和 truck 类型（L， A） 的映射
    examples:
        {'r1_1': ['L'], 'r3_1': ['L', 'A']}
    """

    table_name = "i_unload_setting"

    if is_local:
        table = load_from_local(table_name)
    else:
        table = load_from_mysql(table_name)

    table_dict= \
        table.groupby('equipment_port')['origin_type'].apply(set).apply(list).to_dict()
    return table_dict


def get_reload_setting(is_local: bool=False):
    """
    返回字典形式：
        dest_code 和 reload port 类型的映射
    examples:
        { （"571J"， "reload", ""L""): ["c1_1", ],  （"571K"， "small_sort", "L"): ["c2_3", "c2_5"] }
    """

    table_name = "i_reload_setting"

    if is_local:
        table = load_from_local(table_name)
    else:
        table = load_from_mysql(table_name)
    table_dict= \
        table.groupby(['dest_zone_code', 'sorter_type', 'dest_type'])['equipment_port'].apply(set).apply(list).to_dict()
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

    table2 = table2[["resource_id", "equipment_id"]].drop_duplicates()
    table3 = table3[["equipment_id", "process_time"]].drop_duplicates()

    table_temp = table2.merge(table3, how="left", on="equipment_id")
    table_temp = table_temp

    table_temp2 = table_temp.groupby(["resource_id"])["process_time"].unique().apply(
        lambda x: x[0] if len(x) == 1 else None)
    table_temp2 = table_temp2.to_frame("process_time").reset_index()

    table = table1.merge(table_temp2, how="left", on="resource_id")

    # checking merge correct
    assert table1.shape[0] == table.shape[0]
    return table


def get_resource_equipment_dict(is_local: bool=False):
    """返回资源和设备槽口的对应关系"""
    table_name = "i_equipment_resource"
    table = load_from_local(table_name) if is_local else load_from_mysql(table_name)

    table_dict = dict()

    for _, row in table.iterrows():
        table_dict[row["equipment_port"]] = row["resource_id"]

    return table_dict

def get_pipelines(is_local: bool=False, ):

    """返回队列的表， 包含了每个队列对应的功能区域和传送时间"""

    tab_n_queue_io = "i_queue_io"
    tab_queue_io = load_from_local(tab_n_queue_io) if is_local else load_from_mysql(tab_n_queue_io)
    line_count_ori = tab_queue_io.shape[0]

    # fixme: need to add in database
    # add machine_type
    # m: presort
    # i1 - i8: secondary_sort
    # i17 - i24: secondary_sort
    # i9 - i16: small_sort
    # j: security
    # h: hospital
    # e, x: cross

    secon_sort_mark1 = [f'i{n}' for n in range(1, 9)]
    secon_sort_mark2 = [f'i{n}' for n in range(17, 25)]
    secon_sort_mark = secon_sort_mark1 + secon_sort_mark2

    ind_presort = tab_queue_io.equipment_port_next.str.startswith('m')
    ind_secondary_sort = tab_queue_io.equipment_port_next.apply(lambda x: x.split('_')[0]).isin(secon_sort_mark)
    ind_small_sort = tab_queue_io.equipment_port_next.str.startswith('u')
    ind_security = tab_queue_io.equipment_port_next.str.startswith('j')
    ind_hospital = tab_queue_io.equipment_port_next.str.startswith('h')
    ind_cross = \
        tab_queue_io.equipment_port_next.str.startswith('e') | tab_queue_io.equipment_port_next.str.startswith('x')

    # i-i, i-c, i-e 当做是需要请求资源的传送带
    ind_pipeline_res = \
        tab_queue_io.equipment_port_last.str.startswith('i') & \
        (tab_queue_io.equipment_port_next.str.startswith('c') | tab_queue_io.equipment_port_next.str.startswith('i')\
        | tab_queue_io.equipment_port_next.str.startswith('e'))

    tab_queue_io.loc[ind_presort, "machine_type"] = "presort"
    tab_queue_io.loc[ind_secondary_sort, "machine_type"] = "secondary_sort"
    tab_queue_io.loc[ind_small_sort, "machine_type"] = "small_sort"
    tab_queue_io.loc[ind_security, "machine_type"] = "security"
    tab_queue_io.loc[ind_cross, "machine_type"] = "cross"
    tab_queue_io.loc[ind_hospital, "machine_type"] = "hospital"

    tab_queue_io.loc[ind_pipeline_res, "pipeline_type"] = "pipeline_res"
    tab_queue_io.loc[~ind_pipeline_res, "pipeline_type"] = "pipeline"

    line_count_last = tab_queue_io.shape[0]
    assert line_count_ori == line_count_last
    return tab_queue_io


def get_queue_io(is_local: bool=False):
    """返回 io 对: [(r1_1,  m1_1), (r1_3, m2_3), ]"""
    table = get_pipelines(is_local)
    io_list = []
    for _, row in table.iterrows():
        io_list.append((row['equipment_port_last'], row['equipment_port_next']))
    return io_list


def get_equipment_process_time(is_local: bool=False):
    """
    返回设备对应的处理时间，不一定与资源挂钩
    samples:
        {'a1_1': 0.0,
         'a1_10': 0.0,
         'a1_11': 0.0,
         'a1_12': 0.0,
         'a1_2': 0.0,
         'a1_3': 0.0,}
    """
    table_n = "i_equipment_io"
    table = load_from_local(table_n) if is_local else load_from_mysql(table_n)
    table_dict = table.groupby(["equipment_port"])["process_time"].apply(lambda x: list(x)[0]).to_dict()

    return table_dict

if __name__ == "__main__":
    test = get_pipelines()
    print(test)
