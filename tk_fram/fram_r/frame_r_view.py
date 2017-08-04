# -*- coding: utf-8 -*-

from tkinter import *

#  ====================宽度设置参数=================
FRAME_WIDTH = 1100  # 界面的总计宽度
FRAME_HEIGHT = 650  # 界面的总计高度

FRAME_WIDTH_LEFT = 700  # 左侧界面的总计宽度
FRAME_WIDTH_RIGHT = 400  # 右侧界面的总计宽度

FRAME_WIDTH_LEFT_ONE = 200  # 左侧界面的左宽度
FRAME_WIDTH_LEFT_TOW = 500  # 左侧界面的右宽度

#  ===================高度设置参数===================
FRAME_HEIGHT_HEAD = 50  # 界面顶端主标题的高度

#  ===================左侧设置界面高度设置============
#                        50+50+500
FRAME_HEIGHT_LEFT_PACKAGE = 50  # 包裹设置界面高度
FRAME_HEIGHT_LEFT_SET_PAD_TITLE = 50  # 左侧设置界面标题高度
FRAME_HEIGHT_LEFT_CENTER = 500  # 左侧中间界面的总计高度

#  ===================右侧输出界面高度设置============
#                           50+50+500
FRAME_HEIGHT_RIGHT_INFO_TITLE = 40  # 输出信息板标题高度
FRAME_HEIGHT_RIGHT_INFO = 510  # 输出信息版高度
FRAME_HEIGHT_RIGHT_BUTTON = 50  # 右侧底部界面button的总高度

DATABASES = {
    'HOST': '10.0.149.62',
    'USER': 'root',
    'PASSWORD': 'root123',
    'NAME': 'test3',
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
        'LEFT_SET_PAD_CENTER_LEFT': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_ONE,
                'height': FRAME_HEIGHT_LEFT_CENTER,
                'bd': 8,
                'relief': 'raise'
            },
            'pack': {'side': 'left'}
        },
        'LEFT_SET_PAD_CENTER_RIGHT': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_TOW,
                'height': FRAME_HEIGHT_LEFT_CENTER,
                'bd': 8,
                'relief': 'raise'},
            'pack': {'side': 'right'}
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
    R_CHECK_BTN_ATTR = {
        'font': ('Times', 15, 'bold'),
        'onvalue': 1,
        'offvalue': 0,
        'bd': 6,
        'height': 1,
        'pady': 10,
        # 'padx': 1,
        # 'height': 2,
            }
    R_ENTRY_ATTR = {
        'font': ('Times', 15, 'bold'),
        'bd': 8,
        'width': 6,
        # 'height': 2,
        'justify': 'left',
        'state': DISABLED
    }
    CHECK_BTN_R_ZERO_COLUMN = 0
    CHECK_BTN_R_TOW_COLUMN = 2
    CHECK_BTN_R_Four_COLUMN = 4

    ENTRY_R_ONE_COLUMN = 1
    ENTRY_R_THREE_COLUMN = 3
    ENTRY_R_FIVE_COLUMN = 5

    ENTRY_A_ROW_BASE = 1
    ENTRY_R_ROW_BASE = 1
    CHECK_BTN_R_ROW_BASE = 1
    CHECK_BTN_A_ROW_BASE = 1

    R_CHECK_BTN = {
        'r1_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+0,
                'column': CHECK_BTN_R_ZERO_COLUMN,
                'sticky': 'w'
            }},
        'r1_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+1,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r1_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+2,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r1_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+3,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r2_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+4,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r2_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+5,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r2_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+6,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r2_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+7,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+0,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+1,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+2,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+3,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_5': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+4,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_6': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+5,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_7': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+6,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_8': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+7,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_9': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+0,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r3_10': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+1,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r4_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+2,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r4_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+3,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r4_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+4,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r4_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+5,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r4_5': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+6,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r4_6': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+7,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        # ==================================2===================================
        'r4_7': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+0,
                'column': CHECK_BTN_R_Four_COLUMN, 'sticky': 'w'
            }},
        'r4_8': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+1,
                'column': CHECK_BTN_R_Four_COLUMN, 'sticky': 'w'
            }},
        'r4_9': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+2,
                'column': CHECK_BTN_R_Four_COLUMN, 'sticky': 'w'
            }},
        'r4_10': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+3,
                'column': CHECK_BTN_R_Four_COLUMN, 'sticky': 'w'
            }},
        'r5_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+4,
                'column': CHECK_BTN_R_Four_COLUMN, 'sticky': 'w'
            }},
        'r5_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+5,
                'column': CHECK_BTN_R_Four_COLUMN, 'sticky': 'w'
            }},
        'r5_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+6,
                'column': CHECK_BTN_R_Four_COLUMN, 'sticky': 'w'
            }},
        'r5_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+7,
                'column': CHECK_BTN_R_Four_COLUMN, 'sticky': 'w'
            }},

    }
    R_ENTRY = {
        'r1_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+0, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r1_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+1, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r1_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+2, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r1_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+3, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r2_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+4, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r2_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+5, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r2_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+6, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r2_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+7, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+0, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+1, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+2, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+3, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_5': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+4, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_6': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+5, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_7': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+6, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_8': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+7, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_9': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+0, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r3_10': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+1, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r4_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+2, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r4_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+3, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r4_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+4, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r4_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+5, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r4_5': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+6, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r4_6': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+7, 'column': ENTRY_R_THREE_COLUMN
            }},
        # =====================================5 column======================
        'r4_7': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+0, 'column': ENTRY_R_FIVE_COLUMN
            }},
        'r4_8': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+1, 'column': ENTRY_R_FIVE_COLUMN
            }},
        'r4_9': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+2, 'column': ENTRY_R_FIVE_COLUMN
            }},
        'r4_10': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+3, 'column': ENTRY_R_FIVE_COLUMN
            }},
        'r5_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+4, 'column': ENTRY_R_FIVE_COLUMN
            }},
        'r5_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+5, 'column': ENTRY_R_FIVE_COLUMN
            }},
        'r5_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+6, 'column': ENTRY_R_FIVE_COLUMN
            }},
        'r5_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+7, 'column': ENTRY_R_FIVE_COLUMN
            }},
    }
