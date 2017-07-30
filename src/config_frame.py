# -*- coding: utf-8 -*-


from tkinter import *

FRAME_WIDTH = 1350
FRAME_WIDTH_LEFT = 700
FRAME_WIDTH_LEFT_HALF = 350
FRAME_WIDTH_RIGHT = 640
FRAME_HEIGHT = 750
FRAME_HEAD_HEIGHT = 100
FRAME_HEIGHT_LEFT_CENTER = 330

class ConfigApp(object):
    """"""

    RELOAD_FRAME = {
        'TOP_FRAME': {
        'attr': {
            'width': FRAME_WIDTH,
            'height': FRAME_HEAD_HEIGHT,
            'bd': 14,
            # 'relief': 'raise',
            'bg': '#A2B5CD'
        },
        'pack': {
            'side': 'top'}},
        'LEFT_FRAME': {
        'attr': {
            'width': FRAME_WIDTH_LEFT,
            'height': 650,
            'bd': 8,
            # 'relief': 'raise',
            'bg': '#A2B5CD'
        },
        'pack': {'side': 'left'}},
        'RIGHT_FRAME': {
        'attr': {
            'width': FRAME_WIDTH_RIGHT,
            'height': 650,
            'bd': 8,
            # 'relief': 'raise',
            'bg': '#A2B5CD'
        },
        'pack': {
            'side': 'right'}},
        'LEFT_SET_PAD_TOP': {
        'attr': {
            'width': FRAME_WIDTH_LEFT,
            'height': 450,
            'bd': 8,
            'relief': 'raise'},
        'pack': {
            'side': 'top'}},
        'LEFT_SET_PAD_BOTTOM': {
        'attr': {
            'width': FRAME_WIDTH_LEFT,
            'height': 100,
            'bd': 6,
            'relief': 'raise'},
        'pack': {
            'side': 'bottom'}},
        'LEFT_SET_PAD_TOP_PACKAGE': {
        'attr': {
            'width': FRAME_WIDTH_LEFT,
            'height': 100,
            'bd': 8,
            'relief': 'raise'
        },
        'pack': {
            'side': 'top'}
    },
        'LEFT_SET_PAD_BOTTOM_RESOURCE': {
            'attr': {
                'width': FRAME_WIDTH_LEFT, 'height': 100, 'bd': 8,
                'relief': 'raise'},
                'pack': {
                    'side': 'top'
            }
        },
        'LEFT_SET_PAD_CENTER_LEFT': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_HALF,
                'height': FRAME_HEIGHT_LEFT_CENTER,
                'bd': 8,
                'relief': 'raise'},
            'pack': {
                'side': 'left'
            }
        },
        'LEFT_SET_PAD_CENTER_RIGHT': {
            'attr': {
                'width': FRAME_WIDTH_LEFT_HALF,
                'height': FRAME_HEIGHT_LEFT_CENTER,
                'bd': 8,
                'relief': 'raise'},
            'pack': {
                'side': 'right'
            }
        },
        'RIGHT_OUTPUT_PAD': {
        'attr': {
            'width': FRAME_WIDTH_RIGHT, 'height': 650, 'bd': 12,
            'relief': 'raise', 'bg': '#A2B5CD'},
        'pack': {'side': 'top'}
    },
        'RIGHT_OUTPUT_BUTTON': {
        'attr': {
            'width': FRAME_WIDTH_RIGHT, 'height': 50, 'bd': 16,
            'relief': 'raise'},
        'pack': {'side': 'bottom'}
    },
    }
    TOP_FRAME = {
        'attr': {
            'width': FRAME_WIDTH,
            'height': FRAME_HEAD_HEIGHT,
            'bd': 14,
            # 'relief': 'raise',
            'bg': '#A2B5CD'
        },
        'pack': {
            'side': 'top'}}
    LEFT_FRAME = {
        'attr': {
            'width': FRAME_WIDTH_LEFT,
            'height': 650,
            'bd': 8,
            # 'relief': 'raise',
            'bg': '#A2B5CD'
        },
        'pack': {'side': 'left'}}
    RIGHT_FRAME = {
        'attr': {
            'width': FRAME_WIDTH_RIGHT,
            'height': 650,
            'bd': 8,
            # 'relief': 'raise',
            'bg': '#A2B5CD'
        },
        'pack': {
            'side': 'right'}}
    LEFT_SET_PAD_TOP = {
        'attr': {
            'width': FRAME_WIDTH_LEFT,
            'height': 450,
            'bd': 8,
            'relief': 'raise'},
        'pack': {
            'side': 'top'}}
    LEFT_SET_PAD_BOTTOM = {
        'attr': {
            'width': FRAME_WIDTH_LEFT,
            'height': 100,
            'bd': 6,
            'relief': 'raise'},
        'pack': {
            'side': 'bottom'}}
    LEFT_SET_PAD_TOP_PACKAGE = {
        'attr': {
            'width': FRAME_WIDTH_LEFT,
            'height': 100,
            'bd': 8,
            'relief': 'raise'
        },
        'pack': {
            'side': 'top'}
    }
    LEFT_SET_PAD_BOTTOM_RESOURCE = {
        'attr': {
            'width': FRAME_WIDTH_LEFT, 'height': 100, 'bd': 8,
            'relief': 'raise'},
        'pack': {
            'side': 'top'}
    }
    RIGHT_OUTPUT_PAD = {
        'attr': {
            'width': FRAME_WIDTH_RIGHT, 'height': 650, 'bd': 12,
            'relief': 'raise', 'bg': '#A2B5CD'},
        'pack': {'side': 'top'}
    }
    RIGHT_OUTPUT_BUTTON = {
        'attr': {
            'width': FRAME_WIDTH_RIGHT, 'height': 50, 'bd': 16,
            'relief': 'raise'},
        'pack': {'side': 'bottom'}
    }
    pass
