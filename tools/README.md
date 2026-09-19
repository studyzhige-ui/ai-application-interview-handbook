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
