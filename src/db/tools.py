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
    DATA_FILE = 'tables.pkl'
    DATA_PATH  = join(DATA_DIR, DATA_FILE)


def load_from_local(table_name: str):

    try:
        table = pd.read_csv(join(SaveConfig.DATA_DIR, f"{table_name}.csv"))
    except Exception as exc:
        print(exc)
        table = None

    return table


def load_from_mysql(table_name: str):
    try:
        table = pd.read_sql_table(con=MySQLConfig.engine, table_name=f"{table_name}")
    except Exception as exc:
        print(exc)
        table = None

    return table


def get_trucks(is_test: bool=False, is_local: bool=False):

    """
    :param is_test:
    :param is_local:
    :return: truck dict

    des:
    get data from local file or mysql
    """
    table_name = "i_od_parcel_landside"

    if is_local:
        land_list = load_from_local(table_name)
    else:
        land_list = load_from_mysql(table_name)

    if is_test:
        land_list = land_list[: 1000]

    # add truck type: LL/LA/AL/AA
    land_list['truck_type'] = land_list['orgin_type'] + land_list['dest_code']
    truck_dict = dict(list(land_list.groupby(['plate_num', ' arrive_time', 'truck_type'])))
    return truck_dict


def get_ulds(is_local: bool=False):
    pass

# todo
def get_unload_setting(is_local: bool=False):
    pass

# todo
def get_reload_setting(is_local: bool=False):
    pass


def get_resource_table(is_local: bool=False):
    """
    :param is_local:
    :return: dict of resource {'equipment_in_port': dataframe.series}
    """
    resource_limit = "i_resource_limit"
    resource_equipment = "i_equipment_resource"

    # get tables
    if is_local:
        resource_limit_table = load_from_local(resource_limit)
        resource_equipment_table = load_from_local(resource_equipment)

    else:
        resource_limit_table = load_from_mysql(resource_limit)
        resource_equipment_table = load_from_mysql(resource_equipment)

    # merge table

    resource_table = resource_equipment_table.merge(
        resource_limit_table,
        how='left',
        on='resource_id',)

    resource_table_dict = dict(list(resource_table.groupby('equipment_in_port')))

    return resource_table_dict

# todo
def get_pipeline(is_local: bool=False):
    pass

def get_machine_parameters(is_local: bool=False):
    """
    :param is_local:
    :return: dict of dict of parameters

    des: getting machine var
    """
    table_name = "i_equipment_parameter"

    if is_local:
        parameter_list = load_from_local(table_name)
    else:
        parameter_list = load_from_mysql(table_name)

    parameter_dict = \
        {key: dict(list(val.groupby('parameter_id'))) for key, val in list(parameter_list.groupby('equipment_id'))}

    return parameter_dict



if __name__ == '__main__':
    test = get_machine_parameters(is_local=True)
    print(test)