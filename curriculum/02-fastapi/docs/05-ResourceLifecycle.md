# 05｜资源生命周期：何时取得，何时归还

[← 上一章](04-Dependency与Middleware.md) · [模块主页](../README.md) · [下一章 →](06-AsyncExecution与BlockingBoundary.md)

接口打开文件后发生异常，文件还需要关闭；连接池被多个请求共用，却不能因为一个请求结束就整体关闭。资源管理首先要分清：这份资源只服务一次操作，还是要被后续请求继续使用？

本章把**一次操作借用的资源**和**应用长期持有的资源**分开。先用一个能打印状态的教学对象观察生命周期，再连接到 HTTP 客户端和数据库会话。示例对象只模拟开关状态，不冒充真实数据库连接。

## 1. 先决定“谁拥有，谁负责结束”

| 范围 | 常见对象 | 生命周期 |
|---|---|---|
| 应用实例 | 可复用客户端、连接池、只读配置 | 该实例启动到关闭 |
| 请求或业务操作 | 借用的连接、文件、数据库会话 | 为这次操作取得，用完释放 |
| 当前请求的信息 | 用户、租户、请求编号 | 只对这次请求有效，不一定需要 close |

决定生命周期时，先找出谁创建了对象、谁还在使用它。一次请求可能借用共享池中的连接：应归还借出的连接，而不是销毁整个池。

## 2. yield 依赖：把使用过程夹在获取和释放之间

```python
# example: resource_app
from typing import Annotated
from fastapi import Depends, FastAPI, Request

app = FastAPI()
app.state.events = []  # 教学追踪列表，不用于保存用户业务状态

class Resource:
    def __init__(self):
        self.open = True
    def close(self):
        self.open = False

async def get_resource(request: Request):
    resource = Resource()
    request.app.state.events.append("acquire")
    try:
        yield resource
    finally:
        resource.close()
        request.app.state.events.append("release")

@app.get("/use")
async def use_resource(resource: Annotated[Resource, Depends(get_resource)], request: Request):
    request.app.state.events.append("handler")
    return {"open_during_handler": resource.open}
```

本例依赖只 `yield` 一次。框架在这行先把 resource 交给处理函数，在相应作用域结束时再继续依赖的清理逻辑。`finally` 使成功或异常退出时都经过释放步骤。[yield 依赖](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)

用 TestClient 完成一次请求后，响应应为 `{"open_during_handler":true}`，应用的 events 应为 `acquire, handler, release`。响应中的 true 描述的是**处理函数取值那一刻**，并不表示请求结束后资源仍然打开。

> ⚠️ 传给 Depends 的这个生成器依赖不需要再加 `@asynccontextmanager`。FastAPI 会按依赖语义管理它。应用 lifespan 使用的上下文管理器是另一种调用入口，不要把两个例子的装饰器互换。

## 3. function 与 request：清理时机差在哪里

FastAPI 0.141.1 中，带 yield 的依赖默认采用 request scope：

| 声明 | 清理时机 | 适合的理解 |
|---|---|---|
| `Depends(get_resource, scope="function")` | 处理函数结束后、响应发送前 | 发送结果时不再需要这个资源 |
| `Depends(get_resource, scope="request")` | 响应发送结束后 | 响应生成和发送阶段仍可能需要资源 |

这里“发送结束”是服务端请求生命周期中的事件，不是保证客户端已经阅读或保存结果。这个语义曾随版本演进，查旧文章时要一起检查版本。[scope 与子依赖](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/#early-exit-and-scope)

### 3.1 为什么返回响应对象不等于发送完成

普通 JSON 往往很快生成。流式响应则把生成器交给框架，后续发送时才不断取出内容。因此一个函数已经 return，生成器仍可能在使用它借来的资源。

写普通 JSON 接口时，先掌握获取与释放。写流式接口时，再检查生成器是否仍需访问资源；下面的对照实验用于验证这个问题。

<details>
<summary>按需实验：比较两种 scope，及嵌套依赖的结束顺序</summary>

下面是独立实验。它只观察资源开关，不实际读取已经关闭的数据库。

```python
# example: resource_scope
from typing import Annotated
from fastapi import Depends, FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

class Resource:
    def __init__(self):
        self.open = True

async def acquire():
    resource = Resource()
    try:
        yield resource
    finally:
        resource.open = False

async def observe(resource):
    yield f"resource_open={resource.open}\n"

@app.get("/request-scope")
async def request_scope(resource: Annotated[Resource, Depends(acquire, scope="request")]):
    return StreamingResponse(observe(resource), media_type="text/plain")

@app.get("/function-scope")
async def function_scope(resource: Annotated[Resource, Depends(acquire, scope="function")]):
    return StreamingResponse(observe(resource), media_type="text/plain")
```

前者的响应是 `resource_open=True`，后者是 `resource_open=False`。因为真正产生文本时，function scope 已结束。

这不是“request 总比 function 正确”。若生成前已把需要的数据取出并释放资源，function scope 可以避免长时间占用；若生成过程还需要读取资源，提前释放就不合适。

子依赖的清理也要符合依赖关系：外层依赖清理时可能仍需要内层资源，因此 request scope 的 yield 依赖不能依靠更早结束的 function scope 子依赖。把“谁先用完”画清，比背两个字符串更可靠。

</details>

## 4. lifespan：为整个应用实例准备资源

下面的 Catalog 代表已经加载的小目录。它在应用启动时创建，多次请求复用，应用退出时关闭。

```python
# example: lifespan_app
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request

class Catalog:
    def __init__(self):
        self.closed = False
        self.items = ["笔记", "任务"]
    def close(self):
        self.closed = True

@asynccontextmanager
async def lifespan(app: FastAPI):
    catalog = Catalog()
    app.state.catalog = catalog
    try:
        yield
    finally:
        catalog.close()

app = FastAPI(lifespan=lifespan)

@app.get("/catalog")
async def catalog(request: Request):
    return {"items": request.app.state.catalog.items}
```

`@asynccontextmanager` 把一个只有一次 yield 的异步生成器组织成异步上下文管理器。进入时执行 yield 之前的准备，退出时执行 finally。Uvicorn 通过应用生命周期驱动它，不需要每个路由自己启动一次。

测试时应使用 `with TestClient(app) as client:` 进入并退出生命周期。单纯构造 TestClient 不是“启动逻辑肯定执行过”的证据。[应用生命周期](https://fastapi.tiangolo.com/advanced/events/)

> ⚠️ lifespan 绑定的是**应用实例**，不是整个集群。多个 worker 通常各有自己的实例、目录对象和连接池。`app.state` 不是所有进程共享的数据库。

## 5. 异常和初始化失败也有生命周期

释放资源不等于吞掉错误。若依赖写了 `except`，记录异常后通常要重新抛出，或转成语义明确的新异常；否则调用者可能失去真实失败信息。

多个资源依次初始化时，后一个失败也要释放前面已经取得的资源。固定数量的资源通常用嵌套上下文管理器即可；动态管理一组资源时，再查 `AsyncExitStack` 的用法。

强制结束进程、断电等情况可能没有机会运行 finally。依赖清理保证的是程序的结构化退出路径，不能替代持久任务恢复。

## 6. 后台任务应该自己取得资源

后台任务不应长期引用本次请求借用的会话或文件句柄。即使某个版本的默认清理顺序碰巧允许它工作，也会把任务绑定到隐含时机。

更明确的边界是：

1. 接口把 task_id、file_id 等稳定标识交给任务。
2. 任务开始后，自己取得所需资源。
3. 任务正常或失败结束时，自己释放。

共享 HTTP 客户端可以由应用持有，但一个请求取消时只关闭自己借用的响应流，不要关闭整份共享客户端。

## 7. 从小实验判断真实资源压力

设连接池只有 2 个连接。如果两个慢速流都持续占用连接，第三个请求即使 SQL 本身很快，也要先等连接。这说明“处理函数已 return”并没有把资源压力清零。

**练习：** 给 resource_app 增加一个故意抛异常的接口，检查 events 中是否仍出现 release。需要实现流式资源读取时，再展开 scope 实验，比较发送期间资源是否仍然可用。

---

## 本章小结

资源范围决定谁负责取得和释放。yield 依赖适合请求或操作借用，lifespan 适合应用实例的长期资源。函数返回、响应发送结束、进程退出是不同时间点；流式响应最容易暴露它们之间的差别。

## 🎯 面试怎么回答

**yield 依赖和 lifespan 有什么区别？**

> 前者围绕某次依赖使用管理获取与清理，后者围绕整个应用实例启动和关闭管理共享资源。请求信息不能随意放进应用全局，应用客户端也不能因一个请求结束而整体关闭。

**为什么流式响应需要检查依赖 scope？**

> 处理函数返回响应对象以后，内容可能仍在逐步生成。如果生成器还需要资源，必须让资源范围覆盖它；若已不需要，应及时释放，避免长期占用。

## ⚠️ 易错点

> ⚠️ finally 负责结构化清理，不证明断电或强制终止后仍能完成清理。

> ⚠️ function scope 结束早，不适合仍要借资源生成响应的路径。

> ⚠️ 数据库会话关闭不等于业务事务一定提交；不要把事务承诺藏在读者看不到的清理动作里。

## 本章自测

先回答，再展开核对。涉及操作的题目，应能说出预期结果及原因。

<details>
<summary>1. 响应里 open_during_handler 为 true，为什么请求结束后资源仍可以是关闭的？</summary>

响应保存的是处理函数取值时的结果。依赖随后执行 finally 关闭资源，不会把已经生成的布尔值改写成 false。

</details>

<details>
<summary>2. 四个 worker 中 lifespan 是否通常只创建一份客户端？</summary>

不是。通常每个应用进程各运行自己的生命周期，资源总量要按实例数量估算。

</details>

<details>
<summary>3. 依赖捕获异常只写日志后不再抛出，风险是什么？</summary>

可能吞掉真实失败，使框架与调用者无法正确处理。应该保持明确的传播或映射语义。

</details>

## 知识回看与权威资料

- [yield 与 scope](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)：核对清理时机及嵌套限制。
- [lifespan](https://fastapi.tiangolo.com/advanced/events/)：理解应用级初始化和关闭。
- [生命周期测试](https://fastapi.tiangolo.com/advanced/testing-events/)：核对 TestClient 的上下文管理方式。
