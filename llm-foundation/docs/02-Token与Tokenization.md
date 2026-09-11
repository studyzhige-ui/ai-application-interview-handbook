# 02｜Token 与 Tokenization

> 学 LLM 的第一步不是 Attention，而是先搞清楚：**模型真正看到的不是“文字”，而是 Token ID。**

## 1. 先讲人话

人看到：

```text
今天天气很好
```

模型不会直接处理“这句话”，而会先经过 Tokenizer：

```text
Text
  ↓
Tokenizer
  ↓
Token Pieces
  ↓
Token IDs
```

模型真正接收的是整数 ID 序列。

所以：

> 字符数、单词数、汉字数，都不能直接当成 Token 数。

---

## 2. Token 是什么

Token 是 Tokenizer 词表中的一个离散单元。

它可能是：

- 一个完整英文单词；
- 一个词的一部分；
- 一个汉字；
- 多个汉字组成的片段；
- 标点；
- 空格模式；
- 代码片段；
- 特殊控制符。

例如一个英文单词可能被拆成：

```text
unbelievable
→ un + believe + able
```

具体怎样拆，取决于 Tokenizer 和词表。

---

## 3. 为什么不直接按字符或单词

### 纯字符级

优点：词表很小，不会遇到 OOV。

问题：

- 序列太长；
- 单个字符语义太弱；
- Attention 计算成本增加。

### 纯单词级

优点：语义单元直观。

问题：

- 词表巨大；
- 新词、拼写变化、代码、URL 很难覆盖；
- 多语言更复杂。

### Subword

现代 LLM 常使用 subword 思路，在词表大小和序列长度之间折中。

常见家族包括：

```text
BPE
WordPiece
Unigram
SentencePiece-style tokenization
```

应用工程师不需要推导训练算法，但要知道 Token 数由**具体模型 Tokenizer**决定。

---

## 4. Tokenization 为什么直接影响应用工程

### 4.1 Context 占用

Context Window 按 Token 计，不按字符计。

```text
System Prompt
+ User Input
+ History
+ RAG Context
+ Tool Result
+ Generated Output
= Token Budget
```

### 4.2 成本

很多 Model API 的成本和输入 / 输出 Token 数相关。

所以 Prompt 冗长、重复 Tool Result、大段 JSON 都会变成真实成本。

### 4.3 延迟

输入 Token 越多，Prefill 通常越重；输出 Token 越多，Decode 次数越多。

### 4.4 Chunking

RAG 切块常用 Token 而不是字符作为容量约束，因为最终真正进入模型的是 Token。

---

## 5. 特殊 Token

模型输入中可能存在：

```text
BOS
EOS
PAD
role / message separator
special control token
```

不同模型格式不同。

因此不能假设所有 Chat Model 都把：

```text
system / user / assistant
```

直接作为普通字符串拼起来。

Provider 或模型通常会有自己的 Chat Template / Message Serialization。

---

## 6. Tokenizer 与模型必须匹配

模型的 Embedding Matrix 与 Token ID 语义是按训练时词表建立的。

所以：

> 不能随便拿另一个完全不兼容的 Tokenizer 给模型编码，然后期待 Token ID 仍有正确含义。

应用层做 Token Count 时也应尽量使用目标模型对应的 Tokenizer 或 Provider 提供的估算方式。

---

## 7. 中文、英文、代码的 Token 密度不同

不能用一个固定规则说：

> “1 Token = 4 个字符”。

这只能是非常粗糙的特定场景经验。

实际 Token 密度取决于：

- 语言；
- 词表；
- 文本领域；
- 代码 / JSON / URL；
- 空格与标点；
- Tokenizer 版本。

工程上正确做法是实际编码统计。

---

## 8. AI Application 常见 Failure

### Failure 1：按字符切 RAG Chunk

看起来每块 1000 字，但不同内容 Token 数差异大，导致某些 Chunk 远超预期。

### Failure 2：只统计 User Prompt

真实 Context 还包含：

```text
System
History
Retrieved Documents
Tool Results
Output Reserve
```

### Failure 3：忘记输出预算

如果 Context Window 是有限的，输入占满后就没有足够空间生成回答。

---

## 9. 🎯 面试怎么回答

> Token 是模型词表中的离散单元，文本要先被 Tokenizer 编码成 Token ID，模型实际处理的是这些 ID。现代模型通常使用 subword 思路，在词表规模和序列长度之间折中。Tokenization 对应用工程很重要，因为 Context Window、API 成本、Prefill 延迟、RAG Chunk 和输出预算都按 Token 而不是字符来约束。

---

## 10. ⚠️ 易错点

错误：

> 一个汉字就是一个 Token。

更准确：

> 是否一个汉字对应一个 Token 取决于具体 Tokenizer。

错误：

> Tokenizer 只是预处理，不影响系统设计。

实际上它直接影响容量、成本、延迟和切块。

---

## 11. 🔍 继续追问

- BPE 的基本直觉是什么？
- 为什么代码和 JSON 可能 Token 很多？
- Tokenizer 版本变化会不会影响缓存与统计？
- Chat Template 为什么也会消耗 Token？
- 为什么输出 Token 对延迟影响特别明显？

---

<details>
<summary>自测 1：为什么不能用“字符数”严格替代 Token 数？</summary>

因为 Tokenizer 按自己的词表和分词算法编码，同样字符长度的不同语言、代码、JSON 或生僻词可能产生完全不同数量的 Token。

</details>

<details>
<summary>自测 2：RAG Chunk Size 为什么常用 Token 约束？</summary>

因为 Chunk 最终要进入模型 Context，真正消耗模型容量的是 Token；用 Token 才能和 Context Window、输入预算、输出预算统一计算。

</details>
