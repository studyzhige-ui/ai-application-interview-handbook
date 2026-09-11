# 25. Redis 实现 Rate Limit

Rate Limit 的**算法选择**属于 AI Backend Engineering；这一章只回答 Redis-specific 问题：

> **如果已经决定使用 Fixed Window / Sliding Window / Token Bucket，Redis 里具体怎样安全实现？**

---

## 1. Fixed Window Counter

最简单：

```text
rate:{user}:{minute}
```

每次：

```text
INCR key
EXPIRE key 60
```

如果 Counter 超过限制：

```text
reject
```

优点：

- 简单；
- 内存低；
- 吞吐高。

缺点：

```text
窗口边界突刺
```

例如：

```text
12:00:59 → 100 requests
12:01:00 → 100 requests
```

两秒内可能放过 200 个。

---

# 2. INCR + EXPIRE 为什么要考虑原子性

错误流程：

```text
INCR key
# process crashes
EXPIRE key 60
```

如果第一次创建后没设 TTL：

```text
Counter 永不过期
```

所以可以：

- Lua 一次完成；
- Transaction；
- 或使用客户端/命令模式确保初始化与 TTL 正确绑定。

重点是：

> 多命令业务规则不能因为“每条命令原子”就自动整体原子。

---

# 3. Sliding Window Log + ZSet

Key：

```text
rate:{user}
```

每次请求：

```text
1. ZREMRANGEBYSCORE 删除窗口外请求
2. ZCARD 统计窗口内数量
3. 如果未超限 → ZADD 当前请求
4. EXPIRE
```

Score：

```text
timestamp
```

Member：

```text
request_id
```

优点：

```text
真正按滑动时间窗口统计
```

缺点：

```text
每个请求都要留一条记录
内存更大
命令更复杂
```

---

# 4. 为什么 Sliding Window 通常用 Lua

四个步骤如果分开：

```text
remove old
count
check
add
```

多个请求并发时可能同时看到：

```text
count = 99
```

然后都放行，超过 100。

Lua 可以把整个判断和写入作为一个服务器端原子逻辑。

---

# 5. Token Bucket 的 Redis 思路

Bucket State：

```text
tokens
last_refill_time
```

每次请求：

```text
now
→ 根据 elapsed 补 Token
→ 判断 tokens >= cost
→ 扣减
→ 保存新状态
```

也是典型：

```text
read
calculate
write
```

因此常用 Lua/Function 保证原子。

---

# 6. Key 粒度就是限流维度

按用户：

```text
rate:user:{user_id}
```

按租户：

```text
rate:tenant:{tenant_id}
```

按 API：

```text
rate:{tenant}:{endpoint}
```

按模型：

```text
rate:{tenant}:model:{model}
```

多维组合会带来更多 Key 和内存，所以要从业务 Policy 设计，而不是先写 Redis。

---

# 7. Distributed Rate Limit 的好处

多实例 API：

```text
API-1
API-2
API-3
```

如果每台机器本地 Counter：

```text
每台都允许 100 QPS
→ 总共可能 300 QPS
```

共享 Redis：

```text
所有实例竞争同一个 Counter / Bucket
```

就能形成全局视角。

---

# 8. Redis 挂了：Fail-open 还是 Fail-closed

这是面试 L4 的关键。

## Fail-open

Redis 不可用：

```text
继续允许请求
```

适合：

```text
普通非关键接口
```

风险：

```text
流量失控
```

## Fail-closed

Redis 不可用：

```text
拒绝请求
```

适合：

```text
安全/额度边界很重要
```

风险：

```text
Redis 故障 = 服务大面积不可用
```

所以需要按限流类型决定。

---

# 9. Rate Limit Key 本身可能变 HotKey

如果所有请求都更新：

```text
rate:global
```

这个 Key 会成为超级 HotKey。

治理：

- 按租户/用户分片；
- 本地预限流 + Redis 全局限流；
- Batch Token Allocation；
- 多层 Rate Limit。

所以“用 Redis 做限流”也要考虑 Redis 自己的瓶颈。

---

# 10. AI Provider Rate Limit

AI Backend 常有：

```text
OpenAI provider quota
Anthropic provider quota
tenant token budget
model RPM / TPM
```

可以把 Redis 用于：

- Request Count；
- Token Count；
- Burst Control；
- Tenant Fairness 辅助状态。

但真正：

```text
Priority
Fair Queue
Global Scheduling
```

属于 Backend Engineering，不应该硬塞成 Redis 特性。

---

# 11. 面试怎么答

## Q：Redis 如何实现 Sliding Window Rate Limit？

🎯 **建议回答：**

> 常用 ZSet，把时间戳作为 Score、唯一 Request ID 作为 Member。请求到来时原子地删除窗口外 Member、统计 ZCARD、判断是否超过限制，未超过则加入当前请求并设置 TTL。因为多步骤并发会有 Race，通常用 Lua/Function 在 Redis 服务器端原子执行。

## Q：Redis 做限流挂了怎么办？

> 需要提前定义 Fail-open 或 Fail-closed。普通流量保护可能选择短暂 Fail-open 并用本地限流兜底；额度、安全等关键边界可能 Fail-closed。不能把 Redis 故障策略留到事故现场再决定。

---

# 12. 本章自测

<details>
<summary>1. Fixed Window 最大缺点是什么？</summary>

窗口边界可能出现突刺：前一个窗口末尾和下一个窗口开头都各放满额度，短时间内实际通过两倍流量。

</details>

<details>
<summary>2. 为什么 Sliding Window 的多个 ZSet 命令适合用 Lua？</summary>

需要把清理、计数、判断、写入绑定成一个原子操作，否则并发请求可能同时看到未超限并一起放行。

</details>

<details>
<summary>3. 为什么全局 Rate Limit Key 可能反过来成为 Redis 瓶颈？</summary>

所有实例和请求都访问同一个 Key，会形成 HotKey，使单个 Redis Node / Slot 承受集中流量。

</details>
