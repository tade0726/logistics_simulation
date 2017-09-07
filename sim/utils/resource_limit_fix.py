# coding: utf-8

"""
Author: Ted

build a queue table and insert to mysql

"""

import sys
sys.path.append('..')

from sim.db import *
from sim.config import *

def main():
    table = load_from_mysql('i_resource_limit')
    table['resource_limit'] = table['resource_limit'].mask((table['resource_limit'] == 0.0), table['resource_number'])
    table.to_sql(name='i_resource_limit', con=RemoteMySQLConfig.engine, if_exists='replace', index=0)

if __name__ == '__main__':
    main()


