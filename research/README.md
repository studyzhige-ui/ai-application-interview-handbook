# Research｜2026 AI Application / Agent 真人面经研究库

[↑ Handbook 总目录](../README.md) · [Canonical Questions](questions/README.md) · [Market Analysis](analysis/README.md) · [Curriculum Knowledge Map](../roadmap/knowledge-map.md)

> **状态：✅ Frozen。** 当前研究基线为 `S001–S279` 共 279 个 HUMAN-A 独立招聘流程；主动采集已暂停。

## 1. 研究目的

这里不是“网上见过什么题就都收”的题库，而是回答：

```text
真实 AI Application / Agent 岗位在问什么？
→ 哪些能力反复出现？
→ 一道题会追到多深？
→ 项目怎样被验证？
→ Failure / Scale / Coding / System Design 怎样进入真实面试？
```

课程关系固定为：

> **完整知识体系决定应该学什么；HUMAN-A 面经告诉我们市场怎么问、问多深。**

## 2. 当前冻结基线

| 项目 | 当前值 |
|---|---:|
| HUMAN-A 来源 | 279 |
| Source IDs | `S001–S279` |
| 正式 Batch | 26 |
| ACTIVE Canonical | 235 |
| Mapped Sources | 278 |
| VALID-UNMAPPED | 1（S271） |
| 主动采集 | Frozen |

## 3. HUMAN-A Gate

正式来源必须满足：

```text
候选人本人第一人称
+ 真实招聘流程 / 面试官痕迹
+ 高信息密度
+ 目标 AI Application / Agent Role Scope
+ 正文稳定可核验
+ 非转载 / 非答案帖 / 非重复
```

详细规则：

- [Source Quality Policy](quality/source-quality-policy.md)
- [Role Scope Policy](quality/role-scope-policy.md)

## 4. 去重原则

任何未来新增必须先直接回读全历史，并同时检查 URL、作者、公司、岗位、日期/轮次、项目语义、连续题序与复制链。Search / Code Search 的“0 命中”不能证明未收录。

同一候选人、同一公司、同一招聘流程的多轮面试合并为一个 `Sxxx`；不同候选人的独立流程即使问到同样问题，仍分别计数。

## 5. 目录

```text
research/
├── interviews/          # S001–S279 原始 HUMAN-A 研究记录
├── quality/             # Source / Role Scope Gate
├── monitoring/          # 若未来重开采集时的 Inbox
├── questions/           # 235 Canonical Ownership
├── analysis/            # Frequency / Coverage / Follow-up / Gap
├── agent-sources/       # Agent 源码 + 官方资料证据层
├── fastapi-sources/     # FastAPI 官方资料
└── backend-sources/     # Backend Engineering 权威资料
```

## 6. 研究与教材的边界

- HUMAN-A → 市场频率 / 真实问法 / 追问深度；
- 官方资料 / 源码 → 技术事实 / Production 边界；
- Curriculum → beginner-first 的完整知识演进。

研究层永远不能因为教材 Merge / Rename 而修改 Source Count。

## 7. 如果未来重开采集

从保留编号 `S280` 开始，但必须先读取本 README、质量规则、Inbox 和 `batch-01.md`～`batch-26.md` 全历史，再重新执行同样的 HUMAN-A / 去重 Gate。
