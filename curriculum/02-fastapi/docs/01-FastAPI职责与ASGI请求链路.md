# 01｜从一个可访问的接口理解请求与响应

[模块主页](../README.md) · [下一章 →](02-Routing与APIContract.md)

你写了一个 Python 函数，输入一段文字，返回处理结果。在自己的电脑里调用它很容易。可同学在浏览器里点一下按钮，怎样才能让你的函数执行，并拿到结果？

中间缺的是一个可以接收请求的服务。**FastAPI 把网络请求转换为 Python 函数能够处理的输入，再把函数结果转换为响应。** 先看一个可以被浏览器访问的小接口，再沿这次访问认识客户端、服务器和框架。不需要一开始就背完整的生产架构。

## 1. 一次访问由两边共同完成

浏览器发送请求，服务按请求执行代码，再返回响应。两边通过 HTTP 约定请求和响应的格式，不需要使用同一种编程语言。

- **客户端（Client）** 发起请求，可以是浏览器、手机应用或另一个 Python 程序。
- **服务端（Server）** 监听一个地址，接收请求并发送响应。
- **API（应用程序接口）** 规定可以请求什么、怎样传参、能得到什么。本模块讨论通过 HTTP 访问的 API。

一次 HTTP 请求至少要让服务知道方法和路径。`GET /hello` 表示用 GET 方法请求 `/hello` 这个路径；响应除了内容，还包含 `200`、`404` 等状态码。先把这两个方向分开，不必立刻记完所有状态码。[HTTP 与 ASGI 的边界](https://asgi.readthedocs.io/en/latest/specs/www.html)

## 2. 阅读代码的前提与版本边界

默认你已有 Python 代码环境，不再从安装、虚拟环境和编辑器开始。正文以 Python 3.11+、FastAPI 0.141.1、Pydantic v2 为示例基线；[可执行例子与回归](../examples/README.md)保留运行参考和版本记录。你可以直接沿下面的输入、处理和输出阅读，不需要先启动服务才能理解下一节。

Uvicorn 是加载应用并监听网络的程序，HTTPX 和 TestClient 用来发送或模拟请求，pytest 检查预期行为。它们分别是服务器、客户端和测试工具，不是同一个东西的不同名字。

## 3. 写一个能回答“你好”的接口

下面是一份完整的 `main.py`，创建应用并登记一个接口。

```python
# example: hello_app
from fastapi import FastAPI

app = FastAPI()  # 应用对象：在这里登记有哪些接口

@app.get("/hello")  # 只有 GET 方法和 /hello 路径匹配时，才调用下面的函数
def hello():
    return {"message": "你好，接口已经工作了"}
```

这段程序有三个不同的动作：

1. 导入 `FastAPI` 类，创建应用对象 `app`。
2. 执行装饰器，把“GET + `/hello`”与 `hello` 函数关联起来。这叫注册路由。
3. **真正收到匹配请求时**，框架才调用 `hello`，把返回的字典编码成 JSON 响应。

`return` 把结果交回框架，`print` 只会在服务端终端里打印。函数名不决定网址，把 `hello` 改名成 `greet` 不会自动改变 `/hello`。[官方最小接口](https://fastapi.tiangolo.com/tutorial/first-steps/)

### 3.1 启动不是直接运行一次函数

在 `main.py` 所在目录执行：

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

`main:app` 的意思是“导入 `main.py` 模块中的 `app` 对象”。`8000` 是监听端口，`--reload` 让开发时的代码修改触发重新加载。终端持续运行、没有马上回到提示符，是因为服务正在等待请求，不是卡死。

打开浏览器，访问：

```text
http://127.0.0.1:8000/hello
```

应看到：

```json
{"message":"你好，接口已经工作了"}
```

浏览器显示的空格和中文转义可能不同，JSON 中的键和值才是要核对的内容。停止服务可以在运行它的终端按 `Ctrl+C`。

> ⚠️ `127.0.0.1` 指当前这台电脑。把这个地址发给别人，他访问的是自己的电脑，不是你的服务。本章只做本地练习，不需要开放公网端口。

### 3.2 三次访问，分清三种现象

| 操作 | 应看到什么 | 为什么 |
|---|---|---|
| 访问 `/hello` | JSON，状态 200 | 方法和路径匹配 |
| 访问 `/` | 状态 404 | 我们没有登记根路径 |
| 停止 Uvicorn 后再次访问 | 连接失败，而不是本应用返回的 404 | 已没有服务在该端口接收请求 |

“接口返回错误”和“根本没连上服务”是不同问题。先判断自己到了哪一步，比不停改业务函数有效。

## 4. 打开交互文档，再观察一次真实请求

访问 `http://127.0.0.1:8000/docs`，展开 `GET /hello`，点击 **Try it out**，再点击 **Execute**。页面会发出请求，并展示状态码和响应内容。

三个入口不要混为一谈：

| 地址 | 用途 |
|---|---|
| `/hello` | 本次编写的业务接口 |
| `/docs` | Swagger UI 提供的交互文档页面 |
| `/openapi.json` | 按 OpenAPI 规范描述接口的机器可读文档 |

**OpenAPI 是接口描述，Swagger UI 是一种展示和操作这份描述的工具。** 描述中的参数与响应模型来自代码声明；它不会替你完成业务逻辑。[OpenAPI 说明](https://fastapi.tiangolo.com/tutorial/first-steps/#openapi)

## 5. 这次请求究竟经过了谁

回头看已经成功的访问，就能给过程中的角色起名字：

```text
浏览器发送 GET /hello
          ↓
Uvicorn 接收网络请求
          ↓
通过 ASGI 协议调用 app
          ↓
FastAPI 匹配路由并调用 hello()
          ↓
把字典编码成 JSON 响应
          ↓
Uvicorn 将响应发给浏览器
```

**ASGI（异步服务器网关接口）** 是 Python Web 服务器与应用之间约定的调用方式，不是另一个服务器，也不是 `asyncio` 的别名。

| 组件 | 在这里负责什么 |
|---|---|
| Uvicorn | 监听网络、处理协议，与 ASGI 应用通信 |
| Starlette | 提供请求、响应、路由、中间件等 Web 基础能力 |
| FastAPI | 在这些能力之上组织类型驱动的接口、依赖和 OpenAPI |
| Pydantic | 按模型校验、转换和序列化数据；类型约束的例子在第 03 章完整展开 |

普通接口通过 FastAPI 提供的对象处理请求，不必直接收发 ASGI 消息。中间件和依赖也运行在应用中，不是每增加一个就多部署一台服务器。

### 5.1 ASGI 是一段事件过程，不只是三个参数名

服务器调用 `await app(scope, receive, send)`。`scope` 保存这次交互的元信息；`receive` 是应用等待服务器事件的入口；`send` 是应用把事件交给服务器的入口。请求体可能分批到达，所以它不直接全部塞进 scope。

以下是一条 `POST /echo` 的简化过程（省略 ASGI 规范中的其他字段）：

```text
scope：type="http", method="POST", path="/echo", headers=[...]
应用 await receive()
  ← {type: "http.request", body: b"hi", more_body: False}
应用处理得到 b"HI"
应用 await send(...)
  → {type: "http.response.start", status: 200, headers: [...]}
应用 await send(...)
  → {type: "http.response.body", body: b"HI", more_body: False}
```

`more_body=True` 表示后面还有体数据；最后一块为 False。流式响应就是多次发送 body，而不是反复发送新的 HTTP 状态。响应开始后，应用不能把已交出的状态码和头撤回重发；服务器可以短暂缓冲 start，但业务不应依赖它补救中途失败。第 07 章由此引入流内错误与终止事件。[HTTP ASGI 消息](https://asgi.readthedocs.io/en/latest/specs/www.html)

连接断开可表现为 `receive` 收到 `http.disconnect`，发送时也可能遇到连接关闭错误。二者与任务完成不是同一信号，所以第 12 章还要决定业务是否停止。普通 FastAPI 路由由框架完成这些收发；不需要每个业务函数手工编写 ASGI 消息。

### 5.2 HTTP、WebSocket 与 lifespan 的范围

| scope 类型 | 这次调用覆盖什么 | 典型事件方向 |
|---|---|---|
| `http` | 一次请求与响应，底层连接可复用 | 接收请求体，发送响应开始和体 |
| `websocket` | 一条持续连接 | 收到 connect，接受连接，双向消息，断开 |
| `lifespan` | 服务器与应用的启动/退出协调 | 收到 startup/shutdown，完成准备/清理后回复 complete |

因此一条 HTTP 长连接可先后承载多个请求 scope；WebSocket 则在一个连接范围里交换多条消息。lifespan 不是给某个用户调用的业务网址，而是应用资源就绪与释放的控制过程。[ASGI 调用模型](https://asgi.readthedocs.io/en/latest/specs/main.html)

## 6. 用一个健康响应看“实现”与“检查”的对应关系

保留 `/hello`，下面的路由让同一个应用也能处理 `GET /health`：

```python
@app.get("/health")
def health():
    return {"ok": True}
```

这里只说明服务能接收和处理请求，不把它当成完整的生产健康检查。把声明与测试放在一起，能看清“期望返回什么”如何变成可重复的检查。

可以在 `/docs` 中发送请求。也可以新建 `test_main.py`：

```python
# example: hello_test
from fastapi.testclient import TestClient
from main import app


def test_health():
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"ok": True}
```

`assert` 检查实际结果是否满足预期。只加载最初的 hello_app 时，`/health` 返回 404；加入上面的路由后，同一测试得到 200 和 `{"ok":true}`。如需观察，可在同一目录运行 `python -m pytest -q`。TestClient 在进程里调用应用，不要求同时启动 Uvicorn，也不证明公网或代理配置正常。

不要再创建第二个 `app = FastAPI()` 覆盖原对象，否则之前登记的路由可能不在最终启动的应用上。

## 7. 能返回 JSON，还不等于完成了整个 AI 系统

FastAPI 解决的是输入、输出和请求生命周期。真正检索资料、调用模型、保存业务数据的是你的业务代码或外部系统。小练习可以把几行处理直接放在接口里；当功能需要独立测试、被多个入口调用时，再把它提取到普通 Python 函数或服务对象。


---

## 本章小结

一次接口访问不是直接运行 `.py` 文件，而是客户端发请求、服务器调用应用、应用处理并返回响应。保存代码、启动服务、发送请求是三个不同动作。能够分别检查连接、状态码和响应体，就有了继续学习的基础。

## 🎯 面试怎么回答

**FastAPI、Uvicorn 和 ASGI 分别是什么？**

> Uvicorn 是负责网络通信的 ASGI 服务器，ASGI 是服务器与 Python 应用的接口约定，FastAPI 是组织路由、参数、依赖和响应的应用框架。一个请求先由服务器接收，再交给应用处理。

**只会写一个路由，为什么还不等于会构建服务？**

> 路由只解决请求分发的一部分问题。可用服务还需要明确数据契约、身份权限、资源生命周期、失败处理、测试和部署；这些要沿实际请求逐步建立。

## ⚠️ 易错点

> ⚠️ `return` 才把值交回 FastAPI。终端里的 `print` 不是发给客户端的响应。

> ⚠️ 404 表示到达某个 HTTP 服务后没找到相应资源；连接失败时应先检查地址、端口和服务是否在运行。

> ⚠️ 本地地址、开发热重载和进程内测试都有适用范围，不应被表述成生产部署已经通过。

## 本章自测

先回答，再展开核对。结合正文例子，说出预期结果及原因即可。

<details>
<summary>1. 为什么 `python main.py` 执行完就退出，而 Uvicorn 命令会一直运行？</summary>

本例的模块只创建应用并注册路由，没有启动网络监听。Uvicorn 才负责加载应用并持续处理请求。

</details>

<details>
<summary>2. 函数改名后，访问路径是否必然改变？</summary>

不会。路径由装饰器的路径参数决定，函数名和 URL 是两个概念。

</details>

<details>
<summary>3. 接口练习的测试返回 404，应先检查哪两件事？</summary>

请求方法和路径是否与登记的路由匹配，以及测试导入的是否是同一个 app。

</details>

## 知识回看与权威资料

- [FastAPI 最小应用](https://fastapi.tiangolo.com/tutorial/first-steps/)：核对注册路由、启动和交互文档。
- [ASGI 接口](https://asgi.readthedocs.io/en/latest/specs/main.html)：理解服务器与应用之间的协议。
- [Python：函数与作用域](../../01-python/docs/04-函数-参数-作用域-闭包.md)：回看调用、返回和名字绑定。
