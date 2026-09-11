# Documentation Style Guide｜README 与状态描述规范

[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Final Quality Audit](final-quality-audit.md) · [Terminology Glossary](terminology-glossary.md) · [Progress](../research/questions/progress.md)

> 目标：让任何人打开任意一级模块或核心状态页，都能使用同一种信息架构理解“这是什么、现在是什么状态、从哪里来、接下来去哪里”。

## 一级模块 README 固定结构

```text
# Module｜一句话角色
上一模块 · Handbook 总目录 · 下一模块
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

## Review README 固定结构

- 顶部必须能返回模块主页和 Handbook；
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
