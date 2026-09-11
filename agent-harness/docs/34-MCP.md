# 34｜MCP：Host / Client / Server / Tool / Resource / Prompt

## 1. MCP 解决什么

MCP 是连接 AI Host 与外部能力/Context 的标准协议，不是 Agent Framework。

基本角色：

```text
Host
└─ MCP Client
   ↔ MCP Server
```

## 2. 三类 Server Primitive

官方规范区分：

```text
Prompts    用户控制的模板/指令入口
Resources  应用控制的 Context 数据
Tools      模型控制的可执行能力
```

这个控制边界非常重要。

## 3. MCP Tool 仍要走 Runtime Policy

外部 Server 声明了 Tool，不代表模型可以无条件执行：

```text
MCP catalog
→ local capability normalization
→ permission / approval
→ execute
→ result normalization
```

Codex 源码的 MCP catalog、Hook MCP handler，以及 Claude Code MCP connection 都体现了“协议接入后仍进入产品 Runtime”。

## 4. MCP ≠ Skill

```text
MCP   连接外部 server / data / tool 的协议
Skill 程序性知识、资源、脚本的可发现包
Tool  一次可执行能力
```

## 5. 安全

需要考虑：

- server trust；
- Tool schema 变化；
- credentials；
- data exfiltration；
- approval；
- tenant scope。

## 🎯 面试

MCP 是 Host-Client-Server 协议层，标准化 Tools/Resources/Prompts 接入。它不等于 Agent Loop；MCP Tool 进入 Host 后仍要经过本地 Registry、Permission、Approval、Sandbox 和 Trace。

<details><summary>自测：MCP Resource 和 Tool 最大区别是什么？</summary>

Resource 主要提供 Context 数据，控制更偏 Host/Application；Tool 是模型可请求执行的动作，涉及更强副作用与权限语义。
</details>
