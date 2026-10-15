# 403份面经：考察重点、追问深度与备考依据

[← 面经业务](../README.md) · [备考回答](../../../interview/README.md) · [归并问题](../01-data/questions.json) · [逐记录判断](model-review.json)

## 范围与结论怎么读

本次固定 S001–S403 的38批保存材料，包含404个来源区块（含S288同流程扩展）。模型逐份阅读来源上下文，对全部 **6156条结构记录**完成初审；当前快照未分析记录为0。材料是已保存的一手帖子摘录、简记及补充，不等于逐字面试录音，也不表示本次重新访问了全部403篇线上原帖。

其中4752条标为提问、314条为独立追问；另外704条仅披露主题、236条背景、94条候选人反问、19条作者推断、4条回答、28条未披露题面、5条无法判定。后两类已经阅读并说明缺失或归属歧义，不通过猜测填满。结构记录可以包含多个实际问题，也可能完全不是问题，因此6156、5066和题目数量不能互换。

模型保留5212个明确提问意图，跨来源归为 **3688个共同回答任务**。同组保留每个来源的具体条件、版本和追问边界；标准问句只表达共同任务，不意味着所有成员逐字等价、所有条件都相同。其中3066组只有1个来源支持，622组得到至少2个来源支持。这是较细粒度、保留长尾约束的模型归并结果，不是唯一标准题库，也不能解释成3688道彼此完全独立的考试题。全量模型初审与重点独立复核分开，未宣称每条都经过双重人工审阅。

每题频数先取来源ID集合：同一来源里的多轮、复述和多个追问，对同一归并题只计一次。主表优先使用 **402个保守证据单位下的覆盖数**，并列403来源ID覆盖数；两者都不是已确认独立招聘流程数，更不是抽样得到的行业面试概率。问题归并、技术域与提问角色由模型阅读决定；代码只核对来源、引用、格式和执行集合计数。

## 优先练习哪些共同任务

下面只列通用知识域，个人项目验真、职业选择和Coding另述。排序按保守证据单位覆盖数；同数按题ID稳定排列，不表示教学先后。代表来源只方便回读，全量支持来源可由逐记录结果和核验命令获得。

| 共同回答任务 | 保守单位数 / 来源数 | 题ID与代表来源 |
| --- | ---: | --- |
| RAG 的完整处理流程及各阶段如何衔接？ | 40 / 40 | RAG-0011 · [S021](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-02.md#L158) |
| Harness是什么，在Agent中承担哪些工程职责？ | 27 / 27 | AGENT-0004 · [S001](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-01.md#L19) |
| Agent运行时需要哪些核心模块，怎样组织协作？ | 25 / 25 | AGENT-0011 · [S003](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-01.md#L60) |
| Agent短期与长期记忆如何划分职责并协作？ | 25 / 25 | AGENT-0014 · [S003](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-01.md#L63) |
| 什么时候采用单Agent，什么时候引入多Agent或Sub-agent？ | 23 / 23 | AGENT-0007 · [S001](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-01.md#L22) |
| 文档分块策略如何设计或选择？ | 22 / 22 | RAG-0078 · [S021](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-02.md#L158) |
| Skill与MCP的职责边界是什么？ | 20 / 20 | AGENT-0068 · [S019](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-02.md#L124) |
| 多个Agent之间怎样通信并传递任务信息？ | 17 / 17 | AGENT-0008 · [S001](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-01.md#L23) |
| 工具调用失败后如何处理和恢复？ | 16 / 16 | AGENT-0012 · [S003](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-01.md#L61) |
| Agent上下文压缩应怎样实现？ | 16 / 16 | AGENT-0057 · [S017](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-02.md#L79) |
| 进程和线程有什么区别？ | 16 / 16 | BACKEND-0008 · [S006](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-01.md#L131) |
| 多路检索结果如何融合？ | 16 / 16 | RAG-0010 · [S018](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-02.md#L102) |
| Agent效果的评估维度、指标与达标标准怎样定义？ | 15 / 15 | AGENT-0354 · [S098](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-06.md#L85) |
| LangChain与LangGraph的定位、机制和适用场景有什么区别？ | 14 / 14 | AGENT-0177 · [S054](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-04.md#L54) |
| Agent消息与上下文如何组织维护？ | 14 / 14 | AGENT-0212 · [S068](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-04.md#L362) |
| 上下文超过可用容量或Token预算时怎样处理？ | 14 / 14 | AGENT-0281 · [S064](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-04.md#L273) |
| 词法检索与向量检索的能力边界如何互补？ | 14 / 14 | RAG-0183 · [S084](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-05.md#L210) |
| 热点缓存失效时如何避免请求压垮后端？ | 14 / 14 | REDIS-0010 · [S013](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-01.md#L315) |
| 如何识别并终止Agent无效循环或重复工具调用？ | 13 / 13 | AGENT-0076 · [S022](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-02.md#L185) |
| Agent相对普通LLM调用或聊天增加了什么能力？ | 13 / 13 | AGENT-0078 · [S022](https://github.com/studyzhige-ui/ai-application-interview-handbook/blob/b7da1d9a91c761b48a27ba951bb01cd33a15ffed/market/interview-experience/01-data/raw/batch-02.md#L187) |

这组结果提示：先把完整请求链路说清楚，再解释状态、失败、成本和效果怎样被控制，比孤立背组件名称更有准备价值。这是基于本语料的教学判断；不能据此省略低频但构成完整模型的基础知识。

## 各域的覆盖与教学深度

来源数表示至少支持该域一个明确归并题的来源ID数；同一来源可以出现在多个域，不能相加当总样本数。归并题数受细粒度与原帖详略影响，不用于比较哪个域更重要。

| 域 | 归并题数 | 支持来源数 |
| --- | ---: | ---: |
| [python](../../../interview/01-python/README.md) | 40 | 28 |
| [fastapi](../../../interview/02-fastapi/README.md) | 5 | 4 |
| [mysql](../../../interview/03-mysql/README.md) | 157 | 94 |
| [redis](../../../interview/04-redis/README.md) | 161 | 110 |
| [backend-engineering](../../../interview/05-backend-engineering/README.md) | 570 | 216 |
| [llm-foundation](../../../interview/06-llm-foundation/README.md) | 204 | 139 |
| [vector-db](../../../interview/07-vector-db/README.md) | 35 | 33 |
| [rag](../../../interview/08-rag/README.md) | 292 | 185 |
| [agent](../../../interview/09-agent/README.md) | 1240 | 338 |
| [system-design](../../../interview/10-system-design/README.md) | 158 | 106 |

以下“考察证据”指保存材料确实支持的任务；“建议深度”是模型据此提出的教学安排。具体来源及官方技术依据在各域备考文档对应题目中，不能把补足的教学内容也算作原帖实问。

- **Python**：考察涉及语言选择、GIL、协程与线程、迭代器/生成器、装饰器和对象行为。建议先建立对象与执行模型，再用并发任务、错误传播和资源关闭检验理解；不要从GIL推导出所有共享状态自动安全，也别把普通CPython与可选free-threaded构建混为一谈。
- **FastAPI**：直接具体题仅来自4个来源，涵盖异步接口、流式返回、依赖/资源和服务实现；样本不足以排列框架内部“高频榜”。建议以一次请求的解析、依赖、处理、响应和清理为最小模型，补齐取消、断连和阻塞I/O等工程前提。备考中的教学补足已标明，不能拿13个教学问题冒充13个真实高频题。
- **MySQL**：索引组织与有效使用、事务隔离/锁、SQL和分页都是可复现的解释任务。建议从一条查询走到执行计划、访问记录与锁范围，保留联合索引缺前列、隔离级别和数据分布等条件；“索引失效”不能一律解释成完全不使用索引，锁超时和死锁也要分别处理。
- **Redis**：缓存失效、并发回填、分布式锁、过期与数据结构经常连接到后端负载。建议先说明缓存与权威数据的关系，再推演热点失效、旧值回填和租约过期后旧持有者继续执行。续租、唯一令牌和fencing解决的问题各有边界，不用一个锁模板回答全部场景。
- **Backend Engineering**：进程/线程、线程池与限并发、网络协议、消息队列和故障处理有明确实问。建议从一次请求、一个任务、一次消息投递建立状态变化，再练习阻塞、背压、取消和重复处理；将协议保证、客户端行为和业务端幂等拆开说明。
- **LLM Foundation**：考察把Transformer/注意力、位置编码、训练与推理、采样、KV Cache和适配方法连到工程成本。建议先有最小前向与生成模型，再讨论长度、批量、显存和质量；KV Cache不是答案缓存，LoRA低秩的是增量，论文版本条件不能省略。
- **Vector DB**：ANN索引、相似度、检索参数与过滤条件需要结合召回/延迟权衡。建议从向量、距离和Top-K查询起步，再解释HNSW/IVF等候选搜索、过滤与索引更新；不同产品的过滤位置、可见性和一致性不能通用化。
- **RAG**：全链路、分块、多路融合和词法/向量互补是重复任务，追问进入表格、更新、权限、引用和失败归因。建议先跑通文档到答案的最小链路，再用坏case拆解召回、排序、上下文和生成；具体Embedding/检索实现深度保留，不能只画流程图。实验选择分块参数不等于每个来源都问了overlap。
- **Agent**：Harness、运行时、记忆、协作、工具失败与评测形成相连任务。建议先建立模型提议动作、宿主验证执行、结果回填的闭环，再讲恢复、授权与停止条件；通用工具调用不强行等同某API的Function Calling，Memory与Context、Skill与MCP也不能只背名称对照。
- **System Design**：多模块状态、容量、可靠性、权限与恢复需要在约束下作选择。建议先明确权威数据、请求路径和成功条件，再推导幂等、超时、观测与补偿；SLI/SLO、RTO/RPO等必要基础作为教学补足清楚标注。频率不能代替前置知识顺序，更不能将某个个人项目经验写成普遍系统设计定律。

## 项目、Coding与行为题如何使用

个人项目域有402个细分任务、270个来源支持。重复较多的是个人职责边界（56）、整体架构与运行链路（46）、真正工程挑战（44）和业务流程/需求（29）。这些是对本人经历的核验，不能用一份虚构项目答案替代。备考应准备真实约束、自己做了什么、测量结果和失败复盘；本轮不增加个人项目板块。

Coding域302组、243个来源，包含算法、实现任务及AI编码实践，不能全称算法题。其中日常怎样使用AI编码工具覆盖41个来源，如何验证生成代码质量覆盖22个来源。明确披露的任务保留；二选一题不把两个选项都计为已实际作答，未披露题面的SQL或场景不补成常见题。职业/行为域116组、82个来源，另有少量通用任务；纯到岗时间、年级、学历和自我介绍等背景不进入技术题频。

## 独立性与敏感性：403和402分别表示什么

S162与S253第二轮的一组不常见问题顺序高度相近。两篇公开帖子作者、显示日期和标题不同，现有证据不足以确认是同一次招聘流程，也不足以判断转载关系。因此完整保留两个来源，仅另外把这一对视作一个相关证据组，计算 **402个保守证据单位**。402不是已核实的独立招聘流程数。其余来源也未因此获得完全独立性的证明。

| 受影响的共同任务 | 按403来源ID | 按402保守单位 |
| --- | ---: | ---: |
| AGENT-0284：多Agent中央协调与平级P2P协作如何取舍？ | 3 | 2 |
| AGENT-0403：LangGraph节点增多时，怎样定义传递State并避免膨胀或OOM？ | 2 | 1 |
| AGENT-0405：工具调用的名称、参数或结构错误怎样校验修复？ | 6 | 5 |
| AGENT-0406：支付等高风险动作应在哪里引入Human-in-the-loop？ | 2 | 1 |
| RAG-0038：跨页或截断表格如何识别修复？ | 3 | 2 |
| RAG-0172：回答差或答非所问时如何区分检索与生成问题？ | 6 | 5 |

两种口径下，上述通用知识域前20项的成员、计数及稳定排序均不变；六个受影响长尾任务可能在同频组之间移动。不要为了一个精确总数而把相似帖子武断合并或删除。

[S162公开页面](https://www.nowcoder.com/feed/main/detail/601233a9e7c54235895bdd09fb449eca)的当前显示日期为05-03，保存材料标题中的月份记录为2026-04；[S253页面](https://www.nowcoder.com/feed/main/detail/73d4714ff5b940c39d69f02d0d7edeea)显示04-24。显示日期没有提供足够依据统一修订全部年份，原材料保持原样。语料还包含明确较早的经历，不能把全部403份称为本月或2026年新面试。来源自选择、作者回忆、摘要详略和岗位分布都会影响覆盖数；缺少某主题的记录，不等于面试官没有问过。

## 文件职责、复核与后续追加

- [questions.json](../01-data/questions.json)：共同任务的标准问句、技术域和归并边界。
- [model-review.json](model-review.json)：每条结构记录的实际判断、理由、原文引文、来源区块哈希及问题映射。同一文件保存本次来源快照与相关组，无需另一套统计副本。
- 本页：解释计数、重点与教学参考。具体机制、回答和辨析只在根目录interview的10域三份资料中展开。

九条旧有限审阅断言的歧义和未披露边界均已逐条纳入本次结果，旧重复结论文件退役。原始材料、来源ID和溯源记录保留。

每日追加只更新原始材料、保全凭证和结构索引；本次完成状态只覆盖固定403来源、6156条记录。新增记录显示为尚未纳入本快照，不伪装已分析，也不使旧快照自动失效。同ID原文或来源区块发生变化则必须报错复核。月度重新阅读增量和既有归并边界后，再同步更新分析与备考资料。

在仓库根目录执行以下离线检查与计数；这些命令不决定语义、不生成备考答案，也不采集网络内容：

```sh
python3 market/interview-experience/04-scripts/verify_interview_data.py --check
python3 market/interview-experience/04-scripts/verify_interview_data.py --statistics
```
