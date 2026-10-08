# 官方岗位采集与纳入策略

## 1. 数据模型

```text
69 家目标公司第一方招聘 / 校招入口
        ↓ 岗位存在性核验
official-company-role-index.*
        ↓ 第一方 API / ATS / 浏览器补全与 Role Family 去重
official-2027-agent-jobs.generated.*
        ↓ 代表性高价值 JD / 面试研究
ai-agent-jd-market.md
```

- [69 家公司岗位状态索引](../01-data/official-company-role-index.md)：全部公司保留第一方职位池；已有岗位、完整枚举 0 岗、待枚举分别记录。
- [全量 Role Family / JD 层](../01-data/official-2027-agent-jobs.generated.md)：保存完整第一方 JD、官方标题和待补正文岗位。
- [覆盖审计](../02-analysis/official-2027-coverage-audit.generated.md)：检查 69/69 公司扫描覆盖，并把 Runtime 抓取状态与岗位事实分开。
- [69 家公司扫描池](../02-analysis/company-scan-pool.md)：全量公司名单、主要业务、第一方职位池和当前状态。

## 2. 正式纳入 Gate

代表岗位必须是开发、研发、工程师、全栈、前后端、平台、架构、Infra、Runtime、Harness、FDE 等工程角色，并且职责主体与 Agent / 智能体 / AI 应用 / 大模型应用 / Coding Agent / RAG / MCP / Tool / Workflow 等相关。算法训练、研究、产品、销售、运营等不作为本库的代表工程岗位。

同公司、职责高度一致但城市 / 职位 ID 不同的岗位按 Role Family 合并；所有已知官方 Requisition 仍保留在全量层。

## 9. 可重复官方发现

- [官方 2027 公司源注册表](official-2027-campus-sources.json)
- [官方动态站发现结果](../01-data/official-2027-agent-jobs.generated.md)
- [统一同步器](../04-scripts/jd.py)
- [小米 ATSX Node 适配器](../04-scripts/jd/adapters/xiaomi.mjs)
- [字节 ATSX Node 适配器](../04-scripts/jd/adapters/bytedance.mjs)

```text
逐公司确认 2027 官方项目
→ 官方项目/API全量枚举
→ Agent/AI应用多关键词 + JD正文召回
→ 算法/非目标岗排除
→ 2027届别复核
→ Role Family 去重
→ 正式库
```
