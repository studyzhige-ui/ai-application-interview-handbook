# Learning Path｜从基础到AI应用的学习路线

[← Handbook](../README.md) · [课程目录](../curriculum/README.md) · [知识地图](knowledge-map.md) · [Coding](../practice/coding/README.md) · [Products](../products/README.md) · [术语表](terminology-glossary.md)

这条路线帮助读者把185个正文章节组织成连续学习和实践。章节数量描述范围，不代表质量验收；学习速度由已经掌握的前置与实际练习结果决定。

## 1. 先修关系决定顺序，目录数字不锁定顺序

[Python](../curriculum/01-python/README.md) → [FastAPI](../curriculum/02-fastapi/README.md) → [MySQL](../curriculum/04-mysql/README.md) → [Redis](../curriculum/05-redis/README.md) → [Backend](../curriculum/03-backend-engineering/README.md) → [Vector DB](../curriculum/06-vector-db/README.md) → [LLM Foundation](../curriculum/07-llm-foundation/README.md) → [RAG](../curriculum/08-rag/README.md) → [Agent](../curriculum/09-agent/README.md) → [System Design](../curriculum/10-system-design/README.md)

这条推荐顺序可在内容演进后继续调整。应保持的是“理解当前概念所必需的知识已经建立”，不是永远不能移动某个模块。

### Backend为何接在MySQL、Redis之后

数据库的事务、唯一约束和条件更新，缓存的数据模型、生命周期与命令原子性，是理解可靠任务、幂等、Outbox和一致性组合的重要基础。先学这些行为，再讨论跨系统如何配合，能避免依赖尚未学过的名词解释名词。

FastAPI阶段先学HTTP边界、依赖、资源、执行和测试。涉及数据库时只说明最小角色，用教学适配器观察，不提前要求读者构造完整生产数据库系统。

### 模块之间仍可有小而明确的桥梁

Vector DB可以先把向量理解为可比较的数值表示，再学习距离和索引。需要了解表示来自哪里时，回看[Embedding输入与输出](../curriculum/07-llm-foundation/docs/09-Embedding与Reranker.md)的编码部分；不把Reranker评测或训练机制变成入门前置。

“提前解释一个必要概念”与“必须提前学完整个模块”不同。未知的关键模型需要建立，特定操作可以使用时就地解释。

## 2. Coding与工具实践并行

```text
Python数据与执行基础 ↔ Coding 01—03：看、写、追踪小程序
                                ↓
Coding 04：完整输入输出 → 05—06：结构、成本与算法
                                ↓
Hot100按已具备前置逐步练习 → 笔试 → 多文件工程任务
```

[Git工具指南](../practice/tooling/git-github-desktop-guide.md)帮助保存和审查这些修改。知识课程不用等全部读完才动手，也不为了尽早刷题省掉必要解释。

[Products](../products/README.md)用于学过相关通用机制之后的源码映射。Agent对应Codex、Claude Code、DeepSeek Harness、DeerFlow等入口仍在产品层；不以源码目录替代课程的阅读依赖。

## 3. 一次学习单元怎样完成

1. 阅读相邻的一小组内容，明确本次要解决的具体问题。
2. 合上正文，复述规则或画出状态变化，找出说不清的一步。
3. 运行或手算例子，改变一个输入，检查预测是否成立。
4. 完成自测，再把错误归为定义、过程、边界或操作问题。
5. 用简短口述表达结论，并能继续解释一个失败情况。

可把一个单元安排为约2.5—3小时：先短时回忆，再读正文和练习，最后自测与记录。这个时间是学习安排示例，不是每篇文章的工作量承诺；复杂实验可以拆成几次，基础薄弱时应减少单元内章节数。

## 4. 三遍学习，各有不同任务

**第一遍建立知识模型。** 核心内容都应有归属和理解，不因面经低频而删掉必要前置；可选的深层实现按任务需要回看，不把接口大全变成第一遍考试。

**第二遍用Review重建。** 从空白图、时间线或小实验开始。答不出来时回具体章节，不机械从头重读整个模块。图、警示和速记是提取理解的辅助，不替代机制。

**第三遍用Interview训练表达。** 真人来源影响复习次数和追问深度，不决定第一次从哪个概念开始。冻结Canonical基线S001—S279的统计由[Interview](../interview/canonical/README.md)维护；路线调整不改变计数和主责归属。

历史基线中，≥10来源、4—9来源、2—3来源和单来源分别对应82、83、37、33个Canonical。可以分别安排更多或更少的口述重复；L4问题应另外训练失败、规模与验证，不因来源少就忽略其必要深度。这是复习建议，不是理解质量分数。

## 5. 13周安排示例

下面保留75个模块学习单元，加2个基础综合回顾与1个全局回顾，共78个单元。每周列6个单元；是否能按周完成取决于时间预算和实践反馈，不要求为了追表而跳过没理解的概念。

<details>
<summary>展开逐周安排：MySQL、Redis已放在Backend之前</summary>

### 第1周

1. Python：01—03。
2. Python：04—05。
3. Python：06—08。
4. Python：09—11。
5. Python：12—13。
6. Python：Review、口述与实验回看。

### 第2周

1. FastAPI：01—03。
2. FastAPI：04—06。
3. FastAPI：07—08。
4. FastAPI：09—11。
5. FastAPI：12—14。
6. FastAPI：15—16。

### 第3周

1. FastAPI：Review与完整接口测试。
2. MySQL：01—03。
3. MySQL：04—06。
4. MySQL：07—09。
5. MySQL：10—12。
6. MySQL：13—15。

### 第4周

1. MySQL：16—18。
2. MySQL：19—21。
3. MySQL：22—23。
4. MySQL：Review与事务实验。
5. Redis：01—03。
6. Redis：04—06。

### 第5周

1. Redis：07—09。
2. Redis：10—12。
3. Redis：13—15。
4. Redis：16—18。
5. Redis：19—21。
6. Redis：22—24。

### 第6周

1. Redis：Review与命令/状态实验。
2. Backend：01—03。
3. Backend：04—06。
4. Backend：07—09。
5. Backend：10—12。
6. Backend：13—15。

### 第7周

1. Backend：16—18。
2. Backend：19—20。
3. Backend：21—22。
4. Backend：Review与故障时间线。
5. 基础综合回顾：Python、接口、事务、缓存和可靠任务。
6. 基础综合追问：资源、超时、重复动作与恢复。

### 第8周

1. Vector DB：01—03。
2. Vector DB：04—06。
3. Vector DB：07—09。
4. Vector DB：10—12。
5. Vector DB：13—16。
6. Vector DB：Review与距离/排名实验。

### 第9周

1. LLM Foundation：01—03。
2. LLM Foundation：04—06。
3. LLM Foundation：07—09。
4. LLM Foundation：10—12。
5. LLM Foundation：13—14。
6. LLM Foundation：Review与小数值推导。

### 第10周

1. RAG：01—03。
2. RAG：04—06。
3. RAG：07—09。
4. RAG：10—12。
5. RAG：13—14。
6. RAG：Review与证据/评测实验。

### 第11周

1. Agent：01—03。
2. Agent：04—06。
3. Agent：07—09。
4. Agent：10—12。
5. Agent：13—15。
6. Agent：16—18。

### 第12周

1. Agent：19—21。
2. Agent：22—24。
3. Agent：Review与执行/恢复时间线。
4. System Design：01—03。
5. System Design：04—06。
6. System Design：07—09。

### 第13周

1. System Design：10—12。
2. System Design：13—15。
3. System Design：16—17。
4. System Design：18—19。
5. System Design：Review与约束/方案验收。
6. 全局回顾：跨模块设计、错误记录与能力迁移。

</details>

正文后续发生章节调整时，应同步这张安排，而不是为了旧编号保留错误顺序。

## 6. 模块收束：能做什么，而不是只读了多少

| 模块 | 至少能完成的回忆与应用 |
|---|---|
| Python | 解释对象与引用、函数执行、数据校验、资源管理与并发，能修改例子并预测结果。 |
| FastAPI | 启动接口，验证请求与响应，解释依赖、资源、执行、流式与取消，提供成功和失败证据。 |
| MySQL | 使用核心SQL，解释索引与执行计划，通过会话实验理解事务、版本和锁，说明日志与扩展边界。 |
| Redis | 根据数据关系选命令，观察TTL与更新，解释缓存、持久、高可用、原子操作和锁的限制。 |
| Backend | 用具体故障推演连接/队列容量、等待预算、幂等、可靠任务与一致性。 |
| Vector DB | 计算小向量排名，区分精确与近似，解释索引、过滤、版本和维护。 |
| LLM | 解释Token、注意力、生成、KV缓存与推理成本，区分提示、检索和训练干预。 |
| RAG | 从原文得到候选、证据、答案与引用，计算小数据集指标并定位失败。 |
| Agent | 从任务推导执行，分清上下文/记忆/状态，说明权限、工具失败、恢复与评测。 |
| System Design | 从需求、容量、状态和数据流导出方案，比较取舍并设计验证。 |

可用“多数自测答对、随机口述能继续解释、能画图并完成一次应用”作为自查。80%自测或4/5口述等阈值只可作个人提醒，不是经过验证的质量门槛。关键前置仍不理解时先回补；已掌握部分可以缩短复习，不机械重学。

## 7. 间隔回看与时间较少时的安排

可以在次日、一周后、约三周后安排简短回忆，并在学习新模块时抽一个旧问题。只记真正混淆的地方，不为每个术语制造卡片。

已有基础者可以采用8周压缩安排：第1周Python与FastAPI，第2周MySQL，第3周Redis，第4周Backend，第5周Vector与LLM，第6周RAG，第7周Agent，第8周System Design与全局回看。它是复习压缩示例，不是保证每天固定时长就能完成全部首次学习。

## 8. 14天面试前回看

这不是入门路线。已经有完整知识模型时，可按如下主题复习：

| 天 | 回看重点 |
|---:|---|
| 1 | Python与FastAPI：执行、输入、资源和流式 |
| 2 | MySQL：SQL、索引、事务与锁 |
| 3 | Redis：缓存、原子操作与高可用 |
| 4 | Backend：等待、重试、幂等、队列和一致性 |
| 5 | Vector：距离、ANN、过滤与生命周期 |
| 6 | LLM：注意力、生成、KV与成本 |
| 7 | RAG：资料、切分、召回与排序 |
| 8 | RAG：评测、归因、权限和更新 |
| 9 | Agent：任务、循环与工具 |
| 10 | Agent：上下文、记忆与恢复 |
| 11 | Agent：权限、协议、协作与评测 |
| 12 | System Design：需求、容量、状态与可靠性 |
| 13 | 综合案例与跨模块追问 |
| 14 | 错误记录、简短回答与薄弱点回看 |

优先回看真实错误，再看高频和高深度问题；不要在最后阶段通过堆新章节制造“学了很多”的错觉。

## 9. 最终验收

能理解知识、闭卷重建、清楚表达、完成编程，并在陌生任务中组合多个模块。没有必要等所有理论结束才进入小型跨模块练习；大型项目与完整源码研读则在相应前置具备后推进。

自动检查、文件计数、历史PASS和绿色测试各有用途，但都不能替代读者对规则、过程和边界的实际理解。路线可以改，证据与前提必须清楚。
