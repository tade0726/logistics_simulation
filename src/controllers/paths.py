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

                                    代码整体功能描述：生成所有包裹到陆侧的路径（暂不包含小件）
                                                    调用generate_all_paths生成全体路径
                                                    调用path_choice生成某个包裹的路径



==================================================================================================================================================
"""
__all__ = ["PathGenerator", "generate_all_paths", ]

import random
import pickle
import os.path
import networkx as nx
from src.db.tools import load_from_local, get_reload_setting, SaveConfig


# 输入机器图，生成基本路径
def generate_base_paths(machine_graph):
    # 目前版本只生成空/陆到陆侧终分拣节点的包裹分拣路径
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
                        path_new = path[:]
                        all_paths[key]["without " + label].append(path)
                        for node in path:
                            if node not in add_node:
                                continue
                            edge_pair = nx.find_cycle(machine_graph, node)
                            position = path.index(node)
                            for pair in edge_pair:
                                path_new.insert(position + 1, pair[1])
                                position += 1
                            break
                        all_paths[key][label].append(path_new)
            j += 1
        return all_paths
    else:
        return base_paths


# 生成所有路径
def generate_all_paths():

    # parcel-path是一个临时使用的文件，不包含小件路径
    edge_df = load_from_local("parcel-path")

    cycle_node = [["h1_1", "h2_1", "h3_1"]]
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


class PathGenerator(object):
    """
    路径生成器
    初始化时会加载data文件夹中的pickle文件path
    调用类的path_generator方法生成路径
    """

    def __init__(self, all_paths=None):
        """
        :param all_paths: 存储路径的字典，如果不输入，则从data文件夹下的path文件读取
        """
        # 现在的版本是读取data文件夹下的一个临时文件
        self.reload_setting = get_reload_setting()
        if all_paths is not None:
            self.all_paths = all_paths
        else:
            path_file = os.path.join(SaveConfig.DATA_DIR, "path")
            try:
                with open(path_file, "rb") as pickle_path:
                    self.all_paths = pickle.load(pickle_path)
            except Exception as exc:
                print(exc)
                self.all_paths = None

    def path_generator(self, start_node, dest_code, sorter_type, dest_type):

        # TODO: 确认/db/tools/get_reload_setting 函数中返回字典key元组的变量顺序
        end_node = random.choice(
            self.reload_setting[(dest_code, sorter_type, dest_type)])

        # end_node = dest_code

        if self.all_paths is not None:
            paths = self.all_paths[(start_node, end_node)]
        else:
            raise Exception("There isn't any path!")

        prob = random.random()
        if prob <= 0.05:
            return random.choice(paths["hospital"])
        else:
            return random.choice(paths["without hospital"])


if __name__ == "__main__":

    random.seed(31415927)
    hospital = {"h1_1", "h2_1"}

    all_path = generate_all_paths()

    # 需要时可写入文本文件供检查
    # with open(os.path.join(SaveConfig.DATA_DIR, "paths.txt"), "w") as f:
    #     for item in all_path.values():
    #         for path_list in item.values():
    #             for path in path_list:
    #                 print(",".join(path), file=f)

    i = 0
    for path_dic in all_path.values():
        for path in path_dic.values():
            i += len(path)

    print(f"Number of paths: {i}")

    Paths = PathGenerator()

    # 给定起终点单条路线
    # TODO: /db/tools/get_reload_setting 函数中返回字典key元组的变量顺序
    print(",".join(Paths.path_generator("a1_1", "回流", "reload", "L")))

    # 生成100000条路线，测试进入医院区的概率是否为5%
    land_start_node = ["r1_1", "r1_2", "r1_3", "r1_4", "r2_1", "r2_2", "r2_3",
                       "r2_4"]
    land_end_node = ["571J", "回流", "571JB", "571AE", "571QD", "571TP",
                     "571QE", "571TQ", "571AJ", "571TK", "571CD", "571TB",
                     "571AG", "571NF", "571QC", "571NA", "571DC", "571AQ",
                     "571KL", "571HB", "571B", "571NB", "571AM", "571NH",
                     "571PF", "C571H", "571BM"]

    paths = {"hospital": [], "without hospital": []}
    num = 0
    while num < 100000:
        start = random.choice(land_start_node)
        end = random.choice(land_end_node)
        prob = random.random()
        path = Paths.path_generator(start, end, "reload", "L")
        if set(path) & hospital:
            paths["hospital"].append(path)
        else:
            paths["without hospital"].append(path)
        num += 1

    hospital_num = len(paths["hospital"])
    all_num = len(paths["hospital"]) + len(paths["without hospital"])

    print(
        f"{hospital_num} parcels out of {all_num} will go to the hospital.")
