# Simple Math Utils

一个简单的数学工具库，提供基本的数学运算功能。

## 功能特点

- 提供基本的数学运算：加法、减法、乘法、除法
- 内置类型提示支持
- 详细的文档和示例
- 完整的测试覆盖
- 健壮的错误处理和日志记录

## 安装

使用pip安装：

```bash
pip install dongjak-math-utils
```

## 使用方法

### 基本用法

```python
from dongjak_math_utils import add, subtract, multiply, divide

# 基本运算
result = add(10, 5)      # 15
result = subtract(10, 5)  # 5
result = multiply(10, 5)  # 50
result = divide(10, 5)    # 2.0

# 支持浮点数
result = add(3.14, 2.71)  # 5.85
```

### 高级用法

```python
# 链式操作
result = divide(multiply(add(10, 5), subtract(8, 3)), 2)
# 等同于 ((10 + 5) * (8 - 3)) / 2 = 37.5
```

## 开发

### 环境设置

1. 克隆仓库
2. 创建并激活虚拟环境
3. 安装开发依赖

```bash
git clone https://github.com/yourusername/dongjak-math-utils.git
cd dongjak-math-utils
python -m venv .venv
.venv\Scripts\activate  # Windows
source .venv/bin/activate  # Linux/Mac
pip install -e ".[dev]"
```

### 运行测试

```bash
pytest
```

### 发布到PyPI

本项目使用Hatch作为构建和发布工具。以下是发布到PyPI的步骤：

#### 1. 安装Hatch

```bash
pip install hatch
# 或使用uv
uv pip install hatch
```

#### 2. 配置PyPI凭证

有两种方式配置PyPI凭证：

**方式一：使用API令牌（推荐）**

1. 在[PyPI官网](https://pypi.org/manage/account/)注册并登录账号
2. 在账号设置中创建API令牌
3. 创建`~/.pypirc`文件：

```
[pypi]
username = __token__
password = pypi-AgEIcHlwaS5vcmcCJDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

**方式二：使用环境变量**

```bash
# Windows (PowerShell)
$env:HATCH_INDEX_USER="__token__"
$env:HATCH_INDEX_AUTH="pypi-AgEIcHlwaS5vcmcCJDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

# Linux/Mac
export HATCH_INDEX_USER=__token__
export HATCH_INDEX_AUTH=pypi-AgEIcHlwaS5vcmcCJDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

#### 3. 构建分发包

```bash
hatch build
```

这将在`dist/`目录下创建源代码分发包（.tar.gz）和轮子分发包（.whl）。

#### 4. 发布到PyPI

```bash
hatch publish
```

如果您想先在测试环境（TestPyPI）上发布：

```bash
hatch publish -r test
```

#### 5. 验证发布

发布成功后，您可以通过pip安装您的包来验证：

```bash
pip install dongjak-math-utils
```

## 许可证

MIT

## 项目结构

```
dongjak_math_utils/
├── dongjak_math_utils/       # 主库目录
│   ├── __init__.py          # 导出公共API
│   ├── core.py              # 核心功能
├── tests/                   # 测试目录
│   └── test_core.py         # 核心功能测试
└── examples/                # 示例目录
    └── basic_usage.py       # 基本用法示例
