# 30｜Guardrails 与 Runtime Validation

## 1. Guardrail 放在哪里

不是只有“输入敏感词检查”。

OpenAI Agents SDK 官方区分：

```text
Input Guardrail
Tool Input Guardrail
Tool Output Guardrail
Output Guardrail
```

这对应不同 Runtime lifecycle boundary。

## 2. Validation vs Guardrail

```text
Schema Validation  数据是否合法
Policy Guardrail   行为是否允许 / 安全
Quality Guardrail  输出是否满足质量约束
```

例如邮箱格式合法，不代表允许给该地址发送客户数据。

## 3. Fail Closed vs Fail Open

高风险安全 guardrail 自身故障时通常应该 fail closed；低风险格式检查可以降级。必须显式决定。

## 4. Guardrail 不是万能防线

它不能替代：

- sandbox；
- IAM；
- tenant isolation；
- idempotency；
- output verification。

## 5. Parallel Guardrail

某些低成本检查可与模型运行并行以降低延迟，但若它决定是否允许昂贵/危险动作，就要确保时序不会让副作用先发生。

## 🎯 面试

Guardrail 是挂在输入、Tool、输出等生命周期边界的校验/策略层。我会区分 schema、policy 和 quality guardrail，并根据风险决定 fail-open/fail-closed；它是 defense-in-depth 的一层，不替代真实权限和 Sandbox。

<details><summary>自测：Output Guardrail 能防止已经执行的危险 Tool 吗？</summary>

不能。到最终输出时副作用可能早已发生，高风险控制必须在 Tool 执行前。
</details>
