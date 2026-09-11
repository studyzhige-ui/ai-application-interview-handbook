# 17｜Lua / Redis Functions 与服务器端原子逻辑

当一个业务动作需要多个 Redis 操作，而且：

- 不希望客户端来回多次；
- 需要“读 → 判断 → 写”在服务器内连续完成；
- 不想依赖 WATCH 的高冲突重试；

Lua Script / Redis Functions 就很重要。

---

## 1. 为什么服务器端脚本有价值

假设库存：

```text
stock = 5
```

需求：

```text
如果 stock > 0
→ stock - 1
→ 返回成功
否则失败
```

客户端写法：

```text
GET stock
if stock > 0:
    DECR stock
```

中间存在 Race Window。

Lua 可以把：

```text
read
→ condition
→ write
```

放到 Redis 服务器端一次执行。

---

# 2. EVAL 的基本模型

示意：

```lua
local stock = tonumber(redis.call('GET', KEYS[1]) or '0')
if stock <= 0 then
    return 0
end
redis.call('DECR', KEYS[1])
return 1
```

调用：

```text
EVAL script 1 stock:item:1
```

重要约定：

```text
KEYS[] → Key
ARGV[] → 普通参数
```

不要在脚本里动态拼出一堆 Redis 无法提前知道的 Key，特别是在 Cluster 场景。

---

# 3. Lua 为什么能保证原子执行

Redis 执行 Script 时，脚本作为一个服务器端执行单元运行。

在脚本结束前，其他普通客户端命令不会插到脚本中间。

所以：

```text
GET
判断
SET/DEL
```

能形成一个原子业务片段。

这也是经典分布式锁安全释放常用 Lua 的原因：

```text
if GET lock == my_token
then DEL lock
```

必须把“比较”和“删除”绑定在一起。

---

# 4. 原子性也是风险

如果脚本执行：

```text
5 seconds
```

因为不能被其它普通命令插入：

```text
其它客户端也要等 5 seconds
```

所以 Lua 原则：

> **短、小、确定、有限。**

不要把复杂业务服务写进 Redis Script。

---

# 5. Lua 和 Transaction / WATCH 怎么选

## WATCH + MULTI / EXEC

适合：

- 客户端需要先读值；
- 冲突率低；
- 乐观重试可接受。

## Lua / Function

适合：

- 多步骤逻辑可以在 Redis 内完成；
- 希望一次网络往返；
- 需要服务器端原子 read-modify-write；
- 避免高冲突 WATCH Retry。

---

# 6. Lua 和 Pipeline 怎么区分

```text
Pipeline
→ 减少 RTT
→ 不自动提供业务原子性

Lua
→ 服务器端执行逻辑
→ 提供脚本执行原子边界
```

两者目的不同。

---

# 7. Redis Functions 是什么

现代 Redis 还提供 Redis Functions：

```text
把服务器端逻辑注册/管理在 Redis 中
```

相比每次 `EVAL` 发送脚本文本，更适合：

- 可管理；
- 可复用；
- 版本化服务器端逻辑。

但工程上要谨慎：

> Redis 不是通用 Application Server。

Script / Function 应聚焦于数据附近的短原子操作。

---

# 8. Cluster 下的脚本 Key 约束

Lua 操作多个 Key 时，Cluster 通常要求：

```text
Keys in same hash slot
```

例如：

```text
rate:{user1}:count
rate:{user1}:meta
```

共同 `{user1}` Hash Tag 可以让它们同 Slot。

否则一个 Script 无法跨多个 Cluster Node 保持单节点原子执行。

---

# 9. 脚本里的 Determinism 与 Replication

Script 会改变 Dataset 时，Redis 需要把结果可靠同步到 Replica / Persistence 路径。

从应用角度最重要的是：

- 不要依赖外部网络；
- 不要做不可控长计算；
- Key 显式传入；
- 设计可预测执行时间。

---

# 10. AI Application 场景

## Rate Limit

一个 Lua Script：

```text
清理窗口外 ZSet member
→ ZCARD
→ 判断限额
→ ZADD 当前请求
→ 更新 TTL
```

可以原子完成。

## Lock Release

```text
GET token
→ 比较 owner
→ DEL
```

必须原子。

## Quota

```text
读取剩余额度
→ 判断足够
→ 扣减
```

如果额度只是 Redis 临时计数，可用 Lua；如果涉及最终账单 Source of Truth，则需要 MySQL/业务事务边界。

---

# 11. 面试怎么答

## Q：Redis Lua 为什么常用于分布式锁释放？

🎯 **建议回答：**

> 因为释放锁不能简单 DEL，必须先确认当前锁 Value 仍然是自己的 owner token，再删除。GET + 比较 + DEL 如果分成多条命令存在 Race；Lua 可以把比较和删除作为一个服务器端原子执行单元。

## Q：Lua 和 WATCH 有什么区别？

> WATCH 是客户端乐观锁，有冲突时 EXEC abort 并重试；Lua 把逻辑搬到 Redis 服务器一次原子执行，减少 RTT 和冲突窗口，但脚本过长会阻塞主执行路径。

---

# 12. 高频易错点

⚠️ **Lua 可以写任意复杂业务，因为很快。**  
错误，长脚本会阻塞其它请求。

⚠️ **Lua = Transaction Rollback。**  
不是传统数据库事务。

⚠️ **Lua 可以随便跨 Cluster Node 操作 Key。**  
通常需要同 Slot。

⚠️ **服务器端脚本越多架构越高级。**  
应只放短原子数据逻辑。

---

# 13. 本章自测

<details>
<summary>1. 为什么 GET token 后再单独 DEL lock 不安全？</summary>

两条命令之间锁可能过期并被其他客户端重新获得，旧客户端随后 DEL 会误删新锁。比较和删除必须原子。

</details>

<details>
<summary>2. Lua 最大的性能风险是什么？</summary>

脚本在原子执行期间占用 Redis 主要命令执行路径，长脚本会让其它客户端等待。

</details>

<details>
<summary>3. Redis Functions 是否意味着可以把应用业务层搬进 Redis？</summary>

不应该。Functions 更适合可复用的短服务器端数据逻辑，Redis 仍不是通用 Application Server。

</details>
