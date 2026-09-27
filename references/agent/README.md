# Agent｜源码与权威资料索引

[← Agent Curriculum](../../curriculum/09-agent/README.md) · [Agent Products](../../products/agent/README.md) · [↑ Handbook 总目录](../../README.md) · [Market 首页](../../market/README.md)

> **用途：Agent Runtime 的技术证据与版本边界。** 本目录校准源码事实、开放规范和工程原则，不创建 HUMAN-A 面试证据，也不改变 Canonical Source Count。

**综合证据核验日期：2026-09-21。Codex 源码专项核验：2026-09-27；其余产品沿用各自固定快照。**

## 1. 证据体系

### Tier A｜HUMAN-A 真人面试证据

Frozen Canonical Tier A 来源（`S001–S279`）决定面试频率、真实问法与追问深度：

- [Agent Canonical](../../interview/canonical/agent-harness.md)
- [Verified Follow-up Chains](../../market/analysis/follow-up-chains.md)
- [Market Interviews](../../market/interviews/)

Canonical 统计基线：**44 道 Agent Harness / Runtime Primary Canonical**。频率只能由 Tier A 决定。

### Tier B｜成熟产品固定源码快照

Tier B 回答“某个成熟 Agent 产品在指定版本里到底怎样实现”。

| 产品 | 源码 | 固定快照 | 完整学习入口 |
|---|---|---|---|
| OpenAI Codex | `openai/codex` | `67a709665ac7b50311b93e32612c9a8281684787` | [Products / Codex](../../products/agent/codex/README.md) |
| Claude Code | `studyzhige-ui/claude-code-source-private` | `58231dcce408f805c645cfbc352d2876b517223b` | [Products / Claude Code](../../products/agent/claude-code/README.md) |
| DeepSeek Harness | `deepseek-ai/deepseek-harness` | `477b4f420553e8a52c2fbccc464d7561b239c443` | [Products / DeepSeek Harness](../../products/agent/deepseek-harness/README.md) |
| DeerFlow 2.0 | `bytedance/deer-flow` | `29d285731b326a728a9df33d3641f73b68bbe48b` | [Products / DeerFlow](../../products/agent/deer-flow/README.md) |

源码索引文件维护自己的固定快照和定位用途：

- [Codex 固定源码与问题索引](codex-source-index-current.md)
- [Codex 历史源码索引](codex-source-index.md)
- [Claude Code Source Index](claude-code-source-index.md)

当源码索引与 Products 教材记录的 commit 不同时，只在各自固定快照内解释结论，不跨版本拼接成一个不存在的实现。

### Tier C｜官方文章、开放规范与原始论文

优先使用 Anthropic / OpenAI 官方工程文章、OpenAI Agents SDK 官方文档、MCP / A2A 官方规范、ReAct / SWE-bench 等原始论文。

索引：[Authoritative Web Sources](authoritative-web-sources.md) · [Authoritative Sources](authoritative-sources.md)

### Tier D｜课程抽象

Tier D 不是新的事实来源，而是把 A+B+C 抽象为 beginner-first 的稳定知识体系。

能力入口：[Runtime Capability Map](runtime-capability-map.md)  
正式教材：[Agent Curriculum](../../curriculum/09-agent/README.md)

---

## 2. 冲突处理顺序

```text
市场频率        → 只认 Tier A
具体产品实现    → 以对应 Tier B 固定源码快照为准
协议定义        → 以 Tier C 官方规范为准
课程顺序 / 粒度 → 以 beginner-first 知识依赖与认知闭环为准
```

因此：

- 某个产品版本怎样做 Permission，不代表所有 Agent 必须同构实现；
- MCP 官方 Tool / Resource / Prompt 边界，不因产品 UI 而改变；
- Context Compaction 即使面试频率很高，也必须先学 Context Assembly；
- 外部权威资料不能增加 HUMAN-A Source Count；
- 源码中一个独立 class / primitive 不自动对应一个 Curriculum Markdown 文件。

---

## 3. Curriculum 与 Products 的证据关系

```text
References
├─ 为 Curriculum 校准“通用机制是否准确”
└─ 为 Products 校准“这个固定版本是否真的这样运行”

Curriculum
└─ 建立可迁移知识模型

Products
└─ 沿真实源码还原完整系统
```

Capability 到 Agent 24 章教材的正式映射见 [Runtime Capability Map](runtime-capability-map.md)。

---

## 4. 维护规则

以下变化需要重新核验对应证据：

- 产品 Runtime 固定快照变化；
- MCP / A2A 等规范版本变化；
- HUMAN-A 统计基线变化；
- Agent Framework 出现新的稳定 Runtime Primitive。

版本敏感结论必须显式记录 repo、commit 与核验日期。Products 与源码索引各自固定版本；切换快照时先比较源码变化，再更新对应结论。

项目级修订与历史核验记录统一维护在 [Guide / Project Records](../../guide/project/README.md)。
