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
import logging


class MainConfig:
    IS_TEST = False   # 使用全集数据，还是测试数据
    SAVE_LOCAL = False  # 是否输出结果到本地csv， 还是 mysql
    IS_PARCEL_ONLY = False  # 只有 parcel 件
    IS_LAND_ONLY = False  # True 只有 landside, False landside airside
    CACHE_TYPE = None  # {None, "redis", "pkl", "hdf5"}
    LOCAL_DB = False  # control which DB using
    DEBUG_LEVEL = logging.INFO  # 输出日志信息的级别
    OUTPUT_MACHINE_TABLE_ONLY = True  # 只输出 o_machine_table


class RedisConfig:
    HOST = 'localhost'
    PORT = 6379
    DB = 0
    CONN = redis.StrictRedis(host=HOST, port=PORT, db=DB)


class RemoteMySQLConfig:
    if MainConfig.LOCAL_DB:
        HOST = "localhost"
        USER = "root"
        PASS = "zp913913"
        DB = "hangzhouhubqa"
        CHARSET = 'utf8'
    else:
        HOST = "10.0.149.30"
        USER = "developer"
        PASS = "developer"
        DB = "hangzhouhubqa_v3"
        CHARSET = 'utf8'

    engine = create_engine(
        f'mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}?charset={CHARSET}',
        isolation_level="READ UNCOMMITTED", )


class SaveConfig:
    PROJECT_DIR = split(split(realpath(__file__))[0])[0]
    DATA_DIR = join(PROJECT_DIR , 'data')
    OUT_DIR = join(PROJECT_DIR, 'out')
    LOG_DIR = join(PROJECT_DIR, 'log')
    HDF5_FILE = join(DATA_DIR, 'input_data.h5')


class TimeConfig:
    ZERO_TIMESTAMP = datetime(2017, 7, 25, 21)


def get_logger(logger_name: str):

    logger = logging.getLogger(logger_name)
    logger.setLevel(level=MainConfig.DEBUG_LEVEL)
    # add handlers
    ch = logging.StreamHandler()
    fh = logging.FileHandler(filename=join(SaveConfig.PROJECT_DIR, f"{logger_name}.log"), mode='w')
    # add format
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    # set format
    ch.setFormatter(formatter)
    fh.setFormatter(formatter)

    logger.addHandler(ch)
    logger.addHandler(fh)

    return logger


class LOG:
    logger_font = get_logger("simulation")


def generator_digit(n):
    for i in range(int('9' * n)):
        yield f"{i:0>{n}}"


class SmallCode:
    code_generator = generator_digit(10)


if __name__ == "__main__":
    a = generator_digit(10)
    print(next(a))
    print(next(a))