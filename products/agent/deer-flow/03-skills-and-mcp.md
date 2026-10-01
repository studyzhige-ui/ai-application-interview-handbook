# 技能与 MCP｜发现、激活和调用的边界

[← 上一章](02-tools-and-resources.md) · [本产品目录](README.md) · [下一章 →](04-native-batch-and-acp.md)

工具实现已经能执行，本章解释它怎样成为当前模型可见的能力，以及技能文件怎样变成经过授权的激活状态。MCP 连接又有自己的拥有者和故障边界。

## 工具怎样进入这次运行

工具说明包含名称、参数结构与用途，模型根据说明选择调用；执行端则保存实际工具对象，程序用它完成动作。两边名字和含义必须对齐。

`get_available_tools` 汇合配置工具、内建工具、MCP 工具、ACP 外部智能体工具和插件贡献。MCP（模型上下文协议）在这里接入外部能力；ACP（Agent Client Protocol，智能体客户端协议）把外部智能体包装为工具，不能直接等同本地原生子任务。[工具汇合][s1-tools]

工厂还会按条件追加记忆、项目文档和任务连续性工具。因此查“本次有哪些工具”，既要看汇合函数，也要看调用它的组装器。不是配置文件列出什么，模型就无条件得到什么。[条件追加][s1-assembly]

<a id="11-配置名字模型说明与执行名字必须对齐"></a>

<details>
<summary>工具命名、去重与动态描述的实现细节</summary>

配置名与 `BaseTool.name` 不一致时，该实现警告并按实际名绑定，不是一律拒绝启动。同名候选按实现优先次序去重，避免模型收到含义不确定的重复说明。

视觉工具只在模型声明支持视觉时加入。`write_file` 的描述可按已构造模型的实际输出上限加入长度提示；组装器先复制工具再改描述，避免污染共享单例。字符数提示是启发式换算，不是精确 token 计数。[工具身份与描述生成][s1-tools]

</details>

### 同一个调用怎样走到文件

固定为已存在的支付页文件：本次工具已注册、已向模型展示、策略允许，文件可读。模型先读取当前内容，再提出修改。沿正常路径分别观察：

| 阶段 | 传递什么 | 此刻实际发生什么 |
|---|---|---|
| 模型提出 `read_file` | 路径和调用 ID | 只是提议 |
| 程序检查并读取 | 当前内容与版本标记 | 文件被读取，没有修改 |
| 模型提出 `write_file` | 路径、新内容和新的调用 ID | 仍只是提议 |
| 执行侧检查 | 许可、路径、当前文件与读取依据 | 被拒绝时，不进入写工具正文 |
| 写工具执行并返回 | 结果消息及相应记录 | 文件可能已改变，需要核对结果 |
| 模型继续判断 | 与调用配对的结果 | 决定是否读回、测试或报告未完成项 |

这是固定条件下的教学轨迹，不是所有提供者都必经的单一检查顺序。文件内容正确、测试覆盖充分，还需要后续证据；模型看到一次“成功”不足以代替业务验收。[共同执行链][s1-wrappers]

<a id="2-工具很多时为什么先给索引再给完整说明"></a>

## 工具很多时，为什么先给目录，再展开说明

如果 MCP 工具很多，当前却只需要查支付错误，每次塞进所有参数定义会挤占任务和证据空间。延迟发现保留执行端注册，暂不让模型看到未展开工具的完整说明。

```text
执行端注册工具
    ↓
模型得到有界目录与发现入口
    ↓
tool_search 或路由提示展开相关定义
    ↓
ThreadState.promoted 记录本目录下已展开名称
    ↓
下一次请求加入相应完整说明
    ↓
真正调用时，继续检查发现状态与独立授权
```

promotion 在这里表示“把目录项展开成完整定义”，不是授予业务权限。`tool_search` 支持精确选名、名称关键词等方式；自动路由根据当前请求与路由元数据展开少量相关工具，本身不执行业务操作。[工具搜索][s1-search] · [路由][s1-routing]

<a id="21-为什么展开状态还要记目录哈希"></a>

### 目录变了，旧展开状态为什么不能直接沿用

昨天 `monitor_search` 的参数与今天不同，即使名字没变，也不能让昨天的状态证明今天的定义已被发现。目录哈希标识一组工具定义，状态只在对应目录内有效。

下面是固定快照的真实合并函数。旧值和新值都是状态数据，返回结果仍只是状态，不执行工具、不调用模型。

<!-- source-example: promoted_tools -->
```python
from typing import TypedDict

class PromotedTools(TypedDict):
    catalog_hash: str
    names: list[str]

def merge_promoted(existing: PromotedTools | None, new: PromotedTools | None) -> PromotedTools | None:
    """Reducer for deferred-tool promotions, scoped by catalog hash.

    - new None/empty -> preserve existing (node didn't touch promotions).
    - catalog_hash changed -> replace wholesale, dropping stale names (prevents a
      persisted bare name from exposing a different tool after catalog drift).
    - same catalog_hash -> union names, dedupe, preserve order.
    """
    if not new:
        return existing
    if existing is None or existing.get("catalog_hash") != new["catalog_hash"]:
        return {
            "catalog_hash": new["catalog_hash"],
            "names": list(dict.fromkeys(new["names"])),
        }
    return {
        "catalog_hash": existing["catalog_hash"],
        "names": list(dict.fromkeys(existing["names"] + new["names"])),
    }
```

`TypedDict` 声明这份字典预期有哪些字段，不会替代实际业务校验。`dict.fromkeys` 按首次出现的顺序去重，外层 `list` 取回名称列表。按三个输入观察，比背整个函数更直接：[类型与原函数][s1-state]

| 旧状态 | 新状态 | 结果 |
|---|---|---|
| A 目录：`search` | A 目录：`search, read` | A 目录：`search, read` |
| A 目录：`search` | B 目录：`export` | 只保留 B 的 `export` |
| A 目录：`search` | `None` | 保留原对象，不表示清空 |

同目录合并与换目录更新会构造新结果，不原地修改输入。真正执行时，`DeferredToolFilterMiddleware` 还核对目录哈希与展开状态。模型从历史猜出未展开工具名，也不能绕过发现检查。[执行侧过滤][s1-deferred]

## Skill 提供做事方法，但不能自行创造权限

Skill（技能）通常是一份 `SKILL.md` 和相关资源。目录先说明名字、用途与位置，正文按需要加载。**技能教模型怎样组合工具，工具才由程序实际执行。**

安装或启用只表示可发现。用户用 `/skill-name` 显式选择，或模型实际读取技能文件，才形成激活依据。显式路径加载正文；被动读取路径根据工具结果中的可靠来源标记捕获引用，不相信外部工具自己伪造“技能已读”。[激活][s1-activation] · [来源标记][s1-wrappers]

### 可见、可读、可激活要分别授权

启用产品授权时，组装先按用户/主体与 `skill` 资源策略筛选候选，禁止的技能不进入索引和描述结果。空集合明确表示没有可见技能，不能转成“未设置限制”再把全目录装回来。显式 slash 激活还检查动作级 `skill:activate`，所以自定义策略可以允许看说明，却不允许使用它的执行约定。

模型经工具成功读取 `SKILL.md` 后，工具返回的自报元数据先被清除；宿主根据配置认可的读工具、调用 ID、文件路径和实时用户技能注册表重新确认来源，再检查 `skill:activate`。目录名与技能声明名可能不同，授权目标用注册表的规范名。拒绝激活可以保留读取结果，但不会给它盖“已激活”标记，也不会据此绑定秘密或扩张工具政策。[读取标记与动作授权](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py)

历史保存的 skill_context 也要在后续步骤重新授权；策略收紧后，旧条目不能继续获得 allowed-tools、活跃提醒或凭证。主 Agent 与原生子任务使用同一执行内解析的授权上下文，防止目录过滤和实际激活意外采用两个不同的策略实例。授权未启用时保留相应兼容路径，但其他沙箱、工具和来源规则依然生效。[组装与策略传递](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/lead_agent/agent.py)、[技能策略](https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/authz/skill_filter.py)

<a id="31-allowed-tools-的边界要读完整"></a>

### allowed-tools 怎样限制本次可用集合

技能可通过 `allowed-tools` 声明工具限制。这是技能策略这一层的允许集合，不能取代用户授权、路径权限或沙箱边界。

| 条件 | 该技能策略的处理 |
|---|---|
| 没激活技能，或激活集合都没声明限制 | 保留该层兼容性不限工具行为，其他授权照常生效 |
| 至少一个活动技能明确声明 | 合并明确声明，未声明的技能不抹掉已有限制 |
| 用户本轮显式 slash 激活 | 显式策略优先，随后被动读取不能扩大它 |
| 活动引用无法解析或授权 | 降到框架保留工具集合，不开放全部工具 |

多个被动技能的明确声明采用并集，不是默认交集。`read_file`、`describe_skill`、`review_skill_package`、`tool_search` 是这一策略的保留工具，保留并不意味着允许它们访问任意资源。[声明合并][s1-policy] · [活动策略][s1-skill-policy]

策略既过滤模型看到的定义，也在执行时检查。连 `tool_search` 的返回说明与展开名字也要过滤，否则发现入口会把禁止工具带回来。对应模型请求的决策有组装实例归属标记，客户端同名字段或过期缓存不能冒充有效策略。

> ⚠️ 提示里写“不要发布”可以约束模型规划，却不能代替执行授权。把用户技能正文提升成系统指令，同样不是可靠的权限设计。

<a id="32-secret-绑定的是这次请求不是技能永久拥有宿主环境"></a>

### 凭证只按本次请求提供

技能可声明需要的 Secret（秘密凭证）。实际值来自本次运行上下文，按启用状态、允许列表及激活规则筛选，不因磁盘上有一个技能就交出宿主所有环境变量。

凭证名可用于诊断缺什么，凭证值不应写进普通审计文本。技能停用、更新或本次请求没有提供凭证时，不能沿用历史激活永久获得权限。[秘密绑定][s1-activation]

<a id="7-mcp-会话为什么要有明确的所有者"></a>

## MCP 会话为什么需要明确所有者

浏览器 MCP 服务可能把已打开页面放在会话中。第一次“打开”用连接 X，第二次“点击”若换成全新连接 Y，就可能找不到页面。因此连接复用不仅影响速度，也影响工具能否接续工作。

池化路径按服务器、用户、线程范围及所属事件循环区分连接。同一循环中的连续调用可复用会话，不同循环使用不同会话。该快照同步包装每次运行新的循环，不能承诺同步工具调用之间保留浏览器状态。[会话池边界][s1-mcp-pool]

<a id="71-为什么创建和关闭都交给同一个任务"></a>

### 借用连接，与拥有连接是两件事

事件循环负责调度异步任务。这里的 MCP 异步上下文要求由同一任务进入和退出；调用 A 创建、调用 B 直接退出，可能触发运行错误。

DeerFlow 设置 owner task（拥有者任务）：由它进入上下文、初始化、登记入池，随后等待关闭信号，最终仍由它退出。其他调用者只借用连接或请求关闭。[拥有者任务][s1-mcp-pool]

```text
拥有者任务：创建连接 → 登记可借用 → 等待关闭信号 → 退出连接上下文
调用者 A：                    借用，打开页面
调用者 B：                    借用，点击同一页面
```

初始化完成与登记入池在同一临界区，即受同一并发保护的一段操作内完成，避免返回连接时还没有人负责回收。同键并发创建共享尚未完成的创建结果，不重复建连。容量淘汰后，旧连接退出前还要确认自己仍是当前项，不能误删后来替换的新连接。

明确传输断开时清理对应连接并抛出原错误，不无条件重放调用。网络断开不证明外部按钮没有被点击。[调用与断连][s1-mcp-pool]

<a id="72-外部工具生成的文件也要接回工作区"></a>

### 外部文件要接回本次工作区

stdio MCP 子进程可输出截图或导出文件。桥接处理工作目录、临时目录及虚拟路径，尽量让文件进入线程可访问的数据树；已有环境配置和不同 Server 行为仍要分别核对，这些默认安排不能强制所有服务的输出位置。

宿主路径、沙箱路径和前端产物链接服务不同使用者。字符串看起来正确，还要核对映射、权限和文件存在，才能让模型读到、用户打开。[MCP 桥接][s1-mcp-tools]

[← 上一章](02-tools-and-resources.md) · [本产品目录](README.md) · [下一章 →](04-native-batch-and-acp.md)

[s1-tools]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/tools/tools.py
[s1-assembly]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/lead_agent/agent.py
[s1-wrappers]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py
[s1-search]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/tools/builtins/tool_search.py
[s1-routing]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/mcp_routing_middleware.py
[s1-state]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/thread_state.py
[s1-deferred]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/deferred_tool_filter_middleware.py
[s1-activation]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/skill_activation_middleware.py
[s1-policy]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/skills/tool_policy.py
[s1-skill-policy]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/agents/middlewares/skill_tool_policy_middleware.py
[s1-mcp-pool]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/mcp/session_pool.py
[s1-mcp-tools]: https://github.com/bytedance/deer-flow/blob/4d5607229ef1ebe8a66c9b9644b91da9082c3221/backend/packages/harness/deerflow/mcp/tools.py
