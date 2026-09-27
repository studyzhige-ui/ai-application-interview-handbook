# Curriculum Content Depth｜验收标准与模块证据

[← Handbook](../../README.md) · [学习资源索引](../navigation-index.md) · [粒度与边界](curriculum-granularity-audit.md) · [质量入口](final-quality-audit.md)

正文深度由读者能否建立模型、推演过程和识别边界判断，不由字数、标题数、章节数或文件大小决定。下面的记录入口指出“在哪里查看该次审查”，不是统一 PASS 标签。

## 验收标准

一个知识块围绕可独立理解的问题展开：先说明为什么需要，再解释规则和机制，用给足输入的例子追踪过程，展示失败条件与取舍，最后以小结、口述、易错点和默认折叠自测收束。不同主题按需要组织，不机械套相同章节模板。

简单主题可以较短；复杂子系统只有概览或字段清单不能算讲透。代码检查、结构检查和阅读审查分别记录；课程示例、真实服务与生产实验分开报告。

## 如何读取专项记录

先看记录的基线、覆盖章节、保留与修改判断，再看测试环境和未验证项。一个旧稿快照、一次链接检查或局部解释修订，都不能冒充整门课程重验。System Design 没有本轮独立专项复验记录时，明确保留这个限制，不沿用旧版绿色状态。

## 历史与后续

Python 的基础覆盖整改、MySQL 与 Redis 的 reader-first 重组、Agent 的协议与扩展分章等历史事实保留在各自项目记录。它们说明内容演进，不改变冻结的面经统计。

后续修订遵循“确定认知闭环 → 修改正文与配套 → 检查示例和导航 → 内容审查 → 记录适用范围”。学习反馈继续进入下一次修订，不以既有完成标记阻止改进。

<!-- current-scope:start -->
## 课程范围与证据索引

| 顺序 | 模块 | 正文 | 专项记录入口（按记录自身范围） |
|---:|---|---:|---|
| 01 | [Python](../../curriculum/01-python/README.md) | 13 | [Python Reader Revision｜读者可理解性与课程重组记录](../project/python-reader-revision.md) |
| 02 | [FastAPI](../../curriculum/02-fastapi/README.md) | 16 | [FastAPI 核心范围与表达复核｜2026-09-26](../project/fastapi-core-scope-review-2026-09-26.md) · [FastAPI｜递进落点与真人面经校验记录](../project/fastapi-interview-alignment-2026-09-26.md) |
| 03 | [MySQL](../../curriculum/04-mysql/README.md) | 19 | [MySQL 读者视角重组记录｜2026-09-27](../project/mysql-reader-revision-2026-09-27.md) |
| 04 | [Redis](../../curriculum/05-redis/README.md) | 18 | [Redis｜从零基础阅读过程重组课程](../project/redis-reader-restructure-2026-09-27.md) |
| 05 | [Backend](../../curriculum/03-backend-engineering/README.md) | 22 | [Backend｜讲解清晰度精修与验证记录](backend-clarity-refinement-2026-09-28.md) |
| 06 | [Vector DB](../../curriculum/06-vector-db/README.md) | 16 | [Vector DB Reader Revision｜向量数据库模块维护记录](../project/vector-db-reader-revision.md) |
| 07 | [LLM Foundation](../../curriculum/07-llm-foundation/README.md) | 14 | [LLM Foundation｜讲解清晰度精修与验收](../project/llm-foundation-clarity-refinement-2026-09-27.md) |
| 08 | [RAG](../../curriculum/08-rag/README.md) | 14 | [RAG｜讲解清晰度精修验收](rag-clarity-refinement-2026-09-27.md) |
| 09 | [Agent](../../curriculum/09-agent/README.md) | 24 | [Agent 内容保留、教学修订与发布记录](../project/agent-reader-revision.md) |
| 10 | [System Design](../../curriculum/10-system-design/README.md) | 19 | 无本轮独立专项复验记录；不继承旧版 PASS |

记录入口不自动授予通过状态；需要查看其基线、修改范围、实际检查和未验证项目。
<!-- current-scope:end -->
