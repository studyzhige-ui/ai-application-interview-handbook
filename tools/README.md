# Tools｜研究与质量自动化脚本

[↑ Handbook 总目录](../README.md)

该目录服务 Market / Interview / Guide 的可复现分析与质量检查，不属于学习 Curriculum。

| Script | 作用 |
|---|---|
| `build_market_analysis.py` | 从 HUMAN-A 与 Canonical 构建市场分析 |
| `build_gap_candidates.py` | 生成待人工核验的 Gap 候选 |
| `apply_canonical_audit.py` | 应用 Canonical 审计结果 |
| `sync_expected_canonical_count.py` | 将 Market Analysis 的 Canonical 计数与已审核审计基线同步（跨平台） |
| `validate_source_coverage.py` | 校验来源覆盖与映射 |
| `validate_agent_readability.py` | 校验全仓库 Markdown 链接、Agent 教材可读性与结构 |
| `validate_repository_semantics.py` | 按实际文件与生成目录校验课程结构、Market / Canonical 时间边界、旧路径与章节语义漂移 |
| `fetch_dynamic_official_jobs.mjs` | 从每家公司固定第一手 `job_list_url` 统一搜索、翻页并读取官方职位详情 |
| `sync_official_2027_agent_jobs.py` | 汇总浏览器与官方 ATS/API，应用严格非算法工程 Gate，并生成 Role Family 全量 JD 层 |
| `audit_official_2027_job_sources.py` | 分离审计“当前严格结果是否闭环”与“自动维护链路是否已完整枚举” |
| `validate_official_2027_source_contracts.py` | 强制 69 家扫描公司都有 `official_root + search_url`，并校验第一方招聘域与招聘池范围 |
| `phase2b_canonical_audit.json` | Phase 2B Canonical 审计数据 |

脚本使用的仓库路径基线：

```text
market/
interview/canonical/
curriculum/
products/
practice/
guide/
references/
```

脚本输出不能替代人工 provenance / Role Scope / Source Quality 审核。


## GitHub Actions Runner 策略

工作流同时保留 Windows 与 Linux 两套执行路径，但**同一次运行只会启用其中一套**：

- 仓库为 private：运行 `[self-hosted, Windows]`，用于已配置的本地 Runner；GitHub-hosted Linux job 在 job-level `if` 阶段直接跳过，不消耗 GitHub-hosted minutes。
- 仓库为 public：运行 `ubuntu-latest`，Windows self-hosted job 直接跳过。公开仓库的 PR / push 不会执行本地 Windows Runner，从而避免把公开贡献代码带到本地机器执行。
- 两套 job 共享同一套 `tools/` 脚本、数据契约与生成结果；OS 差异只保留在 Playwright 安装、临时目录和 Git 提交 shell 等必要位置。
- Windows Runner 需要注册到本仓库并具有默认 `self-hosted`、`Windows` labels。Runner 的名称、在线状态与可用环境以 Actions 设置和本次运行结果为准，不从历史测试推断持续在线。

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

`validate_official_2027_source_contracts.py` 强制官方源注册表与岗位状态索引**恰好等于固定 69 家扫描公司**：缺失、重复或额外公司都会使 CI 失败。每家公司必须有第一方职位池，但不再要求当前一定有目标岗位。

审计分离三层状态：**Company Scan Coverage** 表示固定 69 家都有第一方招聘入口；**Target JD Presence** 表示 `HAS_TARGET_JDS / ZERO_TARGET_JDS / NEEDS_ENUMERATION`；**Recurring Runtime Certification** 表示本轮定时采集器已经实际完成该公司的分页 / 关键词穷举。三者不能互相冒充。

Runtime Certification 还要求本轮 Browser / Feishu / Moka 缓存通过 `generated_at` freshness gate；过期缓存可以保留历史证据，但不能把本轮 Runtime 标成 `ENUMERATED`。

<!-- outer-sync:start -->
## 全仓外围导航同步

- [`sync_outer_navigation.py`](sync_outer_navigation.py)：只读扫描全仓 Markdown 的路径、锚点与冲突残留；只在明确允许的入口页、状态页和生成索引内同步数量、顺序、正文指纹与证据入口；默认只预览，`--check` 检查漂移，`--apply` 才写入。
- [`sync_learning_navigation.py`](sync_learning_navigation.py)：复用已有的路线与前后导航转换，保留目录标识。
- [`test_outer_navigation.py`](test_outer_navigation.py)：验证计数、保护边界、真实阅读顺序、链接解析、冲突示例和重复运行。

正文、源码与实践资料可被读取和校验，但不会被同步器改写。同步不会重新生成 Market / Canonical，也不自动宣称阅读或实机验证通过。
<!-- outer-sync:end -->
