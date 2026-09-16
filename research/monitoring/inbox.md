# HUMAN-A Monitoring Inbox

更新日期：2026-09-16

本文件只保存**已经满足 HUMAN-A、但尚未归入当天正式 Batch** 的候选。普通搜索线索、摘要、低质量面经、答案型文章、Role Scope 外来源和待核验复制链都不进入 Inbox。

> **当前状态：🟢 Continuous Monitoring。** 每天 10:00 / 17:00 / 22:00 搜最近 3 天的新面经；当天三次检索只形成一个日批次。10:00 / 17:00 只暂存已通过 Gate 的候选，22:00 重新做全历史去重后再统一分配 `Sxxx`。

## 固定准入与去重

正式候选必须同时满足：

```text
真人面试官
+ 候选人本人第一人称
+ 高技术密度
+ 真实现场 / 招聘流程痕迹
+ AI Application / Agent Role Scope
+ 原始正文稳定可核验
+ 非转载 / 合集 / 内容号 / 答案帖 / AI 自动面试 / 重复
= HUMAN-A
```

通过岗位准入后，整场真实技术问题都保留，包括 Python / Java / Go、FastAPI、MySQL、Redis、MQ、Network、Concurrency、Vector DB、LLM、RAG、Agent、MCP / Skill / Memory / Harness、AI Coding、System Design 等；不使用普通后端 / 普通前端 / 纯训练 Infra 面经人为补频率。

任何候选进入 Inbox 或分配 `Sxxx` 前，都必须直接回读全部历史 Batch，并同时核验 URL、作者、公司 / 岗位 / 日期 / 轮次、项目语义、至少 5–10 个连续独特题序、招聘 Timeline、跨平台镜像与复制链。GitHub / Search 的 0 命中不能证明未收录。

- 同候选人同公司同招聘流程多轮 → 合并一个来源；
- 同候选人不同公司 / 独立流程 → 可以分别计数；
- 不同 URL 但题序 / 项目语义高度一致 → 继续追源；
- 复制链原场不确定 → 整链排除；
- 原文不能稳定打开 → 零贡献。

## 当前正式基线

每次运行都必须以当前 `main` 重新计算。2026-09-16 17:00 复核结果：

- 正式 Batch：`batch-01.md` ～ `batch-26.md`，共 **26** 个；
- HUMAN-A：`S001–S279`，共 **279** 个；
- 最大编号：`S279`；
- 下一保留编号：`S280`。

## 当前 Inbox

> 2026-09-16 Morning + Afternoon Search：当前共有 **7 个候选流程**通过 HUMAN-A + Role Scope + 全历史去重 Gate。此处不分配 `Sxxx`；22:00 仍需重新回读 `batch-01.md`～当前最新 Batch，对全部候选做最终去重。

### 1. 美团｜AI 后端｜一面 + 二面（同一候选人同流程）

- 作者：`SOLDIER_627`（同济大学，个人求职 Timeline 可核验）
- 一面：https://api-cdn.nowcoder.com/discuss/927579574932705280?sourceSSR=post
- 二面：https://www.nowcoder.com/discuss/929087871779110912
- 一面明确日期：2026-09-10；二面在最近 3 天发现窗口内发布。
- HUMAN-A：一面约 76 分钟、二面约 59 分钟，连续记录本人招聘流程和答题状态。
- 代表性题序：故障诊断 Skill → 错误路由 / 幻觉兜底 → 渐进开放 Tool 与校验门禁 → Workflow→Skill → Multi-Skill Routing Conflict → Context Bloat → 历史 Case 回放 / 故障注入 → PI Agent / DeepSeek Harness → Agent Loop 停止条件 → AI Code Review Bottleneck → Cloud DR → Coding。
- 去重：历史 `S228` 是同一候选人的**快手**独立招聘流程；公司与流程不同。当前美团一 / 二面必须合并为一个未来来源。

### 2. 科大讯飞｜Agent 研发工程师 · Harness 方向｜线下一面 + 二面 + HR

- 作者：`Tale2229`（北京邮电大学）
- 来源：https://www.nowcoder.com/feed/main/detail/671d2fa1d7c04322837ee1f5788dd69d
- 面试：2026-09-11 武汉线下半天三场；帖子在最近 3 天发现窗口内发布。
- HUMAN-A：作者记录从北京到武汉面试、一面多题答不上、意外进入二面、二面 / HR 状态和等待结果。
- 代表性题序：即时通信架构 → 多节点消息处理 → Agent 项目验真 → Short / Long-term Memory → 知识库增量更新 → Agent Loop → Harness → LangGraph Node → AI Coding 参与度 → IPC / Deadlock / RWLock / User-Kernel → AVL vs Red-Black → Memory Fragmentation → Algorithm。
- 去重：历史科大讯飞 `S178 / S179` 为不同作者、不同月份与不同项目 / 题序；当前流程独立。

### 3. 快手｜AI 全栈｜秋招一面

- 作者：`明天会有好天气`（个人秋招 Timeline 可核验）
- 来源：https://www.nowcoder.com/feed/main/detail/60d833cbae7f4a668a0bed9e18a428f1
- 发布：2026-09-15 左右，属于最近 3 天窗口。
- HUMAN-A：岗位标题明确 AI 全栈；作者保留“很多八股说不上来”的真实现场状态。
- 代表性题序：实习 → MySQL Insert → 两阶段提交 → GC / ZGC → Slow SQL → AI Coding Workflow → 上线代码遗漏 Bad Case 的处理 → Object Creation → Repeatable Read → Coding。
- 去重：URL / 作者未在历史库出现；历史快手 AI 全栈 / Agent 样本均为其它候选人和招聘流程。

### 4. 美团｜AI Agent｜一面

- 作者：`会收到的打工人`（吉林大学，个人求职账号）
- 来源：https://www.nowcoder.com/feed/main/detail/50bcdc47e7754aa7be59b6318fea514b?sourceSSR=subject
- 发布：2026-09-15。
- HUMAN-A：明确本人一面，题目沿一个 Agent 项目连续深挖，不是分类题库；作者同日 / 近期仍有真实求职互动。
- 代表性题序：Agent 项目背景 / 落地 / 成果 → 长 Agent Flow 正确性保障 → Long-task Hallucination → 置信度规则与二次用户确认 → Multi-Agent Context Bloat → LangChain / LangGraph / Raw Agent 取舍 → 是否手写 Agent → Knowledge Base → 产品更新后的知识保鲜 / 准确度。
- 去重：已直接回读全部 26 个历史 Batch；当前 URL、作者与连续题序均未出现。与 Morning 的另一位美团候选人为不同作者、不同项目与独立招聘流程。

### 5. 美团｜AI 后端开发工程师｜一面

- 作者：`纯牛马🐮🐴`（南京林业大学，个人求职账号；同日还发布本人百度网盘二面和求职状态）
- 来源：https://www.nowcoder.com/feed/main/detail/b3b11822cef24f689c9600e4415f4043
- 发布：2026-09-15。
- HUMAN-A：作者记录“周四面完、周一挂”、多个现场不会 / 蒙数字 / 手撕未完成状态；反问确认团队为小象超市物流供应链，`Spring 传统后端 + 一些 Agent`，岗位标题明确 AI 后端。
- 代表性题序：AI 题目方案 → 图像编辑模型调研 → Elo Model Evaluation → Prompt Test Set → On-call Agent Context / Memory → Context Compression 触发点与 80% 阈值依据 → Redis Cluster / Cache Selection → 商品图片 URL 自动刷新 → MySQL Isolation / Join → Int Reverse Overflow → SQL Coding。
- 去重：已直接回读全部历史；URL、作者、公司流程与“Elo→Prompt Test→Context Compression 参数验真→Redis Cache Refresh”连续题序未在正式库出现。

### 6. 智谱｜AI Native Builder 实习｜一面

- 作者：`牛客671002402号`
- 来源：https://www.nowcoder.com/discuss/929419257438302208?sourceSSR=%E5%85%B6%E4%BB%96
- 发布：2026-09-16 17:00。
- HUMAN-A：除技术题外还有出生年份、住址、研究生论文压力、可实习时长等强招聘现场痕迹；项目追问持续到团队分工和本人负责边界。
- 代表性题序：AI Native Builder 岗位理解 → AI 开发工具 → 最深项目 / 工期 / Architecture / Team Ownership → Quality Data System → Intent Recognition / Routing → 防止 Agent 导出供应商 / 员工敏感数据 → Service Crash / Restart Recovery → 10 万人抢 100 张票 → Anti-bot → Redis Power-loss → 传统课程平台增加 AI Teaching Assistant，是否算 AI Native。
- 去重：已直接回读全部历史 Batch；当前 URL、作者、智谱流程与“Agent Data Exfiltration → Restart Recovery → 秒杀 / Anti-bot → AI Native 产品判断”题序均未出现。

### 7. 小红书｜AI 应用研发（社区搜索 / Agent）｜一面

- 作者：`Florentino_73`（长期个人求职账号；2026 年已有 C++ / AI Agent 实习投递与面试记录）
- 来源：https://www.nowcoder.com/discuss/929475914579136512?sourceSSR=post&weFlow=true
- 面试 / 发布：2026-09-15。
- HUMAN-A：按真实时长记录 `5min 自我介绍 → 30min 项目深挖 → 20min 手撕 → 反问业务`；反问明确岗位做社区搜索 Agent。
- 代表性题序：金融 Agent → RAG Evaluation → 项目难点 → AI Tool 使用 → AI Frontier → Good Skill Design → Claude Code CLI → 蚂蚁实习具体工作 → 为什么需要 Agent Group Chat / 是否落地 → Coding：平方根保留两位小数 → 反问社区搜索 Agent 业务。
- 去重：已直接回读全历史；URL、作者的小红书流程和连续题序未收录。作者历史评论 / 个人求职记录进一步支持候选人本人身份，不是批量内容账号。
