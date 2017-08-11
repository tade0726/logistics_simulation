# -*- coding: utf-8 -*-

from tkinter import DISABLED

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
FRAME_HEIGHT_LEFT_SET_PAD_TITLE = 50  # 左侧设置界面标题高度
FRAME_HEIGHT_LEFT_CENTER = 500  # 左侧中间界面的总计高度
FRAME_HEIGHT_LEFT_CENTER_UP = 250   # 左侧设置界面画布的上高度
FRAME_HEIGHT_LEFT_CENTER_DOWN = 250  # 左侧设置界面画布的下高度
#  ===================右侧输出界面高度设置============
#                           50+50+500
FRAME_HEIGHT_RIGHT_INFO_TITLE = 40  # 输出信息板标题高度
FRAME_HEIGHT_RIGHT_INFO = 510  # 输出信息版高度
FRAME_HEIGHT_RIGHT_BUTTON = 50  # 右侧底部界面button的总高度

# 判断数据更新操作是否已执行
Flag = {
    'update_data': 0,
    'run_sim': 0,
    'save_data': 0,
    'run_time': None
}

ENTRY_STATUS_DIC = {0: 'OFF', 1: 'ON'}

BTN_ENTRY_DICT = {}

CHECK_BTN_ENTRY_DIC = {}

DATABASES = {
    'HOST': '10.0.149.62',
    'USER': 'root',
    'PASSWORD': 'root123',
    'NAME': 'hangzhouhubland',
    'CHARSET': 'utf8'
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
        'LEFT_SET_PAD_LEFT_TITLE': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_ONE,
                'height': FRAME_HEIGHT_LEFT_SET_PAD_TITLE,
                'bd': 2,
                # 'relief': 'raise'
            },
            'pack': {'side': 'left'}
        },
        'LEFT_SET_PAD_RIGHT_TITLE': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_TOW,
                'height': FRAME_HEIGHT_LEFT_SET_PAD_TITLE,
                'bd': 2,
                # 'relief': 'raise'
            },
            'pack': {
                'side': 'left'}
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


class ConfigCheckBtn(object):
    """选择控件"""
    WIG_ID_R = [
        'r1_1', 'r1_2', 'r1_3', 'r1_4',
        'r2_1', 'r2_2', 'r2_3', 'r2_4',
        'r3_1', 'r3_2', 'r3_3', 'r3_4', 'r3_5', 'r3_6', 'r3_7', 'r3_8', 'r3_9',
        'r3_10',
        'r4_1', 'r4_2', 'r4_3', 'r4_4', 'r4_5', 'r4_6', 'r4_7', 'r4_8', 'r4_9',
        'r4_10',
        'r5_1', 'r5_2', 'r5_3', 'r5_4'
    ]
    WIG_ID_M = [

    ]

    WIG_DIC = {
        'left': {
            'rows': 8,
            'columns': 1,
            'wig_id': WIG_ID_LEFT
        },
        'right': {
            'rows': 8,
            'columns': 3,
            'wig_id': WIG_ID_RIGHT
        }
    }

    CHECK_BTN_ATTR = {
        'font': ('Times', 15, 'bold'),
        'onvalue': 1,
        'offvalue': 0,
        'bd': 6,
        'height': 1,
        'pady': 10,
        # 'padx': 1,
        # 'height': 2,
        }
    ENTRY_ATTR = {
        'font': ('Times', 15, 'bold'),
        'bd': 8,
        'width': 6,
        # 'height': 2,
        'justify': 'left',
        'state': DISABLED
    }
    #  初始化check_btn视图字典
    CHECK_BTN = {}
    #  初始化entry视图字典
    ENTRY = {}


class CheckBtnEntryView(ConfigCheckBtn):

    def __init__(self):
        super().__init__()

    def _init_one_view(self, wig_id, rows, columns):
        grid_num = 0
        if len(wig_id) == rows * columns:
            for i in range(columns):
                for j in range(rows):
                    #  check_btn 视图设置
                    self.CHECK_BTN[wig_id[i * rows + j]] = {
                        'attr': self.CHECK_BTN_ATTR,
                        'grid': {
                            'row': j,
                            'column': i + grid_num
                        }
                    }
                    #  entry 视图设置
                    self.ENTRY[wig_id[i * rows + j]] = {
                        'attr': self.ENTRY_ATTR,
                        'grid': {
                            'row': j,
                            'column': i + grid_num + 1
                        }
                    }
                # 更新列值
                grid_num += 1
        else:
            raise ValueError('wig_id numbers not equal to '
                             'rows*columns numbers!')

    def init_view(self):
        #  记录绝对列数
        for _, v in self.WIG_DIC.items():
            self._init_one_view(
                wig_id=v['wig_id'],
                rows=v['rows'],
                columns=v['columns']
            )
