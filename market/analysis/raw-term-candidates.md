# Raw Term Candidates for Knowledge-gap Audit

更新日期：2026-09-11

> 这是**召回辅助表**，不是正式 Evidence。命中关键词只表示该 HUMAN-A 来源值得人工回读；不得直接据此增加 Source Count。

## Prompt / Prompt Engineering

候选来源：**72**

| Source | Flow | Match snippets |
|---|---|---|
| `S003` | 影石创新｜AI Agent｜一面｜2026-08-09｜HUMAN-A | 7. Prompt 优化除了增加规则约束还能做什么？ |
| `S008` | 字节跳动抖音基础架构｜Agent 开发｜一面 90min｜2026-04-09 发布｜HUMAN-A | 1. Prompt Template 如何构建？ |
| `S010` | 小红书｜AI 后端开发｜秋招一面｜面试 2026-08-13，发布 08-20，75min｜HUMAN-A | 34. RAG 不准确时，Parsing、Chunk、Embedding、Recall、Rerank、Prompt 分别怎样排查和优化？ |
| `S015` | 百度｜Coding Agent / Agent 开发｜秋招一面 + 二面 + 三面｜2026-08-18 / 08-21 / 08-24｜HUMAN-A | 2. Agent 整体架构、ReAct、Tool Calling、Context 和 System Prompt 分别如何设计？ |
| `S016` | 字节跳动｜Agent 开发｜日常实习一面｜发布 2026-09-09｜HUMAN-A | 真人 / 第一人称证据：作者围绕本人 Coding Agent / Business Agent 项目复盘，问题连续追 Context Token、Compaction Prompt、Skill Loading、Sub-agent，再落到 OS、MySQL、Linux 和 Coding。 / 1. Business Agent 的 Prompt 怎样设计？ / 4. Compaction Prompt 怎样写，如何验证模型真的完成了有效压缩？ |
| `S017` | 字节跳动｜AI Agent 日常实习｜一面 + 二面｜2026-08-13 / 08-16｜HUMAN-A | 10. Prompt Cache 怎样提高命中率并降低重复上下文成本？ |
| `S027` | 小红书｜Agent 开发｜秋招一面 + 二面（同一候选人同流程合并）｜面试 2026-08-12 / 08-17，发布 09-02｜HUMAN-A | 9. Prompt Injection 如何泄露 System Prompt 或绕过指令，怎样建立防护边界？ |
| `S028` | 小红书｜AI 应用开发工程师｜技术面｜面试 2026-06-18 16:00｜HUMAN-A | 3. **Coding Agent / Agent Runtime 已稳定进入“可控软件执行系统”层。** Skill Mis-selection、Dynamic Args、Context Isolation、Container Restart Resume、Secret / Sensitive Data Boundary、Sub-agent Token Accounting、Loop Oscillation、Compaction、Prompt Cache 等均有真人独立命中。 |
| `S029` | 阿里淘天｜AI Agent 开发｜二面｜2026-04-24 发布｜HUMAN-A | 真人 / 第一人称证据：作者明确以个人“二面凉经”发布，写到“面完人都通透了”，问题围绕自己的两个实习项目、个人负责范围、Prompt 与业务数据连续深挖，并包含现场 Agent 场景设计。 / 7. 一个可靠 Prompt 应包含哪些部分，遵循度不好时如何调优？ |
| `S042` | 名创优品｜Agent 开发实习｜一面｜发布 2026-08-26，已通过｜HUMAN-A | 4. Skill 的 Bad Case / Memory 如何避免被错误反馈或 Prompt 污染？ |
| `S044` | 字节跳动抖音｜AI 全栈开发｜多轮流程｜2026-05-27～06-09｜HUMAN-A | 10. Knowledge Card / Short-term Memory 怎样抽取并注入 Final System Prompt？ / 11. Prompt 中为什么加入 Positive / Negative Example？ |
| `S045` | 腾讯｜AI 应用开发｜一面｜面试 2026-07-25｜HUMAN-A | 真人 / 第一人称证据：作者本人面后发布、记录迟迟没有后续并判断可能失败；问题重点不在背名词，而在 Prompt / RAG / Fine-tuning / Workflow / Agent 的边界以及 Production Metrics、Cost 与 Rollback。 / 1. Prompt、RAG、Fine-tuning、Workflow、Agent 分别解决什么问题？ / 8. Prompt / Model / Index 更新怎样 Rollback？ |
| `S047` | FOSHO｜AI 应用 / Agent 开发｜一面 30min｜面试 2026-07-16，发布 07-23｜HUMAN-A | 6. 用户问问题后怎样 Retrieval 相关视频片段并组装 Prompt？ |
| `S048` | Bilibili｜Agent 开发｜一面 + 二面（同一候选人同流程合并）｜面试 2026-08-11 / 08-13，发布 08-19｜HUMAN-A | 15. Agent 出现 Bad Case 或整体效果下降时，怎样定位应该优化 Model、Prompt、Context、Tool、Memory 还是 Runtime？ |
| `S049` | Bilibili｜Agent 开发｜技术二面｜2026 年秋招 / 实习季｜HUMAN-A | 11. 好的 Skill / Prompt 怎样设计？ |
| `S050` | 字节跳动｜AI 应用开发｜一面｜面试 2026-07-14，发布 07-21｜HUMAN-A | 2. Hallucination 从 Prompt / Tool / RAG / Fine-tuning 哪些层面治理？ / 3. Prompt 具体怎样约束模型“不知道就不要编”？ |
| `S055` | 快手｜AI 应用开发｜实习一面｜2026-04-15｜HUMAN-A | 4. System Prompt 与 User Prompt 的职责有什么区别？ |
| `S061` | 拼多多｜AI Agent｜提前批线下两轮｜2026-07-25｜HUMAN-A | 4. 测试失败后如何定位是模型、Prompt、Tool 还是 Runtime 的问题？ |
| `S064` | 字节跳动｜大模型应用开发｜一面｜发布 2026-03-21｜HUMAN-A | 4. 工业图纸类 Hallucination 怎样通过 Prompt / Post-processing 控制？ |
| `S066` | 腾讯｜AI 应用开发｜实习一面｜2026-05-08｜HUMAN-A | 真人 / 第一人称证据：作者以同岗实习一面发布并明确“攒人品”；题目从真实服务监控与 Prompt 模块化连续追到 RAG、Context、SSE、Memory 与 Agent 产品。 / 2. Prompt、MCP 等调用模块为什么要抽象成独立层？ / 3. 切换基础模型以后 Prompt 是否需要重新适配？ |
| `S067` | OPPO｜AI 全栈开发｜一面｜面试 / 发布 2026-08-13｜HUMAN-A | 1. 从用户输入 Prompt 到前端输出，AI Full-stack 链路中做了哪些处理？ |
| `S068` | 字节跳动｜后端 Agent 开发｜暑期二面｜2026-04-08｜HUMAN-A | 真人 / 第一人称证据：作者以暑期实习二面个人记录发布；面试官要求白板画系统架构，并沿模块、通信、RAG、Tool、Auth、Prompt、Context 继续追问，现场链路非常清晰。 / 7. System Prompt 如何构造？ |
| `S071` | 字节跳动｜AI 应用开发｜实习一面｜2026-05-07｜HUMAN-A | 6. Prompt 如何设计和迭代？ |
| `S074` | 阿里淘天｜Agent 开发｜一面凉经｜2026-04-24｜HUMAN-A | 5. Prompt Combination / Prompt Assembly 如何实现？ |
| `S079` | 蚂蚁财富技术部｜Agent / AI 应用方向｜秋招一面（电话面）｜发布 2026-08-21｜HUMAN-A | 11. Prompt Injection 有哪些更确定性的工程防护，Skill Lazy Loading 如何设计？ |
| `S080` | 平安健康保险｜AI 应用开发｜秋招一面｜面试 2026-08-23，08-26 感谢信｜HUMAN-A | 2. 怎样理解 Harness Engineering，它和单纯 Prompt / Workflow 有什么区别？ |
| `S084` | 快手｜AI Agent 开发｜一面｜面试 2026-07-20，发布 07-30｜HUMAN-A | 4. Prompt Injection 与 Tool Calling Security 如何防护？ |
| `S085` | 快手｜Data Agent｜一面｜发布 2026-07-09｜HUMAN-A | 2. Context Engineering、Prompt Engineering、Harness Engineering 应如何区分？ |
| `S086` | 美团｜大模型应用开发｜一面｜发布 2026-03-25｜HUMAN-A | 3. 对话 Memory 如何保存，超过容量后怎样裁剪 / 总结，Prompt 是否变化？ |
| `S092` | 美团｜AI 后端开发｜二面｜发布 2026-04-10｜HUMAN-A | 真人 / 第一人称证据：作者明确以本人 AI 后端二面发布并邀请同岗候选人交流；问题从本人实习与技术选型追到 Redis、Vector DB、幂等、Prompt、Agent Memory 与 AI Coding。 / 4. Prompt Engineering 在真实项目中沉淀了哪些可复用经验？ |
| `S099` | 小红书｜Agent 后端开发｜日常实习二面｜发布 2026-04-03｜HUMAN-A | 真人 / 第一人称证据：作者明确以本人二面分享并写“攒人品”，问题数量不多但持续围绕实习项目中的 Prompt、Agent、RAG、多模态与 OpenClaw，并有现场 Coding。 / 1. 项目里的 Prompt Engineering 结构怎样设计？ |
| `S100` | 腾讯｜AI 后台开发｜日常实习一面｜发布 2026-04-27｜HUMAN-A | 7. Prompt 应如何设计？ |
| `S102` | 腾讯｜AI 后端开发｜二面 50min｜发布 2026-04-01｜HUMAN-A | 3. LLM、Prompt Engineering、RAG、Agent 在真实项目里分别如何实现和优化？ |
| `S103` | 淘天｜AI 应用开发｜一面｜发布 2026-04-16｜HUMAN-A | 真人 / 第一人称证据：作者以本人淘天 AI 应用一面发布“发面经攒人品”，并记录现场压力和多个 AI Coding 环节；问题从 RAG / Harness 连续进入 Agent 自纠错、Sandbox、Prompt Attack、Multi-Agent 与真实用户量，符合目标岗位且非答案型文章。 / 9. Prompt Attack / Prompt Injection 如何防护？ |
| `S107` | 字节跳动｜Agent 开发｜实习一面 + 二面（同一候选人同流程合并）｜发布 2026-06-17 / 06-23｜HUMAN-A | 2. 一次请求给模型的 Prompt / Context 由哪些部分组成，哪些必须注入？ / 25. Dynamic Prompt 与 Static Prompt 有何区别？ |
| `S150` | 字节跳动｜后端 Agent 开发｜二面｜发布 2026-05-04｜HUMAN-A | 真人 / 第一人称证据：作者明确以本人“后端 Agent 开发二面”发布，开头写面试很难并“攒人品”；问题从实习持续进入 Prompt、RAG、LLM Foundation、Java Reflection 和高并发 System Design。 / 1. Prompt 调优有哪些真实经验，能否让 AI 反过来帮助优化 Prompt？ |
| `S152` | 阿里淘天｜Agent 开发｜暑期一面｜发布 2026-04-17｜HUMAN-A | 7. 除 Prompt 外，怎样减少 AI Coding 产生的冗长 / 复杂代码？ |
| `S155` | 腾讯｜AI 应用开发｜暑期一面｜发布 2026-03-20｜HUMAN-A | 3. Skill 全塞 System Prompt 导致 Context 膨胀时怎么办？ |
| `S159` | CVTE｜AI 应用开发｜一面｜发布 2026-08-14｜HUMAN-A | 2. Prompt Injection 怎样防御？ / 3. Agent Prompt 应怎样设计？ |
| `S168` | 字节跳动｜后端 Agent 开发｜实习一面 1h｜发布 2026-04-19｜HUMAN-A | 5. Prompt Engineering 与 Context Engineering 的本质区别是什么？ |
| `S173` | 腾讯｜后端 AI 开发｜实习面经｜发布 2026-04-28｜HUMAN-A | 10. LLM 与 Agent、MCP 与 Function Calling、Skill 与 Prompt Engineering 如何区分？ |
| `S176` | Bilibili｜Coding Agent / Agent 开发｜日常实习一面｜发布 2026-08-28｜HUMAN-A | 10. Skill Description 放在哪里，System Prompt / Context 的注入顺序是什么？ |
| `S178` | 科大讯飞｜Agent 开发｜一面｜面试 2026-03-04｜HUMAN-A | 5. Prompt 与 Chunk Strategy 怎样设计？ |
| `S179` | 科大讯飞｜AI 应用 / Agent 方向｜技术面｜发布 2026-05-14｜HUMAN-A | 8. 好 Prompt 怎样定义，Prompt Evaluation 怎样做？ / 9. Skill 与 Prompt / Shared Abstraction 的边界是什么？ |
| `S182` | 钉学科技｜FDE 实习｜技术面｜面试 2026-08-13，发布 08-18｜HUMAN-A | 2. Code Review Workflow 中三个并行 SubAgent 在 Prompt 与 Tool Selection 上怎样区分职责？ |
| `S184` | 字节跳动｜大模型应用开发｜日常实习二面｜发布 2026-03-21｜HUMAN-A | 7. No-answer Boundary 怎样通过 Prompt / Evaluation 控制？ |
| `S189` | 百度｜Go Backend / Agent 方向｜秋招一面｜发布 2026-08-28｜HUMAN-A | 11. Agent Evaluation 如何同时评价最终结果和执行过程，LLM-as-Judge 怎样减少通用 Prompt 偏差？ |
| `S192` | 大疆创新｜AI Agent 开发｜一面｜面试 2026-08-11，发布 08-13｜HUMAN-A | 5. Hallucination、Prompt、Token 爆涨和 Context Compression 分别怎样治理？ |
| `S200` | 腾讯｜AI 后端开发｜暑期二面｜发布 2026-04｜HUMAN-A | 5. 最终给 LLM 的 Prompt 怎样构造？ |
| `S202` | 字节跳动｜AI 后端开发｜春招一面｜发布 2026-04-05｜HUMAN-A | 8. AI 自动 Code Review 的规则、流程和 Prompt 怎样设计？ |
| `S207` | 要务科技｜AI 应用开发实习生｜一面｜面试 2026-09-07，约 46min｜HUMAN-A | 6. Prompt Injection 与高风险写操作怎样治理；为什么应把修改权限留给用户或受控 Tool？ |
| `S208` | 猎豹移动｜Agent 全栈开发｜技术面｜发布 2026-05-13，约 40min｜HUMAN-A | 6. Prompt 层的 Few-shot / Self-check 与代码层 Retry / Cleanup 分别能解决什么？ / 1. **“先判断要不要 Agent”已经成为真实能力题。** 腾讯直接把 Prompt / RAG / Fine-tuning / Workflow / Agent 放在同一个选择题里，继续验证面试官关注的是工程边界，而不是背框架名词。 |
| `S210` | 联想｜AI 应用开发｜一面｜发布 2026-04-02，20min｜HUMAN-A | 4. Prompt Engineering 有哪些真实项目经验？ |
| `S216` | 快手｜AI 应用开发｜秋招一面｜发布 2026-08-20，50min｜HUMAN-A | 4. **Security 与 Runtime Boundary 正在合流。** Tool Result Compression、Permission、Prompt Injection、Sandbox、高风险写操作确认越来越常出现在同一条工程链路。 |
| `S218` | 美团｜Agent 开发｜日常实习一面｜发布 2026-08-25，75min｜HUMAN-A | 9. Context Trimming、Prompt Cache 与 Milvus 等组件在真实系统中怎样使用？ |
| `S219` | 元石科技｜后端 / Agent｜一面｜发布 2026-08-25｜HUMAN-A | 3. 一次 Model Request 中 System Prompt、Memory、Chat History、Tool Result 怎样排列和注入？ |
| `S221` | 某中型 AI 设备研发公司｜AI Agent 开发｜一面 + 二面 + HR/Boss，已 Offer｜发布 2026-06-17｜HUMAN-A | 11. Prompt Optimization 如何通过真实 Case 和 Regression 证明有效？ |
| `S224` | 美团｜AI 全栈开发｜实习一面｜发布 2026-04-20｜HUMAN-A | 1. **Context 已经从“超窗怎么办”升级成显式 Runtime Data Structure。** 面试会逐层问 System Prompt、Memory、Chat History、Tool Result、Retrieval Evidence 各放哪里，何时压缩、怎样回填，而不是只要一句“做 Summary”。 |
| `S228` | 快手｜AI 全栈开发（音视频）｜一面 + 二面（同一候选人同流程合并）｜发布 2026-08-31 / 09-07｜HUMAN-A | 12. Agent 必须读取内部算法 / 代码才能诊断时，Prompt Injection 与 Sensitive-data Leakage 怎样从架构层治理？ |
| `S230` | 阿里淘天｜Agent 优化 / 业务 Agent 编排｜一面 + 二面（同流程合并）｜2026-04 上旬，04-09 发布 / 补二面状态｜HUMAN-A | 3. Prompt 应从目标、约束、Context、Tool、Output 等哪些维度设计？ |
| `S233` | 成都某中厂（网络安全 / 自研 Agent 产品）｜Agent 产品开发实习｜一面｜面试 2026-06-15，发布 06-26｜HUMAN-A | 1. Prompt Engineering、Context Engineering、Harness Engineering、Loop Engineering 四者有什么区别？ / 2. 为什么 Context Engineering 能解决单一 Prompt 无法解决的问题？ / 10. 应先改 Prompt 还是直接 Fine-tune，什么情况下微调才值得？训练数据来自哪里、质量如何保证？ |
| `S238` | 佰聆数据｜助理 AI 应用开发工程师实习｜一面｜面试 2026-07-14，发布 07-15｜HUMAN-A | 3. Skill、传统 Prompt Engineering 与 MCP 的差异和边界是什么？ / 7. Prompt Engineering 的核心组成和实际设计原则是什么？ / 去重：已回读全部历史 Batch；URL、佰聆数据流程和“LLM JSON 校验 → Skill / Prompt / MCP → Fine-tuning LR → A2A / SubAgent → 前端 Agent 协议 → FastAPI / ASGI 底层 → Python 深度验真”连续题序均未出现。 |
| `S240` | 百度｜Agent 开发｜秋招一面｜发布 2026-09-06｜HUMAN-A | 19. 面对“某上市公司去年毛利率下降”之类金融问题，从 Prompt 到检索、计算、结论的完整 Agent 链路怎样设计？ |
| `S255` | 百度｜AI 应用开发｜实习一面｜发布 2026-05-03｜HUMAN-A | 11. 出现 Answer Bad Case 时怎样从 Retrieval / Model / Prompt / Runtime 分层定位？ |
| `S258` | 阿里云｜Agent Infra｜暑期实习一面｜发布 2026-04-01，后续未通过｜HUMAN-A | 11. 从输入 Prompt 到模型生成 Token，一次 LLM Generation 的底层路径怎样完整描述？ |
| `S263` | 小红书｜AI 全栈开发｜暑期二面｜发布 2026-04-09｜HUMAN-A | 8. Prompt 日常怎样写，哪些细节最影响稳定性？ / 10. 强制下游需要 JSON 时，怎样设计 Prompt / Structured Output Contract？ / 去重：URL 未入库；作者虽已在别家公司出现，但本场为独立小红书流程。“NL2SQL → Entity Mapping → MCP Update Security → Prompt Constraint / JSON → Redis Lazy Refresh → Nested-if Refactor”题序与历史小红书样本不同。 |
| `S276` | 蚂蚁国际｜AI 应用开发｜一面｜发布 2026-04-21｜HUMAN-A | 真人 / 第一人称证据：作者 `想奋斗的柠檬精天天摸鱼` 是长期个人求职账号，历史上持续记录本人不同公司的招聘流程和普通社区互动，不是订阅 / 题库内容账号。本帖明确以“给我面没招了，发点面经攒攒人品”发布；问题围绕自己的检索、会话、限流与缓存工程连续追问，包含针对恶意用户压垮模型、恶意 Prompt 和双层缓存的具体场景，Role Scope 明确为 AI 应用开发。 / 8. 用户用恶意 Prompt 请求模型私密信息时如何防护？ / 去重：已直接回读全部历史 Batch。当前 URL、4/21 蚂蚁国际流程和“Multi-way Retrieval → Conversation Memory → User-level Fair Queue / 恶意洪泛 → Prompt Security → Circuit Breaker → Cache Aside / L2 Cache”长链未在历史正式来源出现。作者次日存在阿里云另一独立招聘流程，组织、岗位与题序完全不同，按规则分别计数。 |
| `S277` | 快手杭州电商｜大模型应用 Java｜一面 + 二面（同一候选人同流程合并）｜面试 2026-03-05 / 03-09，发布 03-15，二面后当晚 OC｜HUMAN-A | 9. Prompt Engineering 有哪些真实实践原则？ |
| `S284` | 美团｜AI 后端开发工程师｜一面｜发布 2026-09-15｜HUMAN-A | 4. Prompt Test Set 多大才有代表性，怎样构建和回归？ / 去重：全历史未出现当前 URL、作者和“Elo → Prompt Test Set → Context Compression 参数验真 → Redis Cache Refresh”连续题序。 |
| `S286` | 小红书｜AI 应用研发（社区搜索 / Agent）｜一面｜面试 / 发布 2026-09-15｜HUMAN-A | 3. **Evaluation 开始验参数而不是验名词。** Elo 怎样比较、Prompt Test Set 多大、Context 为什么 80% 压缩、Offline Case 是否代表线上故障，都要求解释实验依据。 |
| `S347` | 虾皮｜Agent开发｜一面、二面｜HUMAN-A | 12. （原题12）主题：System Prompt/AGENTS.md |
| `S384` | 理想｜Agent秋招（封面）｜一面｜HUMAN-A | 3. （原题3）中期记忆死循环是否考虑把部分内容写System Prompt |

## Prompt Injection / Prompt Attack

候选来源：**9**

| Source | Flow | Match snippets |
|---|---|---|
| `S027` | 小红书｜Agent 开发｜秋招一面 + 二面（同一候选人同流程合并）｜面试 2026-08-12 / 08-17，发布 09-02｜HUMAN-A | 9. Prompt Injection 如何泄露 System Prompt 或绕过指令，怎样建立防护边界？ |
| `S079` | 蚂蚁财富技术部｜Agent / AI 应用方向｜秋招一面（电话面）｜发布 2026-08-21｜HUMAN-A | 11. Prompt Injection 有哪些更确定性的工程防护，Skill Lazy Loading 如何设计？ |
| `S084` | 快手｜AI Agent 开发｜一面｜面试 2026-07-20，发布 07-30｜HUMAN-A | 4. Prompt Injection 与 Tool Calling Security 如何防护？ |
| `S103` | 淘天｜AI 应用开发｜一面｜发布 2026-04-16｜HUMAN-A | 真人 / 第一人称证据：作者以本人淘天 AI 应用一面发布“发面经攒人品”，并记录现场压力和多个 AI Coding 环节；问题从 RAG / Harness 连续进入 Agent 自纠错、Sandbox、Prompt Attack、Multi-Agent 与真实用户量，符合目标岗位且非答案型文章。 / 9. Prompt Attack / Prompt Injection 如何防护？ |
| `S159` | CVTE｜AI 应用开发｜一面｜发布 2026-08-14｜HUMAN-A | 2. Prompt Injection 怎样防御？ |
| `S207` | 要务科技｜AI 应用开发实习生｜一面｜面试 2026-09-07，约 46min｜HUMAN-A | 6. Prompt Injection 与高风险写操作怎样治理；为什么应把修改权限留给用户或受控 Tool？ |
| `S216` | 快手｜AI 应用开发｜秋招一面｜发布 2026-08-20，50min｜HUMAN-A | 4. **Security 与 Runtime Boundary 正在合流。** Tool Result Compression、Permission、Prompt Injection、Sandbox、高风险写操作确认越来越常出现在同一条工程链路。 |
| `S228` | 快手｜AI 全栈开发（音视频）｜一面 + 二面（同一候选人同流程合并）｜发布 2026-08-31 / 09-07｜HUMAN-A | 12. Agent 必须读取内部算法 / 代码才能诊断时，Prompt Injection 与 Sensitive-data Leakage 怎样从架构层治理？ |
| `S372` | 美团｜Agent日常实习｜一面｜HUMAN-A | 17. （原题17）这段提示词是否有Prompt Injection风险 / 去重：Checkpoint→MultiAgent→Redis BigKey→BM25→现场Prompt Injection→RestoreIP未写出链未入库；S294同算法属于不同公司和作者。 |

## Intent Recognition

候选来源：**22**

| Source | Flow | Match snippets |
|---|---|---|
| `S008` | 字节跳动抖音基础架构｜Agent 开发｜一面 90min｜2026-04-09 发布｜HUMAN-A | 7. Intent Classification 为什么需要并行化？ |
| `S010` | 小红书｜AI 后端开发｜秋招一面｜面试 2026-08-13，发布 08-20，75min｜HUMAN-A | 31. Agent Intent Recognition 不准确时，可以从哪些层优化？ |
| `S012` | 启云方｜AI Agent｜一面｜发布 2026-09-09｜HUMAN-A | 6. Tool Selection 是关键词 / Rule / Intent Recognition，还是模型基于 Tool Schema 自主选择？ |
| `S024` | 小鹏汽车｜AI 全栈产品研发培训生｜一面 13min｜发布 / 更新 2026-09-02，已挂｜HUMAN-A | 4. LLM 如何处理模糊 Intent Recognition，其工程机制怎样理解？ |
| `S057` | 快手｜AI 应用开发｜留用实习一面｜发布 2026-08-26，35min｜HUMAN-A | 5. Intent Tree / Intent Recognition 怎样实现，准确率如何测？ |
| `S122` | 哔哩哔哩｜AI 应用岗 Agent 开发｜一面｜面试 2026-08-16，发布 08-18｜HUMAN-A | 3. Intent Recognition 用 Rule、Small Model、LLM Classification 时怎样选？ / 4. Zero-shot / Few-shot Intent Classification 分别适合什么数据条件？ / 5. 标注数据少时怎样提升 Intent Classification Stability？ |
| `S139` | 联想｜Agent 应用开发｜实习一面｜发布 2026-04-17｜HUMAN-A | 3. Main Agent 的 Intent Recognition 怎样实现？ |
| `S248` | 腾讯｜Agent 开发｜日常实习一面｜发布 2026-04-09，已挂｜HUMAN-A | 真人 / 第一人称证据：作者 `Elite求职中` 以本人“T厂 Agent开发日常实习一面挂凉经”发布，开场先现场手撕约 5 分钟，之后连续深挖多模态 RAG、实习意图识别、代码生成、Qwen Tool Calling、Memory、状态机和代码助手；正文还保留到岗时间、毕业论文等真实招聘流程问题。作者主页 / 评论表现为个人求职轨迹，不是内容账号。 / 6. 实习里的 Intent Recognition 模型解决什么真实问题，效果提升怎样证明？ |
| `S255` | 百度｜AI 应用开发｜实习一面｜发布 2026-05-03｜HUMAN-A | 真人 / 第一人称证据：作者 `静息狂想` 以本人“27实习百度 AI应用开发面经分享”发布，开头自评“面完人都通透了，还是太菜了，下去沉淀一下”。题目从实习 / 项目验真进入 Intent Recognition、Base Model Selection、FAISS、Evaluation、4-GPU Distributed Deployment、PagedAttention、Rerank、Load Test / Bad Case 与现场 Coding，实际 Role Scope 清晰。 / 2. Intent Recognition 怎样实现？ |
| `S260` | 阿里灵犀互娱｜AI 应用开发｜暑期二面｜发布 2026-04-10｜HUMAN-A | 3. Intent Recognition Small Model 怎样训练，Dataset 怎样构造？ |
| `S276` | 蚂蚁国际｜AI 应用开发｜一面｜发布 2026-04-21｜HUMAN-A | 3. Intent Recognition 怎样实现，多路检索相比单路的 Recall 提升如何证明？ |
| `S285` | 智谱｜AI Native Builder 实习｜一面｜发布 2026-09-16｜HUMAN-A | 5. Intent Recognition / Routing 怎样实现？ |
| `S312` | 腾讯｜Agent开发（本人timeline明确）｜一面+二面+三面，合为一个Source｜HUMAN-A | 3. （原题3）意图识别实现/准确率 / 5. （原题5）意图识别实现 / 6. （原题6）抽象化提升意图识别原因 |
| `S320` | 北京金山数娱｜AI应用开发｜一面｜HUMAN-A | 5. （原题5）意图识别 |
| `S328` | 携程｜Agent开发（秋招）｜一面｜HUMAN-A | 1. （原题1）意图识别实现及好坏标准 |
| `S329` | 字节跳动｜Agent开发｜三面｜HUMAN-A | 2. （原文未编号）Supervisor Agent是意图识别还是路由；路由如何实现 / 13. （原文未编号）口述生活助手意图识别Prompt：输入用户问题，输出JSON枚举旅行/购物/吃饭三选一 |
| `S356` | 百度｜AI Agent / Agent Harness｜一面｜HUMAN-A | 5. （原题5）分层架构除意图识别外的工程、效果改进 |
| `S371` | 美团｜Agent开发｜一面｜HUMAN-A | 10. （原题10）是否了解原文称“jev”、可替换意图识别的技术（术语未确认） |
| `S376` | 理想｜Agent开发｜一面｜HUMAN-A | 1. （原题1）意图识别三路融合如何实现；冲突处理及评分机制 |
| `S381` | 阿里—淘宝闪购｜AI研发岗（主体为Agent应用工程）｜一面50min、二面40min、HR面50min｜HUMAN-A | 真人 / 第一人称证据：作者给出从8.11投递到9.4意向书的本人流程，明确以自己面试感受作复盘；按50/40/50分钟三轮分开记录，项目沿意图识别准确率→错误类别→执行链路→工具接口变更异常连续追问；二面/HR围绕数学转计算机、实习经历的具体个人背景追问 / 2. （原题2）意图识别如何实现 / 3. （原题3）意图识别准确率如何计算 |
| `S382` | 小绿书（原文别称，未擅自映射）｜Agent｜一面｜HUMAN-A | 4. （原题3）92%意图识别准确率如何计算，区分单意图与多意图 |
| `S384` | 理想｜Agent秋招（封面）｜一面｜HUMAN-A | 去重：本人理想Agent一面，中期记忆死循环→中长期检索→跨用例冲突/过期→更新触发→Harness/指标，与本批坐标旅人意图识别/Skill/grill-me链和旧理想低密度排除条目不同。 |

## LangGraph / LangChain

候选来源：**65**

| Source | Flow | Match snippets |
|---|---|---|
| `S004` | 小红书｜大模型平台 Agentic 全栈研发｜一面｜2026-08-06｜HUMAN-A | 10. 为什么自研 Agent Runtime，而不是直接使用 LangGraph 等框架？ |
| `S006` | 阿里国际 / Lazada 交易｜Agent 开发实习｜一面 + 二面 + HR｜2026-04-22 / 04-27 / 05-07｜HUMAN-A | 7. 自己修改的 LangGraph Project 中 Memory System 怎样设计？ |
| `S024` | 小鹏汽车｜AI 全栈产品研发培训生｜一面 13min｜发布 / 更新 2026-09-02，已挂｜HUMAN-A | 真人 / 第一人称证据：与 `S012` 为同一真实候选人，但小鹏是完全独立的公司招聘流程。作者明确记录飞书面试只有约 13 分钟、无法确认对方是否开摄像头、体验一般，并于 9/2 更新已挂；问题集中在本人 LangChain / RAG 能力和“Chunk 切断逻辑关系”的具体失败场景。 / 2. LangChain 在项目里具体做了什么，而不是只调用过哪些 API？ |
| `S027` | 小红书｜Agent 开发｜秋招一面 + 二面（同一候选人同流程合并）｜面试 2026-08-12 / 08-17，发布 09-02｜HUMAN-A | 8. 为什么选择 OpenManus，而不是 LangGraph 做编排？Workflow 与自主 Agent 的边界是什么？ |
| `S028` | 小红书｜AI 应用开发工程师｜技术面｜面试 2026-06-18 16:00｜HUMAN-A | 5. **项目价值量化成为强验真信号。** 面试官越来越追 QPS、DAU、Cache Hit Rate、节省人力、准确率、Latency、Cost、失败案例与本人贡献，而不是只接受“用了 LangChain / RAG / MCP”。 |
| `S040` | 原力健康｜Agent 开发｜一面｜面试 2026-06-09｜HUMAN-A | 6. 如果用 LangGraph 编排问答系统，Node 如何拆分？ |
| `S049` | Bilibili｜Agent 开发｜技术二面｜2026 年秋招 / 实习季｜HUMAN-A | 8. Agent Architecture 怎样拆模块，Dify / LangChain 二次开发有什么边界？ |
| `S051` | 机械星球（要务科技）｜AI 应用开发｜一面｜面试 2026-07-14，发布 07-16，凉经｜HUMAN-A | 4. LangGraph 项目最难的地方是什么，Multi-Agent 信息传递、格式与 Hallucination 怎样处理？ / 去重：历史中虽有大量“AI 岗 + Java / Spring”样本，但本场“练手项目是否真有人用 → Spring AI / LangGraph → CORS / Auth → Spring Boot 加载顺序 → Nacos 配置热更 → 连 Linux 系统名都没注意 → Shell 听音失误 → Monolith 改微服务”的真人失败轨迹和题序独立，URL / 作者 / 公司流程均未命中。 |
| `S054` | 快手｜AI 应用开发｜日常实习一面｜2026-02-12｜HUMAN-A | 1. LangGraph 相比 LangChain 的工程差异是什么，State Snapshot 大致如何实现？ |
| `S065` | 字节跳动｜Agent 开发｜二面｜面试 2026-07-18，发布 07-24｜HUMAN-A | 3. Agent Framework 如何选型，除了 LangChain 还调研过什么？ |
| `S071` | 字节跳动｜AI 应用开发｜实习一面｜2026-05-07｜HUMAN-A | 2. LangChain / LangGraph 的使用体验和工程边界是什么？ |
| `S074` | 阿里淘天｜Agent 开发｜一面凉经｜2026-04-24｜HUMAN-A | 真人 / 第一人称证据：作者明确写“面没招了、发点面经攒人品”，问题围绕本人 LangGraph / RAG 项目连续追问，具有明确真人项目验真特征。 / 1. LangGraph 与 LangChain 的差异是什么，为什么项目选择 LangGraph？ |
| `S077` | 深信服｜Agent 开发实习生｜一面 + 二面（同一候选人同流程合并）｜发布 2026-09-02｜HUMAN-A | 7. Dynamic Tool Registry 怎样设计；动态注入与 MCP / LangChain Tool / Skill 有何边界？ |
| `S078` | 拼多多｜Agent 开发｜二面｜面试 2026-08-25，40min｜HUMAN-A | 5. LangChain 与 LangGraph 的核心差异是什么，什么场景需要图状态机？ |
| `S087` | 阿里淘天｜AI 应用开发 / Agent｜一面｜发布 2026-04-10｜HUMAN-A | 8. FastAPI + SSE 如何把 LangGraph 各 Node 的中间结果实时推送到前端？ / 9. 为什么选择 LangGraph 而不是简单 LangChain 编排？ |
| `S094` | 美团｜AI 后端开发｜二面｜发布 2026-04-04｜HUMAN-A | - 9 月 8 日百度 AI 测开等虽然包含 Agent / LangGraph / Skill，但岗位属于测试开发，不通过 Role Scope Gate； |
| `S118` | 阿里平头哥｜AI 应用研发工程师｜暑期一面｜面试 2026-04-28，发布 05-06｜HUMAN-A | 6. 为什么不用 LangChain 完整承载链路，而选择部分能力自研？ |
| `S121` | 阿里｜Agent 开发暑期实习｜一面｜发布 2026-08-05，已 GG｜HUMAN-A | 真人 / 第一人称证据：作者以本人暑期 Agent 开发一面复盘发布，并明确更新已 GG；问题沿个人项目持续进入 Agent 架构、Vector Search、LangGraph、Memory、异常容错与 Coding，不包含标准答案扩写。 / 6. LangChain 与 LangGraph 分别负责什么，为什么这样选？ |
| `S123` | 小红书｜AI 全栈开发｜业务交叉面 + 二面（同一候选人同流程合并）｜发布 2026-06-25 / 07-01｜HUMAN-A | 5. （原题4）LangChain工具调用、Memory与Prompt编排的具体职责 / 17. （原题16）LangGraph关键点 / 22. （原题21）选择LangGraph是否完全依据业务场景 |
| `S124` | 字节跳动财经｜AI 应用开发后端｜日常实习一面｜发布 2026-05-06｜HUMAN-A | 3. 为什么使用 LangGraph 而不是直接原生编排？ |
| `S126` | 阿里灵犀｜AI 应用｜暑期一面｜发布 2026-04-03｜HUMAN-A | 真人 / 第一人称证据：作者以明确的阿里灵犀 AI 应用暑期一面问题记录发布，问题从个人实习进入 RAG / LangGraph / LLM Foundation 与业务算法，不是标准答案或合集。 / 3. LangChain 与 LangGraph 的核心概念和工程边界是什么？ |
| `S136` | 阿里淘天｜AI 应用研发｜一面｜发布 2026-04-17｜HUMAN-A | 真人 / 第一人称证据：作者明确写“一面 2h 没招了、发面经攒人品”；问题从两个本人实习项目深挖到 RAG、LangGraph、Kafka、Text-to-SQL，最后还有约 45 分钟 AI Coding。 / 4. LangGraph State Machine 的 State 怎样流转？ / 5. LangGraph 与 LangChain 的差异和使用场景是什么？ |
| `S162` | 蚂蚁｜AI 应用开发｜暑期二面 65min｜发布 2026-04｜HUMAN-A | 3. LangGraph State 如何定义和传递，Node 很多时怎样避免 State Object 膨胀甚至 OOM？ |
| `S164` | 字节跳动｜Agent 后端开发｜日常实习二面｜发布 2026-04-26｜HUMAN-A | 4. LangChain / LangGraph 分别提供什么能力，工程边界在哪里？ |
| `S165` | 阿里｜AI 应用开发｜一面｜发布 2026-04-26｜HUMAN-A | 真人 / 第一人称证据：作者以本人 AI 应用一面发布并邀请同岗交流；问题从文档 RAG 连续进入 LangGraph、Kafka Backlog、Text-to-SQL 和 AI Tool 使用，具有自然项目追问流。 / 4. LangGraph State 如何存储与流转，为什么选择 LangGraph 而不是 LangChain？ |
| `S177` | 第四范式｜Agent 开发实习生｜一面｜面试 2026-03-13｜HUMAN-A | 真人 / 第一人称证据：作者记录通过 BOSS 投递、HR 询问 Vibe Coding、真人技术面和后续通过结果；问题围绕本人 Agent 项目连续追到 LangGraph、MCP、RAG、Memory、模型路由和故障降级。 / 3. LangChain / LangGraph 怎样使用，MCP Adapter 放在哪一层？ |
| `S179` | 科大讯飞｜AI 应用 / Agent 方向｜技术面｜发布 2026-05-14｜HUMAN-A | 7. LangChain 与 LangGraph 在当前项目里如何比较？ |
| `S180` | 字节跳动｜AI 应用开发｜一面 + 二面面试官合并场｜发布 2026-04-03｜HUMAN-A | 2. LangGraph 怎样编排 Graph？ / 9. LangChain Checkpoint 如何工作？ |
| `S182` | 钉学科技｜FDE 实习｜技术面｜面试 2026-08-13，发布 08-18｜HUMAN-A | 8. LangGraph Checkpointer / Workflow Persistence 应保存哪些 State 字段？ / 13. LangChain 与 LangGraph 分别适合什么场景？ / 14. 使用 LangGraph 编排 Workflow 时，Edge、Node、State 哪个最重要，为什么？ |
| `S186` | 曹操出行｜Agent 开发实习生｜一面｜面试 / 发布 2026-08-17｜HUMAN-A | 真人 / 第一人称证据：候选人围绕本人实习产出和 LangGraph Agent 项目接受连续追问，问题重点是“为什么一定要 Agent、为什么不是脚本 / Workflow”，并追到长链路稳定性和 Evaluation。 / 2. 为什么选择 LangGraph，而不是 Automation Script？ / 5. LangGraph 相比其他框架的具体收益是什么？ |
| `S193` | 字节跳动｜Agent 开发｜日常实习一面｜面试 2026-08-05，发布 08-09｜HUMAN-A | 2. LangGraph 在项目中承担什么作用，State 保存哪些字段？ |
| `S206` | 要务科技｜AI 应用开发实习生｜一面｜发布 2026-08-27｜HUMAN-A | 6. Python 在 AI Service 中用到什么深度，是否真正用 LangChain 做过 RAG？ |
| `S213` | 九号公司｜Agent 开发实习｜一面｜发布 2026-08-31，约 90min，已 OC｜HUMAN-A | 2. LangGraph 自动拆题里每个 Node 的输入 / 输出和完整数据流是什么？ |
| `S221` | 某中型 AI 设备研发公司｜AI Agent 开发｜一面 + 二面 + HR/Boss，已 Offer｜发布 2026-06-17｜HUMAN-A | 3. RAG 与 LangGraph Agent 在真实项目中怎样使用？ |
| `S223` | 阿里国际｜AI 应用开发｜暑期技术面约 1h｜发布 2026-04-30｜HUMAN-A | 7. LangChain / LangGraph / LangChain4j 各自使用了哪些能力？ |
| `S227` | 阿里淘天｜AI / Agent 应用方向｜秋招一面｜面试 / 发布 2026-08-18，次日已挂｜HUMAN-A | 8. LangChain 与 LangGraph 分别解决什么问题，工程选型边界是什么？ |
| `S237` | 北京 B 端 AI 小公司｜AI / Agent 开发｜技术面｜面试 2026-07-14，发布 07-23，约 60min｜HUMAN-A | 11. LangGraph 中有哪些 Node，各自职责是什么？ |
| `S238` | 佰聆数据｜助理 AI 应用开发工程师实习｜一面｜面试 2026-07-14，发布 07-15｜HUMAN-A | 1. Python 中处理 / 校验大模型调用产生 JSON 输出常用什么包或机制，LangGraph / LangChain 中怎样落地？ |
| `S239` | 虾皮（Shopee）｜Agent 开发｜二面｜发布 2026-08-24，约 30min，面后即挂｜HUMAN-A | 5. **AI 应用岗依然大量验真传统后端。** `S051` 把 RAG / LangGraph 与 CORS、Auth、Spring Boot、Nacos、Linux、Monitoring、Monolith → Microservice 放在同一场里，说明“Agent + Backend”仍是一体化能力模型。 |
| `S241` | 百度｜Agent 开发｜秋招一面 + 二面（同一候选人同流程合并）｜面试 2026-08-20 / 08-26｜HUMAN-A | 18. LangChain RAG 从数据进入到 Retrieval / Generation 的完整流程是什么？ |
| `S253` | 蚂蚁｜智能体 / 大模型应用｜暑期一面 + AI 应用开发二面（同一候选人同流程合并）｜发布 2026-04-10 / 04-24｜HUMAN-A | 真人 / 第一人称证据：两篇均由作者 `脆片温柔` 发布，一面标题明确“蚂蚁27暑期智能体大模型应用一面”，二面明确“蚂蚁实习 AI应用开发二面 70m”；项目 / 时间线连续，因此按同一候选人同公司同流程合并。二面从 MinerU / RAGAS、LangGraph State、Memory、GraphRAG 深挖到 Tool Parameter Hallucination、Self-reflection、Human-in-the-loop 和 Skill / MCP。 / 16. LangGraph State 怎样定义 / 流转；Node 很多时如何避免 State Object 过大甚至 OOM？ / 去重：两轮同作者 / 同公司 / 同招聘季，主动合并一个 ID。历史蚂蚁来源未出现“订单状态乱序 / 热评论 → MinerU 跨页表格 → RAGAS Attribution → LangGraph State OOM → Tool Parameter Hallucination → Payment HITL”完整题序，确认独立。 |
| `S269` | 字节跳动抖音电商 / 中国交易与广告｜AI 开发 / 全栈开发｜一面 50min｜面试 2026-08-24｜HUMAN-A | 3. 为什么不用 LangChain 等现成 Framework，而选择当前实现？ |
| `S275` | 百度｜AI 应用工程师｜社招一面｜发布 2026-07-17，视频面，已挂｜HUMAN-A | 3. 从零独立开发 Agent 时为什么选择 LangChain？ |
| `S278` | 快手｜AI 应用服务端开发｜二面｜面试 2026-04-09，发布 04-11｜HUMAN-A | 5. Spring AI Alibaba、LangChain4j、Spring AI 怎样比较，Framework Selection 依据是什么？ / 去重：已直接回读全部历史快手来源。当前 URL、作者和“到岗时间导致流程暂停 → Redis Cluster → Spring AI Alibaba / LangChain4j / Spring AI 选型 → Agent DAG → OpenClaw → RabbitMQ → Merge K Lists”连续题序未在 `S001–S274` 形成同场重复。未找到可稳定核验的同作者快手一面原帖，因此不猜测、不补写，只收当前二面。 |
| `S281` | 科大讯飞｜Agent 研发工程师 · Harness 方向｜线下一面 + 二面 + HR｜2026-09-11｜HUMAN-A | 6. LangGraph Node / State 怎样设计？ |
| `S283` | 美团｜AI Agent｜一面｜发布 2026-09-15｜HUMAN-A | 6. LangChain / LangGraph / Raw Agent 怎样取舍？ |
| `S286` | 小红书｜AI 应用研发（社区搜索 / Agent）｜一面｜面试 / 发布 2026-09-15｜HUMAN-A | - **新旦智能 AI 应用开发**：LangChain 1.0、Hermes Self-evolution / Memory、Harness、Eval、Codex Quality 等题很强，但原始正文持续 Cache Miss，不满足 Verifiable Gate。 |
| `S287` | 字节跳动｜Agent 开发｜秋招一面 + 二面（同一招聘流程）｜发布 2026-09-16 / 09-24｜HUMAN-A | - **百度网络研发 / B站测开等近期 Agent 深挖**：面试中虽出现 LangGraph、OpenClaw、Skill、MCP 或 Agent Evaluation，但岗位主体分别是网络研发 / 测试开发等 Role Scope 外方向。 |
| `S294` | 度小满｜AI 全栈｜一面｜发布 2026-09-20 17:39｜HUMAN-A | 1. （原题3(1)）Agent编排；Plan/ReAct/LangGraph为现成技术还是自研 |
| `S297` | 字节跳动中国交易与广告｜AI 全栈开发工程师｜一面｜面试 2026-09-16，发布 2026-09-24｜HUMAN-A | - **字节剪映 AI 前端一面｜发布 2026-09-22**：公开话题层可看到自研 Agent Framework、为什么不用 LangGraph、ReAct Loop、Tool Registry、`tool_call` JSON Schema、本地 Tool Execution 与 Context 回填等完整技术链；但 post-specific 原帖 / 作者 Timeline 与“AI 前端”实际工作是否属于本库 AI Application Role Scope 仍未同时稳定闭环，继续待追源，不进入 HUMAN-A。 |
| `S301` | 字节跳动｜Agent开发后端（日常实习）｜一面｜HUMAN-A | 1. （原题1）LangGraph选型/工作流 |
| `S302` | 字节跳动｜大模型应用开发（秋招）｜一面｜HUMAN-A | 5. （原题6）主题：LangChain/LangGraph |
| `S303` | 携程｜Agent开发｜一面｜HUMAN-A | 1. （原题2）LangGraph/RAG/图谱项目 / 3. （原题4）LangGraph选型/状态/checkpoint |
| `S304` | 新旦智能｜AI应用开发｜一面｜HUMAN-A | 1. （原题1）LangChain选型/替代框架 |
| `S308` | 小红书｜Agent开发实习生｜两家公司各一面｜HUMAN-A | 4. （原题4）三个LangGraph子图的数据传递 |
| `S309` | 百度｜Agent开发实习生｜两家公司各一面｜HUMAN-A | 4. （原题4）LangGraph+子Agent相对大Agent/脚本 |
| `S312` | 腾讯｜Agent开发（本人timeline明确）｜一面+二面+三面，合为一个Source｜HUMAN-A | 2. （原题2）LangChain/LangGraph使用 |
| `S317` | 斑头雁｜Agent实习生｜一面｜HUMAN-A | 5. 二2 LangChain节点/工具代码 |
| `S329` | 字节跳动｜Agent开发｜三面｜HUMAN-A | 2. （原文未编号）介绍LangGraph框架 |
| `S347` | 虾皮｜Agent开发｜一面、二面｜HUMAN-A | 23. （原题23）不选LangChain原因 |
| `S372` | 美团｜Agent日常实习｜一面｜HUMAN-A | 8. （原题8）是否采用LangGraph等现成Agent框架 |
| `S377` | 快手｜AI应用开发｜一面｜HUMAN-A | Role Scope：AI应用开发明确，LangGraph/工具调用修复/Workflow人工干预和失败处理为主要内容，兼有MySQL和MQ基础 / 1. （原题1）介绍LangGraph核心概念及理解 / 去重：本人设备没配置AI工具而改手写LRU，LangGraph→MCP参数错→人工介入→分表/慢SQL/MQ链独立；与同作者阿里不同公司。 |
| `S380` | 阿里控股｜AI应用研发｜一面｜HUMAN-A | 7. （原题7）LangGraph或Agent开发是否使用栈、队列 |
| `S383` | 东方财富｜AI应用开发（南京）｜一面｜HUMAN-A | 1. （原题1）LangChain/LangGraph对开发者作用 / 2. （原题2）LangChain如何统一上下文、工具、记忆与状态 |
| `S385` | 字节跳动（HR流转的新Agent部门）｜Agent开发｜新部门一面｜HUMAN-A | 真人 / 第一人称证据：原文明确“上次的字节二面完很不幸被挂掉了，不过hr说是给我流转到另外一个部门了，但是是做Agent开发相关的”；本人将模型/工程边界用Harness说明，项目未接第三方框架仍被追问LangGraph；面后称高强度且每题需深入模块 / 1. （原题1）LangGraph基本概念 |

## A2A

候选来源：**7**

| Source | Flow | Match snippets |
|---|---|---|
| `S006` | 阿里国际 / Lazada 交易｜Agent 开发实习｜一面 + 二面 + HR｜2026-04-22 / 04-27 / 05-07｜HUMAN-A | 2. **Python / FastAPI 已被再次独立确认。** 字节大模型应用一面直接追 FastAPI Middleware vs Dependency、multiprocessing / threading、`asyncio.gather` vs `as_completed`、超时降级，并和 Milvus / RAG / Multi-Agent / A2A 同场出现。 |
| `S021` | 腾讯｜Agent 开发｜实习一面｜发布 2026-03-30｜HUMAN-A | 真人 / 第一人称证据：作者以本人腾讯 Agent 一面发布并写“给我面没招了”，问题从 RAG 延迟 / Evaluation 进入 Agent Loop / Tool / Plan，再问 Streaming Protocol、Go Concurrency、Lock、MCP/A2A 与 Claude Code。 / 10. MCP、Function Call、A2A 如何区分；是否自己写过 MCP Server？ |
| `S048` | Bilibili｜Agent 开发｜一面 + 二面（同一候选人同流程合并）｜面试 2026-08-11 / 08-13，发布 08-19｜HUMAN-A | 真人 / 第一人称证据：两篇均由作者 `Bk7` 发布，学校、技术方向、岗位和时间线一致；一面为 8 月 11 日约 45 分钟，二面为 8 月 13 日约 45 分钟。作者记录一面面试官较友好、自己担心能否进入下一轮，二面又明确感受到项目价值被质疑，并记录对 A2A 等问题的现场反应。两轮属于同一候选人同一 Bilibili Agent 招聘流程，因此合并为一个 `Sxxx`。 / 4. A2A Protocol 解决什么问题，适合怎样的 Agent Communication？ / 9. A2A 是否真的适合当前项目，Protocol 与现有通信方式怎么比较？ |
| `S064` | 字节跳动｜大模型应用开发｜一面｜发布 2026-03-21｜HUMAN-A | 12. A2A Communication 怎样避免递归对话 / 无限互调？ |
| `S114` | 快手｜AI 应用服务端开发｜一面 + 二面 + 三面｜2026-08-26 / 09-01 / 09-09｜HUMAN-A | 2. Agent-to-Agent / A2A 与 MCP 分别解决什么问题，如何配合？ / 13. 多 Agent 之间怎样通信，Agent-to-Agent Message / State 应怎样组织？ / 去重：已直接回读所有历史快手来源。本场独特的“CR Agent → A2A / MCP → Java Design Pattern → SDD → 二面微软 Backend + SDD 追问 → 三面 Distributed Agent / A2A Communication / Failure Stability / Lua 业务逻辑膨胀”的连续流程未在历史样本出现；三轮同作者同公司同岗位，主动合并。 |
| `S227` | 阿里淘天｜AI / Agent 应用方向｜秋招一面｜面试 / 发布 2026-08-18，次日已挂｜HUMAN-A | 真人 / 第一人称证据：作者 `Huang7_7` 明确写 `8.18 淘天 AI 秋招一面`，评论区次日由楼主更新“已经 g 了”。问题围绕业务项目、Workflow / Agent、A2A、Skill、Context 与 Memory 连续展开，实际职责明显属于 AI Application / Agent Role Scope。 / 4. A2A / Multi-Agent 适合什么类型的任务，什么时候反而不应拆？ |
| `S238` | 佰聆数据｜助理 AI 应用开发工程师实习｜一面｜面试 2026-07-14，发布 07-15｜HUMAN-A | 6. A2A Protocol 与 SubAgent 分别解决什么问题？ / 去重：已回读全部历史 Batch；URL、佰聆数据流程和“LLM JSON 校验 → Skill / Prompt / MCP → Fine-tuning LR → A2A / SubAgent → 前端 Agent 协议 → FastAPI / ASGI 底层 → Python 深度验真”连续题序均未出现。 |

## AI Coding / Vibe Coding

候选来源：**115**

| Source | Flow | Match snippets |
|---|---|---|
| `S001` | 阿里云｜Agent 开发｜一面｜2026-08-18｜HUMAN-A | 真人 / 第一人称证据：作者明确记录自己被再次捞起后参加 Agent 开发面试，描述面试结果，并记录现场 AI Coding。 |
| `S005` | 字节跳动｜AI 应用开发｜一面 + 二面（同一候选人同流程合并）｜2026-05-12 / 05-15｜HUMAN-A | 6. Vibe Coding、Skill 和其它 AI Coding 范式怎样理解？ |
| `S006` | 阿里国际 / Lazada 交易｜Agent 开发实习｜一面 + 二面 + HR｜2026-04-22 / 04-27 / 05-07｜HUMAN-A | - 普通后端 / 前端岗位仅顺带使用 AI Coding，无法证明实际职责属于 AI Application / Agent 的场次； |
| `S011` | 美团零食杂售｜AI 后端开发｜一面｜2026-09-02｜HUMAN-A | 9. AI Coding：根据少量需求直接实现订单详情页面，如何补足验收标准？ |
| `S012` | 启云方｜AI Agent｜一面｜发布 2026-09-09｜HUMAN-A | 1. 日常使用哪些 AI Coding Tool，在 VS Code 中实际接过哪些 API？为什么选择 Codex / CoderX，和 DeepSeek 使用体验怎样比较？ |
| `S020` | 腾讯｜后端 Agent 开发实习｜一面｜2026-04-27 发布｜HUMAN-A | 7. 平时如何使用 AI Coding？ |
| `S026` | 美团｜Agent 开发｜一面｜面试 2026-08-23，08-25 通知未通过｜HUMAN-A | 10. Vibe Coding 的优缺点是什么；从零设计一个 Agent App 要考虑哪些维度？ |
| `S030` | 360｜Agent 开发｜社招二面｜2026-08-26 发布｜HUMAN-A | 9. OpenSpec / Spec-driven Development 在 AI Coding 中解决什么问题？ |
| `S031` | 多益网络｜AI 应用工程师｜一面 + 三面（同一候选人同流程合并）｜2026-08-20 / 08-28｜HUMAN-A | 5. AI Coding 在项目中的实际编码占比与使用方式是什么，怎样做人工验证？ |
| `S046` | 阿里巴巴｜AI 应用开发｜27 实习一面｜发布 2026-05-06｜HUMAN-A | 真人 / 第一人称证据：作者以本人一面分享并写“给我面没招了，发点面经攒攒人品”，问题从 Agent Workflow / Retrieval / Memory 进入 AI Coding 交付、Java Concurrency、Redis/MySQL。 / 6. Python / Java 如何选择，Cursor / Claude Code 在项目中怎样用？ |
| `S049` | Bilibili｜Agent 开发｜技术二面｜2026 年秋招 / 实习季｜HUMAN-A | 9. AI Coding Agent 常用哪些 Tool？ |
| `S051` | 机械星球（要务科技）｜AI 应用开发｜一面｜面试 2026-07-14，发布 07-16，凉经｜HUMAN-A | 18. 反问：公司真实业务是否做 Agent，以及团队如何看待 AI Coding？ |
| `S055` | 快手｜AI 应用开发｜实习一面｜2026-04-15｜HUMAN-A | 1. 日常开发如何使用 AI Coding、MCP、Skill 等工具提升效率？ / 3. Spec / 规范驱动开发在 AI Coding 中解决什么问题？ |
| `S058` | 腾讯｜AI 应用开发｜日常实习二面｜2026-04-30｜HUMAN-A | 10. 现场 AI Coding：从文本抽取 Entity / Relationship / Claim 并输出规范结构。 |
| `S062` | 中兴通讯｜Agent 开发｜实习一面凉经｜发布 2026-05-21｜HUMAN-A | 9. 项目使用哪些语言和开发工具？除了 Cursor，候选人是否能独立编码？ / 10. Cursor / AI Coding 与本人手写代码各自适合什么场景，怎样证明自己理解生成代码？ |
| `S071` | 字节跳动｜AI 应用开发｜实习一面｜2026-05-07｜HUMAN-A | 真人 / 第一人称证据：作者明确以 27 实习 AI 应用开发一面发布并邀请同岗交流；问题从本人 AI Coding / Agent 实践一路追到推理服务、RAG、MCP 和 Multi-Agent。 / 1. 如何使用 AI Coding 开发一个真实 AI Agent？ |
| `S077` | 深信服｜Agent 开发实习生｜一面 + 二面（同一候选人同流程合并）｜发布 2026-09-02｜HUMAN-A | 5. 公司在 Production 中如何使用 AI Coding，怎样保证生成代码质量？ |
| `S080` | 平安健康保险｜AI 应用开发｜秋招一面｜面试 2026-08-23，08-26 感谢信｜HUMAN-A | 10. 金融保险业务中 Agent / Vibe Coding 实际落地到什么程度，人工开发边界在哪里？ |
| `S083` | 字节跳动｜Agent 开发｜秋招一面｜面试 2026-08-12，发布 08-24，1h+｜HUMAN-A | 真人 / 第一人称证据：作者以本人秋招面试记录发布，明确给出 8 月 12 日、Agent 开发与一小时以上时长；问题从候选人自己的三个项目中任选一个深挖，再进入 RAG、AI Coding、Streaming、高并发场景和现场 Coding。候选人记录了面试官对算法方案继续追问线程安全，具有自然现场互动，而不是答案型题单。 / 3. 使用 AI Coding 时，怎样让生成代码达到更高质量，而不是只追求生成速度？ / 去重：URL 未在 `S001–S245` 正式库出现；历史字节 Agent 来源虽然大量涉及 RAG / Context / Coding，但本场“项目任选深挖 → RAG → AI Coding 质量 → SSE/WebSocket → 高并发排行榜 → 两栈队列 + 线程安全”的连续题序、作者与 8/12 流程均独立。 |
| `S088` | 阿里云｜Agent 开发｜一面｜面试 2026-04-10｜HUMAN-A | 真人 / 第一人称证据：作者明确记录 60 分钟真人面试，前半小时问答、后半小时现场 AI Coding；正文保留自己答不上 RPC 问题、请求面试官提示仍没答出的状态。 / 7. AI Coding：实现本地 YAML / INI 配置文件监听与热更新模块。 |
| `S092` | 美团｜AI 后端开发｜二面｜发布 2026-04-10｜HUMAN-A | 真人 / 第一人称证据：作者明确以本人 AI 后端二面发布并邀请同岗候选人交流；问题从本人实习与技术选型追到 Redis、Vector DB、幂等、Prompt、Agent Memory 与 AI Coding。 / 9. AI Coding 在真实开发流程中应怎样使用与验证？ |
| `S093` | 携程｜AI 后端｜暑期一面｜发布 2026-04-10｜HUMAN-A | 真人 / 第一人称证据：作者明确以“AI 后端一面”发布并写“发点面经攒人品”；问题先验证 AI Coding 的生产可用性，再连续追问分库分表、缓存、锁、事务与算法，属于目标 AI Backend 岗的完整基础工程考察。 / 1. AI Coding 生成的代码质量如何评估，什么条件下才允许进入生产？ |
| `S094` | 美团｜AI 后端开发｜二面｜发布 2026-04-04｜HUMAN-A | - 传统后端 / 普通算法岗，仅因简历中出现 Agent 或 AI Coding 而被零散追问的场次； |
| `S101` | 美团｜后端 AI 开发｜暑期一面｜发布 2026-04-27｜HUMAN-A | 真人 / 第一人称证据：作者以本人同岗一面分享，问题从 RAG 项目一路追到 Tool Failure、Agent Interrupt、隐私、AI Coding 大仓库和模型基础，属于目标 AI Backend 场次。 / 8. AI Coding 面对超大 Repo、Token 不够时怎样选择相关代码？ |
| `S103` | 淘天｜AI 应用开发｜一面｜发布 2026-04-16｜HUMAN-A | 真人 / 第一人称证据：作者以本人淘天 AI 应用一面发布“发面经攒人品”，并记录现场压力和多个 AI Coding 环节；问题从 RAG / Harness 连续进入 Agent 自纠错、Sandbox、Prompt Attack、Multi-Agent 与真实用户量，符合目标岗位且非答案型文章。 / 12. AI Coding：多轮现场编码任务，考察生成、修改和验证能力。 |
| `S104` | 阿里国际｜AI 应用研发｜暑期一面｜发布 2026-04-03｜HUMAN-A | 4. 项目主要是本人手写还是借助 AI Coding，边界怎样证明？ / 5. 平时使用哪些 AI Coding Tool？ |
| `S113` | 商汤 SenseTime｜AI 后端开发｜暑期二面 + 三面｜发布 2026-03-15｜HUMAN-A | 真人 / 第一人称证据：作者以“再战暑期实习”形式连续记录自己的二面和三面，轮次清晰；二面深挖系统瓶颈、重试与 RAG，三面继续问职业规划、AI 认知和 AI Coding 实践。 / 9. AI Coding 在开发中怎样实践？ |
| `S114` | 快手｜AI 应用服务端开发｜一面 + 二面 + 三面｜2026-08-26 / 09-01 / 09-09｜HUMAN-A | 4. SDD / Spec-driven Development 怎样理解，怎样约束 AI Coding 或 Agent 开发？ / 6. 日常写代码有多少使用 AI，形成了怎样的 AI-assisted Development 习惯？ |
| `S115` | 腾讯｜AI 应用开发｜二面｜发布 2026-03-23｜HUMAN-A | 4. Cursor 与 Claude Code 等 Coding Agent 在 Context / Worktree 使用方式上有什么差异？ |
| `S117` | 阿里千问事业群｜AI 应用研发工程师｜一面｜发布 2026-04-29｜HUMAN-A | 3. 平时使用 Vibe Coding 还是手写，模型怎样选？ |
| `S119` | 小红书｜存储云平台·数据库智能化 / Agent｜日常实习一面 + 二面｜面试 2026-07-29 / 08-03｜HUMAN-A | 10. AI Coding 工具的 Context Management 有哪些差异？ |
| `S120` | 米哈游｜Agent 开发｜提前批一面｜面试 2026-08-01，发布 08-05｜HUMAN-A | 1. AI Coding 在日常研发中如何使用？ / 2. 如何验证 AI Coding 生成代码质量？ |
| `S123` | 小红书｜AI 全栈开发｜业务交叉面 + 二面（同一候选人同流程合并）｜发布 2026-06-25 / 07-01｜HUMAN-A | 真人 / 第一人称证据：两个页面均由同一作者 `Recall_15` 发布，岗位均为小红书 AI 全栈开发；首轮约 40 分钟，作者记录面试官对业务、AI Coding 和系统上线的具体追问，二面再次约 40 分钟并写“问很细、95% 答上来、希望能过”等现场状态，因此合并为一个招聘流程来源。 / 9. （原题9）AI Coding各阶段常见陷阱 |
| `S127` | 汇川技术｜AI 全栈开发工程师｜一面 + 二面｜面试 2026-08-27 / 08-28｜HUMAN-A | 3. OpenSpec / Superpower 等 AI Coding 方法解决什么问题？ |
| `S128` | OPPO｜AI 全栈开发｜一面｜发布 2026-08-23，次日查看已挂｜HUMAN-A | 真人 / 第一人称证据：候选人记录面试官开场介绍这是较新的 AI Full-stack 岗位，并说明面试不足 30 分钟；作者自评题基本答出但语言组织不佳，次日查看流程已挂。问题把 AI Coding / Skill 与项目上线、团队协作和基础数据结构放在同一场，现场与结果明确。 |
| `S131` | 小红书社区工程｜AI 与全栈｜一面｜面试 / 发布 2026-03-21｜HUMAN-A | 10. 平时如何使用 AI Coding Tool？ |
| `S133` | 字节跳动｜后端 AI 开发｜暑期一面｜发布 2026-04-30｜HUMAN-A | 真人 / 第一人称证据：作者明确以本人“字节暑期后端 AI 开发一面”复盘发布并写“面完人都通透了”；整场真实地以网络、Redis、并发和 AI Coding / Agent 约束为主，属于目标 AI Backend Foundation 样本。 / 7. 平时怎样使用 AI Coding？ |
| `S136` | 阿里淘天｜AI 应用研发｜一面｜发布 2026-04-17｜HUMAN-A | 真人 / 第一人称证据：作者明确写“一面 2h 没招了、发面经攒人品”；问题从两个本人实习项目深挖到 RAG、LangGraph、Kafka、Text-to-SQL，最后还有约 45 分钟 AI Coding。 / 10. AI Coding：设计可扩展且安全的订单状态机引擎。 |
| `S137` | 快手｜Agent 开发｜暑期一面｜发布 2026-04-30｜HUMAN-A | 真人 / 第一人称证据：作者以本人 Agent 一面“发面经攒人品”发布，问题从实习与 AI Coding 进入 Java Concurrency / JVM / HTTPS 基础，并有现场 Coding。 / 1. AI Coding 未来可能发展到什么程度，目前最大不足是什么？ |
| `S139` | 联想｜Agent 应用开发｜实习一面｜发布 2026-04-17｜HUMAN-A | 11. OpenClaw / Vibe Coding 等产品和范式怎样理解？ |
| `S140` | 阿里国际｜AI 应用研发｜二面｜发布 2026-04-22｜HUMAN-A | 真人 / 第一人称证据：作者以本人二面分享发布并写“面完人都通透了”；问题直接围绕 Agent Project 的数据量、Vector DB、Evaluation、Scale、Inference Service 与 AI Coding 深挖。 / 8. AI Coding Tool 对研发效率的真实提升怎样量化？ |
| `S142` | 阿里淘天｜AI 应用研发｜秋招一面 + AI Coding｜面试 2026-08-26，发布 08-27｜HUMAN-A | ## S142 阿里淘天｜AI 应用研发｜秋招一面 + AI Coding｜面试 2026-08-26，发布 08-27｜HUMAN-A / 真人 / 第一人称证据：同为作者 `Florentino_73` 的本人求职记录，但这是 8 月 26 日淘天 AI 应用研发独立面试，和 8 月 31 日阿里云 Agent Infra 属于不同组织 / 岗位与独立招聘流程，因此不合并。正文记录约 30 分钟项目深挖、5 分钟业务数据结构题、约 30 分钟 AI Coding，并在反问中确认业务重点是把平台商家与用户场景 Agent 化，Role Scope 明确。 / 4. AI Coding：实现商品计价系统，优惠策略需要能够随时更新，例如会员价、满减等。 |
| `S143` | 字节跳动｜Agent 开发｜暑期一面｜发布 2026-04-17｜HUMAN-A | 真人 / 第一人称证据：作者明确记录约 40 分钟真人一面并写“发点面经攒攒人品”，问题围绕本人项目持续深挖，随后直接进入 OpenClaw、Claude Code Memory、AI Coding 与 Context Length。 / 6. 日常怎样使用 AI Coding Tool？ / 7. Cursor / Coding Agent 在 Context 过长时为什么可能发生性能或效果下降？ |
| `S144` | 阿里 Token Foundry｜AI 应用研发｜一面 + 二面 + 三面｜2026-08-17 / 08-24 / 09-03｜HUMAN-A | 10. 项目中哪些设计和代码是本人完成，AI Coding 生成部分如何验证可交付？ |
| `S147` | 阿里淘天｜业务 + AI 全栈工程师｜一面｜发布 2026-09-07｜HUMAN-A | 真人 / 第一人称证据：作者以完整一面过程记录实习确认 → RAG → Agent / AI Coding → MQ 幂等 / 限流 → 深分页 / 账单设计 → 反问；正文保留大量面试官连续追问和作者回答上下文，且反问阶段进一步核实团队确实同时做业务与 Agent。 / 8. AI Coding 如何获得项目规范、模块边界、业务 Wiki 等高质量 Context？ |
| `S151` | 阿里淘天｜AI 应用开发｜二面 80min｜发布 2026-04-17｜HUMAN-A | 真人 / 第一人称证据：作者明确记录二面约 80 分钟并以本人复盘“攒人品”；前半围绕真实 AI 项目和 Multi-Agent 设计追问，后续继续聊模型选择、Fine-tuning、指标和 AI Coding。 / 9. AI Coding 在真实工作中怎样使用，生成代码如何 Review / 验收？ |
| `S152` | 阿里淘天｜Agent 开发｜暑期一面｜发布 2026-04-17｜HUMAN-A | 7. 除 Prompt 外，怎样减少 AI Coding 产生的冗长 / 复杂代码？ |
| `S157` | 蚂蚁｜Agent 开发｜一面｜发布 2026-04-24｜HUMAN-A | 真人 / 第一人称证据：作者明确写“面完人都通透了、还需要沉淀”，以本人 Agent 实习项目为主线连续追问 Multi-Agent、RAG、MCP、Tool Failure、Context 和 AI Coding Quality，问题顺序自然且有明显现场复盘感。 / 10. AI Coding 是否形成方法论，上线前除了 Code Review 还怎样保证质量？ |
| `S159` | CVTE｜AI 应用开发｜一面｜发布 2026-08-14｜HUMAN-A | - CVTE 另一篇虽然现场感很强，但正文只记“项目追问 + Vibe Coding”等少量泛信息，具体技术问题密度不足，不进入正式库； / 3. **AI Coding 不再只问“你用不用 Cursor”。** 真实问题已经追到代码库理解、项目 Wiki / Spec、需求拆分、Git 工作流、质量验收、AI 生成代码能否进 Production、代码复杂度和在线 Coding System Design。 |
| `S165` | 阿里｜AI 应用开发｜一面｜发布 2026-04-26｜HUMAN-A | 8. 日常使用哪些 AI Coding / AI Tool，怎样验证生成结果？ |
| `S166` | 同花顺｜Agent 开发｜实习一面｜发布 2026-04-26｜HUMAN-A | 7. 日常开发使用 AI Coding 的深度如何证明？ |
| `S167` | 同花顺｜Agent 开发｜实习二面｜发布 2026-04-26｜HUMAN-A | 9. 日常 AI Coding Workflow 如何组织？ |
| `S174` | 小米｜后端 AI 开发｜实习一面 1h｜发布 2026-04-25｜HUMAN-A | 真人 / 第一人称证据：作者以本人一小时 AI Backend 面试分享发布；问题按实习项目 → Redis / MQ → 高并发 → MySQL / Spring → AI Coding / SDD 自然展开。 / 8. 公司里怎样使用 AI Coding，同时保证代码规范？ / 9. SDD / Spec-driven Development 对 AI Coding 有什么工程价值？ |
| `S177` | 第四范式｜Agent 开发实习生｜一面｜面试 2026-03-13｜HUMAN-A | 真人 / 第一人称证据：作者记录通过 BOSS 投递、HR 询问 Vibe Coding、真人技术面和后续通过结果；问题围绕本人 Agent 项目连续追到 LangGraph、MCP、RAG、Memory、模型路由和故障降级。 / 9. AI Coding / Spec-driven Development 怎样进入真实研发流程？ |
| `S179` | 科大讯飞｜AI 应用 / Agent 方向｜技术面｜发布 2026-05-14｜HUMAN-A | 真人 / 第一人称证据：作者以本人面试复盘发布并更新当前已通过；面试官会围绕一个回答继续追单点，不是标准题单，问题从自动工单 Agent 进入 Tool Abstraction、Evaluation、Skill 与 AI Coding。 / 10. Claude Code / Codex / Vibe Coding 在真实研发中怎样使用？ |
| `S185` | 京东｜AI Agent 开发实习生｜二面｜面试 2026-04-09｜HUMAN-A | 7. 平时怎样使用 AI Coding？ |
| `S186` | 曹操出行｜Agent 开发实习生｜一面｜面试 / 发布 2026-08-17｜HUMAN-A | 10. AI Coding Tool 有哪些真实 Pitfall，工程师如何控制质量？ |
| `S191` | 美团｜AI 全栈开发｜一面 + 二面｜面试 2026-04-15 / 04-21，次日 Offer｜HUMAN-A | 10. AI Coding：如何让 AI 自动提交员工周报并保证业务正确性？ |
| `S198` | 京东科技｜AI 后端开发｜二面｜发布 2026-04-06｜HUMAN-A | 真人 / 第一人称证据：作者以本人二面分享并“攒人品”，整场围绕 Redis Rate Limit / Distributed Lock / Cache Consistency、ThreadPool Availability 和 AI Coding 生产实践连续追问。 / 9. AI Coding 日常怎样使用，最大收益和典型坑是什么？ |
| `S205` | 广州某小厂｜Agent 后端开发｜一面（三阶段）｜发布 2026-06-12｜HUMAN-A | 真人 / 第一人称证据：作者明确记录整场约 2.5 小时，分为 1h 架构深挖、1h Vibe Coding、30min 围绕改进代码继续追问；多次写到面试官会提示 / 引导并给反馈，自己后半段已记不清具体追问，现场痕迹非常强。 / 8. 现场 Vibe Coding：在现有 Agent Framework 上选择一个方向做真实改进。 / 去重：URL、题序和“1h 架构 + 1h Vibe Coding + 30min 复盘”时间线均未在现有来源命中；未发现跨站同场原帖冲突。 |
| `S207` | 要务科技｜AI 应用开发实习生｜一面｜面试 2026-09-07，约 46min｜HUMAN-A | 9. AI Coding 从需求澄清、Skill、Plan、实现到 Compile / Unit Test / Browser Test 的完整流程是什么？ |
| `S208` | 猎豹移动｜Agent 全栈开发｜技术面｜发布 2026-05-13，约 40min｜HUMAN-A | 3. **AI Coding 已经变成项目验真的一部分。** 面试官会问真实编码占比、怎样从需求到 Plan / Test、是否共享屏幕看代码、AI 生成代码由谁验证，而不是只问“用没用 Cursor / Claude Code”。 |
| `S212` | 文远知行｜AI 全栈开发｜三面｜面试 2026-08-18，进入横向｜HUMAN-A | 5. **AI Coding 正和 Harness / SDD / Product Engineering 汇合。** 平安健康问 Coding Agent 自举与 SDD；FOSHO问为什么自研 Coding Agent；小红书 / OPPO把 AI Coding 质量、MVP、上线与前端性能放进同一场。 |
| `S214` | 字节跳动中国交易与广告｜后端日常实习（实际面试主体为 Agent / Harness）｜一面 + 二面 + 三面 + HR，已书面 Offer｜2026-06-17 / 06-22 / 06-24｜HUMAN-A | 27. 项目代码主要手写还是 AI-assisted，候选人如何证明自己理解生成代码？ |
| `S215` | 快手｜AI 全栈开发工程师｜秋招一面｜面试 2026-08-25，发布 08-26｜HUMAN-A | 真人 / 第一人称证据：作者 `小妞脂` 明确给出公司、8 月 25 日、AI 全栈岗位；现场先深挖个人项目和实习业务，再要求 `O(N)` 的第 K 大，候选人记录自己先想到最小堆、后来才切到 Quickselect 思路，并进行 AI Coding 页面开发。作者还写到面试官认为其表达不够清晰，现场痕迹明确。 / 3. 开发过程中怎样使用 AI，什么才算高质量 AI-assisted Development？ / 6. AI Coding：现场实现“满一定金额赠送赠品”的页面 / 功能，如何从需求到可验收结果？ |
| `S216` | 快手｜AI 应用开发｜秋招一面｜发布 2026-08-20，50min｜HUMAN-A | 真人 / 第一人称证据：作者明确写出公司、`AI应用开发` 岗位和 50 分钟时长；项目追问连续 7～8 问，并直接写“麻了”。后半段从线程池追到 OOM / Java Memory Model，再做现场算法和反问；评论区继续围绕结果、项目来源、算法与 Vibe Coding 流程讨论。 / 5. **AI Coding 继续从“会不会用”升级为“代码归属与质量验真”。** 面试官会直接问代码到底是候选人写的还是 AI 写的，并通过现场修改、复杂度约束、页面实操和测试过程验证本人能力。 |
| `S218` | 美团｜Agent 开发｜日常实习一面｜发布 2026-08-25，75min｜HUMAN-A | 11. Vibe Coding / Spec Coding 怎样进入真实研发流程并保证 AI 生成代码正确？ |
| `S220` | 匿名游戏公司（1000–9999 人）｜AI Agent 应用开发｜一面 + 后续二面｜面试 2026-03-03｜HUMAN-A | 10. Cursor / Codex 连续错误修改同一段代码时，怎样跳出错误循环并恢复？ |
| `S221` | 某中型 AI 设备研发公司｜AI Agent 开发｜一面 + 二面 + HR/Boss，已 Offer｜发布 2026-06-17｜HUMAN-A | 5. Vibe Coding 实际使用哪些工具，如何避免只追求速度？ |
| `S224` | 美团｜AI 全栈开发｜实习一面｜发布 2026-04-20｜HUMAN-A | 真人 / 第一人称证据：同为 `星轨偏差` 的个人求职流程，但本场属于美团独立招聘。本帖以本人一面“攒人品”发布，将 RAG / Multi-step Agent Failure 与真实用户、Latency 指标、安全过滤、Vibe Coding 连在一起，并继续追 HTTP、V8、MySQL、IVF/HNSW 与 Java 基础，符合目标 AI Full-stack 的完整工程范围。 / 8. Vibe Coding 的完整 Workflow 是什么；Long Task 中 Context 丢失、忘需求、乱改代码怎样治理？ / 11. AI Coding 现场写函数，并把这套流程抽象成一个 Skill。 |
| `S230` | 阿里淘天｜Agent 优化 / 业务 Agent 编排｜一面 + 二面（同流程合并）｜2026-04 上旬，04-09 发布 / 补二面状态｜HUMAN-A | 4. Vibe Coding 现场拿到问题时，为什么应该先 Clarify Requirement，而不是立刻开始写？ / 9. AI Coding / 面试场景中，怎样证明回答来自真实理解而不是即时搜索？ / 4. **AI Coding 更接近真实现场交付。** 从“满 XX 赠品”页面到不能运行代码的平台题、Vibe Coding 先澄清需求、Agent Generated Code Verification，重点从“是否会用工具”转向“能否定义需求、验证结果和解释代码”。 |
| `S231` | OPPO｜IT 开发（实际纯 Agent）｜27 届秋招一面｜面试 2026-08-27，发布 09-02，已挂｜HUMAN-A | 真人 / 第一人称证据：作者明确记录约 40 分钟真人一面、无手撕、没有传统 Java 八股，“几乎全程围绕 Agent 项目连续深挖”；面后更新已挂，并写自己第一次被纯 Agent 拷打、很多问题靠面试官给上下文和引导才继续回答。问题从 ReAct 代码实现一路进入 MCP、Skill、多模态 Context、Text-to-SQL 和 AI Coding / 新仓库上手，现场链路完整。 / 8. Cursor / Copilot / Codex / Claude Code 等 Coding Agent 在真实开发中怎样使用？ |
| `S235` | 阿里灵犀互娱｜交易支付·大模型应用开发｜秋招一面 + 二面 + 三面 / HR｜2026-08-31 / 09-02 / 09-07，09-08 意向｜HUMAN-A | 6. **AI Coding 开始考长期软件维护，而不只是现场生成代码。** OPPO 直接追陌生 Repo 的 0→1 上手以及旧需求两个月后演进；中兴追“除了 Cursor 你自己会不会写”；快手二面会评价 Coding 过程与工程表达，而不仅看最终 AC。 |
| `S239` | 虾皮（Shopee）｜Agent 开发｜二面｜发布 2026-08-24，约 30min，面后即挂｜HUMAN-A | 2. **AI Coding 开始被直接当成现场能力测试。** `S237` 要求打开真实项目，让 AI 修 Bug，并输出背景、Root Cause、Solution 后现场汇报，已经从“你平时用不用 Cursor”升级成可观察的工程协作行为。 |
| `S244` | 阿里云｜Agent Infra / Data Infra｜秋招一面 + AI Coding｜面试 2026-08-31，发布 09-01｜HUMAN-A | ## S244 阿里云｜Agent Infra / Data Infra｜秋招一面 + AI Coding｜面试 2026-08-31，发布 09-01｜HUMAN-A / 真人 / 第一人称证据：作者 `Florentino_73` 明确记录 8 月 31 日阿里云一面，并按 30min 项目深挖、10min 系统场景、20min Coding、反问、120min AI Coding 的实际时间结构复盘。反问中团队明确做 Agent Infra 的 Data Infra，包括数据处理、State Persistence 与 Post-train 相关工作，Role Scope 清晰。 / 8. 120 分钟 AI Coding：实现阿里云 SLS → MySQL 的动态写入系统。 |
| `S245` | OPPO｜AI 应用研发 / Agent 方向（实际内容明确）｜秋招一面｜发布 2026-08-21，约 50min｜HUMAN-A | 真人 / 第一人称证据：作者 `启明_不想秋招版` 记录约 50 分钟一面，并写自己原本想推掉流程但未能推掉；面试官主要沿简历持续追项目细节、个人贡献、异常处理和落地效果。虽然标题只写“OPPO 一面”，正文明确讨论“AI 应用研发方向”、Agent 项目、MCP / Skill / Tool / RAG 与 AI Coding，实际 Role Scope 清晰。 / 4. **Agent Infra 开始与 Data / System Infra 深度融合。** 阿里云 `S244` 把 SGX / EPC、多租户安全、吞吐瓶颈、State Persistence 与 120min SLS → MySQL AI Coding 放在同一场，Agent Infra 已远不只是编排框架。 |
| `S246` | 字节跳动抖音电商｜Agent 全栈开发工程师｜秋招一面｜发布 2026-09-03｜HUMAN-A | 9. AI Coding 在真实工作中的代码占比大概怎样，人负责哪些 Review / Verification？ |
| `S247` | 京东｜AI 后台开发｜实习一面｜发布 2026-04-27｜HUMAN-A | 4. **AI Coding 的考法继续工程化。** 字节 `S083` 不只问“会不会用 AI”，而是追代码质量怎样保证；抖音 `S246` 则继续追 AI 生成 Field / API Design 后人如何 Review 和验收。 |
| `S252` | 美团｜AI 全栈开发｜日常实习一面｜发布 2026-04-14｜HUMAN-A | 真人 / 第一人称证据：作者 `脆片温柔` 明确记录本人美团 AI 全栈一面并“攒人品”；前半段持续比较自己 Agent 的 Memory / Retrieval 与 OpenClaw（原帖称“龙虾”），随后要求共享屏幕演示 Agent Architecture、Function、Code，面试官甚至查看 Cursor 对话记录来验真项目；作者明确写“Java 项目一点没问，全问 AI”，最后还有 LC21 与 AI Coding，现场痕迹很强。 / 10. 面试官查看 Cursor Conversation History，怎样证明 AI Coding 过程中本人理解并主导修改？ / 12. AI Coding：现场完成一项开发题并解释验证方式。 |
| `S253` | 蚂蚁｜智能体 / 大模型应用｜暑期一面 + AI 应用开发二面（同一候选人同流程合并）｜发布 2026-04-10 / 04-24｜HUMAN-A | 11. 如果全程 AI Coding，一个外卖 / 评论业务怎样从需求拆到可交付实现？ / 13. AI Coding 普及后，Software Testing 怎样与 AI 协作？ / 27. Vibe Coding 怎样从自然语言任务变成可靠执行路径，Context Cache 怎样参与？ |
| `S256` | 滴滴｜后端开发（实际 AI Agent / RAG 为主体）｜一面｜发布 2026-03-14｜HUMAN-A | 真人 / 第一人称证据：作者 `要睡觉💤` 明确写“周五面的”，保留自己 AI 能力不足、担心挂掉的面后状态；评论区多人追问具体岗位和项目。虽然标题只写“滴滴一面”，但正文几乎全程围绕 OpenClaw、Agent 扩容、Context、RAG、Streaming、ES Vector 与 AI Coding，反问时面试官还明确说明团队正在整体转向 AI，实际职责通过 AI Backend / Agent Role Scope。 / 10. 日常怎样使用 AI Coding？ / 去重：URL、作者、3 月滴滴流程和“OpenClaw → Agent 高并发 → Context 压缩 / 杂乱检索 → WebFlux Streaming → ES Vector → AI Coding → Slow SQL”连续题序均未在 `S001–S255` 形成同场重复。 |
| `S257` | 快手｜后端日常实习（实际全程 AI Agent 项目）｜一面｜面试 2026-04-03，发布 04-04｜HUMAN-A | 真人 / 第一人称证据：作者 `孟之梦` 明确写“无八股，全程都在聊 AI 项目”，并记录现场手撕 LC15；评论区继续追问二面、部门和项目来源。整场不是泛 Agent 八股，而是反复要求候选人用指标证明 RAG / Agent 方案、比较强模型替代方案、解释 MCP Client/Server，并复盘 AI Coding 的真实失败案例。 / 14. 日常是否使用 AI Coding，Web Coding 与传统编程有什么区别？ / 15. AI Coding 犯过的最大错误是什么，候选人怎样修复并沉淀方法？ |
| `S258` | 阿里云｜Agent Infra｜暑期实习一面｜发布 2026-04-01，后续未通过｜HUMAN-A | 15. Cursor / Claude Code 平时怎样进入真实开发流程？ |
| `S259` | 小红书｜AI 全栈｜暑期一面 + 二面（同一候选人同流程合并）｜发布 2026-04-06 / 04-08｜HUMAN-A | 真人 / 第一人称证据：两篇均由 `猪脚饭之王` 发布；一面末尾明确更新“第二天约二面”，二面两天后发布并更新“后续挂”，作者、公司、方向和时间线完整闭环，因此合并为一个 `Sxxx`。两轮覆盖 MCP / Tool、GMP、RAG、Skill、Go Sync / Gin、AI Coding 质量和现场 Coding。 / 14. 怎样使用 AI Coding 从 Requirement 走到完整 Implementation？ / 去重：两 URL 均未在历史来源出现；同作者同公司明确合并。历史小红书样本没有“MCP Tools/Resources/Prompts → GMP Blocking → JSON Diff Coding → Go Sync/Gin → AI Coding Bad Code Testing”的完整题序。 |
| `S260` | 阿里灵犀互娱｜AI 应用开发｜暑期二面｜发布 2026-04-10｜HUMAN-A | 真人 / 第一人称证据：作者同为 `猪脚饭之王`，属于其个人求职 Timeline 中另一家公司独立流程。本页明确是灵犀互娱 AI 应用开发暑期二面，问题集中在 AI Coding、游戏智能客服、Intent Small Model、Multi-Agent、多平台数据源、Context 与 Memory；后续同步页显示该候选人继续进入 HR 流程。 / 1. 日常怎样使用 AI Coding，如何保证生成结果满足 Requirement？ |
| `S261` | 美团｜AI 全栈开发｜日常实习二面 1h｜发布 2026-04-05｜HUMAN-A | 真人 / 第一人称证据：作者 `励志搞钱大鹅` 以本人“AI 全栈开发日常实习二面 1h”发布。题目数量不多，但现场证据很强：面试官要求共享屏幕，直接用本地 AI Coding 工具完成需求，并继续演示面试前准备的 AI Coding 项目和真实效果；这比标准概念题更能反映 AI Application 岗的项目验真方式。 / 3. 平时怎样使用 Cursor？ / 6. 现场 AI Coding：共享屏幕，使用本地 AI Coding Tool 直接实现一个简单需求，并解释过程和验证方式。 |
| `S266` | 美团｜后端 Agent 开发｜实习一面｜发布 2026-04-14｜HUMAN-A | 7. 开放题：怎样看 AI Coding 对 Programmer 门槛、职责和工程能力要求的影响？ / 去重：虽然问题数量较少，但全部为明确技术主题，并处于目标 Agent Backend 实习流程；URL、作者和“Agent Loop / RAG → Redis Lock / Cache Consistency → Java Thread → TCP Reliability → AI Coding Impact”题序未与历史美团来源形成同场重复。 / 4. **AI Application 面试进一步从概念转向现场工程验真。** 美团要求屏幕共享直接 AI Coding，快手追 AI Coding 最大失败，京东追 AI IDE 到底写过什么真实代码以及如何提升质量。 |
| `S270` | 字节跳动抖音｜Agent 开发｜秋招一面｜面试 2026-08-14，08-16 未通过，发布 08-18｜HUMAN-A | 真人 / 第一人称证据：候选人明确写“秋招岗位，8 月 14 号面的，8 月 16 号上午接到通知说是没过”，保留完整面试结果与面后难度感受。问题从本人实习 / 项目验真进入状态机扩展、安全攻防、高流量在线统计、Aerospike / Redis，再到 Vibe Coding 分布式限流 System Design，题序自然且技术密度高。 / 14. Vibe Coding：设计一套 Distributed Rate Limiter 的整体架构。 / 去重：已直接回读 `S001–S269`。URL、8/14 抖音 Agent 流程和“状态机扩展 → SSRF / CSRF → 大规模在线耗时趋势 → Aerospike / Redis → Vibe Coding 分布式限流”连续题序均未在历史正式来源出现。作者更早的其它字节页面中存在与历史其它公司高度同序的复制风险，本来源单独按当前独特题序与明确招聘 Timeline 验证，不从那些不确定页面引入任何问题。 |
| `S271` | 字节跳动中国交易与广告·生活服务｜Agent 开发 / Agent 工程师池（前端画像）｜一面｜面试 / 发布 2026-06-08，一面已过｜HUMAN-A | 真人 / 第一人称证据：作者 `自在极意前端嘉豪` 为东南大学前端候选人，正文先交代自己正在初创公司实习、因 HR 说明岗位是新开的 HC 且侧重前端与 AI Coding 而接面。面试按 0–10min 项目、10–15min React Hook、15–40min Coding、40–50min JS 基础记录，保留“Hook 链表实现答不了”“版本比较 O(1) 思路对但没有写出来”等现场状态。作者在评论区当晚更新“一面过，还有两轮技术一轮 HR”。反问阶段 HR 进一步明确：前端 / 后端 / 客户端进入同一个大池子，**统一按 Agent 工程师招聘，再根据简历技术栈提问**；因此虽然本场问题明显偏前端，Role Scope 仍由招聘流程直接确认。 / 10. 反问 / 招聘：Agent 工程师大池如何按候选人背景分配前端、后端、客户端和 AI Coding / Agent 能力的考察权重？ |
| `S273` | 腾讯｜AI 后台开发｜暑期实习一面｜发布 2026-04-02｜HUMAN-A | 19. 如何看待 AI 与程序员的关系，AI Coding 会怎样改变日常研发？ |
| `S277` | 快手杭州电商｜大模型应用 Java｜一面 + 二面（同一候选人同流程合并）｜面试 2026-03-05 / 03-09，发布 03-15，二面后当晚 OC｜HUMAN-A | 27. 如何看待 Vibe Coding，AI-assisted Coding 有哪些局限？ |
| `S279` | 快手｜大模型应用 Java 实习｜一面｜面试 2026-08-17，发布 08-19｜HUMAN-A | 真人 / 第一人称证据：作者 `Wang_PD` 的个人 Timeline 可串起 3 月得物安全开发入职讨论、8 月快手面试和 9 月知乎全栈一面，账号持续记录本人求职 / 实习而非批量搬运。本帖明确写“8.17 日面”，约 30 分钟全问项目，随后约 30 分钟 Vibe Coding，要求用 AI 现场做出一个浏览器插件并给了 Mock Data；这种现场交付比普通题单具有更强真人验证。岗位标题明确为“大模型应用 Java 实习”。 / 9. Vibe Coding：约 30 分钟内使用 AI 做出浏览器插件，支持 Tab Management、Browsing-history Storage 和 Next-action Recommendation，并基于给定 Mock Data 完成交付。 / 去重：已直接回读 `S001–S274`。当前 URL、作者、8/17 流程和“Agent Project → Tool Integration Metric → Redis Lock + Kafka → SkillHub Compliance → Agent 自动运营 Benchmark → 30min Browser Plugin Vibe Coding”连续链均未在历史来源出现。外部按罕见题序检索仅定位到当前原帖及站内话题 / 评论镜像，未发现更早独立来源。 |
| `S281` | 科大讯飞｜Agent 研发工程师 · Harness 方向｜线下一面 + 二面 + HR｜2026-09-11｜HUMAN-A | 7. AI Coding 在真实项目中的参与度如何证明，生成代码由谁验证？ |
| `S282` | 快手｜AI 全栈｜秋招一面｜发布 2026-09-15｜HUMAN-A | 真人 / 第一人称证据：岗位标题明确 AI 全栈；作者按本人秋招流程发布，并保留“很多八股说不上来”等现场状态。整场不是只问 AI 名词，而是把 Backend Foundation 与 AI Coding 生产实践混合考察。 / 6. 日常 AI Coding Workflow 怎样组织？ / 去重：全历史未发现当前 URL、作者和“Backend Foundation → AI Coding Production Bad Case”连续流程的同场来源；历史快手 AI 全栈 / Agent 来源均为其他候选人或不同流程。 |
| `S286` | 小红书｜AI 应用研发（社区搜索 / Agent）｜一面｜面试 / 发布 2026-09-15｜HUMAN-A | - **望尘科技 AI 全栈 9/14**：能从关联页面看到面试时长、Java 与 AI Coding Quality，但原帖直链没有稳定定位，继续零贡献。 / 4. **AI Coding 已进入 Production Verification。** 面试官关心 Bad Case 漏检、Review Bottleneck、真实落地和人类 Review / Test，而不是只问使用了哪个工具。 |
| `S287` | 字节跳动｜Agent 开发｜秋招一面 + 二面（同一招聘流程）｜发布 2026-09-16 / 09-24｜HUMAN-A | 真人 / 第一人称证据：作者页面显示当前身份为“小红书 Agent 开发（实习员工）”；正文明确记录本人字节 Agent 秋招一面，并写“当天下午已约二面”。面试过程中保留与真人面试官讨论 Computer Use、Pi Agent、DeepSeek Harness、AI Coding 方式与团队业务的现场互动，属于候选人本人第一人称招聘流程，不是答案帖、合集或内容账号整理。 / Role Scope：标题直接为“字节 Agent 秋招一面”，技术主体围绕企业 AI 助手、Memory / Context、Agent Harness、Computer Use、AI Coding 与 Agent 工程集成展开，明确通过 AI Application / Agent Role Scope Gate。 / 10. 日常怎样真正使用 AI Coding，从需求、理解代码、修改、验证到 Review 的完整 Workflow 是什么？ |
| `S288` | 蚂蚁｜AI Native / Agent 应用方向｜一面 + 二面（同一招聘流程合并）｜面试 2026-09-15 / 09-21｜HUMAN-A | 4. Agent / Skill / AI Coding 已明显向普通 Backend、Data、Test 岗扩散，因此 Role Scope Gate 必须比过去更严格； |
| `S289` | 阳光电源｜AI 应用开发工程师｜一面｜面试 2026-09-18 10:00，发布 2026-09-18｜HUMAN-A | 4. **Harness + AI-assisted Engineering Authenticity Verification 是值得继续追的弱信号。** 4399 线索已经把 Harness、SQL 验错、测试指标和“AI 帮你完成后是否真正掌握”放在一起，但 provenance 尚未闭环，因此当前只作为观察，不进入正式频率。 / 5. **Agent / AI 术语继续向普通 Backend / Data / Test 岗扩散。** 这使 Role Scope Gate 更重要，而不是更宽松；出现 Memory / Agent / AI Coding 不能替代目标岗位证据。 |
| `S291` | Shopee｜Chatbot 研发实习｜一面｜面试 2026-09-18，发布 2026-09-19 16:25｜HUMAN-A | Role Scope：岗位标题为 `chatbot研发实习`，技术主体连续覆盖 Agent、Function Call / Tool / MCP、RAG、AI Coding，并混合 Linux 与 Algorithm Foundation；实际职责明确属于 AI Application / Agent Chatbot 研发，不是普通 Backend 顺带问 AI。 / 9. 平时是否 AI Coding，有什么实际方法？ / 去重：正式编号前再次逐个直接回读 `batch-01.md`～`batch-30.md`。历史已有 Shopee `S081`、`S239` 等 Agent 来源，但均为不同作者、不同月份 / 日期与独立流程；未发现当前 URL、作者或“Agent → Function Call / Tool / MCP → RAG 文档规模 → Linux Process → Kth Largest / Quick Sort 深追 → AI Coding”的连续同场来源。 |
| `S294` | 度小满｜AI 全栈｜一面｜发布 2026-09-20 17:39｜HUMAN-A | 14. AI-assisted Development 中最有代表性的真实 Case 是什么；采用度、收益、踩坑和 AI 不擅长的部分怎样评价？ / 3. （原题7(3)）当前AI Coding问题及本人踩坑 / 3. （原题8(3)）AI Coding、手写、算法和协作中哪个最强 |
| `S295` | 百度｜Agent 后端｜三面｜发布 2026-09-22 09:13｜HUMAN-A | - **普通 Backend / Frontend / Data / Test 岗出现 Agent / Skill / AI Coding**：没有目标 Role Scope 时继续排除；术语扩散不等于目标岗位样本。 / 4. **AI Full-stack 仍然是完整软件工程底座 + AI Feature 的组合。** 度小满把 Network / OS / Go / MySQL / Redis / Frontend Foundation 与 AI-assisted Development、AI Q&A System Design 放在同一场。 |
| `S297` | 字节跳动中国交易与广告｜AI 全栈开发工程师｜一面｜面试 2026-09-16，发布 2026-09-24｜HUMAN-A | - **近期算法 / SFT / RL / 模型训练岗位、Test / Data / 普通 Backend / Frontend 岗**：仅出现 Agent、MCP、Skill、AI Coding 等术语不能替代目标 Role Scope；不扩大统计边界。 |
| `S307` | 字节跳动（剪映）｜AI应用开发（日常实习）｜一面｜HUMAN-A | 5. Vibe Coding占比 |
| `S323` | 快手｜AI应用｜二面｜HUMAN-A | 19. （原题19）AI Coding工具与模型 |
| `S330` | 字节跳动/剪映｜AI Agent开发，全栈组｜一面、二面、三面｜HUMAN-A | 31. （原题31）近期Agent和AI Coding实践 |
| `S333` | 字节跳动｜Agent开发秋招｜一面｜HUMAN-A | 10. （原题10）日常AI Coding |
| `S334` | 科大讯飞｜Agent Harness｜一面｜HUMAN-A | 18. （原题18）AI Coding工具 |
| `S345` | 亿联网络｜Agent工程师：企业模型中转路由、员工Agent、硬件产品Agent｜两位面试官合并技术面｜HUMAN-A | 10. （原题4.1）AI Coding看法 / 11. （原题4.2）AI Coding项目实践 |
| `S360` | 快手｜AI全栈开发（Agent）｜一面、二面、三面｜HUMAN-A | ### 一面｜AI Coding现场题 / ### 二面｜AI Coding现场题 |
| `S361` | 字节跳动｜Agent开发｜一面约70分钟｜HUMAN-A | 真人 / 第一人称证据：作者叙述自己列举缓存内容后，面试官继续追问具体设计。；现场缓存编码完成后又要求测试和优化，随后讨论日常AI Coding。；记录面试官对候选人听题方式和本人简历项目介绍的具体反馈。 / ### 算法与AI Coding / 2. （原文未编号）平时是否采用Vibe Coding |
| `S362` | 数字马力｜AI研发实习生｜技术一面，48分钟｜HUMAN-A | 20. （原题7，无编号追问按段序2）常用哪些AI Coding工具，比较多个优点 |
| `S366` | 字节跳动｜AI FDE（Agent客户落地）｜HR初聊+技术一二三面+HR｜HUMAN-A | 真人 / 第一人称证据：作者按第1至第9天串联本人招聘流程；记录具体客户模型报错、现场共享写提示词和AI Coding，最后明确因定级选择在正式offer邮件前终止。 / 10. （原题5）AI Coding制作简单网页，具体需求未披露 |
| `S373` | 京东｜Agent后端开发 / 知识库与大模型应用后端｜二面｜HUMAN-A | Role Scope：原帖标题为Agent后端；34项以上问题围绕知识库平台、向量检索、Agentic RAG、Skills、LLM应用与模型选型连续深挖，远非传统后端偶问AI Coding |
| `S381` | 阿里—淘宝闪购｜AI研发岗（主体为Agent应用工程）｜一面50min、二面40min、HR面50min｜HUMAN-A | 记录边界：4/4全部读完；图2一面项目1–7、八股1–3及只写ai coding的手撕栏目；图3二面1–12（12为反问）；图4 HR1–14。图内无印刷页码，按网站下载顺序和内容映射。 / 10. （原题10）常用AI Coding工具 |
| `S382` | 小绿书（原文别称，未擅自映射）｜Agent｜一面｜HUMAN-A | 16. （原题10）AI Coding使用情况；核心代码为何不由AI生成 |

## Spec-driven Development

候选来源：**17**

| Source | Flow | Match snippets |
|---|---|---|
| `S003` | 影石创新｜AI Agent｜一面｜2026-08-09｜HUMAN-A | 1. Spec Coding 与 Harness 如何理解，Harness 为什么能提升复杂任务完成能力？ |
| `S009` | 蚂蚁国际｜Agent 开发｜一面｜2026-05-09 发布｜HUMAN-A | 6. SDD / TDD 如何与 Agent Coding 结合？ |
| `S030` | 360｜Agent 开发｜社招二面｜2026-08-26 发布｜HUMAN-A | 9. OpenSpec / Spec-driven Development 在 AI Coding 中解决什么问题？ |
| `S080` | 平安健康保险｜AI 应用开发｜秋招一面｜面试 2026-08-23，08-26 感谢信｜HUMAN-A | 7. 是否理解 SDD / Spec-driven Development，它怎样约束 Coding Agent？ |
| `S114` | 快手｜AI 应用服务端开发｜一面 + 二面 + 三面｜2026-08-26 / 09-01 / 09-09｜HUMAN-A | 真人 / 第一人称证据：三篇均由候选人 `27备战秋招` 发布，个人主页是可连续核验的本人求职 Timeline，并明确记录快手 `AI应用服务端`：8 月 26 日一面、9 月 1 日二面、9 月 9 日三面。作者在二面保留“Coding 虽做出但过程不好、感觉面试官态度变化”“SDD 被继续挑战”等现场状态；三面又记录面试官交流体感、到岗时间和其它 Offer，属于连续真人招聘流程而非题单整理。 / 4. SDD / Spec-driven Development 怎样理解，怎样约束 AI Coding 或 Agent 开发？ / 10. SDD 在真实项目中具体怎样落地，为什么面试官会继续挑战方案细节？ |
| `S115` | 腾讯｜AI 应用开发｜二面｜发布 2026-03-23｜HUMAN-A | 5. Spec-driven Coding Agent 如何把需求、实现和验收串起来？ |
| `S127` | 汇川技术｜AI 全栈开发工程师｜一面 + 二面｜面试 2026-08-27 / 08-28｜HUMAN-A | 真人 / 第一人称证据：同一候选人连续记录两轮技术面，二面页面明确更新“已 OC”，并说明最终因实习安排放弃；问题紧贴本人实习、AI Refactor、OpenSpec、MySQL / Sharding 与 Full-stack 能力。 / 3. OpenSpec / Superpower 等 AI Coding 方法解决什么问题？ |
| `S157` | 蚂蚁｜Agent 开发｜一面｜发布 2026-04-24｜HUMAN-A | 11. OpenSpec / Spec 类实践是怎样进入真实项目开发流程的？ |
| `S174` | 小米｜后端 AI 开发｜实习一面 1h｜发布 2026-04-25｜HUMAN-A | 真人 / 第一人称证据：作者以本人一小时 AI Backend 面试分享发布；问题按实习项目 → Redis / MQ → 高并发 → MySQL / Spring → AI Coding / SDD 自然展开。 / 9. SDD / Spec-driven Development 对 AI Coding 有什么工程价值？ |
| `S177` | 第四范式｜Agent 开发实习生｜一面｜面试 2026-03-13｜HUMAN-A | 9. AI Coding / Spec-driven Development 怎样进入真实研发流程？ |
| `S192` | 大疆创新｜AI Agent 开发｜一面｜面试 2026-08-11，发布 08-13｜HUMAN-A | 7. Spec Coding 与 Harness 怎样理解，为什么 Harness 能提高复杂任务完成率？ |
| `S196` | 美团｜后端 Agent 开发｜暑期一面｜发布 2026-04-19｜HUMAN-A | 4. Autonomous Agent Development 与 Spec / Structured-document-driven Workflow 各有什么优缺点？ |
| `S212` | 文远知行｜AI 全栈开发｜三面｜面试 2026-08-18，进入横向｜HUMAN-A | 5. **AI Coding 正和 Harness / SDD / Product Engineering 汇合。** 平安健康问 Coding Agent 自举与 SDD；FOSHO问为什么自研 Coding Agent；小红书 / OPPO把 AI Coding 质量、MVP、上线与前端性能放进同一场。 |
| `S218` | 美团｜Agent 开发｜日常实习一面｜发布 2026-08-25，75min｜HUMAN-A | 11. Vibe Coding / Spec Coding 怎样进入真实研发流程并保证 AI 生成代码正确？ |
| `S334` | 科大讯飞｜Agent Harness｜一面｜HUMAN-A | 22. （原题22）主题：TDD/SDD |
| `S345` | 亿联网络｜Agent工程师：企业模型中转路由、员工Agent、硬件产品Agent｜两位面试官合并技术面｜HUMAN-A | 12. （原题4.3）主题：SDD |
| `S349` | 字节跳动｜Agent开发实习生｜一面45分钟｜HUMAN-A | 13. （原题13）主题：SDD / 15. （原题15）主题：OpenSpec |

