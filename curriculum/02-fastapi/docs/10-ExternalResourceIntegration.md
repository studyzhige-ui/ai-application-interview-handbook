# 10｜连接外部服务：客户端、业务与协议适配

[← 上一章](09-Security与TenantContext.md) · [模块主页](../README.md) · [下一章 →](11-BackgroundTask与Upload.md)

接口已经能接收问题，现在需要向另一个服务取答案。最容易写出的代码是“在路由里创建客户端，再发请求”。小实验能工作，但当请求变多、下游超时或供应商换接口时，问题开始交织。

本章用一个模拟 HTTP 下游，把连接复用、数据转换、业务调用和错误映射分别放到看得见的位置。不需要先安装数据库，也不使用真实模型密钥。

## 1. 先划清三个职责，不急着建立很多类

| 部分 | 应该知道什么 | 不应被迫知道什么 |
|---|---|---|
| 路由 | 请求参数、身份、响应与 HTTP 错误 | 每个供应商的全部协议细节 |
| 业务服务 | 本次任务要取得和组合什么结果 | 结果将由网页还是命令行展示 |
| 外部适配 | 地址、超时、下游字段与错误 | 哪个按钮触发了请求 |

小项目可以用普通函数实现这些职责。分层是为了减少耦合，不是规定每个函数都要有一层抽象类。

## 2. 一份不用联网的完整调用实验

先看一次成功调用。公开接口收 `text`，模拟供应商却用 `answer` 表示返回文字，适配代码需要把两者连接起来：

```text
POST /ask，提交 {"text":"你好"}
    → answer_question 发送 GET /answer?q=你好
    → 模拟供应商返回 {"answer":"模拟回答：你好"}
    → 校验并转换，API 返回 {"text":"模拟回答：你好"}
```

程序中的三个关键位置是：ask 处理 HTTP 输入和错误，answer_question 调用并转换下游结果，lifespan 创建和关闭共享客户端。fake_provider 是测试替身，用固定输入触发成功、超时和错误，便于离线观察。

完整代码保留在下面。先抓住这条调用线，再查看客户端如何配置，不需要从头记住所有类型名称。

<details>
<summary>展开完整调用实验：共享客户端、请求转换与错误映射</summary>

```python
# example: external_app
from contextlib import asynccontextmanager
from typing import Annotated
import httpx
from fastapi import Depends, FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

class Question(BaseModel):
    text: str = Field(min_length=1, max_length=200)

class Answer(BaseModel):
    text: str

class ProviderReply(BaseModel):
    answer: str

class ProviderUnavailable(Exception):
    pass

class ProviderTimeout(Exception):
    pass

def fake_provider(request: httpx.Request) -> httpx.Response:
    mode = request.url.params.get("q")
    if mode == "timeout":
        raise httpx.ReadTimeout("教学超时", request=request)
    if mode == "busy":
        return httpx.Response(503, json={"error": "busy"})
    if mode == "broken":
        return httpx.Response(200, json={"wrong_field": "x"})
    return httpx.Response(200, json={"answer": "模拟回答：" + str(mode)})

@asynccontextmanager
async def lifespan(app: FastAPI):
    async with httpx.AsyncClient(
        base_url="https://provider.example",
        transport=httpx.MockTransport(fake_provider),
        timeout=httpx.Timeout(3.0, connect=1.0, pool=0.5),
        limits=httpx.Limits(max_connections=10, max_keepalive_connections=5),
    ) as client:
        app.state.provider = client
        yield

app = FastAPI(lifespan=lifespan)

def get_provider(request: Request) -> httpx.AsyncClient:
    return request.app.state.provider

async def answer_question(client: httpx.AsyncClient, text: str) -> Answer:
    try:
        response = await client.get("/answer", params={"q": text})
        response.raise_for_status()
        parsed = ProviderReply.model_validate(response.json())
    except httpx.TimeoutException as exc:
        raise ProviderTimeout() from exc
    except (httpx.HTTPError, ValueError) as exc:
        raise ProviderUnavailable() from exc
    return Answer(text=parsed.answer)

@app.post("/ask", response_model=Answer)
async def ask(
    question: Question,
    client: Annotated[httpx.AsyncClient, Depends(get_provider)],
):
    try:
        return await answer_question(client, question.text)
    except ProviderTimeout:
        raise HTTPException(504, "下游服务响应超时") from None
    except ProviderUnavailable:
        raise HTTPException(502, "下游结果暂不可用") from None
```

</details>

测试时使用 `with TestClient(app)`，确保共享客户端已经初始化。通过 `/docs` 或测试发送 `{"text":"你好"}`，应得到 `{"text":"模拟回答：你好"}`。

| text | 预期状态 | 哪个边界处理了它 |
|---|---:|---|
| `你好` | 200 | 适配下游 answer 字段为接口 text 字段 |
| `timeout` | 504 | 下游等待超时映射为 API 错误 |
| `busy` | 502 | 本例将下游非成功响应归为不可用 |
| `broken` | 502 | HTTP 200 但内容不符合下游数据约定 |
| 空字符串 | 422 | 请求输入校验，业务函数不必开始调用 |

例子的 502、504 映射是明确的教学策略，实际系统应根据自身角色与客户端契约选择。不要盲目把下游响应原封不动透传，也不要吞掉所有错误后返回 200。

### 2.1 502 和 504 都是失败，为什么要分开

当服务充当网关或代理调用上游时，**502 表示取得了无效的上游响应，504 表示没有及时取得所需的上游响应**；不是所有内部错误都属于这两类。[HTTP 状态码规范](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.3)给出了角色和含义。

本例把“字段损坏”与其他下游不可用情况统一映射为 502，是简化的对外策略，不是要求把任意下游非 200 都改成 502。真实接口应区分可理解的业务拒绝、暂时不可用和协议错误，并保持约定一致。

排查时还要先找到谁返回了这个状态码：可能是本应用，也可能是它前面的代理。代理等不到应用会返回 504，而应用可能仍在执行；不能看到 504 就断定某个下游动作没有发生。

## 3. 为什么客户端放在 lifespan

共享 HTTP 客户端可以管理连接池，在多个请求间复用合适的连接。每次请求新建客户端，会失去这种持续复用的机会，并增加建连与清理成本。

本例的共享对象只保存连接和配置，不保存“当前用户是谁”。单次请求结束不关闭它；应用退出时才由上下文管理器关闭。

> ⚠️ MockTransport 验证的是协议适配，不是真实 TCP、TLS、连接池或断网行为。真实环境还应做集成测试，不能从本例的速度推算服务吞吐。

## 4. 超时不只有一个数字

HTTPX 将超时分成连接、读取、写入和等待连接池等维度。它们回答的问题不同：

- 连接超时：能否及时与下游建立连接？
- 读取超时：接收数据时是否长时间没有进展？
- 写入超时：发送数据时是否长时间没有进展？
- 连接池超时：本地能否及时获得可用连接？

这些等待限制不自动等价于整个业务操作的统一截止时间。需要总时限时，还要在更外层管理总预算。重试也不放在每个路由里各写一遍，应由明确的可靠性策略管理。

**超时只说明未及时获得结果，不证明下游没有执行。** 读请求与创建订单、发送邮件等动作的重试风险不同。

## 5. 接数据库时，客户端、连接、会话和事务不要混名

先给初学阶段需要的最小区别：

| 对象 | 作用 | 常见生命周期 |
|---|---|---|
| 客户端或连接池入口 | 管理访问和连接复用 | 应用范围 |
| 一次借出的连接 | 本次与服务通信的通道 | 使用期间 |
| 数据库会话对象 | 管理一组数据库操作的上下文 | 请求或业务操作范围 |
| 事务 | 确定一组读写的提交与回滚边界 | 明确的一段业务过程 |

并非每个数据库库都使用同样的类名，也不是一个 HTTP 请求必然对应一个事务。这里先理解谁拥有、谁释放；表、SQL、事务隔离及具体数据库实现由 MySQL 模块系统讲解。

连接资源应由拥有它的层关闭。使用同步驱动时仍遵守执行边界：FastAPI 不会把 async 路由里直接调用的同步驱动自动转到线程池。

## 6. Redis、向量与模型服务怎样接入

接入不同服务时，仍要明确客户端由谁管理、请求怎样转换、用户允许访问什么、失败怎样返回。例如供应商把 answer 改名为 output，适配层可以吸收这个变化，而公开 API 继续使用 text。数据库和缓存有各自的数据规则，但不需要因此让每个路由知道全部外部协议。

## 7. SQL 很快，为什么接口还是很慢

假设一次请求共耗时两秒：

```text
等待可用连接   1.80 秒
执行查询       0.02 秒
其他处理       0.18 秒
```

只看到“查询 20 毫秒”无法解释用户等待。连接池等待、查询执行和结果处理应分开观察。盲目增加 API worker，也可能同时增加连接竞争。

长流式响应还可能使一个不再需要的事务或连接被占用几十秒。先完成必要的短操作、取出后续需要的数据，再释放资源，是常见的改进方向；不是所有业务都适合在 handler 一开始就开事务，直到最后一段网络数据发完才关闭。

**练习：** 将 fake_provider 的 `answer` 字段改名。先确认当前测试会发现 502，再仅调整适配模型和转换逻辑，保持公开 `/ask` 返回字段仍叫 `text`。解释为什么客户端无需因供应商字段变化而同步改接口。

---

## 本章小结

接入外部系统时，先分清资源所有权与数据边界。客户端复用、有限等待、内容校验和错误映射是 API 的职责；具体数据库与可靠性机制仍有自己的学习位置。

## 🎯 面试怎么回答

**为什么外部服务已经返回 200，API 还可能返回 502？**

> HTTP 成功不保证内容符合下游契约。字段缺失或类型异常应在适配边界发现，而不是把错误数据当可信结果返回。

**为什么共享客户端与请求身份不能用同一种全局存储方式？**

> 客户端通常是可复用资源；身份是每次请求的上下文。混放会让并发请求相互覆盖身份或错误关闭共享资源。

## ⚠️ 易错点

> ⚠️ 显式捕获预期的网络和解析错误，不用一个无限宽的异常捕获掩盖所有编程错误。

> ⚠️ 连接池等待也占请求预算；查询快不等于获得连接快。

> ⚠️ 事务不是连接的同义词，也不必与一个 HTTP 请求完全同生共死。

## 本章自测

先回答，再展开核对。涉及操作的题目，应能说出预期结果及原因。

<details>
<summary>1. 怎样在不调用真实模型的情况下验证超时映射？</summary>

用确定的测试适配器抛出网络超时异常，检查 API 状态和错误内容；之后另做真实供应商集成测试。

</details>

<details>
<summary>2. 本例能证明共享客户端减少了真实 TLS 握手吗？</summary>

不能。MockTransport 不建立真实网络连接；它只验证请求转换和错误路径。

</details>

<details>
<summary>3. 哪里适合吸收供应商字段改名？</summary>

外部适配与数据映射层，保持公开响应契约稳定。

</details>

## 知识回看与权威资料

- [HTTPX 客户端复用](https://www.python-httpx.org/async/)：理解异步客户端生命周期。
- [HTTPX 超时](https://www.python-httpx.org/advanced/timeouts/)：区分连接、读写与连接池等待。
- [HTTPX 测试传输](https://www.python-httpx.org/advanced/transports/)：区分模拟协议与真实网络。

真人问题回看：[S294 的 502／504 区分](../../../market/interviews/batch-33.md)、[S060 的模型 API 调用失败排查](../../../market/interviews/batch-04.md)。状态分类要落到响应来源、协议和执行结果，不只是背数字。
