# 03｜Pydantic、Validation、Serialization 与 Error Contract

FastAPI 的类型系统价值，不是“代码看起来更现代”，而是把：

```text
Untrusted Request
→ Parse
→ Validation
→ Typed Object
→ Business Logic
→ Response Validation / Serialization
```

变成一条明确的数据边界。

---

## 1. 为什么 API 层必须做 Runtime Validation

客户端传来的 JSON 本质上是不可信输入：

```json
{
  "top_k": -100,
  "temperature": "hot",
  "tenant_id": null
}
```

如果直接把原始 `dict` 传入深层业务逻辑，错误会在更远的位置才爆炸。

更合理：

```python
from pydantic import BaseModel, Field

class ChatRequest(BaseModel):
    message: str
    top_k: int = Field(default=10, ge=1, le=100)
```

API Boundary 尽早拒绝不满足 Contract 的输入。

---

## 2. Request Model 不等于数据库 Model

不要默认：

```text
Request Schema = ORM Model = Response Schema
```

它们服务不同边界。

例如用户创建：

```python
class UserCreate(BaseModel):
    email: str
    password: str

class UserOut(BaseModel):
    id: int
    email: str
```

Response 不应该把 password/hash 等内部字段意外返回。

---

## 3. FastAPI 怎样识别 Request Body

Pydantic Model 参数通常被识别为 Request Body：

```python
class QueryRequest(BaseModel):
    query: str
    top_k: int = 10

@app.post("/rag/query")
async def query(req: QueryRequest):
    ...
```

FastAPI 会：

```text
读取 JSON Body
→ 解析类型
→ Runtime Validation
→ 构造 Pydantic Object
→ 把 Schema 加入 OpenAPI
```

---

## 4. `Annotated` 为什么越来越常见

例如：

```python
from typing import Annotated
from fastapi import Query

async def list_items(
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
):
    ...
```

它允许把：

```text
Python Type
+ FastAPI Metadata / Validation Rule
```

组合起来，同时保留更清晰的类型信息。

---

## 5. Pydantic v2 的常用心智模型

在现代 Pydantic 中常见：

```python
obj = MyModel.model_validate(data)
data = obj.model_dump()
```

不要继续把历史版本里的 `.dict()` 等写法当成唯一当前接口。

课程重点不是背所有 Pydantic API，而是理解：

```text
External Data
→ Runtime Model Validation
→ Typed Data
→ Explicit Serialization
```

---

## 6. Schema Validation ≠ Business Validation

假设：

```json
{
  "refund_amount": 3000
}
```

Schema 可以验证：

```text
refund_amount 是 number
refund_amount > 0
```

但它不能仅靠类型判断：

```text
这个用户是否拥有订单？
订单是否允许退款？
额度是否超过策略？
是否需要人工审批？
```

因此正确分层是：

```text
Parse / Schema Validation
↓
Business Validation
↓
Authorization / Policy
↓
Execution
```

这和 Python Structured Output 章节里的 Trust Boundary 是一致的。

---

## 7. Response Model 为什么是安全边界

FastAPI 可以根据 Return Type 或 `response_model` 对输出进行验证、序列化和字段过滤。

例如：

```python
class UserInternal(BaseModel):
    id: int
    email: str
    password_hash: str

class UserOut(BaseModel):
    id: int
    email: str

@app.get("/users/{user_id}", response_model=UserOut)
async def get_user(user_id: int):
    return UserInternal(
        id=user_id,
        email="a@example.com",
        password_hash="secret",
    )
```

`response_model` 可以帮助过滤不应暴露字段。

⚠️ 但这不是“只要用了 response_model 就绝对安全”。真正的敏感数据边界仍需设计清楚。

---

## 8. Return Type 和 `response_model`

两种常见方式：

```python
@app.get("/items")
async def get_items() -> list[ItemOut]:
    ...
```

或：

```python
@app.get("/items", response_model=list[ItemOut])
async def get_items():
    ...
```

如果两者同时存在，FastAPI 的 `response_model` 会用于框架的响应模型处理。

什么时候使用哪种，更多是代码类型约束和框架 Contract 的权衡。

---

## 9. Validation Error、Business Error、Server Error 要分层

建议建立错误分类：

```text
Request Validation Error
Business Rejection
Authentication / Authorization Error
Downstream Failure
Internal Programming Error
```

不要所有异常都：

```python
except Exception:
    return {"error": "failed"}
```

这样会丢失错误语义，还可能错误返回 200。

---

## 10. `HTTPException` 应放在哪里

FastAPI 的 `HTTPException` 是 Web/API 层异常。

Service 层如果完全绑定 `HTTPException`：

```text
Domain Logic
→ FastAPI-specific Exception
```

会让业务代码很难脱离 HTTP 测试和复用。

更清晰：

```text
Domain / Service Error
↓
API Exception Mapping
↓
HTTP Status + Error Contract
```

---

## 11. 自定义 Exception Handler

可以把稳定业务异常映射成统一 JSON：

```python
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

class KnowledgeBaseNotFound(Exception):
    pass

@app.exception_handler(KnowledgeBaseNotFound)
async def kb_not_found_handler(request: Request, exc: KnowledgeBaseNotFound):
    return JSONResponse(
        status_code=404,
        content={"error": {"code": "KB_NOT_FOUND"}},
    )
```

这样比每个 Route 都手写相同 `try/except` 更稳定。

---

## 12. AI 场景：Structured Output 到 API Response

模型可能给：

```text
LLM raw output
→ parse structured result
→ domain validation
→ response model
→ client
```

不要直接：

```text
LLM text → return to frontend as trusted JSON
```

尤其 Tool / Agent 场景，模型结构化输出和 HTTP Contract 是两层不同的 Trust Boundary。

---

## 13. 🎯 面试怎么回答

> FastAPI 利用 Python 类型和 Pydantic 把 Request/Response Contract 变成 Runtime Validation 和 OpenAPI Schema。Request Validation 负责尽早拒绝结构不合法的外部输入；Response Model 可以验证、序列化并过滤输出字段。但 Schema Validation 不能替代业务校验和权限判断。真实项目里我会把 Domain Error 与 HTTP Error 分层，再在 API Layer 做统一 Exception Mapping。

---

## 14. 易错点

- ❌ Pydantic 只是自动补全工具。
- ❌ JSON 能 parse 就说明业务数据有效。
- ❌ Request Model、ORM Model、Response Model 应该共用一个类。
- ❌ `HTTPException` 应该从最深层 Repository 一路抛。
- ❌ 所有异常都转成 200 + `{success:false}`。

---

## 15. 本章自测

<details>
<summary>1. 为什么 `response_model` 可能是安全边界？</summary>

它能按声明的输出模型验证和过滤字段，减少内部敏感字段意外暴露。但安全仍依赖正确的模型设计和权限边界。

</details>

<details>
<summary>2. Schema Validation 和 Business Validation 有什么区别？</summary>

Schema 关心结构、类型、字段约束；Business Validation 关心订单状态、额度、资源存在性等业务 invariant。

</details>

<details>
<summary>3. 为什么 Service Layer 不应到处直接依赖 HTTPException？</summary>

HTTPException 是 FastAPI/Web 层概念。业务层保持框架无关的错误语义，更容易测试、复用，并能由不同入口映射成不同协议响应。

</details>
