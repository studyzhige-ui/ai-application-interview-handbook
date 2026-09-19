# Tools｜研究与质量自动化脚本

[↑ Handbook 总目录](../README.md)

该目录服务 Market / Interview / Guide 的可复现分析与质量检查，不属于学习 Curriculum。

| Script | 作用 |
|---|---|
| `build_market_analysis.py` | 从 HUMAN-A 与 Canonical 构建市场分析 |
| `build_gap_candidates.py` | 生成待人工核验的 Gap 候选 |
| `apply_canonical_audit.py` | 应用 Canonical 审计结果 |
| `validate_source_coverage.py` | 校验来源覆盖与映射 |
| `validate_agent_readability.py` | 校验 Agent 教材可读性与结构 |
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
