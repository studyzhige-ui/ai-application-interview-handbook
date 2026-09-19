# 04. Tool Contract：工具说明、参数与语义校验

给同事一个函数名，他未必知道怎样调用；给模型一个函数名，问题更明显。工具先需要一份清楚的说明，再需要真正受控的执行。我们从这两件事开始，而不是先背Schema字段。

[← 上一章](03-AgentLoopAndExecutionScopes.md) · [Agent 目录](../README.md) · [下一章 →](05-ToolRegistrationAndDiscovery.md)

---

<a id="section-1"></a>

## 1. 先讲人话：为什么 Tool 不能只写成一个 Python 函数

<a id="legacy-04-01"></a>

先分“说明书”和“干活的程序”：模型需要名称、用途与参数格式，宿主需要实现、权限与调度信息。它们属于同一工具契约，但不代表同一份对象全部进入模型。

Demo：

```python
# 契约示意：名称/描述/参数可形成模型说明；风险信息与handler供宿主执行。
def search_code(query: str) -> str:
    ...
```

Production（生产环境） 还必须回答：

```text
Tool 叫什么？
模型看到什么描述？
输入 Schema 是什么？
字段缺失 / 类型错怎么办？
这个 Tool 是否只读？
能不能并发？
是否需要权限？
会不会产生外部副作用？
怎样取消？
怎样返回结构化结果？
结果是否会污染 Context / Memory？
```

所以 Tool Contract 更接近：

```text
Identity
+ Description
+ Input Schema
+ Validation
+ Execution Semantics
+ Side-effect Semantics
+ Permission
+ Cancellation / Progress
+ Result Contract
```

---

<a id="section-2"></a>

## 2. Tool Contract 的最小结构

<a id="legacy-04-02"></a>

```python
# 契约示意：名称/描述/参数可形成模型说明；风险信息与handler供宿主执行。
from dataclasses import dataclass
from typing import Callable, Any

@dataclass
class ToolSpec:
    name: str
    description: str
    input_schema: dict  # 模型/程序共同约定的参数结构
    read_only: bool
    destructive: bool
    concurrency_safe: bool
    handler: Callable[..., Any]  # 宿主的真实实现，不发送给模型
```

真实系统还会增加 version、timeout、permission class、tenant scope、result schema 等。

`name/description/input_schema`帮助模型选择并填参数；`handler/call()`、凭证、权限回调和并发信息由宿主持有。后面注册章会把两条路径接起来。只读是风险判断线索，不是绝对安全证明：它仍可能读取秘密。

---

<a id="section-3"></a>

## 3. Schema 解决两个完全不同的问题

<a id="legacy-04-03"></a>

### Model-facing Schema

帮助模型生成：

```json
{
  "query": "ToolExecutor",
  "path": "codex-rs/core"
}
```

### Runtime Validation

决定这个输入**实际上能不能执行**。

模型生成了 JSON，不意味着可信。

因此完整路径：

```text
Model produces arguments
→ Parse
→ Schema validate
→ Semantic validate
→ Permission validate
→ Execute
```

---

<a id="section-4"></a>

## 4. 结构校验 vs 语义校验

<a id="legacy-04-04"></a>

Schema 能发现：

```text
missing field
wrong type
unknown enum
invalid JSON
```

但发现不了：

```text
path = ../../etc/passwd
amount = -100
branch = production
user_id 属于其它 tenant
```

这属于 Semantic / Policy Validation。

不要把：

```text
JSON Schema valid
```

误认为：

```text
这个动作安全且业务正确
```

以 `read_document`为例：

| 检查 | 问的问题 | 失败例子 | 谁修 |
|---|---|---|---|
| Parse（解析） | 是否能按协议读懂输入？ | JSON缺引号 | 可给模型简明反馈修复 |
| Schema validation（结构校验） | 字段和类型是否符合约定？ | ID是数组、多了未知字段 | 按契约修复 |
| Semantic validation（语义校验） | 在该业务里有无意义？ | 空ID、版本不存在、起始行大于结束行 | 提供可行动的业务错误 |
| Authorization（授权） | 当前可信身份能否对目标做该动作？ | 文档属于别的用户 | 程序拒绝；不能靠模型改身份绕过 |

审批与沙箱是另一组问题：某个高风险但可授权的动作是否需要人确认，以及执行环境能够触及哪里。第14章讲它们；这里不再复制安全清单。**前两类合法不推出最后一类合法。** 这种分工在后续章节保持不变。

检查也可能重复执行：发现工具时隐藏无权工具，调用时再校验资源授权。前一次检查减少误选，后一次防止权限变化或恶意参数；不是无意义重复。

---

<a id="section-5"></a>

## 5. Tool Description 也是协议的一部分

<a id="legacy-04-05"></a>

Tool 很多时，模型选择能力依赖：

- name；
- description；
- 参数语义；
- 示例；
- failure / limitation；
- search metadata。

描述太模糊：

```text
run(command)
```

很难帮助模型选择。

更明确：

```text
run_tests(target, timeout_seconds)
Runs repository tests for a specific target.
Does not modify source files.
```

Tool quality 不只是 handler 实现质量，还包括**模型是否能正确发现和使用它**。

---

<a id="section-6"></a>

## 6. Structured Result 也应该有 Contract

<a id="legacy-04-06"></a>

不要默认返回：

```text
一大段字符串
```

更稳定：

```json
{
  "status": "failed",
  "exit_code": 1,
  "summary": "2 tests failed",
  "artifact_ref": "tool-results/call_123.txt",
  "retryable": false
}
```

这样：

- Runtime（运行时执行系统） 能分支；
- Model 更容易理解；
- Trace（执行追踪） 更容易统计；
- 大结果可外部化。

空结果可能意味着“材料为空”“没有权限”“不存在”或“连接中断”。结果契约是让程序和模型区分这些情况，不是让所有工具都返回几十个相同字段。

---

<a id="section-7"></a>

## 7. Tool Arguments 出错时怎么处理

<a id="legacy-04-07"></a>

常见错误分类：

```text
Syntax Error
Schema Error
Semantic Error
Permission Error
Execution Error
Timeout
```

对于前两类，可把结构化错误反馈给模型做一次 Repair：

```json
{
  "error": "invalid_arguments",
  "field": "timeout_seconds",
  "expected": "integer between 1 and 300"
}
```

而不是：

```text
Exception: validation failed
```

---

<a id="section-8"></a>

## 8. Repair 不能无限循环

<a id="legacy-04-08"></a>

一个安全策略：

```text
invalid arguments
→ return structured feedback
→ model repairs
→ retry once / limited times
→ repeated same failure
→ alternate route or stop
```

必须与后面的 Loop Guard / Budget（预算） 联动。

---

<a id="section-9"></a>

## 9. Side-effect Metadata 为什么应该靠 Runtime 保存

<a id="legacy-04-09"></a>

模型可能说：

> “这个 Tool 只是读取。”

这不能作为安全依据。

Tool Contract 应由 Host / Runtime 声明：

```text
read_only
is_destructive
concurrency_safe
requires_approval
```

后续 Permission（权限） / Scheduler 只信 Runtime Metadata，不信模型自述。

---

<a id="section-10"></a>

## 10. 版本升级怎么办

<a id="legacy-04-12"></a>

Tool Schema 变化可能破坏：

- Prompt cache；
- Model selection behavior；
- Replay（重放）；
- persisted Run；
- old Checkpoint（检查点）；
- Evaluation Dataset。

因此成熟 Tool 可以保存：

```text
tool_name
schema_version
runtime_version
```

并在 Resume（恢复执行） / Replay 时明确兼容策略。

版本解决真实的不兼容变化。一个Run可以引用一份工具配置，而不必每次调用复制所有版本全文。执行中换成不兼容接口时，应明确冻结、迁移或停止；不能静默改变已批准动作的含义。

---

<a id="section-11"></a>

## 11. 产品实现与官方资料对照（按需展开）

<details>
<summary>源码证据：Claude Code</summary>

<a id="legacy-04-10"></a>

固定快照的 `Tool.ts` 显示 Tool Contract 不只包含 Schema 和 `call()`，还包含：

- `isConcurrencySafe()`；
- `isReadOnly()`；
- `isDestructive()`；
- `interruptBehavior()`；
- Permission Context；
- Progress Callback；
- Result / Context Modifier；
- Tool Result Budget / Dynamic Discovery 相关状态。

这非常适合说明：

> Production Tool 是 Runtime Contract，不是 Function Signature。

</details>

<details>
<summary>源码证据：Codex</summary>

<a id="legacy-04-11"></a>

固定 Codex 快照中的 `ToolExecutor` 把：

```text
tool_name
spec
exposure
search_info
supports_parallel_tool_calls
handle(invocation)
```

放在同一个执行契约中。

`ToolOutput` 又把：

- model-facing response；
- logging projection；
- host-only metadata；
- external context 标记；

分开表达。

这说明 Tool Input / Output 都应被 Runtime 当成正式协议对象。

</details>

具体实现以[固定源码与官方索引](../../../references/agent/README.md#reader-revision-20260917)为准。这里区分源码事实、功能开关与教学建议，不把一条实现路径当作所有产品默认行为。

---

<a id="human-a"></a>

## 12. HUMAN-A 信号

- `AGENT-018` Tool Calling 完整链路：29 来源；
- `AGENT-019` Tool Lifecycle：10 来源；
- `AGENT-022` Structured Output / Validation：11 来源。

面试官常从：

```text
Tool Calling 是什么？
```

继续追：

```text
参数错了怎么办？
Tool 怎么注册？
Tool Schema 变了怎么办？
Tool Result 太大怎么办？
```

---

<a id="interview"></a>

## 13. 面试怎么答

### Q：怎样设计生产工具契约？

🎯 **30 秒回答**：

> Production Tool 不只是一个函数。它应该有稳定的 name/description、输入 Schema、Runtime Validation、side-effect 和 concurrency metadata、permission/cancellation 语义以及结构化 Result Contract。模型生成的参数永远是不可信输入，必须经过 parse、schema、semantic 和 policy 校验；错误可以结构化反馈给模型做有限 Repair，但不能无限重试。

### Q：为什么 Tool 不是普通 Python 函数？

🎯 **30 秒回答**：

> 函数只是执行实现。Agent 工具还要给模型一份用途与输入说明，并约定结果、错误和运行影响。程序端要绑定真实处理器、可信身份、校验与必要执行策略。模型只产生调用候选，不能因为函数签名匹配就获得执行权限。

### Q：结构校验、语义校验、权限校验有什么区别？

🎯 **30 秒回答**：

> 结构校验检查字段和类型；语义校验检查业务含义，例如ID存在、行号范围合理；权限校验检查可信用户是否能对该对象执行动作。一个字符串ID可以完全符合Schema，却指向别人的文件。三种检查串联，不是后面的安全章节取代前面的参数检查。

### Q：工具的可并发、只读、权限信息会全部进入上下文吗？

🎯 **30 秒回答**：

> 不会自动全部进入。模型请求通常携带工具名、说明、参数Schema以及该API支持的可选字段。处理器、权限回调、凭证和并发调度信息主要留在运行时。需要让模型知道的行为可有意写入说明，但模型看见提示与程序真实执行策略仍然分开。

### Q：模型参数出错后怎么处理？

🎯 **30 秒回答**：

> 解析或结构错误可以给脱敏且可行动的反馈，允许有限次重新生成参数。语义错误可能需要补输入或换合法目标；授权拒绝不能通过修改用户身份继续尝试。修复改变了已批准动作的目标或参数时，要重新判断批准，而不是复用旧确认。

### 🔍 继续追问与下一步

```text
Tool 多到几百个后怎么让模型选择？
Registry / Router 怎样设计？
Deferred Tool 是什么？
Tool 能否按需加载？
```

下一章进入 Tool Registry（注册表） / Router（路由器） / Progressive Discovery。

---

<a id="pitfalls"></a>

## 14. 高频易错点

⚠️ Schema valid = 安全——错；

⚠️ Tool Description 只是文案——错，它影响模型选择；

⚠️ Tool Result 统一返回字符串——会损失结构化状态；

⚠️ `read_only` 由模型判断——错，应由 Runtime 声明；

⚠️ 参数错就自动无限 Retry（重试）——容易形成 Loop。

⚠️ **Schema通过就能安全调用。** 还要检查目标含义与当前身份的权限。

⚠️ **把函数代码或数据库密码塞进工具描述。** 模型只需说明书；执行实现和凭证留在可信程序。

⚠️ **只读标注代表完全无风险。** 只读也可能泄露隐私；不可信标注不能当授权依据。

⚠️ **工具返回200就完成业务。** 还要判断结果是否满足契约及任务验收。

---

<a id="self-test"></a>

## 15. 本章自测

<details><summary>1. 自测：为什么 JSON Schema 不能替代 Permission？</summary>

因为 Schema 只保证输入形状合法，不能判断该用户是否有权执行、资源是否属于当前 tenant、动作是否高风险或路径是否越界。

</details>

<details><summary>2. ID类型正确但不存在，属于哪类问题？</summary>

主要属于语义或业务有效性问题，而非JSON结构错误。应返回“对象不存在/不可访问”等合适信息，并避免向无权用户泄露对象是否存在。

</details>

<details><summary>3. 模型给出的tenant_id可当可信身份吗？</summary>

不能。身份应来自认证后的应用上下文；模型字段只是输入。把它当可信身份会允许模型或提示注入选择别的租户。

</details>

<details><summary>4. 描述写“不修改原件”足够吗？</summary>

不足。运行时应接入确实只读的实现与资源权限。描述减少误选，权限控制即使模型误选也应阻止写入。

</details>

<details><summary>5. 修复参数和重试有什么差别？</summary>

修复生成不同、更合法的候选；重试通常再次尝试同一逻辑请求。前者不能悄悄扩大范围，后者还需判断先前是否已产生副作用。

</details>

<details><summary>6. 结果格式正确，但引用不支持结论，在哪里发现？</summary>

工具/格式层只能证明结构可读，任务验收或评测层才检查结论支持关系。不能把JSON Schema当内容真实性检查器。

</details>

<details><summary>7. 为何要同时在发现时和执行时过滤权限？</summary>

发现时减少无权能力暴露，执行时检查具体目标与最新身份状态。权限可能改变，参数也可能不同，所以执行前重查仍有必要。

</details>

---

[← 上一章](03-AgentLoopAndExecutionScopes.md) · [Agent 目录](../README.md) · [下一章 →](05-ToolRegistrationAndDiscovery.md)
