#!/usr/bin/env python
# * coding: utf8 *
"""
test_validator.py
A module that contains tests for the project module.
"""

from validator import main


def test_hello_returns_hi():
    assert main.hello() == 'hi'
