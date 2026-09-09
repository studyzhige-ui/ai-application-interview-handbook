# 2026 AI 应用 / Agent 面经研究

这里不是“面试题大全”，而是整套知识体系的 **招聘现实校准层**。

## 研究目标

- 尽可能覆盖 2026 年公开可访问的 AI 应用开发、AI Agent 开发、RAG / LLM 应用、Applied AI 等相关面经。
- 保留“原始面经来源”和“规范化问题库”两层，避免去重后丢掉真实面试官的问法。
- 用真实问题反向检查 MySQL、Redis、Vector DB、RAG、Agent Harness 等系统课程是否有缺口。

## 数据层次

### 1. Sources / Interviews

每份面经记录：

- source_id
- 平台
- 日期
- 公司
- 岗位
- 轮次（若已知）
- 原始链接
- 可访问状态
- 问题的简洁转述

第三方面经不整篇复制，只保存研究所需的事实性元数据与问题转述。

### 2. Canonical Questions

将语义等价问题归一化为 canonical question，例如：

- “上下文窗口满了怎么办？”
- “Context 超过限制怎么处理？”
- “Agent 长上下文如何压缩？”

可以归到“Agent 上下文接近/超过窗口限制时，如何设计压缩与保真机制？”，但仍保留来源与变体。

### 3. Taxonomy

问题至少标注：

- 一级模块：MySQL / Redis / Vector DB / RAG / Agent Harness / Python / Backend / LLM / System Design / Project
- 二级知识点
- 问题类型：Definition / Principle / Comparison / Debugging / Design / Project Deep Dive / Coding
- 深度：Basic / Intermediate / Advanced

## 去重规则

1. **转载重复**：同一面经被重复搬运，只计一次。
2. **语义重复**：问法不同但核心问题相同，归并到同一 canonical question。
3. **同主题不同问题**：不合并。例如“Redis 为什么快？”与“Redis 为什么常用单线程执行命令？”属于相关但不同问题。

## 搜索策略

持续组合以下关键词：

- AI Agent 开发 / Agent 开发 / 智能体开发
- AI 应用开发 / 大模型应用开发 / LLM 应用开发
- RAG 开发 / Applied AI / AIGC 应用
- 公司名 + 上述岗位名
- LangGraph / MCP / RAG / Redis / MySQL / Vector DB / Harness / Context Engineering 等高价值术语

优先来源：牛客公开面经；后续可增量补充其他公开可访问来源。

## 批次

- Batch 01：2026-09-09，建立搜索框架并收集第一批高密度样本。
