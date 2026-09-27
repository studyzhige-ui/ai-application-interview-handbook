# Repository Integration｜课程、产品与实践的集成入口

[← Handbook](../../README.md) · [学习资源索引](../navigation-index.md) · [质量与验证](../audits/final-quality-audit.md)

本页提供整合后的职责关系、阅读入口和验证边界。模块专项修订保存在本目录与[审计目录](../audits/README.md)，不把首版完成记录当成后续全部版本的质量结论。

## 八层职责

Curriculum 建立通用模型；Products 在固定源码里对照实现；Practice 将理解转成代码与开发操作。Market 保存招聘证据，Interview 归一化面试能力，References 约束技术事实；Guide 维护导航与审查，Tools 负责可复现生成和检查。

## 维护中的边界

正文、Review、Interview、labs/examples 在模块入口相互衔接。跨模块顺序由前置关系决定，模块内部顺序以其 README 为准。课程目录完整不等于实验运行、内容审查或生产验证已经完成。

面经统计继续使用 `S001–S279 / 235 ACTIVE` 冻结基线；市场总量以[Market](../../market/README.md)为准。冻结的[Canonical 覆盖记录](../../interview/canonical/progress.md)不承担当前课程进度。

## 发布依据

从最新 `main` 读取受影响文件，只合并经过检查的差异。生成文件与生成源一起更新，合并后再次核验。分支完成任务后清理；不因名称像旧分支就丢弃未保留的成果。具体外围同步与分支核对见[2026-09-28 审查记录](../audits/peripheral-sync-2026-09-28.md)。

<!-- current-scope:start -->
## 正式学习主线

[Python](../../curriculum/01-python/README.md) → [FastAPI](../../curriculum/02-fastapi/README.md) → [MySQL](../../curriculum/04-mysql/README.md) → [Redis](../../curriculum/05-redis/README.md) → [Backend](../../curriculum/03-backend-engineering/README.md) → [Vector DB](../../curriculum/06-vector-db/README.md) → [LLM Foundation](../../curriculum/07-llm-foundation/README.md) → [RAG](../../curriculum/08-rag/README.md) → [Agent](../../curriculum/09-agent/README.md) → [System Design](../../curriculum/10-system-design/README.md)

课程合计 175 篇；Products 与 Coding 作为独立轨道。正文标题、阅读顺序、配套入口与内容指纹见[机器目录](../navigation-index.json)。
<!-- current-scope:end -->
