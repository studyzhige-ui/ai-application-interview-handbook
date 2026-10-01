# DeerFlow 源码小实验｜先预测，再检查真实函数的结果

本页保留旧源码快照的维护检查方法，不是本次产品学习主线，也未在本轮运行。当前机制与版本以[产品入口](../README.md)为准。

[← 产品总览](../README.md) · [上下文篇](../01-run-and-model-loop.md) · [记忆篇](../07-memory-pipeline.md) · [工具篇](../02-tools-and-resources.md)

本目录复用正文标记的源码片段，以及字节固定的上游摘要配置文件。不维护第二份业务门控实现，不启动完整 DeerFlow，也不连接模型、数据库或沙箱。

## 1. 环境与运行

局部片段只用 Python 标准库，要求 Python `>=3.10`；完整上游应用要求 `>=3.12`。低版本通过片段实验，不代表能运行上游应用。

在学习仓库根目录执行：

```bash
python products/agent/deer-flow/labs/check_examples.py
```

脚本从记忆篇和工具篇提取唯一标记的代码块，编译后测试。它不会修改正文、创建长期记忆文件或调用真实工具。每次使用新输入，不依赖上次状态，无需重置。

## 2. 先预测，再核对片段结果

| 输入条件 | 要回答的问题 |
|---|---|
| 用户事实，临时寿命，描述性信息 | 门控返回什么，是否写盘？ |
| 三项标签满足长期用户数据条件 | `None` 能否证明语义正确？ |
| 标签含两端空格和大小写差异 | 是否先规范化？ |
| 同目录重复展开工具 | 名字如何去重、顺序如何保留？ |
| 目录哈希改变 | 是否继承旧名字？ |
| 新更新为 `None` | 是否清空，是否新建对象？ |

<details>
<summary>预测答案与解释</summary>

依次是：返回 `durability` 且不写盘；`None` 只代表标签检查未拒绝；先去空格并转小写；同目录按首次出现顺序去重；换目录不继承旧名字；`None` 不更新并返回原对象。

脚本还检查输入未被原地修改，以及同目录空名字更新与换目录空名字更新的区别。候选门控不判断真实自然语言意图，状态合并也不提供业务授权。

</details>

## 3. 与本机固定上游源码比较

已有干净的上游 checkout 时，在 Python `>=3.12` 下执行：

```bash
python products/agent/deer-flow/labs/check_examples.py --upstream-root /path/to/deer-flow
```

`/path/to/deer-flow` 要换成实际本机目录。脚本要求 HEAD 为 `e2feca1e567d9bafce657de8ad8bc668bd7ad513`，被比较文件未修改，并比较三个函数的抽象语法树；它不导入完整应用，不调用模型。

没提供目录时，这项比较记为 `not_run`，不计为通过。片段结果正确、与上游函数一致、完整系统可以运行，是三个不同结论。

<a id="summary-config-lab"></a>
<a id="4-继续使用字节固定的真实配置实验"></a>

## 4. 运行字节固定的摘要配置实验

`verify_source_config.py` 先核对上游配置文件的 Git blob，再执行同一份已校验字节。需要 Python `>=3.12` 与 Pydantic 2；使用独立实验环境，不改现有项目依赖。在该环境中缺少依赖时安装：

```bash
python -m pip install "pydantic>=2,<3"
```

**路径一：已有固定上游仓库。**

```bash
python products/agent/deer-flow/labs/verify_source_config.py --source-root /path/to/deer-flow
```

**路径二：只有[固定版本的配置文件][config]。** 保存原始文件字节为本机 `summarization_config.py`，替换下面路径：

```bash
python products/agent/deer-flow/labs/verify_source_config.py --source-file /path/to/summarization_config.py
```

不要把网页 HTML 保存成 Python 文件，也不要为绕过校验而修改脚本中的期望哈希。脚本接受的 Git blob 为 `965cd2ac12a95f912d822026de2c75dffc926922`。缺文件、版本不符或字节不匹配会明确失败，不会静默跳过再报告成功。

先预测三件事，再运行：

1. 不传配置时，`enabled`、`trigger` 与 `keep` 是什么？
2. 比例 `0.8` 和 `80` 是否都合法？
3. `enabled=true` 且未给触发项，能否仅凭配置构造成功宣称自动摘要已运行？

<details>
<summary>预测答案与验证边界</summary>

配置类默认未启用，`trigger=None`，保留最近 20 条消息。`0.8` 合法，`80` 不合法。允许构造某种配置，不代表服务已加载它、工厂已安装中间件，或本次已达到触发条件。

脚本验证默认值、范围、非法数值与可变默认值隔离，不运行摘要生成或整个工厂。自动触发的流程与失败条件须结合[上下文正文](../01-run-and-model-loop.md)和[实际摘要工厂][summary]理解。

</details>

## 5. 用手工轨迹检查理解，不把推演当集成测试

完成源码片段后，用正文已有例子练三条链：

| 任务 | 初始条件与操作 | 可核对结果 |
|---|---|---|
| 消息更新 | 只有 `h1`，提交日期 `h1` 与原话 `h1__user` | 同 ID 替换、新 ID 追加，共两条；不是整份历史任意拼接 |
| 工具往返 | 用户请求后，模型提出 `c1`，工具才执行并回填 | 模型提议与真实执行分开，结果用调用 ID 配对 |
| delta 恢复 | `C0 → C1 → C2`，选择 C0 恢复 | 先物化，再在当前头部写新状态继续，不把兄弟增量当所选历史 |

第一条是规则推演，不执行 LangGraph；第二条不调用真实工具；第三条不是数据库恢复实验。答案分别在[运行与消息轨迹](../01-run-and-model-loop.md#run-trace)和[检查点恢复](../06-history-and-recovery.md#checkpoint-recovery)。它们验证能否解释步骤，不替代运行证据。

## 6. 下一层验证什么

中间件与检查点需要上游要求的 Python 环境、锁定依赖与相应测试条件。固定快照中的 `backend/tests/test_summarization_middleware.py` 是摘要测试入口之一；应按该版本说明准备配置，不把一条命令说成所有平台都可直接成功。

真实语义提取、多用户服务隔离、远程 MCP 会话、沙箱、数据库恢复和浏览器回放属于更高层验证。运行结果分别写入[维护记录](../../../../guide/audits/deerflow-clarity-refinement-2026-09-27.md)，不把某次作者机器状态写成实验本身的永久性质。

源码片段版权说明：[上游 MIT License](LICENSE.upstream)。

[config]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/config/summarization_config.py
[summary]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/summarization_middleware.py
