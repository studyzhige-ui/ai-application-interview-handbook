# 08｜WebSocket：让双方在连接中持续交流

[← 上一章](07-Streaming与SSE.md) · [模块主页](../README.md) · [下一章 →](09-Security与TenantContext.md)

上一章中，客户端发起请求后主要等待服务端推送结果。如果用户需要一边接收结果，一边持续发送暂停、修改选项或音频片段，单向交付就不够自然了。

WebSocket 提供的是一条持续双向通信的连接。它不会自动管理用户身份、恢复丢失的任务，也不会替应用定义消息含义。本章先完成一次“发一句，回一句”，再讨论连接变长以后新增的责任。即使当前项目不用 WebSocket，也应能判断它与轮询、SSE 的差别，并解释连接断开后哪些状态还能保留。

## 1. 一条 WebSocket 连接怎样工作

```text
客户端发起连接请求
        ↓
服务端判断是否接受
        ↓
连接建立：双方可以持续发送消息
        ↓
任一方关闭，或网络中断
        ↓
清理与该连接关联的资源
```

`accept()` 表示接受连接，`receive_text()` 等待一条文本消息，`send_text()` 发送文本。它们不是每次都重新建立一个普通 HTTP 请求。

```python
# example: websocket_app
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

app = FastAPI()
app.state.connections = 0

@app.websocket("/ws")
async def echo(ws: WebSocket):
    await ws.accept()
    app.state.connections += 1
    try:
        while True:
            message = await ws.receive_text()
            if message == "stop":
                await ws.send_text("已结束")
                await ws.close(code=1000)
                return
            await ws.send_text("收到：" + message)
    except WebSocketDisconnect:
        pass  # 对端离开是本示例允许的连接结束方式
    finally:
        app.state.connections -= 1  # 正常结束、对端断开都归还这份连接计数
```

这个计数只用于观察单进程实验，不是分布式连接注册中心。启动后，在允许连接到本地服务的浏览器页面控制台试验：

```javascript
const socket = new WebSocket("ws://127.0.0.1:8000/ws");
socket.onopen = () => socket.send("你好");
socket.onmessage = event => console.log(event.data);
socket.onclose = event => console.log("关闭码", event.code);
// 收到“收到：你好”后，再执行 socket.send("stop")。
```

应先看到“收到：你好”，发送 `stop` 后看到“已结束”，随后连接正常关闭。若页面是 HTTPS，浏览器可能限制不安全的 `ws://` 连接；真实 HTTPS 部署应使用 `wss://`，不要把浏览器安全阻止误当成函数没执行。

## 2. 为什么需要消息类型，而不是一直发字符串

字符串 `"stop"` 足以做实验，但业务消息可能包含不同操作。把消息分成“类型”和“数据”，客户端就不用猜一段文字究竟是用户内容还是控制指令。

```json
{"type":"ping","request_id":"m1"}
```

预期回复：

```json
{"type":"pong","request_id":"m1"}
```

`type` 用于选择处理逻辑，`request_id` 将回复与这次请求关联。它是应用消息中的标识，不会因为叫这个名字就自动进入 HTTP 日志或分布式追踪。

```python
# example: websocket_protocol_app
from typing import Literal
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from pydantic import BaseModel, ConfigDict, ValidationError

app = FastAPI()

class Command(BaseModel):
    model_config = ConfigDict(extra="forbid")
    type: Literal["ping"]
    request_id: str

@app.websocket("/ws")
async def commands(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            raw = await ws.receive_text()
            try:
                command = Command.model_validate_json(raw)
            except ValidationError:
                await ws.send_json({"type": "error", "code": "INVALID_MESSAGE"})
                continue
            await ws.send_json({"type": "pong", "request_id": command.request_id})
    except WebSocketDisconnect:
        return
```

`Literal["ping"]` 表示本例只接受这个固定值。无效 JSON、缺字段或 `type="delete"` 都会被拒绝为 `INVALID_MESSAGE`，连接仍然保持，允许发下一条正确消息。这是本例的应用策略，不是所有协议都必须允许无限次错误重试。

> ⚠️ WebSocket 握手成功后，不会替每条消息自动重新执行普通 HTTP 请求的数据校验和权限检查。应用必须明确消息模型和操作权限。不同消息需要不同权限时，不能只凭“连接建立时登录过”放行一切。

## 3. 连接身份、消息关联、业务任务是三种不同状态

| 状态 | 回答的问题 | 例子 |
|---|---|---|
| 连接状态 | 当前有哪些客户端在线 | 连接对象、最近活动时间 |
| 消息关联 | 这条回复对应哪个动作 | request_id、序号 |
| 业务任务状态 | 工作做到哪里，是否仍应继续 | run_id、运行中、待批准 |

一个任务可以跨多次连接被观察；一条连接也可以发送多次独立请求。因此不要把它们全部称作同一个 `chat_id`。

多个工作进程各自维护的 `active_connections` 也不互通。A 进程的列表不知道 B 进程有哪些连接。需要跨进程广播时，应设计消息转发或共享协调，而不是以为把列表定义成全局变量就解决了共享。

## 4. 慢客户端为什么会拖累系统

假设服务每秒产生 100 条消息，客户端每秒只能接收 20 条。如果应用把差额无限追加到内存队列，队列每秒增加约 80 条，连接越久占用越大。

这里的选择应根据消息含义决定：

1. 对可替换的进度更新，可以合并，只保留最新状态。
2. 对不能丢失的结果，限制队列并让生产者等待，或转为可按游标读取的持久记录。
3. 客户端长期过慢，可以在说明协议后关闭连接，允许稍后重新获取状态。

这就是背压的入口直觉：消费变慢时，不能让生产端无限制造积压。实现时还应限制消息大小、连接数量和单个身份的消耗。

## 5. 心跳、重连与恢复不是一回事

心跳帮助判断连接是否仍然可用。WebSocket 协议的 Ping/Pong 与应用自己定义的 `{"type":"ping"}` 不同；浏览器脚本不能随意操作底层控制帧，但可以实现自己的应用级心跳。

重连只是重新建立连接。恢复首先要确定：用户需要的是“最新状态”，还是“断开期间每一个事件”？

例如页面只轮播该用户最近 20 条记录，断线重连后，可以重新验证身份、拉取这 20 条当前记录，再继续订阅更新。这里恢复的是最新页面，不是回放所有历史事件。快照应带版本或事件位置，订阅从对应位置接续；不能在“读快照”和“开始订阅”的间隙静默漏掉更新。

如果业务要求每条结果都处理，则需要保存事件与已处理位置，补齐缺口并去重。只保留最近 20 条时，不能承诺断开再久都能完整回放。记录过期后，要明确返回恢复失败或要求重新取得快照。

> ⚠️ 重连时仍要重新核对身份和可订阅范围。知道一个 run_id 或上次的游标，不等于仍有权读取其中的数据。

## 6. 连接关闭以后，要停掉什么

连接断开通常需要移除该连接的注册信息、取消只服务这条连接的发送任务、解除订阅并释放缓冲区。**不要因为一个客户端离开就关闭整个应用共享的模型客户端。**

业务任务则另作决定：临时生成可以随连接取消，已被系统接受的持久任务可能继续运行。这个选择应在 API 契约中明确，并由任务系统落实。

> ⚠️ 本章的两个演示接口没有认证、配额和完整攻击防护，只用于本地练习。公开部署前，需要在握手中确认可信身份、验证允许的 Origin，并在消息层执行权限策略。CORS 中间件不是 WebSocket 权限系统。

## 7. 轮询、SSE 与 WebSocket 怎样选

不需要持续连接，也可以更新页面：客户端每隔一段时间发送 GET 查询最新状态，这就是**轮询（Polling）**。它适合允许一定刷新延迟、只关心当前结果的界面。

| 交互需要 | 可以先考虑 | 需要承担的代价 |
|---|---|---|
| 隔几秒查看任务是否结束或刷新最近记录 | 轮询 | 没变化也会查询；间隔越短，请求越多 |
| 服务端持续推送文字、进度和结果 | SSE | 维护长连接，并定义结束、断开和续接 |
| 双方持续发送语音、控制与状态消息 | WebSocket | 还要管理双向消息、连接身份、缓冲与恢复 |

先问可接受多大的延迟、更新是否频繁、客户端是否也要持续发送，不按工具是否“更高级”选择。轮询不是天然落后，WebSocket 也不会自动让业务状态可靠。

同一业务要支持多种传输时，应共用成功与失败的含义。例如轮询响应的 `status="succeeded"`，与事件流中的任务成功事件，应来自同一项任务事实，不能各自维护互相矛盾的结果。

**练习：** 给消息协议添加 `type="echo"` 和一个非空 `text`。在同一连接中先发错误消息，再发正确消息，最后关闭连接。预期错误不会被当作正常内容回显，正确消息仍可处理。将这些预期写成测试，而不是只靠手动看控制台。

---

## 本章小结

WebSocket 解决持续双向交流；身份、消息含义、缓冲上限和业务恢复仍是应用责任。连接状态与任务状态应分开，通信工具的选择服从交互需要。

## 🎯 面试怎么回答

**为什么不能用全局列表管理所有 worker 的连接？**

> 每个 worker 是独立进程，列表只反映本进程连接。跨进程协作要有明确的消息转发和状态设计。

**用户断开后，Agent 任务一定取消吗？**

> 不一定。应清理连接相关资源；任务是否继续由业务契约和持久执行系统决定，不能把传输断开直接等同于业务取消。

## ⚠️ 易错点

> ⚠️ 握手认证不能自动授权之后的每一项操作，消息应独立校验所需权限。

> ⚠️ 无限缓冲不能解决客户端消费慢，只会把延迟问题变成内存问题。

> ⚠️ 重连不证明事件已补齐；恢复需要记录、游标与去重策略。

## 本章自测

先回答，再展开核对。涉及操作的题目，应能说出预期结果及原因。

<details>
<summary>1. 示例为什么使用 finally 减少连接计数，而不是只写在 stop 分支？</summary>

对端可能直接关闭，或者处理中发生异常。finally 能覆盖控制流退出路径；若进程被强制终止，则不能承诺清理代码一定执行。

</details>

<details>
<summary>2. 页面只需要每五秒刷新最近 20 条记录，是否必须使用 WebSocket？</summary>

不必。若五秒延迟可接受，可以先评估轮询；需要服务端及时推送时再比较 SSE，需要持续双向交流时再考虑 WebSocket。无论哪种方式，都要验证身份并定义断开后的最新状态或事件恢复。

</details>

<details>
<summary>3. 收到 INVALID_MESSAGE 后为什么还能发 ping？</summary>

示例在拒绝消息后 continue，继续等待下一条。真实服务还应限制错误频率和资源消耗。

</details>

## 知识回看与权威资料

- [WebSocket 教程](https://fastapi.tiangolo.com/advanced/websockets/)：核对接收、发送、依赖与断开处理。
- [WebSocket 接口](https://starlette.dev/websockets/)：核对连接状态和关闭行为。
- [浏览器 WebSocket](https://developer.mozilla.org/en-US/docs/Web/API/WebSocket)：核对客户端消息与关闭事件。

真人问题回看：[S089 的弱网恢复](../../../market/interviews/batch-05.md)、[S297 的 WebSocket／轮询选择与用户最近记录](../../../market/interviews/batch-35.md)。本章解释通信与恢复契约；MQ 去重和数据库／缓存一致性不因此变成 WebSocket 的功能。
