# 03. DeepSeek Harness Tool Lifecycle｜从 ToolDefinition 到 Policy、PTC、MCP 与结果回填

[← Memory](02-memory-lifecycle.md) · [DeepSeek Harness 总览](README.md) · [Engineering & Evaluation →](04-engineering-evaluation.md)

> **源码基线：** `deepseek-ai/deepseek-harness@ddefc45fbc7f8e46dd73185e68295696d1297887`

DeepSeek Harness 的 Tool 系统最不应该被简化成：

> “模型输出 function call，Host 执行函数，再把字符串塞回去。”

真实生命周期更像：

~~~text
Plugin 注册 ToolDefinition
        ↓
Scoped Tool Registry
        ↓
System Prompt Assembly 读取 Tool Schemas
        ↓
模型产生 tool-call
        ↓
先 durable 写 tool/call
        ↓
参数校验
        ↓
tools/pre-execute
        ↓
monotonic guard
        ↓
必要时 Approval
        ↓
tools/execute wrappers
        ↓
Tool Body
        ↓
canonical JSON value
        ↓
tools/post-execute
        ↓
finalizeContent
        ↓
frozen final outcome
        ↓
durable tool/result
        ↓
下一 Step 的 Context
~~~

MCP、Skill、Filesystem、Bash、Subagent 甚至 PTC（Programmatic Tool Calling，程序化工具调用）最终都复用这套控制面。

---

## 1. 一个 ToolDefinition 为什么同时有 Value 和 Content

核心实现：

- `packages/core/tools/`

一个 Tool 最基本需要定义：

- name；
-description；
-parameter schema；
-output schema；
-output renderer；
-`execute()`。

这里最值得理解的不是字段，而是：

> **Tool 的 canonical value（规范值）和模型最终看到的 content（内容投影）是两层。**

例如一个 Tool 真正返回：

~~~json
{
  "path": "/tmp/report.json",
  "count": 42,
  "items": [...]
}
~~~

这是 execution-local canonical JSON value。

然后纯函数 renderer 可以把它投影成：

~~~text
Found 42 items.
Report: /tmp/report.json
~~~

供模型读取。

### 为什么不直接让 Tool 返回字符串

因为同一个 Tool Result 可能同时服务：

- Model；
-PTC 程序；
-Host UI；
-Post-execute Policy；
-Telemetry；
-持久化。

如果唯一真值就是一段自由文本：

> Programmatic consumer 无法可靠拿结构化结果。

而如果唯一真值就是复杂对象：

> 模型 Context 又可能极度膨胀。

所以 DSH 把：

~~~text
Canonical Value
和
Model Projection
~~~

分开。

---

## 2. Tool Registry 也是 Scoped 的

`ctx.tools` 不是一个全局不可变 Map。

Tool registration（工具注册）和 Prompt Section 一样，可以绑定 Cordis scope（作用域）。

这意味着：

-全局 Tool；
-Agent-only Tool；
-某个 Preset 下的 Tool；
-临时 Plugin 提供的 Tool；

可以并存。

Agent 的 Tool View（工具视图）还可以通过：

`ctx.tools.restrict(filter)`

进一步收窄。

### 为什么这对 Subagent 很重要

一个 Parent Agent 有：

~~~text
Bash
Edit
Deploy
DatabaseAdmin
~~~

并不意味着 Child Agent 自动拥有同样权限。

Subagent 创建时会有自己的 scope，再根据 composition / filter 形成自己的 Tool Set。

这种隔离发生在 Tool Registry 层，不只是 Prompt 里写一句：

> “你不要使用 Deploy。”

---

## 3. 模型真正看到的 Tool Schema 从哪里来

System Prompt Service 在：

- `packages/core/system-prompt/`

每次 `assemble()` 会从当前 Agent Scope 读取 Tool Schema Provider。

Tool Runtime 只把模型需要的部分暴露出去，例如：

- name；
-description；
-parameter schema。

而这些运行时内部细节不会上 wire：

- `execute` function；
-output renderer；
-timeout；
-finalizeContent；
-UI presenter。

这维持了一个清晰边界：

> **Wire Contract（模型协议）和 Runtime Implementation（执行实现）不是同一个对象。**

---

## 4. 模型 Tool Call 为什么必须先写 `tool/call` 再执行

Tool 调度主要在：

- `packages/core/agent-loop/src/tool-calls.ts`

当 Assistant Message 含有 Tool Calls 时，Agent Loop 会先 append：

`tool/call`

然后才 dispatch（分发）真实执行。

这不是多余日志。

假设模型调用：

> 删除一个远端资源。

真实副作用发生以后，进程立刻 crash。

如果 Session 中连“模型要求执行什么”都没有：

> Resume 根本无法判断外部世界可能发生过什么。

当前设计至少保证：

~~~text
tool/call 已 durable
        ↓
执行开始
        ↓
如果正常完成
tool/result durable
~~~

Crash Recovery 后可以区分：

- Call 根本没开始；
-Call 可能开始，但没有可靠 Result；
-Call 有完整 Result。

后面的 Engineering 篇会看到，这直接决定 Resume 时用什么 synthetic error 提醒模型。

---

## 5. Argument Validation 为什么发生在执行前，而且参数不能被任意重写

Tool Runtime 会先把模型提供的参数：

-检查为 lossless JSON；
-按 Tool Parameter Schema 验证；
- materialize；
-deep freeze（深冻结）。

然后才进入 Policy Pipeline。

这有一个很成熟的设计：

> **`tools/pre-execute` 可以决定 allow / deny / ask，但不能偷偷重写已经记录和展示的 Tool Arguments。**

为什么？

因为一旦模型历史里记录：

~~~json
{"path":"safe.txt"}
~~~

而 Policy 实际偷偷执行：

~~~json
{"path":"secret.txt"}
~~~

就会产生四套不一致：

-模型以为执行 safe；
-UI 展示 safe；
-Audit 记录 safe；
-真实副作用是 secret。

DSH 因此把“Argument Rewrite”排除在 Pre Tool Decision 之外。

历史、权限和执行必须对同一个 Call 达成一致。

---

## 6. `tools/pre-execute` 解决什么

这是第一层 extensible policy（可扩展策略）。

监听器可以：

- allow；
-deny；
-cancel；
-ask。

### deny

直接变成一个 Tool Error Result，不执行 Tool Body。

### cancel

产生规范 cancellation result。

### ask

调用 Approval Service。

只有：

`allowed-once`

才继续执行。

其他结果：

- rejected；
-cancelled；
-unavailable；

全部 fail closed。

### 为什么 missing approval 也要 deny

Headless deployment（无界面部署）很可能没有人能弹批准框。

如果 Tool 说：

> “需要 approval。”

但没有 Approval Service / Answerer，然后 Runtime 默认执行：

> 安全模型就失效了。

所以“没有人能批准”不是 allow。

---

## 7. 为什么 Pre-execute 后面还有 Monotonic Guard

Tool Runtime 还支持：

`ctx.tools.guard()`

Guard（守卫）只能做一件事：

> **进一步 deny。**

它不能返回 allow 去覆盖前面别人的 deny。

因此它是 monotonic（单调的）。

假设：

~~~text
Policy A：
deny /etc/passwd

Policy B：
allow all reads
~~~

如果所有 Hook 都能自由覆盖，注册顺序可能导致：

> 最后一个 allow 把安全拒绝洗掉。

Guard 没有 allow vocabulary（允许词汇），所以只能缩小权限。

这是很适合安全规则 / invariant enforcement（不变量强制）的设计。

---

## 8. Approval 是 Tool Pipeline 的一层，不是 Tool Runtime 本身

Approval Service：

- `packages/interaction/user-approval/`

它回答一个封闭问题：

> **这一次具体动作允许继续吗？**

Outcome 只有：

~~~text
allowed-once
rejected
cancelled
unavailable
~~~

没有永久授权。

每个 request 会生成 ApprovalRequestId，并在 Session Log 写：

~~~text
approval/asked
approval/decided
~~~

这些 audit events 不进入模型 Context。

模型只看到最终 Tool Result。

### 为什么 Approval 不带一份完整 Tool Args 副本

源码设计让 Approval Request 可以通过 `callId` 关联 UI 已经展示的 Tool Call。

避免再复制一份参数。

否则 UI 和 Approval Payload 之间可能产生 drift（漂移）。

---

## 9. Permission Preset 为什么不是新的安全机制

用户界面更希望看到：

~~~text
read-only
workspace-write
danger-full-access
~~~

而不是分别操作：

- Sandbox mode；
-Approval policy。

所以：

- `dsh-permission-presets`

把两个独立 knob（旋钮）组合成一个 UX preset。

Base bundle 的主要组合是：

~~~text
read-only
= sandbox read-only + approval ask

workspace-write
= sandbox workspace-write + approval ask

danger-full-access
= sandbox danger-full-access + approval never
~~~

但执行时仍然分别由：

- Sandbox；
-Approval；

负责。

这说明 Permission Preset 是：

> **用户级配置组合。**

不是第三套 enforcement engine。

---

## 10. Sandbox 管的是文件副作用，不是所有安全问题

Process Sandbox：

- `packages/sandbox/sandbox/`
- `packages/sandbox/sandbox-local/`
- `packages/sandbox/sandbox-policy/`

主要模式：

~~~text
read-only
workspace-write
danger-full-access
~~~

当前 Sandbox vocabulary 明确主要约束：

> **Filesystem Effect（文件系统副作用）。**

网络访问和进程可见性不自动由这个 mode vocabulary 覆盖。

所以不能说：

> “进了 Sandbox 就什么都安全了。”

### per-call policy

Sandbox Policy 不是一个全局开关。

每次 capability call 都会 resolve：

- mode；
-workspaceRoot；
-sessionId。

这允许：

~~~text
Agent A:
workspace-write /repo/a

Agent B:
read-only /repo/b
~~~

同时使用同一个 Sandbox Provider。

---

## 11. Local Sandbox Provider 怎样做到 fail closed

当前 Local Provider 会根据平台选择：

- Linux：Bubblewrap / Landlock；
- macOS：Seatbelt；
- Windows：ACL restricted-token backend。

如果 requested mode 需要 confinement，但平台没有可用 runner：

> 抛 `SANDBOX_UNAVAILABLE`。

不会静默退化成 unrestricted execution。

Provider 还会返回：

- enforcement: full / partial；
-denial signatures；
-runner failure rules。

这样 Bash Consumer 可以区分：

~~~text
命令自己失败

vs

Sandbox 正确阻止了文件操作

vs

Sandbox Runner 根本没成功启动命令
~~~

这对错误诊断非常重要。

---

## 12. `tools/execute` 为什么是 Around-dispatch Wrapper

通过 Pre Policy 和 Guard 后，调用进入：

`tools/execute`

这层适合实现：

- timeout；
-retry；
-metrics；
-execution wrapper。

Wrapper 可以代理下游执行。

唯一比较特殊的是：

> 它可以临时替换 signal。

但 Runtime 会重新把原 caller signal fuse（融合）回来，不能通过 Wrapper 丢掉用户取消。

因此取消 authority（取消权）仍然属于上游 Caller。

---

## 13. Tool Body 返回以后为什么还不能立刻写 Result

Tool Body 返回 canonical value 后，Runtime 还要经过：

`tools/post-execute`

Post Policy 可以：

-接受原结果；
-替换 model-facing content；
-替换 canonical value；
-附加 additional context；
-block 并变成 corrective error。

### 替换 Value 和 Content 为什么互斥

如果同时说：

~~~text
value 换成 A
content 换成 B
~~~

谁才是权威？

DSH 要求一次决策只选一类：

-换 value：重新 schema validate，再重新 render；
-换 content：保留 canonical value，只改展示；
-block：删除 success value，变成 error。

这让每一层语义保持明确。

---

## 14. `finalizeContent` 为什么在 Post Policy 后面

某些 Tool 的最终 model content 需要结合执行后信息。

例如 MCP Tool 的 canonical result 里可能包含：

- text；
-image；
-resource links；
-structured content。

MCP Bridge 可以先保留完整 canonical value。

Post Policy 如果没有改掉结果，再由：

`finalizeContent`

完成最终模型投影，例如把支持的 Image 写到 Attachment Store，生成 durable reference。

如果 Post Policy 已经 Block / Replace：

> MCP 自己的 finalize 不应该再把旧结果强行装回来。

这保证 Policy 层更 authoritative（权威）。

---

## 15. `tools/result` 是观察点，不是再修改点

所有 normalization（规范化）完成以后，Runtime deep freeze：

- ToolExecution；
- ToolExecutionResult。

然后发：

`tools/result`

这一步是 observe-only（只观察）。

为什么？

如果 Telemetry Listener、UI Listener 还能修改最终结果：

> Durable `tool/result` 和不同 observer 看到的内容会不一致。

所以最终观察面应该不可变。

---

## 16. Agent Loop 为什么并发执行，却按模型顺序提交 Result

一条 Assistant Message 可能同时要求：

~~~text
Read A
Read B
Read C
~~~

如果 Tool 都声明 concurrency-safe（并发安全），Agent Loop 可以 bounded parallel（有界并发）执行。

但 durable settlement（持久提交）仍按：

> **模型 Tool Call 顺序。**

也就是说：

~~~text
A、B、C 可以并发跑

即使 B 先完成，
日志仍按 A → B → C commit
~~~

这样模型历史不会因为网络 / 文件速度不同而每次产生随机顺序。

### Exclusive Tool

如果某 Tool 被判定为 exclusive：

> 它形成 ordering barrier（顺序屏障），单独执行。

而且 Runtime 会在真正启动一个 pending call 之前重新查询 execution mode。

所以 Tool Registry 在等待期间发生变化，也能影响尚未开始的调用。

---

## 17. Cancellation 时为什么还要给“未启动 Tool”补结果

假设模型一次请求了 5 个 Tool。

前两个已经启动。

此时用户取消。

Runtime 会：

-停止继续启动后续 Tool；
-等待已经开始的调用收敛；
-对从未 dispatch 的 Call 写 synthetic Tool Result：

`TOOL_ABORTED_BEFORE_DISPATCH`

为什么不能把后 3 个 call 留成没有 Result？

因为下次 Model History 中：

~~~text
assistant: tool-call X
但找不到对应 tool-result
~~~

会破坏 Tool Pairing invariant（工具配对不变量）。

所以取消也必须让 Context 保持 protocol-valid（协议有效）。

---

## 18. PTC 是什么：让模型用代码编排 Tool，而不是一次只 Call 一个

Tool Runtime 支持三种 presentation mode（呈现模式）：

~~~text
native
ptc
both
~~~

Native 就是普通 Function Calling。

PTC = Programmatic Tool Calling（程序化工具调用）。

在 PTC mode 下，模型主要看到：

`run_code`

以及根据当前 Tool Schemas 生成的 typed SDK（类型化 SDK）。

模型可以写类似 TypeScript：

~~~ts
const a = await tools.read_file(...)
const b = await tools.search(...)
return { a, b }
~~~

### 为什么这很有价值

复杂任务可能需要：

-循环；
-条件；
-并发；
-组合多个 Tool Result。

如果每一步都回模型一次：

> LLM round-trip 很多。

PTC 允许在一个程序里完成一段 deterministic orchestration（确定性编排）。

---

## 19. PTC 不是绕过 Tool Permission

这是最容易误解的地方。

`run_code` 里的每个 host binding call（宿主绑定调用）最终仍然重新进入普通 Tool Runtime。

也就是说：

~~~text
PTC Program
→ tools.foo()
→ Tool Runtime
→ pre-execute
→ guard
→ approval
→ execute
→ post-execute
~~~

所以模型不能通过：

> “把危险 Tool 放进 TypeScript 里调用”

绕开 Permission。

PTC 只是新的 orchestration surface（编排表面），不是新的 authority（权限）。

---

## 20. PTC Runtime 本身又怎样隔离

默认 Node PTC Runtime：

- `packages/ptc-runtime/ptc-runtime-node/`

每次调用启动 fresh Node process（新 Node 进程）。

它有：

- elapsed timeout；
-max output bytes；
-V8 heap limit；
-bounded pending host calls；
-managed process cleanup。

而且使用和 Bash 相同的：

- Sandbox Policy；
-Sandbox Provider。

Program-visible `process.env` 会被清空，Host 和 Child 通过受限 control channel 通讯。

因此 PTC 不等于：

> “给模型一个无限制 node -e。”

它是另一条受控执行能力。

---

## 21. Skill 怎样建立在 Tool Runtime 之上

Skills 分为：

- `dsh-skill`：Skill Registry；
-`dsh-skill-filesystem`：Filesystem Provider；
-`dsh-tool-skill`：模型可见 Loader。

### 第一阶段：只发布目录摘要

Tool Skill 会在 `agent/pre-step` 读取当前可见 Skills。

把：

- name；
-有界 description；

渲染成：

`<available_skills>`

并作为 durable user-role context 写入 Session。

完整正文此时不进入 Context。

### 第二阶段：模型按需调用 `skill`

模型判断某个 Skill 相关后：

~~~text
skill({ name })
~~~

Tool Runtime 再真正读取完整 Skill Content。

### 用户显式 `/name`

如果 direct user message 明确包含一个 user-invocable Skill gesture：

> 直接由 pre-step 加载完整内容。

无需模型先调用 Loader。

这仍然符合 Progressive Disclosure（渐进展开）。

---

## 22. Skill Catalog 为什么也要 durable

Skill Provider 可以在运行时变化。

假设 Session 开始时：

~~~text
skill A
skill B
~~~

后来变成：

~~~text
skill B
skill C
~~~

Tool Skill 会检测 digest 变化，写一个完整 replacement catalog message。

因此 Resume 能知道：

> **当时模型被告知哪些 Skill 可用。**

而不是用今天磁盘上的 Skill 目录反推昨天模型知道什么。

这再次体现“model-visible means logged”。

---

## 23. MCP Tool 怎样进入普通 Tool Runtime

MCP Client：

- `packages/mcp/mcp-client/`

每个配置实例连接一个 MCP Server。

Discovery 成功后，把远端 Tool 转成普通 DSH ToolDefinition。

Model-facing name：

`mcp__<serverName>__<rawName>`

### 为什么 Server Name 来自本地配置，不信远端

远端 `serverInfo.name`：

-可能不唯一；
-可能升级后变化；
-本身也是不可信数据。

所以 public tool identity（公开工具身份）由本地配置的 `serverName` 决定。

Raw name 仍然只用于真正 `tools/call` Wire Protocol。

---

## 24. MCP Tool 更新为什么要“整代替换”

MCP Server 可能动态改变 Tool List。

DeepSeek Harness 不会：

> 一个个边发现边覆盖当前 registry。

它把一次 sync（同步）看成 generation（代）。

新 Tool Set 全部成功注册后，才替换旧 generation。

如果：

- discovery 失败；
-同名冲突；
-schema 有问题；

旧 Tool Generation 继续工作。

这样不会出现：

~~~text
20 个 Tool
更新到第 11 个失败
→ Registry 进入半新半旧
~~~

这是很重要的原子更新策略。

---

## 25. MCP 断线时为什么最后已知 Tool 还先保留

MCP Connection Supervisor 有 reconnect policy（重连策略）。

断线时：

-最后已知 Tool 仍保持注册；
-调用在 outage（故障窗口）内可能失败；
-后台指数退避重连；
-成功后重新 sync Tool Generation。

达到最大连续失败次数以后：

-Tool 才 unregister；
-停止自动重连，等待 reload / restart。

这样短暂断线不会让 System Prompt Tool Schema 每几秒来回增删，减少能力面抖动和 Cache churn。

---

## 26. MCP Memory 为什么不需要一条特殊 Tool Pipeline

Memory 篇已经讲过：

> 第三方 Memory 通过 MCP。

这在 Tool 架构上几乎没有特殊逻辑。

Memory Provider 的：

- write；
-search；
-read；

最终都只是：

~~~text
MCP Tool
→ 普通 DSH Tool Runtime
→ 相同 Validation / Policy / Result Pipeline
~~~

这正是 Capability Seam（能力接缝）的价值：

> 新领域能力不需要重新发明一套 Tool 安全模型。

---

## 27. 一个完整 Tool Call 例子

用户说：

> “搜索项目里所有旧 API 的调用，然后用 Memory Server 记住迁移原则，最后修改代码。”

### 模型请求

当前 Tool Schemas 包含：

- grep / fs；
-MCP memory tools；
-skill；
-Bash。

### Search

模型 Call 搜索 Tool。

Agent Loop 先 durable：

`tool/call`

Runtime 校验参数。

Pre Policy allow。

Guard 没有拒绝。

Tool Body 返回 canonical search result。

Renderer 生成 model-facing content。

写：

`tool/result`

### Memory Write

模型调用：

`mcp__memory__write`

MCP Bridge 仍然进入同一 Tool Pipeline。

如果 Policy 要 ask：

Approval Service 记录 audit 并等待 answerer。

获准后执行 MCP。

### Edit

文件修改进入 Sandbox Policy。

当前 Session 是 workspace-write：

> 允许 workspace 内副作用。

修改完成后 durable result 写回。

### 下一 Step

`deriveMessages()`

自然看到三个 Tool Result。

没有任何领域 Tool 绕过统一控制面。

---

## 28. Tool 应该怎样评测

至少分六层。

### Schema

-无效 JSON 是否拒绝；
-oneOf 是否正确；
-output schema 是否真正校验；
-MCP malformed schema 是否 fail。

### Discovery / Scope

- Agent restriction 是否真的同时影响 schema 和 executable lookup；
-Skill Catalog 和实际 Loader visibility 是否一致；
-MCP generation swap 是否原子。

### Policy

- pre-execute deny；
-monotonic guard；
-approval unavailable；
-never policy；
-agentless call；

都应该 fail closed。

### Execution

- timeout；
-cancel；
-parallel / exclusive；
-Sandbox unavailable；
-MCP disconnect；
-PTC nested call。

### Persistence

-每个 durable `tool/call` 是否有合法 settlement；
-取消时未 dispatch call 是否补 synthetic result；
-PTC sub-dispatch logging 是否保持父子 identity。

### End-to-End

最终还要测：

> Tool pipeline 更严格以后，任务是不是仍然能完成。

只测“安全拒绝率”也可能把系统调成什么都不做。

---

## 29. 源码锚点

1. [`packages/core/tools/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/tools/README.md)：Tool contract、PTC、Policy、Output。
2. [`packages/core/tools/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/tools/src/index.ts)：ToolRuntime Pipeline。
3. [`packages/core/agent-loop/src/tool-calls.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/core/agent-loop/src/tool-calls.ts)：并发调度、durable call/result、取消。
4. [`packages/interaction/user-approval/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/interaction/user-approval/README.md)：Approval fail-closed contract。
5. [`packages/interaction/permission-presets/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/interaction/permission-presets/README.md)：Preset 与两套机制的关系。
6. [`docs/subsystems/sandbox.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/docs/subsystems/sandbox.md)：Process Sandbox seam。
7. [`packages/sandbox/sandbox-policy/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/sandbox/sandbox-policy/src/index.ts)：per-call file policy。
8. [`packages/ptc-runtime/ptc-runtime-node/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/ptc-runtime/ptc-runtime-node/README.md)：PTC 隔离执行。
9. [`packages/skill/tool-skill/src/index.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/skill/tool-skill/src/index.ts)：Skill Catalog / Loader / direct invocation。
10. [`packages/mcp/mcp-client/README.md`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/mcp/mcp-client/README.md)：MCP Tool identity、sync、reconnect。
11. [`packages/mcp/mcp-client/src/tools.ts`](https://github.com/deepseek-ai/deepseek-harness/blob/ddefc45fbc7f8e46dd73185e68295696d1297887/packages/mcp/mcp-client/src/tools.ts)：MCP → ToolDefinition bridge。

下一篇：[Engineering & Evaluation →](04-engineering-evaluation.md)
