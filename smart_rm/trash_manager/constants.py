# -*- coding: utf-8 -*-

import simple_rm.constants as trash_const

MAX_ITEMS_PER_TASK = 10000

REMOVE_MODES_MAPPING = (
    ('F', trash_const.REMOVE_FILE_MODE),
    ('D', trash_const.REMOVE_EMPTY_DIRECTORY_MODE),
    ('R', trash_const.REMOVE_TREE_MODE)
)

TASK_STATUS_MAPPING = (
    ('R', 'running'),
    ('C', 'completed'),
    ('W', 'waiting')
)
