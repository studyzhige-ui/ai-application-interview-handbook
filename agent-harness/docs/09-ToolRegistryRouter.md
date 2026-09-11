# 09｜Tool Registry、Router 与 Capability Catalog

## 1. 为什么 Tool 多了以后必须有 Registry

Demo 里可以：

```python
tools = [read, write, search]
```

Production 里可能有几十、几百甚至来自多个 MCP Server 的能力。Runtime 需要一个正式 Catalog：

```text
Tool ID
Name / Version
Description
Schema
Source
Permission metadata
Availability
Tags / Search hint
```

## 2. Registry 与 Router

```text
Registry：系统有哪些能力？
Router：这次 Tool Call 应交给哪个 executor？
```

不要混成一个 dict。

### 注册阶段

- built-in tools；
- MCP tools；
- plugin tools；
- tenant-specific tools；
- dynamically discovered tools。

### 调用阶段

```text
tool_name + version
→ resolve
→ policy check
→ executor
```

## 3. 重名与版本

外部 MCP Server 可能都暴露 `search`。

应考虑：

```text
namespace/tool
server + tool
stable ID
version
```

否则 Trace 和 replay 不知道当时实际执行哪个实现。

## 4. 动态 Availability

Tool 注册过不代表此刻可用：

- credential 过期；
- MCP server offline；
- tenant 没授权；
- environment 没启动。

所以 Catalog 需要区分“存在”和“当前可执行”。

## 🎯 面试

Registry 管能力元数据和身份，Router 把模型的 Tool Call 映射到具体 executor。工具规模变大后还要处理 namespace、version、availability 和 tenant 权限，否则 Tool Call 无法稳定重放和审计。

<details><summary>自测：为什么 Tool 名称不能作为唯一持久化 ID？</summary>

名称会改、会重名、会由不同 Server 提供。可恢复系统需要稳定身份与版本，才能知道历史 Call 对应哪个实现。
</details>
