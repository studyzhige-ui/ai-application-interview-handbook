# Market｜AI Application / Agent 招聘市场证据层

[↑ Handbook 总目录](../README.md) · [Canonical Questions](../interview/canonical/README.md) · [Knowledge Map](../guide/knowledge-map.md)

> Market 回答两个问题：**公司正在招什么？真实面试正在问什么？**

## 1. 两种核心原始证据

### Jobs / JD

[当前校招 / 应届｜AI Application & Agent 官方非算法岗位库](jobs/ai-agent-jd-market.md)

岗位库主口径为 **当前有效校园招聘 / 应届可投 + 第一手官方来源 + 非算法工程岗**。毕业年份、招聘批次与项目名作为元数据保留，不作为唯一入库 Gate。用于观察：

- 岗位名称与 Role Scope；
- 技术栈与工程职责；
- Agent / RAG / Backend / Full-stack 的边界；
- 市场需求随时间的变化。

维护规则：**正式 JD 只允许第一手官方来源。** 只收公司自有招聘官网或从公司官方 Careers 直接跳转、可确认归属的官方 ATS 职位详情页；牛客、Boss 直聘、猎聘、智联、实习僧、高校就业网、聚合站、镜像、媒体/社交帖子与搜索摘要均不能进入正式 JD。二手来源最多用于发现线索，必须追到官方原始职位页后才可入库。

岗位库使用固定 **69 家长期公司扫描池**，覆盖互联网大厂、头部 AI 公司，以及智能硬件/汽车、企业软件、金融科技等与 AI Application / Agent 工程高度相关的知名中大厂。每家公司都必须维护可重复进入的第一方 `search_url`；**公司进入扫描池不要求当前已经有目标岗位**。只有完整搜索 / 分页后才能得到有效的 `ZERO_TARGET_JDS`，页面可达、接口存在或搜索引擎 0 命中都不算完成。

当前升级基线为 **69/69 第一方招聘入口已登记**；原 41 家已核验岗位事实全部保留，新增 28 家进入 `NEEDS_ENUMERATION` 并由自动同步逐公司闭环。公司状态与岗位状态分离为 `HAS_TARGET_JDS / ZERO_TARGET_JDS / NEEDS_ENUMERATION`。详见 [69 家公司扫描池](jobs/company-scan-pool.md) 与 [覆盖审计](jobs/official-2027-coverage-audit.generated.md)。

### HUMAN-A Interviews

[真人面经目录](interviews/)

正式 HUMAN-A 必须满足：

```text
候选人本人第一人称
+ 真人面试官 / 真实招聘流程
+ 高信息密度
+ 目标 AI Application / Agent Role Scope
+ 正文稳定可核验
+ 非转载 / 非答案帖 / 非重复
```

**HUMAN-A 正式库：S001–S295 / 33 Batch。** 候选来源先进入 Market 证据层并完成质量与去重检查；单日热点不直接改变 Curriculum。

## 2. Market 内部结构

```text
market/
├── jobs/         # 第一手官方岗位 JD + 公司覆盖矩阵
├── interviews/   # HUMAN-A 独立招聘流程
├── analysis/     # 频率、覆盖、追问链、Gap 等分析
├── monitoring/   # Inbox / Daily Log
└── policies/     # Source Quality / Role Scope 规则
```

## 3. 去重与质量原则

- JD：**来源 Gate 先于去重。** 非第一手官方来源直接排除；通过官方来源 Gate 后，同公司 + 同岗位主体 + 高度相同职责按一个 Role Family 去重，城市/批次变体不重复计数。
- 面经：同候选人 + 同公司 + 同招聘流程的多轮合并为一个 Source。
- 搜索“0 命中”不能证明未收录；正式入库前必须回读历史做去重。
- 不为数量降低 Gate。

详细规则：

- [Source Quality Policy](policies/source-quality-policy.md)
- [Role Scope Policy](policies/role-scope-policy.md)
- [Market Analysis](analysis/README.md)

## 4. 与其他层的关系

```text
Market JD      → 公司声称需要什么
Market HUMAN-A → 面试实际验证什么
      ↓
Interview Canonical → 归一化成稳定能力
      ↓
Curriculum → 调整复习深度，不破坏知识依赖

References → 校准技术事实，但不创造市场频率
```
