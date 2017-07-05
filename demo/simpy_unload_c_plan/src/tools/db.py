# -*- coding: utf-8 -*-

"""
author:  Ted
date: 2017-06-12

des:
    loading data from mysql save as pickle, function load from pickle if pickle exist

"""

import pandas as pd
from os.path import realpath, join, split
from sqlalchemy import create_engine


# Connect to the database
class MySQLConfig:

    HOST = ""
    USER = ""
    password = ""
    db = ""
    charset=""


class SaveConfig:

    DATA_DIR = join( split(split(split(realpath(__file__))[0])[0])[0], 'data')
    LAND_LIST_PATH = join(DATA_DIR, 'land_list.df.csv')
    LAND_PCS_ALL_PATH = join(DATA_DIR, 'land_pcs_all.df.csv')
    LAND_LIST_CHA_PATH = join(DATA_DIR, 'land_list_change_time.df.csv')
    LAND_LIST_OVERALL = join(DATA_DIR, 'land_table_time_change.pkl')


def load_from_mysql(save=False):

    engine = create_engine(
        f'mysql+pymysql://{MySQLConfig.USER}:{MySQLConfig.password}@{MySQLConfig.HOST}/{MySQLConfig.db}?charset={MySQLConfig.charset}',
        isolation_level="READ UNCOMMITTED", )

    try:
        land_list = pd.read_sql_table(con=engine, table_name="land_list")
        land_pcs_all = pd.read_sql_table(con=engine, table_name="land_pcs_all")

        if save:
            print("Saving data..")
            land_list.to_csv(SaveConfig.LAND_LIST_PATH, index=0)
            land_pcs_all.to_csv(SaveConfig.LAND_PCS_ALL_PATH, index=0)

        return land_list, land_pcs_all

    except Exception as exc:
        print(type(exc), exc)


def load_from_csv():
    try:
        land_list = pd.read_csv(SaveConfig.LAND_LIST_PATH)
        land_pcs_all = pd.read_csv(SaveConfig.LAND_PCS_ALL_PATH)
        return land_list, land_pcs_all

    except Exception as exc:
        print(type(exc), exc)
        return None


def load_from_pkl():
    try:
        land_list_overall = pd.read_pickle(SaveConfig.LAND_LIST_OVERALL)
        return land_list_overall

    except Exception as exc:
        print(type(exc), exc)
        return None


def get_trucks(istest:bool = True):

    land_list_overall = load_from_pkl()
    if istest:
        land_list_overall = land_list_overall[: 1000]
    cols_keep = ["pcs_id", "pcs_type", "destination_type", "destination_city", "ori_type", "truck_id", "landing time"]
    truck_dict = dict(list(land_list_overall[cols_keep].groupby(['truck_id', 'landing time'])))
    return truck_dict


if __name__  == "__main__":
    # load_from_mysql(save=True)
    # print(SaveConfig.DATA_DIR)
    pass
