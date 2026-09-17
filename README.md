# AI Application Interview Handbook

> 面向 **AI Application / AI Agent Engineer** 求职的一套 beginner-first 系统教材、真人面经研究库与面试训练体系。

> **当前状态：✅ 十个正式一级模块第一版教材全部完成** · **Phase 3 Curriculum Build ✅**
> **研究状态：🟢 Continuous Monitoring · 287 个 HUMAN-A 招聘流程（S001–S287）** · **235 ACTIVE Canonical**

## 快速入口

[十板块知识地图](roadmap/knowledge-map.md) · [正式学习路线](roadmap/learning-path.md) · [v1.0 终局质量审计](roadmap/final-quality-audit.md) · [跨模块术语表](roadmap/terminology-glossary.md) · [课程建设进度](research/questions/progress.md) · [真人面经研究库](research/README.md) · [Canonical Questions](research/questions/README.md) · [粒度审计](roadmap/curriculum-granularity-audit.md) · [深度审计](roadmap/content-depth-audit.md) · [Agent阅读修订](roadmap/agent-reader-revision.md)

---

## 1. 这是什么项目

它不是“按面试题拼起来的八股仓库”。项目把三类信息严格分层：

```text
完整知识体系
→ 决定初学者 0→1 的课程主干

HUMAN-A 真人面经
→ 校准市场热度、真实问法、追问深度、Failure / Scale / Evaluation 强度

官方文档 / 规范 / 论文 / 成熟源码
→ 校准技术事实与 Production 工程边界
```

核心原则：**知识体系决定先学什么；真人面经决定哪些地方必须学深，但不能反过来打乱课程演进。**

---

## 2. 十个正式一级模块

| # | 一级模块 | 层级 | 一句话职责 | 教材 | Canonical | 状态 |
|---:|---|---|---|---:|---:|---|
| 01 | [Python Foundation](python/README.md) | Foundation | 建立 AI Application / Agent Engineer 所需的 Python 语言、对象模型、结构化数据与并发 Runtime 基础。 | 13 | 15 | ✅ |
| 02 | [FastAPI](fastapi/README.md) | Foundation | 把 Python Runtime 能力组织成可校验、可 Streaming、可部署的 HTTP / ASGI AI Service。 | 16 | 4 | ✅ |
| 03 | [AI Backend Engineering](backend-engineering/README.md) | Foundation | 把 FastAPI、数据系统、模型服务与 Agent Runtime 可靠地连接成可控、可恢复、可观测的 Production Backend。 | 22 | 39 | ✅ |
| 04 | [MySQL](mysql/README.md) | Data | 理解结构化业务事实怎样持久化，以及查询、事务、并发、日志与规模增长时的正确性和性能。 | 23 | 26 | ✅ |
| 05 | [Redis](redis/README.md) | Data | 掌握 Redis 数据结构、内存生命周期、持久化、高可用、原子性与它在 Cache / Session / Rate Limit / Coordination 中的边界。 | 24 | 19 | ✅ |
| 06 | [Vector Database](vector-db/README.md) | Data | 理解向量空间、ANN 索引、过滤、索引生命周期与分布式 Vector DB，能基于 Recall / Latency / Memory / Update 约束做架构选择。 | 16 | 12 | ✅ |
| 07 | [LLM Foundation（应用工程深度）](llm-foundation/README.md) | Model Foundation | 以应用工程深度理解 Token、Transformer、Generation、KV Cache、Serving、模型选择与 Prompt / Fine-tuning 的边界。 | 14 | 23 | ✅ |
| 08 | [RAG](rag/README.md) | AI Application | 把 Knowledge Source 变成可追溯 Evidence，并通过 Retrieval / End-to-end Evaluation 证明回答质量真的提升。 | 14 | 29 | ✅ |
| 09 | [Agent](agent/README.md) | Agent System | 从 Agent Loop 出发，构建 Tool、Context、Memory、State、Permission、Checkpoint、Trace、Eval 与 Multi-Agent 的可恢复执行系统。 | 24 | 44 | ✅ |
| 10 | [System Design](system-design/README.md) | Integration | 把前九个模块组合成可容量估算、可扩展、可恢复、可观测、可验证、可演进的完整系统。 | 19 | 24 | ✅ |

### 正式学习顺序

[Python Foundation](python/README.md) → [FastAPI](fastapi/README.md) → [AI Backend Engineering](backend-engineering/README.md) → [MySQL](mysql/README.md) → [Redis](redis/README.md) → [Vector Database](vector-db/README.md) → [LLM Foundation（应用工程深度）](llm-foundation/README.md) → [RAG](rag/README.md) → [Agent](agent/README.md) → [System Design](system-design/README.md)

所有模块标题和名称都可以直接点击进入对应 README。

---

## 3. 每个模块现在都使用同一套结构

```text
README.md
├─ 模块职责 / 在十板块中的位置
├─ beginner-first 正式主线
├─ 正式章节目录
├─ HUMAN-A 如何影响复习深度
├─ 模块边界
├─ Review / Interview / Evidence 入口
└─ 完成状态与上一环 / 下一环导航

docs/
└─ 系统正文

review/
└─ 第二遍总图与综合自测

interview/
├─ 高频面试题
├─ 面试易错点
└─ 面试前速查表
```

Python 额外保留 Coding 小题；Agent / FastAPI / AIBE 还维护专门的权威资料或源码索引。

---

## 4. 为什么教材文件数和 Canonical 数不一样

```text
HUMAN-A / Canonical Question = 可独立追问的面试能力
Capability Primitive          = 更细的工程机制
教材 Markdown                 = 一个完整认知闭环
Section                       = 参数 / 变体 / Failure / 追问
```

因此不会默认 `1 Canonical = 1 Markdown`。当前 10 个模块共 **185 个正文知识块**，研究层当前保持 **235 道 ACTIVE Canonical**。

详见：[Curriculum Granularity Audit](roadmap/curriculum-granularity-audit.md)。

---

## 5. 真人面经证据体系

正式市场证据只允许来自 **HUMAN-A：候选人本人第一人称、高信息密度、可核验的真实招聘流程**。

```text
Current HUMAN-A             287（S001–S287）
Formal Batch                 28
ACTIVE Canonical            235
Historical mapping baseline 278 Mapped + 1 VALID-UNMAPPED（S271）
Latest S280–S287            pending periodic Canonical mapping / review
```

从 2026-09-16 起，Research 层进入 **Continuous Monitoring**：每天滚动发现最近 3 天的新面经，但任何新来源分配 `Sxxx` 前仍必须回读全部历史 Batch 做严格去重。新增市场信号先进入 Research 层，不因单日热点直接修改 Curriculum。

源码、官方文章、规范和论文可以帮助我们补齐知识边界，但**不能创建面试频率，也不能提高 Source Count**。

入口：[Research Home](research/README.md) · [Market Analysis](research/analysis/README.md) · [Verified Follow-up Chains](research/analysis/follow-up-chains.md)

---

## 6. 统一学习方法

完整执行版见：[Learning Path｜十板块正式学习路线](roadmap/learning-path.md)。Learning Path 是推荐节奏，不是唯一课表；可以按个人基础、目标和时间预算调整速度。

统一采用三遍：

1. **Curriculum Pass：** 185 个正文知识块按知识依赖完整学习，不按面经频率跳章。
2. **Review Pass：** 每个模块完成后从空白纸重画机制 / 数据流 / Failure，并完成折叠自测。
3. **Interview Pass：** 再用 HUMAN-A Heat 与 L1–L4 Depth 调整口述次数和追问深度。

仓库提供 13 周标准、8 周加速与 14 天冲刺参考；它们只作为可选执行模板，不改变模块知识依赖和正文职责。

正式教材统一追求：

> **定义能说、机制能解释、工程边界能判断、失败能定位、真人追问能接。**

---

## 7. 项目使用与质量入口

| 文档 | 作用 |
|---|---|
| [Knowledge Map](roadmap/knowledge-map.md) | 十板块职责、主线与依赖关系 |
| [Learning Path](roadmap/learning-path.md) | 可选的标准 / 加速 / 冲刺学习节奏与 Module Exit Gate |
| [Final Quality Audit](roadmap/final-quality-audit.md) | v1.0 前全仓库结构、边界、术语、版本与链接终审 |
| [Terminology Glossary](roadmap/terminology-glossary.md) | 跨模块同名概念的稳定工作定义与 Primary Ownership |
| [Documentation Style Guide](roadmap/documentation-style-guide.md) | README / 描述文件统一规范 |
| [Granularity Audit](roadmap/curriculum-granularity-audit.md) | 研究粒度与教材粒度为什么分开 |
| [Content Depth Audit](roadmap/content-depth-audit.md) | 正文深度与完成状态 |
| [Foundation Status](roadmap/foundation-status-audit.md) | Python / FastAPI / AIBE 完成状态 |
| [Progress](research/questions/progress.md) | Curriculum 与使用层当前正式状态 |
| [Module Index](research/questions/module-index.md) | Canonical Ownership ↔ Curriculum 映射 |

---

## 8. 仓库目录

```text
python/              fastapi/             backend-engineering/
mysql/               redis/               vector-db/
llm-foundation/      rag/                 agent/
system-design/

research/            # HUMAN-A / Canonical / Analysis / Source Index
roadmap/             # Knowledge Map / Learning Path / Audits / Documentation Rules
tools/               # Research validation / reproducible analysis
```

> 仓库最新 README、Knowledge Map、Learning Path、Progress 与 Module Index 是当前状态的正式来源；历史聊天和旧摘要不能覆盖仓库当前描述。
