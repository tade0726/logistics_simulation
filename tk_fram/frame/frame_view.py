# -*- coding: utf-8 -*-

from tkinter import DISABLED

from collections import defaultdict
# from .frame_api import menu_file
#  ====================宽度设置参数=================
FRAME_WIDTH = 1100  # 界面的总计宽度
FRAME_HEIGHT = 600  # 界面的总计高度

FRAME_WIDTH_LEFT = 700  # 左侧界面的总计宽度
FRAME_WIDTH_RIGHT = 400  # 右侧界面的总计宽度

FRAME_WIDTH_LEFT_CANVAS = 700
LEFT_SET_WIDTH_PACKAGE = 680
FRAME_WIDTH_LEFT_SET_PAD_TITLE = 680

FRAME_WIDTH_LEFT_ONE = 200  # 左侧界面的左宽度
FRAME_WIDTH_LEFT_TOW = 500  # 左侧界面的右宽度

#  ===================高度设置参数===================
FRAME_HEIGHT_HEAD = 50  # 界面顶端主标题的高度

#  ===================左侧设置界面高度设置============
#                        50+50+500
FRAME_HEIGHT_LEFT_PACKAGE = 50  # 包裹设置界面高度
FRAME_HEIGHT_LEFT_SET_PAD_TITLE = 25  # 左侧设置界面标题高度
FRAME_HEIGHT_LEFT_CENTER = 500  # 左侧中间界面的总计高度
FRAME_HEIGHT_LEFT_CENTER_UP = 400   # 左侧设置界面画布的上高度
#  ===================右侧输出界面高度设置============
#                           50+50+500
FRAME_HEIGHT_RIGHT_INFO_TITLE = 50  # 输出信息板标题高度
FRAME_HEIGHT_RIGHT_INFO = 500  # 输出信息版高度
FRAME_HEIGHT_RIGHT_BUTTON = 50  # 右侧底部界面button的总高度

# 判断数据更新操作是否已执行
Flag = {
    'update_data': 0,
    'run_sim': 0,
    'run_time': None
}

#  人力资源配置：下拉列表的值
LIST_VALUE_COMBOBOX = {
    'R': [0, 1, 2],
    'A': [0, 4],
    'M': [0, 1, 2, 3, 4],
    'J': [
        [0, 2],
        [0, 2, 4]
    ],
    'U': [0, 2],
    'H': [
        [0, 1, 2, 3, 4, 5, 6, 7, 8],
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16]
    ]
}

# 设备人数转换字典
NUM_TRANSLATE_DICT = {
    'A': 4,
    'J': 2,
    'U': 2
}

ENTRY_STATUS_DIC = {0: 'OFF', 1: 'ON'}  # btn状态对应entry的显示值对应字典

BTN_ENTRY_DICT = {}        # 初始化entry状态字典

# -------------------------所有控件的信息缓存字典
# time 表示时间段，取值于 start_time 字段
# num 的值永远与数据库里 resource_limit 的值相等
# {
#     time: {
#         id: {
#             status: value,
#             num: value
#         }
#     }
# }
CACHE_INSTANCE_DICT = {}

# 结构与 CACHE_INSTANCE_DICT 一致，保存控件初始信息
INIT_INSTANCE_DICT = {}

# 保存会随条件变动的全局变量
# CANVAS_DICT : Canvas, Scrollbar 字典
CURRENT = {
    'TIME': {
        'date': '',
        'time': '',
        'start_time': '',
        'last_run_time': ''
    },
    'CANVAS_DICT': {},
    'SHEET': 'R'
}

CACHE_J_STATUS = {}        # J 状态的缓存字典，value 固定为 0

CHECK_BTN_ENTRY_DIC = {}   # 设置控件的id同实例的关联字典
# 可选时间点
PACKAGE_NUM_LIST = ['1000', '50000', '100000', '200000', 'all']
DAY_TIME_DICT = defaultdict(list)

# M口与R口关联字典
M_R_DICT = {
    'm1_1': ('r1_1', 'r1_2'),
    'm1_3': ('r1_3', 'r1_4'),
    'm1_2': ('r2_1', 'r2_2'),
    'm1_4': ('r2_3', 'r2_4'),
    'm2_1': ('r3_1', 'r3_2'),
    'm2_3': ('r3_3', 'r3_4'),
    'm2_5': ('r3_5', 'r3_6'),
    'm2_7': ('r3_7', 'r3_8'),
    'm2_9': ('r3_9', 'r3_10'),
    'm2_2': ('r4_1', 'r4_2'),
    'm2_4': ('r4_3', 'r4_4'),
    'm2_6': ('r4_5', 'r4_6'),
    'm2_8': ('r4_7', 'r4_8'),
    'm2_10': ('r4_9', 'r4_10'),
    'm3_1': ('r5_1', 'r5_2'),
    'm3_2': ('r5_3', 'r5_4'),
    'm4_2': ('a1_1', 'a1_2', 'a1_3'),
    'm4_4': ('a1_4', 'a1_5', 'a1_6'),
    'm4_6': ('a1_7', 'a1_8', 'a1_9'),
    'm4_8': ('a1_10', 'a1_11', 'a1_12'),
    'm4_1': ('a2_1', 'a2_2', 'a2_3'),
    'm4_3': ('a2_4', 'a2_5', 'a2_6'),
    'm4_5': ('a2_7', 'a2_8', 'a2_9'),
    'm4_7': ('a2_10', 'a2_11', 'a2_12'),
}

R_J_DICT = {
    'r3_1': ('j10_1', 'j12_1', 'j14_1', 'j16_1', 'j18_1', 'j20_1', 'j22_1',
             'j24_1'),
    'r3_2': ('j10_1', 'j12_1', 'j14_1', 'j16_1', 'j18_1', 'j20_1', 'j22_1',
             'j24_1'),
    'r3_3': ('j10_1', 'j12_1', 'j14_1', 'j16_1', 'j18_1', 'j20_1', 'j22_1',
             'j24_1'),
    'r3_4': ('j10_1', 'j12_1', 'j14_1', 'j16_1', 'j18_1', 'j20_1', 'j22_1',
             'j24_1'),
    'r3_5': ('j10_1', 'j12_1', 'j14_1', 'j16_1', 'j18_1', 'j20_1', 'j22_1',
             'j24_1'),
    'r3_6': ('j10_1', 'j12_1', 'j14_1', 'j16_1', 'j18_1', 'j20_1', 'j22_1',
             'j24_1'),
    'r3_7': ('j26_1', 'j28_1', 'j30_1', 'j32_1', 'j34_1', 'j36_1', 'j38_1',
             'j40_1'),
    'r3_8': ('j26_1', 'j28_1', 'j30_1', 'j32_1', 'j34_1', 'j36_1', 'j38_1',
             'j40_1'),
    'r3_9': ('j26_1', 'j28_1', 'j30_1', 'j32_1', 'j34_1', 'j36_1', 'j38_1',
             'j40_1'),
    'r3_10': ('j26_1', 'j28_1', 'j30_1', 'j32_1', 'j34_1', 'j36_1', 'j38_1',
              'j40_1'),
    'r4_1': ('j1_1', 'j2_1', 'j3_1', 'j4_1', 'j5_1', 'j6_1', 'j7_1', 'j8_1'),
    'r4_2': ('j1_1', 'j2_1', 'j3_1', 'j4_1', 'j5_1', 'j6_1', 'j7_1', 'j8_1'),
    'r4_3': ('j1_1', 'j2_1', 'j3_1', 'j4_1', 'j5_1', 'j6_1', 'j7_1', 'j8_1'),
    'r4_4': ('j1_1', 'j2_1', 'j3_1', 'j4_1', 'j5_1', 'j6_1', 'j7_1', 'j8_1'),
    'r4_5': ('j1_1', 'j2_1', 'j3_1', 'j4_1', 'j5_1', 'j6_1', 'j7_1', 'j8_1'),
    'r4_6': ('j1_1', 'j2_1', 'j3_1', 'j4_1', 'j5_1', 'j6_1', 'j7_1', 'j8_1'),
    'r4_7': ('j9_1', 'j11_1', 'j13_1', 'j15_1', 'j17_1', 'j19_1', 'j21_1',
             'j23_1'),
    'r4_8': ('j9_1', 'j11_1', 'j13_1', 'j15_1', 'j17_1', 'j19_1', 'j21_1',
             'j23_1'),
    'r4_9': ('j9_1', 'j11_1', 'j13_1', 'j15_1', 'j17_1', 'j19_1', 'j21_1',
             'j23_1'),
    'r4_10': ('j9_1', 'j11_1', 'j13_1', 'j15_1', 'j17_1', 'j19_1', 'j21_1',
              'j23_1'),
    'r5_1': ('j9_1', 'j11_1', 'j13_1', 'j15_1', 'j17_1', 'j19_1', 'j21_1',
             'j23_1'),
    'r5_2': ('j9_1', 'j11_1', 'j13_1', 'j15_1', 'j17_1', 'j19_1', 'j21_1',
             'j23_1'),
    'r5_3': ('j25_1', 'j27_1', 'j29_1', 'j31_1', 'j33_1', 'j35_1', 'j37_1',
             'j39_1'),
    'r5_4': ('j25_1', 'j27_1', 'j29_1', 'j31_1', 'j33_1', 'j35_1', 'j37_1',
             'j39_1'),
    }


class ConfigApp(object):
    """"""
    RELOAD_FRAME = {
        'TOP_FRAME': {
            'attr': {
                'width': FRAME_WIDTH,
                'height': FRAME_HEIGHT_HEAD,
                'bd': 8,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'top'}
        },
        'LEFT_FRAME': {
            'attr': {
                'width': FRAME_WIDTH_LEFT,
                'height': FRAME_HEIGHT,
                'bd': 8,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'grid': {'row': 0, 'column': 0, 'sticky': 'nswe'}
        },
        'RIGHT_FRAME': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT,
                'bd': 8,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'grid': {'row': 0, 'column': 1, 'sticky': 'nswe'}
        },
        'LEFT_SET_PAD_TOP_R': {
            'attr': {
                'width': FRAME_WIDTH_LEFT,
                'height': FRAME_HEIGHT_LEFT_CENTER,
                'bd': 8,
                'relief': 'raise'
            },
            'pack': {
                'side': 'top'}
        },
        'LEFT_SET_PAD_UP_TITLE': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_CANVAS,
                'height': FRAME_HEIGHT_LEFT_SET_PAD_TITLE,
                'bd': 1,
                'bg': 'gray',
                'relief': 'raise'
            },
            'pack': {'side': 'top'}
        },
        'LEFT_SET_PAD_DOWN_TITLE': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_CANVAS,
                'height': FRAME_HEIGHT_LEFT_SET_PAD_TITLE,
                'bd': 1,
                # 'relief': 'raise'
            },
            'grid': {'row': 0, 'column': 0,
                     'sticky': 'nswe'
                     }
        },
        'LEFT_SET_PAD_TOP_PACKAGE': {
            'attr': {
                'width': LEFT_SET_WIDTH_PACKAGE,
                'height': FRAME_HEIGHT_LEFT_PACKAGE,
                'bd': 8,
                'relief': 'raise'
            },
            'grid': {'row': 0, 'column': 0,
                     'sticky': 'nswe'
                     }
        },
        'LEFT_SET_PAD_SHEET': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_SET_PAD_TITLE,
                'height': FRAME_HEIGHT_LEFT_SET_PAD_TITLE,
            },
            'grid': {'row': 1, 'column': 0, 'sticky': 'nswe'}
        },
        'LEFT_SET_PAD_CENTER_UP': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_CANVAS,
                'height': FRAME_HEIGHT_LEFT_CENTER_UP,
                'bd': 8,
                'relief': 'raise'
            },
            'grid': {'row': 2, 'column': 0, 'sticky': 'nswe'}
        },
        'RIGHT_TITLE': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT_RIGHT_INFO_TITLE,
                # 'bd': 8,
                # 'relief': 'raise'
            },
            'grid': {'row': 0, 'column': 0,
                     'sticky': 'nswe'
                     }
        },
        'RIGHT_OUTPUT_PAD_INFO': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT_RIGHT_INFO,
                'bd': 8,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'grid': {'row': 1, 'column': 0,
                     'sticky': 'nswe'
                     }
        },
        'RIGHT_BUTTON': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT_RIGHT_BUTTON,
                'bd': 8,
                'relief': 'raise'
            },
            'grid': {'row': 2, 'column': 0,
                     'sticky': 'nswe'
                     }
        }
    }


class ConfigFrame(object):
    """
    Frame 框架的初始化类
    """
    # 路侧卸货区id
    WIG_BTN_DICT = {
        'R': [
            'r1_1', 'r1_2', 'r1_3', 'r1_4',
            'r2_1', 'r2_2', 'r2_3', 'r2_4',
            'r3_1', 'r3_2', 'r3_3', 'r3_4', 'r3_5', 'r3_6', 'r3_7', 'r3_8',
            'r3_9', 'r3_10',
            'r4_1', 'r4_2', 'r4_3', 'r4_4', 'r4_5', 'r4_6', 'r4_7', 'r4_8',
            'r4_9', 'r4_10',
            'r5_1', 'r5_2', 'r5_3', 'r5_4'
        ],
        'A': [
            'a1_1', 'a1_2', 'a1_3', 'a1_4', 'a1_5', 'a1_6', 'a1_7', 'a1_8',
            'a1_9', 'a1_10', 'a1_11', 'a1_12',
            'a2_1', 'a2_2', 'a2_3', 'a2_4', 'a2_5', 'a2_6', 'a2_7', 'a2_8',
            'a2_9', 'a2_10', 'a2_11', 'a2_12'
        ],
        'M': [
            'm1_1', 'm1_3', 'm1_2', 'm1_4', 'm2_1', 'm2_3', 'm2_5', 'm2_7',
            'm2_9', 'm2_2', 'm2_4', 'm2_6', 'm2_8', 'm2_10', 'm3_1', 'm3_2',
            'm4_2', 'm4_4', 'm4_6', 'm4_8', 'm4_1', 'm4_3', 'm4_5', 'm4_7'
        ],
        'J': [
            'j1_1', 'j2_1', 'j3_1', 'j4_1', 'j5_1', 'j6_1', 'j7_1', 'j8_1',
            'j9_1', 'j10_1', 'j11_1',
            'j12_1', 'j13_1', 'j14_1', 'j15_1', 'j16_1', 'j17_1', 'j18_1',
            'j19_1', 'j20_1',
            'j21_1', 'j22_1', 'j23_1', 'j24_1', 'j25_1', 'j26_1', 'j27_1',
            'j28_1', 'j29_1',
            'j30_1', 'j31_1', 'j32_1', 'j33_1', 'j34_1', 'j35_1', 'j36_1',
            'j37_1', 'j38_1',
            'j39_1', 'j40_1', 'j41_1'
        ],
        'U': [
            'u1_1', 'u1_2', 'u1_3', 'u1_4', 'u1_5', 'u1_6', 'u1_7', 'u2_1',
            'u2_2', 'u2_3', 'u2_4', 'u2_5', 'u2_6', 'u2_7', 'u3_1', 'u3_2',
            'u3_3', 'u3_4', 'u3_5', 'u3_6', 'u3_7', 'u4_1', 'u4_2', 'u4_3',
            'u4_4', 'u4_5', 'u4_6', 'u4_7', 'u5_1', 'u5_2', 'u5_3', 'u5_4',
            'u5_5', 'u5_6', 'u5_7', 'u6_1', 'u6_2', 'u6_3', 'u6_4', 'u6_5',
            'u6_6', 'u6_7', 'u7_1', 'u7_2', 'u7_3', 'u7_4', 'u7_5', 'u7_6',
            'u7_7', 'u8_1', 'u8_2', 'u8_3', 'u8_4', 'u8_5', 'u8_6', 'u8_7'
        ],
        'H': [
            'h1_1', 'h2_1', 'h3_1'
        ]
    }
    WIG_DIC = {
        'R': {
            'columns': 3,                # 视图的列数目
            'wig_id': WIG_BTN_DICT['R']  # 视图的id列表
        },
        'A': {
            'columns': 3,
            'wig_id': WIG_BTN_DICT['A']
        },
        'M': {
            'columns': 3,
            'wig_id': WIG_BTN_DICT['M']
        },
        'J': {
            'columns': 3,
            'wig_id': WIG_BTN_DICT['J']
        },
        'U': {
            'columns': 3,
            'wig_id': WIG_BTN_DICT['U']
        },
        'H': {
            'columns': 3,
            'wig_id': WIG_BTN_DICT['H']
        }
    }

    CHECK_BTN_ATTR = {
        'font': ('Times', 10, 'bold'),
        'onvalue': 1,
        'offvalue': 0,
        'bd': 6,
        'height': 1,
        'pady': 10,
        'padx': 15,
        # 'height': 2,
        }
    ENTRY_ATTR = {
        'font': ('Times', 8, 'bold'),
        'bd': 4,
        'width': 6,
        'justify': 'left',
        'state': DISABLED
    }
    COMBOBOX_LIST_ATTR = {
        'font': ('Times', 10, 'bold'),
        # 'bd': 8,
        'width': 6,
        'height': 6,
        # 'justify': 'left',
        # 'state': DISABLED
    }
    #  初始化check_btn视图字典
    CHECK_BTN = {}
    #  初始化entry视图字典
    ENTRY = {}
    #  初始化combobox list 视图字典
    COMBOBOX_LIST = {}
    #
    SHEET_LABEL_DICT = {}
    #
    SHEET_VAR_DICT = {}
    #
    SHEET_LIST = ['R', 'A', 'M', 'J', 'U', 'H']
    #
    SHEET_ATTR_DICT = {
        'R': {
            'text': "R_路侧卸货区",
            'onvalue': 1,
            'offvalue': 0,
            'relief': 'raise',
            'width': '12',
            'bd': 5,
        },
        'A': {
            'text': "A_空侧卸货区",
            'onvalue': 1,
            'offvalue': 0,
            'relief': 'raise',
            'width': '12',
            'bd': 5,
        },
        'M': {
            'text': "M_初分拣矩阵",
            'onvalue': 1,
            'offvalue': 0,
            'relief': 'raise',
            'width': '12',
            'bd': 5,
        },
        'J': {
            'text': "J_安检机",
            'onvalue': 1,
            'offvalue': 0,
            'relief': 'raise',
            'width': '11',
            'bd': 5,
        },
        'U': {
            'text': "U_小件拆包台",
            'onvalue': 1,
            'offvalue': 0,
            'relief': 'raise',
            'width': '12',
            'bd': 5,
        },
        'H': {
            'text': "H_医院区",
            'onvalue': 1,
            'offvalue': 0,
            'relief': 'raise',
            'width': '11',
            'bd': 5,
        },
    }


class CheckBtnEntryView(ConfigFrame):

    def __init__(self):
        super().__init__()

    def _init_one_view(self, wig_id, columns):
        """ 单一视图初始化方法
        :arg:
            wig_id: 控件id号
            columns: 列数，每个view中的最大列数
        :return: None
        """
        # 起始行数
        row_var = 1
        # 起始列
        columns_var = 0
        for id_wig in wig_id:
            if columns_var >= columns:
                columns_var = 0
                row_var += 1

            self.CHECK_BTN[id_wig] = {
                'attr': self.CHECK_BTN_ATTR,
                'grid': {
                    'row': row_var,
                    'column': columns_var*columns+0,
                    # 'sticky': 'nswe'
                }
            }
            #  entry 视图设置
            self.ENTRY[id_wig] = {
                'attr': self.ENTRY_ATTR,
                'grid': {
                    'row': row_var,
                    'column': columns_var*columns+1,
                    # 'sticky': 'nswe'
                }
            }
            #  combobox list 视图设置
            self.COMBOBOX_LIST[id_wig] = {
                'attr': self.COMBOBOX_LIST_ATTR,
                'grid': {
                    'row': row_var,
                    'column': columns_var*columns+2,
                    # 'sticky': 'nswe'
                }
            }
            columns_var += 1

    def init_view(self):
        """初始化frame视图函数
        
        :return: None
        """
        #  WIG_DIC： 视图各个控件的id号字典:
        # {'id': {'columns': str, 'wig_id': [...], ...}
        for _, v in self.WIG_DIC.items():
            self._init_one_view(
                wig_id=v['wig_id'],
                columns=v['columns']
            )
