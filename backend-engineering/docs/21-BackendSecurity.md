# 21. Backend Security：SSRF / CSRF / SQLi / XSS / Secret / Trust Boundary

> Backend Security 的核心不是背漏洞名，而是理解：**不可信数据从哪里进入、在哪里被解释、能触达什么能力、怎样限制爆炸半径。**

## 1. 先画 Trust Boundary

典型 AI Backend：

```text
User Input
  ↓
API
  ↓
Database / Redis / Vector DB
  ↓
LLM / Tool / URL Fetcher / File Parser
  ↓
External Network
```

每跨一层都要问：

```text
这段数据可信到什么程度？
谁验证？
谁编码？
能访问什么？
```

---

## 2. SQL Injection

错误：

```python
sql = f"SELECT * FROM users WHERE name = '{name}'"
```

用户输入进入 SQL Syntax。

正确核心：

```text
Parameterized Query
```

让：

```text
SQL Structure
和
User Data
```

分离。

ORM 也不是万能安全层；如果自己拼 Raw SQL 仍可能注入。

---

## 3. XSS

攻击者让恶意内容进入浏览器可执行上下文。

后端常见职责：

- 明确 Content-Type；
- 安全输出数据；
- 不把用户内容当 HTML/Script；
- 配合前端 Context-aware Encoding / CSP。

AI 生成内容同样是不可信输出。

不要因为内容来自 LLM 就直接 `innerHTML`。

---

## 4. CSRF

浏览器会自动携带 Cookie，因此恶意页面可能诱导用户浏览器向目标站点发请求。

防护通常包括：

- SameSite Cookie；
- CSRF Token；
- Origin / Referer 验证；
- 不把危险操作设计成 GET。

如果 API 只使用不会被浏览器自动附带的 Authorization Header，威胁模型不同，但仍要正确处理 CORS / Token Storage。

---

## 5. SSRF

AI / Agent Backend 特别常见：

```text
user asks model to fetch URL
→ backend HTTP client
→ arbitrary network target
```

攻击者可能访问：

- localhost；
- cloud metadata；
- internal admin service；
- private IP；
- file/protocol handlers。

---

## 6. SSRF 防护

常见思路：

```text
allowlist domains / schemes
resolve and validate IP
block private / loopback / link-local ranges
limit redirects
network egress policy
separate fetcher sandbox
response size/time limit
```

注意 DNS rebinding / redirect 可能让“第一次校验 URL”不够。

更强的设计是：

> 让 Fetcher 运行在本身就无法访问敏感网络的环境。

这叫 Capability Reduction。

---

## 7. Secret Management

Secret 包括：

- DB Password；
- API Key；
- OAuth Client Secret；
- Signing Key；
- cloud credential。

不要：

- commit 到 Git；
- bake 进 Docker Image；
- 写进日志；
- 返回前端；
- 放 Prompt。

---

## 8. Secret Lifecycle

真正的 Secret 管理包括：

```text
provision
→ distribute
→ use
→ rotate
→ revoke
→ audit
```

“放环境变量”只解决一部分 Distribution 问题，不是完整生命周期。

---

## 9. Log Redaction

日志最容易泄漏：

```text
Authorization header
Cookie
API key
Prompt with personal data
Tool payload
```

应该在 Logging Layer 做：

- field allowlist；
- redact / hash；
- sampling；
- access control；
- retention policy。

Observability 和 Privacy 必须一起设计。

---

## 10. Reverse Shell / Command Injection

危险：

```python
os.system(user_input)
```

或 Agent Tool：

```text
shell(command_from_model)
```

模型输出不能作为可信 Command。

需要：

- structured command schema；
- allowlist；
- no shell when possible；
- sandbox；
- permission / approval；
- resource limit。

---

## 11. Container Escape 的直觉

Container 不是绝对安全边界。

风险来自：

- privileged container；
- host mount；
- Docker socket；
- kernel vulnerability；
- excessive capabilities。

所以 Sandbox 设计要贯彻 Least Privilege。

---

## 12. Least Privilege

每个组件只获得它真正需要的能力。

例如 URL Fetcher：

```text
can access public internet
cannot access DB subnet
cannot read secret store
cannot execute shell
```

Tool Worker：

```text
only scoped credential
only target tenant
only necessary filesystem path
```

即使 Prompt Injection 成功，攻击面也被限制。

---

## 13. Input Boundary

外部输入包括：

```text
HTTP body
file
URL
MQ message
LLM output
tool output
web content
```

每种输入都可能不可信。

所以必须：

```text
parse
→ validate schema
→ validate business invariant
→ authorize
→ execute
```

Python Structured Output 章节已经讲过同一模型。

---

## 14. Output Boundary

服务输出也可能危险：

- XSS；
- CSV injection；
- secret leakage；
- prompt leakage；
- stack trace；
- internal hostname。

错误响应不要把完整 Exception / SQL / Token 返回用户。

---

## 15. Multi-tenant Security

最严重的事故之一：跨租户数据访问。

必须从：

```text
Auth Principal
→ tenant_id
→ DB query
→ Cache key
→ Vector filter
→ MQ task
→ Tool credential
```

全链传递。

任何一层遗漏都可能造成泄漏。

---

## 16. AI 场景：Prompt Injection 进入 Backend

Prompt Injection 本身归 Agent Security 深讲，但 Backend 必须提供硬边界：

```text
untrusted text
→ model asks tool
→ server permission check
→ scoped credential
→ sandbox
→ audit
```

不能让 Prompt 决定真实权限。

---

## 17. Security Failure 要可观测

记录：

```text
auth denied
permission denied
ssrf blocked
invalid schema
secret access
high-risk approval
```

但不能把 Secret 本身记录进去。

---

## 18. 🎯 面试怎么答

**问：什么是 SSRF，AI Agent 为什么更容易遇到？**

可以回答：

> SSRF 是服务端根据不可信输入去访问攻击者指定的网络目标，可能穿透到 localhost、内网或 cloud metadata。Agent 经常有 URL Fetch / Browser Tool，模型还会处理不可信网页内容，所以风险更突出。我会限制协议和目标、验证解析后的 IP、限制 Redirect，更重要的是用 Network Egress / Sandbox 让 Fetcher 本身无法访问敏感网络，并限制响应大小、时间和 Credential。

---

## 19. ⚠️ 易错点

- ORM ≠ 永远没有 SQL Injection；
- CORS ≠ CSRF 防护本身；
- Container ≠ 安全沙箱；
- LLM Output ≠ Trusted Input；
- Secret 放 Env ≠ 完整 Secret Management；
- Prompt “禁止危险操作” ≠ Authorization。

---

## 20. 本章自测

<details>
<summary>1. 为什么 SSRF 最强的防护往往不是 URL 字符串校验？</summary>

URL 解析、DNS、Redirect 都可能绕过简单字符串规则。更可靠的是同时限制目标和网络能力，让 Fetcher 所在环境根本无法访问敏感内网/metadata，并遵循最小权限。

</details>

<details>
<summary>2. 为什么 LLM 输出也要 Schema / Business / Permission Validation？</summary>

模型输出是概率性、不可信数据，可能受 Prompt Injection 或 hallucination 影响。只有经过结构、业务和权限校验后才能执行真实副作用。

</details>

<details>
<summary>3. 为什么日志也属于 Security Boundary？</summary>

日志可能长期保存且被更多人员/系统访问，如果记录 Token、Secret、隐私 Prompt，会成为独立泄漏面，因此必须 Redaction、Access Control 和 Retention 治理。

</details>
