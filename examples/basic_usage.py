"""
dongjak-math-utils 基本用法示例
"""

import logging
from dongjak_math_utils import add, subtract, multiply, divide

# 设置日志级别
logging.basicConfig(level=logging.DEBUG)

def main():
    """演示基本用法"""
    print("简单数学工具库演示")
    print("-" * 20)
    
    # 加法示例
    result = add(10, 5)
    print(f"10 + 5 = {result}")
    
    # 减法示例
    result = subtract(10, 5)
    print(f"10 - 5 = {result}")
    
    # 乘法示例
    result = multiply(10, 5)
    print(f"10 * 5 = {result}")
    
    # 除法示例
    result = divide(10, 5)
    print(f"10 / 5 = {result}")
    
    # 浮点数示例
    result = add(3.14, 2.71)
    print(f"3.14 + 2.71 = {result}")
    
    print("\n高级用法 - 链式操作")
    # 链式操作示例
    result = divide(multiply(add(10, 5), subtract(8, 3)), 2)
    print(f"((10 + 5) * (8 - 3)) / 2 = {result}")


if __name__ == "__main__":
    main()
