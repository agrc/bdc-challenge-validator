#!/usr/bin/env python
# * coding: utf8 *
"""
a description of what this module does.
this file is for testing linting...
"""

from . import version

TEST = 'test'


def hello():
    """doc string
    """
    print('this is good')

    print(
        'this is a really, really, really, really, really, really, really, really, really, really, really, really,'
        'really long line'
    )

    print(f'Version: {version.__version__}')

    return 'hi'


if __name__ == '__main__':
    #: the code that executes if you run the file or module directly
    GREETING = hello()
