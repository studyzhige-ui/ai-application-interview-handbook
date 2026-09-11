# 11｜Tool Failure、Timeout 与 Retry

## 1. 先分类失败

不要统一 `except Exception: retry()`。

```text
Invalid Input        通常先让模型修参
Permission Denied    需要授权/换方案
Not Found            可能搜索其它路径
Timeout              可能 retry / cancel
Rate Limited         backoff
Transient Network    retry
Permanent Business   不应 retry
Partial Success      最危险
```

## 2. Retry 的三个条件

只有同时满足才适合自动 retry：

1. 错误是 transient；
2. 操作可安全重放；
3. 预算允许。

否则 Retry 可能把“小故障”变成“双重副作用”。

## 3. Timeout 不是 Error Message

要区分：

```text
model timeout
tool timeout
process timeout
run deadline
```

一个子 Tool 超时不一定要杀整个 Run。

## 4. Failure 如何给模型

推荐给模型稳定、有限的信息：

```json
{
  "code":"RATE_LIMITED",
  "retryable":true,
  "retry_after_ms":1500
}
```

Runtime 可以自己 retry，也可以把 failure 作为 observation 让模型改计划。

## 5. Loop Failure

Tool 连续失败 N 次时：

```text
same call retry
→ alternative tool / plan
→ ask human
→ terminate
```

不能无限“再试一次”。

## 🎯 面试

Tool Failure 我会先按输入、权限、暂态、永久和 partial success 分类。Retry 需要同时考虑 retryability 和 idempotency，并受 deadline / budget / max-attempt 约束；连续失败要进入 loop guard 或 replan，而不是无限重试。

<details><summary>自测：HTTP 500 一定能 Retry 吗？</summary>

不一定。服务端可能已执行副作用但响应失败。必须知道操作是否幂等或有 idempotency key。
</details>
