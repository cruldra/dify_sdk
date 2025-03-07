# Dify SDK

一个简单的数学工具库，提供基本的数学运算功能。同时支持Dify API的事件处理功能。

## 功能特点

- 提供基本的数学运算：加法、减法、乘法、除法
- 内置类型提示支持
- 详细的文档和示例
- 完整的测试覆盖
- 健壮的错误处理和日志记录
- **新增：** 支持Dify API的事件处理，包括聊天消息、Agent消息等多种事件类型
- **新增：** 支持停止消息生成功能，可以中断正在进行的AI响应

## 安装

使用pip安装：

```bash
pip install dify_sdk
```

## 使用方法

### 基本用法

```python
from dify_sdk import add, subtract, multiply, divide

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

### 事件处理

```python
from dify.app.event_schemas import ConversationEvent, parse_event
from dify.app.schemas import ConversationEventType

# 解析事件
json_data = {
    "event": "message",
    "message_id": "msg_123",
    "conversation_id": "conv_456",
    "answer": "这是一个消息回复",
    "created_at": 1646035200
}

# 自动解析为对应的事件类型
event = parse_event(json_data)

# 根据事件类型处理
if event.event == ConversationEventType.MESSAGE:
    print(f"收到消息: {event.answer}")
elif event.event == ConversationEventType.ERROR:
    print(f"发生错误: {event.message}")
```

### 停止消息生成

```python
from dify import DifyClient
from dify.app.schemas import ApiKey

# 创建客户端
client = DifyClient()

# 停止正在生成的消息
async def stop_message_example():
    # 创建API密钥对象
    api_key = ApiKey(
        id="",
        type="api",
        token="your_api_key_here",
        last_used_at=0,
        created_at=0,
    )
    
    # 调用stop_message方法停止消息生成
    result = await client.app.stop_message(
        api_key=api_key,
        task_id="task_id_here",
        user_id="user_id_here"
    )
    
    print(f"停止结果: {result.result}")
```

更详细的示例请参考 `examples/stop_message_example.py`。

## 开发

### 环境设置

1. 克隆仓库
2. 创建并激活虚拟环境
3. 安装开发依赖

```bash
git clone https://github.com/yourusername/dify_sdk.git
cd dify_sdk
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
pip install dify_sdk
```

## 许可证

MIT

## 项目结构

```
dify_sdk/
├── dify/                    # 主库目录
│   ├── __init__.py          # 导出公共API
│   ├── app/                 # 应用相关功能
│   │   ├── __init__.py
│   │   ├── schemas.py       # 数据模型定义
│   │   ├── event_schemas.py # 事件模型定义
├── tests/                   # 测试目录
│   ├── test_core.py         # 核心功能测试
│   └── test_event_schemas.py # 事件模型测试
└── examples/                # 示例目录
    ├── basic_usage.py       # 基本用法示例
    ├── event_example.py     # 事件处理示例
    └── stop_message_example.py # 停止消息生成示例
```

## 最近更新

### 1.2.0 (2023-03-05)

- 新增：支持停止消息生成功能
  - 添加了`stop_message`方法，用于中断正在进行的AI响应
  - 提供了详细的示例代码和测试用例
  - 完善了文档说明

### 1.1.0 (2023-03-04)

- 新增：支持Dify API的事件处理功能
  - 添加了`ConversationEvent`联合类型，支持多种事件类型的处理
  - 提供了`parse_event`函数，用于根据事件类型自动解析事件对象
  - 添加了事件处理示例和测试用例
