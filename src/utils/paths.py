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

                                    代码整体功能描述：生成所有包裹到陆侧的路径
                                                    调用generate_all_paths生成全体路径
                                                    调用path_choice生成某个包裹的路径



==================================================================================================================================================
"""
__all__ = ["PathGenerator", 'generate_all_paths']

import random
import pickle
import os.path
import networkx as nx
from functools import reduce
from src.db.tools import load_from_mysql, get_reload_setting, SaveConfig, get_equipment_on_off


# 开关控制是否过滤不可用节点
SWITCH = False


def machine_pre():
    return dict(land_unload=["r1_", "r2_", "r3_", "r4_", "r5_"],
                air_unload=["a1_", "a2_", "a3_"],
                small_presort=["u1_", "u2_", "u3_", "u4_", "u5_", "u6_", "u7_",
                               "u8_"],
                land_small_secondary=["c7_", "c8_", "c9_", "c10",
                                      "c11", "c12"],
                air_small_secondary=["c5_", "c6_"],
                land_secondary=["c1_", "c2_", "c3_", "c4_"],
                air_secondary=["c13", "c14", "c15", "c16", "c17", "c18"],
                other_small=["i9_", "i10", "i11", "i12", "i13", "i14", "i15",
                             "i16"],
                hospital=["h1_1", "h2_1", "h3_1"],
                security=[f"j{i+1}_1" for i in range(41)])


# 输入机器图，生成基本路径
def generate_base_paths(machine_graph, start_nodes, end_nodes):
    base_path = {}
    for start_node in start_nodes:
        for end_node in end_nodes:
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
    machine_pre_dict = machine_pre()

    edge_df = load_from_mysql("i_queue_io")
    edge_df = edge_df[edge_df["normal_path"] == 1]

    cycle_node = [machine_pre_dict["hospital"]]
    mgraph = nx.DiGraph()
    machine_graph = nx.from_pandas_dataframe(edge_df, list(edge_df)[0],
                                             list(edge_df)[1],
                                             create_using=mgraph)

    print("Machine graph generated!")

    all_nodes = nx.nodes(machine_graph)
    small_presort_node = [node for node in all_nodes if
                          node[0:3] in machine_pre_dict["small_presort"]]
    land_s_secondary_node = [node for node in all_nodes if
                             node[0:3] in machine_pre_dict[
                                 "land_small_secondary"]]
    air_s_secondary_node = [node for node in all_nodes if
                            node[0:3] in machine_pre_dict[
                                "air_small_secondary"]]
    land_dest_node = [node for node in all_nodes if
                      node[0:3] in machine_pre_dict["land_secondary"]]
    air_dest_node = [node for node in all_nodes if
                     node[0:3] in machine_pre_dict["air_secondary"]]
    land_unload_node = [node for node in all_nodes if
                        node[0:3] in machine_pre_dict["land_unload"]]
    air_unload_node = [node for node in all_nodes if
                       node[0:3] in machine_pre_dict["air_unload"]]
    other_small_node = [node for node in all_nodes if
                        node[0:3] in machine_pre_dict["other_small"]]

    print("Start generating base path...")
    parcel_graph = machine_graph.subgraph(
        list(set(all_nodes) - set(small_presort_node) - set(other_small_node)))
    base_path = generate_base_paths(parcel_graph,
                                    land_unload_node + air_unload_node,
                                    land_dest_node + air_dest_node)
    print("Base paths generated!")

    print("Start generating small secondary path...")
    base_path.update(generate_base_paths(parcel_graph, land_s_secondary_node,
                                         land_dest_node))
    base_path.update(
        generate_base_paths(parcel_graph, air_s_secondary_node, air_dest_node))
    print("Small secondary path added!")

    all_paths = add_cycle_paths(parcel_graph, base_path, cycle_node)
    print("Cycle added!")

    print("Start generating small sort path...")
    small_path_1 = generate_base_paths(machine_graph.subgraph(list(
        set(all_nodes) - set(other_small_node) - set(
            air_s_secondary_node) - set(land_s_secondary_node))),
        land_unload_node + air_unload_node, small_presort_node)
    small_path_2 = generate_base_paths(machine_graph.subgraph(
        small_presort_node + other_small_node + land_s_secondary_node + air_s_secondary_node),
        small_presort_node, land_s_secondary_node + air_s_secondary_node)
    for key, value in small_path_1.items():
        all_paths[key] = {}
        all_paths[key]["all"] = value
    for key, value in small_path_2.items():
        all_paths[key] = {}
        all_paths[key]["all"] = value
    print("Small sort paths added!")

    path_file = os.path.join(SaveConfig.DATA_DIR, "path")
    try:
        with open(path_file, "wb") as pickle_path:
            pickle.dump(all_paths, pickle_path)
        print("Path file wrote!")
    except Exception as exc:
        print(exc)
    return all_paths


class PathGenerator(object):
    """
    路径生成器
    初始化时会加载data文件夹中的pickle文件path
    调用类的path_generator方法生成路径
    """

    def __init__(self):
        self.reload_setting = get_reload_setting()
        self.machine_pre_dict = machine_pre()
        path_file = os.path.join(SaveConfig.DATA_DIR, "path")
        if os.path.isfile(path_file):
            try:
                with open(path_file, "rb") as pickle_path:
                    all_paths = pickle.load(pickle_path)
            except Exception as exc:
                print(exc)
                all_paths = generate_all_paths()
        else:
            all_paths = generate_all_paths()

        if SWITCH:  # 节点开关处理
            _, unavailable = get_equipment_on_off()

            if unavailable:
                for key, path_dic in all_paths.items():
                    for type, path in path_dic.items():
                        all_paths[key][type] = list(
                            filter(lambda x: not set(x) & set(unavailable),
                                   all_paths[key][type]))

        self.all_paths = all_paths

    def path_generator(self, start_node, dest_code, sort_type, dest_type):
        """
        选择路径
        :param start_node: 起点
        :param dest_code: 目的地代码
        :param sort_type: 分拣类型，small_sort和reload
        :param dest_type: 目的地类型，L和A
        :return: 节点列表
        """

        if self.all_paths is None:
            raise Exception("Error: There isn't any path!")

        # machine_dict = machine_pre()

        # 小件分拣机中u节点和c节点的对应关系
        small_dic = dict(c5_=["u1_", "u2_", "u3_", "u4_"],
                         c6_=["u1_", "u2_", "u3_", "u4_"],
                         c7_=["u1_", "u2_", "u3_", "u4_"],
                         c8_=["u1_", "u2_", "u3_", "u4_"],
                         c9_=["u5_", "u6_", "u7_", "u8_"],
                         c10=["u5_", "u6_", "u7_", "u8_"],
                         c11=["u5_", "u6_", "u7_", "u8_"],
                         c12=["u5_", "u6_", "u7_", "u8_"])

        # 小件分拣机中找不到目的地时对应的垃圾槽口
        small_trash_dic = dict(c5_="c9_1",
                               c6_="c9_1",
                               c7_="c9_1",
                               c8_="c9_1",
                               c9_="c8_1",
                               c10="c8_1",
                               c11="c8_1",
                               c12="c8_1")

        if sort_type == "reload" or start_node.startswith("c"):
            position = 0
        else:
            if start_node.startswith("a") or start_node.startswith("r"):
                position = 1
            else:
                position = 2

        if position == 1:  # 小件包 从卸货位到拆包节点
            c_ports = self.reload_setting.get((dest_code, sort_type, dest_type),
                                              [])
            if c_ports:
                end_node = random.choice(
                    small_dic[random.choice(c_ports)[0:3]]) + str(
                    random.randint(1, 7))
            # 假如找不到小件槽口，随机给予 u 槽口
            else:
                all_u_port_pre = list(
                    reduce(lambda x, y: set(x) | set(y), small_dic.values()))
                end_node = random.choice(all_u_port_pre) + str(
                    random.randint(1, 7))
            return random.choice(self.all_paths[(start_node, end_node)]["all"])
        elif position == 2:  # 小件 从拆包节点到装包节点
            c_ports = self.reload_setting.get((dest_code, sort_type, dest_type),
                                              [])
            if c_ports:
                end_node = random.choice(
                    self.reload_setting[(dest_code, sort_type, dest_type)])
            else:
                end_node = "c8_1" if start_node in [f"u{i}" for i in
                                                    range(1, 5)] else "c9_1"
            path_list = self.all_paths.get((start_node, end_node), {"all": []})
            if path_list["all"]:
                return random.choice(
                    self.all_paths[(start_node, end_node)]["all"])
            else:  # 如果找不到路径，则规划到垃圾滑槽
                end_node = small_trash_dic[end_node[0:3]]
                return random.choice(
                    self.all_paths[(start_node, end_node)]["all"])
        else:  # 包裹路线 & 小件包 小件打包节点到终分拣节点
            end_node_list = self.reload_setting.get(
                (dest_code, "reload", dest_type), [])
            if end_node_list:
                end_node = random.choice(
                    self.reload_setting[(dest_code, "reload", dest_type)])
            else:
                if dest_type == "L":
                    end_node = random.choice(["c2_1", "c4_1"])
                else:
                    end_node = "c18_1"
            if start_node == "c8_1" or start_node == "c9_1":  # 小件垃圾滑槽直接送到终分拣
                return [start_node, end_node]
            if start_node[0:3] in self.machine_pre_dict[
                "land_unload"] and end_node[0:3] in self.machine_pre_dict[
                "air_secondary"]:
                security_prob = random.random()  # 安检概率
                if security_prob <= 0.009:
                    path = random.choice(self.all_paths[(start_node, end_node)][
                                             "without hospital"])
                    security_node = list(
                        set(path) & set(self.machine_pre_dict["security"]))
                    if len(security_node) == 0:
                        raise Exception(
                            "Error: There is no security check node in path!")
                    i = path.index(security_node[0])
                    now = path[:i+1]
                    now.append("c3_14")
                    return now
            hospital_prob = random.random()  # 医院区概率
            if hospital_prob <= 0.05:
                return random.choice(
                    self.all_paths[(start_node, end_node)]["hospital"])
            else:
                return random.choice(
                    self.all_paths[(start_node, end_node)][
                        "without hospital"])


if __name__ == "__main__":

    random.seed(31415927)

    machine_pre_dict = machine_pre()
    hospital = set(machine_pre_dict["hospital"])
    security = set(machine_pre_dict["security"])
    re_cal = True

    if re_cal:

        all_path = generate_all_paths()

        # 需要时可写入文本文件供检查
        # with open(os.path.join(SaveConfig.DATA_DIR, "paths.txt"), "w") as f:
        #     for item in all_path.values():
        #         for path_list in item.values():
        #             for path in path_list:
        #                 print(",".join(path), file=f)

        i = j = m = n = 0
        security_paths = {}
        for key, path_dic in all_path.items():
            j += 1
            for path in path_dic.values():
                i += len(path)
                for p in path:
                    if set(machine_pre_dict["security"]) & set(p):
                        m += 1
                        if key not in security_paths:
                            security_paths[key] = []
                        security_paths[key].append(p)
                    if list(set(machine_pre_dict["hospital"]) & set(p)):
                        n += 1

        print(f"Number of paths: {i}")
        print(f"Number of pairs: {j}")
        print(f"Number of security check paths: {m}")
        print(f"Number of hospital paths: {n}")

    Paths = PathGenerator()

    reload = load_from_mysql("i_reload_setting")

    # 给定起终点单条路线
    print(",".join(Paths.path_generator("r3_2", "027", "reload", "A")))
    print(
        ",".join(Paths.path_generator("a1_1", "752", "small_sort", "A")))  # 小件
    print(
        ",".join(Paths.path_generator("u3_7", "752", "small_sort", "A")))  # 小件
    print(
        ",".join(Paths.path_generator("c5_1", "752", "small_sort", "A")))  # 小件

    # 生成100000条路线，测试进入医院区的概率是否为5%
    land_start_node = ["r5_1", "r5_2", "r5_3", "r5_4"]
    air_end_node_list = reload[
        (reload["dest_type"] == "A") & (reload["sorter_type"] == "reload")]
    air_end_node = list(set(air_end_node_list["ident_des_zno"].tolist()))

    paths = {"hospital": [], "without hospital": [], "security": [], "us": []}
    num = 0

    while num < 100000:
        start = random.choice(land_start_node)
        end = random.choice(air_end_node)
        path = Paths.path_generator(start, end, "reload", "A")
        if set(path) & hospital:
            paths["hospital"].append(path)
        else:
            paths["without hospital"].append(path)
        if path[-2] in machine_pre_dict["security"]:
            paths["us"].append(path)
        elif set(machine_pre_dict["security"]) & set(path):
            paths["security"].append(path)
        num += 1

    hospital_num = len(paths["hospital"])
    all_num = len(paths["hospital"]) + len(paths["without hospital"])
    us_num = len(paths["us"])

    print(
        f"{hospital_num} parcels out of {all_num} will go to the hospital.")
    print(
        f"{us_num} parcels out of {all_num} don't pass the security check.")
