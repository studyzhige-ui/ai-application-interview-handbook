# 11｜BackgroundTasks、文件上传与 Long-running Task Boundary

AI 后端最常见的误区之一是：

> “FastAPI 有 `BackgroundTasks`，所以所有长任务都可以扔进去。”

这是错误的。

---

## 1. `BackgroundTasks` 解决什么

FastAPI 的 `BackgroundTasks` 允许在响应返回后继续执行一个小任务：

```python
from fastapi import BackgroundTasks

@app.post("/notify")
async def notify(background_tasks: BackgroundTasks):
    background_tasks.add_task(send_email)
    return {"accepted": True}
```

适合：

- 小型通知；
- 不要求独立调度；
- 与当前应用进程关系紧密；
- 失败后不需要复杂恢复。

---

## 2. 它不等于 Durable Task Queue

如果任务需要：

```text
分钟级 / 小时级执行
Worker 宕机恢复
跨机器并行
Retry / Dead Letter
Lease / Heartbeat
任务状态查询
```

就应该进入：

```text
DB Task State
+ MQ / Job Queue
+ Worker
```

而不是依赖单个 FastAPI Worker 进程里的 BackgroundTasks。

FastAPI 官方也明确提醒：重计算、需要多进程/多服务器的后台工作更适合独立任务系统。

---

## 3. RAG Ingestion 是典型 Long-running Task

上传 500MB PDF 后：

```text
Upload
→ Parse
→ OCR
→ Chunk
→ Embedding
→ Index
```

这不适合全部塞进一个普通 HTTP Request 等到完成。

更常见：

```text
POST /knowledge/files
→ save file / object
→ create task record
→ enqueue
→ 202 Accepted + task_id
```

然后：

```text
GET /tasks/{id}
或 SSE progress stream
```

---

## 4. `bytes` vs `UploadFile`

如果参数声明为 `bytes`，框架会把整个文件内容读入内存。

适合小文件。

`UploadFile` 更适合大文件，因为底层使用 spooled temporary file：

```text
small part in memory
→ larger content can spill to disk
```

并且提供文件名、content type 和 file-like async interface。

---

## 5. 大文件上传的真实风险

至少要考虑：

- 文件大小限制；
- Content-Type 不能完全信任；
- 临时磁盘空间；
- 并发上传；
- Hash / Dedup；
- Virus / Unsafe file；
- 超时；
- 中断重传；
- Object Storage。

FastAPI 只提供 Upload 接口能力，不自动解决整条数据管道。

---

## 6. 不要一次 `await file.read()` 读爆内存

坏模式：

```python
content = await file.read()
```

对于巨大文件，这会把整个内容放进内存。

更稳的是分块处理：

```python
while chunk := await file.read(1024 * 1024):
    await write_chunk(chunk)
```

具体 chunk size 要根据存储和吞吐测试决定。

---

## 7. Upload API 和 Processing API 解耦

推荐状态机：

```text
UPLOADING
→ STORED
→ QUEUED
→ PROCESSING
→ INDEXED
或 FAILED
```

这让你可以区分：

- 网络上传失败；
- 对象存储失败；
- Parser 失败；
- Embedding 失败；
- Index 失败。

否则一句“上传失败”无法排查。

---

## 8. `BackgroundTasks` 和 Request Resource

Background Task 不应该继续依赖即将被 Request cleanup 的 DB Session 等资源。

正确思路：

```text
Task receives stable ID / primitive data
→ task opens its own resources
→ task closes its own resources
```

不要把活跃 Session/Connection 对象直接传过去长期使用。

---

## 9. 为什么任务需要 `task_id`

因为长任务生命周期超出单次连接：

```text
Client disconnect
→ Task still exists
→ User reconnects
→ query by task_id
```

这也是 Long-running Agent API 的基础。

---

## 10. Progress 怎么返回

常见三种：

```text
Polling
GET /tasks/{id}

SSE
GET /tasks/{id}/events

WebSocket
双向控制 + progress
```

选择取决于交互需求。

不要把“有进度”默认等于 WebSocket。

---

## 11. Cancel 怎么设计

Long-running Task 的取消是业务状态：

```text
POST /tasks/{id}/cancel
```

后台 Worker 要看到 Cancel Request，停止后续工作，并清理中间状态。

这和关闭浏览器 Tab 不是同一件事。

---

## 12. 🎯 面试怎么回答

> FastAPI `BackgroundTasks` 更适合响应返回后的轻量进程内任务，不应该替代可靠任务系统。像 RAG Ingestion、OCR、长时间 Agent Run 这类任务，我会返回 202 + task_id，把执行交给持久化 Task State + Queue/Worker。大文件使用 UploadFile 和分块读写，避免一次把整个文件读进内存，并让后台任务自己创建 DB/HTTP 等资源。

---

## 13. 易错点

- ❌ BackgroundTasks = Celery / MQ。
- ❌ Response 返回后任务就一定能可靠执行完。
- ❌ UploadFile 说明文件永远都在内存。
- ❌ `await file.read()` 对任何大小文件都安全。
- ❌ 浏览器断开 = 后台任务取消。

---

## 14. 本章自测

<details>
<summary>1. 为什么重 OCR 不适合只用 BackgroundTasks？</summary>

因为任务可能耗时、CPU 重、需要跨进程/机器调度和失败恢复；进程内 BackgroundTasks 没有完整 Durable Task 语义。

</details>

<details>
<summary>2. `bytes` 与 `UploadFile` 对大文件的主要差异是什么？</summary>

`bytes` 会将整个上传内容放入内存；UploadFile 使用 spooled temporary file，适合大文件并提供 file-like 接口。

</details>

<details>
<summary>3. 为什么后台任务最好只接 task_id / file_id 等稳定标识？</summary>

这样任务能自己重建资源和上下文，不依赖已经结束的 Request-scoped Session/Connection，也更利于重试和恢复。

</details>
