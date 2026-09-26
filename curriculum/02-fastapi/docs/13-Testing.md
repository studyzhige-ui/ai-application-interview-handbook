# 13｜测试：让成功、拒绝与失败都有证据

[← 上一章](12-TimeoutCancellation与Disconnect.md) · [模块主页](../README.md) · [下一章 →](14-Observability与Performance.md)

我们已经知道怎样让接口成功返回，也知道哪里可能失败。测试要做的是把这些预期留成可重复证据：以后改了代码，不用靠记忆逐个点网页，仍能发现行为变化。

本章不是到这里才开始测试，而是把前面每章的请求实验整理成稳定的测试方法。先用一份完整小程序，再逐步加入依赖替换、资源与流式边界。

## 1. 从一个完整的成功与拒绝测试开始

保存为 `main.py`：

```python
# example: tested_app
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, Field

app = FastAPI()

class Input(BaseModel):
    value: int = Field(ge=0, le=10)

class ProviderUnavailable(Exception):
    pass

async def real_calculation(value: int) -> int:
    return value * 2

def get_calculator():
    return real_calculation

@app.post("/double")
async def double(
    body: Input,
    calculate: Annotated[object, Depends(get_calculator)],
):
    try:
        result = await calculate(body.value)
    except ProviderUnavailable:
        raise HTTPException(502, "计算服务不可用") from None
    return {"result": result}
```

再保存同目录的 `test_main.py`：

```python
# example: basic_api_tests
import pytest
from fastapi.testclient import TestClient
from main import app

@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client

def test_success(client):
    response = client.post("/double", json={"value": 3})
    assert response.status_code == 200
    assert response.json() == {"result": 6}

@pytest.mark.parametrize("payload", [{}, {"value": -1}, {"value": 11}])
def test_rejected(client, payload):
    response = client.post("/double", json=payload)
    assert response.status_code == 422
```

`fixture` 是测试准备和收尾的复用入口。`parametrize` 让同一组断言分别检查三份输入。运行 `python -m pytest -q`，预期四个测试用例通过：一个成功路径、三个拒绝路径。

这里检查了状态码和内容，避免“200 但算错”被放过。对于校验错误，优先检查字段位置和错误类别，不把库可能调整的整段英文消息全部写死。

## 2. 怎样制造一个真实可走到的失败分支

如果从未让下游失败，就不知道 502 分支会不会执行。依赖替换允许测试改变外部边界，而保留真实路由、数据校验和错误映射。

```python
# example: override_tests
from fastapi.testclient import TestClient
from main import app, get_calculator, ProviderUnavailable

def test_provider_failure():
    async def unavailable(value: int) -> int:
        raise ProviderUnavailable()

    previous = app.dependency_overrides.copy()
    app.dependency_overrides[get_calculator] = lambda: unavailable
    try:
        with TestClient(app) as client:
            response = client.post("/double", json={"value": 3})
        assert response.status_code == 502
    finally:
        app.dependency_overrides.clear()
        app.dependency_overrides.update(previous)
```

这里有两次不同的调用：FastAPI 先调用 get_calculator 取得计算函数，路由随后调用 calculate 执行计算。因此替换依赖的 `lambda: unavailable` 要返回 unavailable 函数本身，而不是提前调用它。

请求仍经过真实路由和错误映射：是计算函数抛出的异常让接口返回 502，不是测试直接伪造了一个 502 响应。

`finally` 恢复原有覆盖，避免一个测试污染后续测试。已有测试框架也可以用 fixture 管理这个范围。[官方依赖替换文档](https://fastapi.tiangolo.com/advanced/testing-dependencies/)说明了机制。

## 3. TestClient、AsyncClient 与真实服务器验证不同东西

| 方式 | 适合验证 | 不应据此声称 |
|---|---|---|
| TestClient | 路由、校验、依赖、错误、WebSocket 协议 | 真实网络和代理时延已测过 |
| HTTPX ASGITransport | 异步调用与应用组合 | 自动启动了 lifespan，或真实连接池性能已证明 |
| Uvicorn 加真实 HTTP 客户端 | 套接字、逐步到达、断开等集成行为 | 已覆盖所有生产网关与供应商 |
| 实际部署链路 | 代理缓冲、TLS、限额、平台退出行为 | 所有负载与故障都没有问题 |

`with TestClient(app)` 会执行相应应用启动和关闭。HTTPX `AsyncClient(transport=ASGITransport(app))` 本身不会自动触发 ASGI lifespan，需要另行管理。**测试能收到 200 不证明启动资源已经正确创建。**

## 4. 有流式接口时，分别测试协议和时间

协议测试应该核对媒体类型、每条事件的数据结构、开始与结束、错误分支、序号和业务标识。SSE 解析需要处理空行、注释心跳和分块，不要把空行全部删掉后再猜事件边界。

时间测试应启动真实服务器，让生成器在两段之间明确等待，再测第一段是否早于完成时刻到达。可以用本地客户端先证明应用没有一次性攒完，再在部署环境经过代理重复同样实验。

> ⚠️ TestClient 和某些 ASGI 测试传输会缓冲响应。它们适合内容契约测试，但不能仅凭迭代接口的外观就认定自己测到了真实增量到达。

断开测试还需要区分服务是否已看到断开、生成是否被取消、资源是否已释放。这些状态不能只用“客户端关闭了”一条断言代表。

## 5. 有 WebSocket 时，测试同一条连接上的交互

针对第 08 章的回显应用，测试应建立连接，发送消息，读取回应，再完成关闭。调用普通 GET `/ws`不是 WebSocket 测试。

```python
# example: websocket_tests
from fastapi.testclient import TestClient
from websocket_app import app

def test_dialogue():
    with TestClient(app) as client:
        with client.websocket_connect("/ws") as socket:
            socket.send_text("你好")
            assert socket.receive_text() == "收到：你好"
            socket.send_text("stop")
            assert socket.receive_text() == "已结束"
    assert app.state.connections == 0
```

这里 `websocket_app.py` 是第 08 章回显程序的文件名；该测试在配套示例中已按这个名字组织。进一步应测错误消息后是否还能处理有效消息，以及未经授权的握手和动作是否拒绝。

## 6. 建立一张从需求来的测试表

不要用“测试代码行数”替代覆盖判断。针对一个带身份与下游调用的接口，至少应能找到以下几类证据：

1. 合法输入得到正确状态和响应模型。
2. 缺字段、错误类型和边界值被拒绝，且没有意外外部副作用。
3. 身份不存在、资源不属于本人时按契约拒绝。
4. 下游超时、错误状态、畸形内容都映射为预期结果。
5. 成功、异常、取消之后，该释放的资源被释放。
6. 流或后台任务有明确结束语义，不把“请求已接受”当执行成功。

少量重要的端到端测试不可省，但也不应让每个输入校验测试都依赖收费模型、生产数据库和外网。

## 7. 怎样避免越测越像自我证明

替换外部边界，保留你想验证的逻辑。若把路由、服务、适配和响应全部 mock 成想要的样子，测试只证明替身按脚本工作。

**练习：** 故意把计算改成 `value * 3`。成功路径应失败。恢复后把 ge=0 改成 ge=-1，原负数拒绝测试应失败。测试只有能抓住真实回归，才不是装饰。

---

## 本章小结

测试应从接口契约推导，分别覆盖成功、拒绝、依赖失败与资源收尾。模拟与真实网络验证各有责任，报告必须区分它们；让失败分支确实被执行，比只统计测试数量更重要。

## 🎯 面试怎么回答

**FastAPI 依赖替换为什么有利于测试？**

> 它允许替换外部资源或身份提供者，保留真实输入校验、路由和错误映射，从而稳定制造成功与失败。测试结束应恢复覆盖。

**测试 SSE 为什么不能只比较最终文字？**

> 最终文字相同仍可能缺少开始、错误、终止事件，或被代理全部缓冲。协议和真实到达时间需要分别验证。

## ⚠️ 易错点

> ⚠️ AsyncClient 配 ASGITransport 不会自动运行 lifespan。

> ⚠️ 未恢复 dependency_overrides 可能让后续测试错误地继续使用替身。

> ⚠️ 库升级时应核对行为与契约，不用随意放宽断言换取绿色结果。

## 本章自测

先回答，再展开核对。涉及操作的题目，应能说出预期结果及原因。

<details>
<summary>1. 为什么要在错误输入测试中关心有没有调用下游？</summary>

错误应在安全边界被拒绝；若已发送外部动作，再返回 422 也不能说明没有副作用。

</details>

<details>
<summary>2. 测试没经过代理，能证明线上 SSE 没有缓冲吗？</summary>

不能，需要实际部署链路的增量实验。

</details>

<details>
<summary>3. 替换 get_calculator 与直接模拟整个 HTTP 响应有什么区别？</summary>

前者仍执行真实路由和错误映射，后者可能绕过正在验收的逻辑。

</details>

## 知识回看与权威资料

- [测试教程](https://fastapi.tiangolo.com/tutorial/testing/)：理解 TestClient 与测试组织。
- [依赖覆盖](https://fastapi.tiangolo.com/advanced/testing-dependencies/)：替换与恢复依赖。
- [异步测试](https://fastapi.tiangolo.com/advanced/async-tests/)：核对异步客户端与 lifespan 边界。
- [WebSocket 测试](https://fastapi.tiangolo.com/advanced/testing-websockets/)：核对连接式交互测试。
