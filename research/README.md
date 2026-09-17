# Research｜2026 AI Application / Agent 真人面经研究库

[↑ Handbook 总目录](../README.md) · [Canonical Questions](questions/README.md) · [Market Analysis](analysis/README.md) · [Curriculum Knowledge Map](../roadmap/knowledge-map.md)

> **状态：🟢 Continuous Monitoring。** 当前正式库为 `S001–S287` 共 **287** 个 HUMAN-A 独立招聘流程、**28** 个正式 Batch；自 2026-09-16 起按“最近 3 天发现窗口 + 全历史去重”持续增量监测。每天三次检索合并为一个日批次；质量优先，不为数量降低 HUMAN-A 门槛。

## 1. 研究目的

这里不是“网上见过什么题就都收”的题库，而是持续回答：

```text
真实 AI Application / Agent 岗位最近在问什么？
→ 哪些能力持续反复出现？
→ 哪些新主题正在升温？
→ 一道题会追到多深？
→ 项目怎样被验证？
→ Failure / Scale / Coding / System Design 怎样进入真实面试？
```

维护它的目的不是追求来源总数，而是让 Handbook 始终拥有一层**新鲜、可核验、去重后的真人招聘证据**，用于校准：

- 面试复习优先级；
- 真实问法与追问链；
- 岗位能力边界的变化；
- 新技术 / 新框架是否真正进入招聘现场；
- 后续 Canonical / Curriculum 是否值得周期性调整。

课程关系固定为：

> **完整知识体系决定应该学什么；HUMAN-A 面经告诉我们市场最近怎么问、问多深。**

日常采集不会因为某一天出现新词就直接改 Curriculum；新增信号先进入 Research 层，经过独立来源累积与周期性审查后再影响 Canonical / Curriculum。

## 2. 当前正式状态

| 项目 | 当前值 |
|---|---:|
| HUMAN-A 来源 | **287** |
| Source IDs | `S001–S287` |
| 正式 Batch | **28** |
| 下一 Source ID | **`S288`** |
| ACTIVE Canonical | 235 |
| 既有映射基线 | `S001–S279` 中 278 Mapped + 1 VALID-UNMAPPED（S271） |
| 新增映射状态 | `S280–S287` 待 periodic review / Canonical mapping |
| 当前采集状态 | Continuous Monitoring |
| 主动发现窗口 | 运行时最近 3 天 |
| 每日检索 | 10:00 / 17:00 / 22:00 |
| Batch 规则 | 当天三次检索 = 一个日批次 |

所有数字在自动维护时必须以 `main` 的实际最新状态重新计算，不能把任何旧聊天或历史表格当成永远不变的固定值。

## 3. HUMAN-A Gate

正式来源必须满足：

```text
候选人本人第一人称
+ 真实招聘流程 / 真人面试官痕迹
+ 高信息密度
+ 目标 AI Application / Agent Role Scope
+ 正文稳定可核验
+ 非转载 / 非答案帖 / 非重复
```

详细规则：

- [Source Quality Policy](quality/source-quality-policy.md)
- [Role Scope Policy](quality/role-scope-policy.md)

## 4. 去重原则

任何新增在分配 `Sxxx` 前都必须直接回读全历史，并同时检查 URL、作者、公司、岗位、日期 / 轮次、项目语义、连续题序、招聘 Timeline 与复制链。Search / Code Search 的“0 命中”不能证明未收录。

同一候选人、同一公司、同一招聘流程的多轮面试合并为一个 `Sxxx`；不同候选人的独立流程即使问到相同问题，仍分别计数。

最近 3 天窗口只限制“主动发现范围”，不降低全历史去重要求；新帖子若实际是旧面经搬运、重发或同流程补发，仍然零贡献。

## 5. 每日维护节奏

```text
10:00  Morning Search
  ↓
17:00  Afternoon Search（补平台 / 公司 / Query 盲区）
  ↓
22:00  Evening Search + 当日总去重 + Finalize Daily Batch
```

- 10:00 / 17:00：只把已经完整通过 HUMAN-A + Role Scope + 全历史去重的候选放入 Inbox；不分配最终 `Sxxx`，不创建多个 Batch。
- 22:00：进行第三次搜索，重新对当日所有候选做一次全历史去重，再统一分配 ID，并只生成当天一个正式 Batch。
- 每次搜索都在 `monitoring/daily-log.md` 记录搜索覆盖、有效候选、典型排除与盲区；普通低质量线索不进入 Inbox。
- **不设每天正式新增条数 KPI。** 可以要求高搜索量，但当天 0 个新增也比为凑数放低 Gate 更好。

## 6. 目录

```text
research/
├── interviews/          # S001–S287 正式 HUMAN-A / Batch 01–28
├── quality/             # Source / Role Scope Gate
├── monitoring/          # Inbox + 当日三次检索日志
├── questions/           # Canonical Ownership
├── analysis/            # Frequency / Coverage / Follow-up / Gap
├── agent-sources/       # Agent 源码 + 官方资料证据层
├── fastapi-sources/     # FastAPI 官方资料
└── backend-sources/     # Backend Engineering 权威资料
```

## 7. 研究与教材的边界

- HUMAN-A → 市场频率 / 真实问法 / 追问深度 / 新趋势；
- 官方资料 / 源码 → 技术事实 / Production 边界；
- Curriculum → beginner-first 的完整知识演进。

研究层永远不能因为教材 Merge / Rename 而修改 Source Count；反过来，每日新增 HUMAN-A 也不能未经周期性审查就直接打乱 Curriculum。

新增来源优先进入 Research 证据层。若可映射已有 Canonical，进入后续周期性映射；若出现疑似新能力，也先累积独立真人证据，再决定是否新增 Canonical 或修改 Curriculum。

## 8. 持续维护的固定原则

1. 每次运行先读当前 `main`，自动确认最新 Batch、最大 `Sxxx`、下一编号与 Inbox 状态；
2. 主动发现只看最近 3 天，优先目标公司与目标岗位，但平台不设配额；
3. 每次都执行高搜索量，覆盖热门公司、不同平台、不同岗位叫法与作者 Timeline；
4. 分配 ID 前必须直接回读全部历史 Batch；
5. 同候选人同公司同流程多轮继续合并，不虚增样本；
6. 多平台只作为 Recall 手段，不降低 HUMAN-A 门槛；
7. 每天三次搜索只形成一个日批次；
8. 维护目标是**跟踪真实招聘市场变化**，不是让 Source Count 持续变大。
