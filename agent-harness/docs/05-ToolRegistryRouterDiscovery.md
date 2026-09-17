# 05. 工具注册、模型可见说明与按需发现

[← 上一章](04-ToolContractSchemaValidation.md) · [模块目录](../README.md) · [下一章 →](06-ToolExecutionFailure.md)

> 本章要解决：模型工具究竟怎么注册？注册目录、模型说明书、发现与执行之间如何连接？

## 1. “注册”不是把函数装进模型大脑

Registration（注册）是把一个工具名称和它的实际处理方法加入应用的目录。Registry（注册表）是这个目录；模型并不知道你内存里的函数地址。每次调用模型时，应用再把允许使用的工具说明交给模型。模型返回名字与参数后，Router（路由器）查注册表，Executor（执行器）才调用函数。

```text
开发者定义工具 → 加入应用注册表
                      ├→ 选择模型可见说明 → 模型生成调用候选
                      └← 名称查处理器 ← 解析与校验候选
                                      ↓
                                  执行与回填
```

因此常说的“注册工具”其实容易混淆两步：**让程序知道怎么执行**，以及**让模型知道什么可调用**。注册了但本轮不暴露的工具仍可能存在于程序目录中；模型能看见说明也不等于当前参数已获批准。

## 2. 可运行例子：看清楚两份对象

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

## 3. 工具多了，如何少发说明书

直接给十来个小工具的完整说明，往往最简单。数量或描述体积很大时，可以采用 Progressive discovery（渐进发现）：先向模型提供搜索目录的能力或少量候选摘要，找到相关工具后，再加载候选工具的完整参数说明。

| 路径 | 模型先得到什么 | 后面发生什么 | 适用代价 |
|---|---|---|---|
| 直接暴露 | 当前允许工具的完整Schema | 直接选工具 | 简单，但大量Schema占输入预算 |
| 程序预筛选 | 按任务/权限筛过的少量完整说明 | 模型在候选中选择 | 筛选错可能漏掉正确工具 |
| 延迟发现 | 搜索工具和摘要/名称等目录信息 | 搜索后加载命中工具 | 多一次发现过程，要测试召回与权限 |

**按需加载的“完整”通常指模型所需完整说明，不是把处理器代码、凭证和所有宿主字段送给模型。** 有的API允许把延迟标记的Schema先提交给服务端，由服务端控制何时呈现给模型；网络请求携带的工具定义、模型实际可见内容、占用/计费方式也不能简单视为相同。

## 4. 外部 MCP 工具怎么进入同一目录

本地工具由开发者代码注册。MCP工具通常先连接外部Server并列出工具，Host保存“名称→哪一个Client→哪一个Server工具”的映射，同时把合适说明转成模型API支持的格式。真正执行时仍通过该Client发起远程调用，而不是模型自己连接数据库。第16章完整解释MCP协议。

不同Server可能都有`search`。目录需要命名空间或其他稳定身份，不能后注册的覆盖前一个。缓存的工具清单过期时，旧候选可能已不可用；执行前需要解析当前目标与兼容格式，再决定刷新或返回明确错误。

## 5. 发现质量也必须验证

一次选错工具至少可能发生在两个阶段：正确工具没有进入候选集合，或进入后模型选错。分别检查候选召回、歧义描述、授权过滤和参数生成。不要看到错误就只换更强模型。

目录可用率、发现延迟和Schema体积也有成本。小目录不一定值得建设语义搜索；开发者能用明确规则筛选时，规则可能更稳定。版本只需要解决“这个名字当前对应的输入输出是否兼容”，不是给每次发现事件制造一套独立版本历史。

<details>
<summary>Codex 固定源码：注册表与 model_visible_specs 的真实连接</summary>

`codex-rs/core/src/tools/router.rs`中的`ToolRouter`同时保存`registry: ToolRegistry`和`model_visible_specs`。`session/turn.rs::build_prompt`把`tool_router.model_visible_specs()`放进模型请求的`tools`字段；真实工具执行则由Registry和处理器承担。

可以直接跟一项工具：`tools/handlers/plan.rs`的`PlanHandler`定义名字`update_plan`，`spec()`返回说明，`handle()`解析参数并调用内部处理流程。模型看见的是规格，程序保留处理器；计划更新后还会发出`PlanUpdate`事件。这比“工具注册到LLM里”更精确。

该快照还支持不同暴露/延迟发现路径。是否全部直接暴露取决于配置与工具类型，不能把某条路径说成所有Codex调用都使用的唯一机制。

</details>

<details>
<summary>Claude Code 用户快照：getTools → toolToAPISchema → tool result</summary>

`tools.ts::getAllBaseTools()`列出内置工具对象；`getTools()`依据模式、开关和deny规则选择工具。外部MCP工具有自己的连接与合并流程，不在这个内置函数里凭空变成代码。

`utils/api.ts::toolToAPISchema`取工具的名字、`prompt()`生成的描述、输入JSON Schema或由Zod转换的模式，再按能力增加严格模式、延迟加载和缓存等API字段。它使用稳定基础Schema缓存及每请求的覆盖字段，避免无必要地改变请求字节。

`query.ts`把工具对象交给模型调用封装，也交给工具执行器。模型返回`tool_use`后运行时找到实际对象；`TodoWriteTool.ts`说明内部还可更新应用状态，并用单独的结果映射方法生成`tool_result`。这条路径清楚展示“宿主对象”和“模型可见表示”不是同一份数据。

</details>

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. 工具怎样注册并最终调用？

<details>
<summary>参考答案</summary>

先由应用把工具的稳定身份和处理器加入注册目录，再为本次模型请求选择并序列化允许工具的说明。模型返回名字和参数后，路由器按身份找到处理器，经校验与授权后执行，最后规范化结果回填。MCP工具的处理器通常是一个远程调用代理，并不是把远端代码下载进模型。

</details>

### 2. 加载工具时，是否会把所有注册信息都加入上下文？

<details>
<summary>参考答案</summary>

不会自动全部加入。注册表保留实现、连接和运行策略；模型侧主要需要名称、说明、输入格式及支持的可选字段。渐进发现只改变何时暴露候选说明，不意味着最后把凭证、函数和所有元数据都送给模型。还需区分服务端收到延迟定义和模型实际看见它。

</details>

### 3. 为什么工具多时要分目录、候选和调用三个阶段？

<details>
<summary>参考答案</summary>

目录可能很大，而一次任务只需少量工具。先发现候选能节省上下文并降低歧义，但会引入漏召回和额外延迟；候选进入后模型才选择具体调用，执行时仍检查合法性。评估要分别看正确工具能否被找到、找到后能否正确选择，而非只看最终成功率。

</details>

### 4. 两个外部Server都提供search，怎样处理？

<details>
<summary>参考答案</summary>

使用命名空间或稳定工具身份，并保存身份到Server与Client的映射。不要按最后注册覆盖前一项；模型调用应解析到唯一目标。清单变更时检查旧调用兼容性和当前权限，必要时刷新清单或拒绝，而不是把同名调用静默送到另一个系统。

</details>

### 5. Codex 与 Claude Code 中，哪里能看到这种分离？

<details>
<summary>参考答案</summary>

Codex ToolRouter分别保存Registry和model_visible_specs，build_prompt取后者发送；处理器保留本地执行逻辑。Claude Code快照的getTools选择实际对象，toolToAPISchema转换模型说明，调用后再由工具结果映射生成回填。这是源码中可追踪的生命周期，不只是概念图。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| 注册就是给模型安装函数 | 注册在应用中发生；模型得到说明并产生调用候选。 |
| 延迟加载完成后会发送全部宿主字段 | 完整Schema不等于完整实现、权限对象或凭证。 |
| 看不见的工具必然不在注册表 | 注册表可以大于本轮可见工具集。 |
| 工具召回不准就是参数描述不好 | 也可能候选筛选阶段已漏掉正确工具。 |
| 工具清单被缓存就无需调用时检查 | 权限、版本和可用性仍可能改变。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：示例里handler为何不出现在visible_specs？

<details>
<summary>查看参考答案</summary>

函数对象不是模型API需要的JSON说明，真实代码在宿主执行。显式挑字段让边界清晰，也避免把内部配置和敏感信息误序列化。

</details>

### 自测 2：工具说明写了只读，但函数实际上发送邮件，应相信谁？

<details>
<summary>查看参考答案</summary>

这代表契约与实现失配，需要修实现、描述与可信策略并测试。不能因为模型看到只读描述就将其当安全操作；外部说明也可能不可信。

</details>

### 自测 3：只有5个简单工具，需要语义发现系统吗？

<details>
<summary>查看参考答案</summary>

未必。直接暴露经权限筛选的说明更容易维护。先测Schema成本和误选，再判断发现系统的复杂度是否有收益。

</details>

### 自测 4：候选中根本没有正确工具，怎么排查？

<details>
<summary>查看参考答案</summary>

检查权限误过滤、命名空间、描述关键词和检索召回；对固定查询集观察候选命中。此时单纯调整模型选工具提示通常治不了根因。

</details>

### 自测 5：MCP工具的本地handler可能是什么？

<details>
<summary>查看参考答案</summary>

它可以是一个调用代理：接收已校验参数，选择对应MCP Client，把请求发送给Server，再转换结果。远端业务实现仍在Server或其后面的系统中。

</details>

### 自测 6：同一名字输入Schema升级，旧候选怎么办？

<details>
<summary>查看参考答案</summary>

明确版本/兼容性规则。可兼容的变化按约定解析；不兼容时重新发现或返回明确错误，不能悄悄把旧参数解释成新的业务动作。

</details>

## 资料与下一步

固定源码：[codex-rs/core/src/tools/router.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/tools/router.rs)、[codex-rs/core/src/session/turn.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/turn.rs)、[codex-rs/core/src/tools/handlers/plan.rs](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/tools/handlers/plan.rs)、[tools.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/tools.ts)、[utils/api.ts](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/utils/api.ts)。下一章只展开执行后的结果与错误去向。

本章对应研究能力：`AGENT-018`、`AGENT-019`、`AGENT-021`、`AGENT-022`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](04-ToolContractSchemaValidation.md) · [模块目录](../README.md) · [下一章 →](06-ToolExecutionFailure.md)
