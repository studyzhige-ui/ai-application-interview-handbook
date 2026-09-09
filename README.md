# AI Application Interview Handbook

面向 AI 应用开发 / AI Agent 开发求职的系统化学习与面试手册。

本仓库遵循两个原则：

1. **知识体系为骨架**：MySQL、Redis、Vector DB、RAG、Agent Harness 都从 0 建立完整知识体系，不以面经题目代替教材。
2. **真实面经为校验与血肉**：持续收集 2026 年公开可访问的 AI 应用 / Agent 相关真实面经，提取、去重、归一化问题，并反向检查知识体系的覆盖缺口。

## 规划中的模块

- `mysql/`
- `redis/`
- `vector-db/`
- `rag/`
- `agent-harness/`
- `system-design/`
- `research/`：真实面经数据集、规范化问题库、频率分析与覆盖矩阵
- `roadmap/`：总知识地图与学习路线

## Agent Harness 权威实现参考

Agent Harness / Runtime 模块以以下两个源码仓库为首要实现参考：

- Claude Code：`studyzhige-ui/claude-code-source-private`
- OpenAI Codex：`openai/codex`

目标不是复制某个框架 API，而是从成熟 Agent 产品源码中抽取稳定的 Runtime / Harness 设计能力：工具执行、权限与审批、沙箱、上下文管理、会话与状态、MCP、可靠性、异步执行、可观测性、安全边界等。

详细原则见：[`roadmap/agent-authoritative-sources.md`](roadmap/agent-authoritative-sources.md)

## 研究工作流

```text
真实面经
  ↓
来源归档（保留元数据与原始问法的简洁转述）
  ↓
问题提取
  ↓
完全重复 / 转载去重
  ↓
语义归一化
  ↓
模块与知识点标签
  ↓
频率 / 公司覆盖 / 深度分析
  ↓
反向校验完整知识体系
  ↓
发现缺口 → 补充教材
```

> 注意：第三方面经只保存来源信息与面试问题的简洁转述，不复制整篇受版权保护的帖子。

## 当前研究进度

已启动 2026 面经大规模采集：

- [`research/interviews/batch-01.md`](research/interviews/batch-01.md)：第一批 15 个高密度来源/合集样本。
- [`research/interviews/batch-02.md`](research/interviews/batch-02.md)：新增快手、拼多多、网易、第四范式等工程化样本。
- [`research/questions/canonical-batch-01.md`](research/questions/canonical-batch-01.md)：第一版语义归一化问题库。
- [`research/questions/canonical-batch-02-delta.md`](research/questions/canonical-batch-02-delta.md)：Batch 02 新增问题与课程目录约束。

当前数据仅是研究初期批次，不用于宣称最终频率结论。后续继续按公司、岗位别名、月份和技术关键词扩展，再统一做转载去重、语义聚类、频率统计和覆盖矩阵。
