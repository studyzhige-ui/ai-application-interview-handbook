# 技能、MCP 与程序调用｜扩展同一条执行链

[← 上一章](02-tools-files-and-jobs.md) · [本产品目录](README.md) · [下一章 →](04-plans-goals-and-agents.md)

普通工具链已建立，下面解释三种不同扩展：技能提供任务方法，MCP 接入远端实现，PTC 用程序组织受控调用。它们的结果最终仍进入同一个 Agent 循环。

<a id="ptc"></a>
## PTC：把中间处理留在一次程序里

PTC 是 Programmatic Tool Calling（程序化工具调用）。普通原生模式由模型输出结构化调用；PTC 通过 `run_code` 写程序，在程序内调用工具、筛选结果，再输出需要的部分。

```text
本次 run_code：读取若干结果 → 程序筛选 → 输出小结果
下次 run_code：重新取得必要状态，不依赖上次内存变量
```

基础组合提供 Node 运行环境，每次调用有新的执行状态，不是永久保留变量的 REPL（交互式解释器会话）。程序化调用仍经过工具链；一段任意代码不是已经批准的超级工具。[PTC 规则][tools-readme]

收益来自减少某些中间结果和模型轮次，但代码、工具说明、错误修复与最终输出仍有成本。是否更省应在相同任务与成功标准下比较。

> ⚠️ **不能自动重放整段程序。** 超时预算包含嵌套工具与批准等待；后面失败时，前面的副作用可能已完成，应先核验。

<details>
<summary>工具呈现模式与恢复边界</summary>

`native`、`ptc`、`both` 是工具呈现模式。`ptc` 将模型直接入口收束为 `run_code`，底层工具通过程序内受控入口使用，并没有消失；猜旧工具名不能绕过模式限制。执行局部规范值不能靠会话日志原样恢复。Node 是该组合选择，不是 PTC 概念只能使用 JavaScript。[模式实现][tools]、[说明][tools-readme]

</details>

<a id="skills"></a>
## Skill：先发现任务指令，再按需读全文

Skill（技能）是可复用的任务指令，可能附带资源或脚本。DSH 将来源、注册表和模型加载器分开：来源提供技能，注册表整理可用项，`tool-skill` 先展示名称与截短描述；模型需要时再用 `skill` 工具加载全文。[技能服务][skill]、[加载器][skill-tool]

这节省了把所有技能正文一次塞进请求的成本。它仍会产生目录成本；加载指令既不等于运行脚本，也不授予额外文件或网络权限。

用户显式输入允许用户调用的 `/name` 是另一条入口：插件识别被领取的直接用户消息，把技能全文注入当前步骤，不必再让模型重复加载。

<details>
<summary>目录更新与两类可见性</summary>

只有存在可被模型调用的技能，且加载器的 `skill` 工具确实可见时，才发布目录。合格步骤检查目录变化；新增、删除、描述或可见性改变时，追加完整替代目录。先前发布过目录后即使变空，也要发布空目录退役旧名称。

只允许用户调用、不允许模型自主调用的技能，不通过模型目录和工具泄漏；未知 `/name` 可保留为普通文字。每项描述限长不能消除总数量成本，历史目录更新也会占请求空间。[实现边界][skill-tool]

</details>

<a id="mcp"></a>
## MCP：把外部工具接进同一条链

MCP 是外部能力接入协议。客户端连接服务、协商协议、发现工具，再将其注册进 DSH；不是把外部函数名直接拼到提示词里。

模型通常看到 `mcp__服务名__工具名`。两个服务都提供 `search`，也有各自身份；调用远端时使用原始工具名。调用仍携带 Agent、参数、取消与超时，返回值进入同一后处理链。连接成功不等于某次业务调用成功。[MCP 客户端][mcp]

连接丢失后按退避策略重连；故障期间旧工具名可暂时保留，但调用失败。恢复预算耗尽后注销工具，等待重新加载或重启。判断外部记忆是否写成，应查本次调用结果，而不是只看目录。

> ⚠️ **接入外部服务也是信任决策。** 会话引用是不可信快照；MCP 服务器指令却作为文字参与已记录的系统提示。不能声称所有外部文本都被统一降权。服务自身的部署、权限和数据安全也不由客户端自动完成。[服务器上下文][mcp]

<details>
<summary>工具代际、卸载和传输环境</summary>

同一作用域重复注册同一服务名会失败。工具列表按完整代际切换：拉取失败保留上一代，注册冲突回滚本次变更，避免混杂半套工具。公共名称与远端原名分别保存，不通过反向拆字符串猜身份。

卸载时取消重连，关闭客户端，等待连接尝试和同步收束，再注销注册项，避免旧异步回调把工具重新挂回。

本地 stdio（标准输入输出）服务是真实子进程。接入会过滤名称匹配密钥、密码、秘密、令牌模式及 `DSH_*` 的环境项，再合并显式配置，并非传入空环境。HTTP 服务有独立部署与权限。图片能否进入请求还取决于模型输入能力和附件功能；不支持时要明确诊断。[生命周期与环境规则][mcp]

</details>

### 扩展失效后不能靠旧名字继续执行

技能发布要求取得完整目录快照，并确认当前作用域中可见的加载工具就是该插件注册的对象。仅仅存在同名 `skill` 不够，否则可能用一个来源的目录引导模型调用另一个实现。合格步骤观察到新目录后发布完整替代，空目录也明确退役旧入口。[目录发布](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/skill/tool-skill/src/index.ts)

MCP 重连前先关闭旧传输。若不能确认旧传输已经结束，停止重连，避免两个 stdio 服务器进程重叠。目录还显示旧名称时，调用失败是可解释的暂态；不能为了消除错误再绕过当前连接管理器启动另一个同名服务。[连接关闭与重连](https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/mcp/mcp-client/src/connection.ts)

<a id="scale"></a>
## 工具变多以后，分别控制哪一类负担

| 负担 | 可以采取的办法 | 不能忽略什么 |
|---|---|---|
| Skill 正文 | 目录与按需加载 | 目录数量、单项描述和历史更新仍有成本 |
| 不相关工具集合 | 按任务与作用域限制 | 不能丢必需能力，本层注册还要单独检查 |
| 工具定义 | 根据路由能力使用适当呈现与延迟加载 | 标记不保证后端支持 |
| 大工具结果 | 外置、关键证据保留、按需取回 | 原件必须可访问，错误证据不能消失 |
| 长会话历史 | 合法区间压缩，保留近期尾部 | 系统头和不可分单元另有边界 |

分页任务只需文件与测试相关能力时，不必同时暴露全部业务写工具；但精简应以任务覆盖和实际请求为依据。只调一个压缩阈值不能解决所有层面的增长。

<details>
<summary>`deferLoading` 能证明什么</summary>

定义与相关投影保留 `deferLoading: true`，表示请求延迟加载工具说明；它不证明工具已经被历史事件激活，也不证明实现了通用语义工具搜索。路由拒绝、忽略或按普通工具呈现的实际行为，需要核对对应适配器。[定义源码][schema]、[能力说明][tools-readme]

</details>

[← 上一章](02-tools-files-and-jobs.md) · [本产品目录](README.md) · [下一章 →](04-plans-goals-and-agents.md)

[schema]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/tools/src/schema.ts
[tools]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/tools/src/index.ts
[tools-readme]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/core/tools/README.md
[skill]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/skill/skill/README.md
[skill-tool]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/skill/tool-skill/README.md
[mcp]: https://github.com/deepseek-ai/deepseek-harness/blob/639ed015397290b3745d163aafe02ffee4aa3f84/packages/mcp/mcp-client/README.md
