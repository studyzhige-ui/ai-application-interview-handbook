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
| `sync_official_2027_agent_jobs.py` | 汇总浏览器与官方 ATS/API，加工 2027 Agent / AI 应用候选池 |
| `audit_official_2027_job_sources.py` | 分离审计“职位是否可获取”与“是否有 2027 届官方证据” |
| `validate_official_2027_source_contracts.py` | 强制每家公司都有 `official_root + job_list_url`，且不得使用二手招聘域名 |
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

## 2027 官方岗位采集原则

岗位采集不按公司手工维护一套抓取逻辑。固定模型是：

```text
official_root        # 证明招聘入口来自公司第一手官网
       ↓
job_list_url         # 日常固定打开的官方职位列表页 / 官方 ATS
       ↓
统一浏览器穷举关键词 + 翻页 / 无限滚动
       ↓
打开命中职位详情读取官方 JD
       ↓
2027 届别 Gate + 非算法工程 Role Scope
```

专用 API / Feishu / Moka 适配器只用于提速；它们失败时必须回退到固定 `job_list_url`，不能把接口失败解释为“0 岗位”。
