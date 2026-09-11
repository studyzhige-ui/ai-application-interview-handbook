# 09｜Authentication、Authorization、CORS 与 Tenant Context

FastAPI 的安全章节不应该变成 OAuth2 术语大全。

对 AI Application Engineer 更重要的是建立：

```text
谁在请求？
→ 他属于哪个 Tenant？
→ 他能访问哪些资源？
→ API 层怎样把身份传给后续 RAG / Agent / Tool？
```

---

## 1. Authentication 和 Authorization 先分清

```text
Authentication
= 你是谁？

Authorization
= 你能做什么？
```

例如：

```text
Bearer Token
→ 解析 user_id
→ Authentication 完成

user_id + resource_id
→ 检查 ownership / role / scope
→ Authorization 决定允许或拒绝
```

不要把“Token 合法”当成“拥有所有资源权限”。

---

## 2. FastAPI 为什么很适合把身份做成 Dependency

例如：

```python
from typing import Annotated
from fastapi import Depends

async def get_current_user(...) -> User:
    ...

CurrentUser = Annotated[User, Depends(get_current_user)]

@app.get("/me")
async def me(user: CurrentUser):
    return user
```

这让身份成为 Handler 的显式输入。

比隐藏全局变量更安全、更易测试。

---

## 3. Tenant Context 是 AI SaaS 的关键前置

多租户系统中，只传 `user_id` 往往不够。

更常见：

```text
user_id
tenant_id
roles / scopes
request_id
policy context
```

封装成：

```python
class RequestContext:
    user_id: str
    tenant_id: str
    scopes: set[str]
```

然后显式传给：

```text
MySQL Query
Redis Key
Vector Filter
RAG Retrieval
Agent State
Tool Permission
```

Tenant Isolation 不是前端传一个 tenant_id 就完成了。

---

## 4. Authorization 应靠数据和策略，不靠 Prompt

错误：

```text
System Prompt：不要读取别人的知识库
```

正确边界：

```text
Auth Context
→ API / Service Policy
→ DB WHERE tenant_id = ?
→ Vector Metadata Filter
→ Tool Permission
```

Prompt 可以提醒模型，但不能替代硬权限控制。

---

## 5. Route-level Policy

例如：

```text
GET /knowledge/{id}
→ member can read

DELETE /knowledge/{id}
→ admin only

POST /agent/tools/execute
→ authenticated + specific scope
```

Dependency 很适合表达这种 Route-specific Policy。

---

## 6. Middleware 在安全中的角色

Middleware 更适合：

- CORS；
- Security Headers；
- Request ID；
- 全局 Trace；
- 某些 Token Extraction / Context Bootstrap。

但细粒度业务权限通常仍应进入 Route/Service Policy。

---

## 7. CORS 到底解决什么

CORS 主要是浏览器的 Cross-Origin 访问控制机制。

例如：

```text
Frontend: https://app.example.com
API:      https://api.example.com
```

浏览器会根据 Origin 和 Server 返回的 CORS Header 决定前端脚本是否能读取响应。

FastAPI 可以使用 `CORSMiddleware`。

⚠️ CORS 不是：

- API Authentication；
- 防爬虫；
- 防服务端 HTTP Client；
- 权限系统。

---

## 8. `allow_origins=["*"]` 为什么不能无脑用

开发环境图方便可以宽松，但生产要理解：

- 哪些 Origin 真正允许；
- 是否带 Credential；
- 暴露哪些 Header；
- Preflight 行为。

安全配置应该根据实际前端部署关系设计。

---

## 9. Secret Boundary

API Key / Model Provider Secret 不应该：

```text
返回前端
写进普通 Access Log
塞进 Error Message
写入 Prompt Trace 明文
```

Request Log 需要 Redaction：

```text
Authorization: Bearer ***
api_key: ***
password: ***
```

---

## 10. Upload / Prompt / Tool Input 都是不可信输入

AI Service 的输入风险不止 SQL Injection。

包括：

```text
huge body / huge file
path traversal
malformed JSON
prompt injection
malicious retrieved content
tool parameter abuse
```

FastAPI 层负责基础输入 Contract 和上传边界；Prompt Injection / Tool Permission 的深层安全在 Agent Harness。

---

## 11. 错误响应不要泄露内部信息

不要直接把：

```text
stack trace
DB connection string
internal host
provider API error with secret
```

返回给客户端。

外部 Error Contract 应稳定且最小化；内部日志保留诊断信息并做好脱敏。

---

## 12. Multi-tenant Cache Key

例如：

```text
bad:
chat:{session_id}

better:
tenant:{tenant_id}:chat:{session_id}
```

但仅靠 Key 前缀仍不代表完整隔离。

还要确保读取路径中 tenant context 不能被客户端任意伪造。

---

## 13. 🎯 面试怎么回答

> FastAPI 层我会把身份和 Tenant Context 做成显式 Dependency，再在 Service/Data 层继续传递，而不是依赖全局变量或 Prompt。Authentication 解决“谁”，Authorization 解决“能不能访问这个资源”。CORS 只是浏览器跨域控制，不是认证。真正的多租户隔离要在 DB、Redis、Vector Filter、Agent State 和 Tool Permission 都带上可信 Tenant Context。

---

## 14. 易错点

- ❌ Token 合法 = 拥有资源权限。
- ❌ CORS = 后端安全认证。
- ❌ tenant_id 由客户端传过来就可信。
- ❌ Prompt 写“不要越权”就算 Authorization。
- ❌ Secret 可以记录到普通 Trace 里方便排错。

---

## 15. 本章自测

<details>
<summary>1. Authentication 和 Authorization 有什么区别？</summary>

Authentication 确认身份；Authorization 根据身份、资源和策略决定是否允许某个动作。

</details>

<details>
<summary>2. 为什么 Tenant Context 应成为后端可信上下文，而不是直接相信请求参数？</summary>

请求参数可被客户端伪造；可信 tenant 应从认证信息和后端映射得到，并继续用于数据查询、缓存、向量过滤和工具权限。

</details>

<details>
<summary>3. CORS 能阻止 curl 调你的 API 吗？</summary>

不能。CORS 主要由浏览器执行，用来限制前端脚本跨 Origin 读取响应，不是服务端认证机制。

</details>
