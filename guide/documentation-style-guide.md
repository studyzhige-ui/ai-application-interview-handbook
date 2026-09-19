# Documentation Style Guide｜README 与状态描述规范

[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Final Quality Audit](audits/final-quality-audit.md) · [Terminology Glossary](terminology-glossary.md) · [Progress](../interview/canonical/progress.md)

> 目标：让任何人打开任意一级模块或核心状态页，都能使用同一种信息架构理解“这是什么、现在是什么状态、从哪里来、接下来去哪里”。

## 一级模块 README 固定结构

```text
# Module｜一句话角色
上一模块 · Handbook 总目录 · Learning Path · 下一模块
状态 / Blocks / Canonical / Source Coverage

1. 这个模块解决什么
2. 在十板块中的位置
3. 固定课程原则
4. 正式学习主线
5. 正式课程目录
6. HUMAN-A 怎样影响本模块
7. 模块边界
8. Review / Interview / Evidence 入口
9. 推荐学习方式
10. 完成状态
```

- Learning Path 是推荐使用方式，不是模块元数据；一级模块 README / Review README 只保留简洁入口，不写死 Week / Session，避免绑定某一种学习节奏。

## Review README 固定结构

- 顶部必须能返回模块主页和 Handbook；
- 可提供 Learning Path 作为可选入口，但不在 Review 中写死 Week / Session；
- 明确它属于第二遍复习，不重复正文；
- 自测答案默认使用 `<details>` 折叠；
- 图解优先使用保守 GitHub Mermaid。

## 根 README / Knowledge Map

- 十个一级模块名称必须直接可点击；
- 所有模块使用同一列信息：角色、Blocks、Canonical、状态；
- 不在根 README 对某个模块展开数倍于其它模块的细节；
- 详细内容进入模块 README。

## 状态源优先级

```text
当前仓库文件
> Progress / Knowledge Map / Module README
> 历史审计记录
> 聊天摘要 / 旧 PR 描述
```

## 同步规则

模块状态改变时，至少核验：根 README、模块 README、Review README、Knowledge Map、Progress、Module Index、Canonical README、自动生成 Analysis README 的生成源、本地 Markdown 链接，以及是否需要更新 Final Quality Audit / Terminology Glossary 中的跨模块边界。


## 正文可理解性与证据规则

从具体任务和中文解释开始，首次重要英文名给中文含义。字段清单之前说明每项信息服务什么决定；不把“运行事实”“结构化”当不需解释的答案。每章就地保留“面试怎么答、易错点、章节自测”，不能仅链接到集中题库。产品过程用可选折叠承载，明确快照、入口函数、触发、输入、变更、输出和限制；不虚构所有版本相同。

相同故障在不同章节出现时说明当前责任，把完整机制链接回主责章。Trace与恢复数据分开，记录策略由业务需要和隐私约束决定，不以全量收集替代设计。结构/字数/折叠检查只验证文档形式，不作为初学者理解或真实系统可靠性的证明。


## Agent章末的固定形式（2026-09-17）

HUMAN-A信号提供来源关联；面试回答以Q和🎯可见引用块展示；高频易错点用⚠️逐条提醒；自测以题目本身作为折叠标题。不能把四者统一成“查看参考答案”按钮。正文保留引入、分层解释、例子和失败推演；源码对照可选折叠，不用来源清单代替讲解。
