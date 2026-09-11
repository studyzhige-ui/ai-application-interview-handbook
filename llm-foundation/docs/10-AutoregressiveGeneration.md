# 10｜Autoregressive Generation

## 1. 先讲人话

LLM 生成一句话，不是一次性把整句“想出来”。

典型 Decoder-only LLM 做的是：

```text
已有 Token
  ↓
预测下一个 Token
  ↓
把新 Token 拼回输入
  ↓
再预测下一个
  ↓
重复
```

这就是 Autoregressive Generation。

---

## 2. Next-token Prediction

给定前缀：

```text
今天天气很
```

模型输出对整个词表的概率分布：

```text
好      0.42
热      0.18
冷      0.11
不错    ...
...
```

Decoding 策略选出一个 Token，例如“好”。

新的上下文变成：

```text
今天天气很好
```

然后模型继续预测。

---

## 3. 为什么输出是串行依赖

第 t+1 个 Token 的输入包含第 t 个 Token。

因此：

```text
Token 1
  ↓
Token 2
  ↓
Token 3
  ↓
...
```

不能像训练阶段那样完全并行地一次产生所有未来 Token。

这就是为什么生成很长答案时，Decode Latency 会持续累积。

---

## 4. Training 和 Inference 的区别直觉

### Training

已知完整目标序列，可以用 Causal Mask 同时计算多个位置的 next-token loss。

### Inference

未来 Token 不存在，只能生成一个再继续。

所以：

> Transformer 训练可以高度并行，但自回归生成仍是逐 Token 的。

---

## 5. Stop Condition

生成不会无限进行，常见停止方式：

- 生成 EOS；
- 命中特定 Stop Sequence；
- 达到 Max Output Tokens；
- Provider / Runtime 主动取消；
- Structured Output 完成。

应用层必须有硬上限，不能完全依赖模型“自己知道什么时候停”。

---

## 6. Streaming 为什么自然

因为 Token 是逐步产生的，所以服务可以：

```text
Decode Token
→ 立即发送给 Client
→ 再 Decode 下一个
```

这就形成 Streaming Chat。

Streaming 改善的是用户**感知延迟**，不一定减少总生成时间。

---

## 7. 为什么 KV Cache 很重要

如果每生成一个新 Token，都重新计算整个历史前缀：

```text
第 1 次：算 1000 Token
第 2 次：算 1001 Token
第 3 次：算 1002 Token
...
```

大量历史 Attention 计算会重复。

KV Cache 就是为了解决这个问题，后面单独展开。

---

## 8. 应用工程影响

### Output 长度决定延迟

输出 50 Token 和 2000 Token 的 Decode 次数完全不同。

### Tool Call 也属于生成结果

模型生成结构化 Tool Call，仍然经过 token generation / structured decoding，只是最终解析成调用意图。

### Cancellation 很重要

用户关闭页面后，如果 Backend 不取消上游生成，模型仍可能继续消耗算力与费用。

---

## 9. 🎯 面试怎么回答

> Decoder-only LLM 通常以自回归方式生成：给定已有 Token 计算下一个 Token 的概率分布，Decoding 选出 Token 后把它追加回上下文，再继续生成。因为每个新 Token 依赖前面的已生成 Token，所以 Decode 天然有串行依赖，这也是长输出延迟高、KV Cache 和 Streaming 非常重要的原因。

---

## 10. ⚠️ 易错点

错误：

> Transformer 可以并行，所以生成整段文字也是完全并行的。

错误：

> Streaming 能显著减少模型总计算量。

Streaming 主要降低首批内容等待和改善体验，不自动减少总 Decode 工作。

---

<details>
<summary>自测：为什么生成 1000 个 Token 往往比输入多 1000 个 Token 更明显地增加用户等待？</summary>

因为输出 Token 需要逐步 Decode，每个新 Token 依赖前一个生成结果；输入 Token 主要集中在 Prefill 阶段，可以进行更大规模并行矩阵计算。

</details>
