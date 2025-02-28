"""
核心数学函数模块

提供基本的数学运算功能。
"""

import logging
from typing import Union

# 设置日志记录
logger = logging.getLogger(__name__)

Number = Union[int, float]


def add(a: Number, b: Number) -> Number:
    """
    计算两个数的和。

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两个数的和

    Examples:
        >>> add(1, 2)
        3
        >>> add(1.5, 2.5)
        4.0
    """
    logger.debug(f"计算 {a} + {b}")
    return a + b


def subtract(a: Number, b: Number) -> Number:
    """
    计算两个数的差。

    Args:
        a: 被减数
        b: 减数

    Returns:
        两个数的差

    Examples:
        >>> subtract(3, 1)
        2
        >>> subtract(5.5, 2.5)
        3.0
    """
    logger.debug(f"计算 {a} - {b}")
    return a - b


def multiply(a: Number, b: Number) -> Number:
    """
    计算两个数的乘积。

    Args:
        a: 第一个数
        b: 第二个数

    Returns:
        两个数的乘积

    Examples:
        >>> multiply(2, 3)
        6
        >>> multiply(2.5, 2)
        5.0
    """
    logger.debug(f"计算 {a} * {b}")
    return a * b


def divide(a: Number, b: Number) -> Number:
    """
    计算两个数的商。

    Args:
        a: 被除数
        b: 除数

    Returns:
        两个数的商

    Raises:
        ZeroDivisionError: 当除数为0时抛出

    Examples:
        >>> divide(6, 2)
        3.0
        >>> divide(5, 2)
        2.5
    """
    if b == 0:
        logger.error("除数不能为0")
        raise ZeroDivisionError("除数不能为0")
    
    logger.debug(f"计算 {a} / {b}")
    return a / b
