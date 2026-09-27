# 外围文档同步｜2026-09-28

[← 质量入口](final-quality-audit.md) · [学习资源索引](../navigation-index.md) · [机器验证记录](peripheral-sync-2026-09-28.json)

## 基线与范围

核对基线为 `main@a1a86db75f4d9714b95dca25ce9b1b0563bdd72e`。以 10 个课程模块、4 个产品模块、Coding 的实际正文及 README 为依据，核对标题、阅读顺序、配套和跨层职责；对全仓 Markdown 执行本地路径、锚点与冲突检查。外围内容作语义审查，正文只读，不声称重新完成 200 篇正文的逐段教学审查或上游源码核验。

课程为 175 篇，产品专题为 16 篇，Coding 为 9 篇。两条独立轨道不加入 Curriculum 计数。模块当前范围由[机器目录](../navigation-index.json)生成，历史面经统计保持独立。

## 发现与修订

| 问题 | 修订 |
|---|---|
| 原同步器只扫描 65 份 README / 共享导航，漏过外围正文 | 扩为全仓 Markdown 只读扫描；写入仍受独立允许清单约束 |
| 当前质量总览仍写“七层”，并混用旧日期、当前数量与全量 PASS | 补齐 Products，分开范围、导航、内容审查、源码与运行验证；旧总览按原有结论归档 |
| Foundation、集成与 Canonical 入口继承旧学习顺序及绿色状态 | 以语言、接口、MySQL、Redis、Backend 的前置关系说明路线；专项证据不转成永久通过状态 |
| Canonical Progress 同时维护动态课程状态和冻结证据 | 缩回冻结基线与覆盖；课程数量与阅读入口归学习索引；Ownership、QID 与频次不变 |
| 历史审计移动后出现 6 处断链 | 只修复相对路径，保留当时数字与结论 |
| 15 处引用指向缺失的 Agent 资料锚点 | 在 References 恢复兼容锚点和适用边界，不改课程正文 |
| 产品公共标题被误当成所有产品的统一阅读顺序 | 按 README 完整目录表提取顺序；Codex 保持上下文 → 工具 → 记忆 → 工程 |
| 正文改动后，单纯数量检查无法发现外围漂移 | 目录保存正文标题、阅读顺序与 SHA-256 指纹；内容变化会要求重新同步 |
| Git 教学中的冲突标记被误报 | 只豁免明确标记的教学片段；普通代码围栏不能隐藏真实冲突 |
| 写作规范、Tools 说明与分析生成源继续输出旧口径 | 同步必要入口原则、扫描范围、实际计数和课程状态归属；不手改生成结果掩盖源头 |

已一致的模块正文、Review、Interview 和资料内容保留，不为制造修改量重写。System Design 没有本轮独立专项复验记录，质量入口明确说明，不继承旧版 PASS。

## 实际验证

本地使用 Python 3.13.5。24 项外围回归、6 项学习顺序回归通过；全仓 Markdown 路径、锚点与冲突检查无错误；同步器重复运行无漂移。另执行 Python 工具编译、5 个 Node 采集脚本语法检查、官方岗位来源契约检查、Agent 结构与保留映射检查、仓库语义检查、Canonical 审计、Gap 候选生成、市场分析生成及来源覆盖检查。

官方岗位检查只验证已存契约，不代表重新联网穷举岗位。结构、示例、阅读与真实服务验证不是同一层结论。本次未重跑数据库、模型、外部服务、多节点或生产压测，也未穷尽核验外部网址或进行真实用户阅读实验。

200 篇学习正文以及 81 份市场与冻结证据文件逐字节保持基线内容。Canonical 仅修改三个入口/状态页的非统计导航说明；市场分析仅随生成源更新 README 的课程状态指向，其余生成数据不变。原始 Batch、来源归属、Canonical 问答、频次和覆盖审计不被外围同步改写。

## 分支清理依据

请求到达时有 main 和 21 个其他分支。删除依据是确切分支头已属于 main 历史，或匹配已合并 PR 的确切 head，且合并提交可从 main 到达。不能仅凭分支名、同题 PR 或“看起来是旧稿”删除。

Claude Code 的旧 PR #21 已关闭未合并，后继 PR #22 已合并。发布检查逐 blob 核对两个 head 的五份产品文件与修订记录，并检查共享项目索引保留该修订入口；只有这些条件成立，才允许发布并删除旧分支。临时维护分支只承载本次发布与清理，临时工作流不进入 main 的最终树。

| 分支 | 请求时 head | 合并或替代依据 |
|---|---|---|
| `backend-reader-revision-20260927` | `0c5734b13cff27cb280fafbafd7ab262928de20a` | PR #28 的确切 head 已合并 |
| `codex-reader-source-refresh-2026-09-27` | `8f25706910f96ff016e5b01ccd77e223b9bde96e` | PR #24 的确切 head 已合并 |
| `curriculum/backend-clarity-refinement-20260928` | `04599476a438cc436ec896948d2d99e85b4816a4` | PR #38 的确切 head 已合并 |
| `curriculum/rag-clarity-refinement-20260927` | `b18b2dd8a0fd3d2b381ecb035ce3dd335813a358` | PR #36 的确切 head 已合并 |
| `curriculum/rag-reader-first-20260927` | `0ec44f676e62f2e620e155b7a6568ac765a03799` | PR #27 的确切 head 已合并 |
| `docs/backend-reader-first-20260927` | `157bc4bfaa34efdf611b8fa2f858d9123ad22c13` | 属于 main 历史 |
| `docs/claude-code-reader-first-20260927-r2` | `dedffc9e9ef9ebd8ed26eb9657d9b09471e29161` | PR #22 的确切 head 已合并 |
| `docs/claude-code-reader-first-20260927` | `cbea9e31333a63fd7ba04016cb591dfddfd64855` | PR #21 旧稿；由 PR #22 保留内容后替代 |
| `docs/codex-clarity-refinement-20260927` | `d568b7ff5a07dc234c1a8b19fb1f9fc438e8c7f2` | PR #37 的确切 head 已合并 |
| `docs/deepseek-harness-clarity-20260927` | `029f994fd2792a3e3a91ec98c9c0c57850bd0dc2` | PR #33 的确切 head 已合并 |
| `docs/deepseek-harness-reader-first-20260927` | `cd642c24ac6c0406b084a018c48098af36fbd882` | PR #26 的确切 head 已合并 |
| `docs/deerflow-clarity-refinement-20260927` | `89b916dc65c30b663e44890f487717f33ce4d4a8` | PR #35 的确切 head 已合并 |
| `docs/deerflow-reader-first-20260927` | `76475d729fad62150a38ac759d680b2c4e004d76` | PR #25 的确切 head 已合并 |
| `docs/deerflow-reader-first-v2-20260927` | `4c9019f5d51c21969b7c9961c6f798585a51c418` | 属于 main 历史 |
| `docs/llm-clarity-refinement-20260927` | `0aade3e7de74bf3c11ae32fb1640139c8063c659` | PR #30 的确切 head 已合并 |
| `docs/llm-foundation-reader-first-2026-09-27` | `b6ee0c1fe86dab2b5fcc8b8832df21ff4d218b22` | PR #19 的确切 head 已合并 |
| `docs/outer-navigation-sync-20260927` | `5bf374ee1422269eec95739442d1ddb0a40d9344` | PR #32 的确切 head 已合并 |
| `docs/vector-db-clarity-refinement-20260927` | `b50c5df83c9fdce88193ec24ccb30ec6616a775b` | PR #31 的确切 head 已合并 |
| `docs/vector-db-reader-first-20260927` | `f1f03060bd61aaa26f7843bb3f1473e05a24c99b` | PR #20 的确切 head 已合并 |
| `fix/redis-cross-links-20260927` | `5fe2e98a64c1fb8e014d780bd52dd3fc4b3d558a` | PR #23 的确切 head 已合并 |
| `products/claude-code-clarity-20260927` | `4a276b2c13b1e771676fc4f94ffa40400bb03f53` | PR #34 的确切 head 已合并 |

发布后的真实提交、CI 结果与清理后的分支集合，以对应 PR 和 Actions 运行结果核验；本页不把检查计划写成已执行的远端结果。
