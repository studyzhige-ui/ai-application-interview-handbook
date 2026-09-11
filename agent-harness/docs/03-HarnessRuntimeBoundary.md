# 03｜Harness / Runtime 与 Model 的边界

## 1. 为什么要分边界

面试中常见错误是把模型能力和工程能力混成一句：“模型会记忆、会用工具、会恢复”。

实际上：

```text
Model
- 接收当前输入
- 预测输出 / Tool Call
- 本身不知道数据库事务是否提交

Harness
- 构建输入
- 维护状态
- 执行 Tool
- 决定权限
- 记录结果
- 处理失败与恢复
```

## 2. 四层系统

Anthropic 在 trustworthy agents 的框架中把 Model、Harness、Tools、Environment 分开看，是很有用的工程抽象：

```text
Model       决策能力
Harness     控制与约束
Tools       可调用动作
Environment 动作真正发生的地方
```

## 3. 例子：删除文件

模型输出：

```json
{"tool":"delete_file","path":"config.prod"}
```

之后的关键问题都不属于“模型推理”：

1. JSON 合法吗？
2. Tool 存在吗？
3. 该路径允许吗？
4. 是否 destructive？
5. 要人工批准吗？
6. Sandbox 能访问吗？
7. 删除成功了吗？
8. Result 怎样回填？
9. Trace 怎样记录？

这就是 Harness Boundary。

## 4. 为什么边界要稳定

模型会升级、Provider 会替换，但 Tool execution、Permission、Session、Trace 等产品责任不能每次跟着重写。

成熟架构倾向把：

```text
Brain / Model
Hands / Execution
Session / Durable State
```

解耦，使它们可以独立扩展和失败恢复。

## 🎯 面试 30 秒

Model 决定“下一步想做什么”；Harness 决定“模型当前看到什么、这个动作是否允许、怎样执行、结果如何回到 Loop、失败如何恢复”。把这两层分开后，模型可以迭代，Runtime 的状态、安全和执行契约仍保持稳定。

<details><summary>自测：Tool schema 属于 Model 还是 Harness？</summary>

schema 会作为上下文提供给模型，但 schema 的注册、版本、参数校验和执行契约属于 Harness / Tool Runtime。
</details>
