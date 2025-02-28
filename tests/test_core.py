"""
测试核心数学函数
"""

import pytest
from dongjak_math_utils import add, subtract, multiply, divide


def test_add():
    """测试加法函数"""
    assert add(1, 2) == 3
    assert add(-1, 1) == 0
    assert add(1.5, 2.5) == 4.0


def test_subtract():
    """测试减法函数"""
    assert subtract(3, 1) == 2
    assert subtract(1, 3) == -2
    assert subtract(5.5, 2.5) == 3.0


def test_multiply():
    """测试乘法函数"""
    assert multiply(2, 3) == 6
    assert multiply(-2, 3) == -6
    assert multiply(2.5, 2) == 5.0


def test_divide():
    """测试除法函数"""
    assert divide(6, 2) == 3.0
    assert divide(5, 2) == 2.5
    assert divide(-6, 2) == -3.0
    
    # 测试除以0的情况
    with pytest.raises(ZeroDivisionError):
        divide(5, 0)
