# Claude Code｜讲解清晰度精修记录

[模块入口](../../products/agent/claude-code/README.md) · [前轮修订记录](../project/claude-code-reader-revision.md) · [源码索引](../../references/agent/claude-code-source-index.md)

## 基线与授权

- 教材基线：`fe288e14b14930ebed4164f7fff90dec8207facf`。
- 发布准备时主干：`e36d24ecd32f5827ae538dfa1f11b566186f891a`。相对教材基线新增的是 Vector DB PR #31；比较确认没有改动本轮七个目标路径，修订基于新主干构造。
- 固定源码：`studyzhige-ui/claude-code-source-private@58231dcce408f805c645cfbc352d2876b517223b`。
- 用户授权：完成上一轮审查全部问题的精修，然后提交并合并 main。
- 范围：产品 README、四篇正文、Claude Code 源码索引中的导航和本记录。其他产品、课程、Market、Frozen Canonical、来源计数与题目归属不改。

本轮建立在前轮对五个教学文件的完整阅读上，重新核对当前 main 和关键实现，并逐篇通读修订稿。保留四篇观察视角，不以文件数或篇幅变化作为质量指标。源码镜像仍未建立官方发行号映射；不将公开产品新功能拼入固定实现。

## 问题与落点

| 审查问题 | 精修位置 | 处理与验收依据 |
|---|---|---|
| 只提醒追到序列化，没有讲材料最终放在哪里 | 01 §4 | 增加来源到 system/messages/tools 的映射和最小请求字段示意；明确 userContext 包装后的角色 |
| 微压缩路径与结果变化不够具体 | 01 §6 | 时间清理、缓存编辑、原样返回三分支；四条结果保留两条的状态表；说明旧 legacy 路径已移除 |
| 负面辨析多于正常过程 | 四篇正文 | 先给规则与可观察状态，再放相应边界；共同版本限制集中到 README |
| 记忆尚未完整使用，就进入调度细节 | 02 §3–5 | 一条反馈从主题及索引保存，到选择、读取、注入、使用；索引加载与异步预取分开 |
| 容量及调度数字喧宾夺主 | 02 §4、§7 | 就地折叠字符串计数、选择上限、整理默认值；重要失效与权限边界仍在正文 |
| 自测优先检验低频实现数字 | 02 自测 | 改为完整保存、失败写入、迟到召回；不依赖折叠细节 |
| 参数改写后要读者自行查完整链 | 03 §4 | 给出原输入、钩子改写、权限输入、最终调用的追踪表；说明本执行函数没有统一重走初始校验 |
| contextModifier 只出现名字 | 03 §7–8 | 分开 data/newMessages/状态修改；使用增加 Read 规则的具体例子；追到串行消费分支 |
| MCP 定义晚于首次使用 | 03 §2 | 首次出现即建立最小定义，再在连接场景展开 |
| 第四篇已有质量，仍有重复及证据对象不够集中 | 04 §2、§7–10 | 保留恢复、协作、性能和分级验证；补被改、被测、被交付对象的同版本对应和回顾图 |
| 缺少便利的源码定位与知识回看 | 四篇末尾及关键机制附近 | 保留必要源码引用，关键新结论链接固定函数行范围；各章补有用途的回看入口 |
| 源码索引指向不存在的锚点 | references/agent/claude-code-source-index.md 开头 | 改为有效模块、历史记录及本记录；不伪改早期研究日期和历史正文 |

保留的重要内容包括：压缩后的任务约束与恢复父链、工具发现状态、提示缓存与长期记忆的区分；直接写入检测的成功边界；后台提取和整理的区别；读取与写入权限范围；ToolSearch 两种加载位置；Hook、Approval、Sandbox 的分工；MCP 会话和认证恢复；Skill、并发、取消与副作用；工作树集成、任务完成语义和最终验证。展开位置调整不等于删除这些知识。

## 本轮重点源码复核

| 结论 | 固定快照中的定位 |
|---|---|
| 上下文生产与角色包装 | `context.ts` 的 getUserContext/getSystemContext；`utils/api.ts` 的 appendSystemContext/prependUserContext |
| 循环、预算与请求结构 | `query.ts` 的 queryLoop、callModel；`services/api/claude.ts` 的 normalizeMessagesForAPI 调用与 paramsFromContext |
| 微压缩条件及内容变化 | `services/compact/microCompact.ts` 的 microcompactMessages、maybeTimeBasedMicrocompact、cachedMicrocompactPath |
| 记忆主题、索引和相关性选择 | `memdir/memdir.ts` 的 buildMemoryLines/buildMemoryPrompt；`memdir/findRelevantMemories.ts` |
| 写入调用与成功结果不同 | `services/extractMemories/extractMemories.ts` 的 hasMemoryWritesSince |
| 参数改写与权限对象 | `services/tools/toolExecution.ts` 的 checkPermissionsAndCallTool；`services/tools/toolHooks.ts` 的 resolveHookPermissionDecision |
| Skill 状态的生产与消费 | `tools/SkillTool/SkillTool.ts` 的 contextModifier；`services/tools/StreamingToolExecutor.ts` 的 executeTool/getCompletedResults |

公开的记忆、Hook、Tool Search 文档用于核对概念和产品边界；细节结论仍以固定快照为依据。未做私有镜像全库逐文件审计，也没有重访外部真人面经原帖。本轮不新增面经覆盖或频率声明，沿用前轮证据与共性机制的教学落点。

## 验证与限制

已完成的文档验证：

- Markdown 解析，标题层级、代码围栏、表格与 details 结构检查。
- 四篇的小结、面试回答、易错点、自测及知识回看检查；答案默认折叠，主线自测不依赖选读。
- 引用式链接解析、固定源码 SHA 检查、模块内路径核对；失效的旧 reader-revision 锚点不再作为有效导航。
- 两个 JSON 教学片段解析；分页预期、并发时间、超时单位与汉字编码计算检查。JSON 请求片段刻意省略部分必需 API 字段，正文明确不是可直接发送的请求。
- Node.js 直接验证 20,000 个基本汉字的字符串长度与 UTF-8 字节数。
- 四篇正文在 Chromium 中分别以 1280 和 390 像素视口渲染，共 8 个预览检查；未发现整页横向溢出，details 展开与收起均正常。人工查看了请求映射和移动端工具篇等关键区段。

浏览器验证使用本地 Markdown 转换和阅读样式，不等同于登录 GitHub 原站逐设备验收。静态项、教学算式和浏览器预览也不等同于真实产品测试。

未执行：构建私有镜像、运行真实 Claude Code、真实 MCP 断线及认证实验、跨进程记忆调度实验、生产验证。修订稿以显式条件说明相关机制，不报告这些未执行项目为通过。

发布前需重新读取 main 和目标文件，保护并行修改；通过独立分支与 PR 合并后，再对照文件 blob 核验。具体 commit、PR 和合并状态以 GitHub 实际历史为准，本记录不预先宣布发布完成。
