# Repository Integration｜课程、产品与实践的集成入口

[← Handbook](../../README.md) · [学习资源索引](../navigation-index.md) · [质量与验证](../audits/final-quality-audit.md)

本页提供整合后的职责关系、阅读入口和验证边界。模块专项修订保存在本目录与[审计目录](../audits/README.md)，不把首版完成记录当成后续全部版本的质量结论。

## 八层职责

Curriculum 建立通用模型；Products 在固定源码里对照实现；Practice 将理解转成代码与开发操作。Market 保存招聘证据，Interview 归一化面试能力，References 约束技术事实；Guide 维护导航与审查，Tools 负责可复现生成和检查。

## 维护中的边界

正文、Review、Interview、labs/examples 在模块入口相互衔接。跨模块顺序由前置关系决定，模块内部顺序以其 README 为准。课程目录完整不等于实验运行、内容审查或生产验证已经完成。

面经统计继续使用 `S001–S279 / 235 ACTIVE` 冻结基线；市场总量以[Market](../../market/README.md)为准。冻结的[Canonical 覆盖记录](../../interview/canonical/progress.md)不承担当前课程进度。

## Agent 与 System Design 的衔接

Agent 负责模型判断怎样进入受控行动、结果怎样影响下一步，以及任务在取消、中断或批准后怎样继续。System Design 将这些机制放入容量、权威状态、租户隔离和外部协议中，推导完整方案；不把职责分离自动等同于必须拆成多个服务。

[Agent 综合推演](../../curriculum/09-agent/review/README.md#综合推演)用于定位执行边界，[System Design 独立设计任务](../../curriculum/10-system-design/review/README.md#独立设计任务为两个团队交付报告助手)用于验证跨模块迁移。集中问答、自测与本地实验各有用途；标准库模拟通过不等于真实恢复和生产承诺已兑现。

## 发布依据

从最新 `main` 读取受影响文件，只合并经过检查的差异。生成文件与生成源一起更新，合并后再次核验。分支完成任务后清理；不因名称像旧分支就丢弃未保留的成果。外围同步与分支核对分别保留在[首轮记录](../audits/peripheral-sync-2026-09-28.md)和[Agent / System Design 增量同步记录](../audits/peripheral-sync-agent-system-design-2026-09-28.md)。

<!-- current-scope:start -->
## 正式学习主线

[Python](../../curriculum/01-python/README.md) → [FastAPI](../../curriculum/02-fastapi/README.md) → [MySQL](../../curriculum/03-mysql/README.md) → [Redis](../../curriculum/04-redis/README.md) → [Backend](../../curriculum/05-backend-engineering/README.md) → [LLM Foundation](../../curriculum/06-llm-foundation/README.md) → [Vector DB](../../curriculum/07-vector-db/README.md) → [RAG](../../curriculum/08-rag/README.md) → [Agent](../../curriculum/09-agent/README.md) → [System Design](../../curriculum/10-system-design/README.md)

课程合计 175 篇；Products 与 Coding 作为独立轨道。正文标题、阅读顺序、配套入口与内容指纹见[机器目录](../navigation-index.json)。
<!-- current-scope:end -->
