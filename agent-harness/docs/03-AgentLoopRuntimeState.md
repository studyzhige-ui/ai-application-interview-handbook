# 03. Agent 循环、执行层级与新消息

[← 上一章](02-AgentWorkflowHarnessBoundary.md) · [模块目录](../README.md) · [下一章 →](04-ToolContractSchemaValidation.md)

> 本章要解决：一次工作到底怎样推进？Session、Run、Turn、Step 怎样帮助你描述执行，而不把产品术语混在一起？

## 1. 循环不是一直问模型，而是让观察改变下一步

Loop（循环）是重复执行的一段控制逻辑。报告任务中，模型先选择读取 A；程序读完后把 A 的内容作为 Observation（观察结果）交回模型；模型才有依据决定读取 B 还是起草报告。这个“新结果进入下一次决策”的反馈是循环的价值。

```text
目标与约束 → 构造当前输入 → 请求模型
                              ↓
                 工具候选 / 澄清请求 / 完成候选
                      ↓             ↓
             受控执行并得到观察     按任务要求核验
                      ↓             ↓
                 更新进展 ─→ 继续 / 等待 / 停止
```

“受控执行”先作为黑盒理解：只执行已注册且通过校验、授权的动作，返回可解释结果。04—07章逐步打开这个黑盒。完成候选同样不是直接成功，可能因缺引用而回到循环。

### 一个能运行的最小反馈循环

下面的模型由固定动作序列代替，只读取内存里的资料，不调用网络。它演示“拿到观察以后再推进”，不声称已经实现真实模型、安全沙箱或持久恢复。

```python
# runnable-example: minimal_feedback_loop
from collections.abc import Iterable

def run_report(actions: Iterable[dict], limit: int = 4) -> dict:
    docs = {"A": "发布日期待确认", "B": "发布日期为周五"}
    state = {"read": [], "observations": [], "status": "running"}
    for step, action in enumerate(actions, 1):
        if step > limit:
            state["status"] = "budget_exhausted"
            break
        if action.get("type") == "read":
            doc = action.get("id")
            if not isinstance(doc, str) or doc not in docs:
                state["status"] = "denied"
                break
            state["read"].append(doc)
            state["observations"].append(docs[doc])
        elif action.get("type") == "final":
            # 本例只验证所需文件已读，不证明报告语义正确。
            state["status"] = "completed" if {"A", "B"} <= set(state["read"]) else "incomplete"
            break
        else:
            state["status"] = "invalid_decision"
            break
    if state["status"] == "running":
        state["status"] = "no_final_result"
    return state

assert run_report([{"type": "read", "id": "A"}, {"type": "read", "id": "B"}, {"type": "final"}])["status"] == "completed"
assert run_report([{"type": "final"}])["status"] == "incomplete"
assert run_report([{"type": "read", "id": "secret"}])["status"] == "denied"
assert run_report([{"type": "read", "id": "A"}] * 3, limit=2)["status"] == "budget_exhausted"
assert run_report([{"type": "unknown"}])["status"] == "invalid_decision"
assert run_report([])["status"] == "no_final_result"
```

程序明确记住了已读内容和状态，所以State不是仅指计划；最后一条动作是`final`也不自动成功。真实Agent把固定动作来源换成模型请求，再加入后面章节的工具契约、取消与恢复能力。

## 2. 保留一棵清楚的教学树，但声明 Turn 的含义

为讲清故障发生在哪，本章先使用下列**自建运行时的工作约定**：Session 是连续会话，Run 是为一个目标启动的一次执行，Turn 是一次“模型决策—动作—观察”的循环轮次，Step 是其中的操作。用户输入称为“用户交互”，避免又叫同一种 Turn。

```text
Session：这个项目的持续会话
└─ Run：本次整理报告
   ├─ Turn 1：决定读 A → 读取 → 接收结果
   │  ├─ Step：模型请求
   │  └─ Step：工具调用与结果登记
   └─ Turn 2：发现日期冲突 → 读 B → 接收结果
```

这棵树让你能说“第二轮读取失败，但这次报告任务还可继续”，而不是所有问题都叫“会话失败”。**它不是全行业统一对象模型。** 业务的一次任务也可能暂停后继续同一 Run，或因用户明确要求从头做而创建新 Run；需项目自己定义。

### 对照产品语义，不强制一一对应

| 对象体系 | 含义 | 与教学树的关系 |
|---|---|---|
| Codex Thread | 持续对话容器 | 类似会话作用域 |
| Codex Turn | 用户输入发起的一段 Agent 工作，可含多次推理和工具交互 | 常覆盖教学例子中的整个执行段，而非单次模型调用 |
| Codex Item | 消息、工具行动等有类型项目 | 不是每条生命周期事件；一个 Item 可产生多个事件 |
| Claude Code 快照的 conversation / `submitMessage()` | 会话对象持有跨调用数据，提交消息推进交互 | 内部循环次数不应直接当用户 Turn 数 |

面试时先说“在我的实现里 Turn 指……”，再对照产品。清楚的自定义树可以帮助理解，但错误映射会让后面的取消与恢复范围混乱。

## 3. 用一个事件区分“模型说了什么”和“程序做了什么”

Message（消息）是交互内容；Event（事件）是发生过的事情。例如模型输出“读取 A”是一条工具调用消息；程序可能先发出“正在等权限”的事件，再发出“读取开始、读取完成”。权限等待和队列时长不必作为完整文本喂给模型。

需要关联的最小信息由问题决定。`call_id`把工具请求与结果连起来；两个读取并发返回时，不能只靠返回先后猜属于哪个请求。`event_id`区分事件本身；同一调用的开始与结束不是两个不同逻辑动作。

不要立刻给每条事件加五个版本号。一个小运行时用会话/执行标识、调用标识、事件类型和必要结果即可起步。第12章解释恢复要存什么，第19章解释排障额外记什么。

## 4. 用户在执行中又发了一句话，会怎样？

模型当前已发出的请求不能被客户端从中间随意修改。新输入应先由应用接收，再由运行时决定何时生效。

| 新输入意图 | 可采用的行为 | 用户应该看到什么 |
|---|---|---|
| 新增无关任务 | 排队到当前任务结束后新建执行 | 已排队，而非假装立即处理 |
| 补充当前任务信息 | 放入待处理输入，在下一次安全决策点追加 | 已接收，后续将使用 |
| 修改约束，例如“不要写文件” | 更新约束；按风险中断或等待当前动作结束 | 明确已经发生的动作和生效边界 |
| 明确取消 | 停止派发新动作并传播取消 | 取消中与真正结束分开 |

“安全决策点”通常是一次模型/工具阶段完成、控制权回到运行时的时刻。若写入已经提交，新约束不能倒流时间撤销它。07章详细讲传播和迟到结果。

<details>
<summary>具体落点：Codex 的排队/steer 与 Claude Code 的循环输入</summary>

Codex App Server 对正在运行的 Turn 提供 `turn/steer`（追加引导输入），并用预期 Turn 标识避免把新输入送给已结束或被替换的一轮；`turn/interrupt`用于中断。固定源码的 `session/turn.rs`检查待处理输入，决定是否还有后续工作。这个接口语义不同于“开始第二个同时修改同一状态的执行”。

用户提供的 Claude Code 快照中，`query.ts`在工具调用完成后读取按优先级筛选的排队输入，将符合当前Agent范围的内容作为附件加入后续消息，避免把普通用户消息插进未完成的工具请求/结果之间。Slash命令不按普通文本在轮中取出，需走自己的命令处理入口；`Tool.ts`另外提供工具中断行为。官方工作过程也说明用户可随时中断以引导方向。但具体界面是否排队、立即打断，取决于入口和运行模式，不能承诺所有客户端完全一样。

</details>

## 5. 终态不是一个 done 布尔值

状态名可以自定义，但含义必须区分：运行中、等工具、等用户/审批、成功、失败、取消。预算耗尽可以是失败原因或明确的停止原因，不能因为循环退出就显示“成功”。

如果工具参数有误，修正后可继续同一次 Run；如果身份校验失败，不应让模型自由换路径绕过；如果系统关闭，尚未有恢复能力的运行必须承认中断，而不是拿聊天历史假装完整恢复。

本章只建立控制骨架。是否持久化、从哪里恢复、如何核对外部写入，留给12—13章；这不是忘记保障，而是按学习依赖逐步展开。

## 面试怎么答

这些是依据本章机制设计的训练问法，不新增真人来源；先用自己的话回答，再看参考答案。

### 1. 怎样描述一个最小 Agent Loop？

<details>
<summary>参考答案</summary>

程序构造上下文并调用模型，分辨工具、澄清或完成候选。工具经过受控执行后形成观察，更新进展再请求下一次决策；完成候选经过任务验收后才能成功。循环还应有停止原因，不能把等待用户、预算耗尽和成功都当作同一种 done。

</details>

### 2. Session、Run、Turn、Step 怎么区分？

<details>
<summary>参考答案</summary>

我会先声明项目定义：Session 是会话，Run 是一次目标执行，Turn 可定义成一次决策反馈周期，Step 是内部操作。但 Codex 的 Turn 是一次用户请求及后续工作，可含多次模型调用，并使用 Item 表示类型化项目。应映射职责，不强制给所有产品套同一棵树。

</details>

### 3. Agent 运行中用户追加消息，能直接修改当前模型输入吗？

<details>
<summary>参考答案</summary>

已发送请求通常不能原地插入。应用先接收输入，区分新任务、补充、约束变更或取消，再排队、在下一决策点追加，或中断。需要绑定目标执行身份，防止误送；已发生的副作用不会因为新消息自动撤销。

</details>

### 4. Message 和 Event 的区别为什么重要？

<details>
<summary>参考答案</summary>

模型消息表达输入输出内容；运行事件还包括排队、授权、执行开始和检查点等程序事实。一个工具调用可能对应多个事件。用调用标识关联并发结果，而不是依赖文本或时间顺序；诊断事件也不必全部加入模型上下文。

</details>

## 高频易错点

| 容易混淆的说法 | 为什么不对，应怎样理解 |
|---|---|
| Turn 在所有产品里都等于一次模型调用 | 必须查看产品定义；Codex Turn可含多次推理与工具交互。 |
| 新消息总应立即打断所有动作 | 先识别意图和当前动作是否可安全中断。 |
| 循环 return 就是业务成功 | 可能等待、取消、耗尽预算；要有明确终态及验收。 |
| 事件越多，模型越懂运行过程 | 很多事件服务程序或排障，全部喂模型会制造噪声。 |

## 章节自测

先闭卷作答。答案不仅给结论，也解释判断依据；答不出时回到本章相应过程，不必从整套课程开头重读。

### 自测 1：一次 Codex Turn 可否读取文件三次？

<details>
<summary>查看参考答案</summary>

可以。Turn 包含用户请求后的一段 Agent 工作，模型可多次请求工具。每个工具项目及其事件有各自身份；不能把三次调用解释成必然三个 Codex Turn。

</details>

### 自测 2：两次读取先后反转返回，会混吗？

<details>
<summary>查看参考答案</summary>

正确协议用调用标识匹配请求和结果，不靠返回顺序。若只按时间追加两段无标识文本，模型可能误以为 B 的结果属于 A。

</details>

### 自测 3：用户说“稍后再检查 D”，必须取消正在读 A 吗？

<details>
<summary>查看参考答案</summary>

不必。若不改变当前安全边界，可以排队到合适的决策点。应用应明确接收与执行的差别，而不是让用户以为新任务已立即开始。

</details>

### 自测 4：用户说“别发送报告”，但发送已成功，应怎样显示？

<details>
<summary>查看参考答案</summary>

停止后续发送，核对既有回执，并告知已发送这一事实；不能只显示已取消就暗示发送被撤回。是否有撤回或补救能力由外部系统决定。

</details>

### 自测 5：一次参数错误使 Step 失败，Run 一定失败吗？

<details>
<summary>查看参考答案</summary>

不一定。可纠正错误能在预算内反馈后继续；不应重启整段任务或丢失已有进展。安全拒绝与系统损坏则有不同控制策略。

</details>

### 自测 6：需要保存模型的全部隐藏推理才能理解循环吗？

<details>
<summary>查看参考答案</summary>

不需要，也不能假设能取得。应记录必要的可观察输入、候选动作、实际执行结果和停止原因，用它们解释程序路径。

</details>

## 资料与下一步

产品接口：[Codex App Server](https://developers.openai.com/codex/app-server/)。固定源码：[Codex 输入与循环推进](https://github.com/openai/codex/blob/fc948f8c473e5d11e780ffcf1fd7f812a2020932/codex-rs/core/src/session/turn.rs)、[Claude Code query 循环](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/query.ts)、[Claude Code 工具契约](https://github.com/studyzhige-ui/claude-code-source-private/blob/58231dcce408f805c645cfbc352d2876b517223b/Tool.ts)。下一章定义循环所调用的工具究竟是什么。

本章对应研究能力：`AGENT-003`、`AGENT-004`、`AGENT-005`、`AGENT-006`、`AGENT-007`、`AGENT-042`。频次与原始证据以[研究题库](../../research/questions/agent-harness.md)为准。源码案例采用固定快照，官方文档采用明确版本；[核验范围](../../research/agent-sources/README.md#reader-revision-20260917)。

[← 上一章](02-AgentWorkflowHarnessBoundary.md) · [模块目录](../README.md) · [下一章 →](04-ToolContractSchemaValidation.md)
