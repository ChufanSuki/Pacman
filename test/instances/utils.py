"""Various utility fonctions for cli end2end tests"""
import sys
from os import path


def instance_path(instance_filename):
    """
    Build the path to an tests instance file.
    :param instance_filename: the test instance file name
    :return:
    """
    cur_dir = sys.modules[__name__].__file__
    dir_name = path.dirname(cur_dir)
    test_file_path = path.join(dir_name, instance_filename)
    return test_file_path