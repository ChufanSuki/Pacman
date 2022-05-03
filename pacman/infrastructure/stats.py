
"""
This module is used to collect statistics from computations

Each node emits a set of statistics for each step it performed. A step is a
set of computations (compute costs, messages, select a value, etc.) it
performed in response to an event.
Event will generally be : either initialisation or the reception of a message
from another node.

"""

import logging

# When logged in a cvs file, statistics will be written in this order :
from time import time

columns = [
    'time',
    'start_time',  # start time for this step
    'duration',  # duration of the step
    'agent',  # agent hosting the node
    'node_name',  # nome of the node (e.g. name of the variable or factor)
    'node_type',  # type of the node which performed the step : factor, variable
    'step_num',  # number of this step for this node (0,1, 2,3...)
    'event_type',  # event that started the step: init, costs _msg, etc.
    'size_msg',  # size of msg,if the step was started by a message
    'num_msg_out',  # number of msg sent in this step
    'size_msg_out',  # total size of msg sent in this step
    'op_count',  # number of operations performed in this step
    'nc_op_count',  # Non-concurrent number of operations so far
    'current_value',  # for var node, the current selected value
]

computation_logger = logging.getLogger('computation')
logging_enabled = False

is_first = True

def set_stats_file(file_path):
    if not logging_enabled:
        return
    global is_first
    is_first = True
    handler = logging.FileHandler(file_path)
    msg_formatter = logging.Formatter('%(message)s')
    handler.setFormatter(msg_formatter)
    computation_logger.addHandler(handler)

def trace_computation(data):
    """
    Add a entry containing all the data from one computation step.

    :param data: a dict {key: value} where all the key must be defined in
    stats.columns.

    """
    if not logging_enabled:
        return
    global is_first
    if is_first:
        is_first = False
        computation_logger.info(', '.join(columns))

    ordered = [str(time())]
    for k in columns[1:]:
        if k in data:
            ordered.append(str(data[k]))
        else:
            ordered.append('')
    computation_logger.info(', '.join(ordered))

