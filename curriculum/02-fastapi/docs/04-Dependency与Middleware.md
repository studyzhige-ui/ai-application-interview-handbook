# 04｜依赖与中间件：复用前提，不隐藏执行过程

[← 上一章](03-Pydantic与数据契约.md) · [模块主页](../README.md) · [下一章 →](05-ResourceLifecycle.md)

两个接口都需要分页参数，三个接口都需要知道当前用户。最直观的做法是在每个函数开头重复读取和检查。代码渐渐变多以后，你会发现同一条规则被写了好几遍，而且并不总是同步更新。

处理函数需要分页配置，就把这个需要写在参数里，让 FastAPI 调用准备函数，再把结果传进来。这就是**依赖注入**：“依赖”是需要的值或资源，“注入”是由框架准备并传入。

**中间件**处理另一类需求，例如在所有 HTTP 请求到来时记录信息，在内层返回时补上响应头。它们都能复用代码，但执行位置和交付结果的方式不同。

## 1. 先把重复的输入准备提取成依赖

下面两个接口使用同一组分页规则。例子不访问数据库，方便只观察依赖怎样执行。

```python
# example: dependency_app
from typing import Annotated
from fastapi import Depends, FastAPI, Query, Request

app = FastAPI()

def page_options(limit: Annotated[int, Query(ge=1, le=5)] = 2):
    return {"limit": limit}

PageOptions = Annotated[dict, Depends(page_options)]

@app.get("/notes")
def notes(options: PageOptions):
    return {"kind": "notes", "limit": options["limit"]}

@app.get("/tasks")
def tasks(options: PageOptions):
    return {"kind": "tasks", "limit": options["limit"]}
```

请求 `/notes?limit=3` 时，发生的是：

1. FastAPI 发现 `options` 不是要直接从请求里找的字典，而是由 `page_options` 提供。
2. 框架解析 `page_options` 的查询参数，检查 limit 范围。
3. 执行依赖函数，得到 `{"limit":3}`。
4. 把这个结果传给 `notes` 的 options，再运行处理函数。

因此两个接口的 `/docs` 都能显示 limit 参数。依赖是可调用的普通 Python 对象，`Depends` 则是让框架识别这个关系的声明。[依赖基础](https://fastapi.tiangolo.com/tutorial/dependencies/)

> ⚠️ 写 `Depends(page_options)`，不是 `Depends(page_options())`。前者交出“需要框架调用的函数”，后者会在登记路由时提前执行。离开 FastAPI，普通 Python 调用也不会自动解析 Depends；业务内部应传明确参数。

## 2. 依赖图：共享的不只是代码

身份依赖可以先依赖凭证提取，权限依赖再依赖身份。箭头表示“需要它先提供结果”，不是每个节点都单独发一次 HTTP 请求。

```text
处理函数
├── 分页配置
└── 当前用户
    └── 请求凭证
```

同一次请求中，多处需要同一项可复用依赖时，框架默认复用已求出的结果。例如两个检查都需要当前用户，不必重复取得身份；下一次请求仍会重新计算，不会复用别人的身份。

<details>
<summary>按需实验：观察请求内缓存，以及 use_cache=False</summary>

```python
# example: dependency_cache
from typing import Annotated
from fastapi import Depends, FastAPI, Request

app = FastAPI()

async def next_number(request: Request):
    request.state.calls = getattr(request.state, "calls", 0) + 1
    return request.state.calls

@app.get("/cached")
async def cached(
    a: Annotated[int, Depends(next_number)],
    b: Annotated[int, Depends(next_number)],
):
    return {"a": a, "b": b}

@app.get("/uncached")
async def uncached(
    a: Annotated[int, Depends(next_number)],
    b: Annotated[int, Depends(next_number, use_cache=False)],
):
    return {"a": a, "b": b}
```

`request.state` 是本次请求的状态容器，这里只用于记录实验次数。`getattr(..., 0)` 表示尚未记录时从 0 开始。

| 请求 | 结果 | 解释 |
|---|---|---|
| `/cached` | `{"a":1,"b":1}` | 第二处复用已求出的值 |
| 再次 `/cached` | 仍是 `1,1` | 新请求重新计算，没有共享上一请求的缓存 |
| `/uncached` | `{"a":1,"b":2}` | 第二处明确要求重新执行 |

真实依赖的缓存识别还与依赖声明的上下文有关，不要把这个实验推成“同名函数在所有情况下只运行一次”。`use_cache=False` 也不是全局缓存清理操作。[子依赖与缓存](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/)

</details>

## 3. 中间件：在进入和返回时各做一次事情

下面只记录执行顺序：A、B 两层中间件在进入和返回时各记一步，最后通过 `X-Order` 响应头展示。这样能直接看见“包住请求处理”是什么意思，不需要先接日志系统。

```python
# example: middleware_order
from fastapi import FastAPI, Request

app = FastAPI()

@app.middleware("http")
async def layer_a(request: Request, call_next):
    request.state.steps.append("A.before")
    response = await call_next(request)
    request.state.steps.append("A.after")
    return response

@app.middleware("http")
async def layer_b(request: Request, call_next):
    request.state.steps = ["B.before"]
    response = await call_next(request)
    request.state.steps.append("B.after")
    response.headers["X-Order"] = ",".join(request.state.steps)
    return response

@app.get("/order")
async def order(request: Request):
    request.state.steps.append("handler")
    return {"ok": True}
```

访问 `/order`，响应头 X-Order 应为：

```text
B.before,A.before,handler,A.after,B.after
```

最后添加的自定义中间件在这组自定义中间件的外层，所以请求从 B 进入 A，返回时再从 A 回到 B。框架还有自己的错误处理层；这张顺序图不是所有内部异常包装的源码展开。[中间件顺序](https://fastapi.tiangolo.com/tutorial/middleware/)

`call_next` 继续调用内层请求处理，返回响应对象。这个对象可能承载尚未发送完的流，因此 “after” 不应直接命名为“客户端完整收到响应之后”。

> ⚠️ `@app.middleware("http")` 处理 HTTP 请求，不会自动包住每条 WebSocket 消息。不要用它的执行次数推断 WebSocket 的消息次数。

## 4. 怎样选择放在哪里

| 需求 | 更合适的起点 | 原因 |
|---|---|---|
| 请求编号、HTTP 访问记录、CORS | 中间件 | 跨路由处理共同的 HTTP 边界 |
| 当前用户、路由所需权限、某次操作的资源 | 依赖 | 路由能声明自己实际需要什么 |
| “笔记已发布”“退款成功”等业务事件 | 业务代码 | 只有业务层知道动作是否真正完成 |
| 复杂业务内部的一组对象 | 普通构造与显式传参 | 不必全部绑到 FastAPI 的依赖系统 |

这是根据职责作出的选择，不是框架禁止你在中间件认证。应用可以用中间件完成统一身份解析，再由依赖和业务层检查具体资源权限。关键是访问范围能被明确验证。

依赖还可以挂在单个路由、APIRouter 或应用级的 `dependencies` 上。如果只需要执行检查而不使用返回值，可以放在装饰器的依赖列表；需要结果时则声明成函数参数。不要把两种方式混为“依赖返回值丢了”。

## 5. 一次请求的信息应该放在哪里

`app.state` 属于应用实例，多个请求可能同时访问；`request.state` 属于本次请求。把 `current_user` 放进应用全局变量，会让后来的请求覆盖先前请求看到的身份。

更稳妥的方式是：中间件准备请求编号，身份依赖返回可信用户，再把用户或租户上下文显式交给业务函数。请求编号用于关联记录，不能当认证凭证。

**顺序反例：** 若只交换 A、B 的登记顺序，A 先进入，却还没有 steps 列表，会在 append 处失败。稳妥的初始化可以放在确定的最外层，或用 `if not hasattr(request.state, "steps"): request.state.steps = []` 初始化后再 append。重点是初始化必须先于使用，而不是死记哪一个字母必须在外层。

---

## 本章小结

依赖声明“我需要哪个结果”，中间件说明“共同的请求处理怎样被包住”。先根据职责选位置，再观察执行顺序。请求内缓存、请求状态与应用级共享资源是不同的范围，不能因为都叫“共享”就混用。

## 🎯 面试怎么回答

**依赖和中间件的核心差异是什么？**

> 依赖是路由所需输入、资源和前提的图，结果可以直接传给处理函数；中间件包住应用或协议处理，适合请求编号、访问记录等共同逻辑。两者可以配合，不应仅按“都会提前执行”归为同一种东西。

**同一请求里的依赖缓存是什么？**

> 对可复用的相同依赖，框架可以在该请求内保存已计算结果，避免重复执行。它不是跨请求缓存，也不能替代持久存储或用户会话。

## ⚠️ 易错点

> ⚠️ 函数对象和调用结果不同，Depends 接收前者；业务函数直接调用不会凭空获得注入。

> ⚠️ 中间件拿到 response 不代表响应体已经全部发完，尤其是流式响应。

> ⚠️ 不要把身份或租户放进进程全局变量，随后期待每个请求看到自己的那一份。

## 本章自测

先回答，再展开核对。结合正文例子，说出预期结果及原因即可。

<details>
<summary>1. 两个依赖都需要当前用户，是否应该手工复制两份认证代码？</summary>

不需要。可以共享同一个身份依赖，并按请求内缓存规则复用结果。

</details>

<details>
<summary>2. 为什么业务“处理成功”的日志不宜仅由通用中间件决定？</summary>

中间件知道协议层返回情况，不一定知道业务副作用或长任务是否真正完成。

</details>

<details>
<summary>3. X-Order 实验为什么把 B 的返回步骤放在最后？</summary>

B 最后登记，处于自定义中间件外层。内层全部返回后，才继续执行 B 在 call_next 后面的语句。

</details>

## 知识回看与权威资料

- [依赖基础](https://fastapi.tiangolo.com/tutorial/dependencies/)：核对 Depends、参数来源与复用。
- [子依赖与请求内缓存](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/)：理解 use_cache 的作用范围。
- [中间件](https://fastapi.tiangolo.com/tutorial/middleware/)：核对请求和返回方向的顺序。
