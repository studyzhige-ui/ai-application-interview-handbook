# Canonical Questions

这里不做“网上见过什么题就全部收进来”的题库。

## 唯一原则

Canonical Question 只允许由 **HUMAN-A 真人高质量第一人称面经**产生市场证据：

```text
真人面试官
+
候选人本人第一人称
+
高信息密度
+
AI Application / Agent 目标岗位
+
可稳定核验
+
非转载重复
```

任何不满足上述标准的来源都不能创建新的 Canonical Question、提高某题的面试频率或伪装成课程学习优先级。

## 正式一级板块

```text
Python
  ↓
FastAPI
  ↓
AI Backend Engineering
  ↓
MySQL
  ↓
Redis
  ↓
Vector DB
  ↓
LLM Foundation（应用工程深度）
  ↓
RAG
  ↓
Agent Harness / Runtime
  ↓
System Design
```

对应文件：

- `python.md`
- `fastapi.md`
- `ai-backend-engineering.md`
- `mysql.md`
- `redis.md`
- `vector-db.md`
- `llm-foundation.md`
- `rag.md`
- `agent-harness.md`
- `system-design.md`

`Coding / Debug / AI Coding` 只作为 `Question Type`，不再单独成为一级板块。

## 当前冻结基线

- HUMAN-A：`S001–S279`
- Batch：`batch-01.md` ～ `batch-26.md`
- 主动采集：已冻结
- 十板块全库纵向扫描：**10 / 10 完成**
- 十板块 v2 Primary Module 归属审计：**10 / 10 完成**
- Primary-owned ACTIVE Canonical：**230**
- MOVED 旧分类映射：**22**

因此，第一阶段现在才正式完成。

`230` 不是最终发布版的全局独立问题数。第二阶段仍需做跨模块 Global Merge / Split、Evidence 一致性校验、频率 / 公司 / 岗位 / 轮次统计、追问链与课程覆盖分析。

详细状态见：

- `schema.md`：数据规范与板块边界
- `module-index.md`：十板块 Ownership、迁移映射和 ACTIVE 数量
- `progress.md`：阶段状态与下一步

## 与完整知识体系的关系

完整课程体系负责决定“应该学什么”；真人高质量面经只负责提供：

- 真实问法；
- 真实追问深度；
- 公司 / 岗位 / 轮次信号；
- 学习优先级校准。

因此不会为了扩充问题库，把二次创作、题库、标准答案、合集或无法核验的内容转化成额外学习任务。

Agent Harness 未来还会用 Claude Code / Codex 源码补齐课程知识边界，但源码证据不能反向改变 HUMAN-A 的面试频率。
