# Foundation｜基础依赖与验收入口

[← Handbook](../../README.md) · [正式学习路线](../learning-path.md) · [正文深度证据](content-depth-audit.md)

基础学习按“语言与执行 → 网络接口 → 持久数据 → 缓存与短期状态 → 后端可靠性”递进。Python、FastAPI、Backend 是跨层骨架，但 MySQL 与 Redis 是进入 Backend 可靠任务、幂等和一致性组合之前的明确前置，不能在路线里省略。

## 每一步需要建立什么

Python 让读者解释对象、调用、异常与并发。FastAPI 把这些机制放入请求、依赖、资源与响应边界。MySQL 建立表、约束、事务与并发修改模型；Redis 建立命令、生命周期、缓存和原子修改模型。Backend 再组合容量预算、幂等、消息、持久任务、安全、观测与部署。

FastAPI 的外部资源练习可以使用教学替身，不要求先实现完整数据库系统。需要回看的特殊操作可以就地解释；关键前置模型则不能靠一个跨章链接代替。

## 验收怎样完成

先按模块 README 阅读，再用 Review 重建过程，用 Interview 训练解释和失败推演。实验与示例按其运行条件验证。能列出目录只证明材料存在；是否达到学习目标，须结合练习结果与记录中的内容审查范围判断，不使用永久的 Foundation COMPLETE 标记。

Canonical Coverage 是冻结面经能力覆盖，不是课程完成度，更不是读者个人进度。

<!-- current-scope:start -->
## 课程范围与证据索引

| 顺序 | 模块 | 正文 | 专项记录入口（按记录自身范围） |
|---:|---|---:|---|
| 01 | [Python](../../curriculum/01-python/README.md) | 13 | [Python Reader Revision｜读者可理解性与课程重组记录](../project/python-reader-revision.md) |
| 02 | [FastAPI](../../curriculum/02-fastapi/README.md) | 16 | [FastAPI 核心范围与表达复核｜2026-09-26](../project/fastapi-core-scope-review-2026-09-26.md) · [FastAPI｜递进落点与真人面经校验记录](../project/fastapi-interview-alignment-2026-09-26.md) |
| 03 | [MySQL](../../curriculum/04-mysql/README.md) | 19 | [MySQL 读者视角重组记录｜2026-09-27](../project/mysql-reader-revision-2026-09-27.md) |
| 04 | [Redis](../../curriculum/05-redis/README.md) | 18 | [Redis｜从零基础阅读过程重组课程](../project/redis-reader-restructure-2026-09-27.md) |
| 05 | [Backend](../../curriculum/03-backend-engineering/README.md) | 22 | [Backend｜讲解清晰度精修与验证记录](backend-clarity-refinement-2026-09-28.md) |

记录入口不自动授予通过状态；需要查看其基线、修改范围、实际检查和未验证项目。
<!-- current-scope:end -->
