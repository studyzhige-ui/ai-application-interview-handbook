# Repository Integration Status

## 2026-09-09：Python → AI Application Handbook

本次整合把原独立 `python-interview-handbook` 的正文、图解自测和面试专项完整迁入本仓库 `python/`，并将总学习路线扩展为：

```text
Python → FastAPI → AI Backend Engineering → MySQL → Redis → Vector DB → RAG → Agent Harness → System Design
```

### Python 已迁移内容

- `python/docs/`：12 章系统正文
- `python/review/`：12 章 Mermaid 图解与折叠自测 + 总入口
- `python/interview/`：高频面试题、Coding 小题、易错点、速查表
- `python/README.md`：从独立 Python 面试手册升级为总体系的 Python Foundation

迁移时保留了此前修复后的 Mermaid 保守兼容语法与 GitHub `<details>` 折叠答案。

### 新增一级模块

- `fastapi/`：从 Python 到真实 AI HTTP/API Service 的服务层
- `backend-engineering/`：Timeout、Retry、Idempotency、MQ、Backpressure、Observability、Deployment 等横向生产工程能力

### 旧 Python 仓库策略

旧仓库不删除，保留为历史版本 / 独立入口；本次整合合并到主分支后，在旧仓库 README 顶部增加迁移提示，明确本仓库的 `python/` 为后续主维护版本。
