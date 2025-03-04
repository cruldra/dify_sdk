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

## 注意事项

- 这些示例使用了异步编程模式，因为Dify SDK的API是异步的
- 确保您的API密钥具有足够的权限来执行示例中的操作
- 示例中的搜索词和过滤条件可能需要根据您的实际应用情况进行调整 