# -*- coding: utf-8 -*-

"""
Author: Ted
Date: 2017-07-13

Des:
    generate pipelines / resources / parameters / Trucks / Uld

"""

from sqlalchemy import create_engine
from os.path import realpath, join, split
from datetime import datetime
import redis


class RedisConfig:
    HOST = 'localhost'
    PORT = 6379
    DB = 0
    CONN = redis.StrictRedis(host=HOST, port=PORT, db=DB)


class RemoteMySQLConfig:
    HOST = "10.0.149.36"
    USER = "developer"
    PASS = "developer"
    DB = "test3"
    CHARSET = 'utf8'

    engine = create_engine(
        f'mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}?charset={CHARSET}',
        isolation_level="READ UNCOMMITTED", )


class SaveConfig:
    DATA_DIR = join( split(split(realpath(__file__))[0])[0], 'data')
    OUT_DIR = join( split(split(realpath(__file__))[0])[0], 'out')


class TimeConfig:
    ZERO_TIMESTAMP = datetime(2017, 6, 15, 21)


class MainConfig:
    IS_TEST = False
    SAVE_LOCAL = False
    IS_PARCEL_ONLY = True  # 只有 parcel 件
    IS_LAND_ONLY = False  # True 只有 landside, False landside airside


if __name__ == "__main__":
    print(SaveConfig.DATA_DIR)
    print(SaveConfig.OUT_DIR)