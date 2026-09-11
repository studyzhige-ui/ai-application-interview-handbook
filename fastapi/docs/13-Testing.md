# 13｜Testing：Dependency Override、Streaming、WebSocket 与错误路径

FastAPI 测试不能只覆盖：

```text
GET /health -> 200
```

AI Service 更需要验证：

- Dependency 是否可替换；
- Provider Failure 是否正确映射；
- Streaming Event 是否符合协议；
- WebSocket 是否能收发；
- Lifespan Resource 是否正确初始化；
- Tenant / Auth 是否隔离。

---

## 1. 最小 API Test

FastAPI 的 `TestClient` 基于 Starlette/HTTPX 的测试能力：

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_health():
    response = client.get("/health")
    assert response.status_code == 200
```

测试重点不只是 Status，还要看 Contract。

---

## 2. 测试 Input Validation

```python
def test_invalid_top_k():
    response = client.post(
        "/rag/query",
        json={"query": "x", "top_k": -1},
    )
    assert response.status_code == 422
```

要覆盖：

```text
missing field
wrong type
boundary value
unexpected field（按模型策略）
```

---

## 3. `app.dependency_overrides`

这是 FastAPI 测试很重要的能力。

```python
async def fake_current_user():
    return User(id="u_test")

app.dependency_overrides[get_current_user] = fake_current_user
```

测试结束后要恢复：

```python
app.dependency_overrides = {}
```

这样可以替换：

- Auth Provider；
- DB Dependency；
- Feature Context；
- External Service Dependency。

---

## 4. 为什么 Dependency Override 很重要

如果每个测试都真实调用：

```text
OAuth Server
LLM Provider
Production DB
```

测试会：

- 慢；
- 贵；
- 不稳定；
- 难制造错误路径。

所以要区分：

```text
Unit / API Contract Test
Integration Test
End-to-End Test
```

不是所有测试都依赖真实外部服务。

---

## 5. Service Layer 更容易测试

如果 Route 很薄：

```python
@app.post("/chat")
async def chat(req: ChatRequest):
    return await chat_service.run(req)
```

那么：

```text
Service Test
可以脱离 HTTP
```

Route Test 只验证：

```text
HTTP input/output mapping
status
schema
auth dependency
```

这就是分层带来的测试收益。

---

## 6. Lifespan 测试

如果测试依赖 startup/shutdown Resource，要确保 Lifespan 真正执行。

常见方式是用 Context Manager 管 TestClient：

```python
with TestClient(app) as client:
    response = client.get("/health")
```

这样 startup/shutdown 更接近真实 Application Lifecycle。

---

## 7. Streaming Test 测什么

不要只测“最终字符串等于 hello”。

还要测：

```text
事件顺序
首事件
终止事件
error event
run_id
sequence
```

例如期望：

```text
message_start
content_delta
content_delta
message_end
```

如果 Tool Failure：

```text
message_start
 tool_call_start
 error
 message_end / failed
```

---

## 8. SSE Protocol Test

至少验证：

- `Content-Type`；
- event type；
- data schema；
- terminal event；
- error path。

如果前端依赖 `id` / retry，也要测试。

---

## 9. WebSocket Test

FastAPI 官方测试支持用 `TestClient.websocket_connect()`：

```python
with client.websocket_connect("/ws") as websocket:
    websocket.send_json({"type": "ping"})
    data = websocket.receive_json()
    assert data["type"] == "pong"
```

应该覆盖：

- handshake auth；
- invalid message；
- disconnect cleanup；
- event order。

---

## 10. Error Mapping Test

例如 Service 抛：

```text
KnowledgeBaseNotFound
```

API 应稳定映射成：

```text
404
+ error.code = KB_NOT_FOUND
```

测试的是 Contract，不是异常类内部实现。

---

## 11. Provider Failure Test

需要主动构造：

```text
LLM timeout
429
5xx
malformed response
stream broken halfway
```

否则你的“错误处理”只是没有执行过的代码。

---

## 12. Tenant Isolation Test

必须测试：

```text
user A cannot access tenant B KB
session id collision does not cross tenant
vector query always carries tenant filter
```

这类安全测试比“JWT 能成功解析”更重要。

---

## 13. 测试不要过度 Mock

如果所有东西都 mock：

```text
Router mock
Service mock
Repo mock
Provider mock
```

测试只证明 mock 按预期工作。

建议分层：

```text
Pure Unit
Fast API Contract
Integration with local dependency
Provider Contract
End-to-End
```

不同层解决不同风险。

---

## 14. 🎯 面试怎么回答

> FastAPI 测试我会分 API Contract 和业务 Service 两层。Router 层用 TestClient 验证 Validation、Status、Auth、Error Mapping，并通过 `app.dependency_overrides` 替换外部 Auth/DB 等依赖；Service 层尽量脱离 FastAPI 测核心流程。Streaming 还要验证事件顺序、terminal/error event，WebSocket 要测 handshake、message schema 和 disconnect cleanup，而不是只看最终文本。

---

## 15. 本章自测

<details>
<summary>1. Dependency Override 解决什么问题？</summary>

允许测试时替换真实依赖和它的子依赖，例如 Auth Provider，从而构造稳定、便宜、可控的测试环境。

</details>

<details>
<summary>2. 为什么 Streaming Test 不能只校验最终拼接字符串？</summary>

因为前端依赖事件顺序、事件类型、error/terminal semantics；最终字符串正确不代表协议正确。

</details>

<details>
<summary>3. 为什么所有层都 Mock 不是好测试？</summary>

过度 Mock 会失去组件组合和真实 Contract 的验证，测试可能只是在验证自己写的 mock 行为。

</details>
