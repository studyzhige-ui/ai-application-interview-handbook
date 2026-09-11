# 29｜Sandbox 与 Execution Environment

## 1. Permission 不是隔离

Prompt 和 permission check 都可能出错。Sandbox 是最后的执行边界：

```text
Agent says execute
Permission says yes
Sandbox still limits filesystem / network / process
```

## 2. Codex 的实现信号

Codex 固定源码的 `SandboxPolicy` 明确表达 read-only、workspace-write、external sandbox、full access 等模式，并把 writable roots / network access 作为策略的一部分。

## 3. Sandbox 维度

```text
Filesystem read roots
Filesystem write roots
Network egress
Process / syscall
CPU / memory / time
Environment variables
Credentials
```

## 4. Workspace Isolation

多租户 / Multi-Agent 中：

```text
run A workspace
!= run B workspace
```

否则一个 Agent 可能读到另一个用户临时文件或 Git 状态。

## 5. Sandbox 不等于 VM

可以用 container、OS sandbox、namespace、remote execution 等。关键是 policy/enforcement boundary，不是技术名词。

## 6. 安全与自主性的关系

Anthropic 的 sandboxing 工程文章指出，明确 filesystem/network 边界后，可以减少一些逐次 permission prompt。好的隔离不是让 Agent 更弱，而是让安全范围内的自主执行更顺畅。

## 🎯 面试

Permission 决定“该不该做”，Sandbox 决定“最多能做到哪里”。我会至少限制 filesystem、network、process、resource 和 credential，并做 per-run/tenant workspace isolation；高风险系统不应只依赖 Prompt 自律。

<details><summary>自测：read-only sandbox 是否绝对安全？</summary>

不是。仍可能读取 secret 并通过允许的网络外传，所以还要考虑 network、credentials、data exfiltration。
</details>
