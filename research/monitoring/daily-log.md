# HUMAN-A Continuous Monitoring Daily Log

本文件是每天三次持续检索的滚动工作日志，不是正式 HUMAN-A 来源库。

用途：

- 记录 10:00 / 17:00 / 22:00 三次检索覆盖；
- 记录已核验候选、典型排除、平台 / 公司 / Query 盲区；
- 让晚间 22:00 能把三次检索合并为当天一个 Batch；
- 防止同一天三次任务重复劳动。

固定规则：

1. 只记录最近 3 天主动发现结果；
2. 普通搜索线索可以记录为“已排除 / 待追源”，但只有完整通过 HUMAN-A + Role Scope + 全历史去重的候选才允许同步进入 `inbox.md`；
3. 10:00 / 17:00 不分配 `Sxxx`；
4. 22:00 完成第三次搜索和最终全库去重后，统一生成当天唯一正式 Batch；
5. 当天 0 个正式新增也必须记录搜索覆盖与主要排除原因，不允许为凑数降低质量门槛；
6. 新的一天开始时保留上一日 Final Summary，并新建当日日期段；不要删除历史运行摘要。

---

## 2026-09-16

### 10:00

- Status: completed
- Discovery window：运行时最近 3 天（重点 2026-09-13 ～ 2026-09-16 最新发布 / 更新）。
- Baseline：已重新读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy、最新 Batch，并**直接回读 `batch-01.md`～`batch-26.md` 全历史**。当前正式基线确认：26 个 Batch、`S001–S279` 共 279 个 HUMAN-A、最大 `S279`、下一保留编号 `S280`。
- Search effort：完成至少 38 组定向 Query（另有公司 / 平台泛搜），覆盖字节 / 抖音、阿里 / 淘宝闪购 / 飞猪、腾讯、美团、快手、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米、科大讯飞及中小型 AI 应用岗位；岗位词覆盖 AI Application、Agent、RAG、AI Backend、AI Full-stack、Coding Agent、Harness / Runtime 等。
- Verification effort：实际尝试打开 / 核验 20+ 个近期原始候选链接、作者页或可追源条目；对打不开、只能停留在话题聚合页、只有摘要或来源链不清的结果，不视为“已核验”。
- Platform coverage：牛客本轮能稳定提供最多最新原帖；同时检索小红书 / 知乎 / 脉脉 / CSDN / 独立博客等，但本轮尚未找到可同时满足最近 3 天、原文稳定、第一人称、目标 Role Scope 的非牛客 HUMAN-A。下午需继续补这一盲区。
- Passed HUMAN-A → Inbox：**3 个候选流程**：① 美团 AI 后端（同一候选人一面 + 二面合并候选）；② 科大讯飞 Agent 研发工程师 · Harness 方向（三轮同流程）；③ 快手 AI 全栈一面。Morning 不分配 `Sxxx`。

#### 通过候选摘要

1. **美团 AI 后端｜`SOLDIER_627`｜一面 + 二面同流程**
   - 一面：https://api-cdn.nowcoder.com/discuss/927579574932705280?sourceSSR=post
   - 二面：https://www.nowcoder.com/discuss/929087871779110912
   - 核心信号：故障诊断 Skill、Workflow→Skill、Skill Routing Conflict、Context Bloat、历史 Case 回放 / 故障注入、PI Agent / DeepSeek Harness、Agent Loop、AI Code Review Bottleneck、Cloud DR。
   - 去重关键：历史 `S228` 是同一候选人的**快手**流程；公司与招聘流程独立，因此当前美团流程可以作为独立真人命中，但一 / 二面必须合并为一个来源。

2. **科大讯飞｜Agent 研发工程师 · Harness 方向｜`Tale2229`**
   - 来源：https://www.nowcoder.com/feed/main/detail/671d2fa1d7c04322837ee1f5788dd69d
   - 核心信号：9/11 武汉线下三轮；即时通信项目验真、Memory、知识库增量更新、Agent Loop、Harness、LangGraph Node、AI Coding 参与度，以及 IPC / Deadlock / RWLock / OS / Data Structure 等基础。
   - 真实性：作者记录一面答不上、意外进入二面、二面 / HR 状态和等待结果；个人主页非批量面经账号。

3. **快手｜AI 全栈｜`明天会有好天气`**
   - 来源：https://www.nowcoder.com/feed/main/detail/60d833cbae7f4a668a0bed9e18a428f1
   - 核心信号：MySQL Insert / 两阶段提交、GC / ZGC、Slow SQL、AI Coding Workflow、Production Bad Case、Object Creation、Repeatable Read、Coding。
   - 真实性：作者个人秋招 Timeline 可核验，帖子保留“很多八股说不上来”的现场状态；岗位标题明确 AI 全栈。

#### 待追源 / 暂不进入 Inbox

- **新旦智能 AI 应用开发一面**：最近发布，19 道题覆盖 LangChain 1.0、Hermes Self-evolution / Memory、Context、Harness、Agent Eval、Codex 质量控制，技术价值很高；搜索结果能定位 `/feed/main/detail/81ff321675cc41e18513a3fcbcfe4506`，但本轮直接打开仍出现缓存失败，且作者 Timeline 尚未补齐。下午继续追原页与作者，当前不进 Inbox。
- **淘宝闪购 AI 一面**：9/14 发布，第一人称和 Agent / Memory / QPS / Scale 问题都较强，但当前只稳定取得话题聚合页，未拿到可稳定回读的原帖 URL / 作者 Timeline；暂不进 Inbox。
- **望尘科技 AI 全栈转正实习**：9/14 发布，30min、面试官引导、Java 基础 + AI Coding 质量，Role Scope 明确；当前仅能从其它页面的最新条目完整读取，原帖直链尚未可靠定位，暂不进 Inbox。
- **快手 9/14 二面**：真人痕迹强，题目包含 Agent 三引擎、RAG Evaluation、Memory 与 AI Coding 日志排查，但岗位本身的 AI Role Scope 尚未从当前页面 / Timeline 明确确认，暂缓。
- **字节抖音电商二面**：Take-home AI 工具 + Agent 对话验真非常有价值，但当前标题 / 流程只明确普通后端 / 抖音电商，尚不能证明岗位主体属于 AI Application / Agent；按 Role Scope 保守排除候选池。

#### 典型排除

- **美团 AI Agent 校招一面 / 蚂蚁 AI Agent 等 `AIGC小白入门记` 链**：题目高度完整但账号呈连续多公司“标准化面经” / 专刊内容化特征，缺少候选人本人现场状态；不因题目漂亮降低 Gate。
- **PDD / 米哈游 `面试经验地图` 系列**：同一账号批量整理多场、包含旧日期 / 多场拼接，属于整理型内容，零贡献。
- **北京网梯科技 AI 面**：明确 AI 自动面试式长问题，不属于真人面试官 HUMAN-A。
- **飞猪 Agent 算法一面**：原帖稳定且第一人称，但业务明确偏搜索 / 推荐算法，未通过 AI Application / Agent Engineering Role Scope。
- **字节 / 阿里云 AI Infra 推理训练性能优化场次**：即使出现 Agent / MCP / Skill 名词，岗位主体是纯推理 / 算子 / Training Infra，按 Role Scope 排除。
- **乐元素普通后端一面**：候选人有 Agent 项目且被追问，但岗位主体仍为普通游戏后端，不能用来抬高目标岗位频率。

#### Morning 信号

- **Skill / Harness 已从名词进入真实工程追问。** 美团开始问多 Skill 路由冲突、Context 膨胀、历史 Case 回放 / 故障注入、PI Agent / DeepSeek Harness；科大讯飞直接以 Harness 方向招聘，但仍同时考察系统基础。
- **AI Coding 的考法继续向质量保障下沉。** 快手直接问上线代码遗漏 Bad Case 怎么处理；美团继续问“AI 生成速度超过人工 Review 速度”时工程师如何建立质量边界。
- **Backend / OS Foundation 仍与 Agent 同场。** MySQL、GC / ZGC、IPC、锁、用户态 / 内核态、云容灾继续出现；不能因为岗位叫 Agent / AI Full-stack 就削弱基础工程准备。
- 以上只作为 Market Observation；**Morning 不修改 Canonical / Curriculum**。

#### 17:00 补盲计划

- 优先补：新旦智能 / 淘宝闪购 / 望尘科技的原帖与作者 Timeline；
- 扩大非牛客渠道：小红书、知乎、脉脉、技术博客 / 独立站，重点找可稳定回读的第一人称原文；
- 补公司盲区：百度、腾讯、蚂蚁、京东、滴滴、B站、OPPO / vivo / 小米最近 3 天的 AI Application / Agent 原场；
- 对 Morning Inbox 三个候选继续检查跨平台镜像 / 后发复制链，不因为已进 Inbox 就停止追源。

### 17:00

- Status: pending

### 22:00

- Status: pending

### Final Summary

- Status: pending
