# coding: utf-8

"""
Author: Ted

build a queue table and insert to mysql

"""

import sys
sys.path.append('..')

import pandas as pd
import numpy as np
from itertools import product
from sim.db import *
from sim.config import *


def main():
    table = load_from_mysql('i_queue_io')
    c_ports_combos = list(product(['c9_1'], [f'c{i}_{j}' for i, j in product(range(13, 19), range(1, 29))]))
    data = pd.DataFrame(c_ports_combos, columns=['equipment_port_last', 'equipment_port_next'])
    queue_id = data.equipment_port_last.str.split('_').str.get(0) + '_' + data.equipment_port_next.str.split('_').str.get(0)
    data = data.assign(
                    equipment_type='c',
                    queue_id=queue_id,
                    process_time=900.,
                    allocate_rule=None,
                    parcel_type='Small',
                    sorter_zone=None,
                    dest_type='A',
                    normal_path=0,
                    inserted_on=np.datetime64('NaT'),
                    modified_on=np.datetime64('NaT'),)
    data = data[table.columns]
    data.to_sql(name='i_queue_io', con=RemoteMySQLConfig.engine, if_exists='append', index=0)

if __name__ == '__main__':
    main()


