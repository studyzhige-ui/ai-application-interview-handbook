# 10｜Multimodal Foundation

## 1. 多模态模型解决什么

纯文本 LLM 的输入主要是 Token。

多模态模型希望把：

```text
Text
Image
Audio
Video
Document Layout
```

映射到可以共同参与推理的表示空间。

应用层真正需要理解的是：

> 不同模态先由各自 Encoder 提取表示，再通过 Projection / Adapter / Cross-Attention / Unified Tokenization 等方式和语言模型对齐。

具体架构会因模型而不同。

---

## 2. 视觉输入怎样进入语言模型

一种典型直觉：

```text
Image
  ↓
Vision Encoder
  ↓
Visual Features
  ↓
Projector / Adapter
  ↓
Language Model Hidden Space
  ↓
LLM Reasoning / Generation
```

所以模型并不是“直接看像素然后说话”。

---

## 3. Visual Token

图像通常会被分成 Patch 或其它视觉单元，再形成一组向量表示。

这些表示最终会占用模型的输入容量。

因此高分辨率、多图、长视频可能带来：

- 更多 Visual Tokens；
- 更高 Prefill；
- 更高成本；
- 更大 Context 压力。

所以多模态输入也要做 Budget。

---

## 4. OCR 和 Visual Understanding 不一样

图片里有文字时，系统可能：

```text
直接交给 Multimodal LLM
```

也可能：

```text
OCR / Layout Parser
→ Structured Text
→ LLM
```

两种路线的特点不同。

### OCR / Parser

优点：

- 可检索；
- 可索引；
- 可审计；
- 成本可控。

### Direct Vision

优点：

- 能理解图像结构；
- 不只依赖文字；
- 适合图表、UI、照片。

企业文档 RAG 常常两者结合。

---

## 5. 多模态对齐

真正难点不是“让 Vision Encoder 输出向量”，而是：

> 让视觉表示与语言模型的语义空间产生可用对齐。

训练可能包含：

- Image-Text Pair；
- Contrastive Objective；
- Instruction Tuning；
- Multimodal Conversation；
- Preference / Safety Alignment。

应用岗重点理解：

> 模型多模态能力来自训练与对齐，不是给纯文本模型随便加一个图片字段就获得。

---

## 6. Multimodal Embedding 与 Multimodal LLM

也要区分：

### Multimodal Embedding

目标：

```text
image / text
→ comparable vectors
```

用于：

- 图片检索；
- 跨模态检索；
- 推荐。

### Multimodal Generative Model

目标：

```text
image + text
→ reasoning / generation
```

用于：

- VQA；
- Screenshot Understanding；
- Chart QA；
- Document Understanding。

两者不是一个任务。

---

## 7. Failure Case

### 7.1 小字 / Dense Document

直接视觉理解可能漏字或结构错。

### 7.2 多图 Context 太大

Visual Token 暴涨。

### 7.3 图表语义误读

模型可能识别出数字，却误解坐标轴或单位。

### 7.4 权限与隐私

图片可能包含：

- PII；
- Screenshot Secret；
- 内部代码；
- 身份信息。

上传外部 Provider 前要做安全治理。

---

## 8. 多模态与 RAG

多模态 RAG 可能包含：

```text
PDF
├─ Text
├─ Table
├─ Image
└─ Layout
```

后续需要决定：

- 存原图还是 OCR 文本；
- 用 Text Embedding 还是 Multimodal Embedding；
- Retriever 召回什么单位；
- 最终给 LLM 文本还是图片。

完整 Pipeline 归 RAG 模块。

---

## 9. 🎯 面试怎么回答

> 多模态模型的核心不是“LLM 直接读取图片”，而是先把图像、音频等模态编码成表示，再通过 Projection、Adapter、Cross-Attention 或统一 Token 等方式与语言模型对齐。应用工程上要关注 Visual Token 带来的 Context / Cost、OCR 与直接视觉理解的边界、跨模态 Embedding 与生成模型的区别，以及文档场景中的隐私和检索策略。

---

## 10. ⚠️ 易错点

错误：

> 多模态模型就是 OCR + LLM。

OCR 只是其中一种输入处理路线。

错误：

> Multimodal Embedding 和 Multimodal Chat Model 是一回事。

目标和 Serving 方式都不同。

---

<details>
<summary>自测：为什么企业 PDF 场景经常同时需要 OCR / Layout Parser 和 Multimodal LLM？</summary>

OCR / Parser 更适合结构化抽取、索引和检索；Multimodal LLM 更擅长理解图表、版面和视觉关系。两者结合通常比只依赖其中一个更稳定。

</details>
