# 07｜流式响应：逐步交付结果与 SSE 事件

[← 上一章](06-AsyncExecution与BlockingBoundary.md) · [模块主页](../README.md) · [下一章 →](08-WebSocket与EventProtocol.md)

用户等了十秒，页面上仍然什么都没有；第十一秒，整段回答突然出现。服务最终算对了，但等待过程并不好。流式响应尝试改变的是**结果交付的节奏**：有一部分就先交付一部分，而不是等所有内容齐备。

本章从分块发送开始，先比较消息格式，再把 SSE 的事件、错误、结束和续接讲清楚。示例使用假数据，不调用收费模型。原生 SSE 需要 FastAPI 0.135.0+，本课程以 0.141.1 为基线。

## 1. 先观察一个逐步返回的响应

把下面程序保存为 `main.py`，用 `python -m uvicorn main:app --reload` 启动。

```python
# example: raw_stream_app
import asyncio
from fastapi import FastAPI
from fastapi.responses import StreamingResponse

app = FastAPI()

async def pieces():
    for text in ["开始整理", "找到两条材料", "整理完成"]:
        await asyncio.sleep(0.2)  # 模拟下一段结果尚未准备好
        yield text + "\n"        # 交出这一段；下一次迭代再继续执行

@app.get("/stream")
async def stream():
    return StreamingResponse(pieces(), media_type="text/plain")
```

在另一个终端执行下面的命令。Windows PowerShell 中明确写 `curl.exe`；其他环境可以写 `curl`。

```bash
curl -N http://127.0.0.1:8000/stream
```

`-N` 让 curl 不为了自己的输出缓冲而等更多数据。应逐步看到三行文字，而不是先收到一个完整 JSON 数组。生成器的执行过程是：等待、交出一段、等待、交出下一段，最后结束。

> ⚠️ 一次 `yield` 不保证对应客户端的一次底层网络读取。服务器、代理、网络和客户端都可能合并或拆分字节。因此客户端需要按协议边界解析，不能假设“收到一次网络数据就是一条消息”。

`StreamingResponse` 接收可逐项产生内容的对象。同步迭代器和异步迭代器有不同执行路径；上面使用异步生成器，是为了等待期间仍能让其他任务推进。[响应文档](https://fastapi.tiangolo.com/advanced/custom-response/#streamingresponse)说明了接口。

## 2. 字节流为什么还需要消息格式

如果服务先发 `"he"`，再发 `"llo"`，客户端知道这属于同一个词吗？如果中途发生错误，客户端又怎样区分“正常文字”和“错误说明”？

分块只解决“可以逐步发送”。**协议负责说明每段信息的含义，以及一条消息从哪里开始、到哪里结束。**

| 形式 | 消息边界 | 适合的内容 |
|---|---|---|
| 普通文本流 | 由应用自行约定 | 简单文本、明确分隔的日志 |
| SSE | 按字段组织事件，以空行结束事件 | 内容片段、进度、错误、结束通知 |
| JSON Lines | 每行是一个完整 JSON 值 | 逐条返回的结构化记录 |
| WebSocket | 协议提供消息交互能力 | 双方持续发送数据和控制消息 |

<details>
<summary>实现对照：用 JSON Lines 逐条返回结构化记录</summary>

当接口需要逐条导出笔记或处理记录时，可以考虑 JSON Lines（原生支持需要 FastAPI 0.134.0+）。每行都是独立 JSON，不需要等整个数组闭合后才能解析。

```python
# example: native_jsonl_app
from collections.abc import AsyncIterable
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class NoteOut(BaseModel):
    id: int
    text: str

@app.get("/notes/stream")
async def notes() -> AsyncIterable[NoteOut]:
    yield NoteOut(id=1, text="第一条")
    yield NoteOut(id=2, text="第二条")
```

在课程基线版本中，FastAPI 根据流式返回类型对每项进行处理，默认响应媒体类型为 `application/jsonl`。响应体应包含两个 JSON 行，而不是一个 Python 列表的打印结果。

```json
{"id":1,"text":"第一条"}
{"id":2,"text":"第二条"}
```

上面是两个独立 JSON 值组成的 JSON Lines，不是可被一次 `json.loads` 当成单个 JSON 文档解析的内容。使用客户端逐行读取，再分别解析。[原生 JSON Lines 文档](https://fastapi.tiangolo.com/tutorial/stream-json-lines/)列出了流式类型声明。

**核对：** 能否直接对整段响应调用 `response.json()`？不能；应逐行取得完整 JSON 记录，再分别解析。

</details>

## 3. SSE：把一段结果写成一个事件

SSE 是 Server-Sent Events，即服务端发送事件。线上的一条事件可以长这样：

```text
event: delta
id: 2
data: {"text":"第二段"}

```

这几行不是 Python 代码，而是 HTTP 响应体中的文本。

- `event` 是事件类型，客户端可据此决定怎么处理。
- `data` 是事件数据；应用可以约定它是 JSON。
- `id` 是事件标识，可以参与重连后的续接。
- 末尾空行表示这条事件结束；不是为了排版好看。

响应的媒体类型是 `text/event-stream`。`retry` 字段可以向支持它的客户端提供重连等待时间，但不负责重新执行业务。[SSE 官方教程](https://fastapi.tiangolo.com/tutorial/server-sent-events/)给出了字段和用法。

## 4. 使用原生 SSE，观察开始、内容与结束

```python
# example: native_sse_app
import asyncio
from collections.abc import AsyncIterable
from fastapi import FastAPI
from fastapi.sse import EventSourceResponse, ServerSentEvent

app = FastAPI()

@app.get("/events", response_class=EventSourceResponse)
async def events(fail: bool = False) -> AsyncIterable[ServerSentEvent]:
    yield ServerSentEvent(event="start", data={"status": "running"}, id="1")
    await asyncio.sleep(0.02)
    yield ServerSentEvent(event="delta", data={"text": "一条材料"}, id="2")
    if fail:
        yield ServerSentEvent(event="error", data={"code": "SOURCE_UNAVAILABLE"}, id="3")
        yield ServerSentEvent(event="end", data={"status": "failed"}, id="4")
        return
    yield ServerSentEvent(event="end", data={"status": "succeeded"}, id="3")
```

调用 `/events`，期望事件顺序为 `start → delta → end`。调用 `/events?fail=true`，期望 `start → delta → error → end`，结束状态为 `failed`。

`ServerSentEvent(data=...)` 会把这里的字典编码成 JSON。`start`、`delta`、`error`、`end` 是本例约定的事件名，不是框架要求每个应用照抄的固定名单。

这个例子把传输与业务结果分开了：**HTTP 请求成功建立，不等于整项任务最终成功。** 当响应头已经发出，再发生失败，不能指望把先前的 200 改成 500。客户端需要识别流内错误和终止状态。

> ⚠️ 结束事件是应用协议，不是成功保证。连接也可能在结束事件发出前就断开。没有收到预期终止事件时，客户端应显示“中断／结果待确认”，而不是默认为成功。

## 5. POST 能返回 SSE，为什么 EventSource 示例却常用 GET

服务端可以为 POST 返回 SSE。浏览器原生 `EventSource` 主要通过 GET 建立连接，构造参数不能任意设置 POST 请求体或自定义 Authorization 请求头。**服务端能返回什么，与所选客户端能怎样发请求，是两个问题。**

若调用上面的 GET 接口，在浏览器开发者工具中可以试：

```javascript
const source = new EventSource("http://127.0.0.1:8000/events");
source.addEventListener("delta", event => console.log(JSON.parse(event.data).text));
source.addEventListener("end", event => {
  console.log(JSON.parse(event.data).status);
  source.close();
});
```

若前端页面与接口跨源，还需符合 CORS 设置。需要 POST、JSON 请求体或自定义请求头时，可以使用 `fetch` 等支持流式读取的客户端，并正确实现或采用已有的 SSE 解析器。不能只写 `chunk.split("\n")` 就假设每次网络读取包含完整事件。[浏览器 EventSource 接口](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)说明了客户端限制。

## 6. 心跳、代理与重连要分清责任

当前原生 SSE 实现会在适当的空闲间隔发送注释心跳，并设置有助于避免缓存和代理缓冲的响应头。这些默认措施不是端到端保障。部署时仍要观察代理是否立即转发、空闲连接多久会被关闭，以及客户端是否持续读取。

重连也不等于自动恢复全部结果。假设一次任务的事件有稳定序号，客户端收到 12 后断线，服务端又产生了 13、14：

| 阶段 | 客户端与服务端分别做什么 |
|---|---|
| 断开 | 客户端目前只知道收到过 12；任务可能仍在运行 |
| 重连 | 客户端重新建立已授权的订阅，并携带续接位置；EventSource 可发送 `Last-Event-ID` |
| 补发 | 服务端从该任务的记录里读取 12 之后的事件，而不是重新执行任务 |
| 接续 | 补发和实时订阅使用同一序号约定，避免两阶段之间漏掉新事件；客户端按任务与事件 ID 去重 |

这里的序号与保留策略是应用约定。若记录已过期，接口需要明确通知客户端改为查询当前任务状态，不能默默从一个不完整的位置继续。原生 EventSource 的事件 ID 表示它接收事件时维护的续接线索，**不证明应用已经把结果处理或持久保存成功**。[EventSource 标准](https://html.spec.whatwg.org/multipage/server-sent-events.html#the-last-event-id-header)规定的是传输行为，不是业务确认协议。

> ⚠️ 上面的 `/events` 教学接口没有保存事件历史，也没有实现续接。它每次调用从 1 开始，只适合观察单次事件格式；不能把这套编号直接用于生产任务的跨连接恢复。

## 7. 怎样判断流式接口真的工作了

检查不能只停在“最后拼起来的文字正确”。应分别核对：

- **内容与协议：** 媒体类型、事件类型、顺序、字段、错误和终止状态。
- **时间：** 第一段何时到达，段与段之间是否存在预期等待，代理是否把结果攒到最后。
- **生命周期：** 断开后是否停止不再需要的生成，是否释放本次订阅和连接。

测试客户端适合验证协议；真实增量到达需要启动服务并经过实际客户端，部署后的代理也应单独测试。流式接口不能通过“最终响应体相等”证明实时体验。

**练习：** 将 SSE 的第二个事件改成带 `processed=1,total=2` 的 `progress`，保留独立 `end`。先写预期事件顺序，再运行验证；不要让前端从“处理一半了”这句自然语言推算进度。

---

## 本章小结

流式发送让已生成的结果先到达客户端；SSE 再为这些结果定义事件边界和含义。正常、失败、中断与结束必须能区分，实际到达时间也需要经过客户端和代理验证。

## 🎯 面试怎么回答

**SSE 与普通 StreamingResponse 有什么不同？**

> StreamingResponse 提供分块发送能力；SSE 定义 event、data、id 等事件字段和分隔规则。二者不处于同一抽象层。

**SSE 连接恢复后会自动补齐事件吗？**

> 不会。客户端游标只是恢复线索，服务端需要历史或状态，并定义保留期限、去重和游标失效行为。

## ⚠️ 易错点

> ⚠️ 响应头已发出后，错误需要流内协议表达；连接突然中断时甚至无法发出错误事件。

> ⚠️ POST 可以返回 SSE，但浏览器 EventSource 不是任意 HTTP 请求客户端。

> ⚠️ 一次 yield、一条事件与一次网络读取不是一一对应关系。

## 本章自测

先回答，再展开核对。涉及操作的题目，应能说出预期结果及原因。

<details>
<summary>1. 为什么加了流式返回，总生成时间可能没变？</summary>

生成计算本身没改变，只是提前交付已经得到的部分；首段体验与总耗时要分别测。

</details>

<details>
<summary>2. 收到 HTTP 200，却没有收到约定的 end 事件，可以显示“任务完成”吗？</summary>

不能。200 可能只表示流已成功建立，连接仍可能在任务结束前中断。应显示中断或结果待确认，并按应用契约查询状态。

</details>

<details>
<summary>3. 仅测 TestClient 最终得到三段文字，能证明代理没有缓冲吗？</summary>

不能。它没有覆盖真实网络和部署代理，需要服务运行后的实际流式客户端实验。

</details>

## 知识回看与权威资料

- [原生 SSE](https://fastapi.tiangolo.com/tutorial/server-sent-events/)：核对事件字段、POST、心跳及重连。
- [JSON Lines](https://fastapi.tiangolo.com/tutorial/stream-json-lines/)：核对逐项校验与媒体类型。
- [浏览器 EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)：核对客户端能力与限制。

真人问题回看：[S087 的 FastAPI／SSE 中间结果与断线恢复](../../../market/interviews/batch-05.md)。本章落实事件交付与续接位置；任务检查点怎样恢复执行，仍由 Agent 运行系统负责。
