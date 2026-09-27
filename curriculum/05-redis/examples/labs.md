# Redis 实验室｜理解机制后再运行

[← Redis 首页](../README.md) · [准备隔离实例](README.md)

这里承接正文中的连续命令和较长脚本。**它不是另一条必须先完成的学习路线。** 每组都有对应章节，先读清机制、预测结果，再运行所需实验。不要求先学习某种应用语言，也不要求一次跑完所有命令。

以下预期是 Redis 8.10.2、RESP2 下的检查目标，尚不能因列在这里就称为实测结果。redis-cli、Java 或其他客户端对回复的包装可以不同，但返回的类型与含义应相符。

所有键以 lab: 开头，只在本人拥有、可丢弃的独立实例执行。不要把这些操作发向未知服务，也不要用清空整库来替代正确的实验隔离。重复执行前检查初始数据；命令组之间如有依赖，会在对应位置说明。

## 按问题进入

- [观察基本读写和五种类型](#lab-data-types)：第 02 章对应实验。
- [核对覆盖、原地修改和过期](#lab-lifetime)：第 03 章对应实验。
- [紧凑状态与近似统计](#lab-encoding-extra)：第 08 章对应实验。
- [区分缓存未命中、空值和不存在](#lab-cache)：第 04 章对应实验。
- [事务执行与条件修改](#lab-scripts)：第 09 章对应实验。
- [归属检查与安全释放](#lab-locks)：第 13 章对应实验。
- [事件保留、交付与确认](#lab-messages)：第 14 章对应实验。
- [共享会话与最近消息窗口](#lab-state)：第 16 章对应实验。
- [固定与滑动窗口的短脚本](#lab-limits)：第 15 章对应实验。
- [观察快照恢复](#lab-recovery)：第 10 章对应实验。

<a id="lab-data-types"></a>

## 观察基本读写和五种类型

[回到第 02 章](../docs/02-键与常用数据类型.md)

本组从最小读写进入整值、字段和集合。先预测每条回复，再运行；尤其区分新增数量、读取内容、删除结果和类型错误。例子使用不同键名，在新的隔离实例中按顺序执行。

### 连接、写入与读取

<!-- redis-lab: first_commands -->
```redis
PING
SET lab:greeting hello
GET lab:greeting
EXISTS lab:greeting
```
<!-- redis-expect: ["PONG", "OK", "hello", 1] -->

<details>
<summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "PONG" |
| 2 | "OK" |
| 3 | "hello" |
| 4 | 1 |

</details>

### 空字符串与缺失值

<!-- redis-lab: key_types -->
```redis
SET lab:c02:visits 10
TYPE lab:c02:visits
INCR lab:c02:visits
GET lab:c02:visits
STRLEN lab:c02:visits
```
<!-- redis-expect: ["OK", "string", 11, "11", 2] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "OK" |
| 2 | "string" |
| 3 | 11 |
| 4 | "11" |
| 5 | 2 |

</details>

### 故意使用错误类型的命令

<!-- redis-lab: wrong_type -->
```redis
SET lab:c02:title hello
HGET lab:c02:title name
GET lab:c02:title
```
<!-- redis-expect: ["OK", {"error": "WRONGTYPE"}, "hello"] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "OK" |
| 2 | 错误：WRONGTYPE |
| 3 | "hello" |

</details>

### 整值与计数

<!-- redis-lab: string_ops -->
```redis
SET lab:c03:text hello
APPEND lab:c03:text world
GET lab:c03:text
SET lab:c03:count 10
INCRBY lab:c03:count 3
DECR lab:c03:count
MGET lab:c03:count lab:c03:absent
```
<!-- redis-expect: ["OK", 10, "helloworld", "OK", 13, 12, ["12", null]] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "OK" |
| 2 | 10 |
| 3 | "helloworld" |
| 4 | "OK" |
| 5 | 13 |
| 6 | 12 |
| 7 | ["12"；空回复（nil）] |

</details>

### 字段增加、修改和删除

<!-- redis-lab: hash_ops -->
```redis
HSET lab:c03:user name Alice points 10
HGET lab:c03:user name
HSET lab:c03:user points 12
HINCRBY lab:c03:user points 3
HMGET lab:c03:user name points absent
HLEN lab:c03:user
HEXISTS lab:c03:user points
HDEL lab:c03:user points
HGET lab:c03:user points
```
<!-- redis-expect: [2, "Alice", 0, 15, ["Alice", "15", null], 2, 1, 1, null] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | 2 |
| 2 | "Alice" |
| 3 | 0 |
| 4 | 15 |
| 5 | ["Alice"；"15"；空回复（nil）] |
| 6 | 2 |
| 7 | 1 |
| 8 | 1 |
| 9 | 空回复（nil） |

</details>

### 字段视图与返回顺序

<!-- redis-lab: hash_views -->
```redis
HSET lab:c03:views name Alice points 15
HGETALL lab:c03:views
HKEYS lab:c03:views
HVALS lab:c03:views
```
<!-- redis-expect: [2, {"pairs": {"name": "Alice", "points": "15"}}, {"set": ["name", "points"]}, {"set": ["Alice", "15"]}] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | 2 |
| 2 | 字段对应关系：{"name": "Alice", "points": "15"}；顺序不固定 |
| 3 | 成员：["name", "points"]；顺序不固定 |
| 4 | 成员：["Alice", "15"]；顺序不固定 |

</details>

### 两端操作、读取和裁剪

<!-- redis-lab: list_ops -->
```redis
RPUSH lab:c03:messages m1 m2 m3
LRANGE lab:c03:messages 0 -1
LINDEX lab:c03:messages 1
LPOP lab:c03:messages
LPUSH lab:c03:messages m0
LTRIM lab:c03:messages 0 1
LLEN lab:c03:messages
LRANGE lab:c03:messages 0 -1
```
<!-- redis-expect: [3, ["m1", "m2", "m3"], "m2", "m1", 3, "OK", 2, ["m0", "m2"]] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | 3 |
| 2 | ["m1"；"m2"；"m3"] |
| 3 | "m2" |
| 4 | "m1" |
| 5 | 3 |
| 6 | "OK" |
| 7 | 2 |
| 8 | ["m0"；"m2"] |

</details>

### 成员和重复加入

<!-- redis-lab: set_ops -->
```redis
SADD lab:c03:seen alice bob alice
SCARD lab:c03:seen
SISMEMBER lab:c03:seen alice
SREM lab:c03:seen bob
SADD lab:c03:editors alice carol
SINTER lab:c03:seen lab:c03:editors
SMEMBERS lab:c03:seen
```
<!-- redis-expect: [2, 2, 1, 1, 2, {"set": ["alice"]}, {"set": ["alice"]}] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | 2 |
| 2 | 2 |
| 3 | 1 |
| 4 | 1 |
| 5 | 2 |
| 6 | 成员：["alice"]；顺序不固定 |
| 7 | 成员：["alice"]；顺序不固定 |

</details>

### 分数、排名与范围

<!-- redis-lab: zset_ops -->
```redis
ZADD lab:c03:rank 10 alice 20 bob
ZINCRBY lab:c03:rank 15 alice
ZSCORE lab:c03:rank alice
ZRANGE lab:c03:rank 0 1 REV WITHSCORES
ZRANK lab:c03:rank bob
ZCARD lab:c03:rank
ZREM lab:c03:rank bob
```
<!-- redis-expect: [2, "25", "25", ["alice", "25", "bob", "20"], 0, 2, 1] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | 2 |
| 2 | "25" |
| 3 | "25" |
| 4 | ["alice"；"25"；"bob"；"20"] |
| 5 | 0 |
| 6 | 2 |
| 7 | 1 |

</details>

<a id="lab-lifetime"></a>

## 核对覆盖、原地修改和过期

[回到第 03 章](../docs/03-过期与内存淘汰.md)

先完成基本类型，再检查 SET、INCR、HSET 对期限的影响。带期限的数值会随时间下降，预期范围只适用于及时连续执行；停留很久后应重新初始化这一组。HEXPIRE 需要 Redis 7.4 及以后。

### 哪些写入保留键级 TTL

<!-- redis-lab: ttl_changes -->
```redis
SET lab:c07:value hello EX 600
TTL lab:c07:value
SET lab:c07:value world
TTL lab:c07:value
EXPIRE lab:c07:value 600
SET lab:c07:value newer KEEPTTL
PTTL lab:c07:value
PERSIST lab:c07:value
TTL lab:c07:value
```
<!-- redis-expect: ["OK", {"between": [1, 600]}, "OK", -1, 1, "OK", {"between": [1, 600000]}, 1, -1] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "OK" |
| 2 | 在 1–600 之间（随时间变化） |
| 3 | "OK" |
| 4 | -1 |
| 5 | 1 |
| 6 | "OK" |
| 7 | 在 1–600000 之间（随时间变化） |
| 8 | 1 |
| 9 | -1 |

</details>

### 字段期限与键期限

<!-- redis-lab: hash_field_expiry -->
```redis
HSET lab:field-expiry name Alice code 1234
HEXPIRE lab:field-expiry 60 FIELDS 1 code
HTTL lab:field-expiry FIELDS 2 name code
TTL lab:field-expiry
```
<!-- redis-expect: [2, [1], [-1, {"between": [50, 60]}], -1] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | 2 |
| 2 | [1] |
| 3 | [-1；在 50–60 之间（随时间变化）] |
| 4 | -1 |

</details>

<a id="lab-encoding-extra"></a>

## 紧凑状态与近似统计

[回到第 08 章](../docs/08-内部编码与数据规模.md)

用小编号观察 Bitmap，用少量成员观察 HyperLogLog。小例子的输出不能证明 HLL 对任意规模都精确；其业务用途是估算基数。

### 一 个位置对应一个标记

<!-- redis-lab: bitmap_ops -->
```redis
SETBIT lab:c04:attendance 2 1
SETBIT lab:c04:attendance 5 1
SETBIT lab:c04:attendance 2 1
GETBIT lab:c04:attendance 2
GETBIT lab:c04:attendance 3
BITCOUNT lab:c04:attendance
TYPE lab:c04:attendance
```
<!-- redis-expect: [0, 0, 1, 1, 0, 2, "string"] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | 0 |
| 2 | 0 |
| 3 | 1 |
| 4 | 1 |
| 5 | 0 |
| 6 | 2 |
| 7 | "string" |

</details>

### 近似唯一数

<!-- redis-lab: hll_ops -->
```redis
PFADD lab:c04:visitors alice bob alice
PFCOUNT lab:c04:visitors
```
<!-- redis-expect: [1, 2] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | 1 |
| 2 | 2 |

</details>

### 只有任务需要时再看的表示方式

Bitmap 解决每个位置的布尔标记，BITFIELD 则将连续位段解释为指定宽度的小整数，用于确实需要紧凑计数的场景。两者都要控制位置与范围，否则一个巨大偏移就可能产生很大的 String。[BITFIELD](https://redis.io/docs/latest/commands/bitfield/)

Geo 命令面向经纬度附近查询。位置写入、距离和范围查询有自己的单位与边界，不把排序分数直接当经纬度使用。[Geo 文档](https://redis.io/docs/latest/develop/data-types/geospatial/)

8.10.2 配置中也有共享 Hash 字段模板的内存优化，默认不自动转换。它适合特定字段布局，不是学会 Hash 的必要步骤；研究大量同构对象的内存时，再核对版本、配置和编码。[固定版本 redis.conf](https://github.com/redis/redis/blob/8.10.2/redis.conf)

<a id="lab-cache"></a>

## 区分缓存未命中、空值和不存在

[回到第 04 章](../docs/04-缓存读取与更新.md)

缓存身份和状态必须有明确约定。这里的 EMPTY 只是约定的演示文字，不是 Redis 自带的特殊对象，正式应用不能让它与正常业务值冲突。

### 负缓存的状态区分

<!-- redis-lab: cache_values -->
```redis
SET lab:c09:note:42 '{"found":true,"title":"Guide","version":1}' EX 60
GET lab:c09:note:42
SET lab:c09:note:99 '{"found":false}' EX 10
GET lab:c09:note:99
```
<!-- redis-expect: ["OK", "{\"found\":true,\"title\":\"Guide\",\"version\":1}", "OK", "{\"found\":false}"] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "OK" |
| 2 | "{\"found\":true,\"title\":\"Guide\",\"version\":1}" |
| 3 | "OK" |
| 4 | "{\"found\":false}" |

</details>

<a id="lab-scripts"></a>

## 事务执行与条件修改

[回到第 09 章](../docs/09-事务与服务端逻辑.md)

事务先返回 QUEUED，EXEC 才返回各条执行结果。运行时错误示例故意让中间操作失败，用之后的读取确认哪些修改仍存在。Lua 把检查与扣减组合，不访问外部业务数据库。

### 连续执行一组命令

<!-- redis-lab: transaction_ok -->
```redis
MULTI
SET lab:c15:a one
SET lab:c15:b two
GET lab:c15:a
EXEC
```
<!-- redis-expect: ["OK", "QUEUED", "QUEUED", "QUEUED", ["OK", "OK", "one"]] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "OK" |
| 2 | "QUEUED" |
| 3 | "QUEUED" |
| 4 | "QUEUED" |
| 5 | ["OK"；"OK"；"one"] |

</details>

### 运行错误不会通用回滚

<!-- redis-lab: transaction_error -->
```redis
SET lab:c15:number 10
MULTI
SET lab:c15:before saved
LPUSH lab:c15:number x
SET lab:c15:after saved
EXEC
GET lab:c15:before
GET lab:c15:after
```
<!-- redis-expect: ["OK", "OK", "QUEUED", "QUEUED", "QUEUED", ["OK", {"error": "WRONGTYPE"}, "OK"], "saved", "saved"] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "OK" |
| 2 | "OK" |
| 3 | "QUEUED" |
| 4 | "QUEUED" |
| 5 | "QUEUED" |
| 6 | ["OK"；错误：WRONGTYPE；"OK"] |
| 7 | "saved" |
| 8 | "saved" |

</details>

### decrease 脚本

条件扣减：先确保请求数量和库存可解释，再比较是否足够。返回剩余数量；缺失为 -1，不足为 -2，非法数量为错误。

<!-- lua-lab: decrease -->
```lua
local amount = tonumber(ARGV[1])
if not amount or amount < 1 or amount > 1000000 or amount ~= math.floor(amount) then
    return redis.error_reply('invalid amount')
end
local raw = redis.call('GET', KEYS[1])
if not raw then return -1 end
local stock = tonumber(raw)
if not stock or stock < 0 or stock > 1000000 or stock ~= math.floor(stock) then
    return redis.error_reply('invalid stock')
end
if stock < amount then return -2 end
return redis.call('DECRBY', KEYS[1], amount)
```

### 怎样调用 Lua

把对应脚本保存为 `decrease.lua`，在与脚本同一目录的系统终端运行 `redis-cli -p 16379 --eval decrease.lua lab:stock , 3`。逗号分开键与普通参数，不是脚本内容；本例要求先把 lab:stock 初始化为 5。预期剩余 2，再请求扣 3 则返回 -2。

这是针对前述本机学习容器的客户端调用方式。没有对应客户端或端口映射时，使用官方安装入口配置独立环境，不把容器里的路径与宿主路径混用。需要持续管理复用逻辑时，再核对 FUNCTION LOAD 与 FCALL；库部署、持久化和各分片加载均需要自己管理，不能把函数注册当成全服务自动发布。

<a id="lab-locks"></a>

## 归属检查与安全释放

[回到第 13 章](../docs/13-分布式锁.md)

确认不同持有者不能随意删除彼此的记录。DELEX IFEQ 需要 Redis 8.4 及以后；Lua 表达相同的比较再删除。它们只演示释放边界，不证明暂停、切换或下游副作用安全。

### 值相等才删除

<!-- redis-lab: lock_owner -->
```redis
SET lab:c18:lock attempt-a NX PX 600000
SET lab:c18:lock attempt-b NX PX 600000
GET lab:c18:lock
DELEX lab:c18:lock IFEQ attempt-b
DELEX lab:c18:lock IFEQ attempt-a
EXISTS lab:c18:lock
```
<!-- redis-expect: ["OK", null, "attempt-a", 0, 1, 0] -->

<details><summary>核对本组逐条回复</summary>

| 第几条 | 预期回复及含义 |
|---:|---|
| 1 | "OK" |
| 2 | 空回复（nil） |
| 3 | "attempt-a" |
| 4 | 0 |
| 5 | 1 |
| 6 | 0 |

</details>

### release_owner 脚本

安全释放：只有键里的值仍与传入持有者相同时才删除。返回 1 表示删除了键，0 表示没有删除。

<!-- lua-lab: release_owner -->
```lua
if redis.call('GET', KEYS[1]) == ARGV[1] then return redis.call('DEL', KEYS[1]) else return 0 end
```

<a id="lab-messages"></a>

## 事件保留、交付与确认

[回到第 14 章](../docs/14-通知与Streams.md)

必须先执行 stream_records，再执行 stream_group，两组使用同一个 Stream。固定事件 ID 仅用于空白实验实例中复现输出；向已有流重复执行相同 ID 会被拒绝。组已存在时，也不能把再次创建失败误当服务异常。

### 先追加、再读取记录

<!-- redis-lab: stream_records -->
```redis
XADD lab:events 1000-0 kind created task 42
XADD lab:events 1001-0 kind finished task 42
XLEN lab:events
XRANGE lab:events - + COUNT 2
XREAD COUNT 1 STREAMS lab:events 1000-0
```
<!-- redis-expect: ["1000-0", "1001-0", 2, [["1000-0", ["kind", "created", "task", "42"]], ["1001-0", ["kind", "finished", "task", "42"]]], [["lab:events", [["1001-0", ["kind", "finished", "task", "42"]]]]]] -->

### 交付、待确认和 ACK

<!-- redis-lab: stream_group -->
```redis
XGROUP CREATE lab:events workers 0
XREADGROUP GROUP workers alice COUNT 1 STREAMS lab:events >
XPENDING lab:events workers
XACK lab:events workers 1000-0
XPENDING lab:events workers
XLEN lab:events
```
<!-- redis-expect: ["OK", [["lab:events", [["1000-0", ["kind", "created", "task", "42"]]]]], [1, "1000-0", "1000-0", [["alice", "1"]]], 1, [0, null, null, null], 2] -->

<a id="lab-state"></a>

## 共享会话与最近消息窗口

[回到第 16 章](../docs/16-会话与运行状态.md)

这里只保存教学身份与消息，不是真正的认证系统。观察列表加入和裁剪后的内容，不以长度正确代替消息去重或完整历史恢复。

### 保存带期限的会话对象

<!-- redis-lab: session_record -->
```redis
SET lab:session:s1 '{"user":"u1","tenant":"t1","permission_version":3}' EX 600
GET lab:session:s1
TTL lab:session:s1
```
<!-- redis-expect: ["OK", "{\"user\":\"u1\",\"tenant\":\"t1\",\"permission_version\":3}", {"between": [590, 600]}] -->

### 只保留最近窗口

<!-- redis-lab: recent_window -->
```redis
LPUSH lab:recent:u1 m1
LPUSH lab:recent:u1 m2
LPUSH lab:recent:u1 m3
LPUSH lab:recent:u1 m4
LTRIM lab:recent:u1 0 2
LRANGE lab:recent:u1 0 -1
```
<!-- redis-expect: [1, 2, 3, 4, "OK", ["m4", "m3", "m2"]] -->

<a id="lab-limits"></a>

## 固定与滑动窗口的短脚本

[回到第 15 章](../docs/15-共享限流.md)

先用第 15 章时间表算清允许与拒绝，再看脚本。KEYS 传 Redis 键，ARGV 传普通参数，tonumber 将参数文字解释成数值；程序先检查输入再修改。演示的 now_ms 由调用方提供以便复现，生产不能相信不可信客户端随意声明时间。

### fixed_window 脚本

相对固定窗口：第一次成功请求开始一个有期限的窗口，本脚本不是按自然分钟对齐。只记录被接受的请求；返回允许标记、当前计数和剩余毫秒。

<!-- lua-lab: fixed_window -->
```lua
local limit = tonumber(ARGV[1])
local ttl_ms = tonumber(ARGV[2])
if not limit or limit < 1 or limit > 10000 or limit ~= math.floor(limit)
   or not ttl_ms or ttl_ms < 1 or ttl_ms > 60000 or ttl_ms ~= math.floor(ttl_ms) then
    return redis.error_reply('invalid policy')
end
local current = tonumber(redis.call('GET', KEYS[1]) or '0')
if not current or current < 0 or current ~= math.floor(current) then
    return redis.error_reply('invalid counter')
end
if current >= limit then
    return {0, current, redis.call('PTTL', KEYS[1])}
end
local count = redis.call('INCR', KEYS[1])
if count == 1 then
    redis.call('PEXPIRE', KEYS[1], ttl_ms)
end
return {1, count, redis.call('PTTL', KEYS[1])}
```

### sliding_window 脚本

滑动窗口：使用 (now_ms-window_ms, now_ms] 范围，并为同一次演示请求使用稳定标识。返回 1 表示新接受，0 表示拒绝，2 表示同一标识已存在；这是本实验的重试口径，不是所有限流器的固定规则。

<!-- lua-lab: sliding_window -->
```lua
local now = tonumber(ARGV[1])
local window = tonumber(ARGV[2])
local limit = tonumber(ARGV[3])
local member = ARGV[4]
if not now or now < 0 or now > 9000000000000 or now ~= math.floor(now)
   or not window or window < 1 or window > 60000 or window ~= math.floor(window)
   or not limit or limit < 1 or limit > 10000 or limit ~= math.floor(limit)
   or not member or #member < 1 or #member > 128 then
    return redis.error_reply('invalid policy')
end
redis.call('ZREMRANGEBYSCORE', KEYS[1], '-inf', now - window)
local count = redis.call('ZCARD', KEYS[1])
if redis.call('ZSCORE', KEYS[1], member) then
    return {2, count}
end
if count >= limit then
    return {0, count}
end
redis.call('ZADD', KEYS[1], now, member)
redis.call('PEXPIRE', KEYS[1], window)
return {1, count + 1}
```

### 用具体输入核对，不只检查“脚本没报错”

fixed_window 的参数依次是上限、窗口毫秒。对一个不存在的计数键，传入 2、60000，连续调用三次，前两次允许，第三次拒绝；本脚本拒绝时不继续增加计数。等待期限结束后会重新开始。它与正文自然分钟示例同属固定分段思路，但分段起点不同，不能声称完全相同。

sliding_window 的参数依次是当前毫秒、窗口毫秒、上限、请求标识。使用同一键、窗口 1000、上限 2，在真实 TTL 没经过一秒前迅速调用：

| 教学当前时间 | 标识 | 预期回复 | 含义 |
|---:|---|---|---|
| 1000 | a | [1, 1] | 接受，窗口内 1 条 |
| 1500 | b | [1, 2] | 接受，窗口内 2 条 |
| 1600 | b | [2, 2] | 相同标识已记录，不重复加入 |
| 1999 | c | [0, 2] | 满额，拒绝 |
| 2000 | c | [1, 2] | a 离开窗口，接受 c |

真实计时与传入的教学数字是两件事：本脚本还会设置真实键 TTL，手动输入过慢导致键过期时，不能拿结果去反驳这张时间表。自动回归会连续调用；生产需另行验证时钟、重试和最坏负载。

<a id="lab-recovery"></a>

## 观察快照恢复

[回到第 10 章](../docs/10-持久化与恢复.md)

只在按环境说明建立、关闭自动保存和 AOF 的学习容器里做：写入 lab:persist=v1，执行 SAVE 保存快照，再写入 v2。GET 应先得到 v2。随后显式 SHUTDOWN NOSAVE，让服务关闭但不把 v2 再存入快照；重新启动同一个容器，读取应回到 v1。

这是“恢复保存时刻，而非最后看到的值”的实验。不得删除容器后又指望其可写层仍在，也不得换到另一实例读取。SAVE 会阻塞该实例，SHUTDOWN 会关闭它，所以不纳入可随意粘贴到外部服务的命令块。自动检查只对自己启动并验证 PID 的临时进程执行这一过程。

> ⚠️ 正常停止容器不等于模拟突然掉电；这个实验也不验证设备写缓存、AOF fsync、Sentinel 切换或磁盘损坏。它只核对快照恢复边界。
