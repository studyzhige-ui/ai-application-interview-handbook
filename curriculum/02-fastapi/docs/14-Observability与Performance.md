# 14｜观测与性能：把慢请求拆成可定位的时间

[← 上一章](13-Testing.md) · [模块主页](../README.md) · [下一章 →](15-Deployment与GracefulShutdown.md)

用户说“这次等了十秒”，日志却显示处理只用了 20 毫秒。两边可能都没有说错：日志测到了某个函数返回，而用户等的是最后一段内容。性能分析首先要把**计时的起点和终点**说清楚。

本章先判断记录的是哪一段时间，再用日志、指标和追踪定位问题。手写 ASGI 计时器只是可选验证，不是日常排障的前置技能。

## 1. 三种观测资料各回答什么

| 资料 | 主要问题 | 合适的信息 |
|---|---|---|
| 日志 | 具体发生了什么事件 | 请求关联 ID、错误类别、经过筛选的事件上下文 |
| 指标 | 某一类行为随时间怎样变化 | 请求数、错误率、延迟分布、队列等待 |
| 追踪 | 一次请求在哪些阶段消耗时间 | 认证、等待连接、查询、模型调用、发送等 Span |

Span 是追踪中的一段操作。它可以嵌套，也可能与其他 Span 并发，不能把所有 Span 时长直接相加当总耗时。

Request ID 帮助关联记录，但只是标识，不是权限。默认记录全部用户正文和凭证并不会让诊断更专业，反而扩大隐私与泄露范围。

## 2. call_next 返回，不代表流已经发完

第 04 章的 HTTP 中间件中，`await call_next(request)` 得到响应对象。流式响应的内容可能还在继续产生。因此围绕 call_next 的时间，不应无条件命名为“完整响应耗时”。

先用一条时间线区分观察点：

| 假设时间 | 发生的事 | 这个时刻不能证明什么 |
|---|---|---|
| 0 ms | 收到请求，开始处理 | 结果已经生成 |
| 20 ms | 中间件取得响应对象 | 响应体已经发完 |
| 100 ms | 客户端看到第一段有效文字 | 完整答案已经得到 |
| 10000 ms | 客户端收到最后一段 | 后台任务也必然成功 |

这是教学时间线，不是性能基准。比较日志和用户体验之前，要确认两者是否测量同一段过程。使用观测工具时，也应检查指标的开始点和结束点。

<details>
<summary>实现选读：在 ASGI 消息处记录响应开始和结束</summary>

确实需要验证服务端发送边界时，可以观察响应开始消息和最后一个响应体消息。下面只保留最近 100 条测量，不要求在自己的服务中从零实现这套中间件。

```python
# example: observed_app
import asyncio
from collections import deque
from time import perf_counter
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

class MeasureHTTP:
    def __init__(self, app, records):
        self.app = app
        self.records = records

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return
        start = perf_counter()
        result = {"status": None, "headers_s": None, "body_end_s": None}

        async def measured_send(message):
            await send(message)
            elapsed = perf_counter() - start
            if message["type"] == "http.response.start":
                result["status"] = message["status"]
                result["headers_s"] = elapsed
            elif message["type"] == "http.response.body" and not message.get("more_body", False):
                result["body_end_s"] = elapsed

        try:
            await self.app(scope, receive, measured_send)
        finally:
            result["app_end_s"] = perf_counter() - start
            self.records.append(result)

records = deque(maxlen=100)
app = FastAPI()
app.add_middleware(MeasureHTTP, records=records)

async def text_chunks():
    yield "first\n"
    await asyncio.sleep(0.03)
    yield "second\n"

@app.get("/stream")
async def stream():
    return StreamingResponse(text_chunks(), media_type="text/plain")
```

一次成功请求后，`body_end_s` 应晚于 `headers_s`，`app_end_s` 不早于已观测的响应结束。异常或断开时可能没有最后体消息，此时 `body_end_s` 保留 None，不应伪装成成功完成。

这里 `scope` 表示请求或连接信息，`receive` 接收 ASGI 消息，`send` 向服务器交付消息。包装 send 是为了在保留原有发送行为的同时记录观察点；不是直接操纵浏览器。

> ⚠️ “服务端已发送最后一个 ASGI 响应体消息”仍不等于“客户端已收到并显示”。代理缓冲、网络和前端渲染不在这一个测量点内。数据字段的名字必须反映测量边界。

**可选实验：** 把等待从 0.03 改成 0.10 秒。比较 headers_s 与 body_end_s，检查变化出现在响应开始还是内容发送阶段；调度会影响实际数值，不要求精确等于某个小数。

</details>

## 3. SQL 已经变快，为什么接口仍然慢

先看一个教学算例。假设同一次普通请求的三个阶段顺序执行、不重叠，修改前后只有 SQL 时间变化：

| 阶段 | 修改前 | 修改后 |
|---|---:|---:|
| 等待连接 | 100 ms | 100 ms |
| 执行 SQL | 800 ms | 50 ms |
| 其余处理 | 100 ms | 100 ms |
| **请求合计** | **1000 ms** | **250 ms** |

SQL 快了 16 倍，整个请求只快了 4 倍。现在最大的可疑部分已经不再是 SQL；继续只优化查询，不会消除连接等待或其他工作。这些数字用于说明计算关系，不是面经原帖的完整测量记录，也不是性能基准。

下一步先把“其余处理”展开为序列化、其他依赖和响应交付，再根据实际测量决定改哪里：

- 连接等待高：检查资源是否长期占用、请求是否超过池容量。
- 异步请求普遍卡住：检查事件循环中的同步阻塞或重计算。
- 大量同步请求才明显排队：检查线程容量和下游等待。
- 首段很快，后续逐渐变慢：比较生成、网络发送与客户端消费速度。

这些是调查线索，不是看到症状就唯一定位。并发任务的 Span 可能重叠，不能直接套用上表的相加规则；应先找决定整次请求结束的那条路径。

## 4. 分位数比平均值多告诉你什么

把一批请求耗时从小到大排列，P95 描述靠近 95%位置的延迟水平，P99 关注更靠后的尾部。具体统计系统可能使用不同插值或直方图近似，需要了解实现。

假设绝大部分请求 100 毫秒，少量请求十秒，平均值不一定能表达那部分用户的糟糕体验。反过来，一次 P99 升高也要看样本量和请求类型，不能脱离流量分布下结论。

AI 流式请求应分别观察首个有效内容的时间、总生成时间、相邻事件间隔、断开比例、流开始后的失败。首字节可能只是心跳或空事件，不一定是用户看到第一段答案的时刻。

## 5. 指标标签为什么不能什么都加

把每个用户 ID、请求 ID、原始问题都作为指标标签，会产生大量不同时间序列。指标存储成本和查询负担可能迅速扩大。

更适合指标的维度是有限集合，例如规范化路由 `/notes/{id}`、方法、状态类别、受控供应商名。具体请求 ID 放日志或 Trace，原始内容只有在必要、授权和脱敏规则允许时保留。

生产观测还需要限制采样和保留期限；日志、追踪以及教学记录本身，也不能无限占用资源。

## 6. 一个可执行的排查顺序

1. 确认用户说的慢对应哪个时间边界，是首段还是完整结果。
2. 按路由、错误类别和负载拆分，观察是否只影响特定请求。
3. 检查事件循环、线程等待与连接获取，不只看 CPU 平均值。
4. 对照下游调用与发送阶段，找出实际消耗的位置。
5. 用相同工作负载比较修改前后，保留错误率与资源使用，避免只追求一项变快。

对流式接口还要经过实际代理测试。只给应用增加一个计时 Header，不足以解释完整端到端体验。

**练习：** 某个流式请求的中间件计时是 20 毫秒，客户端收到第一段是 100 毫秒，完整结束是 10 秒。分别写出这三个数字测量的范围，并说明仅凭它们能否判断“数据库慢”。

---

## 本章小结

观测先定义边界，再选择记录形式。响应开始、响应结束和客户端显示不同；事件循环、线程、连接池和下游等待也不同。具体测量比一句“P99 高”更接近可行动的原因。

## 🎯 面试怎么回答

**HTTP 中间件 call_next 前后的计时能代表完整 SSE 耗时吗？**

> 不能无条件这样理解。它通常围绕响应对象形成，而流体发送可能继续；需要按 ASGI 响应事件或更外层客户端测量明确终点。

**为什么 request_id 不适合作为指标标签？**

> 它几乎每次都不同，会造成极高基数。更适合日志和追踪关联，指标使用受控类别。

## ⚠️ 易错点

> ⚠️ TTFB 可能只是心跳或响应头，不能自动等同用户看到首个有效 token。

> ⚠️ 服务端完成响应发送，并不证明客户端已经接收并显示完毕。

> ⚠️ 并发 Span 可能重叠，简单相加会重复计算时间。

## 本章自测

先回答，再展开核对。涉及操作的题目，应能说出预期结果及原因。

<details>
<summary>1. 中间件 20 毫秒，客户端 10 秒，是否必有一方测错？</summary>

不一定。前者可能只到取得响应对象，后者包括后续生成和传输。先核对起止点，再定位多出的时间。

</details>

<details>
<summary>2. 查询 20 毫秒，API 两秒，下一步先做什么？</summary>

检查连接获取、线程或事件循环排队、其他下游与发送阶段，确定真正耗时。

</details>

<details>
<summary>3. 为什么指标使用 /notes/{id}，而不是为每个实际笔记编号建立一组标签？</summary>

规范化路径把同类请求聚在一起，避免不同编号不断产生新的时间序列。具体请求标识更适合放在日志或追踪中。

</details>

## 知识回看与权威资料

- [ASGI 响应事件](https://asgi.readthedocs.io/en/latest/specs/www.html)：核对 response.start 与 more_body。
- [Starlette 中间件](https://starlette.dev/middleware/)：核对纯 ASGI 包装与状态隔离。
- [HTTPX 超时](https://www.python-httpx.org/advanced/timeouts/)：把连接池等待与网络读取分开。

真人问题回看：[S293 的 SQL 优化后端到端接口诊断](../../../market/interview-experience/01-data/raw/batch-32.md)、[S066 的应用监控指标](../../../market/interview-experience/01-data/raw/batch-04.md)。实作要能解释测量范围和下一步调查，而不只是列监控工具。
