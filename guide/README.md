# Guide｜知识地图、学习路线与仓库治理

[↑ Handbook 总目录](../README.md) · [Products](../products/README.md)

Guide 负责跨模块导航与整个知识系统的一致性，不承载具体技术模块正文或成熟产品源码正文。

## 学习入口

- [Knowledge Map](knowledge-map.md)：十模块职责、依赖、Products 与实践层的关系。
- [Learning Path](learning-path.md)：正式学习顺序、标准/加速/冲刺节奏、Exit Gate 与成熟源码学习入口。
- [Products](../products/README.md)：成熟 AI 系统源码学习总入口。
- [Terminology Glossary](terminology-glossary.md)：跨模块稳定术语。
- [Documentation Style Guide](documentation-style-guide.md)：文档写作与结构规范。

## 质量治理

- [Audits](audits/README.md)：粒度、深度、Foundation 与全仓库质量审计。
- [Project Records](project/README.md)：迁移、专项修订和集成等项目演进记录。

开发工作流与版本管理实践统一维护在 [Practice / Tooling](../practice/tooling/README.md)。

<!-- learning-inventory:start -->
## 导航事实来源

[学习资源索引](navigation-index.md)汇总当前课程、产品、实践和资料入口；[学习顺序配置](learning-order.json)决定模块先后，[机器可读目录](navigation-index.json)由现有文件生成。

维护时运行 `python tools/sync_outer_navigation.py --check` 检查漂移；先查看默认预览，再使用 `--apply` 更新。历史面经统计和正文不属于同步写入范围。
<!-- learning-inventory:end -->
