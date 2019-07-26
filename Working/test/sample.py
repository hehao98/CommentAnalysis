"""
This is a file header comment
"""

import numpy as np


def function(a, b):
    """
    This is a function header comment
    """
    return a + b


def func_no_doc(a, b):
    # This is a normal comment
    return a - b


class C(object):
    a = 0

    def abs(a):
        '''Documentation Here'''
        return -a


if __name__ == "__main__":
    # This is another normal comment
    function(1, 2)
    func_no_doc(2, 1)
