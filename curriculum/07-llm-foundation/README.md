# LLM Foundation｜从模型机制到应用判断

[← Vector DB](../06-vector-db/README.md) · [↑ Handbook 总目录](../../README.md) · [学习路线](../../guide/learning-path.md) · [RAG →](../08-rag/README.md)

本模块解释大语言模型怎样处理输入、生成结果和消耗资源，以及应用工程师怎样据此选择模型、检查输出、改进任务表现。学习目标不是训练一个基础模型，而是遇到答错、变慢、超出上下文、检索效果下降或微调无收益时，能够还原过程，找到应负责的层次。

## 学习前提与模块位置

能够读懂简单的输入、输出、列表与函数，就可以开始阅读。矩阵只用于说明“多少个位置、每个位置多少个数”，相关形状和计算会在使用处解释。正文的三个可运行示例使用 Python 标准库；Python 是便于验算的示例选择，不是模型机制只能用 Python 实现。

课程顺序以 [学习顺序清单](../../guide/learning-order.json) 为准：Python、FastAPI、MySQL、Redis、Backend、Vector DB、LLM Foundation、RAG、Agent、System Design。目录编号是稳定路径，不等于学习次序。

Vector DB 已建立“向量如何比较与检索”的基本模型。本模块第 09 章解释向量由什么模型产生、为什么不能随意混用，并为后续 RAG 的召回与重排提供前提。首次学习不必倒回去先读整套模型训练知识。

## 主线与章节

先沿一次生成理解对象如何变化，再理解服务怎样调度这些计算，最后判断要改变输入、证据、模型参数还是外部执行逻辑。

| 阶段 | 要回答的问题 | 正文章节 |
|---|---|---|
| 输入与计算 | 文本怎样变成模型可计算的表示？ | [01｜模型在 AI 应用中负责什么](docs/01-LLMFoundation在AI应用中的职责.md)<br>[02｜Token、上下文与长文本：先确定模型实际读到了什么](docs/02-TokenContext与LongContext.md)<br>[03｜Transformer 怎样把 Token 序列变成候选分数](docs/03-TransformerBlock.md)<br>[04｜Attention 与位置信息：算一次信息怎样汇入当前位置](docs/04-Attention与Position.md) |
| 生成与服务 | 下一个 Token 怎样产生，时间与显存花在哪里？ | [05｜从候选分数到一段回答：生成与解码](docs/05-Generation与Decoding.md)<br>[06｜KV Cache 与 Prefill、Decode：为什么少算了，却更占显存](docs/06-KVCache与PrefillDecode.md)<br>[07｜模型服务与性能：把等待、吞吐和显存分开判断](docs/07-ServingEngine与性能.md) |
| 模型在系统中的角色 | 怎样选择、调用、组合生成与检索模型？ | [08｜模型 API 与选型：接口调用成功以后，还要验证什么](docs/08-ModelAPI与Selection.md)<br>[09｜Embedding 与 Reranker：一段文字怎样成为可检索的向量](docs/09-Embedding与Reranker.md)<br>[10｜多模态基础：从看见一张图到给出可验证答案](docs/10-MultimodalFoundation.md) |
| 输入与质量 | 怎样描述任务，怎样定位不可靠的回答？ | [11｜Prompt Engineering：把任务写成可检查的输入](docs/11-PromptEngineering.md)<br>[12｜事实错误与干预边界：什么时候改 Prompt，什么时候需要别的机制](docs/12-Hallucination与干预边界.md) |
| 训练的应用边界 | 什么问题值得用数据改变模型，怎样验证收益？ | [13｜SFT 与 LoRA：模型究竟学了什么，少训练哪些参数](docs/13-FineTuning与LoRA.md)<br>[14｜后训练与蒸馏：示范、偏好和奖励分别在教什么](docs/14-PostTraining与Distillation.md) |

## 阅读、验算与复习

第一次顺序阅读正文。每章先理解输入、动作与结果，再独立完成章末任务；答案默认折叠，面试表达直接展示。例子中的订单、价格、容量配置和评测数据均为教学假设，不代表真实生产结果。

第二次进入 [Review：重建机制与综合判断](review/README.md)，尝试不看正文解释新的条件。需要实际验算时，使用 [机制小实验](labs/README.md)：代码直接从正文提取，不另维护一套实现。

表达训练分别使用 [高频面试题](interview/高频面试题.md)、[面试易错点](interview/面试易错点.md) 和 [面试前速查表](interview/面试前速查表.md)。速查材料用于唤起已学知识，不代替第一次阅读。

## 范围与衔接

| 本模块负责 | 需要继续学习的主责模块 |
|---|---|
| Token、Attention、生成、缓存、推理服务的计算与资源边界 | 通用超时、连接、队列、幂等与故障恢复进入 [Backend](../03-backend-engineering/README.md) |
| Embedding、双塔、交叉编码、多模态表示的模型机制 | 向量索引进入 [Vector DB](../06-vector-db/README.md)；检索流水线与证据质量进入 [RAG](../08-rag/README.md) |
| 模型请求、输出检查、Prompt、模型评测与后训练取舍 | 上下文编排、记忆、工具权限、长任务运行和动作验证进入 [Agent](../09-agent/README.md) |

权限与外部动作检查不会因为属于其他模块而被忽略；本模块解释判断输出是否可信所需的最小边界，不展开完整执行系统。

## 技术依据与维护入口

[LLM Foundation References](../../references/llm-foundation/README.md) 按问题组织论文、官方文档及适用版本。教学以因果 Decoder 文本生成和标准全注意力 KV 缓存为主要模型，其他架构在需要处说明差异，不把示意图当成所有模型的统一实现。

[Canonical Questions](../../interview/canonical/llm-foundation.md) 保存正式题目主责和冻结统计；正式面经在 [Market](../../market/README.md)。来源追溯、阅读范围、版本核验和修改稿验收见 [模块维护记录](../../guide/project/llm-foundation-reader-revision-2026-09-27.md)，不以历史 PASS 代替对正文的理解检查。

下一环：[RAG](../08-rag/README.md)。
