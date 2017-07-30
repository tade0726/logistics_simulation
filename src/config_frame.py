# -*- coding: utf-8 -*-

from tkinter import *

FRAME_WIDTH = 1350  # 界面的总计宽度
FRAME_WIDTH_LEFT = 800  # 左侧界面的总计宽度
FRAME_WIDTH_RIGHT = 550  # 右侧界面的总计宽度
FRAME_WIDTH_LEFT_HALF = 350  #左侧界面的半宽度

FRAME_HEIGHT = 750  # 界面的总计高度
FRAME_HEIGHT_HEAD = 100  # 标题的高度
FRAME_HEIGHT_CENTER = 550  # 中间界面的总计高度
FRAME_HEIGHT_CENTER_PACKAGE = 50  # 包裹设置界面高度
FRAME_HEIGHT_BOTTOM = 50  # 底部界面的总高度
FRAME_HEIGHT_LEFT_CENTER = 330


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
                'bd': 2,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'left'}
        },
        'RIGHT_FRAME': {
            'attr': {
                # 'width': FRAME_WIDTH_RIGHT,
                # 'height': FRAME_HEIGHT,
                'bd': 2,
                'relief': 'raise',
                # 'bg': '#A2B5CD'
            },
            'pack': {'side': 'right'}
        },
        'LEFT_SET_PAD_TOP_R': {
            'attr': {
                # 'width': FRAME_WIDTH_LEFT,
                # 'height': 500,
                'bd': 2,
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
    R_CHECK_BTN = {
        'r1_1':{
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 0, 'column': 0, 'sticky': 'w'
            }},
        'r1_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 1, 'column': 0, 'sticky': 'w'
            }},
        'r1_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 2, 'column': 0, 'sticky': 'w'
            }},
        'r1_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 3, 'column': 0, 'sticky': 'w'
            }},
        'r2_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 4, 'column': 0, 'sticky': 'w'
            }},
        'r2_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 5, 'column': 0, 'sticky': 'w'
            }},
        'r2_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 6, 'column': 0, 'sticky': 'w'
            }},
        'r2_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 7, 'column': 0, 'sticky': 'w'
            }},
        'r3_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 8, 'column': 0, 'sticky': 'w'
            }},
        'r3_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 9, 'column': 0, 'sticky': 'w'
            }},
        'r3_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 10, 'column': 0, 'sticky': 'w'
            }},
        'r3_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 11, 'column': 0, 'sticky': 'w'
            }},
        'r4_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 12, 'column': 0, 'sticky': 'w'
            }},
        'r4_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 13, 'column': 0, 'sticky': 'w'
            }},
        'r4_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 14, 'column': 0, 'sticky': 'w'
            }},
        'r4_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 15, 'column': 0, 'sticky': 'w'
            }},
        'r5_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 0, 'column': 2, 'sticky': 'w'
            }},
        'r5_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 1, 'column': 2, 'sticky': 'w'
            }},
        'r5_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 2, 'column': 2, 'sticky': 'w'
            }},
        'r5_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 3, 'column': 2, 'sticky': 'w'
            }},
        'r6_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 4, 'column': 2, 'sticky': 'w'
            }},
        'r6_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 5, 'column': 2, 'sticky': 'w'
            }},
        'r6_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 6, 'column': 2, 'sticky': 'w'
            }},
        'r6_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 7, 'column': 2, 'sticky': 'w'
            }},
        'r7_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 8, 'column': 2, 'sticky': 'w'
            }},
        'r7_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 9, 'column': 2, 'sticky': 'w'
            }},
        'r7_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 10, 'column': 2, 'sticky': 'w'
            }},
        'r7_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 11, 'column': 2, 'sticky': 'w'
            }},
        'r8_1': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 12, 'column': 2, 'sticky': 'w'
            }},
        'r8_2': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 13, 'column': 2, 'sticky': 'w'
            }},
        'r8_3': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 14, 'column': 2, 'sticky': 'w'
            }},
        'r8_4': {
            'attr': R_CHECK_BTN_ATTR,
            'grid': {
                'row': 15, 'column': 2, 'sticky': 'w'
            }},

    }
    R_ENTRY_ATTR = {
        'font': ('arial', 10, 'bold'),
        'bd': 2, 'width': 6, 'justify': 'left',
        'state': DISABLED
    }
    R_ENTRY = {
        'r1_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 0, 'column': 1}},
        'r1_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 1, 'column': 1
            }},
        'r1_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 2, 'column': 1
            }},
        'r1_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 3, 'column': 1
            }},
        'r2_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 4, 'column': 1}},
        'r2_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 5, 'column': 1
            }},
        'r2_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 6, 'column': 1
            }},
        'r2_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 7, 'column': 1
            }},
        'r3_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 8, 'column': 1}},
        'r3_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 9, 'column': 1
            }},
        'r3_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 10, 'column': 1
            }},
        'r3_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 11, 'column': 1
            }},
        'r4_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 12, 'column': 1}},
        'r4_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 13, 'column': 1
            }},
        'r4_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 14, 'column': 1
            }},
        'r4_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 15, 'column': 1
            }},
        'r5_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 0, 'column': 3}},
        'r5_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 1, 'column': 3
            }},
        'r5_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 2, 'column': 3
            }},
        'r5_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 3, 'column': 3
            }},
        'r6_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 4, 'column': 3}},
        'r6_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 5, 'column': 3
            }},
        'r6_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 6, 'column': 3
            }},
        'r6_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 7, 'column': 3
            }},
        'r7_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 8, 'column': 3}},
        'r7_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 9, 'column': 3
            }},
        'r7_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 10, 'column': 3
            }},
        'r7_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 11, 'column': 3
            }},
        'r8_1': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 12, 'column': 3}},
        'r8_2': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 13, 'column': 3
            }},
        'r8_3': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 14, 'column': 3
            }},
        'r8_4': {
            'attr': R_ENTRY_ATTR,
            'grid': {
                'row': 15, 'column': 3
            }},
    }
