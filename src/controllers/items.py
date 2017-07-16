# -*- coding: utf-8 -*-

"""
作者：
日期：
说明：

存放车辆的控制器，机器及队列的监视器

"""
import simpy

from src.vehicles import Truck
from src.db import get_trucks


__all__ = ["truck_controller", ]


def truck_controller(env: simpy.Environment, trucks: simpy.FilterStore):
    """
    des: 使用 FilterStore 特定的车辆筛选进不同的 r 入口
    """
    trucks_dict = get_trucks()
    time_table = set(trucks_dict.keys())
    time_lst = [x[1] for x in time_table]

    while True:
        if env.now in time_lst:
            time_lst.remove(env.now)
            trucks_tmp = [t for t in time_table if t[1] == env.now]  # when env at 10, filter out truck come at 10
            time_table = set(time_table) - set(trucks_tmp)
            for truck_key in trucks_tmp:
                (truck_id, come_time, truck_type) = truck_key
                trucks.put(
                    Truck(item_id=truck_id,
                          come_time=come_time,
                          packages=trucks_dict[truck_key],
                          truck_type=truck_type,)
                )
        # like a clock, run every second
        yield env.timeout(1)


if  __name__ == '__main__':
    pass