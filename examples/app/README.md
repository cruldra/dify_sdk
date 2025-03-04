# Dify SDK 示例

本目录包含了使用 Dify SDK 的各种示例代码，帮助您快速上手和理解如何使用该SDK。

## 环境准备

在运行示例之前，请确保：

1. 已安装所有必要的依赖
2. 创建了 `.env` 文件，包含以下环境变量：
   ```
   DIFY_API_KEY=your_api_key_here
   DIFY_BASE_URL=https://api.dify.ai  # 或您的自定义Dify实例URL
   ```

## 示例列表

### 1. 获取应用列表 (find_list_example.py)

演示如何使用 `DifyApp.find_list()` 方法获取Dify平台上的应用列表，包括：
- 基本列表获取
- 按名称搜索应用
- 按模式过滤应用
- 分页获取应用
- 获取由当前用户创建的应用

```bash
python examples/find_list_example.py
```

### 2. 应用列表高级用法 (app_list_example.py)

展示了更完整的应用列表获取功能，包括错误处理和日志记录：
- 使用日志记录而非简单打印
- 完整的错误处理
- 所有过滤选项的演示

```bash
python examples/app_list_example.py
```

### 3. 获取单个应用详情 (find_by_id.py)

演示如何使用 `DifyApp.find_by_id()` 方法获取单个Dify应用的详细信息，包括：
- 获取有效应用的详细信息
- 展示应用的基本属性（名称、描述、模式等）
- 展示应用的配置信息
- 展示应用的标签信息
- 错误处理示例（尝试获取不存在的应用）

```bash
python examples/app/find_by_id.py
```

### 4. 创建API密钥 (create_api_key.py)

演示如何使用 `DifyApp.create_api_key()` 方法为Dify应用创建API密钥，包括：
- 创建只读权限的API密钥
- 创建完全访问权限的API密钥
- 使用默认参数创建API密钥
- 展示API密钥的详细信息（ID、名称、密钥值、权限等）
- 错误处理示例

```bash
python examples/app/create_api_key.py
```

### 5. 获取API密钥列表 (get_keys.py)

演示如何使用 `DifyApp.get_keys()` 方法获取Dify应用的API密钥列表，包括：
- 获取并展示应用的所有API密钥
- 创建新的API密钥并验证添加成功
- 展示API密钥的详细信息（ID、类型、创建时间等）
- 错误处理示例

```bash
python examples/app/get_keys.py
```

## 注意事项

- 这些示例使用了异步编程模式，因为Dify SDK的API是异步的
- 确保您的API密钥具有足够的权限来执行示例中的操作
- 示例中的搜索词和过滤条件可能需要根据您的实际应用情况进行调整 