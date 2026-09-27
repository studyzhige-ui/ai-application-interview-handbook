# 03｜工具：从可发现能力到受控副作用

[← 记忆](02-memory-lifecycle.md) · [DeerFlow 总览](README.md) · [下一篇：工程与评测 →](04-engineering-evaluation.md)

用户让智能体查监控、修复支付页，但不要发布。模型提出 `write_file` 后，文件还没有改变。程序要检查许可和执行环境，工具真正运行后，模型才获得新观察。

同样，配置了发布工具，不代表本轮应该让模型看见；看见也不代表获准执行。先把**存在、可见、允许执行、实际完成**四种状态拆开，再追踪它们之间怎样转换。

## 1. 工具怎样进入这次运行

工具说明包含名称、参数结构与用途，模型根据说明选择调用；执行端则保存实际工具对象，程序用它完成动作。两边名字和含义必须对齐。

`get_available_tools` 汇合配置工具、内建工具、MCP 工具、ACP 外部智能体工具和插件贡献。MCP（模型上下文协议）在这里接入外部能力；ACP（Agent Client Protocol，智能体客户端协议）把外部智能体包装为工具，不能直接等同本地原生子任务。[工具汇合][tools]

工厂还会按条件追加记忆、项目文档和任务连续性工具。因此查“本次有哪些工具”，既要看汇合函数，也要看调用它的组装器。不是配置文件列出什么，模型就无条件得到什么。[条件追加][assembly]

<a id="11-配置名字模型说明与执行名字必须对齐"></a>

<details>
<summary>工具命名、去重与动态描述的实现细节</summary>

配置名与 `BaseTool.name` 不一致时，该实现警告并按实际名绑定，不是一律拒绝启动。同名候选按实现优先次序去重，避免模型收到含义不确定的重复说明。

视觉工具只在模型声明支持视觉时加入。`write_file` 的描述可按已构造模型的实际输出上限加入长度提示；组装器先复制工具再改描述，避免污染共享单例。字符数提示是启发式换算，不是精确 token 计数。[工具身份与描述生成][tools]

</details>

### 1.1 同一个调用怎样走到文件

固定为已存在的支付页文件：本次工具已注册、已向模型展示、策略允许，文件可读。模型先读取当前内容，再提出修改。沿正常路径分别观察：

| 阶段 | 传递什么 | 此刻实际发生什么 |
|---|---|---|
| 模型提出 `read_file` | 路径和调用 ID | 只是提议 |
| 程序检查并读取 | 当前内容与版本标记 | 文件被读取，没有修改 |
| 模型提出 `write_file` | 路径、新内容和新的调用 ID | 仍只是提议 |
| 执行侧检查 | 许可、路径、当前文件与读取依据 | 被拒绝时，不进入写工具正文 |
| 写工具执行并返回 | 结果消息及相应记录 | 文件可能已改变，需要核对结果 |
| 模型继续判断 | 与调用配对的结果 | 决定是否读回、测试或报告未完成项 |

这是固定条件下的教学轨迹，不是所有提供者都必经的单一检查顺序。文件内容正确、测试覆盖充分，还需要后续证据；模型看到一次“成功”不足以代替业务验收。[共同执行链][wrappers]

<a id="2-工具很多时为什么先给索引再给完整说明"></a>

## 2. 工具很多时，为什么先给目录，再展开说明

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

promotion 在这里表示“把目录项展开成完整定义”，不是授予业务权限。`tool_search` 支持精确选名、名称关键词等方式；自动路由根据当前请求与路由元数据展开少量相关工具，本身不执行业务操作。[工具搜索][search] · [路由][routing]

<a id="21-为什么展开状态还要记目录哈希"></a>

### 2.1 目录变了，旧展开状态为什么不能直接沿用

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

`TypedDict` 声明这份字典预期有哪些字段，不会替代实际业务校验。`dict.fromkeys` 按首次出现的顺序去重，外层 `list` 取回名称列表。按三个输入观察，比背整个函数更直接：[类型与原函数][state]

| 旧状态 | 新状态 | 结果 |
|---|---|---|
| A 目录：`search` | A 目录：`search, read` | A 目录：`search, read` |
| A 目录：`search` | B 目录：`export` | 只保留 B 的 `export` |
| A 目录：`search` | `None` | 保留原对象，不表示清空 |

同目录合并与换目录更新会构造新结果，不原地修改输入。真正执行时，`DeferredToolFilterMiddleware` 还核对目录哈希与展开状态。模型从历史猜出未展开工具名，也不能绕过发现检查。[执行侧过滤][deferred]

## 3. Skill 提供做事方法，但不能自行创造权限

Skill（技能）通常是一份 `SKILL.md` 和相关资源。目录先说明名字、用途与位置，正文按需要加载。**技能教模型怎样组合工具，工具才由程序实际执行。**

安装或启用只表示可发现。用户用 `/skill-name` 显式选择，或模型实际读取技能文件，才形成激活依据。显式路径加载正文；被动读取路径根据工具结果中的可靠来源标记捕获引用，不相信外部工具自己伪造“技能已读”。[激活][activation] · [来源标记][wrappers]

<a id="31-allowed-tools-的边界要读完整"></a>

### 3.1 allowed-tools 怎样限制本次可用集合

技能可通过 `allowed-tools` 声明工具限制。这是技能策略这一层的允许集合，不能取代用户授权、路径权限或沙箱边界。

| 条件 | 该技能策略的处理 |
|---|---|
| 没激活技能，或激活集合都没声明限制 | 保留该层兼容性不限工具行为，其他授权照常生效 |
| 至少一个活动技能明确声明 | 合并明确声明，未声明的技能不抹掉已有限制 |
| 用户本轮显式 slash 激活 | 显式策略优先，随后被动读取不能扩大它 |
| 活动引用无法解析或授权 | 降到框架保留工具集合，不开放全部工具 |

多个被动技能的明确声明采用并集，不是默认交集。`read_file`、`describe_skill`、`review_skill_package`、`tool_search` 是这一策略的保留工具，保留并不意味着允许它们访问任意资源。[声明合并][policy] · [活动策略][skill-policy]

策略既过滤模型看到的定义，也在执行时检查。连 `tool_search` 的返回说明与展开名字也要过滤，否则发现入口会把禁止工具带回来。对应模型请求的决策有组装实例归属标记，客户端同名字段或过期缓存不能冒充有效策略。

> ⚠️ 提示里写“不要发布”可以约束模型规划，却不能代替执行授权。把用户技能正文提升成系统指令，同样不是可靠的权限设计。

<a id="32-secret-绑定的是这次请求不是技能永久拥有宿主环境"></a>

### 3.2 凭证只按本次请求提供

技能可声明需要的 Secret（秘密凭证）。实际值来自本次运行上下文，按启用状态、允许列表及激活规则筛选，不因磁盘上有一个技能就交出宿主所有环境变量。

凭证名可用于诊断缺什么，凭证值不应写进普通审计文本。技能停用、更新或本次请求没有提供凭证时，不能沿用历史激活永久获得权限。[秘密绑定][activation]

<a id="4-从一个调用提议到真实执行要经过哪些检查"></a>

## 4. 执行侧每一层分别负责什么

沿前面的文件修改轨迹，再把检查职责展开：

| 层次 | 需要确认的问题 |
|---|---|
| 参数与业务输入 | 参数可解析，目标和操作有意义吗？ |
| 发现与技能限制 | 已展开且当前技能允许吗？ |
| 产品授权与护栏 | 当前身份可使用这项能力，策略是否拒绝？ |
| 沙箱与路径 | 操作实际落在哪里，能接触哪些资源？ |
| 文件新鲜度 | 修改前是否读过当前版本？ |
| 结果规范化与收据 | 发生了什么，下一次调用和产品记录怎样理解它？ |

这些是不同责任，不是所有组件无条件依次运行。实际安装由配置决定，外层可提前拒绝。授权提供者通过适配器复用 GuardrailMiddleware 的拒绝与错误语义，护栏和沙箱仍分别承担自己的边界。[实际构建顺序][wrappers]

<a id="12-本地沙箱的名字不等于安全隔离"></a>

### 4.1 LocalSandbox 不等于安全隔离环境

`LocalSandboxProvider` 在宿主环境执行，本身不是安全隔离边界。默认隐藏这条模式下的宿主 Bash，只有明确允许才暴露；不是已经有了安全的本地 Sandbox Bash，再删去多余 Host Bash。

允许命令前必须知道执行位置、可访问文件与网络。AIO、E2B、OpenSandbox 等提供者各有实现限制，更换提供者不能默认安全与持久语义不变。[本地 Bash 门控][security]

<a id="5-先读后写怎样防止基于旧文件反复修改"></a>

## 5. 先读后写怎样防止基于旧文件修改

文件是版本 A，模型执行 `read_file`，工具结果保存完整当前内容的 SHA-256。稍后要 `write_file` 或 `str_replace`，门控重新计算当前哈希：仍是 A 才能沿已读路径继续；已被改成 B，则旧依据失效，需要重读。

一次写入不会替模型更新“已读”标记。成功写入改变字节后，下次修改需要重读；若字节完全相同，哈希未变，不能概括成“任何写调用都无条件废除全部标记”。部分区间读取也可记录文件版本，但不代表模型读过每一行。[读取与版本检查][read-write]

### 5.1 两个并发写为什么还需要锁

若两个修改都检查到了 A，再同时写入，单次检查都正确也挡不住整体覆盖。DeerFlow 用相同作用域和规范化路径的进程内锁，把检查与执行放在同一保护范围；读取与标记也使用相应保护。

```text
写入 1：取得锁 → 检查 A → 写成 B → 释放锁
写入 2：等待锁 → 检查时已经是 B → 旧读取依据不再匹配
```

这段推演假设两次写入确实经过同一把锁，且第一次改变了字节。外部编辑器、其他进程或未接入路径不受它约束，不能扩大成跨进程文件事务。[锁与执行][read-write]

<a id="52-这道门不是普遍的-fail-closed-安全边界"></a>

### 5.2 无法检查时，不是一律拒绝

| 门控观察到什么 | 该实现怎样处理 |
|---|---|
| 文件存在、可检查，但没有当前版本读取标记 | 返回错误，不进入写工具正文 |
| 文件不存在 | 放行，创建或替换是否可行由工具判断 |
| 普通检查故障，或返回 `Error:` 等不可检查内容 | fail-open，即检查失败时放行，由工具产生结果 |
| 沙箱授权明确拒绝 | 返回授权错误，不当成普通检查故障 |

**这是有适用范围的新鲜度检查，不是普遍的 fail-closed 安全边界。** fail-closed 指无法确认时拒绝；这里的普通 I/O 故障并非采用这种策略。真正被拦的大写入参数可在后续模型视图中缩短，原参数仍作为相应证据保留，不能因此声称文件已改变。[实际分支与参数裁剪][read-write]

<a id="6-沙箱是需要管理的资源不是每次调用的装饰对象"></a>

## 6. 沙箱复用时，谁负责释放

沙箱中间件负责取得、复用与释放环境；状态存标识，不存不可序列化的提供者对象。默认 `lazy_init=True` 时，普通共享视图可推迟到工具调用才取得环境；需要按策略投影技能文件时，可能提前取得，防止旧宽权限视图继续被使用。[沙箱生命周期][sandbox]

主智能体与子任务可以同时用一个环境，因此每个使用者各持有一份执行租约，即“我仍在使用这个资源”的持有记录。

| 动作 | 仍在使用的参与者 | 能否因这一步关闭整个环境 |
|---|---|---|
| 主任务与子任务都已取得租约 | 主、子 | 不能 |
| 子任务结束并释放自己的租约 | 主 | 不能，主任务仍在使用 |
| 最后一个使用者释放 | 无 | 按提供者策略回收，可能放回暖池复用 |

暖池是保留可复用环境的集合，release 不一定销毁容器或删除文件；提供者最终关闭又是另一层清理。取消时，已交给工作线程的同步操作可能仍在运行，必须等待自己的操作结束再释放持有资源。取消等待者不会自动杀掉线程，租约也不会回滚命令副作用。

<a id="7-mcp-会话为什么要有明确的所有者"></a>

## 7. MCP 会话为什么需要明确所有者

浏览器 MCP 服务可能把已打开页面放在会话中。第一次“打开”用连接 X，第二次“点击”若换成全新连接 Y，就可能找不到页面。因此连接复用不仅影响速度，也影响工具能否接续工作。

池化路径按服务器、用户、线程范围及所属事件循环区分连接。同一循环中的连续调用可复用会话，不同循环使用不同会话。该快照同步包装每次运行新的循环，不能承诺同步工具调用之间保留浏览器状态。[会话池边界][mcp-pool]

<a id="71-为什么创建和关闭都交给同一个任务"></a>

### 7.1 借用连接，与拥有连接是两件事

事件循环负责调度异步任务。这里的 MCP 异步上下文要求由同一任务进入和退出；调用 A 创建、调用 B 直接退出，可能触发运行错误。

DeerFlow 设置 owner task（拥有者任务）：由它进入上下文、初始化、登记入池，随后等待关闭信号，最终仍由它退出。其他调用者只借用连接或请求关闭。[拥有者任务][mcp-pool]

```text
拥有者任务：创建连接 → 登记可借用 → 等待关闭信号 → 退出连接上下文
调用者 A：                    借用，打开页面
调用者 B：                    借用，点击同一页面
```

初始化完成与登记入池在同一临界区，即受同一并发保护的一段操作内完成，避免返回连接时还没有人负责回收。同键并发创建共享尚未完成的创建结果，不重复建连。容量淘汰后，旧连接退出前还要确认自己仍是当前项，不能误删后来替换的新连接。

明确传输断开时清理对应连接并抛出原错误，不无条件重放调用。网络断开不证明外部按钮没有被点击。[调用与断连][mcp-pool]

<a id="72-外部工具生成的文件也要接回工作区"></a>

### 7.2 外部文件要接回本次工作区

stdio MCP 子进程可输出截图或导出文件。桥接处理工作目录、临时目录及虚拟路径，尽量让文件进入线程可访问的数据树；已有环境配置和不同 Server 行为仍要分别核对，这些默认安排不能强制所有服务的输出位置。

宿主路径、沙箱路径和前端产物链接服务不同使用者。字符串看起来正确，还要核对映射、权限和文件存在，才能让模型读到、用户打开。[MCP 桥接][mcp-tools]

<a id="8-工具返回后观察证据与任务成功仍然不同"></a>

## 8. 返回消息、执行证据和任务完成怎样区分

普通工具异常经 `ToolErrorHandlingMiddleware` 转成带对应调用 ID 的错误 `ToolMessage`，模型可修正参数或换路径。LangGraph 暂停等控制流要继续传播，不能混成业务错误；取消也不能被通用重试吞掉。[错误与控制流][wrappers]

| 表示 | 主要回答什么 |
|---|---|
| `ToolMessage` | 给下一次模型调用什么观察？ |
| Tool Receipt（工具收据） | 哪次执行、哪些参数与结果有记录？ |
| Run Journal（运行事件记录） | 产品历史怎样呈现本轮过程？ |
| 文件读回或业务验证 | 最终对象是否满足任务要求？ |

它们不保证保存完全相同的全文。大结果可在返回后外置或裁剪；外层收据还要能看到策略提前拒绝的结果，不能漏掉真实拒绝。[记录位置][wrappers]

> ⚠️ 外部动作已成功、回填却超时，并不能证明动作没发生。再次执行前先核对实际状态，必要时依赖业务幂等或补偿；不能说所有 DeerFlow 工具都自动具备统一的外部幂等保证。

`task` 从父模型看也是工具，但会启动独立子智能体。父模型收到“子任务完成”之后，还要核对停止原因、收据和验收条件，不能只凭返回文字交付。[工程篇的子任务与验收](04-engineering-evaluation.md#native-task)

## 本章小结

先注册能力，再按需展示，执行侧仍检查许可与实际资源。文件版本保护、沙箱租约和 MCP 会话所有者分别解决不同问题；它们不能互相代替。最后还要分清模型观察、执行记录与业务验收。

## 🎯 面试怎么回答

**Q：Skill 或 MCP 数量太多，怎样避免上下文膨胀？**

> 分开目录、完整定义和实际执行。DeerFlow 通过搜索或路由按需展开 MCP 定义，技能正文也按需加载；展开状态绑定目录哈希，升级后不能沿用旧状态。执行时仍检查发现状态、技能限制、授权和沙箱，发现入口不能恢复被禁止工具。

**Q：修改前强制读文件，能解决并发与安全问题吗？**

> 它减少基于旧内容的修改。DeerFlow 用读取哈希检查新鲜度，进程内锁覆盖检查和执行。但只保护接入路径，普通检查故障还有放行分支，不能当成跨进程事务或完整隔离。权限、外部写入者及最终文件结果仍需单独核对。

## ⚠️ 高频易错点

- **只隐藏说明，不检查执行。** 模型可能从历史或猜测得到工具名。
- **把技能声明并集说成交集。** slash 优先、声明合并和保留工具按该版本区分。
- **把 LocalSandbox 当安全容器。** 名称不能证明宿主命令已隔离。
- **把释放资源当回滚动作。** 环境清理不撤销外部操作，重连也不等于安全重试。

## 本章自测

**任务 A：** 旧展开状态为目录 A 的 `read`，新状态为目录 B 的 `export`；技能只允许 `read`。分别预测合并结果和执行许可。

<details>
<summary>任务 A 提示与答案</summary>

合并只保留 B 的 `export`。它满足的只是发现状态；技能不允许，仍应在可见性与执行阶段限制。合并函数不会替用户授予权限。

</details>

**任务 B：** 文件没有读取标记，检查时出现普通 I/O 故障，没有授权拒绝。此时工具正文尚未执行。预测门控结果，以及什么仍未知。

<details>
<summary>任务 B 提示与答案</summary>

走普通检查失败放行分支。文件是否改变仍未知，需核对工具结果、收据和目标文件。不能说已写成，也不能说被新鲜度门控拒绝。

</details>

## 知识回看与源码定位

- [工具汇合][tools]、[执行链][wrappers]：分别追定义如何出现、调用如何被处理。
- [文件版本与锁][read-write]、[会话池][mcp-pool]：核对检查和资源拥有者。
- [源码小实验](labs/README.md)：预测目录变化、去重与 `None` 更新，不把状态测试当权限测试。
- [上下文篇](01-context-lifecycle.md)：结果返回时的裁剪与请求阶段裁剪有什么不同。

下一篇：[04｜工程与评测 →](04-engineering-evaluation.md)

[tools]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/tools/tools.py
[assembly]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/lead_agent/agent.py
[wrappers]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/tool_error_handling_middleware.py
[search]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/tools/builtins/tool_search.py
[routing]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/mcp_routing_middleware.py
[state]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/thread_state.py
[deferred]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/deferred_tool_filter_middleware.py
[activation]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/skill_activation_middleware.py
[policy]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/skills/tool_policy.py
[skill-policy]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/skill_tool_policy_middleware.py
[security]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/sandbox/security.py
[read-write]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/agents/middlewares/read_before_write_middleware.py
[sandbox]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/sandbox/middleware.py
[mcp-pool]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/mcp/session_pool.py
[mcp-tools]: https://github.com/bytedance/deer-flow/blob/e2feca1e567d9bafce657de8ad8bc668bd7ad513/backend/packages/harness/deerflow/mcp/tools.py
