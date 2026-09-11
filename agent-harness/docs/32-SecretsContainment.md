# 32｜Secrets、Data Exfiltration 与 Containment

## 1. Security 的另一半：Blast Radius

不能只问“模型会不会犯错”，还要问：

> 如果犯错，一次最多能造成多大损失？

Anthropic containment 文章强调的就是这个工程问题。

## 2. Secret 不应直接进入 Context

优先：

```text
Tool executes with credential
Model sees logical result
```

而不是：

```text
API_KEY=xxx → prompt
```

模型不需要知道真实 secret。

## 3. Credential Scoping

```text
per tenant
per tool
per environment
short-lived token
least privilege
```

避免一个万能 Token 贯穿所有 Tool。

## 4. Egress Control

即使 filesystem read-only，如果 Agent 能访问 secret + 任意网络，仍可外传。

所以 containment 要组合：

```text
read boundary
network egress
secret broker
approval
logging / redaction
```

## 5. Trace 的敏感数据

Trace 很重要，但不能把 secret、PII、完整客户数据无脑记录。Observability 本身也有数据治理边界。

## 🎯 面试

我会把 Agent 安全目标从“防止错误”扩展到“限制 blast radius”：Secret 由 Tool/credential broker 使用而不是塞 Context，凭证按 tenant/tool/env 最小化并尽量短期，同时限制 network egress 和 workspace，Trace 做 redaction。

<details><summary>自测：为什么把 API Key 放环境变量仍不一定安全？</summary>

如果 Agent 可执行任意 shell 并读取环境变量，它仍可能打印或外传。需要执行环境和 secret exposure 的进一步限制。
</details>
