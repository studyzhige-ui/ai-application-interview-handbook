# 10｜Multimodal Foundation：从视觉输入到可验证的多模态系统

> 本章不把多模态讲成“给 LLM 多传一个 image 字段”。目标是建立应用工程层的完整心智模型：**模态输入怎样被编码 → 怎样占用 Context / Compute → 怎样与语言表示对齐 → 什么任务该用 OCR / Parser / Vision → 失败发生在哪一层 → 怎样评估与上线。**

---

## 1. 多模态模型解决什么

纯文本 LLM 的主要输入是 Token。多模态模型把更多信息源纳入同一次推理，例如：

```text
Text
Image
Audio
Video
Document Layout
```

稳定抽象不是某一种具体架构，而是：

```text
Raw Modality
→ Modality-specific preprocessing / encoder
→ Feature / Token Representation
→ Alignment / Projection / Fusion
→ Language-model reasoning space
→ Generation / Structured Output / Tool Decision
```

具体模型可能使用 Projection、Adapter、Cross-Attention、Unified Tokenization 或其它方案；应用工程师要掌握的是**输入怎样变成模型可以联合推理的表示，以及这个过程引入什么成本和 Failure**。

---

## 2. 视觉输入怎样进入语言模型

一个常见直觉：

```text
Image
  ↓
Resize / Tile / Patch
  ↓
Vision Encoder
  ↓
Visual Features
  ↓
Projector / Adapter / Fusion
  ↓
Language Model Hidden Space
  ↓
Reasoning / Generation
```

因此模型不是“直接看像素然后说话”。

这里至少有三个不同层次：

```text
Perception
= 看见了什么

Alignment
= 视觉表示能否进入语言语义空间

Reasoning
= 基于已识别信息能否正确推理
```

这三个层次必须分开排障。

例如模型答错图表问题，不一定是“推理能力差”，也可能最早就把坐标轴、图例或小字识别错了。

---

## 3. Visual Token / Multimodal Budget

视觉输入最终也要占用模型的计算与上下文预算。

高分辨率、多图、长文档截图、长视频通常意味着：

```text
更多视觉单元 / visual tokens
→ 更大 Prefill
→ 更高显存 / Compute
→ 更高延迟和成本
→ 更少空间留给 Text Context / Output
```

所以多模态请求也需要 Budget，而不是无限上传原图。

Production 常需要考虑：

```text
Resolution
Image Count
Crop / Tiling
Frame Sampling
Compression
Page Selection
Max Input Budget
```

重点不是记某个 Provider 的 token 公式，而是理解：

> **输入分辨率和模态数量本身就是 Serving 参数。**

---

## 4. 为什么“整份 PDF 截图全塞模型”通常不稳

假设 200 页 PDF：

```text
200 page images
→ huge multimodal input
→ high prefill / cost
→ relevant evidence 被大量无关页面稀释
```

更合理的系统通常先做：

```text
Parse / OCR / Layout
→ Index / Retrieve relevant pages or regions
→ only selected visual evidence
→ Multimodal Model
```

也就是说：

> **Long Context 同样不能替代 Retrieval；Multimodal Context 也不例外。**

完整检索 Pipeline 在 RAG 模块展开。

---

## 5. OCR / Layout Parser / Direct Vision 的边界

### OCR / Parser 路线

```text
Image / PDF
→ OCR / Layout Parser
→ text / table / blocks / coordinates
→ search / index / LLM
```

优势：

- 文本可检索、可版本化；
- 表格和 Block 可以结构化；
- 更容易 Citation / Audit；
- 可复用，不必每次重新做视觉推理；
- 大规模离线 Ingestion 成本更可控。

### Direct Vision 路线

```text
Image / Screenshot
→ Multimodal Model
```

优势：

- 能利用视觉关系；
- 适合图表、UI、照片、版面；
- 不依赖 OCR 能否完全表达视觉语义。

### 两者组合

企业文档常见更稳的思路是：

```text
OCR / Layout
= searchable representation

Original crop / page image
= visual evidence
```

检索先找到相关文档区域，再决定最终给模型文字、表格结构、原图 Crop，或者同时给。

---

## 6. Layout 为什么是一等信息

文档不是纯字符流。

例如：

```text
标题
左栏
右栏
表头
脚注
图例
页码
```

如果只把 OCR 文本按读取顺序拼起来：

```text
Column A + Column B
→ 语义错位
```

所以 Document Understanding 往往需要：

```text
Text
+ Bounding Box
+ Page
+ Block Type
+ Reading Order
+ Table / Figure Relation
```

这也是为什么 RAG 的 Document Processing 不能只等于 `extract_text()`。

---

## 7. 多模态对齐到底意味着什么

Vision Encoder 输出向量并不自动意味着语言模型能理解它。

模型训练通常要建立：

```text
Visual Representation
↔ Language Semantics
```

可能使用：

- Image-Text Pair；
- Contrastive / Matching Signal；
- Instruction Tuning；
- Multimodal Conversation；
- Preference / Safety Alignment。

应用岗不需要推导训练目标，但要知道：

> **多模态能力来自表示 + 对齐 + 后训练，不是给文本模型随便加图片字段。**

这也解释了为什么两个模型即使都“支持图片”，在 OCR、小物体、Chart、Spatial Reasoning、UI Understanding 上仍可能差异很大。

---

## 8. Multimodal Embedding 与 Multimodal Generative Model

必须区分两个系统角色。

### Multimodal Embedding

目标：

```text
text / image / other modality
→ comparable vector space
```

常见用途：

- Image Search；
- Text-to-Image Retrieval；
- 相似商品 / 素材推荐；
- Multimodal RAG Candidate Retrieval。

### Multimodal Generative Model

目标：

```text
image + text
→ understanding / reasoning / generation
```

常见用途：

- VQA；
- Screenshot / UI Understanding；
- Chart QA；
- Document Reasoning；
- Visual Tool Use。

两者可以组合：

```text
Multimodal Embedding
→ retrieve candidates
→ Multimodal LLM
→ inspect selected evidence
```

但不能把“能做跨模态检索”理解成“就能做复杂视觉推理”。

---

## 9. Audio / Video 为什么比单图再多一层复杂性

Audio / Video 不只是“更多图片”。

它们还有：

```text
Time
Sequence
Speaker / Track
Frame Sampling
Temporal Relation
```

例如 Video QA 需要决定：

```text
每秒抽几帧？
事件发生在什么时间？
相隔 30 秒的两个动作怎样关联？
字幕和画面怎样对齐？
```

Frame 抽太少：可能漏事件。

抽太多：Context / Cost 爆炸。

因此长视频系统常需要：

```text
ASR / Shot Detection / Sampling
→ Temporal Index / Retrieval
→ Selected Segment
→ Multimodal Reasoning
```

而不是把整段视频全部交给模型。

---

## 10. Production Failure 要分层定位

### 10.1 Perception Failure

```text
小字没识别
表格单元格看错
图例颜色混淆
对象漏检
```

### 10.2 Retrieval / Selection Failure

真正相关页面 / Crop 根本没有进入模型。

### 10.3 Alignment / Grounding Failure

模型看到了内容，却把文字与图、图例与曲线、区域与标签对应错。

### 10.4 Reasoning Failure

感知正确，但计算、比较或因果推理错误。

### 10.5 Generation Failure

内部判断可能对，但最终文字、数字单位或结构化输出错误。

排障顺序应该是：

```text
Input / Crop 正确吗？
→ Perception 正确吗？
→ Relevant Evidence 被选中了吗？
→ Grounding 正确吗？
→ Reasoning 正确吗？
→ Output Contract 正确吗？
```

而不是统一归因成“模型幻觉”。

---

## 11. 多模态 Evaluation 应该怎么做

不能只看几张 Demo 图。

Evaluation Set 应覆盖真实分布，例如：

```text
高清 / 模糊
大字 / 小字
表格 / 图表 / 截图 / 照片
多页
中英文混排
旋转 / 裁剪
多图对比
权限敏感图片
```

指标也应拆层：

```text
OCR / Extraction Accuracy
Object / Region Grounding
Chart / Table QA Accuracy
Task Success
Citation / Evidence Correctness
Structured Output Pass Rate
Latency / Cost
```

如果是生产文档问答，还应该保留：

```text
source page
bounding box / crop id
parser version
model version
prompt version
```

这样 Bad Case 才可重放。

---

## 12. 模型 / 路线选型不要只看“支持 Vision”

一个实际决策表可以问：

| 问题 | 影响 |
|---|---|
| 输入主要是照片还是文档？ | Perception 类型不同 |
| 是否大量小字 / 表格？ | OCR / Parser 重要性上升 |
| 是否需要图表关系推理？ | Direct Vision 能力更重要 |
| 是否海量文档？ | Offline Parse + Retrieval 更重要 |
| 是否频繁重复看同一文件？ | 预处理 / Cache 价值更大 |
| 数据能否出域？ | Provider / Privacy Boundary |
| 延迟预算多大？ | 分辨率和多图数量要控制 |

所以 Production 的多模态方案通常是：

> **任务分解 + Pipeline 选型，而不是只问哪个模型 Bench 分数最高。**

---

## 13. Security / Privacy / Data Governance

图片和音视频比纯文本更容易无意携带敏感信息：

```text
PII
屏幕上的 Token / Secret
内部代码
身份证件
人脸
地理位置
背景中的机密内容
```

因此上传第三方 Provider 前要考虑：

- Data Classification；
- Redaction / Crop；
- Tenant Isolation；
- Retention Policy；
- Audit Log；
- Region / Compliance；
- 是否允许模型训练使用数据等 Provider Policy。

模型具备 Vision 能力，不代表系统就获得了读取所有截图的权限。

---

## 14. 多模态与 RAG / Agent 的边界

### RAG 负责

```text
哪些页面 / 图 / 表值得召回？
Evidence 怎样版本化、引用和评估？
```

### LLM Foundation 负责

```text
模型怎样接收视觉表示？
Visual Input 为什么有 Context / Cost？
Multimodal Model 能力边界是什么？
```

### Agent Harness 负责

```text
什么时候调用 screenshot / OCR / vision tool？
Tool Result 怎样进入 Context？
权限、预算和循环怎样控制？
```

不要把这三层混成“多模态 Agent”一个词。

---

## 15. 🎯 30 秒回答

> 多模态模型不是简单的 OCR+LLM。图像、音频或视频通常先经过对应 Encoder / Tokenization，再通过 Projection、Adapter、Cross-Attention 或其它方式与语言表示对齐。应用工程上我会重点管理 visual token 和 Prefill 成本，区分 OCR/Layout 与 Direct Vision，按 perception→retrieval→grounding→reasoning 分层定位错误，并用真实分布的多模态 Eval 验证。大规模文档通常先 Parse/Retrieve 再把少量视觉 Evidence 给模型，而不是整份文件全部塞进去。

---

## 16. ⚠️ 高频易错点

- **“Vision Model = OCR。”** OCR 只是感知 Pipeline 的一种能力。
- **“支持图片的模型都差不多。”** 不同任务的感知与推理能力差异很大。
- **“分辨率越高越好。”** 成本、Context、Latency 都会上升。
- **“整份 PDF 截图塞进去就不需要 RAG。”** 相关证据选择和成本仍是问题。
- **“Multimodal Embedding = Multimodal Chat Model。”** 一个主要用于向量检索，一个用于理解与生成。
- **“答错就是 Reasoning Error。”** 可能最早就是 OCR / Crop / Grounding 错。

---

## 17. 🔍 深挖追问

```text
OCR 与 Direct Vision 怎样做 A/B？
100 页 PDF 怎样控制视觉输入成本？
图表问答怎样构建 Ground Truth？
Multimodal RAG 的 Chunk / Evidence 单位是什么？
视频应该怎样 Sampling？
视觉数据出域时有哪些 Security Boundary？
```

---

<details>
<summary>自测 1：为什么企业 PDF 场景经常同时需要 OCR / Layout Parser 和 Multimodal LLM？</summary>

OCR / Parser 更适合结构化抽取、索引、Citation 和大规模离线处理；Multimodal LLM 更擅长理解图表、版面和视觉关系。两者组合可以先用可检索结构定位 Evidence，再用视觉模型理解难以文本化的部分。
</details>

<details>
<summary>自测 2：模型把图表答案答错时，为什么不能直接说是“推理能力差”？</summary>

因为错误可能发生在页面选择、视觉感知、OCR、图例/坐标 Grounding、最终推理或生成任一层。需要先验证模型实际看到了什么以及识别结果是否正确，再定位 Reasoning。
</details>

<details>
<summary>自测 3：为什么高分辨率和多图输入需要 Budget？</summary>

它们会增加视觉表示数量、Prefill 计算、Context 占用、延迟与费用，也可能挤掉更关键的文本 Evidence，因此需要按任务价值选择页面、区域和分辨率。
</details>
