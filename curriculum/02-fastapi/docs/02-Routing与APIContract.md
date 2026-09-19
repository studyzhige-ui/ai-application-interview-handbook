# 02｜Routing、Request / Response 与 OpenAPI Contract

学 FastAPI 时很容易一上来背：

```python
@app.get(...)
@app.post(...)
```

但真正应该理解的是：

> **一个 Route 本质上定义了“什么请求会匹配到这里、请求数据从哪里来、返回什么契约”。**

---

## 1. Route 是 API Contract 的入口

一个 Route 至少包含：

```text
HTTP Method
+ Path
+ Input Contract
+ Output Contract
+ Status / Error Contract
```

例如：

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class ChatRequest(BaseModel):
    message: str

@app.post("/chat")
async def chat(req: ChatRequest):
    return {"answer": req.message}
```

这里不是简单“给函数加了个装饰器”，而是声明了一个可被 HTTP 客户端调用的接口。

---

## 2. Path / Query / Header / Cookie / Body 怎么区分

FastAPI 会根据声明方式和类型信息把参数映射到不同请求位置。

```python
from typing import Annotated
from fastapi import FastAPI, Header, Query
from pydantic import BaseModel

app = FastAPI()

class SearchBody(BaseModel):
    query: str

@app.post("/users/{user_id}/search")
async def search(
    user_id: int,
    body: SearchBody,
    top_k: Annotated[int, Query(ge=1, le=100)] = 10,
    x_request_id: Annotated[str | None, Header()] = None,
):
    ...
```

心智模型：

```text
Path      → 资源定位
Query     → 检索/筛选/分页参数
Header    → 协议/上下文元数据
Cookie    → 浏览器会话类信息
Body      → 结构化业务输入
```

这些不是绝对规则，但能帮助设计一致 API。

---

## 3. HTTP Method 不只是“语法不同”

常见方法：

| Method | 常见语义 |
|---|---|
| GET | 读取资源 |
| POST | 创建 / 执行动作 / 提交复杂请求 |
| PUT | 整体替换或幂等更新 |
| PATCH | 局部更新 |
| DELETE | 删除 |

AI API 中 `/chat`、`/agent/runs`、`/rag/query` 常见 POST，因为输入通常是复杂 Body，而且请求可能触发执行。

但真正的幂等性语义不由 Method 名字自动保证，后面 AI Backend Engineering 会继续讲。

---

## 4. APIRouter 为什么重要

小 Demo 可以：

```python
@app.post("/chat")
...
```

但真实项目更适合按领域拆 Router：

```text
app/
├── main.py
├── routers/
│   ├── chat.py
│   ├── knowledge.py
│   └── agent.py
├── services/
├── schemas/
└── dependencies/
```

```python
from fastapi import APIRouter

router = APIRouter(prefix="/knowledge", tags=["knowledge"])

@router.post("/query")
async def query():
    ...
```

Router 的意义不只是“文件变少”，而是形成清晰的 API Boundary。

---

## 5. Router 不应该承担业务核心

坏例子：

```python
@app.post("/chat")
async def chat(req):
    # 查询数据库
    # 调 Redis
    # 做 RAG
    # 调模型
    # 写审计日志
    # 执行 Agent Loop
    # 全塞这里
```

更清晰：

```text
Router
  ↓
Request / Auth / API Contract
  ↓
Service
  ↓
Domain / Runtime / Repository / Provider
```

FastAPI Route 负责适配 Web 世界和业务世界，不应该变成所有逻辑的唯一容器。

---

## 6. OpenAPI 从哪里来

FastAPI 会利用：

- Path Operation；
- Python Type Hint；
- Pydantic Model；
- Dependency 中声明的参数；
- Response Model；

生成 OpenAPI Schema。

因此类型声明同时影响：

```text
Runtime Validation
+ Interactive Docs
+ Client Contract
+ Code Generation
```

这也是为什么“类型只是 IDE 提示”在 FastAPI 里是不完整的说法。

---

## 7. Status Code 是 API Contract 的一部分

例如：

```text
200 OK              请求成功
201 Created         创建成功
202 Accepted        已接受异步任务
204 No Content      成功但无 Body
400 Bad Request     请求语义不合法
401 Unauthorized    未认证
403 Forbidden       已认证但无权限
404 Not Found       资源不存在
409 Conflict        状态冲突
422 Validation      输入校验失败（FastAPI 常见）
429 Too Many Req    限流
500 Server Error    服务端异常
```

不要把所有失败都返回：

```json
{"code": 200, "success": false}
```

HTTP Status 本身就是协议的一部分。

---

## 8. Error Contract 要稳定

建议统一错误结构，例如：

```json
{
  "error": {
    "code": "KNOWLEDGE_BASE_NOT_FOUND",
    "message": "knowledge base not found",
    "request_id": "req_123"
  }
}
```

客户端真正依赖的是稳定 Contract，而不是 Python Exception Class 名字。

---

## 9. API Versioning 什么时候需要

如果外部客户端已经依赖接口，破坏性修改要谨慎。

常见策略：

```text
/v1/chat
/v2/chat
```

或 Header / Media Type Versioning。

不需要一开始就过度设计，但要认识到：

> **API Schema 一旦被外部系统依赖，就会成为长期兼容性成本。**

---

## 10. 🎯 面试怎么答“FastAPI 路由到底做了什么”

> Path Operation 不只是把 URL 映射到一个 Python 函数。它同时声明 Method、Path、参数来源、Request Schema、Response Schema、Status 和 Dependency，并参与 OpenAPI 生成。真实项目里 Router 应主要负责 Web Contract 和输入输出适配，核心业务逻辑放到 Service/Runtime 层。

---

## 11. 易错点

- ❌ GET / POST 只是装饰器名字不同。
- ❌ 所有参数都从 JSON Body 来。
- ❌ OpenAPI 只是 Swagger 页面。
- ❌ Router 越薄就完全不能做任何逻辑。
- ❌ 业务异常直接把 Python traceback 返回前端。

---

## 12. 本章自测

<details>
<summary>1. 为什么 Type Hint 会影响 FastAPI 的 Runtime 行为？</summary>

FastAPI 会根据类型声明解析输入、构建 Validation / JSON Schema，并用于 OpenAPI；它不仅服务静态检查。

</details>

<details>
<summary>2. Router 和 Service 的职责怎么区分？</summary>

Router 主要处理 HTTP Contract、参数、认证上下文和 Response；Service 承担可脱离 Web Framework 理解和测试的业务流程。

</details>

<details>
<summary>3. 为什么 Long-running Ingestion 更适合返回 202 + task_id？</summary>

因为任务可能远长于普通 HTTP Request 生命周期；API 可以先确认任务已接受，再通过状态接口或 Streaming 返回进度。Durable Task 的实现属于 Backend Engineering。

</details>
