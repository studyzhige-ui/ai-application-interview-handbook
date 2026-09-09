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
