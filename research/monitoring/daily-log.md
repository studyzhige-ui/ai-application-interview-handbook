# HUMAN-A Continuous Monitoring Daily Log

本文件是每天三次持续检索的滚动工作日志，不是正式 HUMAN-A 来源库。

用途：记录 10:00 / 17:00 / 22:00 三次检索覆盖、已核验候选、典型排除和平台 / 公司 / Query 盲区，让 22:00 把三次检索合并为当天一个 Batch，并避免重复劳动。

固定规则：

1. 主动发现只看运行时最近 3 天；
2. 普通线索可以记录为“已排除 / 待追源”，但只有完整通过 HUMAN-A + Role Scope + 全历史去重的候选才进入 `inbox.md`；
3. 10:00 / 17:00 不分配 `Sxxx`、不创建 Batch；
4. 22:00 完成第三次搜索和最终全库去重后，统一生成当天唯一正式 Batch；
5. 0 正式新增也是合法结果，不允许为凑数降低门槛。

---

## 2026-09-16

### 10:00 Morning Search

- Status: completed
- Discovery window：2026-09-13 ～ 2026-09-16 的最新发布 / 更新。
- Baseline：重新读取 `main`、Research README、Inbox、Daily Log、两份 Quality Policy、最新 Batch，并直接回读 `batch-01.md`～`batch-26.md` 全历史。确认 26 个正式 Batch、`S001–S279` 共 279 个 HUMAN-A、下一编号 `S280`。
- Search effort：至少 38 组定向 Query，覆盖字节 / 抖音、阿里 / 淘宝闪购、腾讯、美团、快手、小红书、百度、蚂蚁、PDD、京东、滴滴、B站、OPPO / vivo / 小米、科大讯飞及中小型 AI Application / Agent 岗位。
- Verification effort：实际尝试打开 / 核验 20+ 个近期原始候选、作者页或可追源条目；打不开、只停留聚合页、只有摘要或复制链不清的结果不计 HUMAN-A。
- Passed → Inbox：3 个流程：① 美团 AI 后端 `SOLDIER_627` 一面 + 二面；② 科大讯飞 Agent 研发 · Harness 三轮；③ 快手 AI 全栈一面。
- Platform：牛客稳定原帖最多；小红书 / 知乎 / 脉脉 / CSDN / 独立博客没有找到同时满足最近 3 天、稳定原文、第一人称、Role Scope 的非牛客 HUMAN-A。

Morning 主要信号：Skill / Harness 开始进入 Routing Conflict、Context Bloat、Case Replay / Fault Injection；AI Coding 开始追 Production Bad Case 与 Review Bottleneck；Backend / OS Foundation 仍与 Agent 同场。Morning 不改 Canonical / Curriculum。

Morning 待追源：新旦智能、淘宝闪购、望尘科技；快手 9/14 二面 Role Scope 待确认。典型排除包括批量内容账号、AI 自动面试、纯搜推 / 纯推理训练 Infra、普通后端仅顺带问 AI。

### 17:00 Afternoon Search

- Status: completed
- Discovery window：继续只看最近 3 天；优先补 Morning 未充分覆盖的平台、公司和岗位叫法。
- Baseline：再次读取当前 `main`、Research README、Inbox、Daily Log、两份 Quality Policy、最新 Batch，并再次**直接回读 `batch-01.md`～`batch-26.md` 全历史**。当前正式基线仍为 26 Batch / 279 HUMAN-A / 最大 `S279` / 下一 `S280`。
- Search effort：本轮新增完成至少 **31 组定向 Query**，覆盖最近 3 天的 Agent / AI Application / AI Backend / AI Full-stack / AI Native / Harness，以及美团、小红书、字节、智谱、淘宝闪购、快手、百度、腾讯、蚂蚁、京东、滴滴、B站、OPPO / vivo / 小米等；同时专门搜索小红书 / 知乎 / 脉脉 / CSDN / 独立站。
- Verification effort：实际打开、稳定读取或追源 **22+ 个**候选原帖 / 作者记录 / 平台聚合入口；对稳定原帖缺失、正文 Cache Miss、内容账号、AI 自动面试、Role Scope 模糊和历史流程重合的结果均未放宽 Gate。
- Passed HUMAN-A → Inbox：**4 个新增流程**：① 美团 AI Agent 一面；② 美团 AI 后端开发工程师一面；③ 智谱 AI Native Builder 实习一面；④ 小红书 AI 应用研发一面。加上 Morning 3 个，当前 Inbox 共 **7 个候选流程**。Afternoon 仍不分配 `Sxxx`。

#### Afternoon 通过候选

1. **美团｜AI Agent｜`会收到的打工人`**
   - https://www.nowcoder.com/feed/main/detail/50bcdc47e7754aa7be59b6318fea514b?sourceSSR=subject
   - 9/15 发布；Agent 项目连续追到 Long-task Hallucination、置信度 / 二次确认、Multi-Agent Context Bloat、Framework vs Raw Agent、Knowledge Freshness。
   - 与 Morning 美团候选作者 / 项目 / 流程不同；全历史未发现同场。

2. **美团｜AI 后端开发工程师｜`纯牛马🐮🐴`**
   - https://www.nowcoder.com/feed/main/detail/b3b11822cef24f689c9600e4415f4043
   - 9/15 发布；作者同日还有本人百度网盘二面和求职状态，个人候选人身份明确。
   - 连续追问 Model Comparison / Elo Eval / Prompt Test Set、On-call Agent Context Compression 80% 阈值依据、Redis Cache Fields / Image URL Refresh、MySQL 与 Coding；反问确认团队为小象超市物流供应链，传统 Backend + Agent。
   - 全历史未发现同 URL / 作者 / 题序。

3. **智谱｜AI Native Builder 实习｜`牛客671002402号`**
   - https://www.nowcoder.com/discuss/929419257438302208?sourceSSR=%E5%85%B6%E4%BB%96
   - 9/16 17:00 发布；出生年份、住址、论文压力、可实习时长等强招聘现场信号。
   - 项目从 Architecture / Team Ownership 追到 Intent Routing、Agent 敏感数据导出防护、Crash / Restart Recovery，再进入 10 万人抢 100 张票 / Anti-bot / Redis Power-loss 和 AI Native Teaching Assistant 设计。
   - 全历史未发现同场。

4. **小红书｜AI 应用研发（社区搜索 / Agent）｜`Florentino_73`**
   - https://www.nowcoder.com/discuss/929475914579136512?sourceSSR=post&weFlow=true
   - 9/15 面试 / 发布；`5min 自我介绍 → 30min 项目 → 20min 手撕 → 反问业务`，结构清晰。
   - 金融 Agent / RAG Eval / Skill / Claude Code CLI / 蚂蚁 Agent Group Chat / 是否落地 → 平方根 Coding；反问确认岗位主要做社区搜索 Agent。
   - 作者有长期个人求职记录，2026 年已记录 C++ / AI Agent 实习投递与面试，不是批量内容账号；全历史未发现同场。

#### Afternoon 关键排除 / 待追源

- **字节 Agent 开发 9/15 一面｜`小妞脂`**：当前原帖技术密度和现场痕迹都强，但直接回读历史发现同作者已经有 `S076` 字节 Agent 9/3 一面。属于**同候选人 + 同公司 + 同方向 + 同一秋招季**，目前无法证明是独立 BU / 新招聘流程；GitHub Search 0 命中不能推翻历史作者 Timeline。当前不进 Inbox，22:00 继续判断是 `S076` 后续轮次还是独立流程。
- **去哪儿 AI 全栈 AI 面**：9/14 原帖可读，问题覆盖 Function Calling / Context / AI Coding；但历史 Batch 13 已确认去哪儿该类流程属于 AI 自动面试，违反 Human Interviewer Gate，明确排除。
- **新旦智能 AI 应用开发**：19 道题非常强，包含 LangChain 1.0、Hermes Self-evolution / Memory、Harness、Eval、Codex Quality；但原始 `/feed/main/detail/81ff...` 仍出现直接回读 Cache Miss，不满足“原正文稳定可核验”，继续待追源。
- **淘宝闪购 AI 一面 9/14**：聚合页能读到完整第一人称与 Agent / Memory / QPS / Scale 问题，但仍缺稳定可回读的原帖直链 / 作者链，暂不进 Inbox。
- **望尘科技 AI 全栈 9/14**：可在其它页面的最新条目读到 30min、面试官引导、Java + AI Coding Quality，但原帖直链未稳定定位，继续待追源。
- **快手 9/14 二面**：原帖可访问但正文抓取不稳定，且岗位主体 AI Role Scope 尚未确认；暂缓。
- **PDD Agent 二面 / 200+ 面经账号链**：作者账号存在大型多公司面经合集属性，难以确认单篇是否候选人本人原场；按内容账号风险排除。
- **北京网梯科技 AI 面**：长问题看起来技术密度高，但属于 AI 自动面试，不收。
- **字节 9/14 AI Infra**：虽出现 Agent / MCP / Skill，但主体是 GPU / MPI / Profiling / Serving Infra，属于 Role Scope 外纯 AI Infra，不收。
- **携程后端 Agent 9/11**：真实原帖可读，但发布时间 / 面试已在本轮最近 3 天窗口外，不用旧内容补数量。

#### Afternoon 平台 / 公司盲区

- 小红书 / 知乎 / 脉脉 / CSDN 本轮继续没有产出可稳定核验的非牛客 HUMAN-A；CSDN 近期主要是 Agent / Harness 教学与源码解读，不是候选人面经。
- 百度 / 腾讯 / 蚂蚁 / 京东 / 滴滴 / B站 / OPPO / vivo / 小米最近 3 天的目标岗位高质量原场仍稀缺；搜索结果大量是旧来源、普通后端、纯算法 / Infra、聚合 / 答案化内容。
- 22:00 应继续补这些公司，同时重点追新旦 / 淘宝闪购 / 望尘的稳定原帖，并处理 `小妞脂` 字节流程是否与历史 `S076` 合并。

#### Afternoon 新信号

1. **Agent Reliability 正从抽象“防幻觉”变成确定性门禁。** 美团直接问长流程如何保证每一步按预期、置信度怎么定义、何时必须二次确认用户。
2. **Evaluation 参数本身开始被验真。** 美团 AI 后端会追 Elo 怎么 PK、Prompt Test Set 多大、Context 到 80% 为什么压缩；“用了评测 / 压缩”已经不够，必须解释阈值和实验依据。
3. **Agent Security 与 Data Governance 进入应用工程面试。** 智谱直接问如何阻止 Agent 执行“导出所有供应商及员工敏感数据”，安全边界开始与 Tool / 权限设计融合。
4. **AI Application 仍要求传统 System Design / Failure Recovery。** 智谱同场追 10 万人抢 100 张票、Anti-bot、Redis 掉电和服务重启恢复；美团继续追 Redis / MySQL / Coding。
5. **Skill / Claude Code 已进入热门公司项目验真。** 小红书会问 Good Skill、Claude Code CLI，以及 Agent Group Chat 是否真正落地；不是只问工具名。
6. 这些只记为 Market Observation；**Afternoon 不新增 Canonical、不修改 Curriculum**。

### 22:00 Evening Search + Finalize

- Status: pending
- 必做：第三轮最近 3 天搜索 → 读取 Morning / Afternoon Inbox → 再次直接回读全部历史 Batch → 最终去重 → 当天只生成一个 Batch；即使 0 新增也要记录完整搜索与排除。

### Final Summary

- Status: pending
