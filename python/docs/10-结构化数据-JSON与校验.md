# 10. 结构化数据、JSON 与校验

这章是 Python v1 整改时新增的唯一独立知识块。

原因不是“面经出现了一道新题就加一章”，而是 **AI Application 里的 Structured Output 已经形成独立工程闭环**：

```text
LLM / External API
→ text / JSON-like output
→ parse
→ schema validate
→ business validate
→ accept / repair / reject
→ typed object
```

它既不是单纯 FastAPI/Pydantic 用法，也不是 Agent Tool Runtime 的全部内容，而是 Python 应用层必须具备的“把不可信文本变成可信数据”能力。

---

## 1. 先讲人话：字符串能解析，不代表数据可信

LLM 返回：

```json
{
  "user_id": 123,
  "action": "refund",
  "amount": 99.5
}
```

第一步只是确认它是不是合法 JSON。

```python
import json

data = json.loads(raw_text)
```

这只能证明**语法可解析**，不能证明：

- `user_id` 一定存在；
- `amount` 一定是数字；
- `action` 一定属于允许集合；
- `amount` 一定非负；
- 当前用户真的有退款权限。

所以要把“解析”和“校验”分开。

---

## 2. JSON 的基本边界

Python 标准库：

```python
import json
```

字符串 → Python 对象：

```python
payload = json.loads('{"name": "Tom", "age": 20}')
```

Python 对象 → JSON 字符串：

```python
text = json.dumps(payload, ensure_ascii=False)
```

常见映射：

| JSON | Python |
|---|---|
| object | `dict` |
| array | `list` |
| string | `str` |
| number | `int` / `float` |
| true / false | `True` / `False` |
| null | `None` |

⚠️ JSON object 的 key 是字符串；Python dict 的 key 可以是其它可哈希类型。两者不能完全等同。

---

## 3. Parse Failure：最先处理语法错误

```python
import json

try:
    data = json.loads(raw_text)
except json.JSONDecodeError as e:
    print("invalid JSON", e)
```

典型失败：

```text
单引号
尾逗号
缺右括号
模型在 JSON 前后加解释文字
Markdown code fence
字段值不是合法 JSON literal
```

生产代码不要简单：

```python
json.loads(raw_text)
```

然后把所有异常都变成 500。

更合理的是把错误归类为：

```text
parse error
schema error
business validation error
permission error
```

这样上层才知道应该 Repair、让模型重试、拒绝请求还是直接失败。

---

## 4. Schema Validation：字段结构要明确

最简单可以手动校验：

```python
def validate_order(data: dict) -> None:
    if "order_id" not in data:
        raise ValueError("missing order_id")
    if not isinstance(data["order_id"], str):
        raise TypeError("order_id must be str")
```

但字段一多，手写判断会越来越难维护。

Python AI 项目常使用数据模型库，例如 Pydantic。这里先理解思想，FastAPI 模块再讲框架集成。

```python
from pydantic import BaseModel, Field
from typing import Literal

class RefundRequest(BaseModel):
    order_id: str
    action: Literal["refund"]
    amount: float = Field(gt=0)
```

```python
obj = RefundRequest.model_validate(data)
```

这一步把动态 `dict` 转成带约束的结构化对象。

---

## 5. 类型正确仍不等于业务正确

假设：

```json
{
  "order_id": "A100",
  "action": "refund",
  "amount": 999999
}
```

Schema 可能完全合法，但业务仍可能不允许。

所以至少分三层：

```text
Syntax Validation
→ JSON 能不能解析

Schema Validation
→ 字段、类型、枚举、范围是否正确

Business / Authorization Validation
→ 当前状态、权限、业务规则是否允许
```

这三个层次不能混成一句“做一下 JSON 校验”。

---

## 6. TypedDict、dataclass、Pydantic 各适合什么

### TypedDict

用于静态类型描述，运行时不会自动替你验证输入。

```python
from typing import TypedDict

class UserPayload(TypedDict):
    name: str
    age: int
```

适合：

- IDE / type checker；
- 已经可信的数据流；
- 不需要运行时校验。

### dataclass

```python
from dataclasses import dataclass

@dataclass
class User:
    name: str
    age: int
```

适合应用内部领域对象，但标准 `dataclass` 本身不会自动把外部脏数据做完整 schema validation。

### Pydantic

更适合 API / LLM / Config 等不可信外部输入进入 Python 系统的边界。

> 核心不是“Pydantic 更高级”，而是**数据是不是来自 trust boundary**。

---

## 7. Structured Output 最危险的误区：能 parse 就执行 Tool

错误流程：

```text
LLM output
→ json.loads
→ execute payment/refund/delete
```

更合理：

```text
LLM output
→ parse
→ schema validate
→ semantic/business validate
→ permission / approval
→ idempotency boundary
→ execute
```

Tool Permission、Approval、Sandbox 属于 Agent Harness；这里要掌握的是 Python 侧**不要把模型文本直接当可信程序输入**。

---

## 8. Repair、Retry 还是 Reject？

不是所有 JSON 错误都应该无限让模型重试。

### 可以 Repair / Retry

例如：

```text
少一个必填字段
枚举拼写错误
纯格式问题
```

### 应该 Reject

例如：

```text
用户无权限
业务状态不允许
金额超业务上限
请求本身矛盾
```

### 要限制次数

```text
attempt 1 → parse failed
attempt 2 → schema failed
attempt 3 → stop / fallback
```

否则会形成无限 Repair Loop。

---

## 9. 不要用危险解析方式处理“不可信 Python 文本”

不要因为模型输出看起来像 Python 字典就写：

```python
obj = eval(model_output)
```

`eval` 会执行表达式，不适合处理不可信输入。

如果历史接口返回的是 Python literal 风格文本，`ast.literal_eval` 的风险远低于 `eval`，但 AI API 设计仍应优先要求标准 JSON / Structured Output，而不是依赖 Python literal。

---

## 10. AI Application 中的完整例子

```python
import json
from pydantic import BaseModel, ValidationError

class SearchPlan(BaseModel):
    query: str
    top_k: int


def parse_plan(raw: str) -> SearchPlan:
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as e:
        raise ValueError("model output is not valid JSON") from e

    try:
        plan = SearchPlan.model_validate(payload)
    except ValidationError as e:
        raise ValueError("model output violates schema") from e

    if not 1 <= plan.top_k <= 50:
        raise ValueError("top_k is outside business limit")

    return plan
```

这里清楚地区分：

```text
JSON syntax
Schema
Business invariant
```

---

## 11. Failure / Trade-off

### 太宽松

优点：模型更容易输出成功。

问题：脏数据进入后续 Runtime，失败位置更难定位。

### 太严格

优点：契约清楚。

问题：模型轻微格式漂移就大量失败。

工程上常见做法：

```text
严格核心字段
+ 可控 optional 字段
+ 有限 Repair
+ 明确 Reject
+ Trace 原始输出和 validation error
```

---

## 12. 🎯 面试怎么回答

> Python 处理 LLM Structured Output 时，我会先把 parse、schema validation 和业务校验分层。`json.loads` 只能证明 JSON 语法合法，不能证明字段类型和业务约束正确。外部不可信数据进入系统时可以用 Pydantic 等做运行时 schema validation，再检查业务 invariant、权限和高风险动作边界。解析或 schema 错误可以有限 Repair / Retry，但权限或业务拒绝不应该靠模型重试绕过。也不会对模型输出直接使用 `eval`。

---

## 13. ⚠️ 易错点

- `json.loads` 成功 ≠ 数据可信；
- Type Hint ≠ Runtime Validation；
- `TypedDict` 不会自动在运行时拒绝脏数据；
- Schema 正确 ≠ 有业务权限；
- 不可信模型输出不要直接 `eval`；
- Repair 要有次数上限；
- Structured Output 失败要记录原始输出、模型版本和错误类型，方便回归分析。

---

## 14. 🔍 继续追问

- `TypedDict`、`dataclass`、Pydantic 的职责有什么不同？
- JSON 可解析但字段缺失时应该在哪一层处理？
- Tool Arguments 校验失败应该让模型重试还是直接失败？
- 为什么 Schema Validation 不能代替 Authorization？

---

## 15. 本章自测

<details>
<summary>1. `json.loads()` 成功后为什么还不能直接执行退款 Tool？</summary>

因为它只说明 JSON 语法合法。还需要检查字段类型、业务约束、权限、订单状态以及高风险操作审批等边界。

</details>

<details>
<summary>2. `TypedDict` 能不能替代运行时 Schema Validation？</summary>

不能。`TypedDict` 主要服务静态类型检查，运行时不会自动拒绝外部输入中的错误字段和类型。

</details>

<details>
<summary>3. 为什么不能对 LLM 输出直接使用 `eval()`？</summary>

因为 `eval()` 会执行表达式；模型输出属于不可信输入，直接执行可能造成严重安全问题。应优先使用标准 JSON 加显式 Schema Validation。

</details>

下一章：[11. 内存管理、垃圾回收与 GIL](11-内存管理-垃圾回收-GIL.md)
