# 05. Tool Registry：工具注册、模型可见说明与按需发现

工具只有两个时，名字和函数放在一个字典里就能工作。工具变成几十、几百个以后，你可能会问：

> 难道每次都把所有工具的全部信息塞给模型？

要回答它，先分清“程序注册了什么”和“模型这一轮看到什么”。

[← 上一章](04-ToolContractAndValidation.md) · [Agent 目录](../README.md) · [下一章 →](06-ToolExecutionAndFailure.md)

---

<a id="section-1"></a>

## 1. Registry 解决什么

<a id="legacy-05-01"></a>

Registration（注册）是把一个工具名称和它的实际处理方法加入应用的目录。Registry（注册表）是这个目录；模型并不知道你内存里的函数地址。每次调用模型时，应用再把允许使用的工具说明交给模型。模型返回名字与参数后，Router（路由器）查注册表，Executor（执行器）才调用函数。

```text
开发者定义工具 → 加入应用注册表
                      ├→ 选择模型可见说明 → 模型生成调用候选
                      └← 名称查处理器 ← 解析与校验候选
                                      ↓
                                  执行与回填
```

因此常说的“注册工具”其实容易混淆两步：**让程序知道怎么执行**，以及**让模型知道什么可调用**。注册了但本轮不暴露的工具仍可能存在于程序目录中；模型能看见说明也不等于当前参数已获批准。

最小 Tool Runtime（运行时执行系统） 可以手写：

```python
# 本地目录示意：名字映射到实现；这些函数对象不会直接序列化给模型。
TOOLS = {
    "read_file": read_file,
    "run_tests": run_tests,
}
```

但 Production（生产环境） 需要 Registry 管理：

```text
identity
schema
version
runtime handler
permission class
exposure mode
search metadata
health / availability
provider / tenant scope
```

Registry 是 Host 的能力目录，不等于“模型当前看得见的 Tool List”。

---

<a id="section-2"></a>

## 2. Registry 与 Model-visible Tool Set 必须分开

<a id="legacy-05-02"></a>

假设系统注册 300 个 Tool：

```text
Registry = 300
```

不代表每轮都发送：

```text
Model-visible tools = 300
```

更合理：

```text
Full Capability Registry
        ↓
Policy / Tenant / Environment Filter
        ↓
Task / Intent Candidate Set
        ↓
Progressive Discovery
        ↓
Current Model-visible Tool Set
```

这能降低：

- Token 成本；
- Tool 选择混淆；
- Schema 冲突；
- Prompt cache 抖动；
- 暴露不必要高风险能力。

<details>
<summary>动手看两份对象：注册表与模型说明（标准库示例）</summary>

下面只用 Python 标准库，没有网络、模型API或真实文件写入。模型候选由固定字典模拟；它验证注册、投影、分发与拒绝，不证明模型会正确选择。

```python
# runnable-example: registry_projection
from dataclasses import dataclass
from typing import Callable
import json

DOCUMENTS = {"A": "项目发布日期待确认", "B": "发布日期为周五"}

def read_document(document_id: str) -> str:
    return DOCUMENTS[document_id]

@dataclass(frozen=True)
class Tool:
    name: str
    description: str
    schema: dict
    handler: Callable[[str], str]
    read_only: bool  # 程序调度信息，不会自动发给模型

read_tool = Tool(
    name="read_document",
    description="读取授权清单中的文档，不修改原件",
    schema={"type": "object", "properties": {"document_id": {"type": "string"}},
            "required": ["document_id"], "additionalProperties": False},
    handler=read_document,
    read_only=True,
)
registry = {read_tool.name: read_tool}  # 第一步：注册实际实现

# 第二步：投影成模型端说明；不是某供应商完整请求体
visible_specs = [{"name": t.name, "description": t.description,
                  "input_schema": t.schema} for t in registry.values()]
assert "handler" not in visible_specs[0] and "read_only" not in visible_specs[0]
json.dumps(visible_specs, ensure_ascii=False)  # 可序列化说明，不含函数

def dispatch(call: dict, allowed_documents: set[str]) -> dict:
    tool = registry.get(call.get("name"))
    if tool is None:
        return {"status": "invalid_tool"}
    args = call.get("arguments")
    # 仅实现本示例所需校验；生产中使用相应Schema/类型校验库
    if not isinstance(args, dict) or set(args) != {"document_id"}:
        return {"status": "invalid_arguments"}
    doc = args["document_id"]
    if not isinstance(doc, str) or not doc.strip():
        return {"status": "invalid_arguments"}
    if doc not in allowed_documents:
        return {"status": "denied"}
    if doc not in DOCUMENTS:
        return {"status": "unavailable"}
    return {"status": "ok", "document_id": doc, "text": tool.handler(doc)}

assert dispatch({"name": "read_document", "arguments": {"document_id": "A"}}, {"A"})["status"] == "ok"
assert dispatch({"name": "read_document", "arguments": {"document_id": "B"}}, {"A"})["status"] == "denied"
assert dispatch({"name": "read_document", "arguments": {"document_id": 3}}, {"A"})["status"] == "invalid_arguments"
assert dispatch({"name": "delete_document", "arguments": {}}, {"A"})["status"] == "invalid_tool"
```

`registry`里有函数和运行元数据，`visible_specs`里只有说明。`allowed_documents`来自可信应用，不由模型提供。生产框架会自动完成部分包装，但两份对象的职责不会因此消失。

</details>

---

<a id="section-3"></a>

## 3. Router 做什么

<a id="legacy-05-03"></a>

Router 不是简单的：

```python
# 示意查表分发；实际实现还需处理未知工具、版本和授权。
handler = tools[name]
```

完整路径：

```text
Model Tool Call
→ normalize identity / namespace
→ resolve version
→ verify exposure
→ find runtime handler
→ permission / policy
→ dispatch
```

如果支持 MCP、Built-in Tool、Remote Tool、Code Mode、Subagent（子Agent） Tool，Router 还要统一不同来源。

---

<a id="section-4"></a>

## 4. 为什么需要 Namespace

<a id="legacy-05-04"></a>

多个来源可能都有：

```text
search
read
execute
```

可以使用：

```text
filesystem.read
jira.search
github.search
mcp.crm.lookup
```

Namespace 解决：

- collision；
- provenance；
- permission；
- ownership；
- observability。

---

<a id="section-5"></a>

## 5. Tool Exposure 不应该只有“注册 / 未注册”

<a id="legacy-05-05"></a>

成熟 Runtime 往往需要多种暴露模式：

```text
Direct
Deferred / Discoverable
Hidden
Code-only / Internal
Tenant-scoped
Environment-scoped
```

一个 Tool 可能存在于 Registry，但当前模型不能直接看到。

---

<a id="section-6"></a>

## 6. Progressive Discovery 的核心

<a id="legacy-05-06"></a>

当 Tool 数量很大时：

```text
先给能力目录 / namespace summary
→ Model / Router 识别需要哪个能力域
→ Tool Search / Capability Search
→ 加载少量相关 Schema
→ 再调用具体 Tool
```

这和传统数据库：

```text
先读 catalog
再访问具体 object
```

有些相似。

直接给十来个小工具的完整说明，往往最简单。数量或描述体积很大时，可以采用 Progressive discovery（渐进发现）：先向模型提供搜索目录的能力或少量候选摘要，找到相关工具后，再加载候选工具的完整参数说明。

| 路径 | 模型先得到什么 | 后面发生什么 | 适用代价 |
|---|---|---|---|
| 直接暴露 | 当前允许工具的完整Schema | 直接选工具 | 简单，但大量Schema占输入预算 |
| 程序预筛选 | 按任务/权限筛过的少量完整说明 | 模型在候选中选择 | 筛选错可能漏掉正确工具 |
| 延迟发现 | 搜索工具和摘要/名称等目录信息 | 搜索后加载命中工具 | 多一次发现过程，要测试召回与权限 |

**按需加载的“完整”通常指模型所需完整说明，不是把处理器代码、凭证和所有宿主字段送给模型。** 有的API允许把延迟标记的Schema先提交给服务端，由服务端控制何时呈现给模型；网络请求携带的工具定义、模型实际可见内容、占用/计费方式也不能简单视为相同。

---

<a id="section-7"></a>

## 7. Tool Discovery 可以怎么做

<a id="legacy-05-07"></a>

### Rule / Intent Filter

```text
“查工单” → jira tools
“改代码” → filesystem + shell + test tools
```

优点：快、稳定。

### Embedding / Semantic Search

对 Tool name / description / metadata 建索引，根据当前任务召回候选 Tool。

### LLM Router

让一个较小模型先做 capability classification。

### Hybrid

```text
hard policy filter
→ rule / intent narrowing
→ semantic tool retrieval
→ main model final choose
```

通常更稳。

---

<a id="section-8"></a>

## 8. Discovery 的 Evaluation

<a id="legacy-05-08"></a>

不能只看最终任务成功率。

还应测：

```text
Tool Recall@K
Tool Selection Accuracy
Wrong-tool Rate
Discovery Latency
Schema Tokens Loaded
Fallback Rate
```

如果正确 Tool 根本没被召回，后面的 Main Agent 再强也没用。

正确工具没进入候选集合，是发现阶段问题；候选齐全但模型选错，是描述与选择问题。分别测候选召回、选择准确性和调用结果，不能看到选错就一律换模型。

---

<a id="section-9"></a>

## 9. Tool Unavailable 怎么办

<a id="legacy-05-09"></a>

候选 Tool 可能：

- server down；
- permission denied；
- version mismatch；
- tenant 不可用；
- health degraded。

Runtime 应区分：

```text
not found
not exposed
temporarily unavailable
permission denied
unsupported version
```

然后决定：

```text
repair route
fallback capability
ask user
fail fast
```

备用工具不能借“恢复”扩大权限。只读来源失效可以选等价来源；替代动作若变成写入或扩大范围，必须重新检查任务与批准。

---

<a id="section-10"></a>

## 10. Registry 更新与版本问题

<a id="legacy-05-12"></a>

新增 / 升级 Tool 时需要考虑：

```text
schema compatibility
cache invalidation
old checkpoint resume
running session snapshot
permission policy
benchmark regression
```

一个长任务不应该在执行中途无意识地从 Tool v1 切到不兼容的 v2。

可以保存：

```text
capability_snapshot_id
schema_version
resolved_tool_version
```

---

<a id="section-11"></a>

## 11. 产品实现与官方资料对照（按需展开）

<details>
<summary>源码证据：Codex</summary>

<a id="legacy-05-10"></a>

固定快照中的 `ToolRouter` 明确区分：

- full registry；
- `model_visible_specs`；
- deferred tool search；
- namespace；
- code-mode tool identity。

`ToolExposure` 还能表达：

```text
Direct
Deferred
DeferredModelOnly
DirectModelOnly
CodeModeOnly
Hidden
```

这直接证明：

> 注册能力与本轮向模型暴露能力是两件事。

### Codex 固定源码：注册表与 model_visible_specs 的真实连接

`codex-rs/core/src/tools/router.rs`中的`ToolRouter`同时保存`registry: ToolRegistry`和`model_visible_specs`。`session/turn.rs::build_prompt`把`tool_router.model_visible_specs()`放进模型请求的`tools`字段；真实工具执行则由Registry和处理器承担。

可以直接跟一项工具：`tools/handlers/plan.rs`的`PlanHandler`定义名字`update_plan`，`spec()`返回说明，`handle()`解析参数并调用内部处理流程。模型看见的是规格，程序保留处理器；计划更新后还会发出`PlanUpdate`事件。这比“工具注册到LLM里”更精确。

该快照还支持不同暴露/延迟发现路径。是否全部直接暴露取决于配置与工具类型，不能把某条路径说成所有Codex调用都使用的唯一机制。

</details>

<details>
<summary>源码证据：Claude Code</summary>

<a id="legacy-05-11"></a>

固定快照的 `Tool.ts` 中存在 `searchHint`，`ToolUseContext` 还包含 dynamic skill discovery / discovered skill names 等状态。

这与 HUMAN-A 中“Tool/Skill（技能包） > 100 后如何按需发现”高度呼应。

### Claude Code 用户快照：getTools → toolToAPISchema → tool result

`tools.ts::getAllBaseTools()`列出内置工具对象；`getTools()`依据模式、开关和deny规则选择工具。外部MCP工具有自己的连接与合并流程，不在这个内置函数里凭空变成代码。

`utils/api.ts::toolToAPISchema`取工具的名字、`prompt()`生成的描述、输入JSON Schema或由Zod转换的模式，再按能力增加严格模式、延迟加载和缓存等API字段。它使用稳定基础Schema缓存及每请求的覆盖字段，避免无必要地改变请求字节。

`query.ts`把工具对象交给模型调用封装，也交给工具执行器。模型返回`tool_use`后运行时找到实际对象；`TodoWriteTool.ts`说明内部还可更新应用状态，并用单独的结果映射方法生成`tool_result`。这条路径清楚展示“宿主对象”和“模型可见表示”不是同一份数据。

</details>

具体实现以[固定源码与官方索引](../../../references/agent/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

<a id="human-a"></a>

## 12. HUMAN-A 信号

- `AGENT-019` Tool Lifecycle：10 来源；
- `AGENT-021` Dynamic Discovery / Progressive Loading：20 来源；
- `AGENT-024` / `AGENT-025` Tool / Skill / MCP 边界与 Progressive Disclosure。

Verified Chain 中 `S077`、`S214`、`S236`、`S274` 都出现：

```text
Tool 多了
→ Discovery / Lazy Loading
→ Tool unavailable / failure
→ Schema / Permission / Fallback
```

---

<a id="interview"></a>

## 13. 面试怎么答

### Q：注册、发现和调用怎样配合？

🎯 **30 秒回答**：

> Tool Registry 是完整能力目录，当前 Model-visible Tool Set 只是它经过 tenant、policy、task 和 discovery 筛选后的一个视图。Tool 数量大时不应该把所有 Schema 一次塞入 Context，而应通过 namespace、intent/rule、semantic tool search 或混合路由做 Progressive Discovery，再把少量候选 Tool 暴露给模型。Router 负责把模型 Tool Call 解析到具体 runtime handler，并做版本、exposure 和 policy 检查。

### Q：工具怎样注册并最终调用？

🎯 **30 秒回答**：

> 先由应用把工具的稳定身份和处理器加入注册目录，再为本次模型请求选择并序列化允许工具的说明。模型返回名字和参数后，路由器按身份找到处理器，经校验与授权后执行，最后规范化结果回填。MCP工具的处理器通常是一个远程调用代理，并不是把远端代码下载进模型。

### Q：加载工具时，是否会把所有注册信息都加入上下文？

🎯 **30 秒回答**：

> 不会自动全部加入。注册表保留实现、连接和运行策略；模型侧主要需要名称、说明、输入格式及支持的可选字段。渐进发现只改变何时暴露候选说明，不意味着最后把凭证、函数和所有元数据都送给模型。还需区分服务端收到延迟定义和模型实际看见它。

### Q：为什么工具多时要分目录、候选和调用三个阶段？

🎯 **30 秒回答**：

> 目录可能很大，而一次任务只需少量工具。先发现候选能节省上下文并降低歧义，但会引入漏召回和额外延迟；候选进入后模型才选择具体调用，执行时仍检查合法性。评估要分别看正确工具能否被找到、找到后能否正确选择，而非只看最终成功率。

### Q：两个外部Server都提供search，怎样处理？

🎯 **30 秒回答**：

> 使用命名空间或稳定工具身份，并保存身份到Server与Client的映射。不要按最后注册覆盖前一项；模型调用应解析到唯一目标。清单变更时检查旧调用兼容性和当前权限，必要时刷新清单或拒绝，而不是把同名调用静默送到另一个系统。

### Q：Codex 与 Claude Code 中，哪里能看到这种分离？

🎯 **30 秒回答**：

> Codex ToolRouter分别保存Registry和model_visible_specs，build_prompt取后者发送；处理器保留本地执行逻辑。Claude Code快照的getTools选择实际对象，toolToAPISchema转换模型说明，调用后再由工具结果映射生成回填。这是源码中可追踪的生命周期，不只是概念图。

---

<a id="pitfalls"></a>

## 14. 高频易错点

⚠️ Registry = 当前 Tool List——错；

⚠️ Tool 越多模型越强——可能反而更难选择；

⚠️ Discovery 只做 embedding search——不是唯一方案；

⚠️ Tool Search 命中就直接执行——仍需 Validation / Permission（权限）；

⚠️ 长任务中 Tool Catalog 可以随意变化——会破坏 Resume（恢复执行） / Replay（重放）。

⚠️ **注册就是给模型安装函数。** 注册在应用中发生；模型得到说明并产生调用候选。

⚠️ **延迟加载完成后会发送全部宿主字段。** 完整Schema不等于完整实现、权限对象或凭证。

⚠️ **看不见的工具必然不在注册表。** 注册表可以大于本轮可见工具集。

⚠️ **工具召回不准就是参数描述不好。** 也可能候选筛选阶段已漏掉正确工具。

⚠️ **工具清单被缓存就无需调用时检查。** 权限、版本和可用性仍可能改变。

---

<a id="self-test"></a>

## 15. 本章自测

<details><summary>1. 自测：为什么 Deferred Tool 能同时降低 Token 和风险？</summary>

因为它既不把所有 Schema 放进每轮 Context，也不默认向模型暴露所有能力；只有经过 Discovery / Policy 后才进入当前可见集合。

</details>

<details><summary>2. 示例里handler为何不出现在visible_specs？</summary>

函数对象不是模型API需要的JSON说明，真实代码在宿主执行。显式挑字段让边界清晰，也避免把内部配置和敏感信息误序列化。

</details>

<details><summary>3. 工具说明写了只读，但函数实际上发送邮件，应相信谁？</summary>

这代表契约与实现失配，需要修实现、描述与可信策略并测试。不能因为模型看到只读描述就将其当安全操作；外部说明也可能不可信。

</details>

<details><summary>4. 只有5个简单工具，需要语义发现系统吗？</summary>

未必。直接暴露经权限筛选的说明更容易维护。先测Schema成本和误选，再判断发现系统的复杂度是否有收益。

</details>

<details><summary>5. 候选中根本没有正确工具，怎么排查？</summary>

检查权限误过滤、命名空间、描述关键词和检索召回；对固定查询集观察候选命中。此时单纯调整模型选工具提示通常治不了根因。

</details>

<details><summary>6. MCP工具的本地handler可能是什么？</summary>

它可以是一个调用代理：接收已校验参数，选择对应MCP Client，把请求发送给Server，再转换结果。远端业务实现仍在Server或其后面的系统中。

</details>

<details><summary>7. 同一名字输入Schema升级，旧候选怎么办？</summary>

明确版本/兼容性规则。可兼容的变化按约定解析；不兼容时重新发现或返回明确错误，不能悄悄把旧参数解释成新的业务动作。

</details>

---

[← 上一章](04-ToolContractAndValidation.md) · [Agent 目录](../README.md) · [下一章 →](06-ToolExecutionAndFailure.md)
