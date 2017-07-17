# -*- coding: utf-8 -*-

"""
==================================================================================================================================================
                                                     杭州HUB仿真项目

                                    项目启动日期：2017年7月6日
                                    项目启动标识：AIRPORT OF EZHOU'S PROJECT  -- HZ
                                    ===========================================
                                    代码创建日期：2017年7月14日
                                    代码创建工程师：元方
                                    代码版本：1.0
                                    版本更新日期：2017年7月  日
                                    版本更新工程师：

                                    代码整体功能描述：生成包裹的路径（暂不包含小件）
                                                    调用generate_all_paths生成全体路径
                                                    调用path_choice生成某个包裹的路径



==================================================================================================================================================
"""


import random
import pickle
import os.path
import networkx as nx
from src.db.tools import load_from_local, SaveConfig


# 输入机器图，生成基本路径
def generate_base_paths(machine_graph):

    dest_node = [node for node in nx.nodes(machine_graph) if
                 node[0:3] in ["c1_", "c2_", "c3_", "c4_"]]
    road_unload_node = [node for node in nx.nodes(machine_graph) if
                        node.startswith("r")]
    air_unload_node = [node for node in nx.nodes(machine_graph) if
                       node.startswith("a")]
    all_unload_node = road_unload_node + air_unload_node
    base_path = {}
    for start_node in all_unload_node:
        for end_node in dest_node:
            pair = (start_node, end_node)
            if pair not in base_path:
                base_path[pair] = []
                for b_path in nx.all_simple_paths(machine_graph, start_node,
                                                  end_node):
                    base_path[pair].append(b_path)
    return base_path


def add_cycle_paths(machine_graph, base_paths, cycle_nodes_group=None):
    """
    在生成的基本路径中添加环路的函数，将生成的路线写入pickle文件
    :param machine_graph: 机器图，networkx的DiGraph格式
    :param base_paths: generate_base_paths生成的基本路径
    :param cycle_nodes_group: 环路组嵌套列表，例如医院区的输入是[["h1_1", "h2_1]]
    :return: 生成的全部路径
    生成路径的格式：嵌套字典，最外层键是元组(卸货位,终分拣格口)，第二层键是"hospital"和"without hospital"
                  标志该路线是否包含医院区，值为对应路线的列表
    """

    cycle_label = ["hospital"]  # 添加环路的标签

    if cycle_nodes_group:
        all_paths = {}
        j = 0
        while j < len(cycle_nodes_group):
            label = cycle_label[j]
            cycle_nodes = set(sum(list(nx.simple_cycles(machine_graph)), []))
            for key, path_list in base_paths.items():
                all_paths[key] = {label: [], "without " + label: []}
                all_nodes = set(sum(path_list, []))
                if all_nodes & set(cycle_nodes_group[j]):
                    for i in range(len(path_list)):
                        if set(path_list[i]) & set(cycle_nodes_group[j]):
                            all_paths[key][label].append(path_list[i])
                        else:
                            all_paths[key]["without " + label].append(
                                path_list[i])
                else:
                    add_node = list(all_nodes & cycle_nodes)
                    for i in range(len(path_list)):
                        path = path_list[i]
                        all_paths[key]["without " + label].append(path)
                        for node in path:
                            if node not in add_node:
                                continue
                            edge_pair = nx.find_cycle(machine_graph, node)
                            path_new = path[:]
                            position = path.index(node)
                            for pair in edge_pair:
                                if pair[1] not in path:
                                    path_new.insert(position + 1, pair[1])
                                position += 1
                            all_paths[key][label].append(path_new)
                            break
            j += 1
        return all_paths
    else:
        return base_paths


# 生成所有路径
def generate_all_paths():

    # parcel-path是一个临时使用的文件，不包含小件路径
    edge_df = load_from_local("parcel-path")

    cycle_node = [["h1_1", "h2_1"]]
    mgraph = nx.DiGraph()
    machine_graph = nx.from_pandas_dataframe(edge_df, list(edge_df)[0],
                                             list(edge_df)[1],
                                             create_using=mgraph)
    base_path = generate_base_paths(machine_graph)
    all_paths = add_cycle_paths(machine_graph, base_path, cycle_node)
    path_file = os.path.join(SaveConfig.DATA_DIR, "path")
    try:
        with open(path_file, "wb") as pickle_path:
            pickle.dump(all_paths, pickle_path)
    except Exception as exc:
        print(exc)
    return all_paths


def load_path_file():
    path_file = os.path.join(SaveConfig.DATA_DIR, "path")
    try:
        with open(path_file, "rb") as pickle_path:
            all_paths = pickle.load(pickle_path)
    except Exception as exc:
        print(exc)
        all_paths = None
    return all_paths


def path_generator(start_node, end_node, all_paths=None, hospital=False):
    """
    生成包裹路径的函数
    :param start_node: 起点卸货位ID
    :param end_node: 终点ID
    :param all_paths: generate_all_paths生成的所有路径嵌套字典，不传递则从本地文件读取
    :param hospital: 是否进入医院区
    :return: 包裹路线，节点的列表格式
    """
    if not all_paths:
        paths = load_path_file()[(start_node, end_node)]
    else:
        paths = all_paths[(start_node, end_node)]
    if not hospital:
        return random.choice(paths["without hospital"])
    else:
        return random.choice(paths["hospital"])


if __name__ == "__main__":

    random.seed(42)
    hospital = {"h1_1", "h2_1"}

    all_path = generate_all_paths()

    i = 0
    for path_dic in all_path.values():
        for path in path_dic.values():
            i += len(path)

    print(f"Number of paths: {i}")

    # 给定起终点单条路线
    print(",".join(path_generator("a1_1", "c1_1", hospital=False)))
    print(",".join(path_generator("a1_1", "c1_1", hospital=True)))

    # 生成100000条路线，测试进入医院区的概率是否为5%
    land_start_node = ["r1_1", "r1_2", "r1_3", "r1_4", "r2_1", "r2_2", "r2_3",
                       "r2_4"]
    land_end_node_pre = ["c1_", "c2_", "c3_"]
    paths = {"hospital": [], "without hospital": []}
    num = 0
    while num < 100000:
        start = random.choice(land_start_node)
        end = random.choice(land_end_node_pre) + str(random.randint(1, 50))
        prob = random.random()
        if prob <= 0.05:
            path = path_generator(start, end, all_path, hospital=True)
            if set(path) & hospital:
                paths["hospital"].append(path)
            else:
                print("Error! Hospital without hospital!")
                break
        else:
            path = path_generator(start, end, all_path, hospital=False)
            if not set(path) & hospital:
                paths["without hospital"].append(path)
            else:
                print("Error! Without hospital with hospital!")
                break
        num += 1

    print(len(paths["hospital"]))
    print(len(paths["without hospital"]))
