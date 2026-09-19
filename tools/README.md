# Tools｜研究与质量自动化脚本

[↑ Handbook 总目录](../README.md)

该目录服务 Market / Interview / Guide 的可复现分析与质量检查，不属于学习 Curriculum。

| Script | 作用 |
|---|---|
| `build_market_analysis.py` | 从 HUMAN-A 与 Canonical 构建市场分析 |
| `build_gap_candidates.py` | 生成待人工核验的 Gap 候选 |
| `apply_canonical_audit.py` | 应用 Canonical 审计结果 |
| `validate_source_coverage.py` | 校验来源覆盖与映射 |
| `validate_agent_readability.py` | 校验全仓库 Markdown 链接、Agent 教材可读性与结构 |
| `validate_repository_semantics.py` | 校验 185-block 结构、Market / Canonical 时间边界、旧路径与章节语义漂移 |
| `fetch_dynamic_official_jobs.mjs` | 从每家公司固定第一手 `job_list_url` 统一搜索、翻页并读取官方职位详情 |
| `sync_official_2027_agent_jobs.py` | 汇总浏览器与官方 ATS/API，应用严格非算法工程 Gate，并生成 Role Family 全量 JD 层 |
| `audit_official_2027_job_sources.py` | 分离审计“当前严格结果是否闭环”与“自动维护链路是否已完整枚举” |
| `validate_official_2027_source_contracts.py` | 强制 41 家公司都有 `official_root + search_url`，并校验第一方招聘域与招聘池范围 |
| `phase2b_canonical_audit.json` | Phase 2B Canonical 审计数据 |

脚本使用的仓库路径基线：

```text
market/
interview/canonical/
curriculum/
guide/
references/
```

脚本输出不能替代人工 provenance / Role Scope / Source Quality 审核。


## 生成文件一致性

`market/analysis/` 中由脚本生成的索引、覆盖、统计与 README 以 `tools/` 生成源为权威。CI 会重新运行 Canonical Audit、Gap Candidate、Market Analysis 与 Source Coverage，并要求生成后 `git diff --exit-code`；如果手工改了生成结果却没有同步生成器，验证会失败。

**生成文件必须可复现，当前状态文本必须可验证。**

## 官方岗位采集原则

岗位采集使用统一的第一方招聘池契约：

```text
official_root        # 证明来源属于公司官网 / 官方招聘体系
       ↓
search_url           # 可重复进入并枚举的固定第一方职位池
       ↓
board_scope
  ├─ campus              # 当前校园招聘 / 应届职位池
  └─ official_recruiting # 当前官方混合招聘池，JD 必须明确允许应届生
       ↓
完整分页 + 全关键词穷举 / 官方 API 全量枚举
       ↓
严格 Role Scope：Agent / AI应用 / RAG / Harness / Runtime / Infra / Coding Agent 工程
       ↓
排除算法、模型训练/研究、产品、销售、运营、纯实习与普通岗位 AI 工具套话
       ↓
Role Family 去重 + 第一方 JD 正文
```

专用 API / Feishu / Moka / ATS 适配器用于提高稳定性和效率；失败时必须回退到固定 `search_url`。只有完整枚举后的 0 才是有效结论。

`validate_official_2027_source_contracts.py` 同时强制官方源注册表与岗位核验索引**恰好等于固定 41 家公司**：缺失、重复或额外公司都会使 CI 失败，避免旧公司或临时测试公司重新混入正式矩阵。

审计同时保留两种状态：**Persistent Coverage Closure** 表示固定 41 家公司全部具备第一方招聘入口，并且每家公司至少有一个已核验目标工程岗位；**Recurring Runtime Certification** 表示本轮定时采集器已经实际完成该公司的分页 / 关键词穷举。覆盖事实与本轮运行健康度不能互相冒充。

Runtime Certification 还要求本轮 Browser / Feishu / Moka 缓存通过 `generated_at` freshness gate；过期缓存可以保留历史证据，但不能把本轮 Runtime 标成 `ENUMERATED`。
