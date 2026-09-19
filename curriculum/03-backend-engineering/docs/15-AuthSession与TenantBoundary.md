# 15. Authentication、Authorization、Session 与 Multi-tenant Boundary

> 这一章的主线是：**先确认“你是谁”，再确认“你能做什么”，最后确保任何下游状态都不会越过 Tenant / Permission Boundary。**

## 1. Authentication vs Authorization

### Authentication

回答：

```text
Who are you?
```

例如：

- password login；
- OAuth login；
- API Key；
- service identity。

### Authorization

回答：

```text
What are you allowed to do?
```

例如：

- 能否读某 Knowledge Base；
- 能否调用高风险 Tool；
- 能否访问某 Tenant 数据；
- 能否执行 Admin API。

不要混为一谈。

---

## 2. Access Token 与 Refresh Token

典型模型：

```text
Login
→ Access Token（短）
→ API

Access Token expires
→ Refresh Token
→ new Access Token
```

为什么 Access Token 通常较短？

因为泄漏以后影响窗口更小。

Refresh Token 能长期换新 Token，风险更高，需要更严格保护。

---

## 3. JWT 不等于“Authentication System”

JWT 只是 Token Representation / Signing Format 的一种常见选择。

它不会自动解决：

- 登录流程；
- 权限模型；
- Revocation；
- Session Device 管理；
- Token Rotation；
- Secret / Key Management。

不要回答：

> “用了 JWT 就是无状态且安全。”

---

## 4. Stateless Token 的 Trade-off

优势：

```text
API instance 不需要每次查 Session Store
```

但代价：

- Token 一旦签发难立即撤销；
- 权限变化传播可能延迟；
- Payload 版本治理；
- Key Rotation；
- Token 大小。

因此很多系统仍然有：

```text
Token + Server-side session / revocation state
```

---

## 5. Server-side Session

```text
session_id cookie/token
→ Session Store
→ user / tenant / permissions / device
```

多实例下 Session Store 需要共享。

Redis 常见，但不是唯一选择。

要考虑：

- TTL；
- logout；
- concurrent device；
- session fixation；
- tenant context；
- failover。

---

## 6. OAuth2 应该掌握到什么程度

AI Application Engineer 至少理解：

```text
Resource Owner
Client
Authorization Server
Resource Server
```

以及 Authorization Code Flow 的基本关系。

当前 OAuth 安全最佳实践强调：

- Authorization Code + PKCE；
- exact redirect URI；
- 避免 Implicit / Password Grant 等旧式高风险模式；
- public client 的 refresh token 需要更严格保护。

不需要在本模块推导 OAuth 每个 RFC，但不能只会“拿 Token”。

---

## 7. API Key

机器到服务常用：

```text
Authorization: Bearer api_key
```

或自定义 Header。

API Key 应该：

- 可 revoke；
- 有 scope；
- 有 owner / tenant；
- 可 rotate；
- 日志不明文；
- 不放 URL query。

---

## 8. RBAC

Role Based Access Control：

```text
user
→ role
→ permissions
```

例如：

```text
viewer → read
editor → read/write
admin → manage
```

简单、可解释。

但复杂多租户场景可能需要更多上下文。

---

## 9. ABAC / Policy

Attribute Based：

```text
subject attributes
resource attributes
context
→ policy decision
```

例如：

```text
user.tenant_id == document.tenant_id
AND user.department in document.allowed_departments
```

Agent Tool Permission 常更接近 Policy / Capability，而不只是 Role。

---

## 10. Permission 必须在 Server 执行

错误：

```text
System Prompt:
"不要访问别的用户数据"
```

Prompt 不是 Authorization Boundary。

正确：

```text
request identity
→ server policy
→ scoped query / tool permission
```

Agent Harness 中 Prompt Injection 防护也依赖这个原则。

---

## 11. Multi-tenant Context

Request 进入后形成：

```text
principal
user_id
tenant_id
roles/scopes
request_id
```

这个 Context 要安全地传播到：

- DB query；
- Redis key；
- Vector filter；
- MQ message；
- task record；
- tool call。

不能只在 Controller 校验一次。

---

## 12. Background Task 的身份问题

用户发请求：

```text
User A
→ create background task
```

Worker 10 分钟后执行时，HTTP Request 已不存在。

所以 Task Record 必须保存：

```text
subject / tenant
permission context / resource scope
```

但不要简单保存一个永不过期 Access Token。

更成熟的是：Worker 用 Service Identity，并重新按 task owner / tenant 做授权检查。

---

## 13. Token Refresh Race

多个并发请求发现 Access Token 过期：

```text
request A → refresh
request B → refresh
request C → refresh
```

可能造成：

- refresh token rotation 冲突；
- 多个新 token；
- old token invalidation race。

常需要：

- singleflight / lock；
- refresh state；
- token version。

这也是面经常从 Auth 追到并发正确性的原因。

---

## 14. Session Routing

多实例：

```text
LB
├─ API A
├─ API B
└─ API C
```

如果 Session 外置：

```text
任何实例都能处理
```

如果 Session 只在本机：

```text
需要 sticky session
```

Sticky 不是一定错误，但要考虑实例故障和扩缩容。

---

## 15. AI 场景：RAG Permission

错误：

```text
retrieve Top-K
→ generate
→ 再检查权限
```

敏感 Chunk 已经进入模型 Context。

更安全：

```text
identity / tenant / ACL
→ retrieval filter
→ evidence
→ generation
```

Permission 应尽可能前置到数据访问边界。

---

## 16. AI 场景：Agent Tool Approval

Authentication：

```text
这是用户 A
```

Authorization：

```text
用户 A 可以调用 deploy_tool?
```

Approval：

```text
即使有权限，这次高风险动作是否需要人工确认？
```

三者是不同层。

---

## 17. Metrics / Audit

安全链应记录：

```text
who
what tenant
what resource
what action
allowed / denied
policy version
request_id / trace_id
```

敏感 Token / Secret 不能写入日志。

---

## 18. 🎯 面试怎么答

**问：Authentication 和 Authorization 有什么区别？**

可以回答：

> Authentication 确认身份，Authorization 判断这个身份对具体资源/动作是否有权限。生产系统通常先把 Token/Session 解析成 Principal，再在 Server/Policy 层做资源权限。对多租户 AI 系统，tenant_id 和权限还必须传播到 DB、Cache、Vector Retrieval、MQ Task 和 Tool，不能只靠前端或 Prompt。

---

## 19. ⚠️ 易错点

- JWT ≠ 完整 Auth System；
- Authentication ≠ Authorization；
- RBAC ≠ 所有场景够用；
- Prompt ≠ Permission Boundary；
- Background Worker 不能默认继承 HTTP Request 的权限上下文；
- Sticky Session 不能替代 Durable State。

---

## 20. 本章自测

<details>
<summary>1. 为什么 JWT 无法自动解决 Logout？</summary>

已签发 Token 在过期前仍可能有效。立即撤销通常需要短 TTL、Revocation State、Token Version、Key/Session 管理等额外机制。

</details>

<details>
<summary>2. 为什么 RAG Permission 应在 Retrieval 前执行？</summary>

如果先取敏感 Chunk 再检查，数据已经进入模型上下文或服务内存，形成泄漏风险。权限应该尽量下沉到数据访问过滤边界。

</details>

<details>
<summary>3. Authorization 与 Approval 有什么区别？</summary>

Authorization 判断主体是否具备执行动作的权限；Approval 是即使有权限，某次高风险操作是否仍需人工确认。Agent Tool 常同时需要两者。

</details>