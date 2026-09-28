# System Design｜读者优先修订与分层验证记录

[← 审计入口](README.md) · [模块入口](../../curriculum/10-system-design/README.md)

> **记录分层：** 第 1—8 节保留仅文件稿交付时的审查快照；第 9 节记录用户随后授权发布后的完整仓库集成。旧记录中的“未发布、未运行全仓检查”只描述原交付阶段，不覆盖后续验证。

## 1. 交付状态与基线

日期：2026-09-28。任务为系统优化；发布权限采用用户默认的**仅形成修改稿**。本记录随文件稿交付，不表示远端已有这些文件。未向目标仓库创建远端分支、Git 对象、commit 或 PR，未合并 main，未触发 CI。补丁工具测试仅在临时合成仓库生成测试提交，与目标仓库无关。

最初通过可用 GitHub 连接器读取的基线为 `a1a86db75f4d9714b95dca25ce9b1b0563bdd72e`。交付整合基线为 `a6b51b9f00bf3fe7910cfe4ca248e80545f566e3`。比较结果为一个后继提交：PR #39 修改 35 个外围文件；目标的 19 篇正文及四份 Review/Interview 配套未变，目标 README 只有两处完成状态措辞改变。稿件保留其“按记录范围判断、读完不等于验收”的决定，不恢复旧版绿色声明。

实际输出限定为目标模块、这一份独占审计，以及五个共享文件中的本模块局部同步规则：`guide/learning-order.json`、`guide/navigation-index.json`、`guide/navigation-index.md`、`guide/audits/README.md`、`guide/audits/content-depth-audit.md`。不改其他模块正文、市场记录、准入规则、冻结统计、主题责任或历史快照。不创建旧 research 目录。

19 个正文路径和章内阅读顺序均保留。标题更易读，保留旧一级标题锚点作为兼容入口；其他历史小节锚点是否在全仓仍被引用，需要完整仓库扫描，不能由这一项兼容措施推定全部无断链。

## 2. 实际阅读范围

| 层次 | 实际读取 | 没有据此宣称的范围 |
|---|---|---|
| 目标原稿 | 19 篇正文连续全文；README、Review、三份 Interview 全文；真实树中无原有实验、测试或模块资料文件 | 不以旧 PASS 或文件时间代替本轮审查 |
| 目标修改稿 | 19 篇主线连续独立复读，随后单独复读小结、面试回答与自测；Review、三份 Interview 和实验统一核对 | 作者审查不是目标初学者真实阅读验收 |
| 规范与导航 | 根入口、课程入口、学习路线、知识地图、文档规范；目标树与验证工作流；导航生成器相关代码及 PR #39 变更 | 未在本地取得完整仓库，未运行全仓生成/语义测试 |
| 已认可的 Coding 参照 | `practice/coding/README.md`；01 章 1—180 行样读；09 AI Coding 全文 | 不宣称逐段重审全部 Coding 教材或独立复核用户认可过程 |
| 必要关联 | Backend 入口与 09 幂等章；RAG 入口、12 治理章 1—175 行；Agent 入口、23 生产章 1—180 行、13 恢复章 1—160 行；14 权限章 1—28 行用于核对链接与职责 | RAG、Agent 的其余正文不在本轮完整验收范围 |
| 面经 | System Design 全部 24 个 Canonical 条目；下节列出的 21 个正式流程上下文；两份准入政策；批次目录及最新 batch-35 | 未回读冻结覆盖所含全部 71 个原始流程；外部原帖复核为 0 |

正式批次检索没有以旧 `S279` 为上限。GitHub 索引检索使用过 `system-design`、`System Design`（限定市场目录的 API 查询）、`10-system-design/docs/`、`State Ownership` 等；受 topn 和响应截断约束，检索结果只用于定位。这里的“全仓/正式库检索”指查询范围，不等于全库每份正文逐篇完整审读，也不保证关键词查询覆盖所有相关问题。

正式上下文回读：batch-23 中三个流程，以及 batch-27 至 batch-35 的正式流程。batch-27 分段补齐；batch-33 获取到两个正式流程和既有流程后续轮次，但末尾过程总结被截断，不称整个批次逐字读完。其余已读正式流程的证据范围以原文为界。旧批次中的 research 字样仅作历史记录。

## 3. 教学判断与具体改动

实际判断是保留 19 章的依赖顺序：需求、规模、状态与数据流、缓存和分区、正确性与排队、故障和安全、验证，再综合到不同系统。每章仍有独立问题，不为适配固定文件数而强行拆合。主要修订发生在解释深度和过程，不在目录扩容。

| 正文 | 处理 | 理由与落点 |
|---|---|---|
| [01](../../curriculum/10-system-design/docs/01-SystemDesign职责与答题框架.md) | 保留设计顺序，重写具体引入 | 从团队报告任务区分受理、结果、发送完成；逻辑职责不强制拆成微服务。 |
| [02](../../curriculum/10-system-design/docs/02-Requirement与SLO.md) | 补充 SLO 可检查口径 | 增加合格请求、统计窗口、成熟任务分母、错误预算；安全不变量与可容忍失败率分开。 |
| [03](../../curriculum/10-system-design/docs/03-Workload与CapacityEstimation.md) | 纠正计算并补全推导 | 输入和输出 Token 分别计算，不能连乘；区分 HTTP 请求、模型调用、在途量、吞吐、存储与费用。 |
| [04](../../curriculum/10-system-design/docs/04-API数据模型与StateOwnership.md) | 精修状态和接口语义 | 操作身份、参数绑定、条件版本、状态权威、游标和保留责任；不按 Session/Lease 名字判断能否丢失。 |
| [05](../../curriculum/10-system-design/docs/05-DataFlow与StateMachine.md) | 保留同步异步框架，加深时序 | 任务与派发双写窗口、重复交付、结果提交、取消和断线恢复使用同一报告对象。 |
| [06](../../curriculum/10-system-design/docs/06-Cache与HotPath.md) | 保留旧值回填竞态并加深 | 明确 TTL 起算点、失效代际、回源容量、权限与热点；版本字段本身不是防护协议。 |
| [07](../../curriculum/10-system-design/docs/07-PartitionRouting与Fanout.md) | 补充分区选择的推理 | 区分分区、副本和命名空间；给出局部精确 Top K 充分性的条件与反例；迁移包括旧写入者。 |
| [08](../../curriculum/10-system-design/docs/08-Consistency与Idempotency.md) | 保留幂等、事务、补偿；补清未知 | 稳定意图与执行代际分开；外部未找到可能与在途请求竞争；fencing 必须由实际资源执行。 |
| [09](../../curriculum/10-system-design/docs/09-QueueBackpressure与LongRunningTask.md) | 补充积压计算和接管时序 | 到达/处理净差、ACK 边界、死信去向、租户公平及租约过期后旧执行者仍运行。 |
| [10](../../curriculum/10-system-design/docs/10-Reliability与Overload.md) | 补充可靠性选择边界 | 总 deadline、重试预算和多层放大；故障隔离、降级安全底线、RTO/RPO 与恢复业务核验。 |
| [11](../../curriculum/10-system-design/docs/11-MultiTenancy与Security.md) | 精修可信范围和资源隔离 | 身份来源、对象与事件权限、撤权后恢复、批准参数、沙箱；不把候选 ID 内部计算等同内容泄露。 |
| [12](../../curriculum/10-system-design/docs/12-ObservabilityEvaluation与Evolution.md) | 补充归因、比较与演进 | 分母一致、并行关键路径、质量/延迟/费用联合选择，影子写入隔离，版本不能保证确定性。 |
| [13](../../curriculum/10-system-design/docs/13-HighConcurrencyTransactionalSystems.md) | 保留各类竞争场景，修正边界 | 库存守恒与迟到支付；固定窗口/令牌桶最小模型、守恒额度；Refresh Token 轮换未知；二维码两个终态。 |
| [14](../../curriculum/10-system-design/docs/14-RealtimeReadHeavySystems.md) | 加深实时读模型主问题 | 最近 20 条、用户范围、重复与乱序、连续水位、快照/增量交接；保留排行、Feed、联想、通知。 |
| [15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md) | 保留数据处理范围，补完整过程 | 保留与压缩单位、查询组织、keyset/快照/增量区别、并行检查点空洞、精确去重和上传清理。 |
| [16](../../curriculum/10-system-design/docs/16-LLMGateway与MultiTenantAIPlatform.md) | 加深网关的资源与费用责任 | 能力不等价、RPM/TPM/并发分别受限；预留、未知、幂等结算、实际超支；流中断不等于免费。 |
| [17](../../curriculum/10-system-design/docs/17-EnterpriseRAGSystemDesign.md) | 收束为部署与取舍综合章 | 不复制 RAG 内部教材；补双链路容量、当前权限、版本与代际、写成功/可见性、切换回滚条件。 |
| [18](../../curriculum/10-system-design/docs/18-ProductionAgentBackend.md) | 保留长任务结构，补恢复第一步 | Run 与 HTTP 解耦，恢复先查操作账本、权限、批准、剩余预算；沙箱、接管和外部防重分别负责。 |
| [19](../../curriculum/10-system-design/docs/19-VerticalAIAgentPatterns.md) | 保留业务差异，不堆新案例 | 分析定义/算术/因果分开，客服知识/实时事实/写操作分开，文档和内容看产物，游戏认权威状态。 |

正文使用虚构团队报告任务作为主要对象。价格、流量、延迟和业务数字都标明为教学条件，不伪装为实测生产收益。机制先用语言、状态表、输入和结果解释，完整初始化、重复测试集中在 `review/mechanism_lab.py`，测试导入这一实现，不维护平行代码副本。

Review 保留六张关系图，但把“状态名称决定是否临时”“重试—补偿必须串成固定流水线”等暗示改为条件关系。综合自测使用八组完整新条件；提示和答案分开折叠。Interview 保留原 36 个问题的范围，增加实时读模型、质量与时延两组表达训练，不给来源数或题目数授予教学质量。每章正文的 🎯 回答保持直接可见，回答中的关键机制均已在章内主线出现。

## 4. 面经的知识去向

### 4.1 Canonical 层：24 个条目的完整机制映射

下表序号仅表示本记录中的排列，不另造 Canonical ID。问题范围来自 [System Design Canonical](../../interview/canonical/system-design.md)，本轮不调整其冻结统计或主责归属。

| 条目 | 原问题范围 | 抽象机制与必要前置 | 主体位置 | 原解释与本轮处理 |
|---|---|---|---|---|
| 01 | 秒杀/库存 | 不变量、原子预占、支付与释放竞争；先修状态与幂等 | [04](../../curriculum/10-system-design/docs/04-API数据模型与StateOwnership.md)、[08](../../curriculum/10-system-design/docs/08-Consistency与Idempotency.md)、[13](../../curriculum/10-system-design/docs/13-HighConcurrencyTransactionalSystems.md) | 原有范围保留；补守恒、最后一件、迟到支付和回调防重。 |
| 02 | 排行榜 | 全局排序、热点、快照新鲜度；先修分区 | [07](../../curriculum/10-system-design/docs/07-PartitionRouting与Fanout.md)、[14](../../curriculum/10-system-design/docs/14-RealtimeReadHeavySystems.md) | 保留；补局部 Top K 充分条件和失效条件。 |
| 03 | Autocomplete | 前缀查询、请求频率、结果新旧；先修缓存 | [06](../../curriculum/10-system-design/docs/06-Cache与HotPath.md)、[14](../../curriculum/10-system-design/docs/14-RealtimeReadHeavySystems.md) | 保留；防抖与旧响应保护分开，不绝对禁止 SQL。 |
| 04 | Feed | 读写放大和热门作者；先修扇出与读模型 | [07](../../curriculum/10-system-design/docs/07-PartitionRouting与Fanout.md)、[14](../../curriculum/10-system-design/docs/14-RealtimeReadHeavySystems.md) | 保留混合策略，解释代价发生在哪条路径。 |
| 05 | 通知平台 | 交付阶段、未知结果、重试、防重；先修队列 | [08](../../curriculum/10-system-design/docs/08-Consistency与Idempotency.md)、[09](../../curriculum/10-system-design/docs/09-QueueBackpressure与LongRunningTask.md)、[14](../../curriculum/10-system-design/docs/14-RealtimeReadHeavySystems.md) | 补受理、送达、已读分别证明什么。 |
| 06 | 10 TB 数据存储/查询 | 单位、保留、压缩、访问模型；先修容量 | [03](../../curriculum/10-system-design/docs/03-Workload与CapacityEstimation.md)、[15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md) | 补 450 TB 主体计算与遗漏空间，存储形式按查询选。 |
| 07 | 大表迁移 | 稳定游标、快照、增量、检查点；先修版本和幂等 | [08](../../curriculum/10-system-design/docs/08-Consistency与Idempotency.md)、[15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md) | 保留 keyset；加乱序完成空洞、删除和在线负载保护。 |
| 08 | 海量 IP/ID 去重 | 精确成员、位图空间、概率过滤；先修数据规模 | [15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md) | 保留；说明布隆命中不能直接裁定重复，计算 IPv4 位图。 |
| 09 | 分布式限流 | 窗口、速率、突发、额度守恒；先修并发/队列 | [09](../../curriculum/10-system-design/docs/09-QueueBackpressure与LongRunningTask.md)、[13](../../curriculum/10-system-design/docs/13-HighConcurrencyTransactionalSystems.md) | 补固定/滚动窗口、令牌桶最小模型；修正分散额度必然超发的泛化。 |
| 10 | 共享 Token Refresh | 刷新所有权、轮换、未知结果；先修缓存/幂等 | [06](../../curriculum/10-system-design/docs/06-Cache与HotPath.md)、[08](../../curriculum/10-system-design/docs/08-Consistency与Idempotency.md)、[13](../../curriculum/10-system-design/docs/13-HighConcurrencyTransactionalSystems.md) | 加深多实例时序，不把锁或旧令牌重试写成万能恢复。 |
| 11 | 二维码登录 | 一次性身份、绑定、有效期、终态；先修状态机 | [05](../../curriculum/10-system-design/docs/05-DataFlow与StateMachine.md)、[13](../../curriculum/10-system-design/docs/13-HighConcurrencyTransactionalSystems.md) | 修正已交换与过期串联；补边界时刻与浏览器绑定。 |
| 12 | 大文件/视频 | 分块、流式、提交、失败清理；先修可靠任务 | [09](../../curriculum/10-system-design/docs/09-QueueBackpressure与LongRunningTask.md)、[15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md) | 补并发资源上限、续传身份与 ETag 边界。 |
| 13 | LLM 网关 | 能力兼容、配额、流交付、计费；先修模型与容量 | [03](../../curriculum/10-system-design/docs/03-Workload与CapacityEstimation.md)、[16](../../curriculum/10-system-design/docs/16-LLMGateway与MultiTenantAIPlatform.md) | 补未知费用、幂等结算、超支和部分输出。 |
| 14 | 多租户 AI 平台 | 可信范围、权限、资源公平；先修状态/安全 | [11](../../curriculum/10-system-design/docs/11-MultiTenancy与Security.md)、[16](../../curriculum/10-system-design/docs/16-LLMGateway与MultiTenantAIPlatform.md) | 加深跨步骤授权和多维配额，不限于 tenant_id 过滤。 |
| 15 | SGX/EPC 有限资源调度 | 有限工作集、并发、隔离；先修容量与过载 | [03](../../curriculum/10-system-design/docs/03-Workload与CapacityEstimation.md)、[11](../../curriculum/10-system-design/docs/11-MultiTenancy与Security.md) | 保留稀缺资源模型；不扩写未经运行核实的硬件细节。 |
| 16 | 企业 RAG | 后台/在线边界、来源/版本/安全状态；先修 RAG | [17](../../curriculum/10-system-design/docs/17-EnterpriseRAGSystemDesign.md) | 收束系统组合；内部检索原理回主讲模块。 |
| 17 | 600 GB/1 TB PDF RAG | 代表性抽样、阶段吞吐、增量与发布 | [15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md)、[17](../../curriculum/10-system-design/docs/17-EnterpriseRAGSystemDesign.md) | 补不能从 PDF 字节猜 Token、原始向量不等于完整索引。 |
| 18 | 财务分析 Agent | 指标定义、确定性计算、解释证据 | [19](../../curriculum/10-system-design/docs/19-VerticalAIAgentPatterns.md) | 加实际计算，贡献拆分不等于因果结论。 |
| 19 | 客服 Agent | 政策知识、实时事实、受控动作 | [11](../../curriculum/10-system-design/docs/11-MultiTenancy与Security.md)、[19](../../curriculum/10-system-design/docs/19-VerticalAIAgentPatterns.md) | 保留三类责任，补批准和未知结果。 |
| 20 | PDF/HTML 处理 | 来源结构、产物版本、安全输出 | [15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md)、[19](../../curriculum/10-system-design/docs/19-VerticalAIAgentPatterns.md) | 保留结构/布局/安全最小责任；解析细节归 RAG。 |
| 21 | Agent 后端 | Run、步骤、状态、交付和执行环境 | [18](../../curriculum/10-system-design/docs/18-ProductionAgentBackend.md) | 补跨连接/部署的完整恢复顺序。 |
| 22 | 长时间 Agent | 检查点与外部操作账本、接管和预算 | [08](../../curriculum/10-system-design/docs/08-Consistency与Idempotency.md)、[09](../../curriculum/10-system-design/docs/09-QueueBackpressure与LongRunningTask.md)、[18](../../curriculum/10-system-design/docs/18-ProductionAgentBackend.md) | 加深外部成功但本地未保存窗口，恢复先核对。 |
| 23 | 游戏 Agent | 世界权威状态、允许动作和验收 | [19](../../curriculum/10-system-design/docs/19-VerticalAIAgentPatterns.md) | 保留领域裁定，不把模型文本作为世界事实。 |
| 24 | 内容/视频 Agent | 分阶段产物、版本、资源与人工验收 | [15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md)、[19](../../curriculum/10-system-design/docs/19-VerticalAIAgentPatterns.md) | 保留；主线机制复用，不按垂类再造生产组件大全。 |

### 4.2 正式原始上下文层：21 个流程的处理

“保留”表示相应机制已有位置并仍成立，不意味着该来源所有算法、语言、前端或框架追问均由本模块教授。“交回”只给建议去向，没有改写对方正文，也没有把对方全部验收算为完成。

| 正式流程 | 回读的问题/连续条件 | 机制、前置与判断 | 处理及去向 |
|---|---|---|---|
| [S267](../../market/interviews/batch-23.md) | 布隆过滤、APT 与 MCP/访问边界 | 概率过滤不是安全门；性能要证据；数据访问需权威与权限 | 保留并加深 06/11/12；APT、前端、Function Calling 细节交回 Coding/Backend/Agent。 |
| [S268](../../market/interviews/batch-23.md) | 多实例 Access/Refresh Token、刷新延迟、锁超时、旧值、崩溃 | 缓存/执行权/轮换未知需一起推演 | 13 加深；前置 06/08；不能靠一把锁结束答案。 |
| [S269](../../market/interviews/batch-23.md) | Agent 交互、网络、状态、记忆与大文件处理 | 状态边界、安全与运行环境选择；基础机制不扩散 | 11/18/19 保留；Memory/HTTPS/OS 交回主讲模块。 |
| [S280](../../market/interviews/batch-27.md) | 故障诊断、工具门禁、Case Replay、停止条件、容灾 | 恢复、故障验证、有限预算；先修 Agent 循环 | 10/12/18 加深；Skill 发现与具体框架留 Agent。 |
| [S281](../../market/interviews/batch-27.md) | 多节点消息、知识增量、State/Framework、OS | 实时交付和知识新鲜度需要持久依据 | 14/17/18 保留；框架 API 和 OS 交回对应基础。 |
| [S282](../../market/interviews/batch-27.md) | AI 生成代码遗漏 Bad Case、回滚、补测试；数据库/JVM | 验证范围与受控发布，不以绿色测试作生产证明 | 12 加深；数据库/JVM 不越界重写。 |
| [S283](../../market/interviews/batch-27.md) | 长流程按预期执行、置信度确认、知识更新、框架取舍 | 确定性验收、授权确认与更新控制 | 12/17/18 保留与补边界；模型置信度不充当唯一批准。 |
| [S284](../../market/interviews/batch-27.md) | Elo、测试集代表性、压缩阈值、Redis/商品 URL 刷新 | 指标和参数需要适用场景；缓存新鲜度 | 06/12 加深；Elo/压缩实现留评测与 Agent 主责。 |
| [S285](../../market/interviews/batch-27.md) | 敏感数据导出、重启、10 万人抢 100 票、断电 | 授权、可恢复事实、库存守恒；先修 08/09 | 11/13/18 加深；Redis 持久细节交回 Redis。 |
| [S286](../../market/interviews/batch-27.md) | 财务 Agent 架构、RAG 评测、Skill 与真实落地 | 领域验收、架构收益、证据来源 | 12/19 保留；Skill/Coding 细节不新增章节。 |
| [S287](../../market/interviews/batch-28.md) | 文档并发幂等、防覆盖、RocketMQ vs 定时、Harness 迁移 | 幂等与版本不同；事件加核对扫尾；迁移有成本 | 04/08/15/17/18 加深；框架与算法追问交回 Agent/Coding。 |
| [S288](../../market/interviews/batch-29.md) | 写链路副作用、业务校验、批准、长任务、二面 Runtime/Plugin 化 | 能力格式不等于业务合法；恢复与授权需确定性依据 | 11/12/18/19 加深；同流程二面只增加深度，不增加独立来源。 |
| [S289](../../market/interviews/batch-30.md) | 线上支付失败链路、Network、RAG 低召回、异构 PDF | 端到端归因与副作用核对；检索需阶段证据 | 08/12/17 保留与加深；原帖 MPC 保留原文，不擅自修证据。 |
| [S290](../../market/interviews/batch-31.md) | 为何 Multi-Agent 而非简单方案、真实反馈、准确率 | 架构选择需对照与收益验证 | 12/19 加深；不因一场面经另建多 Agent 场景章。 |
| [S291](../../market/interviews/batch-31.md) | RAG 文档规模、Agent/Tool/MCP、Linux、Quick Sort | 容量对象明确；基础算法/工具不是本模块新主线 | 03/17 保留；其余交回 Agent/Coding/基础。 |
| [S292](../../market/interviews/batch-32.md) | 只有 MySQL 表，10 万 QPS 商品详情与价格修改可见 | 读模型、缓存回填竞态、新鲜度、回源保护 | 06 加深，03/07 前置；不把加节点视为完整解决。 |
| [S293](../../market/interviews/batch-32.md) | 视频 OOM、并行/串行、分块续传、清理、SQL 改善但接口慢 | 受限流式处理、连续检查点和关键路径归因 | 07/12/15 加深；Skill 遵从性归 Agent。 |
| [S294](../../market/interviews/batch-33.md) | AI Q&A 的前后端、体验、安全；防抖和限流 | 交互路径与后端事实分开，迟到响应不能覆盖新意图 | 11/14/16/17 承接；CSS/CORS/语言不越界扩写。 |
| [S295](../../market/interviews/batch-33.md) | 动态知识事件/定时、质量采纳、阶段门禁、多等一分钟 | 阶段质量与最终任务目标、延迟/成本联合取舍 | 12/17/19 补例；20—30pp 是面试条件，不当实测结果。 |
| [S296](../../market/interviews/batch-34.md) | Skill/MCP 膨胀、发现、无框架记忆压缩、Coding Agent | 执行职责、资源与范围；大部分机制主责在 Agent | 18 保留最小桥梁；其余交回 Agent，不重复教材。 |
| [S297](../../market/interviews/batch-35.md) | MQ 驱动最近 20 条、用户隔离、重复、断线恢复、指标 | 有序读模型、去重范围、连续水位和快照交接 | 14 完整补例，12/15 支撑；统一实验演示，不复述成题库。 |

这 21 个流程是本轮实际回读集合，不是“系统设计全部相关流程”或重新计算的市场覆盖量。尤其不能用新增轮次、关键词命中或问题条数充当独立来源数。外部原帖（牛客等）本轮没有重新打开核验，因此不授予新的来源准入结论。

## 5. 技术依据、适用版本与示例性质

官方资料按具体问题收录在 [模块资料索引](../../curriculum/10-system-design/references.md)，结论在相关正文附近给出处。实际打开核对的资料包括 Google SRE 的 SLO、容量设计、监控、过载、级联故障和灰度发布；RFC 9110、RFC 9700；AWS Outbox、幂等与 S3 Multipart；RabbitMQ Confirms；Azure Cache-Aside；OWASP 授权；Redis Bloom；WHATWG SSE；OpenAI Chat Completions 的流式 usage 说明。

| 对象 | 课程采用的依据/目标 | 实际运行或核验 |
|---|---|---|
| HTTP | RFC 9110，202 与幂等方法语义 | 官方网页核对；没有启动 HTTP 服务 |
| OAuth | RFC 9700，刷新令牌轮换与重放防护边界 | 官方网页核对；没有接入供应商或验证账号 |
| 消息确认 | RabbitMQ 文档页面标示 4.3；这里只引用确认与重投责任 | 没有安装或运行 RabbitMQ，不把文档版本当实机版本 |
| SSE | WHATWG Living Standard | 核对 Last-Event-ID；重放历史仍是应用责任；未跑真实 SSE |
| S3 | 托管服务 Multipart 文档，无本地二进制版本 | 核对完成/清理与 ETag 限制；未调用真实 S3 |
| 模型 API | OpenAI Chat Completions 官方参考 | 核对 include_usage 与中断可能缺最终用量；未调用模型、无实付费用 |
| 机制实验 | Python 3.13 标准库；不是课程的通用语言限制 | CPython 3.13.5 实际执行；未静默替换成仓库 CI 的 Python 3.12 |
| 数字与状态 | 虚构工作负载、价格、状态对象；顺序确定性模型 | 单元测试与手算模型可复核；没有真实持久化、多连接或网络 |

本模块不声称部署了 MySQL、Redis、向量库、OAuth、消息系统或模型服务。它们的生产默认值、弃用和部署行为应按具体使用版本再次验证。官方网页核对日期为 2026-09-28，不把页面最新状态当作本地安装版本。不存在为了所谓“最新能力”自动扩写课程的处理。

## 6. 主体独立检查与迁移检查

先隐藏本章小结、🎯、自测答案及复习材料，沿 19 篇主线读取。检查对象为具体引入、概念前提、状态变化、计算单位、失败原因及跨章依赖；随后单独检查章末回答没有首次引入必答机制。以下是检查时使用的新条件及可推导结论，不以“出现过术语”作通过依据。

| 主责 | 新条件 | 主线可推导的判断 |
|---|---|---|
| [01](../../curriculum/10-system-design/docs/01-SystemDesign职责与答题框架.md) | HTTP 已响应但邮件未查到 | 受理、产物完成和外部发送分开验收。 |
| [02](../../curriculum/10-system-design/docs/02-Requirement与SLO.md) | 任务尚未到完成期限 | 不应把未成熟任务直接混入完成率分母；需独立统计等待。 |
| [03](../../curriculum/10-system-design/docs/03-Workload与CapacityEstimation.md) | 每项任务改成两次模型调用 | 先展开调用率；输入输出与在途、费用分别重算。 |
| [04](../../curriculum/10-system-design/docs/04-API数据模型与StateOwnership.md) | 版本 7 的执行者面对取消后的版本 8 | 旧条件提交失败；不能只把版本号改为 8 重试。 |
| [05](../../curriculum/10-system-design/docs/05-DataFlow与StateMachine.md) | 报告已保存，客户端仍显示运行中 | 查询事实并恢复交付，不重做生成。 |
| [06](../../curriculum/10-system-design/docs/06-Cache与HotPath.md) | 命中率 90% 降为 50% | 相同流量下回源放大五倍，按剩余容量保护源。 |
| [07](../../curriculum/10-system-design/docs/07-PartitionRouting与Fanout.md) | Top K 后才做权限过滤 | 旧充分性条件不成立，需前置过滤或补取。 |
| [08](../../curriculum/10-system-design/docs/08-Consistency与Idempotency.md) | 新执行者查询旧请求未找到，但请求仍可能在途 | 保留未知；无可靠防重协议时不自动重做。 |
| [09](../../curriculum/10-system-design/docs/09-QueueBackpressure与LongRunningTask.md) | 突发结束后到达恰好等于理想容量 | 无净消化余量，不能宣布积压恢复。 |
| [10](../../curriculum/10-system-design/docs/10-Reliability与Overload.md) | 剩余 0.4 秒，下一次有用调用至少 0.5 秒 | 即使还有重试次数也不启动完整尝试。 |
| [11](../../curriculum/10-system-design/docs/11-MultiTenancy与Security.md) | 暂停期间撤权，恢复时缓存仍命中 | 重新核对当前资格，不以旧缓存放行。 |
| [12](../../curriculum/10-system-design/docs/12-ObservabilityEvaluation与Evolution.md) | 优化了非关键并行分支 | 最长分支未变时端到端不一定改善。 |
| [13](../../curriculum/10-system-design/docs/13-HighConcurrencyTransactionalSystems.md) | QR 在 expires_at 同时交换，规则为严格小于 | 拒绝交换；成功消费后的清理不能重写成功历史。 |
| [14](../../curriculum/10-system-design/docs/14-RealtimeReadHeavySystems.md) | 快照 104 到订阅期间产生 105/106 | 从快照游标补齐或可靠缓冲交接，不能只接新消息。 |
| [15](../../curriculum/10-system-design/docs/15-LargeScaleDataProcessingSystems.md) | 后一批完成，前一批失败 | 保存独立完成记录，但不越过连续检查点空洞。 |
| [16](../../curriculum/10-system-design/docs/16-LLMGateway与MultiTenantAIPlatform.md) | 预留 30，实际 22，结算重复 | 先解除未知，再幂等结算；余额 78，不再次扣减。 |
| [17](../../curriculum/10-system-design/docs/17-EnterpriseRAGSystemDesign.md) | 旧代际可用但漏了新内容且含旧 ACL | 同时检查内容追平与当前授权；不能直接切回。 |
| [18](../../curriculum/10-system-design/docs/18-ProductionAgentBackend.md) | 批准 r7 给 A，计划换成 r8 给 B | 原批准不覆盖新参数；预算与操作账本也不重置。 |
| [19](../../curriculum/10-system-design/docs/19-VerticalAIAgentPatterns.md) | 上期收入为零 | 普通环比公式无定义，报告绝对变化并澄清业务口径。 |

正文的多数机制仍需部署版本和真实故障实验才能证明工程实现有效；这里检查的是给定条件下的教学推理是否闭合，不是宣称真实读者已经全部学会。

## 7. 实际验证结果与未验证项

实际结果随交付包 `verification/` 保存：`unit-tests.txt`、`demo-output.json`、`content-checks.json`、`browser-checks.json` 与截图。包内清单记录最终文件摘要，修改后应重新执行，而不是复用本记录的旧结果。

已经执行 Python 语法检查、42 项共享实现的机制单元测试，以及命令行示例；第二次独立启动的示例输出与第一次相同。补丁工具另有 12 项测试，其中完整补丁检查发生在临时合成 Git 仓库，不是实际 Handbook 的整合测试。测试覆盖容量/费用、积压、乱序窗口、库存守恒、租约代际、预算、QR 终态、外部未知。随机序列测试是确定种子的顺序模拟，不是多连接并发测试。代码状态均在内存里；重新启动即重置。

实际检查 26 份 Markdown、326 个包内链接，未发现缺失目标、锚点、目录顺序、折叠或表格结构错误。模块的链接、锚点、目录映射、折叠和 Markdown 结构检查以 `content-checks.json` 的实际文件清单为准。跨模块目标区分“本地内容已验证”和“通过 GitHub 读取确认存在”；没有取得其他文件全字节时，不冒充全仓锚点扫描。

本地阅读预览采用 Markdown 渲染与 Chromium 144.0.7559.96；26 个内容页面在 1440×1000 与 390×844 两种视口共做 52 组检查，正文没有页面级横向溢出，宽表在容器内滚动。已检查折叠开合和 DOM 锚点，生成六张样图，并人工查看其中四张（容量章桌面/窄屏、复习图桌面、网关章窄屏）。浏览器策略阻止 file:// 与本地 HTTP 页面导航，改用 set_content 加载同一生成 HTML；这不是跨页点击测试。实际文档导航未执行，不计通过。视口、页面和结果见 `browser-checks.json`。六张 Mermaid 图保留在原稿，预览为同一图语义的 Graphviz 布局。没有运行 GitHub 自身 Mermaid 渲染器，也没有在真实手机、GitHub App 或远端 GitHub 页面做验收。

**未执行：** 仓库完整导航生成器与全仓回归；真实数据库事务/持久化、真实多连接竞争、消息交付、OAuth 刷新、模型费用、跨系统集成、负载/故障转移/生产验证。无部署版本与服务凭证时不把模拟换成真实通过。CI 未触发。

## 8. 共享同步与交付边界

同一正文路径和数量不代表无需更新导航：PR #39 的生成器已把正文标题和 SHA-256 放入机器目录。交付包因此包含五个共享文件的本模块局部变化，以及只读补丁生成工具；它检查目标正文的基线 Git blob，拒绝覆盖已改变的模块稿，并在用户仓库副本上读取共享文件的当前内容，仅合并本模块的指纹、标题、记录入口。

工具只向单独输出目录写补丁与候选文件，不修改目标工作区、不提交、不推送。目标模块已有不同后继修改、共享结构不匹配或受影响文件存在未提交修改时，应停止并报告具体冲突。它不以一整份旧 Git 树挂到新父提交，也不自动替用户裁决知识语义冲突。

本环境没有取得完整仓库字节，因此这里交付的是**已写成并验证的课程文件稿，以及可审查的局部共享同步规则**，不是“全仓整合已验证”。发布前仍应在最新 main 的独立工作区应用稿件，运行仓库生成器，审查实际生成差异与受保护内容，再执行全仓验证。该阶段不因稿件测试通过而被自动算作完成。


## 9. 发布授权后的完整仓库集成

用户随后明确授权创建 commit、PR 并合并 main。本节记录发布前的实际集成验证，最终合并事实以对应 PR 为准；不回写第 1—8 节的历史检查结果。

集成基线：`a6b51b9f00bf3fe7910cfe4ca248e80545f566e3`。原稿写入候选提交：`9cf188b889da02ed0939d4e12a730e3a78e92c8d`。原始 29 份文件的路径与 Git blob 聚合 SHA-256 为 `592d7d603afb582e4e913b88360f37da7adb227a07f451d970c8835ac30b2425`，与已交付文件稿逐项一致。

在完整仓库的独立 GitHub Actions 工作区执行，运行环境为 Python 3.13.5、git version 2.55.0，Node 版本 `v22.23.2`。实际日志及文件指纹见[本次集成运行](https://github.com/studyzhige-ui/ai-application-interview-handbook/actions/runs/36363944573)的验证产物。

完成：模块机制测试、两次冷启动示例一致性、Python 与五个 JavaScript 工具语法检查、外围导航回归、学习顺序回归、岗位契约、仓库可读性与语义检查、Canonical 和市场分析生成复现、正式来源覆盖及 Git 差异检查。生成器从真实文件计算课程总数 175；检查 428 份 Markdown、4421 个本地链接，无缺失目标、未解析锚点或冲突标记，生成漂移为零。详细命令和各自退出结果保存在运行产物中。

共享变更仅限本模块审核入口、章节标题及指纹对应的五个文件；不改变课程章节数、阅读顺序、其他模块正文、冻结证据、来源规则或历史快照。28 份教学与实验文件保持原稿字节不变，本审计仅增加明确的后续集成记录。临时发布工作流在最终 PR 差异中移除，不进入 main。

本阶段未重新进行浏览器显示验收，沿用原稿显示检查的限定范围；未运行真实数据库、消息代理、模型供应商、OAuth、S3、多连接并发、负载或生产实验。完整仓库验证不把顺序内存模型升级为真实服务保证。PR 的常规 CI 在最终文件状态上单独执行。
