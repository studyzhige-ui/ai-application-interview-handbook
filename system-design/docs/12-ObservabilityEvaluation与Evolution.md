# 12｜Observability、Evaluation、Cost 与 Evolution

系统设计最后一环不是“架构图画完”，而是：

> **上线后怎样知道它有没有达到目标、坏在哪、花了多少钱，以及怎样安全地继续演进。**

---

## 1. Observability 不等于“有日志”

至少要有三类信号：

```text
Metrics
Logs
Trace
```

它们分别回答：

```text
系统整体怎么样？
某个事件发生了什么？
一次请求跨组件经历了什么？
```

---

# 2. Golden Signals

常见可以从：

```text
Latency
Traffic
Errors
Saturation
```

建立基础服务视图。

但 AI 系统还需要质量信号。

---

# 3. Stage-level Trace

一个 RAG 请求：

```text
API
→ Query Rewrite
→ Retrieval
→ Rerank
→ LLM
```

如果只记录：

```text
request = 3.2s
```

不知道慢在哪里。

更好：

```text
rewrite=100ms
retrieval=80ms
rerank=700ms
llm_ttft=1.4s
decode=900ms
```

System Design 需要按关键阶段切 Span。

---

# 4. Metric 必须有合适维度

AI Gateway 总 P99 正常，但：

```text
model=A   P99 500ms
model=B   P99 12s
```

如果只看总平均会被掩盖。

常见维度：

```text
route
model
tenant
tool
shard
region
error_type
```

但 Label Cardinality 过高也会增加监控成本。

---

# 5. SLO 与 Alert

Alert 不应该是：

```text
CPU > 80% 就报警
```

更应该围绕用户可见问题：

```text
SLO burn rate
error rate
P99
queue age
freshness lag
failed task rate
```

CPU 是原因候选，不一定是用户问题本身。

---

# 6. Evaluation 是 AI 系统的“功能正确性监控”

传统系统可能：

```text
200 OK
```

就算接口成功。

但 AI 系统：

```text
HTTP 200
但答案错了
```

仍然失败。

所以还需要：

```text
Task Success
Faithfulness
Retrieval Recall
Tool Accuracy
Schema Pass Rate
Human Escalation Rate
```

这就是为什么 Evaluation 必须进入 System Design，而不是模型团队的附录。

---

# 7. Online 与 Offline Evaluation

## Offline

```text
固定 Dataset
→ Regression
→ Baseline Comparison
```

适合发布前。

## Online

```text
A/B
User Feedback
Outcome Metric
Production Sample Review
```

适合验证真实流量。

两者需要结合。

---

# 8. Cost Model

系统成本不只是机器。

AI Application 常包括：

```text
LLM input/output token
Embedding
Rerank
Vector storage
GPU
Object storage
Network egress
Queue / Worker
Observability
```

所以最好建立：

```text
cost / request
cost / tenant
cost / successful outcome
```

而不是只看月度总账单。

---

# 9. Cost 与 Architecture Trade-off

例如：

```text
Rerank Top100
```

可能质量更高，但：

```text
Latency ↑
Cost ↑
```

需要实验找：

```text
Top20 vs Top50 vs Top100
```

的 Pareto Point。

同理：

```text
large model for all requests
```

可能被：

```text
routing + small model + fallback
```

替代。

---

# 10. Version 是 Observability 的一部分

Trace 最好记录：

```text
service_version
model_version
prompt_version
index_generation
schema_version
feature_flag
```

否则发布后 Quality 下降，无法知道哪次变更导致。

---

# 11. Safe Rollout

新版本不要默认：

```text
100% traffic immediately
```

可以：

```text
shadow
canary
1%
10%
50%
100%
```

同时观察：

```text
error
latency
quality
cost
```

AI Pipeline 更应该做 Regression / Canary，因为模型和 Prompt 行为变化不总是类型系统能发现。

---

# 12. Data / Index Migration

Schema / Embedding / Index 升级常需要：

```text
build new generation
→ backfill
→ delta catch-up
→ validate
→ switch read pointer
→ rollback window
→ cleanup old
```

而不是在线原地改完就祈祷。

---

# 13. Capacity Feedback Loop

生产系统应形成：

```text
Measure
→ Forecast
→ Load Test
→ Capacity Plan
→ Deploy
→ Measure Again
```

Google SRE 也强调不要把过去的容量比率永久当事实，代码和流量会变化。

---

# 14. Incident 后要转成系统改进

例如一次 Queue 堆积事故：

不要只说：

```text
扩容了
```

还应问：

```text
为什么没提前看到？
为什么 Admission Control 没生效？
Retry 是否放大？
Alert 是否太晚？
能否自动降级？
```

Observability 的价值是让系统可学习。

---

# 15. 🎯 面试怎么答

> 我会把 Observability 和 Evaluation 当成架构本身的一部分。传统指标看 latency、traffic、error、saturation，AI 系统还要看 retrieval/tool/task quality。Trace 会记录 stage latency 和 model/prompt/index/version，方便 Bad Case Replay。成本会归一到 request/tenant/outcome。上线采用 canary + regression，数据或索引升级用 new generation + validation + cutover + rollback，而不是直接原地替换。

---

# 16. 本章自测

<details><summary>1. 为什么 AI API 返回 200 仍可能算失败？</summary>
因为模型可能给出错误、无依据或工具执行失败但被包装成正常文本，所以需要质量和任务成功指标。
</details>

<details><summary>2. 为什么 Trace 要记录 Prompt / Model / Index Version？</summary>
AI 输出高度依赖这些版本，没有版本无法复现 Bad Case，也无法把质量回归归因到具体变更。
</details>

<details><summary>3. 为什么 Migration 常用 new generation 而不是原地更新？</summary>
这样可以独立构建、校验、灰度切换并保留回滚窗口，降低半更新状态的风险。
</details>
