# -*- coding: utf-8 -*-

from tkinter import *

FRAME_WIDTH = 1350  # 界面的总计宽度
FRAME_WIDTH_LEFT = 800  # 左侧界面的总计宽度
FRAME_WIDTH_RIGHT = 550  # 右侧界面的总计宽度  vc
FRAME_WIDTH_LEFT_HALF = 350  #左侧界面的半宽度

FRAME_HEIGHT = 750  # 界面的总计高度
FRAME_HEIGHT_HEAD = 100  # 标题的高度
FRAME_HEIGHT_CENTER = 550  # 中间界面的总计高度
FRAME_HEIGHT_CENTER_PACKAGE = 50  # 包裹设置界面高度
FRAME_HEIGHT_BOTTOM = 50  # 底部界面的总高度
FRAME_HEIGHT_LEFT_CENTER = 330

DATABASES = {
    'HOST': '',
    'USER': '',
    'PASSWORD': '',
    'NAME': '',
    'CHARSET': 'utf8'
}

class ConfigApp(object):
    """"""
    RELOAD_FRAME = {
        'TOP_FRAME': {
            'attr': {
                # 'width': FRAME_WIDTH,
                # 'height': FRAME_HEIGHT_HEAD,
                'bd': 7,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'top'}
        },
        'LEFT_FRAME': {
            'attr': {
                # 'width': FRAME_WIDTH_LEFT,
                # 'height': FRAME_HEIGHT,
                'bd': 8,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'left'}
        },
        'RIGHT_FRAME': {
            'attr': {
                # 'width': FRAME_WIDTH_RIGHT,
                # 'height': FRAME_HEIGHT,
                'bd': 8,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'right'}
        },
        'LEFT_SET_PAD_TOP_R': {
            'attr': {
                # 'width': FRAME_WIDTH_LEFT,
                # 'height': 500,
                'bd': 8,
                'relief': 'raise'
            },
            'pack': {
                'side': 'top'}
        },
        'LEFT_SET_PAD_BOTTOM': {
            'attr': {
                'width': FRAME_WIDTH_LEFT,
                'height': 100,
                'bd': 2,
                'relief': 'raise'},
            'pack': {
                'side': 'bottom'}
        },
        'LEFT_SET_PAD_TOP_PACKAGE': {
            'attr': {
                # 'width': FRAME_WIDTH_LEFT,
                # 'height': 50,
                'bd': 2,
                'relief': 'raise'
            },
            'pack': {'side': 'top'}
        },
        'LEFT_SET_PAD_BOTTOM_RESOURCE': {
            'attr': {
                # 'width': FRAME_WIDTH_LEFT,
                # 'height': FRAME_HEIGHT_BOTTOM,
                'bd': 2,
                'relief': 'raise'},
            'pack': {'side': 'bottom'}
        },
        'LEFT_SET_PAD_CENTER_LEFT': {
            'attr': {
                # 'width': FRAME_WIDTH_LEFT_HALF,
                # 'height': FRAME_HEIGHT_CENTER,
                'bd': 8,
                'relief': 'raise'},
            'pack': {'side': 'left'}
        },
        'LEFT_SET_PAD_CENTER_RIGHT': {
            'attr': {
                # 'width': FRAME_WIDTH_LEFT_HALF,
                # 'height': FRAME_HEIGHT_CENTER,
                'bd': 8,
                'relief': 'raise'},
            'pack': {'side': 'right'}
        },
        'RIGHT_TITLE': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': 50,
                'bd': 2,
                # 'relief': 'raise'
            },
            'pack': {'side': 'top'}
        },
        'RIGHT_OUTPUT_PAD_INFO': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT_CENTER,
                'bd': 2,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'top'}
        },
        'RIGHT_BUTTON': {
            'attr': {
                'width': FRAME_WIDTH_RIGHT,
                'height': FRAME_HEIGHT_BOTTOM,
                'bd': 2,
                # 'relief': 'raise'
            },
            'pack': {'side': 'bottom'}
        }
    }


class ConfigCheckBtn(object):
    """选择控件"""
    R_CHECK_BTN_ATTR = {
                'onvalue': 1,
                'offvalue': 0,
                'font': ('arial', 10, 'bold')
            }
    R_ENTRY_ATTR = {
        'font': ('arial', 10, 'bold'),
        'bd': 2, 'width': 6, 'justify': 'left',
        'state': DISABLED
    }
    CHECK_BTN_R_ZERO_COLUMN = 0
    CHECK_BTN_R_TOW_COLUMN = 2
    CHECK_BTN_A_ZERO_COLUMN = 0

    ENTRY_R_ONE_COLUMN = 1
    ENTRY_R_THREE_COLUMN = 3
    ENTRY_A_ONE_COLUMN = 1

    ENTRY_A_ROW_BASE = 1
    ENTRY_R_ROW_BASE = 1
    CHECK_BTN_R_ROW_BASE = 1
    CHECK_BTN_A_ROW_BASE =1

    R_CHECK_BTN = {
        'r1_1':{
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
                'row': CHECK_BTN_R_ROW_BASE+8,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+9,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+10,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r3_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+11,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r4_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+12,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r4_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+13,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r4_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+14,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r4_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+15,
                'column': CHECK_BTN_R_ZERO_COLUMN, 'sticky': 'w'
            }},
        'r5_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+0,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r5_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+1,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r5_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+2,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'r5_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_R_ROW_BASE+3,
                'column': CHECK_BTN_R_TOW_COLUMN, 'sticky': 'w'
            }},
        'a1_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+0,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+1,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+2,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+3,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_5': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+4,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_6': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+5,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_7': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+6,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_8': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+7,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_9': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+8,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_10': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+9,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_11': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+10,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
            }},
        'a1_12': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': CHECK_BTN_A_ROW_BASE+11,
                'column': CHECK_BTN_A_ZERO_COLUMN, 'sticky': 'w'
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
                'row': ENTRY_R_ROW_BASE+8, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+9, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+10, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r3_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+11, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r4_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+12, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r4_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+13, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r4_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+14, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r4_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+15, 'column': ENTRY_R_ONE_COLUMN
            }},
        'r5_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+0, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r5_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+1, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r5_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+2, 'column': ENTRY_R_THREE_COLUMN
            }},
        'r5_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_R_ROW_BASE+3, 'column': ENTRY_R_THREE_COLUMN
            }},
        'a1_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+0, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+1, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+2, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+3, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_5': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+4, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_6': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+5, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_7': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+6, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_8': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+7, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_9': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+8, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_10': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+9, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_11': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+10, 'column': ENTRY_A_ONE_COLUMN
            }},
        'a1_12': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': ENTRY_A_ROW_BASE+11, 'column': ENTRY_A_ONE_COLUMN
            }},
    }
