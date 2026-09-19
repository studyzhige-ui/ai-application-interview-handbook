# 11｜Multi-tenancy、Security、Permission 与 Isolation

> **本章定位：System Design 组合层。** 这里关注 Tenant / Permission / Security 怎样贯穿 State、Cache、Queue、Trace 与 Tool。HTTP/API 身份上下文回到 [FastAPI Security](../../02-fastapi/docs/09-Security与TenantContext.md)，通用 Auth / Backend Security 回到 [AIBE Auth](../../03-backend-engineering/docs/15-AuthSession与TenantBoundary.md) 与 [AIBE Security](../../03-backend-engineering/docs/21-BackendSecurity.md)，Agent 高风险动作回到 [Permission / Sandbox](../../09-agent/docs/14-PermissionApprovalAndSandbox.md) 和 [Prompt Injection / Containment](../../09-agent/docs/15-InjectionAndContainment.md)。

多租户系统最危险的故障通常不是慢，而是：

> **Tenant A 看到了 Tenant B 的数据，或者一个高风险 Agent Tool 越过了权限边界。**

所以 Security 不能作为架构图最外面最后补的一圈，而要进入 State、Routing、Cache、Queue、Trace 和 Tool Contract。

---

## 1. Authentication 与 Authorization 要分清

Authentication：

> 你是谁？

Authorization：

> 你能做什么？

例如：

```text
User authenticated
≠
User can access document X
≠
User can call refund tool
```

---

# 2. Tenant Isolation 的四层

至少考虑：

```text
Identity Layer
→ request carries tenant / workspace

Data Layer
→ row / partition / namespace isolation

Compute Layer
→ quota / concurrency / worker isolation

Observability Layer
→ trace / metric / audit scoped by tenant
```

只在 API 层传一个 `tenant_id` 不够。

---

# 3. Shared vs Dedicated

多租户架构常见：

## Shared

```text
shared DB / shared cluster
+ tenant_id
```

优点：资源利用率高、运维简单。

问题：

```text
Noisy Neighbor
Security Blast Radius
Hot Tenant
```

## Dedicated

```text
large / sensitive tenant
→ dedicated DB / cluster / worker pool
```

隔离更强，但成本更高。

真实系统常混合：

```text
long-tail shared
large tenant dedicated
```

---

# 4. Permission 必须尽量靠近数据源执行

RAG 场景：

错误：

```text
全局召回
→ LLM 已经看到文档
→ 最后 UI 再隐藏
```

泄漏已经发生。

更合理：

```text
Authorization
→ tenant / ACL filter
→ Retrieval
→ Result validation
```

Permission 不应该只靠 Prompt。

---

# 5. Cache 也必须隔离

错误 Cache Key：

```text
answer:{query_hash}
```

如果不同 Tenant 问同一句话，可能共享答案。

更安全：

```text
answer:{tenant}:{permission_scope}:{version}:{query_hash}
```

是否还需 user 级维度取决于权限模型。

---

# 6. Queue 与 Worker 的 Tenant Fairness

如果所有任务共用 FIFO：

```text
Tenant A 塞 1M jobs
Tenant B 的小任务长期排队
```

除了性能问题，也可能形成资源滥用。

所以需要：

```text
quota
priority
per-tenant concurrency
fair scheduler
```

---

# 7. Secret Management

不要把：

```text
API Key
DB Password
Model Token
```

硬编码进：

```text
repo
prompt
log
trace
```

系统要考虑：

```text
Secret Store
rotation
least privilege
redaction
```

尤其 Agent Tool Result / Screenshot / Log 里可能无意带出 Secret。

---

# 8. Agent 的权限是“能力授权”

Agent 不是普通文本服务。

Tool 可能：

```text
read file
write file
execute command
send email
refund order
delete resource
```

所以 Tool Metadata 应至少表达：

```text
read-only?
destructive?
requires approval?
permission scope?
sandbox boundary?
```

高风险 Tool 需要 HITL / Approval，而不是模型自己决定“我应该有权限”。

---

# 9. Sandbox 解决什么

即使模型被允许执行代码，也不意味着：

```text
可以访问宿主机所有文件
可以任意出网
可以读所有 Secret
```

Sandbox 可以限制：

```text
filesystem
network
process
resource
credential
```

它是执行隔离，不是 Prompt Guardrail。

---

# 10. Prompt Injection 是 Trust Boundary 问题

外部文档、网页、Tool Result 中的文字：

```text
Ignore previous instructions
```

应该被视为**不可信数据**，而不是系统控制指令。

系统需要：

```text
instruction hierarchy
untrusted context marking
tool permission
output validation
secret isolation
approval
```

而不是只加一句：

> “不要听恶意 Prompt。”

---

# 11. Audit Log

高风险操作最好能回答：

```text
who
when
tenant
request / run
what action
which resource
approval by whom
result
```

这对：

- Incident；
- Compliance；
- User Dispute；
- Agent Debug；

都很重要。

---

# 12. Secure Multi-tenant Compute

如果共享 GPU / Enclave / SGX EPC 等受限资源，还要考虑：

```text
resource isolation
scheduling
memory pressure
side-channel / secret boundary
quota
```

这是 `SD-015` 的真实面试场景。

教材重点不是特定硬件细节，而是：

> **共享昂贵资源时，安全隔离与调度公平性会同时成为架构约束。**

---

# 13. 🎯 面试怎么答

> 多租户设计我会把 Isolation 放到身份、数据、计算和可观测四层，而不是只加 tenant_id。权限尽量靠近数据源执行，Cache/Queue/Trace 同样带 Tenant Scope。Agent 系统还要把 Tool 看成能力授权对象，对写、执行和敏感 Tool 配 Permission、Approval 和 Sandbox。外部 RAG/Tool 内容则作为 Untrusted Data，Prompt Injection 不能只靠 Prompt 自己防。

---

# 14. 本章自测

<details><summary>1. 为什么 UI 层过滤不能防 RAG 越权？</summary>
因为受保护内容可能已经被 Retriever 返回并进入 LLM Context，泄漏发生在生成前。
</details>

<details><summary>2. Sandbox 与 Permission 有什么区别？</summary>
Permission 决定是否允许执行某能力；Sandbox 限制即使执行了，该能力能访问的文件、网络、进程和资源范围。
</details>

<details><summary>3. 为什么 Queue Fairness 也属于 Multi-tenancy？</summary>
因为单个 Tenant 可以通过大量任务耗尽共享 Worker / Queue，影响其他租户的资源权利和 SLO。
</details>
