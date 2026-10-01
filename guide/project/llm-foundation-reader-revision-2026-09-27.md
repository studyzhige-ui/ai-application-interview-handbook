# LLM Foundation｜Reader-first 系统优化记录

日期：2026-09-27。基线及发布前回读的 main：`41c42937c720517781cf29bd61566260766d7729`。

**审查阶段状态（历史快照）：先形成修改稿并完成本地验收；用户随后于同日追加授权创建 commit、PR 并合并 main。实际发布对象以 GitHub commit / PR / main 历史为准。正文与配套已落稿；不将本轮验收扩大为全仓库或全部历史面经验收。**

## 1. 范围、基线和实际阅读

- 连续阅读目标模块原有全部 14 篇正文、README、Review 及 3 份 Interview；独立工作目录保存修改稿，保持原路径与 14 章规模。基线 Blob SHA 见交付包 baseline.json。
- 阅读根 README、现行 writing guide、Curriculum 入口、学习路线与知识地图；学习路线尾部分段回读，未宣称每一行全库导航验收。读取 guide/learning-order.json 作为现行顺序权威源。
- 质量参照实际读取 practice/coding/README.md、docs/01-programming-fundamentals.md 的 1–220 行和 docs/09-ai-coding.md 全文。继承先对象、再动作、再结果的写法，没有套固定代码比例或章节数。
- 前后衔接读取 Vector DB 与 RAG 入口，并全文读取 Vector DB 的 02-VectorSpace与Similarity、RAG 的 08-Rerank与CandidateBudget。其他模块正文只读不改，不宣称相邻模块全部验收。
- 对应 References 原本没有 LLM 目录，目标模块没有 labs；读取 References 总入口并增加本模块索引与教学实验。
- 维护核对读取目标模块最近 3 次提交记录、content-depth-audit、integration-status 和导航生成器。历史 PASS 没有当作本轮内容通过；未核定上一次完整 LLM 逐段审查时间，因此没有声称已穷尽“自那次审查起的所有来源差异”。
- 面经检索读取 Market 入口、两份准入政策、LLM Frozen Canonical 23 项、证据矩阵至 LLM 完整段及追问链文档可见前半部分；检索结果与正式回读范围见第 3 节。

## 2. 保留、精修与补充

保留 14 章认知主线、原路径和模块分工。没有跨模块迁移正文；新增只为补足机制、实验与本模块维护。正文中的面经叙事与过时版本状态不承担教学依据；追溯集中在本记录和 Interview。

| 章 | 原有判断 | 本轮处理 |
|---|---|---|
| 01 | 职责和工程边界值得保留，但术语先于过程；存在“后面 28 章”旧引用 | 用订单 A 错误承诺串起模型、服务、应用三主体，建立数据流与归因；移除失效数量引用 |
| 02 | Token、窗口与长文本限制已涉及，但预算和模板边界不够可操作 | 补教学 BPE 合并过程、最终序列计数、8192 Token 完整预算及追加工具结果；区分容量、能力与应用记忆 |
| 03 | 结构组件齐全，矩阵对象和残差路径缺乏逐步解释 | 用 3×4 隐藏状态到 3×6 logits 建立形状；保留结构图并补两条残差连线、训练标签移位和 FFN 上下文来源 |
| 04 | QKV、位置和复杂度已有结论，缺一次能核算的注意力过程 | 补点积、缩放、因果屏蔽、Softmax、加权 V 的数值过程；说明整行屏蔽、MHA/GQA/MQA、RoPE 相对位置与 FlashAttention 边界 |
| 05 | 生成与采样参数偏描述，易混淆依赖、一次前向和流式传输 | 加入稳定 Softmax 函数、温度分布、Top-k/Top-p 候选变化、结束分支、流分片与 Token 区别；补推测解码的限定解释 |
| 06 | 已有缓存与两阶段概念，缺精确时间线和容量对象 | 从 Prefill 得首 Token，按新 Token 输入解释 cache 何时增长；补普通全注意力 KV 公式、1 GiB 例算、前缀复用和取消释放条件 |
| 07 | 服务组件与指标已有覆盖，但数值口径和版本默认值需落地 | 以异长请求说明连续批处理，补分页尾块与量化对象；固定 vLLM 0.30.0 V1 默认重算与可选卸载；计算 TTFT/TPOT/完成时间 |
| 08 | 模型选型和 API 要点有效，成功条件与评测方法过简 | 拆响应、终止、结构、事实及动作检查；补能力探测、任务保留集、成对评价偏差、单位成功任务成本 |
| 09 | 双塔和 Cross-Encoder 分工应保留，但 Token 到段落向量有断层 | 补带 Padding 掩码的池化与归一化算例、对比训练与难负例、联合评分和表示版本；不重写 ANN 或 RAG 调度 |
| 10 | 原有感知—对应—推理排障、检索与隐私边界值得保留 | 围绕 100→120 万图表增长加入可复核对象，保留版面/坐标、OCR 与直接视觉、跨模态检索、音视频时间对应和风险 |
| 11 | 已有 Prompt/Context 分工，缺完整可检验输入和正常/异常分支 | 加入订单完整 Prompt 与结果、缺值/缺编号/冲突区别、Few-shot 与回归对照；不把提示词当授权 |
| 12 | 干预边界合理，归因与指标缺完整条件 | 增加事实性/忠实性、引用支持、未知与澄清区别、拒答分母和节点与任务成功；修正新稿自测的联合样本可行性 |
| 13 | LoRA 与微调角色应保留，参数节省结论缺机制台阶 | 补 SFT 标签移位与计损失位置、梯度/优化器最小模型、矩阵形状/参数量/初始化、训练数据分组与适配器回滚 |
| 14 | 方法比较有效，易变成算法名词清单 | 从示范、偏好、奖励区分反馈，补标准 DPO 相对参考策略目标、GRPO 组内例算、奖励漏洞和分布/序列蒸馏边界 |

Review 由按组件记忆转为重建计算、缓存、检索与干预关系，包含新条件下的手算和诊断；Interview 保留 23 项现行主责的表达入口，新增情境不重新计频。正文代码通过命名标记成为 labs 的单一实现来源，不维护两份函数。

## 3. 面经校准覆盖层次

**层次 A：当前正式库索引与检索。** 基线 Market 为 35 个 Batch、S001–S297，冻结 Canonical 仍采用 S001–S279。实际全仓库检索词族包括 Prompt、Embedding、KV，以及 Transformer 的正式 Batch 路径搜索。一个多词 AND 查询命中很少，未被当作覆盖证明。检索可以定位候选，但没有证明全 297 条已逐段阅读，也不保证所有同义表述全部召回。

**层次 B：正式条目上下文回读。** 完整回读 S001–S006、S271–S274、S275–S297，共 33 个正式编号的已收录问题与上下文。Batch01 只回读这些明确条目，不宣称整批历史备注全读；Batch25 的四个正式条目已读，尾部观察不计覆盖。Batch26–35 的正式条目已读，部分批次历史统计或排除列表尾部没有连续回读。S288 追加二面仍属于同一来源。

**层次 C：外部原帖重新核验。** 本轮没有重新核验候选人外部原帖。使用的是仓库正式收录上下文，不把历史“原帖已核验”改写成本轮结果。

**证据验收尚有限制：** 尚未把冻结 23 项所引用的所有旧正式来源逐个回读，也未逐一回读检索命中的其他旧条目。因此下面的 Canonical 表是现行问题—机制—正文去向表，不是“该题所有独立来源全文已经核验”的承诺。需要以全部相关旧来源的逐项回读作为严格全量证据验收的后续门槛；本稿不标全量 Evidence PASS。

### 3.1 冻结问题的机制去向（不修改 Canonical）

| QID / 原问法摘要 | 抽象机制 | 必要前置 | 正文主要位置 | 原解释及本轮处理 |
|---|---|---|---|---|
| LLM-001：为什么用 Token 而不是字符/单词 | 词表与子词、模型—分词器匹配 | 01 | [第 02 章](../../curriculum/06-llm-foundation/docs/02-TokenContext与LongContext.md) | 原有概念保留；补合并过程和计数边界 |
| LLM-002：Context Window 怎样影响应用设计 | 最终序列与输入/输出预算 | 01–02 | [第 02 章](../../curriculum/06-llm-foundation/docs/02-TokenContext与LongContext.md) | 补完整预算与多轮增长 |
| LLM-003：Lost in the Middle、长上下文是否代替 RAG | 容量与信息利用、受控位置实验 | 02 | [第 02 章](../../curriculum/06-llm-foundation/docs/02-TokenContext与LongContext.md) | 保留，限定论文条件并补验证方法 |
| LLM-004：自回归生成怎样进行 | 条件依赖、logits、采样与终止 | 03–04 | [第 05 章](../../curriculum/06-llm-foundation/docs/05-Generation与Decoding.md) | 加深，区分推测解码与逐步依赖 |
| LLM-005：Transformer 各组件怎样协作 | Embedding、Attention、FFN、归一化与残差 | 02 | [第 03 章](../../curriculum/06-llm-foundation/docs/03-TransformerBlock.md) | 加深对象、形状与跳连 |
| LLM-006：Q/K/V 和 Attention 怎样计算 | 投影、点积、Softmax、加权和 | 03 | [第 04 章](../../curriculum/06-llm-foundation/docs/04-Attention与Position.md) | 补数值过程、未来掩码和失败条件 |
| LLM-007：为什么需要多头 | 不同投影与拼接，共享 K/V 的结构差异 | 03–04 | [第 04 章](../../curriculum/06-llm-foundation/docs/04-Attention与Position.md) | 保留并补尺寸与非人工角色边界 |
| LLM-008：FFN 有什么作用 | 逐位置非线性加工、已含上下文的隐藏状态 | 03 | [第 03 章](../../curriculum/06-llm-foundation/docs/03-TransformerBlock.md) | 补 4→12→4 过程 |
| LLM-009：位置编码与 RoPE 原理 | 旋转后点积依赖位置差 | 04 | [第 04 章](../../curriculum/06-llm-foundation/docs/04-Attention与Position.md) | 补相对位置等式；未交付完整张量手写训练营 |
| LLM-010：多模态怎样输入与融合 | 视觉表示、对齐、预算与证据定位 | 03/09 | [第 10 章](../../curriculum/06-llm-foundation/docs/10-MultimodalFoundation.md) | 保留原有分层排障，补图表与坐标案例 |
| LLM-011：KV 为什么加速，怎样影响并发 | 因果前缀不变、缓存形状和容量 | 04–05 | [第 06 章](../../curriculum/06-llm-foundation/docs/06-KVCache与PrefillDecode.md) | 补时间线、字节单位和结构适用条件 |
| LLM-012：Prefill 和 Decode 差别 | 已知前缀批量处理、首 Token 与后续依赖 | 05–06 | [第 06 章](../../curriculum/06-llm-foundation/docs/06-KVCache与PrefillDecode.md) | 明确首 Token 从 Prefill 末位置得分采样 |
| LLM-013：推理引擎、分页和调度怎样选 | 异长请求、KV 分页、抢占、精度和负载 | 06 | [第 07 章](../../curriculum/06-llm-foundation/docs/07-ServingEngine与性能.md) | 补尾块与固定版本语义；真实引擎未运行 |
| LLM-014：怎样度量推理延迟 | 测量起止、Token 与流分片、分位数 | 05–07 | [第 07 章](../../curriculum/06-llm-foundation/docs/07-ServingEngine与性能.md) | 补时间轴与 TPOT 不适用条件 |
| LLM-015：Temperature、Top-p 等怎样影响输出 | 重标定分数、截断候选与重新归一化 | 04–05 | [第 05 章](../../curriculum/06-llm-foundation/docs/05-Generation与Decoding.md) | 补分布计算与错误输入验证 |
| LLM-016：模型 API 应怎样抽象 | 消息语义、能力差异、结果与业务检查 | 01/05 | [第 08 章](../../curriculum/06-llm-foundation/docs/08-ModelAPI与Selection.md) | 补可见成功层级与安全边界 |
| LLM-017：模型选型依据什么 | 真实任务、独立评测、成本质量延迟 | 07–08 | [第 08 章](../../curriculum/06-llm-foundation/docs/08-ModelAPI与Selection.md) | 补成对比较偏差和单位成功任务成本 |
| LLM-018：Embedding 模型怎样生成与训练 | Token 表示、池化、对比学习、空间版本 | 03；可先读09桥梁 | [第 09 章](../../curriculum/06-llm-foundation/docs/09-Embedding与Reranker.md) | 补池化算例与难负样本 |
| LLM-019：Embedding 与 Reranker 差别 | 独立编码与联合交互、候选上限 | 09 | [第 09 章](../../curriculum/06-llm-foundation/docs/09-Embedding与Reranker.md) | 保留主线，补输入截断/校准条件 |
| LLM-020：何时微调，LoRA 为什么省参数 | 任务目标、梯度、冻结权重与低秩增量 | 12 | [第 13 章](../../curriculum/06-llm-foundation/docs/13-FineTuning与LoRA.md) | 补样本监督、初始化和资源边界 |
| LLM-021：SFT/PPO/DPO/GRPO 与蒸馏 | 示范、偏好、奖励、参考策略及教师信号 | 13 | [第 14 章](../../curriculum/06-llm-foundation/docs/14-PostTraining与Distillation.md) | 补机制而非逐算法新增章节 |
| LLM-022：幻觉怎样归因与干预 | 证据来源、进入请求、支持关系与真实结果 | 08/11 | [第 12 章](../../curriculum/06-llm-foundation/docs/12-Hallucination与干预边界.md) | 加深分层归因、误拒分母与验证 |
| LLM-023：怎样优化 Prompt | 完整任务、条件分支、示例和回归 | 08 | [第 11 章](../../curriculum/06-llm-foundation/docs/11-PromptEngineering.md) | 补完整输入与可核验对照 |

### 3.2 已回读正式来源逐项去向

同一条目有多组追问时按同一机制合并记录，避免逐问新增章节。下表归其他模块的内容没有在接收模块改写，也没有宣称已由其补齐。

| 来源与正式位置 | 原有问题或连续追问 | 机制去向、保留与处理 |
|---|---|---|
| [S001](../../market/interviews/batch-01.md) | 工具数量增长、按需发现与可靠 Loop | 02/11 的输入压力是最小前提；完整发现、权限与循环交回 Agent，未改该模块 |
| [S002](../../market/interviews/batch-01.md) | ASR/隐私→Tokenization→QKV→长窗口→SFT/PPO/DPO/GRPO | 02–04、10、14；补模型机制，不把 ASR 服务或训练 Infra 搬入本模块 |
| [S003](../../market/interviews/batch-01.md) | 超时恢复、压缩信息损失、Prompt 优化、幻觉与 Token 异常 | 02、11、12；确定性恢复与记忆归 Agent/Backend |
| [S004](../../market/interviews/batch-01.md) | 不同基础模型适配，实际用户/流量下扩容 | 07–08；讲能力与负载评测，不把来源场景数值写成课程实测 |
| [S005](../../market/interviews/batch-01.md) | 数据库优化验真、指标与 AI Coding | 无独立 LLM 缺口；不据此扩写模型章节，去向 Backend/Practice |
| [S006](../../market/interviews/batch-01.md) | Transformer、多头、RAG 生成、Memory | 03–04 机制加深；检索流程和记忆分别属 RAG/Agent |
| [S271](../../market/interviews/batch-25.md) | Agent 招聘池中的 React Hook、版本号与前端基础 | 无本模块新增；保留正式岗位上下文，不把所有 Agent 面试题都归 LLM |
| [S272](../../market/interviews/batch-25.md) | Embedding 训练、BGE 精排、GraphRAG、多模态 Schema、带 Mask 的 MHA 与 RoPE 手写 | 04、09、10；机制与手算已补。GraphRAG 归 RAG；完整张量手写 MHA/RoPE 实验未交付，建议 Practice 承接，未声称接收模块已补齐 |
| [S273](../../market/interviews/batch-25.md) | AI 后台的压测、热点、数据库与网络 | 无本模块新增；不把应用岗通用基础改写成 LLM 内容 |
| [S274](../../market/interviews/batch-25.md) | Agent Bad Case/Eval、Tool Result 过长、Tool List 膨胀 | 02、08、11、12；机制最小前提补齐，完整生命周期仍归 Agent |
| [S275](../../market/interviews/batch-26.md) | 文件内容、长窗口、上下文与 RAG 方案 | 02/09；按实际输入预算解释，完整文件解析与检索归 RAG |
| [S276](../../market/interviews/batch-26.md) | 模型选型与恶意请求、输入数据、队列和 Memory 连问 | 08/11/12；模型能力与输入权限分开，队列恢复归 Backend |
| [S277](../../market/interviews/batch-26.md) | 同流程多轮中的模型选择、Prompt、RAG 评测与上下文 | 02/08/11/12；补对照与归因，不新增来源数 |
| [S278](../../market/interviews/batch-26.md) | 目标岗的后端基础问题 | 未发现需要新增的 LLM 机制；维持原归属 |
| [S279](../../market/interviews/batch-26.md) | Agent 工程实践与浏览器扩展/表单任务 | 不把不使用 LLM 的确定性练习包装为模型实验；Practice/Agent 承接 |
| [S280](../../market/interviews/batch-27.md) | 路由、幻觉、外部动作、回归条件和工具规模 | 01/02/05/08/11/12；完整停止/恢复/审批仍属 Agent |
| [S281](../../market/interviews/batch-27.md) | Memory、知识库与 Agent 基础 | 02/11 提供最小桥梁；无独立 LLM 新章 |
| [S282](../../market/interviews/batch-27.md) | AI Coding 成果验真与工程基础 | 08 的任务评价原则可复用；代码工作流仍归 Practice |
| [S283](../../market/interviews/batch-27.md) | 长任务中的幻觉、自评置信度与人工确认 | 12 的校准和证据分支加深；持久任务执行归 Agent |
| [S284](../../market/interviews/batch-27.md) | 图像编辑模型选择、Elo 成对比较、测试集代表性、Prompt、80% 压缩阈值 | 02/08/10/11；补评价偏差与阈值需实测，不采纳固定万能百分比 |
| [S285](../../market/interviews/batch-27.md) | 查询授权、导出、崩溃与 Redis | 11 明确 Prompt 不授权；其余 Backend/Agent，未改正文 |
| [S286](../../market/interviews/batch-27.md) | 社区检索、RAG 评价与项目验真 | 08/12 最小评价模型，召回流水线归 RAG |
| [S287](../../market/interviews/batch-28.md) | 滑动窗口大小、Summary 切换、Context Compression 与 Harness | 02 预算、11 上下文分工；压缩正确性和恢复归 Agent |
| [S288](../../market/interviews/batch-29.md) | 一面 Schema 跨字段约束、Review Agent 幻觉；9.21 二面新增读写权限与长任务 | 08/11/12；回读同条目追加轮次及 Batch33 扩展，不分配新 ID |
| [S289](../../market/interviews/batch-30.md) | RAG 低召回、异构 PDF、原文 MPC 和 Function Calling | 09/10；不替原帖把 MPC 自动改成 MCP，未据这个拼写新增协议解释 |
| [S290](../../market/interviews/batch-31.md) | Multi-Agent 必要性、真实准确率与同事反馈 | 08/12；评价定义与独立结果，架构必要性归 Agent |
| [S291](../../market/interviews/batch-31.md) | Function Call/Tool/MCP、RAG、Linux、算法 | 08 只保留模型工具请求的最小边界；其余归原模块 |
| [S292](../../market/interviews/batch-32.md) | 10 万 QPS 商品详情、缓存更新、最长回文 | 本模块无新增；Backend/Redis/Practice，不因岗位叫 Agent 扩写 LLM |
| [S293](../../market/interviews/batch-32.md) | Skill 不遵守限制、提升规则优先级、视频 OOM 与端到端性能 | 11 规则不等于授权，10 模态预算；视频上传、恢复和清理归 Backend |
| [S294](../../market/interviews/batch-33.md) | AI 全栈的系统与 AI Q&A 综合设计 | 08 可复用能力和评价框架；没有新增模型机制，完整设计归 System Design |
| [S295](../../market/interviews/batch-33.md) | 知识质量、节点 Gate、效率稳定性；多约一分钟换 20–30pp 的条件题 | 08/12；指标必须定义且共同评价，此数值明确是面试假设而非实测收益 |
| [S296](../../market/interviews/batch-34.md) | 大量 Skill/MCP 的发现与上下文压力，无框架压缩/Memory | 02/11 最小前提；Agent 负责真正状态与发现生命周期 |
| [S297](../../market/interviews/batch-35.md) | 每个节点怎样定义准确率，代码质量与事实准确率怎样区分 | 08/12；补节点评价与端到端成功，语法通过不等于业务正确 |

## 4. 技术版本与事实证据

检索日期为 2026-09-27。公开稳定发布核对 Hugging Face Transformers v5.17.0 与 vLLM v0.30.0；排除预发布，不宣称二者存在此处未经证明的 LTS 承诺。前者用于分词、模板、生成与缓存文档示例，后者用于引擎实现边界。经典 Attention、RoPE、LoRA、DPO、GRPO 与蒸馏分别依据原始论文。托管 API 能力按具体接口说明，不与开源库参数混用。

官方事实和新例子分开：vLLM V1 默认 RECOMPUTE 与可选卸载属于版本事实；KV 1 GiB、分页尾块、订单样本和质量成本数字均为明确假设下的教学计算，不是真实 GPU、服务或训练结果。所有技术索引见 [本模块 References](../../references/llm-foundation/README.md)。

## 5. 内容、运行、呈现与整合验证

### 内容检查

连续沿 14 篇修改后正文检查前置、对象和推导，并将章末与 Review 从主线检查材料中剥离；再次核对正文能否支持新条件推导。修复了 Schema、Q/K、Sigmoid、微调权重等先用后讲，以及训练 Padding 不应当作有效上下文的表述。检查具体任务与答案的共同可行性，修复拒答自测样本数约束。

新条件检查包括禁止位置的 V 改大但输出不变、不同层数/头数/长度的 KV 容量、输出 1 Token 的 TPOT 边界、不同输入图表/坐标变换、旧文档向量与新查询模型不兼容、格式与事实指标不能独立相乘、不同词表的教师文本不是逐 Token 分布蒸馏。它们是内容与数值验证，不证明每位初学者均已理解；最终读者体验仍需实际阅读。

### 实际运行

Python 3.13.5 执行教学实验的 21 项 unittest；源码片段来自正文，检查 Softmax、KV、LoRA 的正常/异常输入及数值关系。AST 额外使用 Python 3.10 语法规则解析，但这不等于在 Python 3.10 解释器运行。完整原始日志随包交付。

**没有执行：** Transformers/vLLM 安装与真实模型加载、GPU 并发推理、完整 Tokenizer/模板集成、远端 Model API、真实多模态输入、SFT/LoRA/GRPO 训练、服务故障注入、跨系统集成与生产验证。没有拿模拟对象替代真实服务并记 PASS。

### 呈现与局部整合

最终结果由随包 validation 中的实际检查记录提供：包含修改稿链接与锚点、默认折叠、导航、渲染和截图检查。HTML 是本地 Chromium 阅读预览，不是 GitHub 实际桌面或移动页面验收。其他模块链接需要根据已读取的真实仓库路径核对；未取得目标锚点内容时不记通过。

章数和路径未变，因此不对根入口与知识地图的章节统计做加减。共享文件只给 references/README.md 加一行本模块入口，并用新鲜回读的原内容验证 Blob SHA；没有整份旧快照挂到新父提交。未运行会修改所有模块的导航生成器，也没有放宽公共测试。

## 6. 保护范围、冲突与未完成项

- 发布前 main 与基线相同，未发现审查开始与发布前回读之间的远端提交冲突；本次发布分支从该基线创建，不覆盖其他模块的新提交。
- 本轮不含其他模块正文、market 原始证据、来源准入规则、Frozen Canonical、Source Count、题目主责或历史统计的改动；不创建或恢复 research/ 目录。
- 根入口和部分既有维护页存在早期学习顺序表达，当前权威顺序以 learning-order.json 为准。只使本模块入口匹配现行顺序，不把本轮描述为全仓库顺序修复。
- S272 完整张量手写 MHA/RoPE 实验、全部相关旧面经回读、真实引擎与训练验证未完成，不能以算术测试或文档关键词出现替代。
- 发布流程使用独立分支，并在 PR 创建前比较基线、分支与变更文件范围；commit、PR、合并与最终 main 的具体标识以 GitHub 历史和本轮最终发布报告为准。

## 7. 交付前补充检查结果

本地 Chromium 实际渲染了 22 个阅读条目；6 张图按 Mermaid 文本中的节点、标签和连线用 Graphviz 布局为 SVG，2 个公式由本地 KaTeX 输出 MathML。检查桌面 1365 像素和移动 390 像素视口、折叠开启/关闭及默认闭合。原生 Mermaid 库因本环境依赖不完整没有通过执行，不能将上述 SVG 转换记作 GitHub 原生 Mermaid 验收；浏览器本地 HTTP 导航受限后使用内存文档渲染，没有更改浏览器策略。

截图检查发现并修复了中文术语括号与相邻文字导致加粗标记失效的问题，并给 details 内的 Markdown 增加空行，避免答案中的行内代码被当作普通文字。正文 Block 图改为纵向以完整呈现两条残差；宽图允许区域内横向滚动。

交付辅助工具另有 6 项临时 Git fixture 测试：正常生成不改 clone、拒绝本地目标脏修改、拒绝 HEAD 中目标并发修改、允许其他文件的提交、拒绝稿件校验和漂移、新文件补丁。它们不是目标仓库 CI 或真正整合后的补丁应用测试。未运行全仓库测试和全部外部 URL 可用性检查。
