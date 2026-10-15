# LLM Foundation｜理解模型输入、注意力、生成、推理成本与模型适配

[← AI Backend Engineering](../05-backend-engineering/README.md) · [课程目录](../README.md) · [Handbook](../../README.md) · [Vector Database →](../07-vector-db/README.md)

先沿一次生成理解 Token、计算与解码，再学习推理服务、Embedding、Reranker、输入质量与训练边界。

## 学习前提与目标

能够读懂函数与列表即可进入；必要的向量、矩阵与概率模型在正文首次使用处解释。

学完后应能理解模型输入、注意力、生成、推理成本与模型适配。

## 学习顺序

1. [01｜模型在 AI 应用中负责什么](docs/01-LLMFoundation在AI应用中的职责.md)
2. [02｜Token、上下文与长文本：先确定模型实际读到了什么](docs/02-TokenContext与LongContext.md)
3. [03｜Transformer 怎样把 Token 序列变成候选分数](docs/03-TransformerBlock.md)
4. [04｜Attention 与位置信息：算一次信息怎样汇入当前位置](docs/04-Attention与Position.md)
5. [05｜从候选分数到一段回答：生成与解码](docs/05-Generation与Decoding.md)
6. [06｜KV Cache 与 Prefill、Decode：为什么少算了，却更占显存](docs/06-KVCache与PrefillDecode.md)
7. [07｜模型服务与性能：把等待、吞吐和显存分开判断](docs/07-ServingEngine与性能.md)
8. [08｜模型 API 与选型：接口调用成功以后，还要验证什么](docs/08-ModelAPI与Selection.md)
9. [09｜Embedding 与 Reranker：一段文字怎样成为可检索的向量](docs/09-Embedding与Reranker.md)
10. [10｜多模态基础：从看见一张图到给出可验证答案](docs/10-MultimodalFoundation.md)
11. [11｜Prompt Engineering：把任务写成可检查的输入](docs/11-PromptEngineering.md)
12. [12｜事实错误与干预边界：什么时候改 Prompt，什么时候需要别的机制](docs/12-Hallucination与干预边界.md)
13. [13｜SFT 与 LoRA：模型究竟学了什么，少训练哪些参数](docs/13-FineTuning与LoRA.md)
14. [14｜后训练与蒸馏：示范、偏好和奖励分别在教什么](docs/14-PostTraining与Distillation.md)

## 学习与面试

首次学习沿 docs 的完整主线理解输入、状态变化、结果与失败边界；完成每章后，使用章末总结与自测检查是否能独立解释和推导。

面试准备集中在 [本知识域](../../interview/06-llm-foundation/README.md)：[高频面试题](../../interview/06-llm-foundation/01-高频面试题.md)、[易混易错点](../../interview/06-llm-foundation/02-易混易错点.md)与[面试速查](../../interview/06-llm-foundation/03-面试速查.md)。正文负责完整模型，面试材料负责回答、追问与快速回忆。

技术事实以正文引用的官方资料及适用范围为依据；[Market](../../market/README.md)中的真实岗位与面试材料用于校准学习深度，不能代替技术证明。
