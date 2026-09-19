# Documentation Style Guide｜README 与状态描述规范

[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Final Quality Audit](audits/final-quality-audit.md) · [Terminology Glossary](terminology-glossary.md) · [Progress](../interview/canonical/progress.md)

> 目标：让任何人打开任意一级模块或核心状态页，都能使用同一种信息架构理解“这是什么、职责是什么、从哪里开始、边界在哪里”。

## README 的正式身份

README 是仓库或目录的 **canonical entry document（正式入口文档）**。它描述当前有效的定义、职责、结构、使用方式、边界和权威入口，不承担 Changelog、迁移日志或聊天纪要的职责。

README 主体应优先回答：

```text
这是什么？
→ 为谁服务、解决什么问题？
→ 由哪些部分组成？
→ 各部分职责和边界是什么？
→ 应该怎样进入和使用？
→ 哪些文档是权威入口？
```

以下内容默认不写入 README 主体：

```text
以前是什么 / 原来怎样
这次为什么重构
本轮改了什么
从旧目录迁到哪里
哪些句子刚刚被重写
阶段性 PR / 聊天决策过程
```

这类信息进入 `guide/project/`、`guide/audits/`、专门的 migration / revision record 或 Changelog。

### 语言规则

README 采用稳定陈述式语言，优先写：

- “本模块负责……”
- “目录包含……”
- “课程按……组织”
- “技术事实以……为准”
- “统计基线：S001–S279”

避免把项目建设过程写成主体叙事，例如：

- “现在……”
- “不再……”
- “原来 / 以前 / 之前……”
- “本轮 / 这次 / 这一版改成……”
- “已经从 A 迁到 B……”

“当前”并非绝对禁词，但只在语义确实需要“运行时当前状态”或“明确时间基线”时使用。版本敏感事实优先写明 **版本 / commit / 核验日期**，而不是使用模糊的“现在”。

### 状态表达

状态使用名词化、可核验的元数据，而不是过程叙事：

```text
课程版本：V1
教材状态：✅ 完整
统计基线：S001–S279
资料核验日期：2026-09-11
```

不要写成：

```text
我们现在已经完成……
这次终于重构完……
原来的内容已经迁走……
```

### 例外

`guide/project/` 与 `guide/audits/` 的职责本身就是记录历史演进与审计，因此可以描述迁移、修订和历史状态；但其 README 仍应先定义“这个目录是什么”，具体过程进入目录中的记录文件。

## 一级模块 README 固定结构

```text
# Module｜一句话角色
上一模块 · Handbook 总目录 · Learning Path · 下一模块
课程版本 / 教材规模 / Canonical / Source Coverage

1. 这个模块解决什么
2. 在十板块中的位置
3. 固定课程原则
4. 正式学习主线
5. 正式课程目录
6. HUMAN-A 怎样影响本模块
7. 模块边界
8. Review / Interview / Evidence 入口
9. 推荐学习方式
10. 教材状态
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
- 根 README 只定义仓库、信息架构、主要入口和层级关系，不写迁移过程；
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

相同故障在不同章节出现时说明当前责任，把完整机制链接回主责章。Trace 与恢复数据分开，记录策略由业务需要和隐私约束决定，不以全量收集替代设计。结构/字数/折叠检查只验证文档形式，不作为初学者理解或真实系统可靠性的证明。

## Agent 章末固定形式

HUMAN-A 信号提供来源关联；面试回答以 Q 和 🎯 可见引用块展示；高频易错点用 ⚠️ 逐条提醒；自测以题目本身作为折叠标题。不能把四者统一成“查看参考答案”按钮。正文保留引入、分层解释、例子和失败推演；源码对照可选折叠，不用来源清单代替讲解。
