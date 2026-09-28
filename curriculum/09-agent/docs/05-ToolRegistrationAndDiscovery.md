# 05. 工具注册与发现：程序有的，不一定都给模型看

[← 上一章](04-ToolContractAndValidation.md) · [Agent 目录](../README.md) · [下一章 →](06-ToolExecutionAndFailure.md)

报告助手有两个工具时，用名字找到函数并不难。但接入多个资料系统后，可能出现几百项工具，其中好几个都叫 search。每次把它们全部交给模型，会花更多输入预算，也更容易选错。

先区分两件事：应用知道怎样执行哪些工具；模型这一次知道可以选择哪些工具。

<a id="1-registry-解决什么"></a>
<a id="legacy-05-01"></a>
<a id="section-1"></a>
<a id="core-1"></a>

## 1. 注册是在应用里建立执行目录

**Registry（注册表）**把工具身份与实际实现关联起来。**注册**就是把这项关联加入目录。模型不能直接调用你内存里的函数地址；它返回名称和参数后，程序再查目录，找到处理器。

```text
开发者定义工具 → 注册名称、说明和处理器
                       ├─ 取允许的说明 → 本次模型请求
                       └─ 名称查处理器 ← 模型返回调用候选
                                            ↓
                                        检查与执行
```

注册表可以保存函数、连接对象和运行策略；模型侧只接收其 API 支持的可序列化说明。将宿主对象转换成某个使用者所需表示，称为**投影**。这里不需要先记术语，只要能指出“函数留在哪，说明发给谁”。

<a id="2-registry-与-model-visible-tool-set-必须分开"></a>
<a id="legacy-05-02"></a>
<a id="section-2"></a>
<a id="core-2"></a>

## 2. 用同一个工具看两份表示

下面的标准库例子没有真实模型或网络，调用候选用字典模拟。它展示注册、说明投影、参数检查与授权拒绝；不是完整模型 SDK。

<details><summary>运行例子：注册表、模型说明与调用结果</summary>

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

保存为 `registry_projection.py` 后运行 `python registry_projection.py`。没有异常表示末尾断言成立。要观察说明，可以打印 `json.dumps(visible_specs, ensure_ascii=False)`；它不会包含 `handler` 或 `read_only`。

</details>

| 观察位置 | 里面有什么 | 为什么不同 |
|---|---|---|
| registry | 工具对象，包括实际函数 | 程序需要真正执行 |
| visible_specs | 名称、说明和输入 Schema | 模型需要选择与填参数 |
| allowed_documents | 可信应用允许读取的文档集合 | 不能由模型自己授予 |
| dispatch 返回 | ok、denied 或参数等错误 | 下一步必须知道实际结果 |

已注册 B 的读取能力，也不代表当前只允许 A 的任务可以读 B。发现阶段筛掉无权工具能减少误选，执行阶段仍要校验具体资源。

<a id="3-router-做什么"></a>
<a id="4-为什么需要-namespace"></a>
<a id="9-tool-unavailable-怎么办"></a>
<a id="legacy-05-03"></a>
<a id="legacy-05-04"></a>
<a id="legacy-05-09"></a>
<a id="section-3"></a>
<a id="section-4"></a>
<a id="section-9"></a>
<a id="core-3"></a>

## 3. 名称要能唯一指向实现

如果 GitHub 和工单服务都有 `search`，简单“后注册覆盖先注册”会把调用送错地方。可以使用 `github.search`、`jira.search` 这样的命名空间，或维护另外一套稳定身份映射。

**Router（路由器）**在这里负责解析调用身份、检查当前是否暴露和兼容，再找到正确处理器。MCP 工具的处理器可以是发往对应客户端的代理；它不是把远端代码装进模型。

目录变化时，旧候选可能引用已删除工具或旧 Schema。程序应明确返回不存在、不兼容、暂时不可用或权限拒绝；不能把同名请求静默送到不同系统。

<a id="6-progressive-discovery-的核心"></a>
<a id="7-tool-discovery-可以怎么做"></a>
<a id="embedding--semantic-search"></a>
<a id="hybrid"></a>
<a id="legacy-05-06"></a>
<a id="legacy-05-07"></a>
<a id="llm-router"></a>
<a id="rule--intent-filter"></a>
<a id="section-6"></a>
<a id="section-7"></a>
<a id="core-4"></a>

## 4. 工具多时，先缩小候选集合

只有少量简单工具时，直接提供经过权限筛选的完整说明往往最清楚。工具数量或说明体积很大，再考虑候选筛选与按需发现。

| 方式 | 模型先看什么 | 收益 | 代价 |
|---|---|---|---|
| 直接暴露 | 当前允许工具的完整说明 | 最少的发现步骤 | 大目录会占输入并增加歧义 |
| 程序预筛选 | 与任务相关的少量工具 | 控制成本，路径简单 | 筛错可能遗漏必要工具 |
| 渐进发现 | 搜索目录的工具或轻量摘要 | 需要时才加载详细说明 | 增加发现调用，需检查召回 |

候选可以按明确规则筛选，也可以对用途做语义检索，或用分类模型辅助。通常先用可信权限缩小范围，再选择适合任务的候选。算法不是越复杂越好；没有真实漏选或预算问题时，不必先建工具向量库。

**按需加载的“完整”指完整使用说明，不是凭证、处理器代码和所有宿主字段。** 有的服务接受延迟工具定义，再决定何时让模型看到；请求中发送、模型实际可见和计费处理也要按具体 API 分开核对。

<a id="8-discovery-的-evaluation"></a>
<a id="legacy-05-08"></a>
<a id="section-8"></a>
<a id="core-5"></a>

## 5. 发现失败和选择失败，不要用同一种补救

假设正确工具是“读取批准版本”：

1. 候选集合没有它：检查权限过滤、工具元数据和目录召回。
2. 候选里有它，模型却选择“读取草案”：检查描述歧义与选择质量。
3. 已选对但参数错：回到工具契约校验。
4. 参数正确，服务却不可用：回到执行错误与恢复策略。

用固定任务比较候选召回、选择准确性、错误工具率、发现时延和加载的说明量。不要把所有失败都归因于主模型不够强，也不要只看最终成功率而掩盖目录遗漏。

> ⚠️ 备用工具必须仍在任务允许范围内。只读资料服务失效，不意味着可以自动改用权限更大的通用 Shell。

<a id="10-registry-更新与版本问题"></a>
<a id="5-tool-exposure-不应该只有注册--未注册"></a>
<a id="legacy-05-05"></a>
<a id="legacy-05-12"></a>
<a id="section-10"></a>
<a id="section-5"></a>
<a id="core-6"></a>

## 6. 目录也有生命周期

工具可以直接可见、需要发现后加载、只供内部调用，或对某个租户和环境不可用。它们是暴露策略，不要求每个项目照抄同一组枚举。

长任务开始时可以固定一份能力配置引用。工具升级后，明确哪些变化兼容，旧运行是否继续使用原配置，还是重新发现或暂停。缓存说明能节省工作，但不能让权限、版本和可用性从此永久有效。

<a id="summary"></a>

## 本章小结

注册解决程序怎样找到实现，暴露解决模型本次知道什么，发现解决如何从大目录找到候选，执行仍要检查具体输入与权限。把这些阶段分开，才能定位“选不到、选错、参数错、执行错”。

<a id="13-面试怎么答"></a>
<a id="qcodex-与-claude-code-中哪里能看到这种分离"></a>
<a id="q两个外部server都提供search怎样处理"></a>
<a id="q为什么工具多时要分目录候选和调用三个阶段"></a>
<a id="q加载工具时是否会把所有注册信息都加入上下文"></a>
<a id="q工具怎样注册并最终调用"></a>
<a id="q注册发现和调用怎样配合"></a>
<a id="interview"></a>

## 🎯 面试怎么回答

### 注册工具是不是把函数安装给模型？

不是。应用保存名称到处理器的关联，再把允许工具的说明序列化给模型。模型生成调用候选，宿主查表、校验并执行，结果再回填。

### 工具太多时怎样优化？

先测说明量和误选，再选择权限过滤、任务预筛选或渐进发现。发现后加载模型需要的完整说明，不发送凭证与函数。评估分别看候选召回、选择质量、时延和成本。

### 工具清单已缓存，调用时还要检查吗？

需要。缓存主要复用说明，不能保证资源授权、版本和可用性未变。具体调用仍应绑定正确身份和目标，防止清单过期造成错路由。

<a id="14-高频易错点"></a>
<a id="pitfalls"></a>

## ⚠️ 易错点

> ⚠️ 工具存在于注册表，不等于当前任务可以使用；模型看见说明也不等于参数已获批准。

> ⚠️ 同名工具不能默默互相覆盖，应以稳定身份定位到唯一实现和来源。

> ⚠️ 候选召回漏掉工具时，单纯改主模型提示通常不能补回缺失能力。

<a id="15-本章自测"></a>
<a id="self-test"></a>

## 本章自测

<details><summary>1. 只有五个简单工具，应立即建设语义发现系统吗？</summary>

未必。先直接暴露允许的工具并测量输入成本与误选。只有这些问题真实存在，才比较发现系统的复杂度是否值得。

</details>

<details><summary>2. registry_projection 中读 B 为什么返回 denied？</summary>

应用传入的允许文档集合只有 A。B 存在和工具已注册，都不能替代本次资源授权。

</details>

<details><summary>3. 正确工具在目录里却始终不在候选中，应该先检查什么？</summary>

检查权限是否误过滤、任务分类和检索是否遗漏、描述是否能被找到；先修发现阶段，而不是假设模型拿到工具后仍不会用。

</details>

<a id="05-tool-registry工具注册模型可见说明与按需发现"></a>
<a id="11-产品实现与官方资料对照按需展开"></a>
<a id="12-human-a-信号"></a>
<a id="claude-code-用户快照gettools--tooltoapischema--tool-result"></a>
<a id="codex-固定源码注册表与-model_visible_specs-的真实连接"></a>
<a id="human-a"></a>
<a id="legacy-05-10"></a>
<a id="legacy-05-11"></a>
<a id="section-11"></a>
<a id="references"></a>

## 知识回看与权威资料

- [工具契约](04-ToolContractAndValidation.md)：回看说明、输入规则与授权边界。
- [MCP 完整往返](16-MCPArchitectureAndLifecycle.md)：观察外部目录怎样接到宿主工具系统。
- [固定注册与投影实现](../../../references/agent/implementation-notes.md#chapter-05)：跟踪注册表、模型可见说明和处理器的实际分离。


---

[← 上一章](04-ToolContractAndValidation.md) · [Agent 目录](../README.md) · [下一章 →](06-ToolExecutionAndFailure.md)
