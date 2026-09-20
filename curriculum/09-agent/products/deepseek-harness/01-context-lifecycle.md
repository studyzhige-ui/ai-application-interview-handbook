# 01. DeepSeek Harness Context Lifecycle｜从 Session Event 到真正的 Model Request

[← DeepSeek Harness 总览](README.md) · [Memory →](02-memory-lifecycle.md)

> **源码基线：** `deepseek-ai/deepseek-harness@ddefc45fbc7f8e46dd73185e68295696d1297887`

如果只看 DeepSeek Harness 最终发给 LLM 的 `messages`，会错过它最重要的 Context 设计。

这个产品不是先维护一份“当前聊天数组”，再偶尔把它存盘；恰恰相反：

> **Session Event Log（会话事件日志）是 durable truth（持久事实），Surface（模型可见表面）是从日志上投影出的当前 Context，而 `deriveMessages()` 只是发送请求前的最后一次读取。**

因此这一篇不从 Prompt 字段讲起，而从用户的一句话进入 Agent Inbox（智能体收件箱）开始。

---

## 1. 从 Inbox 到可重建的 Model Request

### 1. 用户输入先进入 Inbox，而不是立刻成为 Model Message

Agent 公共接口在：

- `packages/core/agent/`

默认 Driver 在：

- `packages/core/agent-loop/`

一个 Agent 有两类 pending input（待处理输入）：

~~~text
nextTurn
等待独立下一 Turn 的消息

nextStep
希望在当前 Turn 最近的 Step 边界进入的 steering / injected input
~~~

对外常见操作对应：

- `followup()`：排进 next-turn；
- `steer()`：排进 next-step，并唤醒 Driver；
- `inject()`：加入 model-facing context，但本身不唤醒 Driver。

这里有一个很关键的语义：

> **“消息已经被 Host 接受”不等于“消息已经进入模型历史”。**

它先是 Inbox 中的 pending work。

只有 Agent Loop 在 Step boundary（步骤边界）真正 claim（认领）以后，才有机会成为当前请求的一部分。

这让 Queue、Steer、插件注入和取消都可以在“还没提交到 Session History”之前有明确生命周期。

---

### 2. Turn 和 Step 在这里是两个真实层级

DeepSeek Harness 的 Session Log 会显式记录：

~~~text
turn/start
  step/start
  ...
  step/end
  step/start
  ...
  step/end
turn/end
~~~

一个 User Turn（用户轮次）里可能因为 Tool Call 发生很多 Step。

例如：

~~~text
用户：
修复测试

Turn 1
├─ Step 1：模型决定运行测试
├─ Tool Result
├─ Step 2：模型决定读文件
├─ Tool Result
├─ Step 3：模型修改文件
├─ Tool Result
└─ Step 4：模型给最终回答
~~~

这比笼统说“Agent Loop 一轮”更精确。

#### 为什么 Session 要把这些边界记录下来

因为 Retry、Approval、Compaction、Tool Pairing 都需要知道：

- 当前是否有 open turn；
-当前是否有 open step；
-失败发生在哪个 step；
-某个 tool/result 应该配对哪个 call。

这些都不是 UI 信息，而是恢复语义的一部分。

---

### 3. 每个 Step 开始前，Context 先经过 `agent/pre-step`

默认 Driver 的 `preStep()` 会先从 Inbox claim 当前应处理的消息。

然后它会调用：

- `ctx.systemPrompt.assemble(...)`
- Runtime Context projection；
- `agent/pre-step` waterfall（瀑布式扩展链）。

这一步是 DeepSeek Harness 很重要的 Context Extension Seam（上下文扩展接缝）。

插件可以在这里把新的 User-role Context 加进当前 Step。

例如：

- Workspace Instructions；
- Session Reference；
- Skill Catalog；
-用户直接调用的 Skill；
-当前 Permission / Sandbox policy 的 runtime context；
-其他插件提供的 context。

#### 为什么这些东西很多都用 User-role Message

因为 DeepSeek Harness 希望动态变化的信息：

~~~text
在当前历史后面追加
~~~

而不是每次都重写 System Prompt 的稳定前缀。

这对 KV Cache（键值缓存）很重要。

---

### 4. System Prompt 不是一个字符串，而是可组合的 Section / Context / Tool Schema

核心实现：

- `packages/core/system-prompt/src/index.ts`

`ctx.systemPrompt` 允许插件注册：

- Section；
- Context；
- Variable；
- Tool Schema Provider。

而且这些注册是 scoped（作用域化）的。

全局可以有一个默认 Persona，但 Agent scope（智能体作用域）里可以用同名 section shadow（覆盖）它。

因此两个 Agent 即使跑同一个 Agent Loop，也可以看到不同的：

- Persona；
- Tool Set；
- Runtime Policy；
- Subagent guidance。

#### `assemble()` 做什么

一次 assembly（组装）会：

1. 收集当前作用域下的 variables；
2. 合并 sections / contexts；
3. 收集当前可见 Tool Schemas；
4.按稳定顺序排列；
5.求值动态文本；
6.运行 `system-prompt/assemble` waterfall；
7.得到这一 Step 的完整 prompt assembly。

所以 Tool Catalog 变化和 Prompt 变化是同一个请求组装过程里的两个面。

---

### 5. AGENTS.md / CLAUDE.md 怎样进入 Context

对应实现：

- `packages/context/agent-instructions/`

DeepSeek Harness 会加载 Workspace Instructions（工作区指令），包括：

- `AGENTS.md`
- `CLAUDE.md`

Base bundle 默认给这个插件约 65,536 bytes 的 render budget（渲染预算）。

#### Baseline Instructions

Agent 启动时会根据：

- Session cwd；
- Project root；

计算 baseline instruction set（基础指令集合）。

它们会在首次相关 Step 通过 `agent/pre-step` 进入 accepted messages。

#### Nested / Changed Instructions

当成功执行文件：

- Read；
- Write；
- Edit；

插件会观察被触及的路径。

下一 Step 前再重新投影：

- 新发现的 nested instructions；
-已经修改的 instructions；
-已经删除的 instructions。

所以 Instructions 不是“启动时读一次就结束”。

#### 为什么这样做

大型仓库中：

~~~text
root/AGENTS.md
backend/AGENTS.md
ios/AGENTS.md
~~~

模型不需要一开始承担所有局部规则。

真正访问 backend 文件以后，才需要 backend 层约束。

---

### 6. 最重要的顺序：`agent/pre-step` 接受消息后，还没有立刻 commit

这是 DeepSeek Harness Context Lifecycle 最值得理解的一段。

`agent/pre-step` 返回：

~~~text
{ kind: 'enter', messages, ... }
~~~

并不等于这些 messages 已经写进 Session。

Agent Loop 接下来先执行：

~~~text
agent/request
        ↓
ctx.llm.prepareCall()
~~~

这两步决定：

-最终 provider；
-最终 model；
-reasoning effort；
-模型默认 max tokens；
-provider-specific request preparation。

只有路由准备成功以后，Loop 才真正 append 当前请求需要的 durable events。

#### 为什么不先写消息，再决定 model

假设：

1. 用户输入已经被写成 `user/message`；
2.随后 `prepareCall()` 因取消或路由错误失败；
3.模型其实从没看到这条输入。

如果 Resume 后只看日志，就会误以为：

> 模型已经消费过这条 Context。

DeepSeek Harness 因此把“Context Admission（上下文准入）”和“Durable Commit（持久提交）”分成两阶段。

这非常符合：

> **Model-visible means logged，反过来也要尽量避免 logged-as-visible-but-never-sent。**

---

### 7. Request Envelope 为什么也要持久化

路由成功后，Agent Loop 会根据需要追加：

- `request/header`
- `request/context`

#### `request/header`

用于记录一段 request series（请求序列）的关键配置，例如当前 provider / model 等。

如果模型路由不变，就不必每 Step 重复写完整 header。

#### `request/context`

当一些请求环境变化时追加，例如：

- provider / model context capacity；
- system-prompt update；
-相关 route context。

这样 Resume 不只是知道：

> “历史里有这些 messages。”

还知道：

> “这些 Assistant Turns 当时是在什么模型 envelope 下生成的。”

这也是为什么 Agent Model Switch（模型切换）可以在历史中留下清晰边界。

---

### 8. `system/message` 为什么会进入 Session Surface

System Prompt 最终也不是“每次请求临时拼完就忘掉”。

Agent Loop 会通过 System Prompt projection 判断当前组装结果是否需要写新的：

`system/message`

它成为 Surface 节点之一。

这样当前请求的 system head（系统头部）也能够从 Session 中重建。

如果 Prompt 一直不变，就不需要每 Step 增加重复 System Message。

所以稳定 Prompt 前缀可以持续复用。

---

### 9. `deriveMessages()` 才是最终 Model History

完成这一轮 durable admission 后，Agent Loop 调：

`session.deriveMessages()`

核心实现：

- `packages/core/session/src/index.ts`
- `packages/core/session/src/surface.ts`

它不是遍历所有 Event，然后全部发给模型。

它只看当前：

`session.surface.nodes`

然后把能形成模型消息的事件投影出来。

例如：

~~~text
system/message     → system role
user/message       → user role
assistant/message  → assistant role
tool/result        → tool result 对应的 user-side model message
~~~

而这些事件：

~~~text
turn/start
step/start
approval/asked
llm/retry
compaction/start
...
~~~

虽然是 durable facts，却不会自动变成 Model Message。

因此最准确的关系是：

~~~text
Session Log
包含“发生过什么”

Surface
定义“当前什么仍然对模型可见”

deriveMessages()
把 Surface 变成 LLM Message[]
~~~

---

## 2. Surface 与多层 Compaction：缩小模型视图，但不删历史证据

### 10. Surface 为什么是整个 Context 系统的关键抽象

Surface 支持两个核心操作：

~~~text
append
replace
~~~

普通新消息就是 append。

Compaction / Tool Result Pruning 则会产生 replace。

假设当前：

~~~text
Surface:
seq 0  system
seq 1  user
seq 2  assistant
seq 3  tool result
seq 4  assistant
seq 5  user
~~~

Compaction 可以新写一条 summary：

~~~text
seq 20 replacement user/message
surfaceOp:
  replace seq 1..4
~~~

于是模型看到：

~~~text
system
summary
user(seq 5)
~~~

但 seq 1..4 仍然在 Session Log 里。

这让：

- Debug；
-审计；
-恢复；
-来源追踪；

和模型 Context Budget（上下文预算）不必互相冲突。

---

### 11. Tool Result Pruner：先做 model-free 的便宜压缩

Base bundle 默认加载：

- `dsh-compaction-tool-result-pruner`

默认配置大致是：

- thresholdChars: 8192；
-headChars: 4096；
-tailChars: 1024。

超大 Tool Result 可以先做确定性的 head / middle / tail pruning（头中尾裁剪）。

它会追加：

- `compaction/prune` 记录；
-一个 replacement `tool/result`。

新的 Tool Result 只改变 model-facing content，但原始 Tool Event 仍留在日志。

#### 为什么它放在 Summary Compaction 前面

因为很多 Context 爆炸只是：

> 一个 Tool 输出太大。

这种问题不值得先花一次 LLM Summarization。

所以 Basic Compaction 在测到压力以后，会先调用可选 `toolResultPruner`，然后重新计量。

如果已经降到阈值以下：

> 不做 Summary。

这是一种很清晰的成本层级。

---

### 12. Basic Compaction：把“压缩”做成 durable transaction

默认 Compaction backend：

- `packages/compaction/compaction-basic/`

自动触发点主要有两类。

#### Step Boundary Pressure

在 `agent/pre-step` 时，通过：

`ctx.tokenMeter.measure(session)`

测当前 Surface。

如果达到当前模型 Context Window 的阈值，就尝试压缩。

#### Provider-confirmed Context Overflow

如果真实模型请求返回 context window exceeded：

`agent/request-error`

可以触发：

`compactIfNeeded(agent, 'context-overflow')`

成功改变 Surface 后返回：

`{ kind: 'retry' }`

让同一个 Step 重建请求。

这比单纯依赖本地 Token Estimate 更可靠，因为它还处理了：

> Provider 已经明确说这份请求放不下。

---

### 13. 为什么 Compaction 有 `start → summary → replacement → end`

真正区域压缩逻辑在：

- `compaction-basic/src/region.ts`

Compaction 先验证要压缩的 Surface range。

它不能：

-包含 System Head；
-切断 Tool Call / Tool Result pairing；
-压缩一个仍未闭合的 Step。

然后立即写：

`compaction/start`

这条 durable event 同时充当 Compaction Lock（压缩锁）。

之后才开始异步 Summarization。

成功以后再写：

- `compaction/summary`；
- replacement `user/message`；
- `compaction/end`。

#### 为什么先写 start

因为 Summary Request 可能很慢。

如果进程中途 crash，有一条 unmatched `compaction/start` 就能说明：

> 上一次压缩没有正常完成。

而不是只能猜。

---

### 14. Summary 为什么刻意复用原请求前缀

`compaction-basic/src/summarizer.ts` 的实现很值得学。

它没有构造一个全新的：

~~~text
System:
你是摘要模型
~~~

然后把历史重新塞进去。

相反，它尽量重放原会话的：

-同一 System Prompt；
-同一 Tool Schemas；
-原历史 prefix；

最后只追加一条：

> 现在请把上面的对话压成 checkpoint。

这样从 Provider 角度：

~~~text
原请求前缀几乎相同
        ↓
只有末尾 compaction instruction 是新增
~~~

因此更容易复用已经暖起来的 KV / Prompt Cache。

这说明 Cache 不是 API 层的附加优化，而是 Compaction Prompt 设计本身的约束。

---

### 15. Summary 不是“生成了就算成功”

DeepSeek Harness 会继续验证：

-输出必须有有效文本；
-不能带 image；
-不能因为 max tokens 截断；
-压缩后的 summary 必须真的比被 shadow 的内容更小；
-异步 Summarization 期间原 Surface 不能发生不允许的变化。

否则不会把它当成功 checkpoint。

尤其手动 Compaction 还会区分：

- busy；
-changed；
-summary；
-commit；
-persistence；

这些失败阶段。

这让“压缩失败”不再是一个模糊 Error。

---

## 3. 运行中的结果怎样继续进入下一次 Context

### 16. Streaming 为什么不直接作为历史真源

Agent Loop 会向：

`agent/assistant-stream`

发出 live frames（实时帧）。

UI 可以边生成边显示。

但 Session 不会每个 token / delta 都变成模型历史。

流结束后，Runtime 才把完整结果压成：

`assistant/message`

如果一个 attempt 失败且不能作为完整 Assistant Message，才使用：

`assistant/attempt`

记录这次尝试。

#### 这样有什么好处

如果每个 streaming chunk 都是 replay source：

-恢复要重新拼 delta；
-中断流容易出现半条消息；
-UI transient state 和 durable state 混在一起。

当前设计把它们分开：

~~~text
Live Stream
给当前 UI / observer

Durable Settlement
给 Resume / Model History
~~~

---

### 17. Tool Result 怎样回到下一次 Context

Assistant Message 中有 Tool Call 时，Agent Loop 会执行工具。

核心顺序：

~~~text
append tool/call
→ Runtime dispatch
→ append tool/result
~~~

Tool Result 是 Surface Message Producer。

所以下一次 `deriveMessages()` 会把它自然放进模型历史。

Tool 还可以返回：

`additionalContexts`

这些不会在 Tool Body 仍未结束时偷偷注入当前请求，而是进入 next-step Inbox，等下一个 Step 边界再成为可追踪 Context。

因此 Tool Execution 和 Context Injection 之间也有明确 commit boundary。

---

### 18. Cross-session Reference 怎样进入当前 Context

Session Reference：

- `packages/context/session-reference/`

当用户明确引用另一个 Session 时，Resolver 会在 `agent/pre-step`：

1. 解析 canonical `dsh-session:` reference；
2.读取源 Session 当前 Surface 的一个 snapshot；
3.按 byte budget 截断；
4.把用户原消息里的 mention 改成可读 label；
5.紧接着插入第二条 user-role `Referenced sessions` context。

这个 snapshot 一旦进入目标 Session，就是**不可变捕获**。

之后源 Session 再变化，不会反向改变目标会话历史。

这满足：

> Model-visible means logged。

---

## 4. 把完整 Context 生命周期串起来

用户说：

> “参考昨天那个支付重构会话，继续修现在这个测试失败；遵守当前 backend 目录的 AGENTS.md。”

#### Step 1 admission

当前消息进入 next-turn Inbox。

Driver 开：

`turn/start`

#### Pre-step

系统组装当前 Prompt。

Agent Instructions 插件准备 root / backend instructions。

Session Reference 插件识别另一个 Session，捕获它的有限只读 snapshot。

Skill Catalog 等其他 Context 也可以一起进入 batch。

#### Request routing

`agent/request`

选择 DeepSeek provider / model。

`prepareCall()`

确认模型能力和 exact request defaults。

#### Durable commit

现在才写入：

- System Message；
-用户问题；
-Workspace Instructions；
-Referenced Session Snapshot；
-Request Header / Context。

#### Derive

`deriveMessages()` 从 Surface 形成真正模型 History。

#### Model → Tool

模型先运行测试。

Tool Call / Result 都进入 Session Log。

Result 很大，下一 Step 前 Tool Result Pruner 可能先替换它的模型可见版本。

#### Context pressure

任务继续很长，Token Meter 达到阈值。

Basic Compaction：

-写 `compaction/start`；
-用相同 Prompt / Tools prefix 做 Summary；
-写 checkpoint replacement；
-写 `compaction/end`。

原始历史还在 Session Log，但模型只看新的 Surface。

#### Resume

进程退出后重启。

JSONL Persistence 恢复 Session Event Log。

Surface 重新投影。

下一次 `deriveMessages()` 得到和压缩后语义一致的 Context，而不是简单把所有原始 Event 全塞回模型。

这就是 DeepSeek Harness 的完整 Context Lifecycle。

---

## 5. 源码锚点

建议按因果链阅读：

1. [`packages/core/agent/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/agent/README.md)：Agent、Inbox、Create / Resume、Live Event。
2. [`packages/core/agent-loop/src/agent.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/agent-loop/src/agent.ts)：Turn / Step / Request / Stream / Tool Loop。
3. [`packages/core/session/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/session/src/index.ts)：Session Log 和 `deriveMessages()`。
4. [`packages/core/session/src/surface.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/session/src/surface.ts)：Surface append / replace。
5. [`packages/core/system-prompt/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/system-prompt/src/index.ts)：Prompt / Context / Tool Schema assembly。
6. [`packages/context/agent-instructions/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/context/agent-instructions/src/index.ts)：AGENTS.md / CLAUDE.md 动态进入 Context。
7. [`packages/context/session-reference/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/context/session-reference/README.md)：Cross-session Snapshot。
8. [`packages/compaction/compaction-basic/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/compaction/compaction-basic/src/index.ts)：Pressure / Overflow trigger。
9. [`packages/compaction/compaction-basic/src/region.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/compaction/compaction-basic/src/region.ts)：Durable Compaction Transaction。
10. [`packages/compaction/compaction-basic/src/summarizer.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/compaction/compaction-basic/src/summarizer.ts)：Cache-preserving Summary。
11. [`packages/compaction/compaction-tool-result-pruner/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/compaction/compaction-tool-result-pruner/src/index.ts)：Tool Result 的确定性裁剪。

下一篇：[Memory Lifecycle →](02-memory-lifecycle.md)
