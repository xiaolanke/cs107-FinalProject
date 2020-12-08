"""Test the interface for the reverse mode in farad package.
"""

import pytest
import numpy as np
from farad.elem import *
import farad.driverRAD as rad


def test_get_forwardpass1f():
    """Test of _forwardpass1f method, i.e., testing one-function situation"""
    def f(x):
        return sin(x)
    function = rad.AutoDiff(f)

    # test scalar input
    function.forwardpass(1.0)
    try:
        assert function.get_val() == np.sin(1.0)
        assert function.reverse() == np.cos(1.0)
    except AssertionError as e:
        print(e)
        raise AssertionError

    # test fi(x) at different x values
    function.forwardpass([1.0,2.0])
    try:
        assert function.get_val() == np.sin([1.0,2.0])
        assert function.reverse() == np.cos([1.0,2.0])
    except AssertionError as e:
        print(e)
        raise AssertionError

    def f2d(x, y):
        return x * y

    function = rad.AutoDiff(f2d)
    # test f2d(x,y) at point (x,y)
    function.forwardpass([1,2])
    try:
        assert function.get_val() == 2.
        assert np.array_equal(function.reverse(), [2,1])
    except AssertionError as e:
        print(e)
        raise AssertionError

    # test f2d(x,y) at multiple points, i.e., (x,y) and (x1, y1)
    function.forwardpass([[1,2],[3,4]])
    try:
        assert np.array_equal(function.get_val(), [2,12])
        assert np.array_equal(function.reverse(), [[2,1],[4,3]])
    except AssertionError as e:
        print(e)
        raise AssertionError

def test_get_forwardpass():
    """Test of _forwardpass method, i.e., testing vector function situation"""
    def f1(x):
        return sin(x)

    def f2(x):
        return cos(x)

    function = rad.AutoDiff([f1, f2])
    # test scalar input
    function.forwardpass(1.0)
    try:
        assert np.array_equal(function.get_val(), [np.sin(1), np.cos(1)])
        assert np.array_equal(function.reverse(), [np.cos(1), -np.sin(1)])
    except AssertionError as e:
        print(e)
        raise AssertionError

    # test [f1(x),f2(x)] at different x values
    function.forwardpass([1,2])
    try:
        assert np.array_equal(function.get_val(), [[np.sin(1), np.cos(1)],[np.sin(2), np.cos(2)]])
        assert np.array_equal(function.reverse(), [[np.cos(1), -np.sin(1)],[np.cos(2), -np.sin(2)]])
    except AssertionError as e:
        print(e)
        raise AssertionError

    def f2d1(x, y):
        return x * y

    def f2d1(x, y):
        return 2* x * y

    # test [f2d1(x,y), f2d1(x,y)] at point (x,y)
    function.forwardpass([1,2])
    try:
        assert np.array_equal(function.get_val(),[2,4])
        assert np.array_equal(function.reverse(), [[2,1],[4,2]])
    except AssertionError as e:
        print(e)
        raise AssertionError

    # test [f2d1(x,y), f2d1(x,y)] at multiple points, i.e., (x,y) and (x1, y1)
    function.forwardpass([[1,2],[3,4]])
    try:
        assert np.array_equal(function.get_val(),[[2,4],[12,24]])
        assert np.array_equal(function.reverse(), [[[2,1],[4,2]],[[4,3],[8,6]]])
    except AssertionError as e:
        print(e)
        raise AssertionError