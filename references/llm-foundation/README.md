# LLM Foundation｜模型机制与应用边界的技术依据

[← References](../README.md) · [课程入口](../../curriculum/07-llm-foundation/README.md)

本索引按读者要核对的问题组织技术证据。论文说明机制或特定实验，库文档说明对应实现，托管接口说明对应产品行为；三者不相互替代。实际教学例子的数值、订单、价格和评测样本均为作者构造的可验算假设，不是论文或生产系统的实测结果。

## 适用基线

| 对象 | 教学使用范围 | 版本与核验边界 |
|---|---|---|
| 通用模型机制 | 因果 Decoder 文本生成；标准全注意力 KV 缓存 | 这是主要解释模型，不代表 Encoder、滑窗注意力、MLA、状态空间模型和所有多模态架构 |
| Hugging Face Transformers | 消息模板、生成与缓存的实现例证 | 以核验的稳定发布 [v5.17.0](https://github.com/huggingface/transformers/releases/tag/v5.17.0) 为课程文档基线；不以 `main` 或预发布功能代表稳定版 |
| vLLM | V1 推理调度、分页缓存、资源与默认值 | 以核验的稳定发布 [v0.30.0](https://github.com/vllm-project/vllm/releases/tag/v0.30.0) 为课程文档基线；不把 V0 的默认行为推广到 V1 |
| 托管 Model API | 以公开文档说明完成、拒绝、结构化输出与 Prompt 边界 | 文档核验日期为 2026-09-27；接口、模型能力与客户端支持分别核对，不据此保证所有 Provider 一致 |
| Python 验算 | 三个正文函数与标准库测试 | 语法目标为 Python 3.10+；实际运行版本、检查结果与未验证项见模块维护记录 |

稳定发布不等于厂商声明的长期支持版本；这里不自行赋予 LTS 身份。课程没有训练或部署 Transformers/vLLM 模型，因此这些是技术文档基线，不是“实测环境版本”。浮动托管模型别名也不能当成固定权重版本。

## 输入如何形成可计算的序列

| 要核对的问题 | 主要来源 | 使用时注意 |
|---|---|---|
| BPE 的词表学习与按合并规则编码有什么区别 | [Hugging Face：Byte-Pair Encoding](https://huggingface.co/learn/llm-course/chapter6/5) | 正文用的是小型虚构合并规则，不声称复现某个商业模型 Tokenizer |
| 对话角色如何转成具体 Token 模板 | [Transformers 5.17.0：Chat templates](https://huggingface.co/docs/transformers/v5.17.0/en/chat_templating) | 模板必须与模型配套，角色名称不能自动证明模型如何理解优先级 |
| Token 计数、输入与输出预算为什么依赖模型 | [OpenAI：Understanding and counting tokens](https://help.openai.com/en/articles/4936856-understanding-and-counting-tokens) | 精确限制、推理 Token 和缓存计费按实际模型接口核对；不使用固定中英文字符换算比做容量保证 |
| 长输入中的位置敏感性如何评估 | [Lost in the Middle](https://arxiv.org/abs/2307.03172) | 论文观察有模型与任务条件，不把它改写成“任何模型都无法读取中间信息” |

## 表示、Attention 与生成

| 要核对的问题 | 主要来源 | 使用时注意 |
|---|---|---|
| Q/K/V、缩放、Mask、FFN、多头与残差 | [Attention Is All You Need](https://arxiv.org/html/1706.03762v7) | 原论文图与现代 Pre-Norm 模型并非同一归一化顺序；正文明确区分 |
| RMSNorm 与 LayerNorm 的差别 | [Root Mean Square Layer Normalization](https://arxiv.org/abs/1910.07467) | 归一化对象不是词表概率，不与 softmax 混淆 |
| RoPE 怎样引入位置关系 | [RoFormer](https://arxiv.org/abs/2104.09864) | 理解旋转点积的相对位置结构，不据此承诺无限外推 |
| Greedy、Sampling、Beam 等生成策略 | [Transformers 5.17.0：Generation strategies](https://huggingface.co/docs/transformers/v5.17.0/en/generation_strategies) | 默认值可能来自具体模型配置，不把库文档的一组缺省值当成所有托管 API 的默认值 |
| 为什么一次验证能接受多个候选 Token | [Fast Inference from Transformers via Speculative Decoding](https://arxiv.org/abs/2211.17192) | 经典方法在条件满足时保持目标分布；不把这一结论推广到所有近似实现、硬件逐位复现或固定加速比 |

## KV、调度与显存

| 要核对的问题 | 主要来源 | 使用时注意 |
|---|---|---|
| 增量生成怎样复用缓存 | [Transformers 5.17.0：Caching](https://huggingface.co/docs/transformers/v5.17.0/en/cache_explanation) | 缓存类型、模型架构、滑窗与具体实现会改变容量和行为 |
| KV Head 为什么可能比查询 Head 少 | [GQA: Training Generalized Multi-Query Transformer Models](https://arxiv.org/abs/2305.13245) | GQA/MQA 是架构及训练条件，不是事后免费修改原模型头数 |
| KV 逻辑位置为什么可以映射到物理块 | [PagedAttention](https://arxiv.org/abs/2309.06180) | 分块组织需要相应访问实现，仍存在尾块、元数据与容量上限 |
| 注意力计算如何减少内存读写 | [FlashAttention](https://arxiv.org/abs/2205.14135) | 精确注意力的 IO 优化不等于把全部位置两两关系改成稀疏或线性结构 |
| V1 抢占、Chunked Prefill 与负载取舍 | [vLLM 0.30.0：Optimization and Tuning](https://docs.vllm.ai/en/v0.30.0/configuration/optimization/) | 重点核对默认抢占方式为 RECOMPUTE、支持条件下的 Chunked Prefill；可选卸载能力不等于默认抢占行为 |

正文中的 KV 公式是根据明确的张量形状推导的**原始缓存字节数**，不是引用一个“真实部署总显存”数字。延迟公式是声明测量口径后的计算关系，不把网络分片、首 Token 和完成事件视为同一事件。

## 模型调用、检索与多模态

| 要核对的问题 | 主要来源 | 使用时注意 |
|---|---|---|
| JSON 模式与 Schema 约束有什么差异 | [OpenAI：Structured Outputs](https://developers.openai.com/api/docs/guides/structured-outputs) | 拒绝和不完整输出需要独立处理；格式符合不证明业务事实正确，也不授予外部操作权限 |
| Prompt 怎样表达任务与示例 | [OpenAI：Prompt engineering](https://developers.openai.com/api/docs/guides/prompt-engineering) | 以其为具体接口示例，不把托管产品特性说成模型通用机制 |
| 句向量怎样从 Token 表示形成 | [Sentence Transformers：Custom Models](https://www.sbert.net/docs/sentence_transformer/usage/custom_models.html)、[Sentence-BERT](https://arxiv.org/abs/1908.10084) | 池化、投影与归一化须符合训练约定；不机械地对所有模型使用均值池化 |
| 双塔与交叉编码怎样分工 | [Sentence Transformers：Cross-Encoders](https://www.sbert.net/examples/cross_encoder/applications/README.html) | 联合评分的成本与质量需在任务上验证，不代表每个 Reranker 都是同一种结构 |
| 图像表示怎样与语言联合使用 | [Visual Instruction Tuning / LLaVA](https://arxiv.org/abs/2304.08485) | 是代表性架构和训练证据，不代表所有多模态模型实现相同 |
| 跨模态检索空间从哪里来 | [CLIP](https://arxiv.org/abs/2103.00020) | 跨模态相似性检索不等于复杂视觉推理能力 |
| 模型评审可能有哪些系统性偏差 | [Judging LLM-as-a-Judge with MT-Bench and Chatbot Arena](https://arxiv.org/abs/2306.05685) | 成对偏好、顺序和长度偏差要与业务事实校验区分；正文的比较示例不是某个平台真实评分 |

## 微调、偏好优化与蒸馏

| 要核对的问题 | 主要来源 | 使用时注意 |
|---|---|---|
| 低秩增量、参数量与初始化 | [LoRA](https://arxiv.org/html/2106.09685) | 正文按标准增量形式推导；参数量比例不是总训练显存比例 |
| 冻结量化基础权重如何参与微调 | [QLoRA](https://arxiv.org/abs/2305.14314)、[PEFT：Quantization](https://huggingface.co/docs/peft/en/developer_guides/quantization) | 仅用于机制和边界；未提供绑定某个 PEFT 运行版本的训练脚本 |
| RLHF 背景及 DPO 的相对偏好目标 | [Direct Preference Optimization](https://arxiv.org/html/2305.18290) | 偏好对、参考策略与数据假设不能省略；标注偏好不等于事实真值 |
| GRPO 为什么用组内相对奖励 | [DeepSeekMath](https://arxiv.org/html/2402.03300v3) | 组内标准化数值只是教学演算；实际更新还涉及策略比率、约束等条件 |
| 教师分布能如何向目标模型迁移 | [Distilling the Knowledge in a Neural Network](https://arxiv.org/abs/1503.02531) | 原始分布蒸馏与仅使用教师文本的路线要区分；拿不到 logits 时不能假装已获得教师概率 |

## 验证和来源追溯

[模块维护记录](../../guide/project/llm-foundation-reader-revision-2026-09-27.md) 区分技术核验、源材料回读、示例运行与尚未验证的环境。[正文小实验](../../curriculum/07-llm-foundation/labs/README.md) 不访问外部模型。真人面经仍以 [Market](../../market/README.md) 为正式证据层，不用这些技术文档增加来源数或改变冻结题目统计。

## 补充核验：量化与换出

- [PyTorch torchao：Quantization-Aware Training](https://docs.pytorch.org/ao/stable/workflows/qat.html)：用于第 07 章区分 PTQ 与 QAT 的训练时机和量化误差模拟，不作为已运行训练的证据。
- [vLLM 0.30.0：KV Offloading](https://docs.vllm.ai/en/v0.30.0/features/kv_offloading_usage/) 与 [CacheConfig](https://docs.vllm.ai/en/v0.30.0/api/vllm/config/cache/)：用于区分可选换出能力与 V1 默认重算语义，不给出未经执行的性能收益。

- [Transformers 5.17.0 生成处理器](https://huggingface.co/docs/transformers/v5.17.0/en/internal/generation_utils) 和 [Chat Completions 参数](https://developers.openai.com/api/reference/resources/chat/subresources/completions/methods/create)：用于区分重复惩罚、频率惩罚和存在惩罚的语义，不把一家的处理顺序或参数支持推广给其他接口。
