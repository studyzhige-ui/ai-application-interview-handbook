# Canonical Question 重建进度

更新日期：2026-09-10

## Frozen Baseline

- 正式 HUMAN-A：`S001–S279`
- 正式 Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- 本轮目标：不再搜索新面经，只把冻结语料归一化为正式问题数据集

## 全库读取状态

`S001–S279` 所在 26 个 Batch 已完成一轮直接回读，用于建立统一归一化标准。

> 注意：Batch 文件中的历史“累计来源数 / 下一编号”等过程性统计按采集时口径保留；Canonical 重建只使用当前去重后的 `S001–S279` 正式编号。

## 模块纵向扫描

| 模块 | 状态 | 说明 |
|---|---|---|
| MySQL | ✅ v1 完成 | 已对 `S001–S279` 做一次全库纵向扫描，建立正式 Canonical Question 与证据 Source IDs |
| Redis | ⏳ 待开始 | 下一模块 |
| Vector DB | ⏳ 待开始 | |
| RAG | ⏳ 待开始 | |
| Agent Harness / Runtime | ⏳ 待开始 | 最后结合 Claude Code / Codex 做知识体系校准；面经仍只负责市场证据 |
| FastAPI | ⏳ | 前五模块后处理 |
| Backend Engineering | ⏳ | |
| LLM Foundation | ⏳ | |
| System Design | ⏳ | |
| Coding / Debug / AI Coding | ⏳ | |

## 为什么先按模块完成，再做最终频率榜

真实面试问题高度交叉。例如：

```text
“Redis + MySQL 双写一致性”
```

既属于 Redis，也属于 MySQL / Backend System Design。

又例如：

```text
“Vector + BM25 → RRF → Rerank”
```

同时跨 Vector DB 与 RAG。

因此当前每个模块先完成自己的 Canonical Question 与证据链接；待五大核心模块完成后，再做一次跨模块 Merge / Split 审计，最终生成：

- 全局 Canonical Question Index；
- 独立来源频率榜；
- 独立公司覆盖；
- 追问深度；
- 典型追问链；
- Curriculum Coverage Matrix；
- Knowledge Gap Analysis。

## 质量状态

MySQL v1 中的 `Source Count` 等于该条目列出的唯一 `Sxxx` 数量。它是本轮全库人工语义扫描的可复核结果，不使用搜索引擎命中数，也不使用被删除来源。

在最终跨模块审计前，文件标记为 `v1`，允许出现以下两类修正：

1. 某个问题更适合被拆成两个 Canonical Question；
2. 某个跨模块问题需要增加 / 移动证据来源。

修正必须保留可追溯的 `Sxxx`，不能凭常识虚增“面试频率”。
