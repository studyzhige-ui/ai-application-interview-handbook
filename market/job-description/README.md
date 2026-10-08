# 岗位需求与官方 JD

保管第一方岗位正文、官方链接、职位 ID、公司与岗位状态及采集时间；按当前官方校招 / 应届资格与非算法 AI 应用、Agent 工程范围进行采集和分析。公司扫描范围与当前有无目标岗位分开管理。

## 阅读入口

- [人工核验岗位正文](01-data/curated-official-jds.md)：保留人工确认的职责、要求、边界岗和排除事实
- [全量岗位正文与 Requisition](01-data/official-2027-agent-jobs.generated.md)及[结构化数据](01-data/official-2027-agent-jobs.generated.json)
- [持久化公司岗位状态](01-data/official-company-role-index.md)、[人工第一方线索](01-data/official-first-party-role-seeds.json)
- [公司扫描池](02-analysis/company-scan-pool.md)、[覆盖审计](02-analysis/official-2027-coverage-audit.generated.md)、[市场快照](02-analysis/ai-agent-jd-market.md)
- [当前采集配置](03-strategy/official-2027-campus-sources.json)与[纳入策略](03-strategy/collection-policy.md)
- [采集维护日志](05-logs/collection-history.md)

## 五层职责

| 目录 | 内容 |
|---|---|
| 01-data | 完整人工材料、浏览器 / ATS 原始采集快照、规范化岗位及公司状态；生成文件也是事实载体 |
| 02-analysis | 公司扫描与覆盖分析、人可读的市场快照 |
| 03-strategy | 当前生效的公司与官方来源配置、岗位纳入边界 |
| 04-scripts | 独立岗位业务接口、适配器、规范化、状态维护、呈现、发布和离线测试 |
| 05-logs | 保留的岗位采集日志及迁移核验记录 |

## 保存口径

迁移保留既有 JSON 快照的原始字节，包括完整正文、URL、ID、时间戳、人工种子与公司状态。历史快照中的 `generated_at` 和 `source_commit` 保持原值，不冒充本次实时采集。2026-09-20 的保存快照记录 69 家公司、479 个 Role Family、469 份第一方完整 JD；这些是该快照的口径，不是迁移后的新抓取结果。

后续采集覆盖当前快照之前，将原始字节保存为 01-data/observations 下的内容寻址观测；相同内容不重复写入。新的规范化数据保留每个 Requisition 的全部职责、要求与来源字段；家族代表正文不能取代各职位正文。采集失败、分页不完整和缓存过期均不能被解释为当前 0 岗或删除历史核验事实。

## 执行入口

从仓库根目录运行：

- `python market/job-description/04-scripts/jd.py check`：离线配置合同、Python 回归、Node 语法与浏览器回归；不会联网或更新正式数据
- `python market/job-description/04-scripts/jd.py collect --live`：显式启动网络采集、原始观测保存、规范化、公司状态维护、报表及覆盖审计
- `python market/job-description/04-scripts/jd.py audit`：只读取已保存快照并更新本地分析，不发起采集
- `python market/job-description/04-scripts/jd.py publish`：仅供 main 分支授权 Actions 使用；检查输入变化、复用同一发布实现并处理推送竞争

离线检查需要 Python 3.12+ 与 Node 22+。联网采集另需 [Python 依赖](04-scripts/requirements.txt)、Playwright 1.55.0 和 Chromium；工作流安装这些依赖。浏览器调试保留独立手动工作流，仅向 runner 临时目录输出。

[代码职责与验证说明](04-scripts/README.md)
