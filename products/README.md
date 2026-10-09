# Products｜优秀产品学习

[Handbook](../README.md) · [通用课程](../curriculum/README.md) · [实践](../practice/README.md)

沿具体产品的固定源码快照，理解上下文、记忆、工具、权限、恢复与验证怎样组成完整运行过程。每个产品由 README 提供介绍、整体概览、阅读入口和源码地址，学习正文直接放在产品目录下。

## 产品入口与源码

| 产品 | 学习入口 | 固定源码 |
|---|---|---|
| OpenAI Codex | [OpenAI Codex](codex/README.md) | [openai/codex@67a709665a](https://github.com/openai/codex/tree/67a709665ac7b50311b93e32612c9a8281684787) |
| Claude Code | [Claude Code](claude-code/README.md) | [studyzhige-ui/claude-code-source-private@58231dcce4](https://github.com/studyzhige-ui/claude-code-source-private/tree/58231dcce408f805c645cfbc352d2876b517223b) |
| DeepSeek Harness | [DeepSeek Harness](deepseek-harness/README.md) | [deepseek-ai/deepseek-harness@477b4f4205](https://github.com/deepseek-ai/deepseek-harness/tree/477b4f420553e8a52c2fbccc464d7561b239c443) |
| DeerFlow 2.0 | [DeerFlow 2.0](deer-flow/README.md) | [bytedance/deer-flow@e2feca1e56](https://github.com/bytedance/deer-flow/tree/e2feca1e567d9bafce657de8ad8bc668bd7ad513) |

Claude Code 使用私有学习镜像，需相应访问权限；它不等同于可直接构建的官方完整仓库。源码快照、安装版本和实际运行验证须分别说明。

## 四个产品的架构差异

四个学习模块使用相同的观察问题进行对照；具体能力是否实现、默认开启或可用，须以各自固定快照和入口条件判断，不能从同名栏目推导能力等价。

| 产品 | 核心架构 | 状态与模型视图 | 关键边界 |
|---|---|---|---|
| [OpenAI Codex](codex/README.md) | 围绕一条用户请求反复组装输入、调用模型、处理工具结果 | 一次 Turn 可以跨多次模型调用；模型输入、工作历史、持久记录分别承担职责 | 工具许可不等于执行成功；上下文压缩不等于长期记忆 |
| [Claude Code](claude-code/README.md) | 沿一个代码任务理解输入、工具调用和结果回填 | 保存的对话记录不等于每次完整发送给模型的内容；项目约定与反馈各有保存和注入条件 | 私有学习镜像不等于可构建的官方完整源码；批准必须针对实际执行内容 |
| [DeepSeek Harness](deepseek-harness/README.md) | 插件装配 Agent、Session 和工具，使一次任务经过多轮工作 | 会话记录输入、结果和执行边界；每次请求只取需要的表示 | Profile 与插件入口决定能力是否安装；恢复记录不代表允许重做副作用 |
| [DeerFlow 2.0](deer-flow/README.md) | 从 Gateway 默认内嵌运行路径进入 RunWorker，再由 Agent 与有序中间件协作 | Thread、Run、ThreadState 与 ModelRequest 分开；检查点和运行证据服务不同问题 | 默认路径与可选执行模式分开；子任务返回结果后仍要检查验收条件 |

各产品 README 负责展开本产品的对象模型、真实请求链和源码边界；Context、Memory、Tool、Permission、Recovery 等专题进入对应生命周期文档。

## 阅读方式

先在通用课程建立相应机制，再沿一个产品的完整任务阅读：输入怎样组织成模型可见信息，程序怎样执行动作，状态怎样保存，失败后怎样恢复，最后凭什么证明完成。第一次按产品 README 的实际顺序阅读；完成一套后再横向比较。

固定源码说明版本相关事实；引用的调用链说明系统行为；工程解释应由这些事实支持。产品未实现、未启用或未验证的能力应保留边界，不从同名组件推导能力等价。
