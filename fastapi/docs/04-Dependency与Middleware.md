# 04｜Dependency Injection 与 Middleware：职责、顺序与横切逻辑

`FASTAPI-002` 是一个很有代表性的真人问题：

> **Middleware 和 Dependency Injection 有什么区别？认证、日志、公共上下文到底应该放哪里？**

这不是 API 记忆题，而是在考你是否真正理解 Request Lifecycle。

---

## 1. 先看两个抽象解决什么问题

Middleware 解决的是：

> **整个 ASGI Application 的横切逻辑。**

Dependency Injection 解决的是：

> **某个 Route / Dependency Graph 需要哪些输入、资源、身份和前置条件。**

它们可能都能“执行一段前置逻辑”，但语义完全不同。

---

## 2. Middleware 的位置

FastAPI 官方语义可以抽象成：

```mermaid
flowchart LR
    A["Request"] --> B["Middleware Before"]
    B --> C["Routing / Dependencies / Handler"]
    C --> D["Middleware After"]
    D --> E["Response"]
```

常见 Middleware：

- Request ID；
- Access Log；
- Timing；
- CORS；
- Trace Context；
- 全局安全 Header；
- 某些全局 Context 初始化。

Middleware 不知道某个函数参数为什么叫 `current_user`，它更接近整个 Application 的外层。

---

## 3. Dependency 的位置

Dependency 是 Route-aware 的：

```python
from typing import Annotated
from fastapi import Depends

async def get_current_user(...):
    ...

@app.get("/me")
async def me(user: Annotated[User, Depends(get_current_user)]):
    return user
```

你声明的是：

> `/me` 这个 Handler 运行前需要一个 `User`。

FastAPI 会解析 Dependency Graph。

---

## 4. Dependency Graph 可以嵌套

```text
Handler
├── CurrentUser
│   └── TokenParser
├── DBSession
└── TenantContext
    └── CurrentUser
```

这比“在每个 Route 顶部手写认证代码”更适合复用和测试。

同时 Dependency 声明的参数可以进入 OpenAPI Contract，这也是它和纯 Middleware 的一个重要区别。

---

## 5. Middleware 的执行顺序

当有多层 Middleware 时，它们形成嵌套栈。

例如：

```python
app.add_middleware(MiddlewareA)
app.add_middleware(MiddlewareB)
```

可以理解为：

```text
Request:
B → A → Route

Response:
Route → A → B
```

最后添加的 Middleware 在外层。

顺序会影响：

- Trace Context 是否已经建立；
- CORS Header 是否还能加；
- Error 是否被外层捕获；
- Timing 到底包含哪些阶段。

---

## 6. Middleware vs Dependency 对比

| 问题 | Middleware | Dependency |
|---|---|---|
| 作用范围 | 通常全局 / Application | Route / Router / Dependency Graph |
| 是否理解 Handler 参数 | 否 | 是 |
| 是否适合 Request ID | 很适合 | 通常没必要 |
| 是否适合获取 Current User | 可以做，但 Dependency 更自然 | 很适合 |
| 是否适合 DB Session | 不推荐全局创建 | Request-scoped Dependency 很自然 |
| 是否进入 OpenAPI 输入声明 | 通常不会 | 可以 |
| 是否易做 dependency override | 不属于该机制 | 很适合 |

---

## 7. Authentication 放哪？

通常需要区分：

```text
Token Extraction
→ Authentication
→ Authorization
```

例如全局 Middleware 可以建立：

```text
request_id / trace context
```

而具体用户身份更常通过 Dependency：

```python
CurrentUser = Annotated[User, Depends(get_current_user)]
```

因为不同 Route 可能：

- 不需要登录；
- 需要用户；
- 需要管理员；
- 需要某个 Scope。

Dependency 的 Route-aware 特性更自然。

---

## 8. Logging 放哪？

也要分层：

### Access Log / Request Timing

更适合 Middleware：

```text
method
path
status
request_id
latency
```

### 业务事件日志

更适合 Service：

```text
order_refunded
knowledge_base_rebuilt
agent_run_cancelled
```

不要把所有业务日志都塞到 Middleware，因为 Middleware 不知道业务语义。

---

## 9. Tenant Context 放哪？

常见做法是：

```text
Header / Token
→ Dependency resolve tenant
→ validate membership
→ inject TenantContext
```

之后 DB / Redis / Vector DB 调用都显式拿 TenantContext。

⚠️ 不要只把 tenant_id 放进一个全局变量。

多用户并发时会产生严重状态串扰。

---

## 10. Dependency Caching 的直觉

同一 Request 内，同一个 Dependency 默认情况下可以被复用，而不是每处重新执行一遍。

这能避免：

```text
CurrentUser
被多个子依赖重复解析 Token / 查用户
```

但你不应该依赖隐含副作用来“顺便执行一次”。Dependency 最好返回明确资源或上下文。

---

## 11. Dependency 不等于 Service Locator

坏模式：

```text
所有对象
→ 全部 Depends
→ Route 获得十几个内部 Service
```

DI 应该帮助表达 API 边界和资源生命周期，而不是把整个程序都变成 FastAPI-specific Dependency Graph。

Service 内部仍然可以用普通 Python 构造和明确接口。

---

## 12. Failure：Middleware 和 Dependency 放错位置会怎样

### 把 DB Session 放 Middleware

问题：

- 静态资源 / 健康检查也可能无意义占连接；
- 生命周期难和业务 Route 对齐；
- Transaction Boundary 模糊。

### 把 Request ID 放每个 Dependency

问题：

- 重复；
- 某些非依赖路径可能缺失；
- 横切上下文不统一。

### 把 Authorization 只放 Middleware

问题：

- Route-specific Policy 很难表达；
- 容易出现 path 条件分支地狱。

---

## 13. 🎯 面试怎么回答 FASTAPI-002

> Middleware 是 ASGI Application 的外层横切机制，适合 request id、访问日志、统一 timing、CORS、trace context 这类几乎每个请求都需要的逻辑。Dependency Injection 是 Route-aware 的参数和资源图，适合 current user、tenant context、DB session、权限 scope 等具体 Endpoint 需要的前置条件。两者可以配合：Middleware 建全局请求上下文，Dependency 把身份和资源以类型化方式注入到 Handler。

---

## 14. 本章自测

<details>
<summary>1. 为什么 Current User 通常更适合 Dependency，而不是全局 Middleware？</summary>

因为不同 Route 的认证/权限要求不同，Dependency 能表达 Route-aware 的输入和子依赖，也便于 OpenAPI 与测试 override。

</details>

<details>
<summary>2. 为什么 Request ID 很适合 Middleware？</summary>

它是跨整个请求生命周期的横切上下文，通常所有 Route 都需要，而且要尽早建立、在 Response 和日志中统一传播。

</details>

<details>
<summary>3. Middleware 顺序为什么重要？</summary>

Middleware 是嵌套栈，请求和响应经过顺序相反；Trace、Exception、CORS、Timing 等层的先后会直接影响最终行为。

</details>
