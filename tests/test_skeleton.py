#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from translates.skeleton import fib

__author__ = "Andrey Vasnetsov"
__copyright__ = "Andrey Vasnetsov"
__license__ = "mit"


def test_fib():
    assert fib(1) == 1
    assert fib(2) == 1
    assert fib(7) == 13
    with pytest.raises(AssertionError):
        fib(-10)
