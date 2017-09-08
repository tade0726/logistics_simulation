from sqlalchemy import create_engine
import os
import pandas as pd

__all__ = ['reading_csv', 'SaveConfig', 'RemoteMySQLConfig']


def reading_csv(dir_path):
    files_name = os.listdir(dir_path)
    files_csv = [os.path.splitext(x)[0] for x in files_name if os.path.splitext(x)[-1] == '.csv']
    return {name: pd.read_csv(os.path.join(dir_path, f"{name}.csv")) for name in files_csv}

class SaveConfig:
    DATA_DIR = '../data'
    OUT_DIR = '../out'

class RemoteMySQLConfig:
    HOST = "127.0.0.1"
    USER = "root"
    PASS = "zp913913"
    DB = "hangzhouhubqa"
    CHARSET = 'utf8'

    engine = create_engine(
        f'mysql+pymysql://{USER}:{PASS}@{HOST}/{DB}?charset={CHARSET}',
        isolation_level="READ UNCOMMITTED", )