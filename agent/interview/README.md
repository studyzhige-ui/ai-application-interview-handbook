# Agent 面试训练｜整体设计与细粒度追问

[← Agent](../README.md) · [综合复习](../review/README.md) · [可选学习路线](../../roadmap/learning-path.md) · [真人来源](../../research/questions/agent-harness.md)

> 沿任务→四层→治理的同一主线训练，不另建一套教材。先闭卷口述再展开答案；所有节奏自行安排。

## 使用方式与证据边界

保留main固定版本 `0266cbfa131f` 中56个细粒度训练问题的能力范围，按新16章重排，并加入8个系统推导题。共64道练习不等于64道真人Canonical。题目原型来自旧教材，新增示例、追问链与评分点是教学设计，不冒充真人原话；真实问法、频次和已核验追问只在研究层维护。

练习分三步：先用约30秒说明核心区别，再沿具体追问解释机制与失败，最后对照“掌握标准”检查证据。不是背完整答案；不懂的机制只回对应正文。

## 按16章展开的64道训练题

### 01｜Agent 系统与任务契约

<a id="q-01"></a>

<!-- legacy-question: 2 -->

<details>
<summary>Q01｜什么是 Agent Harness / Runtime？为什么 Model 外面还要这一层？</summary>

**参考开场：** Harness / Runtime把模型候选变成受控执行，负责循环、上下文、状态、工具、安全门、恢复与观测。它以L2运行职责为核心，工程上可包含L3适配，但不等于承接与交付任务的整个Agent应用；具体组件按任务需要选择。

**具体追问：** 模型之外谁真正发起动作？→谁决定授权和停止？→应用层交付与Harness执行有什么差别？

**掌握标准：** 把四层职责说清；Harness以L2为核心，可包含L3适配，不等于整个产品。不要把长期记忆、多Agent、数据库列成所有任务的必选项。

回到[第01章：Agent 系统与任务契约](../docs/01-AgentSystemAndTaskContract.md)。

</details>

<a id="q-02"></a>

<!-- teaching-question: new -->

<details>
<summary>Q02｜怎样把“读这些文件并整理报告”变成可实现的任务契约？</summary>

**参考开场：** 先澄清授权清单、只读/写入范围、输出形式、验收证据、冲突与缺失处理、时间/成本约束，再决定是否需要动态Loop。

**具体追问：** 输入清单变更如何版本化？→证据缺失可否部分交付？→如何证明原件未修改？

**掌握标准：** 能填写一份契约而不是重复字段名；清楚区分设计输入、软件职责和验证证据。

回到[第01章：Agent 系统与任务契约](../docs/01-AgentSystemAndTaskContract.md)。

</details>

### 02｜能力设计与自主权分配

<a id="q-03"></a>

<!-- legacy-question: 1 -->

<details>
<summary>Q03｜Agent 和普通 LLM Application / Workflow 有什么区别？</summary>

**参考开场：** Workflow 路径主要由程序预定义；Agent 根据中间 Observation 动态决定下一步。是否需要 Agent 取决于路径不确定性与自主决策价值，不取决于步骤数量。

**具体追问：** 固定抽取为什么不一定需要Agent？→哪一步确实需要观察反馈？→怎样验证新增自主性的收益？

**掌握标准：** 先判断控制权和不确定性，不以步骤数量或是否调用工具划分；比较相同任务下的质量、时延、成本及失败处理，保留更简单的基线。

回到[第02章：能力设计与自主权分配](../docs/02-CapabilityAndAutonomy.md)。

</details>

<a id="q-04"></a>

<!-- teaching-question: new -->

<details>
<summary>Q04｜自主权应按整个Agent设置，还是按动作和阶段分配？</summary>

**参考开场：** 按具体动作与阶段分配建议、查询、修改和提交权限；模型提出候选，可信程序与资源兑现授权并验证。

**具体追问：** 只读阶段需要联网吗？→提交前谁确认？→拒绝授权后能否换工具绕过？

**掌握标准：** 画出能力—控制权—执行权—验收权表；明确权限拒绝不能通过路由或重试绕过。

回到[第02章：能力设计与自主权分配](../docs/02-CapabilityAndAutonomy.md)。

</details>

<a id="q-05"></a>

<!-- teaching-question: new -->

<details>
<summary>Q05｜哪些Agent可以不需要Memory、向量库、多Agent和代码沙箱？</summary>

**参考开场：** 没有跨任务复用就不必建长期Memory；固定小输入不必向量化；无独立子任务不必多Agent；无任意代码执行不必配代码环境。

**具体追问：** 不装这些是否仍可动态行动？→什么失败证据会促使升级？

**掌握标准：** 组件由任务推导，保留简单基线，升级必须有质量/成本/风险的验证依据。

回到[第02章：能力设计与自主权分配](../docs/02-CapabilityAndAutonomy.md)。

</details>

### 03｜L1 应用层：任务、流程与用户交互

<a id="q-06"></a>

<!-- legacy-question: 44 -->

<details>
<summary>Q06｜Intent Routing 怎么实现？</summary>

**参考开场：** Rule/metadata/small classifier/embedding/LLM/agentic discovery，从简单可靠开始；低置信澄清，做 route eval。

**具体追问：** Rule、分类器、LLM如何比较？→未知意图怎么办？→高风险误路由怎么算？

**掌握标准：** 先简单基线，低置信澄清；用标注集及风险加权下游影响评估，而非只看总体accuracy。

回到[第03章：L1 应用层：任务、流程与用户交互](../docs/03-ApplicationAndInteraction.md)。

</details>

<a id="q-07"></a>

<!-- teaching-question: new -->

<details>
<summary>Q07｜Run停止以后，应用为什么还不能直接显示“任务完成”？</summary>

**参考开场：** 停止可能是预算耗尽、取消、缺输入、失败或等待审批。应用应按任务验收状态交付结果和未完成事项。

**具体追问：** 用户断线是否取消？→重连显示哪个权威状态？→如何交付部分成果？

**掌握标准：** 区分连接、Run与业务Task生命周期；不把202接受或final文本当作业务完成。

回到[第03章：L1 应用层：任务、流程与用户交互](../docs/03-ApplicationAndInteraction.md)。

</details>

### 04｜L2 运行层：执行循环与控制

<a id="q-08"></a>

<!-- legacy-question: 3 -->

<details>
<summary>Q08｜一个 Minimal Agent Loop 怎么写？</summary>

**参考开场：** `build context → model decision → validate/execute tool → observation → state update → repeat/stop`。

**具体追问：** 模型提出final后马上成功吗？→无权限怎么办？→状态何时记录？

**掌握标准：** 画一次工具调用与观察回填；完成候选需验收，等待输入/预算停止不等于成功。明确图中黑盒和当前实现没有解决的持久化/副作用边界。

回到[第04章：L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md)。

</details>

<a id="q-09"></a>

<!-- legacy-question: 4 -->

<details>
<summary>Q09｜Run / Turn / Step 怎么区分？</summary>

**参考开场：** Run / Step是本课程的执行工作定义，Codex的Thread / Turn / Item是产品交互对象。一次Turn可包含多次推理和工具交互，Item可有多个生命周期事件；要先给本项目定义，再说明映射，而不是强制套一棵通用树。

**具体追问：** Codex的Turn一定只有一次模型调用吗？→Item与Event为什么不是一一对应？→本项目Run如何关联Thread？

**掌握标准：** 先给项目工作定义再做产品映射。Turn可包含多次推理与工具交互；不要套用Session→Run→Turn作为行业统一树，也不要混淆Thread与OS线程。

回到[第04章：L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md)。

</details>

<a id="q-10"></a>

<!-- legacy-question: 5 -->

<details>
<summary>Q10｜Runtime Message 和 Event 有什么区别？</summary>

**参考开场：** Message 是 model-visible conversation 的一部分；Event 是真实 Runtime 事实，未必都喂模型。

**具体追问：** 一个Tool Result对应哪些事件？→并行返回顺序不同怎么办？→哪些事件不应送给模型？

**掌握标准：** 用call_id关联请求与结果，用event_id追踪生命周期；权限决定、排队和检查点事实可只留在运行系统，不必全部成为模型消息。

回到[第04章：L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md)。

</details>

<a id="q-11"></a>

<!-- legacy-question: 6 -->

<details>
<summary>Q11｜Agent 为什么会 Dead Loop？怎么防？</summary>

**参考开场：** 重复 Tool/error、无状态进展；用 signature、max turns、budget、progress detection、replan/human/terminate。

**具体追问：** 合法分页也反复调用同一个Tool，怎么区别？→换查询却一直没新证据呢？→触发后继续还是暂停？

**掌握标准：** 联合动作签名、状态变化、同类错误与无进展计数；区分重复形式和无效循环。停止后记录原因或请求澄清，不只盲加max_steps。

回到[第04章：L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md)。

</details>

<a id="q-12"></a>

<!-- legacy-question: 16 -->

<details>
<summary>Q12｜ReAct 是什么？和 Plan-and-Execute 区别？</summary>

**参考开场：** ReAct 强调 Reason/Act/Observe 交替；Plan-and-execute 先形成较稳定计划，再执行和修订。按环境不确定性选择。

**具体追问：** 环境反馈改变原计划怎么办？→ReAct是否必须展示思维链？→固定阶段能否包含动态Loop？

**掌握标准：** ReAct强调行动与观察反馈，不要求暴露隐藏推理；根据阶段前置条件重规划，确定性流程与动态探索可组合。

回到[第04章：L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md)。

</details>

<a id="q-13"></a>

<!-- legacy-question: 17 -->

<details>
<summary>Q13｜Planning 越详细越好吗？</summary>

**参考开场：** 不是。高不确定环境过度前置规划容易基于错误假设，应该增量 replanning。

**具体追问：** 计划十步后第二步前提失效怎么办？→什么时候不必显式Planner？→怎么防目标漂移？

**掌握标准：** 计划是可修订状态，不是成功证据；保留目标、约束、验收与非目标，并在阶段完成时核验下一步前提。

回到[第04章：L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md)。

</details>

### 05｜L2 运行层：上下文组装、预算与压缩

<a id="q-14"></a>

<!-- legacy-question: 18 -->

<details>
<summary>Q14｜Agent Context 由什么组成？</summary>

**参考开场：** Instructions、Goal、State、History、Memory、Tools、Retrieved Evidence、Tool Results、Environment hints。

**具体追问：** 哪些内容稳定、哪些易过期？→各自预算怎样分？→怎样知道为何丢弃某段？

**掌握标准：** 按来源、版本、权限、优先级与token成本形成可解释的当前输入视图；History只是来源之一，不能拼接所有材料。

回到[第05章：L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md)。

</details>

<a id="q-15"></a>

<!-- legacy-question: 19 -->

<details>
<summary>Q15｜Prompt Engineering、Context Engineering、Harness Engineering 区别？</summary>

**参考开场：** Prompt Engineering主要组织指令；Context Engineering选择和组织本次模型可见信息；Harness Engineering兑现跨轮循环、状态、能力与约束。三者协作，不是用更长Prompt替代可靠执行。

**具体追问：** 改System Prompt能解决重复付款吗？→Context裁剪谁负责？→模型Provider适配在哪？

**掌握标准：** 指令编写、当前输入编排、跨步执行是不同责任；副作用需要状态与执行协议，不靠更长Prompt取代。

回到[第05章：L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md)。

</details>

<a id="q-16"></a>

<!-- legacy-question: 20 -->

<details>
<summary>Q16｜Context Window 大了还需要 Compaction 吗？</summary>

**参考开场：** 是否压缩取决于任务长度、信息增长、成本和质量。大窗口仍需要信息选择与新鲜度管理，但短任务不必为凑组件强行启用Compaction。

**具体追问：** 窗口没满但效果变差怎么办？→何时先外部化不压缩？→何时不需要压缩？

**掌握标准：** 从成本、相关性、噪声、新鲜度和任务长度判断；短任务可不启用压缩，长任务也不能用更大窗口代替状态与信息治理。

回到[第05章：L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md)。

</details>

<a id="q-17"></a>

<!-- legacy-question: 21 -->

<details>
<summary>Q17｜Context Compaction 完整链路？</summary>

**参考开场：** Trigger → select history → compact → build replacement → preserve invariants → persist → recompute tokens → continue。

**具体追问：** 何时触发？→替换哪些消息？→压缩候选失败怎么办？→切换后如何验证？

**掌握标准：** 先预算/外部化，再构建候选、保必需信息、验证保存、切换活动视图并重新计数；区分教学恢复协议和某产品具体实现。

回到[第05章：L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md)。

</details>

<a id="q-18"></a>

<!-- legacy-question: 22 -->

<details>
<summary>Q18｜Compaction 后怎么保证关键约束没丢？</summary>

**参考开场：** Goal/hard constraints/side-effect/artifact/version/current task 等结构化 invariant，summary 不是 source of truth；做 long-task regression。

**具体追问：** 什么约束不能只留在summary？→压缩后合法路径不同算错吗？→怎样构建回归集？

**掌握标准：** 任务约束、批准和动作回执应有独立权威记录；检查继续执行的结果/约束而非逐token或逐动作完全一致，统计重执行和遗漏约束。

回到[第05章：L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md)。

</details>

<a id="q-19"></a>

<!-- legacy-question: 23 -->

<details>
<summary>Q19｜Tool Result 太长怎么办？</summary>

**参考开场：** 先判断哪些结果仍有价值。大且需后续使用的原始信息外部化为受控artifact，Context保留摘要、相关片段和版本引用；不可逆截断会丢证据，重新读取还要验证权限和新鲜度。

**具体追问：** 截前5K会丢什么？→原始结果如何再读取？→artifact失效/越权怎么办？

**掌握标准：** 外部化保留可访问且版本明确的原件，输入中放相关片段、摘要和引用；重新加载必须校验权限和版本。

回到[第05章：L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md)。

</details>

<a id="q-20"></a>

<!-- teaching-question: new -->

<details>
<summary>Q20｜Provider Prompt Cache与Context投影、工具结果缓存有什么区别？</summary>

**参考开场：** 前者复用相同前缀计算；后两者复用应用材料或结果，需版本/权限/新鲜度治理。缓存命中不证明语义正确。

**具体追问：** 新文件内容应放哪里？→如何查“总用旧信息”？→该看什么命中指标？

**掌握标准：** 从应用输入是否过期和Provider计算复用分开排查，不把Prompt Cache解释为缓存最终回答。

回到[第05章：L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md)。

</details>

### 06｜L2 运行层：记忆的选择、使用与维护

<a id="q-21"></a>

<!-- legacy-question: 24 -->

<details>
<summary>Q21｜Stale Context / Stale Memory 怎么处理？</summary>

**参考开场：** version/hash/provenance，read-on-use validation，invalidate superseded projection。

**具体追问：** 旧文件摘要仍在Context怎么办？→Memory纠正但索引未更新呢？→谁是最终事实？

**掌握标准：** 按来源版本及失效标记刷新/重载，不靠新Prompt抵消旧事实；Memory与派生索引不能覆盖权威业务状态。

回到[第06章：L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md)。

</details>

<a id="q-22"></a>

<!-- legacy-question: 25 -->

<details>
<summary>Q22｜Context、Memory、State、History 有什么区别？</summary>

**参考开场：** Context 是当前 token；Memory 是未来可检索信息；State 是当前执行事实；History 是过去轨迹。

**具体追问：** 这四种信息是否都放同一数据库？→摘要能当恢复依据吗？→哪个可以丢弃重建？

**掌握标准：** 语义不同不强制物理分库；Context可重新编译，精确运行/授权/副作用事实需可靠保存，Memory是经选择的未来复用信息。

回到[第06章：L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md)。

</details>

<a id="q-23"></a>

<!-- legacy-question: 26 -->

<details>
<summary>Q23｜Memory 应该怎么分层？</summary>

**参考开场：** Working/Episodic/Semantic/Procedural；写入和读取都有 relevance/confidence/freshness/provenance。

**具体追问：** 短期工作记忆与长期偏好区别？→程序性Memory是否就是Tool？→检索时如何取舍？

**掌握标准：** 分类是帮助设计生命周期的视角，不是必装组件；分别定义写入条件、作用域、来源、更新/失效与按需召回。

回到[第06章：L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md)。

</details>

<a id="q-24"></a>

<!-- legacy-question: 27 -->

<details>
<summary>Q24｜错误 Memory 写进去怎么办？</summary>

**参考开场：** Write gate、provenance/confidence、version、user correction、supersede/delete、revalidation。

**具体追问：** 两条Memory冲突如何裁决？→用户撤销后缓存还命中怎么办？→怎样验证纠错有效？

**掌握标准：** 保留source/version和supersedes关系，读取端排除失效记录并回查权威来源；测纠错后不再误用、删除传播和租户隔离。

回到[第06章：L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md)。

</details>

### 07｜L2 运行层：执行状态、持久化与恢复

<a id="q-25"></a>

<!-- legacy-question: 28 -->

<details>
<summary>Q25｜Checkpoint 保存什么？</summary>

**参考开场：** Run identity、state version、current step、context reference、pending tool/approval、side-effect ledger、artifact、budget。

**具体追问：** messages之外缺了什么？→工具等待/审批等待怎么恢复？→环境引用失效怎么办？

**掌握标准：** 保存执行身份、目标/约束、进度、预算、版本、pending动作/审批和产物引用；检查点不能自动复制或回滚外部世界。

回到[第07章：L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md)。

</details>

<a id="q-26"></a>

<!-- legacy-question: 29 -->

<details>
<summary>Q26｜Resume 为什么不能只重放 messages？</summary>

**参考开场：** 外部副作用、结构化 state、approval、artifact version 可能不在 messages；还需 reconciliation。

**具体追问：** 哪类事件可安全重放？→真正副作用怎么处理？→怎样冷恢复环境？

**掌握标准：** 状态重建与重新执行动作不同；先验证版本和引用、核对未知动作，再重建Context继续，不能只重发旧Prompt。

回到[第07章：L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md)。

</details>

<a id="q-27"></a>

<!-- legacy-question: 30 -->

<details>
<summary>Q27｜Tool 成功但 Checkpoint 失败，恢复后怎么办？</summary>

**参考开场：** 稳定 logical action id/idempotency key + side-effect ledger，先 reconcile external status，再决定 retry/compensate/human。

**具体追问：** 意图应该何时持久化？→下游成功本地失败怎么办？→新worker接管后使用什么键？

**掌握标准：** 逻辑操作标识在可重试动作前建立；接管后复用同一幂等/查询依据补状态，没有下游保证就不能许诺exactly-once。

回到[第07章：L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md)。

</details>

<a id="q-28"></a>

<!-- legacy-question: 31 -->

<details>
<summary>Q28｜Pause、Cancel、Fail 有什么区别？</summary>

**参考开场：** Pause 可 resume；Cancel 是明确终止意图；Fail 是未达到目标的错误终态/可重试态，语义要分开。

**具体追问：** 取消中与已取消相同吗？→暂停多久还能恢复？→失败重试是否新Run？

**掌握标准：** 明确状态转换、保留期限、所有权及结果核对；取消意图不等于外部回滚，失败后的新尝试如何关联由应用契约定义。

回到[第07章：L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md)。

</details>

<a id="q-29"></a>

<!-- legacy-question: 32 -->

<details>
<summary>Q29｜Fork / Branch 需要决定哪些继承语义？</summary>

**参考开场：** Instructions snapshot、state、history、memory、workspace、permission、credentials、budget，不能无脑 deepcopy。

**具体追问：** Fork复制授权吗？→复制实时指令源还是快照？→共享workspace会怎样？

**掌握标准：** 按组件明确继承/重载/拒绝策略；快照不等于实时来源，凭证与批准不可盲复制，外部世界不会因Fork回到过去。

回到[第07章：L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md)。

</details>

<a id="q-30"></a>

<!-- teaching-question: new -->

<details>
<summary>Q30｜Instruction Source与Applied Snapshot在Resume/Fork时有什么差别？</summary>

**参考开场：** 来源是可能变化的提供机制，快照是已用于当前执行的版本。恢复和分叉要明确继承、重载与授权，不默认复制来源和凭证。

**具体追问：** 冷恢复与热恢复怎么验证？→旧批准会不会随Fork继承？

**掌握标准：** 区分产品固定快照观察与通用设计，记录指令/策略/环境版本，变更时核验适用性。

回到[第07章：L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md)。

</details>

### 08｜L2 运行层：多 Agent 协作与调度

<a id="q-31"></a>

<!-- legacy-question: 46 -->

<details>
<summary>Q31｜Multi-Agent 什么时候值得？</summary>

**参考开场：** 子任务独立可并行、Context 可隔离、role/tool 区分明显、结果易聚合。否则单 Agent 更简单。

**具体追问：** 怎样证明子任务独立？→上下文开销如何计算？→单Agent基线是否更好？

**掌握标准：** 看可并行性、共享资源、返回证据和聚合难度；同一任务集比较质量、时延、成本及失败传播，避免按角色数量设计。

回到[第08章：L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md)。

</details>

<a id="q-32"></a>

<!-- legacy-question: 47 -->

<details>
<summary>Q32｜Manager、Agent-as-Tool、Handoff 区别？</summary>

**参考开场：** Manager 持有控制权；agent-as-tool child 返回结果；handoff 转移控制权。

**具体追问：** 谁持有最终完成权？→子任务失败传给谁？→交接后取消由谁处理？

**掌握标准：** 区分控制权保持、调用返回和控制权转交；写清父子状态、返回契约、取消传播及最终验收责任。

回到[第08章：L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md)。

</details>

<a id="q-33"></a>

<!-- legacy-question: 48 -->

<details>
<summary>Q33｜多 Agent 同时修改 Repo 怎么办？</summary>

**参考开场：** Task ownership、独立 worktree/branch、version check/lock、merge + verification。

**具体追问：** 不同工具同写一个文件呢？→worktree隔离后还能有冲突吗？→谁合并与验证？

**掌握标准：** 用资源所有权、基线版本、隔离分支和合并验证；信息隔离不能替代写入协调，合并仍需回归与验收。

回到[第08章：L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md)。

</details>

<a id="q-34"></a>

<!-- legacy-question: 49 -->

<details>
<summary>Q34｜A2A 需要哪些关键语义？</summary>

**参考开场：** 需要核对采用版本的发现、任务身份/状态、消息与产物、认证及取消/失败语义；跨系统trace、预算和结果验收还要由应用与运行层设计，不是协议自动保证。

**具体追问：** task与artifact如何关联？→取消请求丢失怎么办？→如何跨系统追踪？

**掌握标准：** 对齐任务身份、状态、消息/产物与认证，明确超时、取消和预算传播；具体协议版本需要核对，不能靠发消息替代协作语义。

回到[第08章：L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md)。

</details>

<a id="q-35"></a>

<!-- legacy-question: 41 -->

<details>
<summary>Q35｜MCP 和 A2A 区别？</summary>

**参考开场：** MCP 偏 Agent ↔ capability/context server；A2A 偏独立 Agent system ↔ Agent system。

**具体追问：** 内部Agent-as-Tool一定用A2A吗？→MCP能封装远程Agent能力吗？→协议解决不了什么？

**掌握标准：** 接口包装与任务协作是不同抽象；协议可组合，但分工、预算、授权、聚合与验收仍由应用/运行层负责。

回到[第08章：L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md)。

</details>

### 09｜L3 接入层：模型适配、路由与容错

<a id="q-36"></a>

<!-- legacy-question: 45 -->

<details>
<summary>Q36｜Model Routing 看哪些因素？</summary>

**参考开场：** Task、quality、context size、risk、latency SLO、cost、provider health、capability compatibility。

**具体追问：** 便宜模型是否支持同一Tool协议？→切换后状态如何保留？→Fallback如何记录？

**掌握标准：** 能力、上下文、多模态、质量、SLO和成本共同约束；Provider失败不是重跑全部业务动作的理由，显式记录兼容性与降级。

回到[第09章：L3 接入层：模型适配、路由与容错](../docs/09-ModelAccessAndRouting.md)。

</details>

### 10｜L3 接入层：工具契约、注册与发现

<a id="q-37"></a>

<!-- legacy-question: 7 -->

<details>
<summary>Q37｜Tool Calling 完整链路是什么？</summary>

**参考开场：** Model call → parse/schema → semantic validation → permission/approval → route/executor → result → persist/trace → observation。

**具体追问：** JSON已解析为何还不能执行？→使用哪个工具版本？→执行结果怎样回到下一轮？

**掌握标准：** 顺着解析、目录解析、结构/语义、身份权限、执行、回执/事件、观察投影回答；说明外部动作和本地记录未必原子。

回到[第10章：L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md)。

</details>

<a id="q-38"></a>

<!-- legacy-question: 8 -->

<details>
<summary>Q38｜Tool schema 为什么不等于安全？</summary>

**参考开场：** Schema 只保证结构；还需业务语义、权限、sandbox、side-effect policy。

**具体追问：** 字段类型正确但tenant_id伪造怎么办？→资源版本变了呢？→校验失败反馈给谁？

**掌握标准：** 结构校验不能建立身份/授权；从可信上下文取身份，执行端校验资源范围、版本和业务规则。有限参数修复不允许修复掉权限边界。

回到[第10章：L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md)。

</details>

<a id="q-39"></a>

<!-- legacy-question: 13 -->

<details>
<summary>Q39｜为什么 Tool 需要 read-only / destructive / concurrency-safe metadata？</summary>

**参考开场：** 决定 approval、parallelism、retry 和 sandbox policy。

**具体追问：** 只读工具是否完全安全？→同名工具不同资源能否并行？→metadata由谁可信地产生？

**掌握标准：** 只读也有泄密和负载风险；按输入、资源键和执行条件判断风险/并发，不信模型自报安全。执行端仍做授权。

回到[第10章：L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md)。

</details>

<a id="q-40"></a>

<!-- legacy-question: 15 -->

<details>
<summary>Q40｜Tool 很多时怎么处理？</summary>

**参考开场：** Capability catalog → discovery/rank → progressive load 少量完整 schemas → exact selection。

**具体追问：** 正确工具没进候选怎么办？→选对但版本不匹配怎么办？→怎样测发现效果？

**掌握标准：** 目录覆盖、候选召回、模型选择、执行成功分别评估；按权限和任务逐步暴露，namespace/版本解析独立于相似度排名。

回到[第10章：L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md)。

</details>

### 11｜L3 接入层：工具执行、副作用与取消

<a id="q-41"></a>

<!-- legacy-question: 9 -->

<details>
<summary>Q41｜Tool Result 应返回字符串还是结构化对象？</summary>

**参考开场：** 优先有稳定 status/error/data 结构；给模型可读摘要，raw result 可外置。

**具体追问：** 模型、日志、Host是否需要同一份结果？→结果50K token怎么办？→HTTP 200但产物不存在呢？

**掌握标准：** 分离可见摘要、结构化状态、受控原始产物、遥测和内部元数据；执行成功还需结果验收，失败不能伪装空成功。

回到[第11章：L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md)。

</details>

<a id="q-42"></a>

<!-- legacy-question: 10 -->

<details>
<summary>Q42｜Tool Failure 怎么分类？</summary>

**参考开场：** Invalid input、permission、not found、timeout、rate limit、transient network、permanent business、partial success。

**具体追问：** 参数错、权限拒绝、网络断开分别怎么处理？→partial/unknown归哪一类？→何时Fatal？

**掌握标准：** 区分可修参数、可能暂态、永久业务失败、取消、结果未知和运行时致命错误。错误分类决定动作，不用统一异常重试吞掉状态。

回到[第11章：L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md)。

</details>

<a id="q-43"></a>

<!-- legacy-question: 11 -->

<details>
<summary>Q43｜哪些 Tool 可以自动 Retry？</summary>

**参考开场：** 错误 transient + 动作安全重放/幂等 + budget/deadline 允许。

**具体追问：** HTTP 500是否一定可重试？→多层重试会怎样？→调用超时但动作已执行呢？

**掌握标准：** 重试资格同时要求错误可能恢复、动作可安全重放/核对、deadline及重试预算允许；服务端失败响应也不能证明副作用未发生。

回到[第11章：L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md)。

</details>

<a id="q-44"></a>

<!-- legacy-question: 12 -->

<details>
<summary>Q44｜Tool 已成功但响应超时怎么办？</summary>

**参考开场：** 进入 UNKNOWN，按 idempotency key/resource id reconcile，而非盲 retry。

**具体追问：** 结果未知时先查哪里？→没有幂等/查询接口怎么办？→迟到回执怎样合并？

**掌握标准：** 稳定operation_id/幂等键关联同一逻辑动作，核对外部权威状态；不能核对则保留UNKNOWN并升级，不生成新业务ID重复提交。

回到[第11章：L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md)。

</details>

<a id="q-45"></a>

<!-- legacy-question: 14 -->

<details>
<summary>Q45｜用户在 Tool 执行中发新消息怎么办？</summary>

**参考开场：** Runtime 要定义 interrupt behavior：cancel、block，或特定 Tool 的 cooperative handling。

**具体追问：** 新消息是澄清还是换目标？→正在提交外部写入时能立即取消吗？→何时应用新契约？

**掌握标准：** 将消息转成带版本的运行事件；在可中断/安全边界生效，传播取消并处理迟到结果，不能修改已经发出的模型请求当作即时生效。

回到[第11章：L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md)。

</details>

### 12｜L3 接入层：知识、记忆与扩展能力接入

<a id="q-46"></a>

<!-- legacy-question: 39 -->

<details>
<summary>Q46｜MCP 是什么？解决什么？</summary>

**参考开场：** Host/Client/Server 标准协议，连接 Tool/Resource/Prompt；不等于 Agent Loop。

**具体追问：** 有MCP为何还需自己的Loop？→server不可用如何处理？→认证由谁保证？

**掌握标准：** 协议连接能力并不决定任务控制；Host保留权限、状态和预算责任，失败要以运行语义返回，不静默假成功。

回到[第12章：L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md)。

</details>

<a id="q-47"></a>

<!-- legacy-question: 40 -->

<details>
<summary>Q47｜MCP Tool、Resource、Prompt 怎么区分？</summary>

**参考开场：** MCP中Tool暴露可调用能力，Resource暴露供应用选择的上下文资源，Prompt暴露可选择的模板/交互入口。控制意图与实际界面可不同；工具也能读数据，不能简单按“读/写”划分原语。

**具体追问：** 工具能读取数据吗？→Resource何时进入Context？→Prompt能修改权限吗？

**掌握标准：** 按协议原语与控制意图解释而非按HTTP方法划分；工具也可查询，模板/资源都不自动成为可信授权。

回到[第12章：L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md)。

</details>

<a id="q-48"></a>

<!-- legacy-question: 42 -->

<details>
<summary>Q48｜Tool、Skill、MCP、Command 有什么区别？</summary>

**参考开场：** Tool 动作；Skill 程序性能力包；MCP 连接协议；Command 用户显式入口。

**具体追问：** Skill含脚本是否自动执行？→Command入口会不会触发确定性流程？→为何渐进加载？

**掌握标准：** 程序性知识、动作、连接协议和用户入口分开；脚本执行仍经授权，加载按需要以控制token、歧义与风险。

回到[第12章：L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md)。

</details>

<a id="q-49"></a>

<!-- legacy-question: 43 -->

<details>
<summary>Q49｜Hook / Plugin 在 Runtime 里怎么定位？</summary>

**参考开场：** Hook 是 lifecycle extension point；Plugin 可打包 tools/hooks/skills 等。核心安全语义不要只依赖可选 hook。

**具体追问：** 安全Hook失败如何处理？→Plugin卸载时当前Run怎么办？→Hook能否代替主循环？

**掌握标准：** 扩展点有明确阶段/错误策略/版本，安全门不能仅靠可选插件；核心运行语义由Runtime持有。

回到[第12章：L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md)。

</details>

### 13｜L4 资源层：模型、数据与执行环境

<a id="q-50"></a>

<!-- legacy-question: 38 -->

<details>
<summary>Q50｜怎样限制 Agent blast radius？</summary>

**参考开场：** workspace/network/credential scope、destructive approval、tenant isolation、resource quota、containment。

**具体追问：** 只限制文件目录够吗？→网络外传和共享凭证呢？→sandbox重建会丢什么？

**掌握标准：** 范围覆盖文件/网络/进程/身份/配额/产物；按资源生命周期验证隔离，不把容器存在当成安全证明。

回到[第13章：L4 资源层：模型、数据与执行环境](../docs/13-ResourcesAndEnvironments.md)。

</details>

### 14｜横切治理：身份、权限、审批与安全

<a id="q-51"></a>

<!-- legacy-question: 33 -->

<details>
<summary>Q51｜Permission、Approval、Sandbox 区别？</summary>

**参考开场：** Policy定义允许范围，Approval绑定一次具体动作的人工决定，Sandbox或其他资源侧执行约束限制真实访问。三者不同；是否需要代码沙箱取决于执行环境，审批不能授予资源本来没有的权限。

**具体追问：** 系统规则允许是否还需本次确认？→有确认为何还需隔离？→哪些任务没有代码沙箱？

**掌握标准：** 策略、本次批准和执行约束是不同责任；按动作风险组合，API-only任务可不建代码环境，但资源服务自身授权仍必需。

回到[第14章：横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<a id="q-52"></a>

<!-- legacy-question: 34 -->

<details>
<summary>Q52｜HITL 为什么不是一个 confirm 弹窗？</summary>

**参考开场：** 长任务中要持久化 WAITING_APPROVAL / RunState，绑定 call_id+args，批准后恢复原 Run。

**具体追问：** 审批等待时worker重启怎么办？→批准绑定工具名够吗？→参数或策略变更呢？

**掌握标准：** 保存等待状态和具体动作范围，绑定身份、参数/资源版本与有效期；恢复和执行时再校验，不依赖进程内弹窗状态。

回到[第14章：横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<a id="q-53"></a>

<!-- legacy-question: 35 -->

<details>
<summary>Q53｜Prompt Injection 怎么防？</summary>

**参考开场：** Trust boundary + least privilege + permission + approval + sandbox + secret/egress containment；检测只是附加层。

**具体追问：** 注入来自工具结果怎么办？→检测漏了还能限制什么？→输出过滤为何太晚？

**掌握标准：** 保持指令/数据可信边界，最小权限、动作门与环境/凭证/外传限制联动；检测只是附加防线，不能保证永不被骗。

回到[第14章：横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<a id="q-54"></a>

<!-- legacy-question: 36 -->

<details>
<summary>Q54｜RAG / Tool Result 为什么也是 untrusted context？</summary>

**参考开场：** 外部数据可能携带恶意或过期 instruction，不应提升为 system policy。

**具体追问：** 内部文档是否自动可信？→外部内容能否要求扩大权限？→如何保留来源？

**掌握标准：** 内容可信度与指令权限不同；保留来源、作用域、版本及trust标签，资源返回不能自授予执行授权。

回到[第14章：横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<a id="q-55"></a>

<!-- legacy-question: 37 -->

<details>
<summary>Q55｜Secret 为什么不要直接放 Context？</summary>

**参考开场：** 用 credential broker/tool 代持；Context 暴露会被模型输出、日志或 injection 外传。

**具体追问：** Key放环境变量是否就安全？→任意Shell会读到吗？→Trace会泄漏吗？

**掌握标准：** 凭证代持和最小scope，避免模型与任意代码直接接触；对可访问环境、日志、产物与外传路径共同控制。

回到[第14章：横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

<a id="q-56"></a>

<!-- teaching-question: new -->

<details>
<summary>Q56｜用户已批准写文件，但执行前文件或参数变化了怎么办？</summary>

**参考开场：** 批准绑定具体身份、目标、参数/差异、契约版本和有效期。变化后重新校验，不匹配则拒绝或再次确认。

**具体追问：** 只批准工具名够吗？→原批准后来被撤销呢？→已完成的写入能自动撤销吗？

**掌握标准：** 说明检查到执行之间的变化窗口；授权、资源版本和已发生副作用分别处理。

回到[第14章：横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md)。

</details>

### 15｜横切治理：观测、评测与持续改进

<a id="q-57"></a>

<!-- legacy-question: 50 -->

<details>
<summary>Q57｜Agent Trace 应记录什么？</summary>

**参考开场：** Run/Turn/Generation/Tool/State/Approval/Handoff，model-visible context、tool evidence、latency/cost/error。

**具体追问：** 如何知道模型看到了哪版文件？→大payload放哪里？→如何兼顾脱敏？

**掌握标准：** 关联模型调用、工具、状态、审批、压缩、产物与结果；保留可受控解析的证据引用和版本，不要求记录隐藏推理。

回到[第15章：横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md)。

</details>

<a id="q-58"></a>

<!-- legacy-question: 51 -->

<details>
<summary>Q58｜Replay 时为什么不能直接重执行所有 Tool？</summary>

**参考开场：** 会重复副作用且环境已变化；应区分 event replay 和 eval replay，外部 Tool 通常 mock/freeze。

**具体追问：** 回放历史事实、重调模型、重执行工具有什么差异？→环境已变怎么办？→如何隔离危险操作？

**掌握标准：** 分别使用事件重建、冻结输入的评测、受限测试环境/Mock；默认不向线上真实副作用接口重放。

回到[第15章：横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md)。

</details>

<a id="q-59"></a>

<!-- legacy-question: 52 -->

<details>
<summary>Q59｜Agent Eval 和普通 LLM Eval 有什么不同？</summary>

**参考开场：** 除了输出文本，还要评 trajectory、Tool、artifact、environment outcome。

**具体追问：** 只看最终回答会漏什么？→哪个结果可确定性验证？→过程指标怎么用？

**掌握标准：** 同时评价任务结果、运行过程、组件、资源与安全；过程只是诊断，不能用少token或漂亮轨迹代替完成任务。

回到[第15章：横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md)。

</details>

<a id="q-60"></a>

<!-- legacy-question: 53 -->

<details>
<summary>Q60｜LLM Judge 可以作为唯一 Agent Grader 吗？</summary>

**参考开场：** 不建议。能 deterministic 验证的环境结果优先；Judge 补主观维度并做人工校准。

**具体追问：** 测试通过是否证明所有需求？→Judge偏好变化怎么办？→怎样构建可信评分？

**掌握标准：** 确定性检查覆盖明确不变量；主观质量由校准Judge与人工补充。固定数据和评分版本，防泄漏与对评分器过拟合。

回到[第15章：横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md)。

</details>

<a id="q-61"></a>

<!-- teaching-question: new -->

<details>
<summary>Q61｜如何把一次Agent bad case变成可证明有效的改进？</summary>

**参考开场：** 用trace和外部结果定位责任，形成固定输入/环境的回归用例，修改相应机制，再比较结果、约束、成本与失败恢复并受控上线。

**具体追问：** 是检索、Context还是Loop错误？→改动如何隔离？→怎样防只对单一案例过拟合？

**掌握标准：** 能说出定位证据、修改对象、对照条件、验收指标和回滚，而不是泛泛说换模型。

回到[第15章：横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md)。

</details>

### 16｜系统收口：部署、成本、选型与演进

<a id="q-62"></a>

<!-- legacy-question: 54 -->

<details>
<summary>Q62｜Coding Agent 怎样证明 Patch 可交付？</summary>

**参考开场：** Repo understanding → patch → focused/broad tests → lint/typecheck/build → diff review → requirement verification。

**具体追问：** 改对文件了吗？→测试弱或未覆盖需求怎么办？→工作区有他人改动怎么办？

**掌握标准：** 检查最小差异、原始baseline、focused/broad测试及独立验收；不覆盖无关改动，不把模型自评或exit0当全部正确性证据。

回到[第16章：系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md)。

</details>

<a id="q-63"></a>

<!-- legacy-question: 55 -->

<details>
<summary>Q63｜Production Agent Runtime 怎么拆？</summary>

**参考开场：** API / Run Service / Harness Worker / Model Router / Tool Gateway / Sandbox / State-Event / Artifact / Queue / Trace-Eval / Tenant isolation。

**具体追问：** 四层如何映射单进程/多worker？→长任务重启怎么继续？→额度不足如何接纳？

**掌握标准：** 先职责和状态所有权，再考虑队列、租约、凭证/环境、持久状态、事件及评测；规模化不要求所有组件立即拆微服务。

回到[第16章：系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md)。

</details>

<a id="q-64"></a>

<!-- legacy-question: 56 -->

<details>
<summary>Q64｜LangGraph / Agents SDK / 自研 Loop 怎么选？</summary>

**参考开场：** 先列 state/recovery/tool-policy/streaming/multi-agent/trace/deployment 需求，再匹配框架抽象；不是看流行度。

**具体追问：** 框架支持恢复为何还要测试？→能否替换state store/tool执行？→升级迁移如何做？

**掌握标准：** 用固定版本和真实工作负载验证恢复、审批、取消、trace等；保留Domain State、Tool Contract、Eval Dataset边界及escape hatch。

回到[第16章：系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md)。

</details>

## 易错点｜保留细粒度，但按主题折叠

以下保留旧版86个错误辨析位置，对必选组件、运行对象、缓存、授权和验证范围做了边界澄清。这是检查表，不是另一条学习顺序。

<details>
<summary>系统与控制权｜1–6</summary>

1. ❌ LLM+Tools就足以解释完整Agent系统。✅ 还需说明由谁推进、约束、验收与处理失败；具体Memory、Checkpoint、多Agent等按任务需要选择，不是身份必选项。

2. ❌ 有 Function Calling 就一定是 Agent。✅ 固定单步/流程仍可能是 Workflow。

3. ❌ Agent 一定比 Workflow 高级。✅ 确定流程优先 deterministic workflow。

4. ❌ Harness 就是 System Prompt。✅ Harness 是真实执行 Runtime。

5. ❌ messages[] 就是全部 Agent State。✅ State/History/Memory/Event 必须区分。

6. ❌ Run、Turn、Step 都是“一轮”。✅ 它们承担不同 scope。

</details>

<details>
<summary>工具、重试与取消｜7–18</summary>

7. ❌ Tool Call JSON解析成功就能执行。✅ 还需语义、可信身份/权限与资源前置检查；是否需要代码沙箱取决于实际执行方式。

8. ❌ Tool schema 等于安全。✅ Schema 不处理授权和副作用。

9. ❌ 所有 Tool Error 都 Retry。✅ permanent/permission/partial-success 不能盲重试。

10. ❌ HTTP 500 一定可重试。✅ Server 可能已产生副作用。

11. ❌ Timeout 代表 Tool 没执行。✅ 结果可能 UNKNOWN。

12. ❌ 每次重试都建立新的逻辑动作身份。✅ operation_id/幂等键需稳定；attempt_id和网络request_id可以区分每次尝试。

13. ❌ read-only Tool 没风险。✅ 可能读取 secret 并外传。

14. ❌ async Tool 都可以并行。✅ 要看共享 workspace/resource。

15. ❌ 破坏性Tool只能一概禁止或一概放行。✅ 按合法业务、风险、具体批准和资源侧约束决定；不能用提示词替代授权。

16. ❌ Cancellation 就抛 CancelledError。✅ 需要传播、cleanup、terminal event、late-result reconcile。

17. ❌ Progress 就是打印 log。✅ 应有稳定阶段和 machine-readable event。

18. ❌ Streaming 等于执行完成。✅ 仍需 terminal result。

</details>

<details>
<summary>规划与上下文｜19–29</summary>

19. ❌ Planning 越长越好。✅ 高不确定环境需要增量 replanning。

20. ❌ ReAct 就是把 Thought 打出来。✅ 核心是 reasoning/action/observation 反馈循环。

21. ❌ Model说done就算成功。✅ 按任务契约校验结果；有限检查只能证明覆盖的属性。

22. ❌ max_turns 足够防死循环。✅ 还要 repeated action / no-progress detection。

23. ❌ Context = Prompt。✅ Context 包含全部当前 inference token 来源。

24. ❌ Context 越长越好。✅ 有延迟、成本、噪声与质量问题。

25. ❌ 大窗口保证不再需要上下文治理。✅ 仍需管理成本、相关性和新鲜度；短任务也不必强制启用压缩。

26. ❌ Compaction = summary(history)。✅ 还涉及 trigger/replacement/persistence/invariant/failure。

27. ❌ 摘要写得通顺就算正确。✅ 关键是 constraint/state 不丢。

28. ❌ Summary 可以当 Source of Truth。✅ 精确状态应结构化持久化。

29. ❌ Tool Result 太大就直接截断。✅ 重要原始信息要可寻址 offload。

</details>

<details>
<summary>记忆、状态与恢复｜30–39</summary>

30. ❌ Memory = Vector DB。✅ Memory 是 lifecycle/provenance 模型，存储只是实现。

31. ❌ 所有聊天都写长期 Memory。✅ 会产生污染与隐私问题。

32. ❌ History = Memory。✅ History 是轨迹，Memory 是可复用筛选信息。

33. ❌ State = Context。✅ State 是 Runtime truth，Context 是投影。

34. ❌ Checkpoint = 保存 messages。✅ 还要 step/side-effect/approval/artifact/version。

35. ❌ Resume = 把旧 prompt 再发一次。✅ 先 load/reconcile/rebuild/continue。

36. ❌ Tool success 后写 checkpoint 就绝对安全。✅ 两者之间仍有 crash window。

37. ❌ Compensation = rollback transaction。✅ 外部 Saga 补偿本身也可能失败。

38. ❌ Fork就是deepcopy全部session。✅ 定义状态、指令快照、工作区与预算继承；凭证、批准和实时来源不能默认复制。

39. ❌ Replay = 重跑历史 Tool。✅ 会重复副作用；区分 state replay / eval replay。

</details>

<details>
<summary>权限、注入与秘密｜40–49</summary>

40. ❌ Permission等于Sandbox。✅ 前者表达允许范围，后者限制特定环境的真实操作；API-only工具还依赖资源服务本身的授权。

41. ❌ Approval = confirm dialog。✅ 长任务要可持久化 WAITING_APPROVAL 和 resume。

42. ❌ 只批准Tool名就够。✅ 批准需绑定实际身份、动作参数/目标版本、契约范围和有效期，并在执行时核验。

43. ❌ Guardrail 可以替代 IAM。✅ Guardrail 是 defense-in-depth。

44. ❌ Output Guardrail 能阻止已执行副作用。✅ 已经太晚。

45. ❌ Prompt Injection 只来自用户。✅ RAG/网页/邮件/Tool result/repo 都可能是载体。

46. ❌ System Prompt 写“不要泄密”就够。✅ 要 least privilege / sandbox / egress containment。

47. ❌ 公司内部文档都是 trusted instruction。✅ 业务数据仍不应升级为控制指令。

48. ❌ API Key 放 env 就安全。✅ 任意 shell 仍可能读取/打印/外传。

49. ❌ Trace越全越好。✅ 脱敏、访问控制、保留期限与可受控解析的证据引用一起设计，不记录隐藏思维链。

</details>

<details>
<summary>发现、协议与扩展｜50–58</summary>

50. ❌ Tool 多了只要模型更强。✅ Schema 数量会吞 Context，需要 discovery。

51. ❌ Discovery 只为省 Token。✅ 也影响正确 Tool 的 candidate recall。

52. ❌ Tool name 可以永久做 ID。✅ 重名/改名/版本会破坏 replay。

53. ❌ MCP = Agent Framework。✅ MCP 是 Context/Capability 协议。

54. ❌ MCP就是Tool Calling。✅ 它还定义资源、模板等协议原语；工具可以读数据，控制意图不等于固定用户界面。

55. ❌ Skill = Tool。✅ Skill 是程序性知识/资源包，Tool 是动作。

56. ❌ Skill 全量加载最好。✅ 应 progressive discovery/load。

57. ❌ Hook = Plugin。✅ Hook 是生命周期点，Plugin 是可打包扩展。

58. ❌ 安全关键逻辑只做 hook。✅ 核心 permission/sandbox 应是一等 Runtime 机制。

</details>

<details>
<summary>路由与协作｜59–69</summary>

59. ❌ Router 一律用最大 LLM。✅ 从 rule/small classifier 等最低复杂度开始。

60. ❌ Route accuracy 高就够。✅ 高风险误路由、latency、fallback 也要测。

61. ❌ Fallback 只换 model name。✅ Context/tool capability/state 可能不兼容。

62. ❌ Multi-Agent 一定更强。✅ token/coordination/failure/eval 成本高。

63. ❌ 子任务多就拆 Agent。✅ 关键看独立性、并行性与聚合难度。

64. ❌ Subagent 自动知道 Parent 一切。✅ Context 必须显式传递。

65. ❌ Child 返回完整 transcript 最完整。✅ 会污染 parent Context，优先 artifact/evidence。

66. ❌ Handoff = Agent-as-Tool。✅ 控制权语义不同。

67. ❌ A2A = MCP。✅ Agent-to-Agent vs Agent-to-Capability。

68. ❌ Agent 互相发消息就解决并发。✅ 共享资源仍需 ownership/version/lock。

69. ❌ 多 Agent 同 branch 写代码没问题。✅ 极易 lost update / dirty workspace。

</details>

<details>
<summary>观测、评测与交付｜70–77</summary>

70. ❌ Log = Trace。✅ Trace 要有 Run/Turn/Tool/State correlation。

71. ❌ 只记录 final response 就能 Debug。✅ 需要 model-visible context 与 tool evidence。

72. ❌ Replay 可以用线上真实 Tool。✅ 可能重复危险动作。

73. ❌ Agent 自己说完成就算成功。✅ 看 environment outcome / artifact。

74. ❌ LLM Judge 可以验证所有 Coding Task。✅ 能跑 test 的就优先 deterministic verifier。

75. ❌ Benchmark分数等于线上质量。✅ 数据、环境、评分及版本决定适用范围，还需真实任务验证。

76. ❌ Coding Agent = 代码生成器。✅ Repo understanding + execution + verification 才完整。

77. ❌ Test 过了必然正确。✅ 可能测试弱、需求没覆盖、hack 测试。

</details>

<details>
<summary>生产选型与证据边界｜78–86</summary>

78. ❌ Production Agent必须同步HTTP长连接跑到底。✅ 请求、连接和任务生命周期分开；是否异步化由持续时间、恢复和规模要求决定。

79. ❌ Worker 内存就是 durable session。✅ crash/迁移会丢状态。

80. ❌ 每个Agent都必须永久绑定一个容器。✅ 按状态、隔离、资源成本和恢复需要管理环境生命周期，也可同进程实现逻辑职责。

81. ❌ Redis 是所有 Agent State 的唯一答案。✅ durability/query/transaction 不同层需要不同存储。

82. ❌ LangGraph Node/Edge 就是 Agent 本质。✅ 它是一种 Runtime implementation mapping。

83. ❌ 框架越重越 Production。✅ 抽象不匹配反而增加复杂度。

84. ❌ 自研 Loop 一定更专业。✅ 成熟 checkpoint/trace/integration 可通过框架节省成本。

85. ❌ Claude Code/Codex具体实现就是行业标准。✅ 固定源码是实现证据，四层是教材综合参考架构，不复制不需要的组件。

86. ❌ 官方文章出现的概念可以增加面经频率。✅ HUMAN-A Source Count 只由 Tier A 决定。

</details>

## 面试前速查｜只回忆职责与关键失败窗口

| 主题 | 一句话检查 | 回正文 |
|---|---|---|
| 任务与自主权 | 先明确目标/范围/环境/验收，再决定控制权；组件由需求推导。 | [01](../docs/01-AgentSystemAndTaskContract.md) |
| 四层与横切 | 应用交付、运行推进、接入适配、资源兑现；安全质量贯穿，非四个微服务。 | [03](../docs/03-ApplicationAndInteraction.md) |
| Loop与停止 | Context→候选→校验/执行→观察/状态→验证或继续；停止原因不等于成功。 | [04](../docs/04-AgentLoopAndControl.md) |
| 对象与事件 | Task/Run是工作定义，Codex Thread/Turn/Item是产品交互；call/operation/attempt分别标识。 | [04](../docs/04-AgentLoopAndControl.md) |
| Context与压缩 | 选择/去重/预算→外部化→候选压缩→验证/保存/切换；保留可恢复事实。 | [05](../docs/05-ContextEngineering.md) |
| Memory | 选择→写入→按需召回→纠错/失效；Memory不建立权限，也不替代权威事实。 | [06](../docs/06-MemoryLifecycle.md) |
| 恢复 | 载入版本与状态→核对未知动作→恢复引用/环境→重建Context→继续。 | [07](../docs/07-StateAndRecovery.md) |
| 多Agent | 先独立性与汇聚契约，再控制共享资源、子预算、失败和取消。 | [08](../docs/08-MultiAgentCoordination.md) |
| 模型接入 | 能力兼容、时延/成本与错误分类决定路由，Fallback不是全任务重跑。 | [09](../docs/09-ModelAccessAndRouting.md) |
| 工具发现 | 完整目录→受控候选→完整schema→精确handler/版本；曝光不等于授权。 | [10](../docs/10-ToolContractAndDiscovery.md) |
| 工具执行 | 结构/语义/权限→Invocation→结果核验→事件与观察；未知结果先核对。 | [11](../docs/11-ToolExecutionAndEffects.md) |
| MCP/Skill/Hook | 连接协议、程序性知识包、生命周期扩展分别设计；加载不产生执行许可。 | [12](../docs/12-KnowledgeAndCapabilityAccess.md) |
| 资源与安全 | 模型/数据/环境保存不同事实；审批绑定实际动作，隔离与外传限制可共同约束。 | [14](../docs/14-IdentityPermissionsAndSafety.md) |
| Trace与Eval | 观察事实≠评估成功；回放证据≠重做副作用；独立验证后再形成改进闭环。 | [15](../docs/15-ObservabilityAndEvaluation.md) |
| 代码交付 | 理解资源→最小patch→测试/构建→diff→独立验收；测试过不等于所有需求正确。 | [16](../docs/16-ProductionArchitectureAndEvolution.md) |
| 部署选型 | 先状态所有权、故障边界与预算，再选Worker/Queue/框架；固定版本验证真实负载。 | [16](../docs/16-ProductionArchitectureAndEvolution.md) |

## 44 道真人问题的学习位置

下表只维护学习位置，不复制或重算研究证据。

| Canonical | 主责章节 |
|---|---|
| `AGENT-001` | [02 能力设计与自主权分配](../docs/02-CapabilityAndAutonomy.md) |
| `AGENT-002` | [01 Agent 系统与任务契约](../docs/01-AgentSystemAndTaskContract.md) |
| `AGENT-003` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-004` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-005` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-006` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-007` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-008` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-009` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-010` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-011` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-012` | [05 L2 运行层：上下文组装、预算与压缩](../docs/05-ContextEngineering.md) |
| `AGENT-014` | [06 L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md) |
| `AGENT-015` | [06 L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md) |
| `AGENT-016` | [06 L2 运行层：记忆的选择、使用与维护](../docs/06-MemoryLifecycle.md) |
| `AGENT-017` | [07 L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md) |
| `AGENT-018` | [10 L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md) |
| `AGENT-019` | [10 L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md) |
| `AGENT-020` | [11 L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md) |
| `AGENT-021` | [10 L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md) |
| `AGENT-022` | [10 L3 接入层：工具契约、注册与发现](../docs/10-ToolContractAndDiscovery.md) |
| `AGENT-023` | [12 L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md) |
| `AGENT-024` | [12 L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md) |
| `AGENT-025` | [12 L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md) |
| `AGENT-026` | [11 L3 接入层：工具执行、副作用与取消](../docs/11-ToolExecutionAndEffects.md) |
| `AGENT-027` | [07 L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md) |
| `AGENT-028` | [14 横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md) |
| `AGENT-029` | [07 L2 运行层：执行状态、持久化与恢复](../docs/07-StateAndRecovery.md) |
| `AGENT-030` | [08 L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md) |
| `AGENT-031` | [08 L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md) |
| `AGENT-032` | [09 L3 接入层：模型适配、路由与容错](../docs/09-ModelAccessAndRouting.md) |
| `AGENT-034` | [15 横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md) |
| `AGENT-035` | [15 横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md) |
| `AGENT-036` | [16 系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md) |
| `AGENT-037` | [12 L3 接入层：知识、记忆与扩展能力接入](../docs/12-KnowledgeAndCapabilityAccess.md) |
| `AGENT-038` | [09 L3 接入层：模型适配、路由与容错](../docs/09-ModelAccessAndRouting.md) |
| `AGENT-041` | [15 横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md) |
| `AGENT-042` | [04 L2 运行层：执行循环与控制](../docs/04-AgentLoopAndControl.md) |
| `AGENT-043` | [15 横切治理：观测、评测与持续改进](../docs/15-ObservabilityAndEvaluation.md) |
| `AGENT-044` | [14 横切治理：身份、权限、审批与安全](../docs/14-IdentityPermissionsAndSafety.md) |
| `AGENT-045` | [03 L1 应用层：任务、流程与用户交互](../docs/03-ApplicationAndInteraction.md) |
| `AGENT-046` | [08 L2 运行层：多 Agent 协作与调度](../docs/08-MultiAgentCoordination.md) |
| `AGENT-047` | [16 系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md) |
| `AGENT-048` | [16 系统收口：部署、成本、选型与演进](../docs/16-ProductionArchitectureAndEvolution.md) |
