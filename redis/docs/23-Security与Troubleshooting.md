# 23｜Security、Latency 与 Production Troubleshooting

学到这里，Redis 已经不只是“会用命令”。

生产环境真正危险的问题通常是：

```text
连不上
延迟突然高
内存暴涨
Key 被误删
权限泄漏
Failover 抖动
BigKey 卡住
```

这一章建立最基本的生产排查框架。

---

## 1. Redis 安全的第一原则

Redis 不应该裸奔在不可信网络上。

至少要考虑：

- Network Isolation；
- ACL / Authentication；
- TLS；
- Least Privilege；
- Secret 管理；
- 危险命令控制；
- Audit / Access Log；
- 备份与恢复权限。

不要把：

```text
requirepass / password
```

当成全部安全模型。

---

# 2. ACL 比“一个全局密码”更成熟

Redis 支持用户和 ACL 权限模型。

不同服务可以只允许：

```text
GET / SET 某些 Key Prefix
```

而不是都拥有：

```text
FLUSHALL
CONFIG
DEBUG
```

最小权限可以降低：

- 误操作；
- 横向移动；
- Secret 泄漏后的爆炸半径。

---

# 3. TLS 解决什么

应用到 Redis 的流量可能包含：

- Session；
- User ID；
- Token；
- Business State。

跨不可信网络时要考虑 TLS。

Redis 官方也支持 Replication、Cluster Bus、Sentinel 相关 TLS 配置。

但 TLS 会增加：

```text
CPU / Handshake / 运维复杂度
```

仍然是安全需求驱动。

---

# 4. Key 里不要直接放敏感 Secret

例如：

```text
session:<raw_access_token>
```

Key 可能出现在：

- Metrics；
- Slowlog；
- Debug；
- 运维命令；
- Dump。

更稳：

```text
session:<opaque_id_or_hash>
```

真正 Secret 放受控 Value 或专门 Secret Store。

---

# 5. Redis 延迟排查先分层

出现 P99 高，不要第一句就说：

> “Redis 单线程瓶颈了。”

先拆：

```text
Client Queueing
Network RTT
Connection Pool
Redis Server CPU
Slow Command
BigKey
Fork / COW
Disk / AOF
Eviction / Expiration
Replica / Failover
OS / Swap
```

---

# 6. Slow Command 怎么查

常见工具/思路：

- `SLOWLOG`；
- `LATENCY` 相关监控；
- Command latency metrics；
- Client-side Trace；
- Key Size；
- CPU / Network。

`SLOWLOG` 主要记录命令执行耗时，网络等待不一定在里面。

所以：

```text
Client 看到 500ms
SLOWLOG 只有 2ms
```

说明可能问题在：

```text
网络 / 排队 / 连接池 / 客户端
```

---

# 7. CPU 高怎么分析

候选：

- 高频 Command；
- O(N) Command；
- HotKey；
- Lua Script；
- Expiration Pressure；
- Serialization / Network Handling；
- Cluster Migration。

不要只做：

```text
加 CPU
```

因为单实例核心执行路径不会自动线性利用所有 Core。

---

# 8. 内存高怎么分析

先问：

```text
Key 数量增多？
Value 变大？
BigKey？
TTL 没设？
Eviction 不工作？
Fragmentation？
Fork/COW Peak？
```

工具思路：

```text
INFO memory
MEMORY USAGE
bigkeys / memkeys analysis
```

同时检查业务 Key Schema。

---

# 9. Connection Pool Exhaustion

AI 服务常见：

```text
1000 async requests
→ 每个都要 Redis
```

如果连接池太小：

```text
请求排队等连接
```

Redis 服务器可能很空，但应用 P99 很高。

如果连接池太大：

```text
大量连接
→ Redis / OS / TLS / Client 都有额外压力
```

所以连接池必须根据：

```text
Concurrency
Command Latency
Timeout
QPS
```

设计。

---

# 10. Timeout 不能无限长

Redis 短暂卡住时，如果客户端 Timeout 很长：

```text
大量请求挂起
→ Connection 占满
→ Thread/Coroutine 堆积
→ 上游继续进流量
```

形成级联故障。

所以需要：

- Connect Timeout；
- Command Timeout；
- Retry Budget；
- Circuit Breaker；
- Pool Timeout。

通用 Resilience Primary 在 Backend Engineering。

---

# 11. Retry 也可能放大事故

Redis 超时：

```text
1000 requests
```

每个立即重试 3 次：

```text
瞬间变 3000 requests
```

这就是 Retry Storm。

应该：

```text
Backoff
Jitter
Retry Budget
Only retry safe operations
```

尤其写操作要考虑：

```text
请求可能已经执行成功，但 Reply 丢了
```

不能盲目重复副作用。

---

# 12. Failover 时应用会看到什么

可能出现：

- Connection reset；
- Read/Write error；
- MOVED / ASK；
- 短暂 timeout；
- Stale Read；
- 最近写丢失窗口。

成熟客户端要：

- Sentinel / Cluster aware；
- 自动重新发现；
- 有明确 Retry Policy。

但自动重连不等于业务正确。

---

# 13. AI 系统里 Redis 故障如何降级

## Cache

```text
回源 DB + 限流
```

## Session

```text
短暂拒绝 / Token fallback
```

## Rate Limit

```text
Fail-open / Fail-closed
```

## Agent State

```text
通常暂停执行比继续双跑更安全
```

## Semantic Cache

```text
直接绕过 Cache 调 LLM
```

不同 Namespace 必须有不同 Degrade Policy。

---

# 14. 面试怎么答

## Q：Redis 突然变慢怎么排查？

🎯 **建议回答：**

> 我会先区分客户端、网络和 Redis Server。先看应用连接池等待和 RTT，再看 Redis CPU、SLOWLOG/latency、BigKey/HotKey、O(N) 命令、Lua；同时排查 RDB/AOF fork、COW、磁盘 I/O、Expiration/Eviction、Swap 和 Failover。不能只看到“Redis 单线程”就直接下结论。

## Q：Redis 安全怎么做？

> 先网络隔离，再用 ACL 最小权限、Authentication、TLS、Secret 管理和危险命令控制。Key/Value 里的敏感数据也要考虑日志和运维可见性，多租户应用不能只依赖 Key 前缀做授权。

---

# 15. 本章自测

<details>
<summary>1. 为什么客户端看到 500ms、SLOWLOG 只有 2ms 并不矛盾？</summary>

SLOWLOG 更偏服务器命令执行时间；额外延迟可能发生在连接池等待、网络、客户端排队或重试。

</details>

<details>
<summary>2. 为什么 Redis 故障时 Retry 可能让事故更严重？</summary>

大量请求同步立即重试会放大 QPS，形成 Retry Storm；写操作还可能因 Reply 丢失而重复执行。

</details>

<details>
<summary>3. 为什么不同 Redis Key Namespace 应有不同降级策略？</summary>

Cache、Session、Rate Limit、Agent Lease 的业务安全要求不同，Redis 不可用时允许的行为也不同。

</details>
