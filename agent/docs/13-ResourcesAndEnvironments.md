# 13. L4 资源层：模型、数据与执行环境

[← 12](12-KnowledgeAndCapabilityAccess.md) · [Agent 主线](../README.md) · [14 →](14-IdentityPermissionsAndSafety.md)

> 主线位置：**L4 资源层**。接口背后必须有真实资源，现在明确谁提供能力、保存事实与执行动作。
>
> 本章产物：**资源所有权、环境生命周期与隔离方式**。

<!-- enrichment: reading-guide -->
> **阅读提示：** 先问哪类资源保存什么事实，再选择执行环境及其生命周期。沙箱是有执行风险时采用的约束手段，不是每个 Agent 都必须部署一个容器。

[资源层保存事实并提供真实能力](#part-1) → [存储选择服从状态语义](#part-2) → [执行环境与隔离](#part-3) → [环境生命周期、工作区与产物](#part-4)

<a id="part-1"></a>

## 1. 资源层保存事实并提供真实能力

模型服务提供推理与生成；业务系统产生真实状态变化；知识源和索引提供信息；持久化存储保存状态、事件、记忆与产物；执行环境承载文件、进程、浏览器或代码。

| 资源 | 主要承载内容 | 需要明确的边界 |
|---|---|---|
| 模型/Embedding/Reranker 服务 | 计算能力 | 能力、额度、版本、时延与数据边界 |
| 业务系统与 API | 权威记录、真实操作 | 身份、授权、事务、回执与幂等 |
| 文档、搜索与向量索引 | 原始资料和派生检索结构 | 来源、更新、ACL 和版本 |
| 状态与事件存储 | 恢复事实和执行记录 | 持久性、一致性、版本与保留期限 |
| 记忆与产物存储 | 可复用信息、大对象及引用 | 生命周期、完整性与租户范围 |
| 文件/进程/浏览器/沙箱 | 真实执行环境 | 资源额度、隔离、凭证与清理 |

把模型服务放在 L4 表达依赖关系，不代表模型在产品中不重要。把数据库放在 L4 也不意味着忽略数据模型；数据的语义由拥有相应责任的上层定义。

数据库和模型的内部原理分别回到 [MySQL](../../mysql/README.md)、[Redis](../../redis/README.md)、[Vector DB](../../vector-db/README.md) 和 [LLM Foundation](../../llm-foundation/README.md)。

<a id="part-2"></a>

## 2. 存储选择服从状态语义

不要按组件名分配数据。先决定哪些记录是权威、哪些是派生、哪些允许丢失，再检查所选部署的持久化和一致性保证。

### Session Store 选什么

不能只问：

> Redis 还是 MySQL？

要先问数据语义。

##### Redis 适合

```text
高频 transient state
TTL session cache
lease / heartbeat
fast coordination
```

##### MySQL / Durable DB 适合

```text
long-term session metadata
durable run record
billing / ownership
high-value audit facts
```

##### Object / Artifact Store

适合：

```text
large logs
file snapshots
model/tool artifact
```

最终通常是组合，而不是一库包办。

<a id="part-3"></a>

## 3. 执行环境与隔离

仅通过受控 API 行动的 Agent 不必具备任意代码执行能力。需要执行代码、命令或浏览器操作时，再设计与风险相称的隔离环境。普通进程或容器的存在本身不是完整安全保证。

### Sandbox 解决的是另一层问题

即使 Runtime Policy 有 bug，Sandbox 仍可以限制：

```text
filesystem
network
process
syscall
resource
workspace
```

Codex Source Index 已确认其协议层 `SandboxPolicy` 至少表达：

```text
dangerFullAccess
readOnly
externalSandbox
workspaceWrite + writable roots + network access
```

同时有独立 sandboxing / filesystem 代码路径。

这支持课程里的三层分离：

```text
Permission decision
≠ Approval workflow
≠ Sandbox enforcement
```

### Filesystem Sandbox

常见能力：

```text
read-only roots
writable workspace roots
temp directory
forbidden paths
```

例如 Coding Agent：

```text
repo workspace: write
home secrets: deny
system dirs: deny
```

重要的是：

> “模型答应不读 `/etc`”不是安全控制。

真正限制要在执行层。

### Network Sandbox

Agent 能联网后风险显著增大：

```text
数据外泄
下载恶意代码
访问内部 metadata service
调用高风险 API
```

可以按：

```text
deny by default
allow specific domain
proxy / egress gateway
DNS / IP policy
request audit
```

控制。

Anthropic 的 sandbox / containment 官方工程资料正是强调 filesystem / network isolation 与 permission prompt 要分离。

### Sandbox 不是“绝对安全”

Sandbox 仍可能有：

```text
kernel / container escape
misconfiguration
mounted secret
excessive writable path
allowed network exfiltration
```

因此要组合：

```text
Least Privilege
Sandbox
Secret Broker
Audit
Short-lived Credential
Human Approval
```

### Execution Sandbox Pool

Coding / Browser / Shell Agent 需要隔离环境。

可以：

```text
prewarm sandbox pool
→ assign to run
→ mount scoped workspace
→ execute
→ collect artifact
→ reset / destroy
```

需要治理：

```text
CPU / memory
filesystem
network
process count
timeout
secret
image version
```

Sandbox 生命周期不一定和 Session 生命周期相同。

<a id="part-4"></a>

## 4. 环境生命周期、工作区与产物

任务状态、工作区和运行进程不必同生共死。持久状态记录环境与产物引用，重建环境时验证版本、权限及未完成操作，而不是假设重新挂载就等于完全恢复。

### Workspace State 必须可控

Coding Agent 需要知道：

```text
base commit
current branch
modified files
untracked files
running processes
```

如果没有清晰 workspace boundary：

```text
上一次任务残留修改
→ 被下一次任务误认为原始代码
```

所以每个 Run 最好有：

```text
workspace identity / snapshot
```

### Patch Application 要有前置版本

如果 Agent 读到：

```text
file version A
```

准备 Patch。

但期间文件变成 B：

```text
直接覆盖
→ Lost Update
```

更安全：

```text
base hash / line context
→ apply patch
→ conflict if base changed
```

Multi-Agent 场景尤其重要。

### Command Execution 的风险

Coding Agent 需要 shell：

```text
pytest
npm test
git diff
```

但 shell 也是高风险 Tool。

必须结合：

```text
Permission
Sandbox
Network Policy
Timeout
Output Offloading
```

例如不允许测试脚本：

```text
访问 production DB
```

### Rollback / Delivery

交付前至少保留：

```text
base commit
final diff
test evidence
run trace
artifact / patch id
```

如果上线后有问题：

```text
能定位这次 Agent 修改
→ revert / rollback
```

这也是 Agent Trace 与普通开发审计连接的地方。

## 产物不是一个随时可用的字符串路径

文件报告至少有输入清单版本、读取证据、草稿产物和引用清单。产物引用应携带归属、版本/摘要、保留策略与授权范围；使用时重新检查可访问性，不把缓存的路径当成永久许可。

环境回收、工作区被修改或文件已删除时，Run仍可能存在。恢复必须验证引用是否可解析和内容是否仍对应旧证据；不成立则重建或明确阻塞，不能把空文件当成成功恢复。执行环境、模型服务、数据库和外部系统是不同资源，不要求同一进程或相同持久性。

## 本章自测

<details>
<summary>只有受控 API 工具的 Agent 必须配代码沙箱吗？</summary>

不必须。没有任意代码执行需求时，不应为凑组件增加执行环境；API 仍需自身授权与隔离。

</details>

<details>
<summary>模型和数据库在 L4 是否意味着它们是次要的？</summary>

不意味着。分层表达能力与事实的提供关系，不对重要性排序。

</details>

<!-- enrichment: scenario-checks -->
<details>
<summary>Checkpoint里的artifact路径存在就能复用吗？</summary>

还需核对身份、版本/摘要、有效期与可访问性；同一路径可能已经指向新内容。

</details>

<details>
<summary>运行状态存在而沙箱已回收，意味着无法恢复吗？</summary>

取决于持久状态与产物是否足以重建；重新验证环境、引用和未知副作用后决定继续或阻塞。

</details>

[本章面试练习与具体追问](../interview/README.md#chapter-13) · [综合复习](../review/README.md)

## 回到主线

现在应能独立说明：资源所有权、环境生命周期与隔离方式。下一章：[横切治理：身份、权限、审批与安全](14-IdentityPermissionsAndSafety.md)。

资料核对入口：[官方资料](../../roadmap/agent-authoritative-sources.md) · [源码索引](../../research/agent-sources/README.md)。四层归位与工作定义是教材抽象，产品 API、默认行为与源码路径以标注版本为准。

[← 12](12-KnowledgeAndCapabilityAccess.md) · [Agent 主线](../README.md) · [14 →](14-IdentityPermissionsAndSafety.md)
