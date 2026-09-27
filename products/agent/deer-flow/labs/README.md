# DeerFlow 源码小实验｜先预测，再检查真实函数的结果

[← 产品总览](../README.md) · [记忆篇](../02-memory-lifecycle.md) · [工具篇](../03-tool-lifecycle.md)

这里直接提取正文中标记的源码片段执行，不维护第二份门控或状态合并实现。实验不启动 DeerFlow，不连接模型、数据库或沙箱，也不模拟一个成功的外部服务。

## 1. 环境与运行

局部示例使用 Python 标准库，要求 Python `>=3.10`；完整上游应用要求 Python `>=3.12`。这两个要求不同：低版本通过这里的纯函数实验，不代表能运行上游应用。

在学习仓库根目录执行：

```bash
python products/agent/deer-flow/labs/check_examples.py
```

脚本从 `02-memory-lifecycle.md` 与 `03-tool-lifecycle.md` 提取唯一标记的代码块，编译并执行测试。运行不会更改学习正文，不创建长期记忆文件，也不调用工具。每次运行都创建新的测试输入，不依赖上次状态，无需额外重置。

## 2. 运行之前先预测

| 输入条件 | 需要预测什么 | 预期核对结果 |
|---|---|---|
| 用户事实，临时寿命，描述性信息 | 门控返回值 | `durability` |
| 分类三项满足长期用户数据条件 | 门控返回值 | `None`，不等于已经保存 |
| 分类标签含空格和大小写差异 | 是否先规范化 | 合法标签仍可通过这道检查 |
| 同目录重复展开工具 | 名字顺序与去重 | 保留原顺序，追加新名字 |
| 目录哈希改变 | 是否继承旧名字 | 不继承旧目录展开状态 |
| 新更新为 `None` | 是否清空、是否新建对象 | 不更新，返回原对象 |

测试还检查输入未被原地修改，以及同目录空名字更新与换目录空名字更新的差异。门控函数不负责判断自然语言真实意图，状态合并函数不负责业务授权；这两项必须在口头解释中说清。

## 3. 与本机固定上游源码比较

已有上游 checkout 时，可在 Python `>=3.12` 下做额外比较：

```bash
python products/agent/deer-flow/labs/check_examples.py --upstream-root /path/to/deer-flow
```

这里的 `/path/to/deer-flow` 是需要替换的本机目录参数，不是已经存在的环境。脚本要求该 checkout 的 HEAD 等于本组正文固定的 `e2feca1e567d9bafce657de8ad8bc668bd7ad513`，并要求被比较文件未修改。它比较三个函数的抽象语法树，不导入完整上游应用，也不执行模型。

未提供目录时，这项检查明确记为 `not_run`，不算通过。当前交付环境没有可用的完整上游本地副本，因此只运行了正文片段测试，没有执行此比较。

## 4. 继续使用字节固定的真实配置实验

此前已经发布的 `verify_source_config.py` 不与本页的正文片段测试重复：它要求你提供固定上游 checkout 或单个 `summarization_config.py`，先核对 Git blob，再直接运行上游配置类的边界测试。需要检查摘要配置的默认关闭、比例、保留量和非法值时，使用：

```bash
python products/agent/deer-flow/labs/verify_source_config.py --source-root /path/to/deer-flow
```

因此本目录有两类局部实验：`check_examples.py` 检查正文中抽出的门控与状态合并规则；`verify_source_config.py` 检查字节固定的上游摘要配置。两者都不启动完整 DeerFlow，也都不能替代真实模型、数据库、MCP 或沙箱验证。

## 5. 下一层应该验证什么

要验证中间件和检查点，应在上游要求的 Python 环境与锁定依赖下运行其测试。已核验存在的 `backend/tests/test_summarization_middleware.py` 可用于继续追摘要相关测试，但运行前仍须按该快照说明准备配置和依赖，不能假定一条命令在所有平台直接成功。

真实模型提取、跨用户隔离服务、远程 MCP 会话、沙箱、数据库回滚和浏览器重放属于更高层验证。这里的纯函数测试结果只回答它标明的问题，不以测试数量代替这些实际行为。

源码片段版权说明：[上游 MIT License](LICENSE.upstream)。
