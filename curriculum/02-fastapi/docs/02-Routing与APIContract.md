# 02｜路由与参数：请求怎样变成函数输入

[← 上一章](01-FastAPI职责与ASGI请求链路.md) · [模块主页](../README.md) · [下一章 →](03-Pydantic与数据契约.md)

同一个接口不应该只会返回同一句话。用户可能想看第 3 条笔记，也可能只要前 2 条，或者提交一段新文字。**先判断每项数据在请求的哪个位置，再用参数声明告诉 FastAPI 怎样读取它。**

本章用一个笔记服务解释方法、路径、参数与路由组织。每个完整示例可以单独保存为 `main.py`，按第 01 章启动；不要把多个完整示例中的 `app` 定义混在同一文件里。

## 1. 先读懂一个 URL

```text
http://127.0.0.1:8000/notes?limit=2
```

这个 URL 包含服务地址 `http://127.0.0.1:8000`、路径 `/notes` 和查询参数 `limit=2`。它请求笔记列表，并用 limit 限制返回数量。方法、请求头和请求体是请求的其他部分，不都写在 URL 里。

**路由匹配主要看 HTTP 方法和路径。** 同样的 `/notes` 可以登记 GET 和 POST，分别承担读取与创建等不同职责。Python 函数参数则说明匹配后怎样取数据。[路径参数](https://fastapi.tiangolo.com/tutorial/path-params/)

### 声明语法怎样接上 Python

Python 中 `name: str | None = None` 分别表达名字、允许的类型和缺省值。FastAPI 再读取这些声明，决定如何解析外部输入。`Annotated[T, ...]` 在类型 T 之外附带元信息，例如 `Annotated[int, Query(ge=1)]`：Python 类型仍是 int，Query 元信息交给框架说明来源与限制。它本身不是一次业务函数调用。

这里继续使用 Python 的[类型提示与默认值](../../01-python/docs/04-函数-参数-作用域-闭包.md)；完整请求字段的“必填/可空”组合在下一章集中展开。

## 2. 用 Path 和 Query 读取一份已有数据

```python
# example: notes_query
from typing import Annotated
from fastapi import FastAPI, HTTPException, Query

app = FastAPI()
notes = {1: "复习函数返回值", 2: "运行第一个接口", 3: "区分路径和查询参数"}

@app.get("/notes")
def list_notes(limit: Annotated[int, Query(ge=1, le=3)] = 2):
    return [{"id": key, "text": text} for key, text in list(notes.items())[:limit]]

@app.get("/notes/{note_id}")
def get_note(note_id: int):
    if note_id not in notes:
        raise HTTPException(status_code=404, detail="笔记不存在")
    return {"id": note_id, "text": notes[note_id]}
```

先按顺序读参数声明：

1. 路径里的 `{note_id}` 与函数参数同名，因此该参数从路径取值。
2. `note_id: int` 要求把路径文字转换成整数。`/notes/2` 会让函数得到整数 `2`。
3. `limit` 没出现在路径里，使用 `Query(...)` 声明为查询参数。`= 2` 是不提供时的默认值。
4. `Annotated[int, Query(ge=1, le=3)]` 把“类型是整数”和“数值在 1 到 3 之间”放在一起。`ge` 表示大于等于，`le` 表示小于等于。[查询约束](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/)

`HTTPException` 用来中止本次接口处理并给出 HTTP 错误。这里 404 表示编号合法但记录不存在，与参数无法转换产生的 422 不同。

| 请求 | 预期 | 原因 |
|---|---|---|
| `GET /notes` | 前两条笔记 | 使用默认 limit |
| `GET /notes?limit=1` | 只有编号 1 的笔记 | 提供合法查询参数 |
| `GET /notes?limit=0` | 422 | 违反下限，不进入正常处理函数 |
| `GET /notes/2` | 编号 2 的笔记 | 路径数字转换成功 |
| `GET /notes/abc` | 422 | 不能按声明得到整数 |
| `GET /notes/99` | 404 | 已经得到整数，但不存在该记录 |

> ⚠️ `int` 类型声明不是让 Python 自动对任意函数调用作运行时校验。这里是 FastAPI 读取声明并执行了请求校验；直接在 Python 中调用函数是另一条执行路径。

### 固定路径要注意登记顺序

假设又添加 `/notes/recent`，同时已有 `/notes/{note_id}`。路由按顺序匹配，动态路径可能先把 `recent` 接住，再因不能转成整数而报 422。因此固定路径应放在可能捕获它的动态路径之前。类型校验不能代替路由优先级。[路径顺序](https://fastapi.tiangolo.com/tutorial/path-params/#order-matters)

## 3. 先接收请求体，再区分 Header 与 Cookie

读取笔记主要使用路径和查询参数；提交一段新文字时，可以把内容放在 JSON 请求体中。先只增加这一个来源：

```python
# example: note_body_app
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NoteInput(BaseModel):
    text: str  # 请求体必须提供 text 字段

@app.post("/notes/preview")
def preview(body: NoteInput):
    return {"text": body.text.upper()}
```

在 `/docs` 提交 `{"text":"hello"}`，应得到 `{"text":"HELLO"}`。`BaseModel` 是 Pydantic 的数据模型基类：FastAPI 读取 JSON，按 `NoteInput` 校验，再把模型对象传给 body。`body.text` 就是已经读出的文字。

同一条请求还可能携带请求编号、Cookie 或查询选项。下面只用来对照位置，不需要手工编写这段 HTTP 文本：

```http
POST /notes/3/preview?uppercase=true HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json
X-Request-ID: demo-1
Cookie: theme=light

{"text":"hello"}
```

| 位置 | 本例数据 | 用途 |
|---|---|---|
| Path（路径） | `3` | 定位笔记 |
| Query（查询参数） | `uppercase=true` | 控制预览选项 |
| Header（请求头） | `X-Request-ID` | 随请求携带的元信息 |
| Cookie | `theme=light` | 浏览器常用的会话或偏好载体 |
| Body（请求体） | `{"text":"hello"}` | 本次提交的内容 |

参数声明中的 `Header()` 告诉框架读取请求头，`Cookie()` 告诉框架读取 Cookie。例如 `x_request_id: Annotated[str | None, Header()] = None` 接收可省略的请求编号；Header 默认把参数名中的下划线映射为连字符，因此它对应 `X-Request-ID`。请求头名称不区分大小写。

> ⚠️ Header 和 Cookie 也来自客户端，不能仅因放在这些位置就被当作可信身份。[Header](https://fastapi.tiangolo.com/tutorial/header-params/) · [Cookie](https://fastapi.tiangolo.com/tutorial/cookie-params/)

<details>
<summary>组合实验：同时使用五种参数来源</summary>

```python
# example: notes_input
from typing import Annotated
from fastapi import Cookie, FastAPI, Header
from pydantic import BaseModel

app = FastAPI()

class NoteInput(BaseModel):
    text: str  # 声明请求体里必须有字符串字段 text

@app.post("/notes/{note_id}/preview")
def preview(
    note_id: int,
    body: NoteInput,
    uppercase: bool = False,
    x_request_id: Annotated[str | None, Header()] = None,
    theme: Annotated[str | None, Cookie()] = None,
):
    text = body.text.upper() if uppercase else body.text
    return {"id": note_id, "text": text, "request_id": x_request_id, "theme": theme}
```

本例把五种来源合在一起，输出可以逐项核对：路径决定 id，查询参数决定是否转大写，Body 提供 text，Header 和 Cookie 分别提供 request_id 与 theme。普通字符串参数不会因名字叫 theme 就自动读 Cookie。

在 `/docs` 提交 `{"text":"hello"}`、设置 `uppercase=true`，预期 text 为 `HELLO`。Cookie 的收发由浏览器管理，不要把交互文档当作能任意设置 Cookie 请求头的工具。

</details>

## 4. 方法和状态码共同构成接口约定

| 方法 | 常见意图 | 需要注意 |
|---|---|---|
| GET | 读取 | 不应被设计成改变业务状态的操作 |
| POST | 创建或执行动作 | 重试安全性需要业务实现保证 |
| PUT | 替换目标资源的表示 | 按协议语义应幂等，不能只换装饰器名 |
| PATCH | 局部修改 | 并非天然保证幂等 |
| DELETE | 删除目标资源 | 第二次的状态码可不同，不等于幂等性被破坏 |

这里“幂等”先理解为同一逻辑操作重复执行，不产生额外的预期业务效果；具体可靠性实现要依赖数据库和后端设计，HTTP 方法本身不会帮你去重。[HTTP 方法语义](https://www.rfc-editor.org/rfc/rfc9110.html#section-9)

先会区分正在使用的几种结果，不必背状态码全集：

| 常见状态 | 告诉客户端什么 |
|---|---|
| 200 | 请求成功，读取响应内容 |
| 201 / 202 / 204 | 分别是已创建、已接受但未完成、成功且无响应体 |
| 401 / 403 | 缺少有效身份凭证，或身份已确认但不允许这次访问 |
| 404 / 405 | 没有找到资源，或该路径不支持本次方法 |
| 422 | 本课程示例中，请求不满足声明的数据规则 |
| 429 / 500 | 请求超过限制，或服务内部发生错误 |

400 可表达其他不合法请求，409 可表达与当前资源状态冲突。实际选用哪些，应与接口约定和测试一致。

> ⚠️ `{"code":200,"success":false}` 中的 `200` 只是 JSON 字段，不能替代真正的 HTTP 状态码。204 也不能一边宣称没有内容，一边返回普通 JSON 正文。

### 4.1 301 和 302：响应让客户端换一个地址

重定向不是目标业务已经完成，而是服务用响应状态和 `Location` 告诉客户端另一个地址。例如旧笔记入口迁到新地址：301 表示永久迁移，302 表示暂时使用另一个地址。[HTTP 重定向规范](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.4)说明了这些含义。

浏览器或测试客户端可能自动跟随重定向，最终只让你看到新地址的 200。排错时应查看中间响应或暂时关闭自动跟随，分清“收到迁移指示”和“目标请求成功”两个步骤。

> ⚠️ 对 POST 等请求，301／302 的后续请求可能改用 GET。必须保留原方法和请求体时，应明确选择具有该语义的 307／308，不能只看“临时”或“永久”两个词。

## 5. 接口多了，再用 APIRouter 组织

当笔记、账号和任务接口开始混在一个文件里，可以按领域拆分。下面两份文件组成一个可运行例子，不是两份独立应用。

`notes_api.py`：

```python
# example: notes_router
from fastapi import APIRouter

router = APIRouter(prefix="/notes", tags=["notes"])

@router.get("/count")
def note_count():
    return {"count": 3}
```

`main.py`：

```python
# example: router_main
from fastapi import FastAPI
from notes_api import router

app = FastAPI()
app.include_router(router)
```

访问 `/notes/count` 应返回 `{"count":3}`。`prefix` 与装饰器路径组合成完整路径，`tags` 主要帮助文档分组。**只定义 router 而没有接入 app，接口就不会出现在这个应用中。**[多文件应用](https://fastapi.tiangolo.com/tutorial/bigger-applications/)

业务复杂后，再让路由调用普通服务函数。分层的目的，是让 HTTP 适配与业务计算分别可理解、可测试，不是每个五行接口都必须制造四层类。

## 6. OpenAPI 与版本兼容

FastAPI 会把参数来源、类型、约束、模型和状态声明组织成 OpenAPI。客户端可根据这份文档理解请求，但文档不替你证明实现正确。修改字段名、把可选参数变成必填，都可能破坏现有客户端。

`/v1/notes` 是一种显式版本策略，但不是任何加字段都必须创建 `/v2`。先判断旧客户端是否还能按原方式工作，再选择兼容扩展、迁移窗口或新版本入口。

**例子推导：** 若 `/notes` 增加 keyword，筛选条件可写成 `if keyword in text`。空字符串是每段文本的子串，所以空 keyword 保留全部记录；keyword 为“接口”时，这份输入只保留编号 2。先筛选再截取 limit，表示“匹配结果中的前 N 项”；顺序颠倒会先丢掉可能匹配的记录。

---

## 本章小结

参数从哪里来，由路由路径、类型和 Header、Cookie、Query 等声明共同决定。先分清位置，再明确约束和错误结果。APIRouter 组织接口，OpenAPI 描述接口；两者都不替代业务实现。

## 🎯 面试怎么回答

**一个路由声明了什么？**

> 它把方法和路径连接到处理函数，同时声明参数来源、数据类型、默认值、约束以及响应契约。框架利用这些声明解析请求并生成 OpenAPI。

**Router 与业务服务怎样分工？**

> Router 负责协议适配和请求上下文，业务服务负责可以脱离 HTTP 理解的处理过程。小功能可保持简单，复杂功能再提取，避免机械分层。

## ⚠️ 易错点

> ⚠️ 422 和 404 的排查方向不同：前者可能还没进入正常处理函数，后者可能是合法编号对应的资源不存在。

> ⚠️ 必填与能否为 None 是两个维度；`str | None` 不等于自动带默认值。

> ⚠️ 固定路径与动态路径可能互相捕获，先检查登记顺序，不要只看参数类型。

## 本章自测

先回答，再展开核对。结合正文例子，说出预期结果及原因即可。

<details>
<summary>1. 同样的 /notes，GET 成功而 POST 返回 405，可能是什么原因？</summary>

应用只登记了 GET 路由。405 表示该路径不支持本次方法，不是 JSON 字段缺失。

</details>

<details>
<summary>2. 把 x_request_id 的 Header() 去掉，会仍然读取 X-Request-ID 吗？</summary>

不会按原来的请求头声明读取。普通标量参数通常按查询参数处理。参数名相同不代表请求位置相同。

</details>

<details>
<summary>3. 只在文件里创建 APIRouter，为什么 /docs 看不到接口？</summary>

该 router 还要通过 include_router 接入实际启动的 app，同时核对 prefix 和导入的应用。

</details>

## 知识回看与权威资料

- [路径与查询参数](https://fastapi.tiangolo.com/tutorial/path-params/)：核对转换、校验与路由顺序。
- [Annotated 与查询约束](https://fastapi.tiangolo.com/tutorial/query-params-str-validations/)：理解声明的类型与框架元信息。
- [多文件应用](https://fastapi.tiangolo.com/tutorial/bigger-applications/)：查看 APIRouter 的接入方式。
