# 17. Context Budget / Token Economics：Context Window 不是“能塞多少就塞多少”

Context Assembly 解决“放什么”，这一章解决：

> **有限 Context Window 怎么分预算，怎样同时控制正确性、延迟和成本。**

相关 HUMAN-A 信号包括：

- `AGENT-009` Context Compaction：**41** sources；
- `AGENT-012` Prompt / Context Cache：**5** sources；
- `AGENT-011` Large Tool Result：**11** sources。

Long-context Model 本身的能力边界已经归到 LLM 模块；这里专注 Runtime Budget。

---

# 1. 先讲人话：100K Context 不代表应该每轮塞 100K

一个 Model 最大 Context 假设是：

```text
128K tokens
```

错误理解：

```text
128K 全部拿来放输入
```

因为还要考虑：

```text
输出空间
Tool Call / Result
下一轮增长
Compaction headroom
Provider-specific overhead
```

更合理：

```text
Context Window
= Input Budget
+ Reserved Output
+ Safety Headroom
```

---

# 2. Context 成本有哪些来源

一次 Agent Request 的输入可能包含：

```text
System Prompt
Developer / Repo Instructions
Tool Schemas
Conversation History
Compaction Summary
Memory
RAG Chunks
Current Tool Results
Plan / State
Current User Message
```

这些都占 Token。

尤其容易被忽略：

> **Tool Schema 也是输入 Token。**

500 个 Tool 即使一个都没调用，也可能先把 Context 吃掉一大块。

---

# 3. 一个简单 Budget 表

假设有效输入预算 80K：

| Context Source | 目标预算 |
|---|---:|
| Stable Instructions | 8K |
| Tool Specs | 10K |
| Goal / State | 4K |
| History / Summary | 24K |
| Memory / Retrieval | 12K |
| Recent Tool Results | 16K |
| Current User Input | 2K |
| Buffer | 4K |

这不是通用固定比例。

真正原则：

> **预算要按任务和当前信息价值动态分配。**

---

# 4. 为什么必须预留输出空间

如果输入已经占满 Window：

```text
Model 根本没有足够空间输出
```

更重要的是 Agent 可能需要输出：

- Tool Call Arguments；
- Long Code Patch；
- Structured JSON；
- Compaction Summary。

因此 Runtime 不能只问：

```text
input_tokens < context_window ?
```

而应该：

```text
input_tokens
+ expected_output_reserve
+ safety_buffer
<= context_window
```

---

# 5. Claude Code AutoCompact 的直接实现证据

固定 commit：

```text
58231dcce408f805c645cfbc352d2876b517223b
```

`services/compact/autoCompact.ts` 当前明确：

- 为 compaction summary 预留输出 token；
- 先计算 effective context window；
- auto compact threshold 再减去额外 buffer；
- warning / blocking limit 与真正 Context 上限不同。

源码中的具体常量属于该快照实现，课程不把这些数字当通用最佳实践。

我们抽象出的原则是：

> **Context Runtime 必须留 headroom，而不是等 Provider 报 prompt-too-long 才处理。**

---

# 6. Proactive vs Reactive Context Management

## Proactive

接近阈值前：

```text
Offload large result
Trim low-value items
Compact history
Reduce Tool Specs
```

优点：

- 用户不容易撞硬错误；
- latency 更稳定。

## Reactive

Provider 返回：

```text
context_window_exceeded
prompt_too_long
```

再补救。

优点：

- 不会过早压缩。

缺点：

- 已经付出失败请求成本；
- 可能没有足够空间做高质量 summary。

Production 通常：

```text
proactive main path
+ reactive fallback
```

---

# 7. Token Counting 为什么只是估算

不同 Model / Provider 的 tokenizer 不同。

Tool schema、multimodal、协议 metadata 也会影响实际计费。

所以 Runtime 可能有：

```text
estimated tokens before request
actual usage after response
```

并通过实际 usage 纠偏。

不要假设：

```text
len(text) / 4
```

永远精确。

---

# 8. Token Budget 与信息价值

假设两个 Fragment：

```text
A: 12K token old build logs
B: 200 token current failure summary
```

A 更长不代表更重要。

可以抽象：

```text
Utility / Token
```

Context Budget 本质是在做：

> **有限 token 下的信息选择。**

考虑因素：

- relevance；
- recency；
- authority；
- uniqueness；
- cost；
- required for correctness。

---

# 9. Hard-pinned Context

有些信息不能因为 Budget 被随便裁掉：

```text
System Safety Policy
Original Goal
Critical User Constraint
Current Permission Scope
Current Plan Step
Important Side-effect State
```

可以标记：

```text
pinned / mandatory
```

剩下再做竞争。

这比所有 Context 一视同仁更安全。

---

# 10. Recent History 不一定永远最重要

简单 Sliding Window：

```text
keep last N messages
```

优点：简单。

但可能删掉：

```text
30 轮前用户明确说“禁止修改生产配置”
```

同时保留：

```text
最近 8 条无意义 progress
```

所以成熟策略更像：

```text
Pinned critical state
+ recent local context
+ compacted older context
+ on-demand retrieval
```

---

# 11. Tool Result 是最容易爆 Context 的来源之一

Shell：

```text
pytest -vv
```

可能输出几万行。

Search：

```text
repo grep
```

也可能几 MB。

如果每次完整回填：

```text
Context Window 很快被 Tool Output 吃完
```

因此 Tool Result 应有：

- per-result limit；
- aggregate limit；
- preview；
- offload artifact；
- on-demand read。

下一章专讲。

---

# 12. Tool Schema Budget

假设：

```text
200 tools × 平均 300 tokens schema
= 60K tokens
```

这甚至还没开始任务。

解决：

```text
Tool Discovery
Progressive Loading
Namespace Search
Task-specific Tool Set
```

所以 `AGENT-021 Dynamic Tool Discovery` 和 Context Budget 是同一个系统问题的两面。

---

# 13. Prompt Cache 为什么重要

如果稳定 Prefix 每轮都一样：

```text
System Instructions
Stable Tool Specs
Repo Instructions
```

Provider 可能利用 Prompt Cache 降低：

- latency；
- input cost。

但如果你每轮在 Prefix 顶部插入：

```text
current timestamp
random order tool schemas
dynamic session data
```

可能破坏 cache reuse。

因此：

> **Context Ordering 也有经济性。**

---

# 14. Claude Code 的 Cache-aware Context Assembly

`utils/queryContext.ts` 的注释直接把：

```text
systemPrompt + userContext + systemContext
```

称为 API cache-key prefix。

Side-question fallback 还会尝试重建与主 Loop 一致的 Prefix，注释明确提到 preserving cache hit。

这提供一个真实产品证据：

> Context 设计不只是“模型看懂”，还要考虑 Prefix Stability。

---

# 15. Cache Hit 不能凌驾于 Correctness

不能为了缓存稳定，把已经变化的安全/用户信息留旧值。

例如：

```text
Permission changed
User revoked access
Thread instruction changed
```

必须更新 Context。

所以优先级：

```text
Correctness / Safety
> Cache Hit
```

Cache 只是在正确 Context 上做优化。

---

# 16. Context Budget 与 Latency

更长输入通常意味着：

- Prefill 时间增加；
- 网络传输增加；
- Tool Schema 解析负担；
- 模型注意力噪声增加。

所以：

```text
Long Context
≠ Free Memory
```

即使价格足够便宜，延迟和质量也可能变差。

---

# 17. Context Budget 与 Accuracy

把更多相关内容塞进去有时提升准确率。

但过多低质量信息可能产生：

```text
Distractor
Conflicting Instructions
Stale Facts
Attention Dilution
```

所以目标不是：

```text
maximize context tokens
```

而是：

> **maximize useful evidence under constraints。**

---

# 18. Budget 分配算法的教学版本

```python
def select_fragments(fragments, max_tokens, reserved_tokens):
    budget = max_tokens - reserved_tokens

    pinned = [f for f in fragments if f.pinned]
    optional = [f for f in fragments if not f.pinned]

    selected = list(pinned)
    used = sum(f.tokens for f in pinned)

    optional.sort(
        key=lambda f: f.utility_score / max(f.tokens, 1),
        reverse=True,
    )

    for f in optional:
        if used + f.tokens <= budget:
            selected.append(f)
            used += f.tokens

    return selected
```

真实系统不一定用这个公式，但它帮助理解：

```text
Context Selection 是 Budgeted Optimization
```

---

# 19. 分层 Budget

可以给每类 Context 设置：

```text
minimum
soft maximum
hard maximum
```

例如：

```text
Goal: minimum guaranteed
Tool Result: soft cap
Retrieval: dynamic cap
Tool Schema: task-dependent cap
```

防止某一个类别把其他信息挤光。

---

# 20. Codex Compaction 的 Token Analytics

固定 `compact.rs` 当前会记录：

```text
active_context_tokens_before
compaction_summary_tokens
cached_input_tokens
cache_write_input_tokens
```

并在 compaction 后重新计算 token usage。

这提供一个重要实践：

> **Context Management 应该可观测。**

否则你根本不知道：

```text
为什么成本突然变高？
compaction 到底省了多少？
cache 是否命中？
```

---

# 21. Context Economics 的核心指标

可以监控：

```text
input_tokens / turn
output_tokens / turn
context_fill_ratio
tool_schema_tokens
tool_result_tokens
retrieval_tokens
memory_tokens
compaction_count
compaction_saved_tokens
cache_hit / cached_input
cost per successful task
```

不要只看：

```text
total tokens
```

最后应该归一到：

> **成功任务的成本。**

---

# 22. Context Budget 与 Model Routing

不同模型 Context Window / 价格 /速度不同。

可能策略：

```text
small model + compact context
```

或：

```text
large-context model for specific step
```

但不能把 Model Routing 当成 Context 管理替代品。

如果 Runtime 一直无节制累计垃圾：

```text
换更大窗口只是在推迟问题
```

---

# 23. 高频易错点

⚠️ **Context Window = 可用输入容量**  
还要预留输出和安全 headroom。

⚠️ **Token 多就一定准**  
噪声、冲突、过期信息会伤害质量。

⚠️ **只控制 History，不控制 Tool Schema / Result**  
后两者可能才是大头。

⚠️ **Prompt Cache 只由 Provider 决定**  
Runtime 的 Prefix Stability 直接影响能否利用缓存。

⚠️ **Context 管理不可观测**  
应该有 token/cost/cache/compaction 指标。

---

# 24. 面试怎么回答

## Level 1｜30 秒

🎯 **可以这样回答：**

> Context Budget 不能把 Context Window 全部当输入容量，我会预留输出和 safety headroom，再在 instructions、tool schemas、history、memory、retrieval、tool results 之间分配预算。关键约束和 goal 要 pinned，低价值大结果优先 offload/compact。稳定 prefix 尽量保持稳定利用 prompt cache，但 correctness/safety 优先于 cache hit。

## Level 2｜2–3 分钟

> 我会做 estimated token budgeting + request 后 actual usage 校准。每类 Context 可以有 minimum/soft cap/hard cap，Tool Result 和 Tool Schema 单独计量。接近阈值时 proactive offload/compaction，provider prompt-too-long 只作为 reactive fallback。Metrics 看 context fill、各类 token、compaction saved tokens、cached input 和 cost per successful task，而不是只看总 token。

## Level 3｜继续追问

🔍 **为什么 Sliding Window 不够？**  
可能删掉旧但关键的约束，同时保留最近低价值噪声。

🔍 **为什么 Prompt Cache 与 Tool 顺序有关？**  
稳定 Prefix 更容易复用，动态重排 Tool Spec 会破坏缓存前缀。

🔍 **什么时候换大 Context Model？**  
当任务确实需要更多高价值信息且成本/延迟可接受；不是用来掩盖 Runtime Context 泄漏。

---

# 25. 本章证据

## HUMAN-A

- `AGENT-009` Context Compaction：41 sources；
- `AGENT-011` Large Tool Result：11 sources；
- `AGENT-012` Prompt / Context Cache：5 sources。

## Claude Code

- `services/compact/autoCompact.ts`
- `utils/queryContext.ts`

固定 commit：`58231dcce408f805c645cfbc352d2876b517223b`

## OpenAI Codex

- `codex-rs/core/src/compact.rs` token/cache analytics

固定 commit：`fc948f8c473e5d11e780ffcf1fd7f812a2020932`

---

# 26. 自测

<details><summary>1. 为什么 Context Window 不能全部给输入？</summary>

还要为模型输出、Tool Call、Compaction 等保留空间，并留安全 headroom 防止估算误差和下一轮增长。
</details>

<details><summary>2. Context Budget 最大的隐藏来源有哪些？</summary>

Tool Schemas、超大 Tool Results、Retrieved Chunks、重复 Memory/Instructions，不能只盯着聊天 History。
</details>

<details><summary>3. Prompt Cache 优化为什么不能影响 Correctness？</summary>

权限、用户指令、环境状态变化必须及时更新；缓存只能优化正确 Context，不能保留过期信息换 hit。
</details>

<details><summary>4. Context 管理应该监控哪些指标？</summary>

各来源 token、fill ratio、compaction 次数/节省量、cache usage、latency、cost per successful task 等。
</details>
