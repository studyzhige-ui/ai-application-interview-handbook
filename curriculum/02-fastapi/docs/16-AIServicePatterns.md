# 16｜接口模式：把问答、任务与运行边界连起来

[← 上一章](15-Deployment与GracefulShutdown.md) · [模块主页](../README.md)

现在给你一个小需求：“团队成员可以问一个问题，查看返回依据；处理较久的任务可以稍后查询，也能请求取消。”这不是要把所有工具装上，而是判断每一项能力应由谁负责，再让接口行为能被验证。

本章用一个完整的离线接口模型，解释前面知识如何共同作用。它不是 RAG 算法实现，也不是可靠 Agent 执行引擎。随后把短请求、流式回答、文件处理和持久 Run 分别放回恰当的生命周期。

## 1. 从需求推导接口契约

这个解释模型的范围是：可信教学身份、问答输入与响应、证据展示、任务创建、查询与取消请求。我们明确选择以下规则：

- 没有有效身份返回 401，不能访问其他团队的任务。
- 提问不能为空，回答只返回公开字段。
- 创建任务返回 202 与 task_id，这个例子只创建待执行记录，不声称已执行。
- 对待执行任务发起取消可以变成 cancelled；重复取消不制造第二项任务。
- 本例的任务只在单进程内存，不持久、不自动恢复，不用于真实业务。

本章只解释这份 API 契约。可靠执行需要持久记录和执行者；Agent 怎样规划、调用工具和恢复，不由这张内存任务表实现。

## 2. 一个可以实际请求的接口模型

```python
# example: integrated_app
from typing import Annotated, Literal
from uuid import uuid4
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel, Field, field_validator

app = FastAPI()
bearer = HTTPBearer(auto_error=False)
TEAMS = {"demo-alice": "team-a", "demo-bob": "team-b"}
TASKS = {}  # 只用于本地单进程教学；重启丢失，不是持久任务系统

class Question(BaseModel):
    text: str = Field(min_length=1, max_length=200)

    @field_validator("text")
    @classmethod
    def nonblank(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("问题不能为空")
        return value

class Citation(BaseModel):
    source_id: str
    excerpt: str

class Answer(BaseModel):
    answer: str
    citations: list[Citation]

class TaskOut(BaseModel):
    task_id: str
    status: Literal["queued", "cancelled"]

def current_team(
    cred: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> str:
    team = TEAMS.get(cred.credentials) if cred else None
    if team is None:
        raise HTTPException(401, "需要有效凭证", headers={"WWW-Authenticate": "Bearer"})
    return team

Team = Annotated[str, Depends(current_team)]

@app.post("/ask", response_model=Answer)
def ask(question: Question, team: Team):
    # 确定性演示：实际问题内容被校验，但未实现语义检索或模型生成。
    return Answer(
        answer="这是接口契约演示，不是真实模型回答。",
        citations=[Citation(source_id=team + ":demo", excerpt="演示资料允许团队内部读取。")],
    )

@app.post("/tasks", response_model=TaskOut, status_code=202)
def create_task(question: Question, team: Team):
    task_id = uuid4().hex
    TASKS[task_id] = {"team": team, "text": question.text, "status": "queued"}
    return TaskOut(task_id=task_id, status="queued")

def owned_task(task_id: str, team: str) -> dict:
    task = TASKS.get(task_id)
    if task is None or task["team"] != team:
        raise HTTPException(404, "任务不存在或不可访问")
    return task

@app.get("/tasks/{task_id}", response_model=TaskOut)
def get_task(task_id: str, team: Team):
    task = owned_task(task_id, team)
    return TaskOut(task_id=task_id, status=task["status"])

@app.post("/tasks/{task_id}/cancel", response_model=TaskOut)
def cancel_task(task_id: str, team: Team):
    task = owned_task(task_id, team)
    task["status"] = "cancelled"
    return TaskOut(task_id=task_id, status="cancelled")
```

函数在这个简化场景中没有真正的执行中状态，因此取消只改变待执行记录。真实任务可能已经产生外部动作，不能把这一行赋值推广成任何任务都能立即安全取消。

## 3. 沿同一条任务推导状态与拒绝

1. Alice 身份 POST `/tasks`，输入 `{"text":"整理资料"}`，返回某个新 task_id。
2. Alice GET 这项任务，应该看到 queued。
3. Bob 用同一个 task_id 查询，应得到 404，不能读到 Alice 团队的任务。
4. Alice 发送 cancel，应看到 cancelled；再次取消仍是同一 task_id 的 cancelled。
5. 不带身份创建任务，或提交空白问题，应分别得到 401、422。

不要把随机 task_id 写死在测试里，应从创建响应中读取。也不要把返回的内部 text 或 team 假定为公开响应字段；TaskOut 明确只公开 task_id 与 status。

## 4. 短问答、流式回答与长期任务怎样分工

| 任务 | 连接内主要交付 | 连接外需要考虑 |
|---|---|---|
| 短问答 | 一次 JSON 答案和必要依据 | 质量与访问控制 |
| 流式回答 | 开始、内容、错误与终止事件 | 中断是否继续、是否可恢复 |
| 文件处理 | 上传结果、接受任务的标识 | 持久状态、阶段重试和结果查询 |
| Agent Run | 查询、事件、取消和批准入口 | 动态循环、工具动作、状态恢复 |

并非每个服务都必须实现四类接口。复杂度由任务要求决定，而不是为了满足“成熟系统至少有多少 Endpoint”的模板。

## 5. 从任务到 Session、Run 和事件

当系统开始长期与用户协作，可以把 Session 看成一段交互组织，Run 看成一次具体执行。一个 Session 可能包含多个 Run；具体对象含义须以产品契约为准，不是所有系统都使用同样命名。

Run 可提供创建、查询、事件、取消和批准等接口。批准应绑定具体动作和参数版本，不能把一次旧批准当成无限授权。接口传递请求，实际能否执行由运行系统校验。

```text
用户动作 → HTTP请求 → 身份与输入边界
                         ↓
                    业务/运行系统
                    ├─ 做什么、做到哪
                    ├─ 工具、模型和副作用
                    └─ 产生可信状态与事件
                         ↓
                    API/SSE适配
                         ↓
                    用户看到结果
```

FastAPI 不凭空完成 RAG 证据质量或 Agent 恢复。反过来，API 层也不能以“归 Runtime”为由不做身份校验、请求限制、批准对象校验和错误协议。

## 6. 幂等、版本与恢复要留下明确契约

客户端重试创建任务时，本例会创建一个新 task_id，**并未实现创建幂等**。正式设计若需要“一次用户操作只创建一次”，必须定义稳定操作键、参数一致性、保存结果和重复窗口；不能把随机 UUID 本身当作去重机制。

先把客户端重试后应得到什么写成契约，再让存储和执行系统实现它。随机编号用于区分任务；稳定的业务操作键用于识别同一次操作的重试，两者不能互相替代。

## 7. 把整条请求链收回到一个框架

以 Alice 创建任务为例：服务器接收 POST，路由匹配 `/tasks`；Pydantic 拒绝空白输入，身份依赖把凭证转成 team-a；处理函数创建记录，TaskOut 只公开编号和 queued；HTTP 202 表示本例已接收记录。Bob 查询同一编号时，owned_task 在返回内容前拒绝跨团队访问。每一步的输入、状态和结果都能由已有章节解释。

这里没有执行者，所以没有 running→succeeded；没有持久存储，所以进程重启后记录消失；没有稳定操作键，所以重复 POST 创建新任务。这些不是让读者补完才能毕业的作业，而是识别 API 示例边界的三个事实。

若业务需要持久执行，接下来学习 MySQL 的表、约束和事务，再在 Redis 与 Backend 中理解缓存、消息和幂等。存储接口可以隔离“按编号保存/读取”的实现变化，但仅换成数据库不会自动解决并发取消、重复领取和重启恢复；可靠性来自明确的事务、状态转换及执行协议。FastAPI 主线到这里形成的是完整 Web 边界框架，不要求读者额外建造一个任务平台。

---

## 本章小结

FastAPI 把业务能力转换成可调用、可校验、可观察的接口。完成一个接口模型与完成可靠执行系统是两件事。通过身份、契约、资源和失败证据连接各层，才能在后续数据库与 Backend 学习中逐步替换教学实现。

## 🎯 面试怎么回答

**只会 GET 和 POST 为什么不足以构建 Agent 服务？**

> 路由语法只是入口。还需要请求与响应契约、身份权限、资源与并发、事件协议、取消和任务状态、测试、观测、部署；动态执行与恢复由运行系统承担。

**run_id 为什么不能同时代表所有 Session 和连接？**

> 它们生命周期不同。一段交互可含多次执行，一次执行也可被多条先后连接观察；混用会让取消、恢复和事件归属不清楚。

## ⚠️ 易错点

> ⚠️ 内存任务表用于接口实验，不能被表述成持久、可恢复的生产执行系统。

> ⚠️ 返回 202 或 UUID 不等于已经获得可靠任务与创建幂等。

> ⚠️ 引用字段存在不证明答案被证据支持，真实 RAG 仍需质量与权限验证。

## 本章自测

先回答，再展开核对。结合正文例子，说出预期结果及原因即可。

<details>
<summary>1. Bob 能否靠知道 Alice 的 task_id 读取任务？</summary>

不能。owned_task 同时检查可信团队范围，标识不可猜测性不能替代授权。

</details>

<details>
<summary>2. 重复 POST/tasks 会发生什么，为什么？</summary>

本例每次生成新 UUID，可能产生多项任务。它没有实现业务操作去重，文档应明确这一边界。

</details>

<details>
<summary>3. 为什么把存储换成 MySQL 后仍要做重启和并发实验？</summary>

数据持久不自动保证状态转换、重复请求和跨进程执行正确，需要按真实事务与并发语义验证。

</details>

## 知识回看与权威资料

- [FastAPI 教程总览](https://fastapi.tiangolo.com/tutorial/)：核对接口各部分的官方实现。
- [后续：MySQL](../../03-mysql/README.md)：建立表、约束和事务基础。
- [后续：Backend](../../05-backend-engineering/README.md)：在数据库与 Redis 之后学习幂等、可靠任务与恢复。
- [Agent 执行系统](../../09-agent/README.md)：理解循环、工具、记忆与检查点的完整职责。
