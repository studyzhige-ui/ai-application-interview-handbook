# 08｜Tool Schema、Validation 与 Structured Result

## 1. 为什么 Schema 是 Runtime 边界

模型输出 JSON 不是可信程序输入。

```text
Model-generated args
→ Parse
→ Schema Validate
→ Semantic Validate
→ Permission
→ Execute
```

缺一层都可能把 hallucination 变成真实副作用。

## 2. 三种校验

### 结构校验

```json
{"user_id": 123, "amount": 9.9}
```

检查类型、必填字段、enum、长度。

### 语义校验

即使类型合法：

```text
amount = -10
path = ../../secret
```

仍可能非法。

### Policy 校验

参数本身合法，但当前 caller / tenant / run 无权限。

## 3. Structured Result

不要所有 Tool 都返回自由文本：

```json
{
  "status": "not_found",
  "retryable": false,
  "data": null,
  "message": "repository path not found"
}
```

结构化结果更利于：

- 模型判断；
- Runtime retry；
- Trace；
- Eval；
- API versioning。

## 4. Validation Failure 怎样回 Loop

不要默认 crash。可以形成明确 observation：

```text
INVALID_ARGUMENT
field=path
reason=must be inside workspace
```

让模型修正一次；重复失败则触发 loop guard。

## ⚠️ 易错点

- JSON parse 成功 ≠ 参数正确；
- Schema ≠ Permission；
- Pydantic/Zod 校验 ≠ 业务约束；
- 把完整 stack trace 原样塞回 Context 可能泄密且浪费 Token。

## 🎯 面试

Tool args 是模型生成的非可信输入。我会做结构、语义和权限三层验证，并把错误归一化为模型可理解、Runtime 可分类的 structured result，避免一次 hallucinated 参数直接进入真实系统。

<details><summary>自测：为什么 Tool Error 也要有 schema？</summary>

因为 Runtime 需要判断 retryable / non-retryable / approval-required 等语义，模型也需要稳定 observation；纯字符串很难可靠自动处理。
</details>
