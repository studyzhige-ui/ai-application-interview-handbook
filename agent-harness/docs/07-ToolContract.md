# 07｜Tool Contract：不只是函数调用

## 1. 初学者版本

```python
def search(query: str) -> str:
    ...
```

## 2. Production Tool Contract

成熟 Tool 需要描述：

```text
identity / version
description
input schema
output schema
permission level
read-only / destructive
concurrency safety
timeout / cancellation
error model
progress
side-effect semantics
```

Claude Code `Tool.ts` 直接能看到 schema、permission context、`isConcurrencySafe`、`isReadOnly`、`isDestructive`、`interruptBehavior` 等概念；Codex 也把 ToolCall / ToolExecutor / ToolOutput 抽成共享边界。

## 3. Tool Description 是模型 API

人写函数名看得懂，不代表模型能正确选择。

差的：

```text
run
```

好的 Tool metadata 应告诉模型：

- 它解决什么问题；
- 什么时候不要用；
- 输入字段语义；
- 结果是什么；
- 关键限制。

Tool quality 本身需要 Eval，而不是凭感觉写 description。

## 4. Tool ≠ Business Function

一个内部函数可能没有权限/超时/幂等契约，不应该直接暴露给模型。

通常需要 Adapter：

```text
Model Tool Contract
→ validation
→ policy
→ domain service
→ normalized result
```

## 🎯 面试

生产 Tool 是 Agent 与真实世界之间的协议，不只是函数。除了 schema，我会定义权限、是否只读/破坏性、并发和取消语义、错误模型、幂等与结果格式，然后用真实任务评测 Tool description 与参数设计是否让模型能稳定使用。

<details><summary>自测：为什么 delete_file 和 read_file 不应只有不同函数名？</summary>

因为它们的风险与运行语义不同：delete 是破坏性副作用，通常要更严格 permission/approval，并且 retry / compensation 语义也不同。
</details>
