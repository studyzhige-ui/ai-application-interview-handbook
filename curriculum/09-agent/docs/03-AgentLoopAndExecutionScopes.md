# 03. Agent Loop：观察怎样改变下一步

[← 上一章](02-WorkflowAutonomyAndRuntimeBoundary.md) · [Agent 目录](../README.md) · [下一章 →](04-ToolContractAndValidation.md)

模型提出“读取 A”，程序读到了“发布日期待确认”。如果程序只把这句话打印到终端，没有让下一次模型请求得到它，模型就没有获得新证据。

反馈循环的关键不是反复调用模型，而是让已发生的行动进入后续判断，并让停止有明确原因。

<a id="1-先讲人话agent-的核心不是会调用-tool而是会循环推进任务"></a>
<a id="9-runtime-state-应该有什么"></a>
<a id="legacy-03-01"></a>
<a id="legacy-03-09"></a>
<a id="section-1"></a>
<a id="section-9"></a>
<a id="core-1"></a>

## 1. 先把一轮拆成三个动作

**一轮反馈** 包含判断、行动和观察：程序先把当前目标与必要信息交给模型；模型提出行动；程序检查并执行，把结果带回来。只有这样，下一轮才能基于新信息而不是重复猜测。

| 时刻 | 程序已知状态 | 本次决定 | 状态如何变化 |
|---|---|---|---|
| 开始 | 尚未读 A | 请求读取 A | 准备一次工具调用 |
| 工具结束 | A 的内容已返回 | 还没有新的模型决定 | 将内容记入观察 |
| 下一次请求 | 模型输入包含 A 的内容 | 提交结果或继续查证 | 验收、继续或等待 |

程序保存的状态，不会自动进入模型。真实接入时，需要按模型接口把选中的信息编码成请求；这是[上下文编排](09-ContextAssemblyAndCache.md)负责的工作。

<a id="2-一个最小可运行的-agent-loop"></a>
<a id="legacy-03-02"></a>
<a id="section-2"></a>
<a id="core-2"></a>

## 2. 看一个能够运行的反馈例子

下面用固定函数代替模型，用内存里的 A 代替文件。它不访问网络，没有真实模型，也不实现生产恢复；只观察“结果回填以后，决定发生变化”。Python 是演示载体，前面的过程不依赖某种编程语言。

```python
# runnable-example: feedback_loop
# 只验证反馈与有限停止；不模拟生产授权、持久化或模型质量。
def decide(state):
    if not state['observations']:
        return {'kind': 'tool', 'name': 'read', 'doc': 'A'}
    return {'kind': 'final', 'text': state['observations'][-1]}

def run_report():
    state = {'goal': '读取A并交付内容', 'observations': []}
    documents = {'A': '发布日期待确认'}  # 已授权内存材料，替代真实文件
    for _ in range(3):                    # 明确上限，防止无限循环
        decision = decide(state)
        if decision['kind'] == 'tool':
            if decision['name'] != 'read' or decision['doc'] not in documents:
                raise ValueError('未知工具或未授权材料')
            # 结果不能只打印；后一次决策必须能读到它。
            state['observations'].append(documents[decision['doc']])
        elif decision['kind'] == 'final':
            # 本例只验证交付的是刚读取的内容，不证明任意报告语义正确。
            if state['observations'] and decision['text'] == state['observations'][-1]:
                return decision['text']
            raise ValueError('没有可核对的交付物')
        else:
            raise ValueError('未知决定类型')
    raise RuntimeError('预算耗尽，不等于成功')

assert run_report() == '发布日期待确认'
```

保存为 `feedback_loop.py` 后运行 `python feedback_loop.py`。原例用断言检查返回值；没有报错表示这个条件成立，不表示调用了真实模型。也可以在最后加 `print(run_report())`，观察 `发布日期待确认`。

顺着程序追踪：

1. `observations` 为空，`decide` 提出读 A。
2. 程序检查工具名与材料名，将读取内容追加到观察列表。
3. 下一轮 `decide` 能看到这条观察，返回完成候选。
4. 程序检查候选确实来自刚才的读取，才返回；最多三轮的限制另行阻止无限执行。

> ⚠️ 这个固定决策函数本身不是自主模型。测试通过只证明反馈连通与有限停止，不能证明真实模型会选对工具，也不能证明报告语义正确。

<a id="11-loop-什么时候继续什么时候停止"></a>
<a id="4-为什么这个分层对-failure-很重要"></a>
<a id="8-state-machineloop-不只是-while-true"></a>
<a id="legacy-03-04"></a>
<a id="legacy-03-08"></a>
<a id="legacy-03-13"></a>
<a id="section-11"></a>
<a id="section-4"></a>
<a id="section-8"></a>
<a id="core-3"></a>

## 3. 停止原因不是一个 done

循环可能交付结果，也可能尚未完成就停止。至少要让调用方区分下面几种情况：

| 条件 | 应表达的结果 | 能否当作任务成功 |
|---|---|---|
| 候选结果满足任务验收 | 成功 | 可以，仍披露验证范围 |
| 缺关键输入或等待批准 | 等待或暂停 | 不可以 |
| 用户要求停止 | 取消中，随后确认取消范围 | 不可以 |
| 时间、调用次数或费用耗尽 | 预算停止 | 不可以 |
| 不可恢复错误 | 失败 | 不可以 |

```text
模型决定
  ├─ 工具候选 → 检查并执行 → 观察回填 → 下一轮
  ├─ 澄清请求 → 保存等待原因 → 等待输入
  └─ 完成候选 → 验收
                  ├─ 通过 → 成功退出
                  └─ 未通过 → 有预算则修正，否则说明缺口后停止
```

一次测试工具超时，不一定要把整个报告任务判为失败；也不能因为模型结束生成，就直接认为业务完成。继续资格由当前错误、任务范围和剩余预算共同决定。

<a id="3-为什么要分-run--turn--step"></a>
<a id="legacy-03-03"></a>
<a id="section-3"></a>
<a id="对照产品语义不强制一一对应"></a>
<a id="core-4"></a>

## 4. 用执行范围说明“哪里出了问题”

本书采用一组工作定义：**Session** 是持续会话；**Run** 是为一个目标发起的执行；**Turn** 是一次判断—行动—观察反馈轮；**Step** 是其中的操作。用户的一次输入称为“用户交互”，不再与反馈轮混叫。

```text
Session：同一项目的持续会话
└─ Run：这次报告任务
   ├─ Turn 1：请求并读取 A
   │  ├─ Step：模型请求
   │  └─ Step：工具执行与结果登记
   └─ Turn 2：根据 A 决定后续工作
```

这使我们能准确说“工具步骤失败，任务仍可继续”。它不是行业统一对象树。例如 Codex 的 Turn 可以覆盖一次用户输入后的多次推理和工具交互；应用对照产品时，应查作用域，而不是把同名字强行对应。[产品对象对照](../../../products/claude-code/01-context-lifecycle.md#implementation-chapter-03)只作选读。

<a id="5-runtime-不是只有-message还需要-event"></a>
<a id="6-event-为什么最好是结构化的"></a>
<a id="7-correlation-id-为什么关键"></a>
<a id="legacy-03-05"></a>
<a id="legacy-03-06"></a>
<a id="legacy-03-07"></a>
<a id="section-5"></a>
<a id="section-6"></a>
<a id="section-7"></a>
<a id="core-5"></a>

## 5. 消息给模型看，事件帮助程序管理执行

模型消息记录输入、输出和工具交互。程序事件还会记录排队、工具开始、批准到达、取消请求等事情。这些事会影响控制，但不必全部送进模型。

以两个工具并行为例，后发出的工具可能先结束。因此需要**调用标识 `call_id`** 把结果关联到正确请求，不能按到达顺序猜配对。

```text
请求 c1：读 A ─────────→ 结果 c1：A 的内容
请求 c2：读 B ─→ 结果 c2：B 的内容
```

同一个调用可以有开始、进度和结束多个事件。事件只需记录实际管理需要的信息；如何持久保存、跨进程恢复，在状态与恢复章节处理，不要求这个最小循环先建立完整事件数据库。

<a id="10-新用户指令怎样进入正在运行的-agent"></a>
<a id="legacy-03-10"></a>
<a id="section-10"></a>
<a id="core-6"></a>

## 6. 运行中收到新指令，什么时候生效

已发出的模型请求通常不能在中间随意插入文字。应用先接收新输入，再判断它是在补充材料、改变约束、取消任务，还是提出另一项工作。

补充信息可以在当前模型或工具阶段结束、控制权回到运行时后加入下一次请求；无关任务可以排队。若新约束是“不要发送报告”，程序应立即阻止尚未派发的发送，并根据当前动作是否可中断处理正在执行的部分。

**收到新指令、让新指令生效、撤销已经发生的动作，是三件事。** 邮件已经发出，不能靠把新消息放进历史假装它没有发生。取消传播与迟到结果的具体处理见[工具并发与取消](07-ToolConcurrencyAndCancellation.md)。

<a id="summary"></a>

## 本章小结

反馈循环通过观察更新下一步判断；执行范围说明失败发生在哪里；消息与事件服务不同对象。成功必须经过验收，等待、取消和预算停止都应有自己的结果语义。

<a id="-继续追问与下一步"></a>
<a id="14-面试怎么答"></a>
<a id="qagent-运行中用户追加消息能直接修改当前模型输入吗"></a>
<a id="qmessage-和-event-的区别为什么重要"></a>
<a id="qsessionrunturnstep-怎么区分"></a>
<a id="q怎样描述一个最小-agent-loop"></a>
<a id="q怎样解释一个完整agent-loop"></a>
<a id="interview"></a>

## 🎯 面试怎么回答

### 一个最小 Agent Loop 怎样推进？

程序组织输入，请模型提出行动或完成候选；行动经检查执行后形成观察，进入下一次判断。完成候选按任务标准验收。循环另外检查等待、取消、错误和预算，不能只依赖模型主动结束。

### Message 与 Event 有什么区别？

Message 是模型交互表示，Event 记录程序发生的事情，例如排队、授权和工具进度。一次调用可以对应多个事件。用调用标识关联结果，不需要把所有事件都送给模型。

### Session、Run、Turn、Step 有统一定义吗？

没有必须通用的同一对象树。应先说明项目自己的会话、任务、反馈轮和步骤口径，再对照产品的作用域与生命周期，不能因为名称相同就认为取消和恢复范围相同。

<a id="15-高频易错点"></a>
<a id="pitfalls"></a>

## ⚠️ 易错点

> ⚠️ 结果只打印而不回填，下一次模型调用未必知道工具做过什么。

> ⚠️ `return` 只代表当前函数结束，是否业务成功还要看终止原因和验收。

> ⚠️ 新消息到达不等于外部动作已停止，已经发生的结果仍要如实记录。

<a id="16-本章自测"></a>
<a id="self-test"></a>

## 本章自测

<details><summary>1. 删除例子中追加观察的语句，会发生什么？</summary>

每次 decide 都看见空观察，重复提出读取；达到三轮上限后抛出预算耗尽错误，而不是成功返回。

</details>

<details><summary>2. c2 比 c1 先结束，怎样避免 A、B 内容错配？</summary>

每条结果携带对应调用标识，按 c1、c2 关联原请求，而不是按到达次序排序后配对。

</details>

<details><summary>3. 模型交了无引用报告，预算又已耗尽，应记录成功吗？</summary>

不能。报告不满足验收；应说明未完成的引用要求以及预算停止原因，可以交付明确标识的部分结果。

</details>

<details><summary>4. 用户说“停止发送”，发送请求已发出但没有回执，能显示“没有发送”吗？</summary>

不能。可以停止后续派发并请求取消，但原动作结果仍未知，需查询回执或按业务流程核对。

</details>

<a id="03-agent-loopsessionrunturnstep-与执行事件"></a>
<a id="12-产品实现与官方资料对照按需展开"></a>
<a id="13-human-a-信号"></a>
<a id="human-a"></a>
<a id="legacy-03-11"></a>
<a id="legacy-03-12"></a>
<a id="section-12"></a>
<a id="references"></a>

## 知识回看与权威资料

- [工具契约](04-ToolContractAndValidation.md)：理解候选执行之前具体检查什么。
- [状态与持久化](12-StateHistoryAndPersistence.md)：区分当前控制信息和需要跨重启保留的事实。
- [Agents SDK 的执行循环](https://openai.github.io/openai-agents-python/running_agents/)：用一种官方实现对照循环，而非将本书术语树当其对象模型。


---

[← 上一章](02-WorkflowAutonomyAndRuntimeBoundary.md) · [Agent 目录](../README.md) · [下一章 →](04-ToolContractAndValidation.md)
