# -*- coding: utf-8 -*-

"""
author:  Ted
date: 2017-06-24
des: some loggers

"""

import logging
from os.path import join, realpath, split, dirname

log_dir = join(split(split(dirname(realpath(__file__)))[0])[0], 'logs')


def get_logger(log_name:str):

    logger = logging.getLogger(log_name)
    logger.setLevel(logging.DEBUG)

    fh = logging.FileHandler(join(log_dir, f"{log_name}.log"))
    fmt = '%(message)s'
    formatter = logging.Formatter(fmt)
    fh.setFormatter(formatter)

    logger.addHandler(fh)
    return logger


if __name__ == "__main__":
    print(log_dir)
