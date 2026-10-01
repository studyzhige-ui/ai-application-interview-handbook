# Repository Quality｜范围、证据与验证入口

[← Handbook](../../README.md) · [学习资源索引](../navigation-index.md) · [正文深度](content-depth-audit.md) · [历史审计](history/README.md)

本页区分课程范围、导航一致性、专项内容审查和运行验证。文件齐全、链接可达与 CI 成功都不能直接推导“全部教材已易读”或“系统已通过生产验收”。具体修订和运行结果按记录中的提交、环境与检查范围阅读。

## 信息架构

八个职责层分别是：`curriculum/` 通用知识，`products/` 固定源码研读，`practice/` 动手实践，`market/` 招聘证据，`interview/` 面试能力归一化，`references/` 技术依据，`guide/` 导航治理，`tools/` 自动化。Products 与 Practice 不并入正式课程章数。

## 怎样判断验证结论

| 检查对象 | 依据 | 不能据此推断 |
|---|---|---|
| 文件数量、标题、阅读顺序、配套入口 | [实际文件索引](../navigation-index.json)与各模块 README | 读者已经掌握、章节已经完成内容验收 |
| 本地路径、锚点、冲突残留、生成漂移 | `python tools/sync_outer_navigation.py --check`；[导航工作流](../../.github/workflows/validate-navigation.yml) | 外部网页仍有效、私有镜像所有读者都有权限 |
| 模块解释、题意、示例与渲染 | [模块专项审查](content-depth-audit.md) | 记录日期之后的正文都已再次验收 |
| 官方版本、源码机制 | [References](../../references/README.md)及产品固定提交 | 固定快照等于最新发行版、源码阅读等于实机运行 |
| 服务、故障与生产行为 | 对应模块实验记录中明确的环境和结果 | 本地模拟测试覆盖真实数据库、网络、模型或生产集群 |

## 时间与统计边界

Canonical 保留 `S001–S279 / 235 ACTIVE` 冻结基线；课程重排不重新计算频次、独立来源或 Primary Ownership。Market 的动态总量读取[市场入口](../../market/README.md)，不复制成长期静态结论。历史审计、Batch 和 Daily Log 保留当时事实。

## 发布与回归

先从最新 `main` 核对受影响正文，再同步入口和生成源。检查完成后通过独立分支与 PR 发布；合并后再次读取 `main`。分支清理先核验确切提交已合并，或确认旧稿被保留内容的后继稿替代；不把同名 PR 的存在当作已经合并。

外围核对按轮次记录：见[首轮全仓同步](peripheral-sync-2026-09-28.md)与[Agent / System Design 增量同步](peripheral-sync-agent-system-design-2026-09-28.md)。基线、发现和实际验证范围分别认对应记录，不复用上一轮的链接数量或通过结论。历史结论见[历史审计目录](history/README.md)。

<!-- current-scope:start -->
## 可重建的内容范围

正式课程：**10 个模块 / 175 篇正文**。Products：**4 套 / 30 篇专题正文**。Coding：**9 篇正文**。

此段由实际文件生成，只表示文档范围；检查结果与专项证据见上文。
<!-- current-scope:end -->
