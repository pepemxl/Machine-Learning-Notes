import sys


def is_unittest():
    if 'unittest' in sys.modules.keys():
        return True
    return False