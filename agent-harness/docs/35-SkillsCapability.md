# 35｜Skills、Commands 与 Reusable Capability

## 1. 为什么有 Tool 还需要 Skill

Tool 回答：

> 能执行什么动作？

Skill 更像：

> 完成某类任务时，应该按什么程序、用哪些资源和 Tool？

Anthropic Agent Skills 把 instructions、scripts、resources 打成可发现、可加载的能力包。

## 2. Skill 的组成

```text
metadata
instructions
examples
scripts
resources
tool dependencies
```

它可能完全不新增底层 Tool，只教 Agent 怎样组合已有能力。

## 3. Progressive Loading

理想流程：

```text
skill metadata catalog
→ discover relevant skill
→ load instructions/resources
→ execute using tools
```

避免所有 domain guide 永久占 Context。

## 4. Command / Skill / Tool

```text
Command  用户显式触发的交互入口
Skill    可加载程序性知识
Tool     Runtime executable action
```

产品可组合它们，但概念不要混。

## 5. Skill 版本与可信度

Skill 会影响模型行为，也应管理：

- source；
- version；
- permission；
- allowed tools；
- evaluation。

## 🎯 面试

Skill 是可发现、按需加载的程序性能力包，常由 instructions + scripts + resources 组成；Tool 是执行动作，MCP 是连接协议。Skill 的价值是把 domain procedure 外置并 progressive load，而不是不断增大 system prompt。

<details><summary>自测：Skill 一定需要自己的模型吗？</summary>

不需要。它可以由同一个 Agent 加载特定 instructions/resources 后完成任务。
</details>
