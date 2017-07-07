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


class SaveConfig:

    DATA_DIR = join( split(split(split(realpath(__file__))[0])[0])[0], 'data')



def load_from_local(table_name: str):
    pass


def load_from_mysql(table_name: str):
    pass


def get_trucks(is_test:bool = True, is_local:bool = True):

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

    truck_dict = dict(list(land_list.groupby(['plate_num', ' arrive_time'])))

    return truck_dict

def get_ulds():
    pass

def get_machine_vars(is_local: bool = True):
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


def get_queues(is_local: bool = True):
    """
    :param is_local:
    :return: two tables

    des: getting the queues data
    """
    machine_io = "i_equipment_io"
    queue_io = "i_queue_io"

    if is_local:
        machine_io_table = load_from_local(machine_io)
        queue_io_table = load_from_local(queue_io)

    else:
        machine_io_table = load_from_mysql(machine_io)
        queue_io_table = load_from_mysql(queue_io)

    return machine_io_table, queue_io_table



def get_io_rules(is_local: bool = True):

    """
    :param is_local:
    :return: dict -> {'head': dataframe.series}

    des:
    """

    if is_local:
        machine_io_table = load_from_local(machine_io)
        queue_io_table = load_from_local(queue_io)

    else:
        machine_io_table = load_from_mysql(machine_io)
        queue_io_table = load_from_mysql(queue_io)

    machine_io_dict = dict(list(machine_io_table.groupby('equipment_in_port')))
    queue_io_dict = dict(list(queue_io_table.groupby('queue_in_port')))

    machine_io_dict.update(queue_io_dict)

    return machine_io_dict

def get_resource_limit():
    pass