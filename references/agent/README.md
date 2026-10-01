# Agent｜源码与权威资料索引

[← Agent Curriculum](../../curriculum/09-agent/README.md) · [Agent Products](../../products/agent/README.md) · [↑ Handbook 总目录](../../README.md) · [Market 首页](../../market/README.md)

> **用途：Agent Runtime 的技术证据与版本边界。** 本目录校准源码事实、开放规范和工程原则，不创建 HUMAN-A 面试证据，也不改变 Canonical Source Count。

各项技术结论按对应资料或产品记录的固定提交与核验范围阅读。综合资料、源码快照和后续教学修订分别定版本；索引同步日期不冒充重新核验上游源码的日期。

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
| OpenAI Codex | `openai/codex` | `cda82a2c6853b484e0ba56d38f13902adfb2a6a1` | [Products / Codex](../../products/agent/codex/README.md) |
| Claude Code | `studyzhige-ui/claude-code-source-private` | `58231dcce408f805c645cfbc352d2876b517223b` | [Products / Claude Code](../../products/agent/claude-code/README.md) |
| DeepSeek Harness | `deepseek-ai/deepseek-harness` | `639ed015397290b3745d163aafe02ffee4aa3f84` | [Products / DeepSeek Harness](../../products/agent/deepseek-harness/README.md) |
| DeerFlow 2.0 | `bytedance/deer-flow` | `4d5607229ef1ebe8a66c9b9644b91da9082c3221` | [Products / DeerFlow](../../products/agent/deer-flow/README.md) |

源码索引文件维护自己的固定快照和定位用途：

- [Codex 固定源码与问题索引](codex-source-index-current.md)
- [Codex 历史源码索引](codex-source-index.md)
- [Claude Code Source Index](claude-code-source-index.md)
- [DeepSeek Harness 固定源码与机制](deepseek-harness-source-index.md)
- [DeerFlow 固定源码与机制](deer-flow-source-index.md)

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

<a id="reader-revision-20260917"></a>

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

Capability 到 Agent 教材的正式映射见 [Runtime Capability Map](runtime-capability-map.md)。旧的 `reader-revision-20260917` 锚点保留给课程引用；历史修订依据见[Agent 修订记录](../../guide/project/agent-reader-revision.md)，产品行为仍认各自固定快照。

---

## 4. 维护规则

以下变化需要重新核验对应证据：

- 产品 Runtime 固定快照变化；
- MCP / A2A 等规范版本变化；
- HUMAN-A 统计基线变化；
- Agent Framework 出现新的稳定 Runtime Primitive。

版本敏感结论必须显式记录 repo、commit 与核验日期。Products 与源码索引各自固定版本；切换快照时先比较源码变化，再更新对应结论。

项目级修订与历史核验记录统一维护在 [Guide / Project Records](../../guide/project/README.md)。

<!-- product-evidence:start -->
## 产品阅读与修订证据

| 产品 | 实际阅读顺序 | 教学修订记录 |
|---|---|---|
| [Claude Code](../../products/agent/claude-code/README.md) | [01](../../products/agent/claude-code/01-input-and-query-loop.md) → [02](../../products/agent/claude-code/02-tool-execution-and-permissions.md) → [03](../../products/agent/claude-code/03-skills-hooks-and-mcp.md) → [04](../../products/agent/claude-code/04-subagents-and-task-ownership.md) → [05](../../products/agent/claude-code/05-context-and-compaction.md) → [06](../../products/agent/claude-code/06-session-and-auto-memory.md) → [07](../../products/agent/claude-code/07-persistence-and-resume.md) → [08](../../products/agent/claude-code/08-observation-and-delivery.md) | [修订范围与验证](../../guide/audits/claude-code-clarity-refinement-2026-09-27.md) |
| [Codex](../../products/agent/codex/README.md) | [01](../../products/agent/codex/01-thread-and-turn.md) → [02](../../products/agent/codex/02-tools-and-processes.md) → [03](../../products/agent/codex/03-extensions-and-discovery.md) → [04](../../products/agent/codex/04-agent-collaboration.md) → [05](../../products/agent/codex/05-history-and-recovery.md) → [06](../../products/agent/codex/06-memory-pipeline.md) → [07](../../products/agent/codex/07-delivery-and-review.md) | [修订范围与验证](../../guide/audits/codex-clarity-refinement-2026-09-27.md) |
| [DeepSeek Harness](../../products/agent/deepseek-harness/README.md) | [01](../../products/agent/deepseek-harness/01-boot-and-agent-loop.md) → [02](../../products/agent/deepseek-harness/02-tools-files-and-jobs.md) → [03](../../products/agent/deepseek-harness/03-skills-mcp-and-ptc.md) → [04](../../products/agent/deepseek-harness/04-plans-goals-and-agents.md) → [05](../../products/agent/deepseek-harness/05-session-and-recovery.md) → [06](../../products/agent/deepseek-harness/06-cross-session-knowledge.md) → [07](../../products/agent/deepseek-harness/07-delivery-and-review.md) | [修订范围与验证](../../guide/audits/deepseek-harness-clarity-refinement-2026-09-27.md) |
| [DeerFlow](../../products/agent/deer-flow/README.md) | [01](../../products/agent/deer-flow/01-run-and-model-loop.md) → [02](../../products/agent/deer-flow/02-tools-and-resources.md) → [03](../../products/agent/deer-flow/03-skills-and-mcp.md) → [04](../../products/agent/deer-flow/04-native-batch-and-acp.md) → [05](../../products/agent/deer-flow/05-delivery-and-goals.md) → [06](../../products/agent/deer-flow/06-history-and-recovery.md) → [07](../../products/agent/deer-flow/07-memory-pipeline.md) → [08](../../products/agent/deer-flow/08-observation-and-review.md) | [修订范围与验证](../../guide/audits/deerflow-clarity-refinement-2026-09-27.md) |

正文序号与各产品阅读主线保持一致。历史修订记录只说明其基线与实际验证，当前源码依据见产品入口。
<!-- product-evidence:end -->


## 课程讲解与固定实现选读

[实现对照](implementation-notes.md)集中保存各章有用途的固定源码选读；[能力映射](runtime-capability-map.md)定位正式主责章节。不要将选读中的私有类名、历史开关或产品参数当成首次学习的必备概念。

课程精修关键事实核验：2026-09-28。JSON Schema 数值范围、MCP 2026-07-28、A2A 1.0.0、框架恢复与工具护栏等按正文官方链接校准；没有重新核验全部上游源码，也没有运行真实模型和外部恢复系统。产品目录与本页既有快照表保留各自范围。

[本轮维护记录](../../guide/project/agent-clarity-refinement-2026-09-28.md)与[证据映射](../../guide/project/agent-clarity-mapping-2026-09-28.json)记录移入、保留和验证边界，不修改真人来源准入、Canonical 归属或冻结计数。
