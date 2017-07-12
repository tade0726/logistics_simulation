# -*- coding: utf-8 -*-

"""
======================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月6日
                                    代码创建工程师：元方
                                    代码版本：1.0
                                    版本更新日期：2017年7月6日
                                    版本更新工程师：元方

                                    代码整体功能描述：预分拣机器测试单元


=====================================================================================================
"""

import simpy
import random
from src.machine.presort import Presort

# from src.vehicles.items import Package

RANDOM_SEED = 42
WORKER_NUM = 2
MACHINE_ID = ["m1-1", "m1-2", "m1-3", "m1-4"]
DEST_NUM = 3
DEST_ID = {}
ALL_PACKAGES = {}
INPUT_QUEUE_DICT = {}
OUTPUT_QUEUE_DICT = {}
random.seed(RANDOM_SEED)


def package_time_interval():
	return random.uniform(40, 60)


def package_num():
	return random.randint(5, 10)


def process_time():
	return random.uniform(40, 200)


def generate_dest_id():
	dest_list = []
	for mid in MACHINE_ID:
		DEST_ID[mid] = [mid.replace("m", "i")[0:3] + str(i + 1) for i in
						range(DEST_NUM)]
		dest_list += DEST_ID[mid]
	return list(set(dest_list))


class PackagePresort(object):
	def __init__(self, package_id, path, generate_time):
		self.package_id = package_id
		self.path = path[:]
		self.plan_path = path[:]
		self.time_list = [generate_time]


def generate_package():
	for mid in MACHINE_ID:
		interval = package_time_interval()
		dest_id = random.choice(DEST_ID[mid])
		path = [mid, dest_id]
		ALL_PACKAGES[mid] = [PackagePresort(f'{mid}-{i+1}', path, interval * i)
							 for i in range(package_num())]


def generate_queue(env, machine_id):
	package_queue = simpy.PriorityStore(env)
	for i in range(len(ALL_PACKAGES[machine_id])):
		item = ALL_PACKAGES[machine_id].pop(0)
		package_queue.put(
			simpy.PriorityItem(priority=item.time_list[0], item=item))
	INPUT_QUEUE_DICT[machine_id] = package_queue


if __name__ == '__main__':
	print("start")
	dest_id_list = generate_dest_id()
	generate_package()
	machine_dict = {}
	env = simpy.Environment()
	for did in dest_id_list:
		OUTPUT_QUEUE_DICT[did] = simpy.PriorityStore(env)
	for mid in MACHINE_ID:
		generate_queue(env, mid)
		input_queue = INPUT_QUEUE_DICT[mid]
		time = process_time()
		presort_machine = Presort(env, mid, time, WORKER_NUM, input_queue,
								  OUTPUT_QUEUE_DICT)
		machine_dict[mid] = presort_machine
		env.process(presort_machine.run())
	env.run()
	for _, next_queue in OUTPUT_QUEUE_DICT.items():
		for item in next_queue.items:
			package = item.item
			print(
				f'Package {package.package_id} go to {package.plan_path[0]} at {package.time_list[0]}')
			print(
				f'Package {package.package_id} go to {package.plan_path[1]} at {package.time_list[1]}')
	print("End")
