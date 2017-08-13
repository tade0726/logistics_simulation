# -*- coding: utf-8 -*-

from tkinter import DISABLED
# from .frame_api import menu_file
#  ====================宽度设置参数=================
FRAME_WIDTH = 1100  # 界面的总计宽度
FRAME_HEIGHT = 650  # 界面的总计高度

FRAME_WIDTH_LEFT = 700  # 左侧界面的总计宽度
FRAME_WIDTH_RIGHT = 400  # 右侧界面的总计宽度

FRAME_WIDTH_LEFT_CANVAS = 670

FRAME_WIDTH_LEFT_ONE = 200  # 左侧界面的左宽度
FRAME_WIDTH_LEFT_TOW = 500  # 左侧界面的右宽度

#  ===================高度设置参数===================
FRAME_HEIGHT_HEAD = 50  # 界面顶端主标题的高度

#  ===================左侧设置界面高度设置============
#                        50+50+500
FRAME_HEIGHT_LEFT_PACKAGE = 50  # 包裹设置界面高度
FRAME_HEIGHT_LEFT_SET_PAD_TITLE = 20  # 左侧设置界面标题高度
FRAME_HEIGHT_LEFT_CENTER = 500  # 左侧中间界面的总计高度
FRAME_HEIGHT_LEFT_CENTER_UP = 250   # 左侧设置界面画布的上高度
FRAME_HEIGHT_LEFT_CENTER_DOWN = 250  # 左侧设置界面画布的下高度
#  ===================右侧输出界面高度设置============
#                           50+50+500
FRAME_HEIGHT_RIGHT_INFO_TITLE = 40  # 输出信息板标题高度
FRAME_HEIGHT_RIGHT_INFO = 560  # 输出信息版高度
FRAME_HEIGHT_RIGHT_BUTTON = 50  # 右侧底部界面button的总高度

# 判断数据更新操作是否已执行
Flag = {
    'update_data': 0,
    'run_sim': 0,
    'save_data': 0,
    'run_time': None
}

#  人力资源配置：下拉列表的值
LIST_VALUE_COMBOBOX= {
    'R': [1, 2],
    'M': [1, 2, 3, 4]
}

ENTRY_STATUS_DIC = {0: 'OFF', 1: 'ON'}  # btn状态对应entry的显示值对应字典

BTN_ENTRY_DICT = {}       # 初始化entry状态字典

CHECK_BTN_ENTRY_DIC = {}   # 设置控件的id同实例的关联字典

DATABASES_DIC = {
    'TEST': {
        'HOST': '10.0.149.62',
        'USER': 'root',
        'PASSWORD': 'root123',
        'NAME': 'hangzhouhubland',
        'CHARSET': 'utf8'
    },
    'PRODUCTION': {

    }
}
DATABASES = DATABASES_DIC['TEST']
# 可选时间点
TIME_LIST = ['21:00', '22:00', '23:00', '02:00', '10:30']


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
            'pack': {'side': 'left'}
        },
        'RIGHT_FRAME': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT,
                'bd': 8,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'right'}
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
        'LEFT_SET_PAD_TITLE': {
            'attr': {
                'width': FRAME_WIDTH_LEFT,
                'height': FRAME_HEIGHT_LEFT_SET_PAD_TITLE,
                # 'bd': 8,
                # 'relief': 'raise'
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
                'relief': 'raise'
            },
            'pack': {
                'side': 'top'}
        },
        'LEFT_SET_PAD_TOP_PACKAGE': {
            'attr': {
                'width': FRAME_WIDTH_LEFT,
                'height': FRAME_HEIGHT_LEFT_PACKAGE,
                'bd': 8,
                'relief': 'raise'
            },
            'pack': {'side': 'top'}
        },
        'LEFT_SET_PAD_CENTER_UP': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_CANVAS,
                'height': FRAME_HEIGHT_LEFT_CENTER_UP,
                'bd': 8,
                'relief': 'raise'
            },
            'pack': {'side': 'top'}
        },
        'LEFT_SET_PAD_CENTER_DOWN': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_CANVAS,
                'height': FRAME_HEIGHT_LEFT_CENTER_DOWN,
                'bd': 8,
                'relief': 'raise'},
            'pack': {'side': 'top'}
        },
        'RIGHT_TITLE': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT_RIGHT_INFO_TITLE,
                # 'bd': 8,
                # 'relief': 'raise'
            },
            'pack': {'side': 'top'}
        },
        'RIGHT_OUTPUT_PAD_INFO': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT_RIGHT_INFO,
                'bd': 8,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'left'}
        },
        'RIGHT_BUTTON': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT_RIGHT_BUTTON,
                'bd': 8,
                'relief': 'raise'
            },
            'pack': {'side': 'bottom'}
        }
    }


class ConfigFrame(object):
    """
    Frame 框架的初始化类
    """
    # 路侧卸货区id
    WIG_ID_R = [
        'r1_1', 'r1_2', 'r1_3', 'r1_4',
        'r2_1', 'r2_2', 'r2_3', 'r2_4',
        'r3_1', 'r3_2', 'r3_3', 'r3_4', 'r3_5', 'r3_6', 'r3_7', 'r3_8', 'r3_9',
        'r3_10',
        'r4_1', 'r4_2', 'r4_3', 'r4_4', 'r4_5', 'r4_6', 'r4_7', 'r4_8', 'r4_9',
        'r4_10',
        'r5_1', 'r5_2', 'r5_3', 'r5_4'
    ]
    # 初分拣矩阵id
    WIG_ID_M = [
        'm1_1', 'm1_3', 'm1_2', 'm1_4', 'm2_1', 'm2_3', 'm2_5', 'm2_7', 'm2_9',
        'm2_2', 'm2_4', 'm2_6', 'm2_8', 'm2_10', 'm3_1', 'm3_2', 'm4_2', 'm4_4'
        , 'm4_6', 'm4_8', 'm4_1', 'm4_3', 'm4_5', 'm4_7'
    ]

    WIG_DIC = {
        'R': {
            'columns': 3,       # 视图的列数目
            'wig_id': WIG_ID_R  # 视图的id列表
        },
        'M': {
            'columns': 3,
            'wig_id': WIG_ID_M
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
                columns_var=0
                row_var += 1

            self.CHECK_BTN[id_wig] = {
                'attr': self.CHECK_BTN_ATTR,
                'grid': {
                    'row': row_var,
                    'column': columns_var*columns+0
                }
            }
            #  entry 视图设置
            self.ENTRY[id_wig] = {
                'attr': self.ENTRY_ATTR,
                'grid': {
                    'row': row_var,
                    'column': columns_var*columns+1
                }
            }
            #  combobox list 视图设置
            self.COMBOBOX_LIST[id_wig] = {
                'attr': self.COMBOBOX_LIST_ATTR,
                'grid': {
                    'row': row_var,
                    'column': columns_var*columns+2
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
