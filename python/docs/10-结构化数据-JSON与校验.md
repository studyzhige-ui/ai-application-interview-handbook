# 10. 结构化数据、JSON 与校验

[← 上一章：异常与文件](09-异常-文件-模块与导入.md) · [模块主页](../README.md) · [下一章：内存管理与 GIL →](11-内存管理-垃圾回收-GIL.md)

外部接口或模型返回了一段看起来像字典的文本，能不能马上拿它执行操作？不能把“长得像”“能解析”“满足字段要求”“业务允许”当成同一件事。

上一章解决失败怎样报告，本章解决输入经过哪些检查，才能进入后续程序。先学习 JSON 与 Python 对象的转换，再讲字段模型，最后连接到模型输出的处理闭环。

```text
外部文本／LLM 输出
→ Parse（解析）：文本能否解释成数据
→ Schema Validation（结构校验）：字段、类型、枚举和范围是否满足契约
→ Business Validation（业务校验）：当前状态与业务规则是否允许
→ Authorization / Approval（权限／审批）：当前主体是否可以执行
→ 接受、有限修复或明确拒绝
```

## 1. JSON 与 Python 对象：先区分两种表示形式

### 1.1 JSON 是数据格式，不是 Python 字典的另一种拼写

**JSON（JavaScript Object Notation）** 是一种文本数据交换格式。网络上传来的是文本或字节；程序通常需要先把它解析成 Python 对象，才能按键、按索引访问。

```python
import json                  # Python 标准库，不需要额外安装

raw_text = '{"name": "Tom", "age": 20}'  # 这是一个 str，里面的内容符合 JSON 格式
payload = json.loads(raw_text)            # loads 从文本解析，得到 Python 对象
print(type(payload).__name__)             # dict
print(payload["age"])                     # 20：现在才能按字典键访问

text = json.dumps(payload, ensure_ascii=False)  # dumps 把 Python 对象编码成 JSON 字符串
print(type(text).__name__)                       # str
```

`loads`／`dumps` 的 `s` 可以帮助记忆“字符串版本”；`load(file)`／`dump(obj, file)` 则面向文件对象。`ensure_ascii=False` 让非 ASCII 字符可以直接出现在结果文本中，不表示跳过 JSON 规则，也不等于文件编码设置。

| JSON 表示 | 解析到 Python 后 |
|---|---|
| object（对象） | dict |
| array（数组） | list |
| string（字符串） | str |
| number（数值） | 通常为 int／float |
| true／false（布尔值） | True／False |
| null（空值） | None |

JSON object 的键是字符串，Python dict 的键可以是其他可哈希对象。序列化还可能把 tuple 表示为 JSON array，再解析回来得到 list。**可以来回转换，不代表所有 Python 类型信息都会原样保留。**

### 1.2 能解析，只意味着通过了第一道门

```python
import json                  # 使用标准 JSON 解码器

data = json.loads('{"amount": "很多"}')  # 语法合法，可以解析成 dict
print(data["amount"])                    # 很多：值并不是可以直接计算的金额
```

解析成功不能证明必填字段存在、类型正确、操作在允许集合内，更不能证明当前用户有权限。一个 JSON 数组或单个字符串也可以是合法顶层 JSON；业务期待字典时仍要检查结构。

## 2. 第一层：处理格式与解析失败

### 2.1 捕获解析错误，而不是把所有失败变成服务器错误

```python
import json                  # 提供 loads 和 JSONDecodeError

raw_text = "{'name': 'Tom'}"  # 错误示例：Python 风格单引号，不是这里要求的标准 JSON 对象写法
try:                         # 在解析边界捕获格式错误
    data = json.loads(raw_text)  # 尝试解析
except json.JSONDecodeError as error:  # JSON 格式不被解析器接受
    print("invalid JSON", error.msg)  # 报告格式原因

correct = '{"name": "Tom"}'   # 正确：JSON 字符串与键使用双引号
print(json.loads(correct))    # {'name': 'Tom'}：这是 Python 对象的显示形式
```

其他常见问题包括尾逗号、缺括号、非法字面量、JSON 前后的解释文字，以及 Markdown 代码围栏。不要用“随便删几个字符”代替协议设计；上游输出约定与失败分类应明确。

### 2.2 标准库的默认兼容行为，也要知道边界

`json.loads` 默认还接受某些非严格 JSON 扩展，例如 `NaN`／`Infinity`，重复对象键也可能由后值覆盖。需要严格互操作契约时，应明确是否拒绝这些情况，而不是把“默认解码成功”当成符合所有外部标准的证明。

不可信输入还要在进入解析器前考虑长度、嵌套深度和执行资源限制。语法解析器不等于拒绝服务防护；它也不会替你决定允许模型消耗多少内存和时间。

## 3. 第二层：字段结构、类型与范围

### 3.1 从手动检查理解 Schema 的职责

**Schema（结构规则）** 描述数据应该有哪些字段、字段是什么类型、哪些值允许出现。

```python
def validate_order(data):            # 输入不能只因为注解写 dict 就假定一定是 dict
    if not isinstance(data, dict):   # 先检查顶层结构
        raise TypeError("输入必须是对象／字典")  # 不是对象时不能继续按字段检查
    if "order_id" not in data:       # 再检查必填字段
        raise ValueError("missing order_id")  # 缺少必需字段
    if not isinstance(data["order_id"], str):  # 检查该字段实际值的类型
        raise TypeError("order_id must be str")  # 拒绝错误类型

validate_order({"order_id": "A100"})  # 合法输入，通过检查
```

注意顺序：先知道它是不是映射，再问某个字段是否存在，最后检查字段值。`data: dict` 只是类型提示，不会自动完成第一步运行时检查。

### 3.2 字段多时，用数据模型集中表达契约

下面使用 **Pydantic v2**，它是第三方库。需要运行示例时，在对应 Python 环境安装：

```bash
python -m pip install "pydantic>=2,<3"
```

```python
from typing import Literal             # 描述只允许若干指定字面值
from pydantic import BaseModel, ConfigDict, Field  # 模型、配置和字段约束

class RefundRequest(BaseModel):        # 仅演示输入结构，不是可直接执行的退款系统
    model_config = ConfigDict(strict=True, extra="forbid", allow_inf_nan=False)  # 严格类型、拒绝多余字段与非有限数
    order_id: str                      # 必需的订单编号文本
    action: Literal["refund"]          # 只接受恰好这个动作值
    amount: float = Field(gt=0)        # gt 表示 greater than，要求大于 0

request = RefundRequest.model_validate({  # 运行时执行模型校验
    "order_id": "A100",                # 必需文本字段
    "action": "refund",                # 允许的字面值
    "amount": 99.5,                     # 正的有限数值；此处只讨论类型示例
})
print(request.order_id)                 # A100：现在通过模型属性访问
```

`BaseModel` 提供运行时验证；`Field` 补充字段约束；`model_validate` 检查输入并产生模型实例，不只是加注解。真实结算系统还需单独设计金额精度与业务规则，不能直接把这个结构示例当财务执行模型。

### 3.3 严格还是允许转换，要主动选

Pydantic 默认模式会对某些输入进行类型转换；严格模式用于限制这类宽松接受，但具体允许什么仍取决于字段类型和输入来源。例如整数到浮点数字段的接受规则，不能只凭 strict 一词猜测。

要区分三种约定：输入必须原本就是目标类型、允许某些明确转换、任何近似值都尽量接受。第三种会使脏数据容易进入系统。对模型工具参数等边界，应明确转换政策、多余字段政策与数值范围，并通过测试验证；不能假设用了一个库就自动采用最严格规则。

## 4. 三种数据描述工具，各自在哪个边界使用

### 4.1 TypedDict：描述字典结构，主要服务静态检查

```python
from typing import TypedDict          # 为字典定义字段类型描述

class UserPayload(TypedDict):         # 不是运行时输入验证器
    name: str                         # 期望 name 字段是字符串
    age: int                          # 期望 age 字段是整数

payload: UserPayload = {"name": "Tom", "age": 20}  # 注解供编辑器与检查器使用
print(isinstance(payload, dict))                    # True：运行时仍是普通 dict
```

将错误数据放进普通字典不会因为声明了 TypedDict 就自动抛出校验异常。它适合帮助 IDE（集成开发环境）和 Type Checker（类型检查器）理解已建立信任的数据流。

### 4.2 dataclass：方便表达内部领域对象

```python
from dataclasses import dataclass, field  # 自动生成常见类方法和字段默认工厂

@dataclass                               # 根据字段声明生成 __init__、__repr__ 等
class User:                              # 应用内部的数据对象
    name: str                            # 字段描述
    age: int                             # 字段描述
    tags: list[str] = field(default_factory=list)  # 每个实例创建独立列表

user = User("Tom", 20)                  # 创建实例
print(user.age)                          # 20
```

`default_factory=list` 沿用了第 03、08 章的原则：需要独立可变状态，就每次创建一个新对象。标准 dataclass 不会仅凭注解完成严格的外部数据校验；需要验证时，应自己实现或在进入领域对象之前完成。

### 4.3 Pydantic：在不可信输入边界建立运行时约束

| 工具 | 主要问题 | 不自动提供的能力 |
|---|---|---|
| TypedDict | 字典字段如何供静态检查理解 | 运行时拒绝脏数据 |
| dataclass | 内部数据对象怎样减少重复样板代码 | 完整输入 Schema 校验 |
| Pydantic | 外部输入怎样在运行时验证并形成模型 | 业务授权、事务正确性、所有安全边界 |

重点不是哪个工具“高级”，而是数据是否经过 **Trust Boundary（信任边界）**：外部 API、配置文件、模型输出不能只因为看起来像本地对象，就享有内部可信数据的地位。

## 5. 第三层：类型正确仍不等于业务允许

假设订单号是字符串、动作是 refund、金额也是正数，Schema 都通过。但订单可能不属于当前用户，金额可能超过可退余额，订单状态也可能不允许操作。

```text
Syntax Validation（语法检查）   → 能否解析成数据？
Schema Validation（结构检查）  → 数据是否符合字段契约？
Business Validation（业务检查）→ 当前状态与业务限制是否满足？
Authorization（授权检查）       → 当前主体能否对这个资源执行该动作？
```

同一个范围规则可以按系统设计放在模型约束或业务层，但职责要明确。依赖数据库现状、用户身份、资源归属或审批状态的判断，不能仅靠静态 Schema 替代。

错误流程：

```text
LLM 输出 → json.loads → 直接执行支付／退款／删除
```

正确的职责链：

```text
LLM 输出 → 解析 → 结构校验 → 业务语义检查 → 权限／审批
→ 幂等边界 → 执行动作 → 保存结果与必要审计信息
```

**Idempotency（幂等）** 是避免同一业务请求因重试而重复产生效果的一类约束。权限、审批、沙箱与工具执行的完整设计属于 Agent 模块；Python 这里先建立“不可信文本不能直接变成可信指令”的边界。

## 6. 修复、重试、拒绝：由错误类别决定

### 6.1 哪些可能修复，哪些不能靠模型重试绕过

**Repair（修复）** 可以针对允许修复的格式与结构问题，例如输出围栏、缺失可补充字段、枚举值格式不符合约定；不能凭空伪造用户身份、订单编号或其他业务事实。**Retry（重试）** 应带着明确错误反馈和预算重新请求，而不是无条件再来一次。

无权限、业务状态禁止、超过业务上限、请求内在矛盾通常需要 **Reject（拒绝）** 或清晰的替代流程。让模型反复改写输入，不能把原本不允许的操作变成允许。

```text
第 1 次：解析失败 → 提供受控的格式反馈
第 2 次：结构仍不合约 → 在预算内再次尝试
达到上限：停止／返回明确失败／进入替代流程
```

总次数、总时间和成本都要有边界。不要把模型能够再次生成文本误当成系统能够无限重试。

### 6.2 严格程度与可用性的取舍

过于宽松，错误可能在更深的执行位置才暴露；过于严格，非关键格式差异也可能带来大量拒绝。可行起点是：核心字段严格、可选字段语义明确、转换有限、修复有上限、拒绝原因可定位。

回归分析需要知道失败阶段、模型版本、错误类型以及足够的输入上下文，但原始输出可能含隐私、密钥或业务数据。**按权限、脱敏、截断和保留期限记录必要证据，不等于无条件全量留存。**

## 7. 不可信文本不要用 eval 执行

`eval` 会求值 Python 表达式，输入不是纯数据边界。错误设计是 `obj = eval(model_output)`；正确方式是约定标准数据格式，用对应解析器，再做明确校验。

`ast.literal_eval` 只处理有限的 Python 字面量结构，不像 eval 那样提供一般表达式执行能力，但恶意的巨大或深度嵌套输入仍可能耗尽内存或栈。它不能被称为“不可信输入无条件安全解析器”。历史接口必须接收 Python 字面量时，也要限制来源与资源；新接口应优先采用清晰的数据协议。

## 8. 完整例子：把模型文本变成可用的搜索计划

下面是一个可独立运行的 Pydantic v2 示例。它区分三类异常，不包含真实网络调用，也不执行高风险工具。

```python
import json                               # 标准库 JSON 解码
from pydantic import BaseModel, ConfigDict, Field, ValidationError  # 结构验证工具

class PlanParseError(ValueError):          # 表示文本不能按约定解析
    pass                                  # 只用异常类型表达类别

class PlanSchemaError(ValueError):         # 表示结构不符合约定
    pass

class PlanBusinessError(ValueError):       # 表示业务规则拒绝
    pass

class SearchPlan(BaseModel):               # 定义搜索计划的字段
    model_config = ConfigDict(strict=True, extra="forbid")  # 不接受意外字段和宽松整数字符串转换
    query: str = Field(min_length=1)       # 查询文本至少有一个字符
    top_k: int                            # 检索数量必须是整数，不接受 bool 代替


def reject_constant(value):               # json 遇到 NaN／Infinity 等常量时调用
    raise PlanParseError(f"不允许非有限常量：{value}")  # 拒绝默认解码器允许的这类扩展


def parse_plan(raw: str) -> SearchPlan:    # 返回通过本函数各层检查的模型对象
    if not isinstance(raw, str):           # 注解不能替代运行时检查
        raise PlanParseError("输入必须是文本")  # 明确解析入口类型
    if len(raw) > 10000:                   # 示例采用字符数上限；服务边界还需限制请求字节与其他资源
        raise PlanParseError("输入超过示例长度限制")  # 防止无界接受文本
    try:                                  # 第一层：解析
        payload = json.loads(raw, parse_constant=reject_constant)  # 解码为 Python 对象
    except json.JSONDecodeError as error: # 标准解析失败
        raise PlanParseError("model output is not valid JSON") from error  # 保留原因
    try:                                  # 第二层：结构校验
        plan = SearchPlan.model_validate(payload)  # 不是字典或字段错误都会被拒绝
    except ValidationError as error:      # Pydantic 的结构错误
        raise PlanSchemaError("model output violates schema") from error  # 与解析失败区分
    if not plan.query.strip():            # 第三层：本例不接受全空白查询
        raise PlanBusinessError("query 不能只有空白")  # 结构是文本仍不代表有有效搜索含义
    if not 1 <= plan.top_k <= 50:          # 本例业务检索上限
        raise PlanBusinessError("top_k is outside business limit")  # 不让非法数量进入下游
    return plan                           # 全部通过才返回

plan = parse_plan('{"query": "Python 引用", "top_k": 5}')  # 合法示例
print(plan.query, plan.top_k)              # Python 引用 5
```

本例没有实现对所有 JSON 重复键、嵌套深度和服务级请求资源的完整防护；这些必须根据真实入口另行设置，不能把示例长度检查当成完整防护方案。它展示的是**不同检查层分别负责什么、失败怎样分类**，不是可直接替代业务授权的万能解析函数。

本章依据：[json 标准库及兼容边界](https://docs.python.org/3.14/library/json.html)、[typing.TypedDict](https://docs.python.org/3.14/library/typing.html#typing.TypedDict)、[dataclasses](https://docs.python.org/3.14/library/dataclasses.html)、[Pydantic 严格模式](https://docs.pydantic.dev/latest/concepts/strict_mode/)、[ast.literal_eval 的限制](https://docs.python.org/3.14/library/ast.html#ast.literal_eval)。

---

## 9. 🎯 面试怎么回答

> Python 处理 LLM Structured Output 时，我会先把 parse、schema validation 和业务校验分层。`json.loads` 只能证明 JSON 语法合法，不能证明字段类型和业务约束正确。外部不可信数据进入系统时可以用 Pydantic 等做运行时 schema validation，再检查业务 invariant、权限和高风险动作边界。解析或 schema 错误可以有限 Repair / Retry，但权限或业务拒绝不应该靠模型重试绕过。也不会对模型输出直接使用 `eval`。

表述边界：默认 JSON 解码器有上文说明的兼容扩展；严格格式要求应显式约束。Invariant 指业务必须保持的条件，并不只是一种字段类型。

---

## 10. ⚠️ 易错点

- `json.loads` 成功 ≠ 数据可信；
  正确流程：解析后还需结构、业务与授权检查，必要时限制格式扩展。
- Type Hint ≠ Runtime Validation；
  正确理解：类型提示服务静态工具，运行时验证需要实际执行检查代码。
- `TypedDict` 不会自动在运行时拒绝脏数据；
  正确选择：外部输入使用明确的运行时校验边界。
- Schema 正确 ≠ 有业务权限；
  正确做法：结合当前身份、资源状态和审批规则检查是否允许执行。
- 不可信模型输出不要直接 `eval`；
  正确做法：解析数据，不执行模型给出的表达式；其他解析器也要控制资源边界。
- Repair 要有次数上限；
  正确做法：同时管理次数、时间与成本，并明确拒绝／替代结果。
- Structured Output 失败要记录原始输出、模型版本和错误类型，方便回归分析。
  正确边界：原始输出按权限、脱敏、截断和保留期限处理，不能无条件全量写日志。

---

## 11. 🔍 继续追问

- `TypedDict`、`dataclass`、Pydantic 的职责有什么不同？
- JSON 可解析但字段缺失时应该在哪一层处理？
- Tool Arguments 校验失败应该让模型重试还是直接失败？
- 为什么 Schema Validation 不能代替 Authorization？

---

## 12. 本章自测

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
