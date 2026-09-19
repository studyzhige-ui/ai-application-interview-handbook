# AI 应用开发 & Agent / 智能体研发｜官方 JD 市场库

> 核验基线：**2026-09-19**
>
> 本库只收录**第一手官方职位 JD**。任何二手招聘站、聚合站、转载、搜索摘要或第三方镜像都不能进入 Active JD，也不能用于补全官方 JD 缺失的信息。

## 1. Official-source-only Gate

### 允许进入 Active JD 的来源

只允许以下两类：

1. **公司自有域名**上的官方 Careers / 招聘官网职位详情页；
2. 从公司官方 Careers 页面**直接跳转**、并能明确确认属于该公司的官方 ATS 租户职位详情页，例如官方 Workday / Moka / 飞书招聘 ATS。

每条 Active JD 必须能够从官方页面直接核验：

- 公司；
- 岗位名 / Requisition ID；
- 岗位职责；
- 任职要求；
- 可直接回访的官方职位 URL。

只有招聘首页、职位名称片段、搜索摘要，而无法稳定读取完整官方 JD 的，不进入 Active JD。

### 永久禁止作为正式 JD 来源

以下来源对 Active JD **零贡献**：

```text
牛客
Boss 直聘
猎聘
智联招聘
实习僧
高校就业网
JDWatch
niuqizp
ultraai
datahub
招聘公众号转载
媒体文章
个人博客
GitHub Issue
社交媒体
搜索结果摘要
第三方镜像 / 聚合站
```

它们最多只能帮助发现线索。发现后必须继续追到官方原始职位页；追不到官方 JD，就不入库。

### Role Scope

只收工程开发岗：

```text
AI Application Engineering
Agent / 智能体研发
Agent Runtime / Harness / Infra
Coding Agent
AI Native Application
RAG Application Engineering
AI Backend / Full-stack / Client / Platform Engineering
```

严格排除：

- 岗位标题为算法工程师 / 研究员；
- 预训练、后训练、SFT、DPO、RLHF、RL、模型训练为主体；
- 纯模型算法、搜广推算法；
- 纯训练 / 推理 Infra，且主体不是 Agent Infra；
- 产品、运营、销售岗位。

岗位标题即使没有“算法”二字，只要 JD 主体是模型训练 / 研究，也排除。

---

## 2. 公司官方覆盖矩阵

状态定义：

- **✅**：官方招聘系统已核验，并找到至少 1 个符合范围的 Active 官方 JD；
- **△**：官方招聘入口已核验，本轮没有发现符合范围的非算法 Active JD；
- **⟳**：官方招聘 / ATS 已确认，但职位详情动态加载、暂不可稳定读取，后续必须重试；
- **?**：尚未确认稳定的官方招聘职位入口，优先补入口。

### 互联网 / 平台 / 大型科技公司

| 公司 | 官方招聘入口 | 状态 | 本轮结论 |
|---|---|:---:|---|
| 字节跳动 | https://jobs.bytedance.com/ | △ | 官方 Agent 热招结果以算法 / 研究方向为主；未纳入非算法工程岗 |
| 阿里巴巴 | https://www.alibabagroup.com/zh-HK/careers | ⟳ | 官方 Careers 已确认；本轮未稳定取得符合范围的完整官方职位详情 |
| 蚂蚁集团 | https://talent.antgroup.com/ | ⟳ | 官方招聘入口已确认；职位详情需继续追官方原页 |
| 腾讯 | https://tencent.wd1.myworkdayjobs.com/Tencent_Careers | ✅ | 发现 2 个符合范围的官方 Agent 开发 JD |
| 百度 | https://talent.baidu.com/jobs/list | ✅ | 官方站发现多条 AI Application / Agent 工程 JD |
| 美团 | https://zhaopin.meituan.com/ | △ | 官方站已核验；本轮未获得符合条件的非算法完整 JD |
| 京东 | https://zhaopin.jd.com/ | ✅ | 发现 Agent 开发工程师官方 JD |
| 拼多多 / PDD | https://careers.pddglobalhr.com/ | △ | 官方招聘站已确认；本轮未发现符合范围的非算法完整 JD |
| 快手 | https://zhaopin.kuaishou.cn/ | ⟳ | 官方招聘入口已确认；相关职位详情需继续稳定核验 |
| 小红书 | https://job.xiaohongshu.com/campus | ⟳ | 官方招聘入口已确认；岗位列表动态，未以二手页补录 |
| 哔哩哔哩 | https://www.bilibili.com/blackboard/join-list.html | ⟳ | 官方职位页可访问但列表动态；未补二手 JD |
| 网易 | https://hr.163.com/ | ⟳ | 网易官方政策确认社招 hr.163.com / 校招 campus.163.com；需继续读取具体职位 |
| 携程 | https://careers.ctrip.com/ | ⟳ | 官方招聘体系已确认；本轮未稳定取得相关完整 JD |
| 滴滴 | https://careers.didiglobal.com/job | △ | 官方职位搜索已核验；未发现符合范围的当前职位 |
| 小米 | https://hr.xiaomi.com/website/opportunities.html | △ | 官方站已核验；本轮未发现符合范围的非算法完整 JD |
| 华为 | https://career.huawei.com/ | △ | 官方站已核验；AI 热招存在，但本轮未获得符合范围的非算法 Agent JD |
| OPPO | https://careers.oppo.com/ | ⟳ | 官方招聘入口已确认；职位详情需继续稳定核验 |
| vivo | https://hr.vivo.com/ | △ | 官方站已核验；未发现符合范围的当前完整 JD |
| 360 | https://hr.360.cn/ | ⟳ | 官方职位详情可访问但部分字段动态；继续追具体 Agent JD |
| 金山办公 / WPS | https://join.wps.cn/ | ⟳ | 官方 WPS 页面可追到招聘 ATS；本轮未稳定取得符合范围的完整 JD |
| 荣耀 | https://www.honor.com/cn/career/ | △ | 官方站已核验；展示的重点 AI 岗以算法方向为主 |
| 得物 | https://www.dewu.com/ | ⟳ | 官网存在“加入得物”入口；具体职位系统需继续追踪 |
| Shopee | https://careers.shopee.sg/ | ? | 纳入互联网平台扩展覆盖，下一轮优先确认中国 / 研发岗位官方入口 |

### 头部 AI / AI Native 公司

| 公司 | 官方招聘 / 公司入口 | 状态 | 本轮结论 |
|---|---|:---:|---|
| DeepSeek | https://deepseek.com/ | ⟳ | 官网明确链接 Careers / talent.deepseek.com；详细职位列表需继续稳定读取 |
| 月之暗面 / Kimi | https://careers.kimi.com/social | ⟳ | 官网 Careers 直接链接官方 Moka ATS；ATS 本轮重定向不稳定 |
| MiniMax | https://www.minimax.cn/careers | ⟳ | 官网直接链接 MiniMax 飞书招聘 ATS；具体职位列表需继续解析 |
| 智谱 / Z.ai | https://www.zhipuai.cn/zh/joinus | △ | 官方招聘页已核验；当前页面职位分类以算法 / 训练框架等为主 |
| 阶跃星辰 | https://www.stepfun.com/ | ? | 公司官网已核验，尚未找到稳定的官方招聘职位入口 |
| 百川智能 | https://www.baichuan-ai.com/ | △ | 官网提供官方招聘联系渠道，但没有可直接核验的详细 Agent JD |
| 零一万物 | https://www.01.ai/ | △ | 官网存在“加入我们”入口，本轮未取得符合范围的完整官方 JD |
| 商汤科技 | https://www.sensetime.com/cn/join-us | △ | 官方 Agent 热招方向当前主要是研究 / 算法岗位，按规则排除 |
| 科大讯飞 | https://www.iflytek.com/cn/ | ⟳ | 官方招聘体系存在，具体 ATS 与目标职位需继续从官网闭环核验 |
| 生数科技 | https://www.shengshu-ai.com/ | ? | 下一轮优先确认官方招聘入口与职位系统 |
| 硅基流动 | https://siliconflow.cn/ | ? | 官网已核验产品与公司主体，尚未找到公开招聘职位入口 |
| 面壁智能 | https://www.modelbest.cn/ | △ | 官网提供 career@modelbest.cn，但没有详细可核验 Agent JD |
| Manus | https://manus.im/ | △ | 官网明确正在全球招聘，但本轮未发现可直接读取的具体岗位 JD |
| LiblibAI | https://www.liblib.art/us/joinus | ✅ | 官方 Join Us 页面有 AI Agent 研发工程师完整 JD |
| 无问芯穹 / Infini-AI | https://www.infini-ai.com/ | ? | 纳入 Agent / AI Infra 扩展覆盖；下一轮优先补官方招聘入口 |
| 昆仑万维 / 天工 | https://www.kunlun.com/ | ? | 纳入头部 AI 应用公司扩展覆盖；下一轮优先确认官方招聘入口 |

> 覆盖矩阵是固定检查清单。公司即使当前 0 个合格岗位，也不会从矩阵里删除。

---

## 3. 当前 Active 官方 JD 快照

**官方 Active JD：18 个 Role Family**

- AI 应用开发：**4**
- Agent / 智能体研发：**14**
- 有合格 Active JD 的公司：**4**（百度、腾讯、京东、LiblibAI）

固定公司覆盖矩阵：**39 家**。

- ✅ 已找到合格官方 Active JD：**4 家**
- △ 官方招聘站已核验，本轮暂无合格非算法 JD：**14 家**
- ⟳ 官方招聘系统已确认、详情待稳定重试：**15 家**
- ? 官方招聘职位入口仍待补齐：**6 家**

旧基线的 47 条岗位不再沿用：凡来源不是第一手官方职位页的记录均已从 Active 主清单删除。

---

# AI 应用开发

## 百度｜大模型应用研发工程师（J103341）

- 分类：AI 应用开发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/a5ff8d15-b547-4a87-ba55-a128dae953cd

**官方职责要点**

- 建设企业开放平台及面向 Agent 的企业能力开放底座；
- 建设 API、CLI、Skill 从注册、生成、发布、调用到治理与效果评估的工具链；
- 使用大模型完成 API 分析、接口适配、代码 / 文档生成与能力质量检测；
- 建设面向 Agent 的组织知识与项目上下文能力。

**官方要求要点**

- 计算机 / AI 等相关专业本科及以上；
- Java / Python / Go 至少一种；
- 熟悉大模型应用开发和 Agent 工程框架；
- 具备系统设计、抽象和工程交付能力。

## 百度｜北京-大模型研发工程师（J100679）

- 分类：AI 应用开发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/GRADUATE/66a12645-f0f1-435c-8426-9fb91f1be330

**官方职责要点**

- 研发大模型应用系统、推理服务、工具链和数据工程管道；
- 将大模型能力集成到业务产品，建设 RAG、Agent 等 AI 应用；
- 优化模型调用链路的响应速度与稳定性；
- 推进大模型工程化最佳实践。

**官方要求要点**

- 本科及以上，计算机 / 软件工程相关专业优先；
- 熟练 Python；
- 有大模型 API 调用与应用开发经验；
- 理解 RAG、Agent、Prompt Engineering；
- Docker / Kubernetes 经验加分。

## 百度｜AI 开放平台研发工程师实习生（J103363）

- 分类：AI 应用开发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/INTERN/ef30e579-2d3d-4539-ad90-884521b815c9

**官方职责要点**

- 将大模型、Agent、API、CLI、Skill 封装为企业级服务；
- 开发 API 网关、鉴权配额、能力注册、调用链路和日志监控；
- 建设 Agent Tool、Skill、MCP 开放能力接入框架；
- 参与模型路由、上下文管理、流式响应、Function Calling、限流缓存等调用中间层。

**官方要求要点**

- 扎实的计算机基础；
- 熟练 Java / Spring Boot；
- 熟悉 MySQL、Redis；
- Agent、RAG、Function Calling、MCP 项目经验加分。

---

## 百度｜后端研发工程师（智能体 / AIGC 业务）（J94546）

- 分类：AI 应用开发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/a2876e5d-b3f5-4a50-bdbd-7eb0cef0e356

**官方职责要点**

- 负责智能体在 B/C 端、AIGC、数字人等业务的后端架构设计与实现；
- 持续优化框架架构、性能与可靠性；
- 保障线上系统稳定并沉淀工程最佳实践；
- 与产品、策略、设计团队协同，把 AI 能力落到业务系统。

**官方要求要点**

- 本科及以上，计算机相关专业；
- 具备多年后端研发经验，熟练 Golang；
- 熟悉数据库、消息队列、缓存和分布式系统；
- 大模型应用开发经验优先。

---

# Agent / 智能体研发

## 百度｜2027 AIDU - Agent应用全栈工程师（J99974）

- 分类：Agent / 智能体研发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/GRADUATE/6f9c3a86-6557-409d-8fa7-e6f4c68d6765

**官方职责要点**

- 构建 Autonomous Agent；
- 设计 Planning → Acting → Reflection 闭环；
- 建设 Tool / API、Memory、多轮推理与状态管理；
- 探索 Multi-Agent；
- 融合 RAG + Agent，并建设成功率、稳定性、成本、延迟等 Eval。

**官方要求要点**

- 深度使用主流 LLM；
- 有 Agent / 自动化工具 / 智能助手项目实践；
- 使用过主流 Agent 框架；
- 强调快速实验与工程落地。

## 百度｜云原生 Agent Infra 高级研发工程师（J100117）

- 分类：Agent / 智能体研发
- 地点：北京 / 上海
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/4b326f6b-2c39-461c-ae64-69b4201c680e

**官方职责要点**

- 研发 Agent 沙箱、网关、可观测等规模化运行基础设施；
- 建设多租户安全隔离、资源管控、网络接入与安全防护；
- 建设 Multi-Agent 与海量 Agent 沙箱的编排、调度、观测和自动恢复；
- 提供 CLI、MCP、SDK、Skill 等 Agent-Ready 接口与开发体验。

**官方要求要点**

- Go / Python / C++ 至少一种；
- 网络、操作系统、Linux 与系统设计基础扎实；
- 熟悉 Kubernetes、容器 / 沙箱与分布式系统；
- 理解 Agent 执行、工具调用、上下文、Skill / MCP / Plugin；
- 有生产级 Agent / Agentic Workflow 经验优先。

## 百度｜客户端研发工程师（PC + Mobile，DuMate Agent）（J103883）

- 分类：Agent / 智能体研发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/3b07fd0b-8dc0-419a-b804-f3c94d709e18

**官方职责要点**

- 开发百度搭子 DuMate 的 PC 与 Mobile 下一代通用智能体客户端；
- 覆盖 Windows / macOS / Linux、Android / iOS / 鸿蒙等多端；
- 调研和落地 Agent Harness 等前沿 Agent 技术；
- 参与需求、系统设计、研发、集成测试、部署和运行维护。

**官方要求要点**

- 具备桌面端或移动端软件开发经验；
- 多端 / 全栈经验优先；
- 熟悉 Go / TypeScript，或 Swift / Kotlin；
- 掌握大模型与 Agent 应用开发相关技术。

## 百度｜智能体客户端研发工程师（J103289）

- 分类：Agent / 智能体研发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/ecb74d60-fc3c-4d49-8934-fa0c51869cce

**官方职责要点**

- 研发 DuMate 下一代 Agent 客户端、工具和基础设施；
- 调研和落地 Agent Infra / Agent Harness；
- 参与系统设计、软件研发、集成测试、部署和运行维护；
- 优化客户端 Agent 产品体验。

**官方要求要点**

- 操作系统、网络、数据库基础；
- Go / TypeScript 等工程语言；
- Windows / macOS / Linux 桌面开发经验优先；
- 掌握大模型 / Agent 应用开发技术。

## 百度｜智能体研发工程师（J84599）

- 分类：Agent / 智能体研发
- 地点：北京 / 上海
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/f5c06e32-856c-4cae-81e2-8d09669ae78d

**官方职责要点**

- 建设商业智能体系统基础架构和 Multi-Agent 协同；
- 提升系统稳定性与扩展性；
- 建设智能体实验、仿真、评估与回溯能力；
- 建设 Agent 生产、应用与反馈的数据流通路和迭代体系。

**官方要求要点**

- Python / C++ 至少一种；
- 网络、多线程、分布式和高并发系统经验；
- 熟悉 SQL、Redis、Hadoop 等基础工具；
- 强调工程问题分析与跨团队协作。

## 百度｜智能体应用开发实习生（J99649）

- 分类：Agent / 智能体研发
- 地点：北京 / 上海
- 官方来源：https://talent.baidu.com/jobs/detail/INTERN/e3cec5b8-b7a3-4946-99fc-b292b749cd53

**官方职责要点**

- 开发混合云场景的大模型智能体应用；
- 基于代码库构建结构化知识，支持代码理解、问题溯源和根因分析；
- 用 Agent 分析代码质量和研发效能；
- 探索 AI Coding、代码生成、自动测试和自动部署。

**官方要求要点**

- Python / Java / Go 任一种；
- 掌握 RAG、Prompt、知识图谱基础；
- 熟悉 LangChain / LlamaIndex 等 Agent 编排框架；
- 有 Code Agent / AI Coding 实践优先。

## 百度｜伐谋-Agent研发工程师（J99560）

- 分类：Agent / 智能体研发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/75d3af47-7f79-4d71-862b-6fbca577bb19

**官方职责要点**

- 建设长程任务规划、工具调用、代码执行、状态管理等 Agent 执行框架；
- 建设自我演化 Agent 系统的任务采样、调度、回传与实验管理链路；
- 建设代码任务执行环境与自动评测系统；
- 支撑多租户、任务编排、资源管理和权限控制的云端产品落地。

**官方要求要点**

- Go / Python 至少一种；
- 分布式、任务调度或复杂业务系统经验；
- Kubernetes、容器、存储、网络与资源管理经验；
- 能独立完成模块设计、开发、测试和上线。

## 百度｜Agent后端研发工程师（J103882）

- 分类：Agent / 智能体研发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/d1876313-6604-4e8d-bbcc-0dca5be4e51b

**官方职责要点**

- 研发 DuMate 智能体云上基础设施；
- 建设推理链路、Agent 网关、高性能链路和数据闭环系统；
- 调研和落地 Agent Infra / Agent Harness；
- 覆盖需求、设计、研发、测试、部署和运维。

**官方要求要点**

- 熟悉 Go；
- 操作系统、网络、数据库基础；
- Agent Harness 云上基础服务经验优先；
- 了解大模型和 Agent 应用开发。

## 百度｜AI研发工程师（J100861）

- 分类：Agent / 智能体研发
- 地点：北京
- 官方来源：https://talent.baidu.com/jobs/detail/SOCIAL/740fc1e0-6539-4d81-8aa1-e0dbdc7a8e22

**官方职责要点**

- 建设面向研发效能的 Agent 能力；
- 构建支撑大规模工程协作的研发平台；
- 研发理解需求、自主编码、联调测试的智能编程 Agent；
- 建设 Agent 研发基础设施。

**官方要求要点**

- Java / Spring Boot；
- MySQL、Redis、Kafka；
- 熟悉 Agent 开发、大模型应用、云原生或 CI/CD 优先。

## 百度｜Agent Harness 研发工程师（北京 J100815 / 上海 J100779）

- 分类：Agent / 智能体研发
- 地点：北京 / 上海
- 官方来源（北京）：https://talent.baidu.com/jobs/detail/GRADUATE/8683fc23-9bff-4d25-84b2-f5ddce782c5a
- 官方来源（上海）：https://talent.baidu.com/jobs/detail/GRADUATE/74d83772-1bd0-42b9-8cc5-69eb45696b62

> 两个官方 Requisition 的职责主体高度一致，按一个 Role Family 计数。

**官方职责要点**

- 设计和开发 Agent Harness 产品技术架构；
- 建设状态管理、沙箱、反馈闭环、执行约束、上下文交接与关键信息 compaction；
- 从 Harness 视角联合优化 LLM 与系统行为，并验证不同 Harness 设计的真实影响；
- 建设 Human-Agent 协作与反馈闭环，提升长时间复杂任务的稳定性与可控性。

**官方要求要点**

- 理解 ReAct、CoT、Plan-and-Execute 等 Agent 机制；
- 熟悉 Agent 框架以及复杂文件读写、环境反馈、长任务执行等工程问题；
- 能分析并改良 Harness Failure；
- Agent / Harness 工程落地、开源贡献等经验优先。

## 腾讯｜Agent开发工程师（R108051）

- 分类：Agent / 智能体研发
- 地点：深圳
- 官方来源：https://tencent.wd1.myworkdayjobs.com/en-US/tencent_careers/job/China-Shenzhen/Agent_R108051-1

**官方职责要点**

- 承担 Agent 产品从架构、前后端、测试、部署到持续迭代的完整闭环；
- 建设企业知识库、RAG、Memory、Tool、MCP、Multi-Agent 与人机协作；
- 接入模型平台、身份权限、知识库和数据平台；
- 建设 Agent Benchmark、自动评测、Tracing、日志监控和反馈闭环；
- 建设 CI/CD、灰度、故障恢复、权限控制、审计和数据隔离。

**官方要求要点**

- 复杂系统 / 产品从 0→1 的软件研发经验；
- JavaScript / TypeScript 与前端工程能力；
- 能承担生产级 Agent 系统设计与完整交付。

## 腾讯｜AI Agent开发工程师（游戏研发）（R107498）

- 分类：Agent / 智能体研发
- 官方来源：https://tencent.wd1.myworkdayjobs.com/zh-CN/Tencent_Careers/job/AI-Agent--_R107498-2

**官方职责要点**

- 面向策划、程序、美术、测试、运营等游戏研发环节建设 AI Agent；
- 将 Agent 接入 Unreal Engine 5 与现有研发工具链；
- 把业务痛点抽象为可自动 / 半自动执行任务；
- 建立任务成功率、人工节省时长、生成质量、稳定性与安全性等评估指标。

**官方要求要点**

- 软件工程与系统集成能力；
- 能做 Agent 原型验证、技术选型和工具链工程化；
- 需要和策划、客户端、TA、美术等跨职能协作。

## 京东｜Agent开发工程师（Requisition 219990）

- 分类：Agent / 智能体研发
- 地点：北京
- 官方来源：https://zhaopin.jd.com/web/job-info-detail?requementId=219990

**官方职责要点**

- 研发和设计 O2O 上门服务核心系统；
- 将 AI 大模型用于智能匹配、用户画像、辅助方案生成和合规风险识别；
- 建设可复用服务组件与技术中台；
- 探索大模型在医疗健康业务的工程化应用。

**官方要求要点**

- 本科及以上，计算机 / 软件工程 / AI / 数据相关专业；
- 具备软件系统研发与工程实践能力；
- 岗位主体是业务软件 + AI 应用工程，不按算法岗收录。

## LiblibAI｜AI Agent研发工程师

- 分类：Agent / 智能体研发
- 地点：上海
- 官方来源：https://www.liblib.art/us/joinus

**官方职责要点**

- 开发稳定、高效的多模态视觉生成 Agent；
- 优化 Planner、Memory、MCP Tool 等 Agent 架构模块；
- 对通信、调度、存储系统进行工程选型并提升迭代效率；
- 将算法原型持续工程化，提升稳定性和用户体验；
- 独立负责业务分析、核心方案设计与代码实现。

**官方要求要点**

- 本科及以上计算机相关专业；
- Golang / Java / Python / C++ 至少一种；
- 了解 Agent 框架与架构实现；
- 有 Agent 应用落地经验优先。

---

## 4. 去重规则

- 同公司、同岗位主体、职责高度一致但仅城市不同：合并为一个 **Role Family**；
- 同 Role Family 的不同官方 Requisition 可以并列保留官方 ID / URL，但岗位计数只计 1；
- 不以职位标题关键词去重，必须比较实际职责；
- 二手来源不存在“降级保留”，只能删除或追到官方原页后重新入库。

---

## 5. 维护查询词

只在公司**官方招聘站**内使用：

`Agent研发`、`Agent开发`、`智能体研发`、`智能体开发`、`AI应用开发`、`AI应用研发`、`大模型应用开发`、`LLM应用开发`、`AI全栈`、`AI Backend`、`Applied AI Engineer`、`Agent Engineer`、`Agent Platform`、`Agent Runtime`、`Agent Infra`、`Agent Harness`、`Coding Agent`、`AI Native`、`RAG Engineer`、`LLMOps`、`MCP`、`Tool`、`Skill`。

---

## 6. 维护日志

### 2026-09-19｜First-party reset

- 将来源政策从“官方优先、二手可补 Recall/正式库”收紧为：**正式库 100% 第一手官方 JD**；
- 删除旧 47 条基线中所有二手 / 未完成官方 provenance 的 Active 记录；
- 使用公司官网与官网直连 ATS 重新建立 Active 清单；
- 当前官方 Active JD：**18 个 Role Family**；
- 建立固定公司覆盖矩阵，互联网大厂与头部 AI 公司即使 0 岗位也持续逐公司核验；
- 二手站以后只可作为 Recall 线索，永远不能进入正式 JD 证据。
