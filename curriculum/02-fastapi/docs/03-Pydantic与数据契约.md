# 03｜数据契约：校验输入、限制输出、解释错误

[← 上一章](02-Routing与APIContract.md) · [模块主页](../README.md) · [下一章 →](04-Dependency与Middleware.md)

用户说要重复一段文字两次，却把次数写成 `-2`；服务查询到一条笔记，却差点把内部诊断字段也返回给用户。两种问题发生在相反方向：一个是外部数据进入系统，一个是内部数据离开系统。

**数据契约（Contract）就是事先约定输入和输出的形状及规则。** 本章先让一个具体请求经过解析、校验、处理和输出，再区分结构错误、业务拒绝和程序错误。

## 1. 三个关卡不要混成一个“校验”

| 关卡 | 在问什么 | 例子 |
|---|---|---|
| 解析 | 这段字节能按声明的格式读懂吗？ | JSON 少了右括号 |
| 结构和字段校验 | 读出来的值满足类型、必填和范围吗？ | 次数小于 1 |
| 业务及权限判断 | 对这个用户和资源，这次动作允许吗？ | 访问了别人的笔记 |

Pydantic 主要处理第二类规则，也可表达适合本地完成的字段关联检查。资源是否存在、用户是否拥有它，通常需要额外的可信信息，不能仅靠“JSON 可以解析”推断。

### 必填与可空：先把两条规则分开

**必填（required）** 问“这个字段能否省略”，**可空（nullable）** 问“提供了字段时，值能否是 JSON null”。null 进入 Python 后是 None；缺字段则是没有这条输入，二者不能混为同一个状态。

| Pydantic v2 字段声明 | 能省略吗 | 接受 null 吗 | 省略后的值 |
|---|---|---|---|
| `name: str` | 否 | 否 | 没有默认值，拒绝 |
| `name: str | None` | 否 | 是 | 没有默认值，拒绝 |
| `name: str = "匿名"` | 是 | 否 | `"匿名"` |
| `name: str | None = None` | 是 | 是 | None |

因此 `{"name": null}` 可满足第二行，`{}` 却不能；第三行的默认值也不会把显式 null 自动改成匿名。`Optional[str]` 等同 `str | None`，不自动赋默认值。[Pydantic 字段规则](https://docs.pydantic.dev/latest/concepts/fields/)

路径参数必须出现在路径里；查询参数通常是文本，`?name=null` 是四个字符，不是 JSON null。这张四格表首先讨论 JSON 模型字段，不能把传输形式也抹平。


## 2. 定义输入：先明确哪些值允许进来

下面是完整 `main.py`。输入包含 `text` 和 `repeat`，输出只暴露 `result`。

```python
# example: contract_app
from fastapi import FastAPI
from pydantic import BaseModel, ConfigDict, Field, field_validator

app = FastAPI()

class PreviewInput(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str = Field(min_length=1, max_length=200)
    repeat: int = Field(default=1, ge=1, le=3)

    @field_validator("text")
    @classmethod
    def reject_blank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("文字不能全部为空白")
        return value

class PreviewOutput(BaseModel):
    result: str

@app.post("/preview", response_model=PreviewOutput)
def preview(body: PreviewInput):
    return {"result": body.text * body.repeat, "internal_debug": "do-not-expose"}
```

先认识每个声明的作用，再看运行结果：

- `BaseModel` 把类中的字段声明变成可执行的数据规则。
- `Field` 为字段添加长度、范围或默认值。本例的长度先按原始字符串检查；随后 `strip()` 去掉首尾空白，再拒绝全空白内容。
- `@field_validator("text")` 将下面的函数用于 text 校验；默认在基础字段校验后执行。`@classmethod` 表示它是类方法，第一个参数 cls 接收模型类；value 才是待检查的字段值。正常时返回值，拒绝时抛出错误。
- `extra="forbid"` 拒绝没有声明的字段。本例选择尽早暴露拼写错误，不代表所有接口必须使用同一策略。

这些动作由框架接收请求时触发，不是让客户端自行承诺“我会按类型发送”。[请求模型](https://fastapi.tiangolo.com/tutorial/body/) · [Pydantic 字段校验](https://docs.pydantic.dev/latest/concepts/validators/)

### 2.1 从具体请求观察结果

在 `/docs` 调用 `/preview`：

| JSON 请求体 | 预期状态 | 结果或失败原因 |
|---|---:|---|
| `{"text":"ha","repeat":2}` | 200 | `{"result":"haha"}` |
| `{"text":" ha "}` | 200 | 默认重复一次，结果为 `ha` |
| `{"text":"ha","repeat":0}` | 422 | 次数小于下限 |
| `{"text":"   "}` | 422 | 空白校验失败 |
| `{"repeat":2}` | 422 | 缺少 text |
| `{"text":"ha","repeet":2}` | 422 | 未声明的字段，不会悄悄使用默认次数 |

故意发错请求很有价值。它让你看到“规则写在哪里”和“错误在哪里被发现”是一一对应的。

### 2.2 类型转换与严格校验是不同策略

默认宽松规则下，某些兼容输入会被转换，例如本例的 `"repeat":"2"` 可以得到整数 2。若业务要求 JSON 中必须是整数而不能是数字字符串，可把该字段改为 `Field(default=1, ge=1, le=3, strict=True)`。

是否允许转换取决于接口约定。JSON 可以区分数字 `2` 和字符串 `"2"`；URL 中的路径、查询参数原本是文字，不能直接照搬同一套严格类型策略。[严格模式](https://docs.pydantic.dev/latest/concepts/strict_mode/)

### 2.3 每个字段都合法，组合起来仍可能不合法

假设接口让用户选择材料的起止页。`start_page=5` 和 `end_page=2` 都是正整数，但“从第 5 页读到第 2 页”不满足本接口的顺序约定。只检查每个字段的下限，不会发现这个错误。

可以在单个字段检查完成后，再检查这两个字段之间的关系：

```python
# example: page_range_model
from pydantic import BaseModel, Field, model_validator

class PageRange(BaseModel):
    start_page: int = Field(ge=1)
    end_page: int = Field(ge=1)

    @model_validator(mode="after")
    def check_order(self):
        if self.start_page > self.end_page:
            raise ValueError("起始页不能晚于结束页")
        return self

pages = PageRange(start_page=2, end_page=5)
print(pages.start_page, pages.end_page)  # 2 5
```

`mode="after"` 让这个方法在模型的基础校验之后执行；`self` 是已经取得字段值的对象。关系正确时返回这个对象，关系不正确时抛出错误。[模型校验器](https://docs.pydantic.dev/latest/concepts/validators/#model-validators)用于这种跨字段检查，不需要为此学习全部校验器变体。

| 起止页 | 结果 | 拒绝发生在哪里 |
|---|---|---|
| 2、5 | 允许 | 两个字段和顺序都符合要求 |
| 2、2 | 允许 | 本例允许只读一页 |
| 5、2 | 拒绝 | 模型校验器发现顺序颠倒 |
| 0、5 | 拒绝 | 字段校验发现页码小于 1 |

把这个模型作为请求体时，框架会在正常处理函数执行前拒绝不满足模型规则的输入。不过，“这份材料是否真的有第 5 页”“当前用户是否有权读取它”仍需要服务查询并核对。**输入自身能判断的关系，与依赖外部事实的业务条件，应分开处理。**

> ⚠️ 给模型或客户端的字段说明不能代替服务端执行校验。跨字段规则也不一定会完整出现在自动生成的 JSON Schema 中；重要约束要写入接口说明，并测试错误响应是否可理解。

### 2.4 嵌套列表与别名：字段形状可以逐层描述

```python
# example: nested_contract
from pydantic import BaseModel, Field

class Note(BaseModel):
    text: str = Field(min_length=1)

class Notebook(BaseModel):
    owner_id: str = Field(alias="ownerId")
    notes: list[Note] = Field(default_factory=list)

book = Notebook.model_validate({"ownerId": "u1", "notes": [{"text": "第一条"}]})
print(book.notes[0].text)                  # 第一条
print(book.model_dump(by_alias=True))     # {'ownerId': 'u1', 'notes': [{'text': '第一条'}]}
```

Python 内部用 `owner_id`，这个模型的外部输入使用别名 `ownerId`；输出是否用别名要看序列化设置，这里显式写 `by_alias=True`。嵌套校验会逐项进入 Note：例如 `notes[0]` 缺少 text，错误位置能指出 notes、0、text，而不只是说“整个对象坏了”。`default_factory=list` 在缺省时为每个实例创建列表；不等于传入 null 也自动变成空列表。

别名用于连接命名约定，不能代替字段权限或业务迁移策略。需要同时接受内部名和外部名时，应明确配置并测试，不能默认所有拼写都会被接受。[嵌套模型](https://fastapi.tiangolo.com/tutorial/body-nested-models/) · [字段别名](https://docs.pydantic.dev/latest/concepts/alias/)

### 2.5 PATCH：没有提供，和明确清空，是不同更新

假设现有记录 `{"description": "原说明"}`。本接口约定：省略 description 表示保留，显式 null 表示清空，字符串表示替换。

```python
# example: patch_contract
from pydantic import BaseModel

class NotePatch(BaseModel):
    description: str | None = None

stored = {"description": "原说明"}
missing = NotePatch.model_validate({})
clear = NotePatch.model_validate({"description": None})
print(missing.description, clear.description)       # None None：单看属性分不出来
print(missing.model_dump(exclude_unset=True))       # {}
print(clear.model_dump(exclude_unset=True))         # {'description': None}
print({**stored, **missing.model_dump(exclude_unset=True)})  # 保留原说明
print({**stored, **clear.model_dump(exclude_unset=True)})    # 清空为 None
```

模型记录哪些字段实际被提供，`exclude_unset=True` 只取这些字段。`exclude_none=True` 会把明确清空也删掉，`exclude_defaults=True` 会按值是否等于默认值过滤，都不是这里的同一契约。合并后仍要检查完整记录的关联规则和修改权限；`model_copy(update=...)` 也不自动重新校验更新数据。这里解释更新语义，不把字典合并当事务或并发控制。[部分更新](https://fastapi.tiangolo.com/tutorial/body-updates/)


## 3. JSON Content-Type：格式不是靠服务器猜的

发送 JSON 时要带 `Content-Type: application/json`。FastAPI 从 0.132.0 起默认启用严格 Content-Type 检查：缺少相应类型声明的请求，不再默认当作 JSON 解析。[严格 Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/)

使用 HTTPX 或 TestClient 的 `json={...}` 会同时完成 JSON 编码和相应请求头设置。手写 `content=` 只提供正文，不应假设它会替你选择正确类型。

> ⚠️ 在本课程版本与请求模型下，缺少 JSON Content-Type 的这个请求预期被拒绝为 422。先修正客户端的请求头，不要为绕过错误而关闭应用级检查。

## 4. 输出模型：内部有这个字段，不代表外部该看见

本例函数返回了 `internal_debug`，但客户端应只收到 `result`，因为 `response_model=PreviewOutput` 限定了输出字段。

这三种模型不要默认共用：

| 模型 | 服务谁 | 典型内容 |
|---|---|---|
| 请求模型 | 客户端提交 | text、repeat |
| 内部模型或数据库对象 | 业务处理、存储 | 用户归属、诊断信息、内部状态 |
| 响应模型 | 客户端读取 | 允许公开的 result |

FastAPI 会对普通返回值进行响应校验和序列化。若返回结果缺少必要字段，这是服务端没有履行承诺，属于程序错误；不应伪装成用户输入错误。[响应模型](https://fastapi.tiangolo.com/tutorial/response-model/)

返回类型注解也能声明响应模型。如果同时指定返回注解与 `response_model`，框架以 `response_model` 作为响应处理配置。直接返回 `Response`、`JSONResponse` 对象，则是你自行构造响应的路径，不能再假设声明模型会替这个对象过滤字段。

> ⚠️ 输出模型是减少意外泄露的一道边界，不是权限系统。模型本身设计错了、直接返回了未经处理的响应对象，仍可能泄露数据。

## 5. 脱离 HTTP，也能观察 Pydantic 的两个方向

下面是独立 Python 实验，不需要启动服务：

```python
# example: pydantic_roundtrip
from pydantic import BaseModel

class Count(BaseModel):
    value: int

obj = Count.model_validate({"value": "2"})
print(obj.value, type(obj.value))  # 2 <class 'int'>
print(obj.model_dump())          # {'value': 2}，得到 Python 字典
print(obj.model_dump_json())     # {"value":2}，得到 JSON 字符串
```

`model_validate` 是从外部值到模型，`model_dump` 是从模型到 Python 数据。包含日期等对象时，`model_dump(mode="json")` 会生成适合 JSON 的值；不要把 Python 字典、JSON 字符串和已经发出的 HTTP 响应当成同一种东西。

### 5.1 Python 值到 JSON 值，还需要序列化规则

JSON 没有 datetime 或 Decimal 类型。模型的 Python 模式可以保留这些对象；JSON 模式则按类型的序列化规则产生字符串、数字、列表等可编码值。

```python
# example: serialization_contract
from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel

class Quote(BaseModel):
    created_at: datetime
    amount: Decimal

quote = Quote(created_at=datetime(2026, 1, 1, tzinfo=timezone.utc), amount=Decimal("1.20"))
print(type(quote.model_dump()["amount"]).__name__)    # Decimal
print(quote.model_dump(mode="json"))
# {'created_at': '2026-01-01T00:00:00Z', 'amount': '1.20'}
```

Pydantic 的这个 JSON 模式将 Decimal 编码成文本以保留十进制表示；客户端必须按契约读取，不能猜它必是 JSON number。若改用别的编码器，规则可能不同。直接给 JSONResponse 一个含 datetime 的普通字典，不会自动执行上面模型的规则；应先显式转换。[Pydantic 序列化](https://docs.pydantic.dev/latest/concepts/serialization/)

### 5.2 同一份内部数据，两条返回路径

```python
# example: response_paths
from fastapi import FastAPI, Response
from fastapi.responses import JSONResponse
from pydantic import BaseModel

app = FastAPI()
class PublicNote(BaseModel):
    text: str

INTERNAL = {"text": "第一条", "internal_debug": "demo-only"}

@app.get("/model", response_model=PublicNote)
def model_path(response: Response):
    response.headers["X-Format"] = "public-note"
    response.set_cookie("theme", "light", httponly=True, samesite="lax")
    return INTERNAL

@app.get("/direct", response_model=PublicNote)
def direct_path():
    public = PublicNote.model_validate(INTERNAL)  # 先显式限定字段
    return JSONResponse(content=public.model_dump(mode="json"))

@app.delete("/theme", status_code=204)
def clear_theme():
    response = Response(status_code=204)
    response.delete_cookie("theme", path="/")
    return response
```

`/model` 的普通数据返回经过 response_model，只留下 text；注入的临时 Response 提供头和 Cookie。`/direct` 已自行构造响应，框架不会再替它过滤 INTERNAL；所以这里先构造 PublicNote，再转成 JSON 兼容值。若直接写 `JSONResponse(content=INTERNAL)`，内部字段就会被发出去。

Cookie 通过 `Set-Cookie` 交给浏览器；后续是否携带取决于 Domain、Path、Secure、SameSite 等范围。删除 Cookie 也需要匹配原有范围。本例 theme 只是本地偏好示意，不建立登录会话；认证 Cookie 的安全策略见第 09 章。

| 返回方式 | 谁负责表示内容 | 常见场景 |
|---|---|---|
| 普通对象加 response_model | 模型验证、过滤和序列化 | 结构化 API |
| JSONResponse / Response | 调用方准备好内容、状态、头 | 明确控制完整响应 |
| PlainTextResponse / HTMLResponse | 按指定媒体类型返回文本 | 文本或可信 HTML；不会自动替你处理所有 HTML 注入 |
| FileResponse | 从受控路径交付文件 | 文件下载；不把任意用户路径直接传入 |
| StreamingResponse | 逐项产生响应体 | 第 07 章的流式交付 |

路由的 `status_code=201` 决定普通返回路径的默认状态，也用于文档；`responses={...}` 可以补充 OpenAPI，但不会自动实现这些分支。直接返回 Response 时，其实际状态与媒体类型由响应对象决定。声明了 404 文档，不等于代码已经会返回 404。[响应与 Cookie](https://fastapi.tiangolo.com/advanced/response-cookies/) · [自定义响应](https://fastapi.tiangolo.com/advanced/custom-response/)


## 6. 业务错误怎样成为稳定响应

不存在的笔记不是 Python 程序崩溃。让业务函数用自己的异常表达问题，再在 Web 边界映射到 HTTP，是一种可测试的分工。

```python
# example: domain_error_app
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class NoteMissing(Exception):
    pass

def load_note(note_id: int) -> str:
    if note_id != 1:
        raise NoteMissing()
    return "第一条笔记"

app = FastAPI()

@app.exception_handler(NoteMissing)
async def missing_handler(request: Request, exc: NoteMissing):
    return JSONResponse(status_code=404, content={"error": {"code": "NOTE_NOT_FOUND"}})

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    return {"text": load_note(note_id)}
```

`GET /notes/1` 成功，`GET /notes/2` 返回 404 和稳定错误码。普通 Python 测试还可以直接调用 `load_note`，不必依赖 HTTP。

框架输入错误由 `RequestValidationError` 表达；可以注册处理器调整对外结构，但不要原样返回所有异常细节或整个请求体。内部日志保留必要诊断，外部错误尽量稳定且不含秘密。[错误处理](https://fastapi.tiangolo.com/tutorial/handling-errors/)

## 7. 用失败类型决定排查位置

| 现象 | 先检查什么 |
|---|---|
| JSON 不能解析、字段缺失、类型不符 | 客户端载荷和模型声明 |
| 合法请求被业务拒绝 | 资源状态、用户权限、业务条件 |
| 下游响应格式错误 | 供应商协议适配与下游契约 |
| 响应模型校验失败 | 本服务的返回值和输出声明 |

模型生成的结构化结果也是外部输入。它还要经过解析、结构、业务和权限检查，不能因为来源是模型就直接当成可信 HTTP 响应。

**策略对照：** 若 repeat 使用 `strict=True`，JSON 数字 `2` 满足整数与范围要求；字符串 `"2"` 和布尔值 `true` 被拒绝为 422，字符串重复的处理函数不会执行。这改变的是输入契约，不是重复计算的算法。

---

## 本章小结

把解析、字段规则、业务权限和输出约束分开，才能知道错误由谁负责。输入校验阻止不满足规则的数据进入正常业务；响应模型限制对外数据。它们都不能自动替代授权、事务或对下游结果的核实。

## 🎯 面试怎么回答

**Pydantic 与 FastAPI 怎样协作？**

> Pydantic 定义并执行数据模型规则，FastAPI 根据参数和返回声明把这些规则接入 HTTP 输入输出，并生成接口描述。模型负责数据形状，业务和权限需要额外判断。

**输入校验失败和响应校验失败的责任相同吗？**

> 不同。输入不满足约定通常是请求问题；本服务返回值不满足自己声明的响应模型，通常是服务端实现错误。错误分类影响状态码、告警和排查位置。

## ⚠️ 易错点

> ⚠️ “能解析为 JSON”只说明格式可读，不说明字段、权限和业务都有效。

> ⚠️ `str | None` 说明允许 None；是否可省略要看有没有默认值。

> ⚠️ 默认转换、strict 字段规则和 Content-Type 检查是三种不同层次，不应合成一个“严格开关”。

> ⚠️ 不要把完整请求体、密码、令牌或内部 traceback 放入公开错误响应。

## 本章自测

先回答，再展开核对。结合正文例子，说出预期结果及原因即可。

<details>
<summary>1. 为什么内部返回了 internal_debug，客户端却不应收到？</summary>

本例使用 PreviewOutput 作为响应模型，它只允许公开 result。前提是走普通返回值的模型处理路径，而不是自行返回未过滤的 Response。

</details>

<details>
<summary>2. 一个不存在的笔记应该算输入结构错误吗？</summary>

编号可以已经是合法整数。记录是否存在需要业务查询判断，本例将其映射成 404。

</details>

<details>
<summary>3. 把 repeat 改成 strict=True 后，JSON 字符串 "2" 和布尔值 true 应怎样处理？</summary>

都不满足严格整数字段，预期拒绝；JSON 数字 2 满足类型和范围。

</details>

## 知识回看与权威资料

- [Pydantic 严格模式](https://docs.pydantic.dev/latest/concepts/strict_mode/)：核对转换与严格类型的差异。
- [响应模型](https://fastapi.tiangolo.com/tutorial/response-model/)：核对输出校验、过滤及直接响应的边界。
- [请求错误处理](https://fastapi.tiangolo.com/tutorial/handling-errors/)：区分请求错误与程序错误。
- [JSON Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/)：核对默认检查及版本前提。

真人问题回看：[S288 的跨字段业务约束与错误反馈](../../../market/interviews/batch-29.md)。原记录讨论 Zod／Schema 的边界；本章用 Pydantic 的页码例子解释可迁移的校验思想，不把这个自拟例子当作面试原题。
