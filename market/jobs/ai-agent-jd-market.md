# 当前校招｜AI 应用开发 & Agent / 智能体研发官方 JD 市场库

> **正式口径：当前有效校园招聘 + 第一手官方来源 + 非算法工程岗。年份仅作备注，不作为筛选 Gate。**
>
> 搜索引擎、牛客、Boss、猎聘、智联、实习僧、JDWatch、聚合站、媒体/社交转载均为 **0 正式证据**。动态官网必须通过官方项目页 / ATS / 招聘 API 做站内枚举，不能把搜索引擎 0 命中解释成“无岗位”。

## 1. 两层数据模型

```text
当前官方校园招聘页 / 官方 ATS / 官方招聘 API
        ↓ 全量枚举
official-2027-agent-jobs.generated.*
        ↓ 当前校招 + Role Scope + 非算法 Gate + Role Family 去重
ai-agent-jd-market.md
        ↓
当前正式 Agent / AI应用工程 JD
```

- [机器发现候选池](official-2027-agent-jobs.generated.md)：尽可能全量抓官方动态校招站，允许边界岗。
- 本文件：二次审核后的正式核心库。
- `⟳` 表示未知/待闭环，不等于“暂无岗位”。

## 2. 正式纳入 Gate

必须同时满足：官方第一手；当前官方校招链接有效；工程开发岗；岗位主责为 Agent/智能体/AI应用/大模型应用/Coding Agent/RAG Application/Agent Harness/Runtime/Infra；模型训练/算法研究不是岗位主体。

同公司、职责高度一致但城市/职位 ID 不同，合并为一个 Role Family。

## 3. 当前快照｜2026-09-19

- **正式当前校招 Role Family：38**
- **AI 应用开发：13**
- **Agent / 智能体研发：25**
- **已进入正式库的公司：10 家**：小米、快手、百度、OPPO、美团、顺丰、阿里巴巴、小红书、商汤科技、MiniMax。
- **固定官方公司覆盖：42 家**；每家公司都维护 `official_root` 与固定 `job_list_url`。
- 日常采集不再依赖搜索引擎索引：直接打开固定官方职位页，穷举 Agent / 智能体 / AI 应用 / 大模型应用 / Coding Agent / RAG / Harness / Runtime / MCP / Skill / Tool 等关键词并翻完分页。
- 专用 API / Feishu / Moka 只作为加速器；失败时必须回退固定 `job_list_url`，不能把接口失败解释成“0 岗位”。

## 4. 公司当前校招官方覆盖矩阵

这里现在只回答一个问题：**当前官网校招职位池能否稳定获取并完整枚举**。年份、毕业窗口和项目名只作为备注，不参与筛选。\n\n| 公司 | 固定官方职位列表页 | 获取方式 | 当前校招状态 |
|---|---|---|---|
| 小米 | https://xiaomi.jobs.f.mioffice.cn/campus/ | xiaomi_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 快手 | https://campus.kuaishou.cn/recruit/campus/e/ | kuaishou_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 百度 | https://talent.baidu.com/jobs/list?projectType=1 | baidu_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 腾讯 | https://join.qq.com/post.html | tencent_campus_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 美团 | https://zhaopin.meituan.com/web/campus | meituan_campus_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 网易 | https://campus.163.com/ | netease_api 加速 → 固定职位页浏览器兜底 | △ 职位可获取；届别需官方 JD/项目证据 |
| 哔哩哔哩 | https://jobs.bilibili.com/campus/positions | bilibili_api 加速 → 固定职位页浏览器兜底 | △ 职位可获取；届别需官方 JD/项目证据 |
| 滴滴 | https://campus.didiglobal.com/campus_apply/didiglobal/96064#/jobs | 固定职位页 → 通用浏览器穷举 | ✅ 2027 已确认 |
| 拼多多 | https://careers.pddglobalhr.com/campus/grad | pdd_campus_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 华为 | https://career.huawei.com/cn/campus-recruitment | huawei_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 小红书 | https://job.xiaohongshu.com/campus/position | xiaohongshu_2027_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 字节跳动 | https://jobs.bytedance.com/campus/position | bytedance_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 阿里巴巴 | https://campus-talent.alibaba.com/campus/position?batchId=100000760001 | alibaba_campus_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 蚂蚁集团 | https://talent.antgroup.com/campus-full-list | ant_2027_api 加速 → 固定职位页浏览器兜底 | △ 职位可获取；届别需官方 JD/项目证据 |
| 京东 | https://campus.jd.com/ | jd_campus_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| OPPO | https://careers.oppo.com/university/oppo/campus/post?recruitType=Graduate | oppo_campus_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| vivo | https://hr-campus.vivo.com/campus/jobs | vivo_2027_api 加速 → 固定职位页浏览器兜底 | △ 职位可获取；届别需官方 JD/项目证据 |
| 金山办公/WPS | https://join.wps.cn/ | 固定职位页 → 通用浏览器穷举 | ✅ 2027 已确认 |
| 荣耀 | https://career.honor.com/SU60eea919bef57c1023f6fe78/pb/school.html | honor_2027_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 科大讯飞 | https://iflytek.zhiye.com/5/jobs | iflytek_2027_api 加速 → 固定职位页浏览器兜底 | △ 职位可获取；届别需官方 JD/项目证据 |
| 携程 | https://careers.ctrip.com/#/campus | ctrip_2027_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 360 | https://hr.360.cn/hr/list | 固定职位页 → 通用浏览器穷举 | — 官网当前未公开 2027 项目 |
| 得物 | https://poizon.jobs.feishu.cn/578078/ | feishu_direct 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| DeepSeek | https://talent.deepseek.com/ | 固定职位页 → 通用浏览器穷举 | — 官网当前未公开 2027 项目 |
| 月之暗面/Kimi | https://app.mokahr.com/apply/moonshot/148506 | 固定职位页 → 通用浏览器穷举 | △ 职位可获取；届别需官方 JD/项目证据 |
| MiniMax | https://vrfi1sk8a0.jobs.feishu.cn/379481/?project=7495675705720965415 | feishu_direct 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 智谱/Z.ai | https://www.zhipuai.cn/zh/joinus | 固定职位页 → 通用浏览器穷举 | △ 职位可获取；届别需官方 JD/项目证据 |
| 阶跃星辰 | https://app.mokahr.com/campus-recruitment/step/94905 | 固定职位页 → 通用浏览器穷举 | △ 职位可获取；届别需官方 JD/项目证据 |
| 百川智能 | https://cq6qe6bvfr6.jobs.feishu.cn/646926/?project=7676396828845639987 | feishu_direct 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 零一万物/01.AI | https://01ai.jobs.feishu.cn/index/ | feishu_direct 加速 → 固定职位页浏览器兜底 | — 官网当前未公开 2027 项目 |
| 商汤科技 | https://hr-jobs.sensetime.com/edu/ | feishu_direct 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 生数科技 | https://www.shengshu-ai.com/ | 固定职位页 → 通用浏览器穷举 | — 官网当前未公开 2027 项目 |
| 硅基流动 | https://www.siliconflow.cn/ | 固定职位页 → 通用浏览器穷举 | — 官网当前未公开 2027 项目 |
| 面壁智能 | https://www.modelbest.cn/ | 固定职位页 → 通用浏览器穷举 | — 官网当前未公开 2027 项目 |
| Manus | https://www.manus.im/ | 固定职位页 → 通用浏览器穷举 | — 官网当前未公开 2027 项目 |
| LiblibAI | https://www.liblib.art/us/joinus | 固定职位页 → 通用浏览器穷举 | — 官网当前未公开 2027 项目 |
| 无问芯穹/Infini-AI | https://infinigence.jobs.feishu.cn/088717 | feishu_direct 加速 → 固定职位页浏览器兜底 | △ 职位可获取；届别需官方 JD/项目证据 |
| 昆仑万维/天工 | https://jobs.kunlun.com/459522/position/list | 固定职位页 → 通用浏览器穷举 | △ 职位可获取；届别需官方 JD/项目证据 |
| Shopee | https://careers.shopee.cn/jobs?limit=50&offset=0 | 固定职位页 → 通用浏览器穷举 | — 官网当前未公开 2027 项目 |
| 联想 | https://talent.lenovo.com.cn/position?jobTypeName=AI%E5%BC%80%E5%8F%91%E7%B1%BB&projectType=1 | lenovo_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |
| 蔚来 | https://nio.jobs.feishu.cn/campus/ | feishu_direct 加速 → 固定职位页浏览器兜底 | △ 职位可获取；届别需官方 JD/项目证据 |
| 顺丰 | https://campus.sf-express.com/positionList | sf_campus_api 加速 → 固定职位页浏览器兜底 | ✅ 2027 已确认 |

> 公司当前没有公开校招职位池时仍保留在矩阵；官方校招入口重新开放后直接在同一个固定入口继续枚举。

## 5. AI 应用开发｜当前校招 Active 官方 JD

### 快手｜AI应用开发工程师

- **校招项目备注**：快手官方2027项目 20271779425607
- **官方职位 / ID**：AI应用开发工程师 / `13150`
- **地点**：杭州 / 北京
- **官方职位页**：
- https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/13150?code=dd3c94b2618e48e48146a46c98d25c10&recruitSubProjectCodes=20271779425607

**官方职责**

- 1、参与AI应用的全栈开发，用于解决生产场景的一系列复杂问题，赋能业务，实现高ROI的业务指标提升，以及全流程提升产研效能，保障业务稳定性，改进提高系统性能等；
- 2、开发适用于生产场景的 MultiAgent 系统，探索 MultiAgent 上下文工程的最佳实践，解决将 MultiAgent 应用于产品时遇到的最棘手的挑战；
- 3、探索前沿AI技术，包括但不限于多模态大模型、Agent架构设计、RAG技术优化、工具调用链路设计等，并快速构建原型验证技术可行性；
- 4、跟踪AI技术发展趋势，深度研究相关产品、开源项目、前沿论文，提炼核心技术要点并在团队中分享，推动技术创新应用。

**官方要求**

- 1、本科及以上学历，计算机科学、软件工程、人工智能、数据科学等相关专业优先；
- 2、熟悉至少一种编程语言（如 Java、Python 等），具备一定的编程基础，了解常见的数据结构与算法，能独立完成代码编写与调试；
- 3、熟悉 AI 产品的使用逻辑与应用场景，有 AI 工具使用经验，对 AI 技术有浓厚兴趣；
- 4、了解Agent核心组件（如 Chains、Agents、Memory等）的使用场景与实现原理；
- 5、了解 prompt engineering 的基本原理与方法，能根据具体任务设计有效的提示词，提升 AI 模型的任务完成效果。
- 加分项
- 1、有AI相关项目经验或互联网公司实习经历，特别是大模型应用、Agent开发、多模态应用等实践经验；
- 2、有深度学习/机器学习相关的科研和探索经历，有相关竞赛获奖经历；

### 快手｜AI应用服务端开发工程师

- **校招项目备注**：快手官方2027项目 20271779425607
- **官方职位 / ID**：AI应用服务端开发工程师 / `13115`
- **地点**：北京
- **官方职位页**：
- https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/13115?code=721e12629eed4095872ba6c8d389c3d5&recruitSubProjectCodes=20271779425607

**官方职责**

- 1、负责AI工程化落地，利用提示词工程，微调等一系列技术，解决将大模型用于生产场景的一系列复杂问题，平衡效果，成本，速度；
- 2、开发适用于生产场景的Agent系统，探索Agent提示词工程的最佳实践，解决将Agent应用于产品时遇到的最棘手的挑战；

**官方要求**

- 1、本科及以上学历，具备扎实的计算机专业基础，比如操作系统、计算机体系结构等；
- 2、熟练掌握C/C++/Java/python，具备优秀的编程素养，对代码质量追求极致；
- 3、思维严谨，逻辑清晰，有强烈的技术热情，工作责任感强；
- 4、日常熟练使用各种AI工具，对大模型的工作原理有一定了解；
- 5、了解提示词工程，有Agent系统开发经验的优先；

### 快手｜【快Star】AI应用开发工程师

- **校招项目备注**：快手官方2027项目 20271779425607
- **官方职位 / ID**：【快Star】AI应用开发工程师 / `12779`
- **地点**：北京
- **官方职位页**：
- https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/12779?code=ea8ab823cff346b5861e92a5d5e01c63&recruitSubProjectCodes=20271779425607

**官方职责**

- 1、业务链路的 AI 化设计：深入理解业务核心链路，识别 AI 切入点与价值杠杆,主导从场景判断、范式选型(LLM / VLM / 多模态生成 / 垂类模型 / Agent 编排)到链路改造的端到端方案落地；
- 2、模型的"本土化"驯服：针对业务特有的内容生态、用户行为与合规口径,设计 Prompt、RAG、SFT、偏好对齐等多种知识注入路径的组合策略；搭建 Bad Case 驱动的数据飞轮与业务感知评测体系，让模型在真实业务分布上持续进化；
- 3、部署方案的调优：在效果、实时性、成本三者之间为业务找到稳态——主导分层部署(在线/异步/离线)、推理加速与压缩(量化/蒸馏/投机解码/语义缓存)、在离线协同链路设计，保障核心场景 P99 与首 Token 的 SLO；
- 4、稳定性与可演进性：建立 AI 链路的灰度、回滚、多版本并存机制，让 AI 服务的发布节奏与业务发布流程对齐；沉淀可复用的工程范式与方法论,支撑业务持续规模化。

**官方要求**

- 1、计算机、人工智能、统计学等相关专业本科及以上学历,3 年以上算法或 AI 工程相关经验；
- 2、熟悉 LLM / VLM / 多模态模型的能力边界与典型范式，有过将通用大模型落地到具体业务、并取得可度量业务收益的完整项目经验；
- 3、精通 Prompt Engineering、RAG、SFT、偏好对齐中的至少两项,对各自适用边界有清晰判断，反对"一招鲜"；
- 4、熟悉模型推理加速与压缩的主流技术栈(量化、蒸馏、投机解码、KV Cache、语义缓存等)，理解每种手段的效果代价；
- 5、具备扎实的工程素养,能独立完成从离线实验、在线部署到 SLO 保障的完整闭环，具备处理高并发、低延迟在线服务的实战经验；
- 6、数据敏感,擅长把模糊的业务问题拆解为可度量的指标与可证伪的实验，反感"故事化"归因。
- 加分项：
- 1、主导过亿级流量在线 AI 服务的部署与稳定性治理；

### 百度｜大模型应用研发工程师（RAG / Agent）

- **校招项目备注**：百度当前校园招聘=2027届
- **官方职位 / ID**：上海-大模型研发工程师(J100835) / `76a527f1-ddc9-4b52-aa11-7cd96e52f5d9`；北京-大模型研发工程师(J100679) / `c8af44f4-9837-48bc-94f0-736c003b3180`
- **地点**：上海市 / 北京市
- **官方职位页**：
- https://talent.baidu.com/jobs/detail/GRADUATE/76a527f1-ddc9-4b52-aa11-7cd96e52f5d9
- https://talent.baidu.com/jobs/detail/GRADUATE/c8af44f4-9837-48bc-94f0-736c003b3180

**官方职责**

- -负责大模型应用系统的研发，包括大模型推理服务、工具链、数据工程管道等
- -与算法团队协作，将大模型能力快速集成到业务产品，构建RAG、Agent等AI应用
- -设计并优化大模型调用链路，提升系统响应速度与稳定性
- -参与大模型数据工程建设，推动训练数据质量提升
- -关注大模型工程化前沿（如vLLM、LangChain），推动最佳实践落地

**官方要求**

- -本科及以上学历，计算机、软件工程等相关专业优先
- -熟练掌握Python，有大模型API调用与应用开发经验
- -了解RAG、Agent、Prompt Engineering等大模型应用技术
- -有大模型工程化或AI应用开发实习经历者优先
- -熟悉Docker、Kubernetes等容器化技术者优先

### OPPO｜AI工程师（AI应用方向）

- **校招项目备注**：2027届应届生校园招聘
- **官方职位 / ID**：AI工程师（AI应用方向） / `1819`
- **地点**：成都市,深圳市
- **官方职位页**：
- https://careers.oppo.com/university/oppo/campus/post/1819

**官方职责**

- 方向一：负责推荐相关能力迭代、产品基础体验优化，参与端侧架构优化及演进；
- 方向二：负责记忆产品的开发，基础体验提升与业务架构演进，持续提升个性化产品竞争力

**官方要求**

- 1.计算机、通信、电子信息、通信工程、软件工程等相关专业；
- 2.熟悉Java/Kotlin语言，深刻理解算法和数据结构相关知识；
- 3.熟悉TCP/IP，HTTP，HTTPS等网络协议；
- 4.热爱互联网，对互联网产品和技术有浓厚的兴趣；
- 5.具备优秀的分析问题和解决问题的能力，对解决具有挑战性的问题充满激情；
- 6.学习能力强，具有良好的沟通能力和良好的团队合作精神；
- 我们更希望你：
- 1.有Android项目开发经验；

### OPPO｜IT开发工程师（AI应用方向）

- **校招项目备注**：2027届应届生校园招聘
- **官方职位 / ID**：IT开发工程师（AI应用方向） / `1807`
- **地点**：东莞市
- **官方职位页**：
- https://careers.oppo.com/university/oppo/campus/post/1807

**官方职责**

- 1、负责营销/供应链/研发/财务/HR/办公等IT产品AI升级重构中的技术方案设计及落地，主要包含相关AI/Agent智能体的技术设计、工程实现与效果测试等工作；
- 2、协助产品经理完成AI场景落地可行性分析，主要包含场景落地关键AI相关技术难点识别、技术预研等工作；
- 3、参与营销/供应链/研发/财务/HR/办公等IT产品的建设工作，主要包含系统架构设计、方案设计、开发实现等工作。

**官方要求**

- 1、计算机、人工智能、通信、电子信息、通信工程、软件工程等相关专业；
- 2、熟悉Java/Python编程语言，编程功底扎实，熟悉Web网络编程及常用中间件的使用（Redis/RocketMQ/MySQL）；
- 3、对大模型使用/应用有一定的了解，了解MCP、A2A协议，具备良好提示词撰写/优化思路；
- 4、逻辑清晰，独立思考，乐于学习了解新事物；具备一定的AI思维，善于利用AI解决问题。
- 5、懂AI功能实现，懂AI的基本原理，掌握编程能力，能调用，能做算法复现

### 美团｜AI应用开发工程师

- **校招项目备注**：美团官方当前校园招聘正式岗（届别需主库复核）
- **官方职位 / ID**：AI应用开发工程师 / `4694862735`
- **地点**：北京市 / 上海市
- **官方职位页**：
- https://zhaopin.meituan.com/web/position/detail?jobUnionId=4694862735&highlightType=campus

**官方职责**

- 岗位职责
- 1. 参与大模型应用、Agent应用、企业内部AI工具等产品的研发与落地。
- 2. 基于大模型API、RAG、工具调用、工作流编排等能力，构建可用、稳定、可迭代的AI应用。
- 3. 与产品、算法、数据、业务团队合作，将真实业务场景转化为AI解决方案。
- 4. 负责AI应用的后端服务、接口设计、数据处理、效果监控与持续优化。

**官方要求**

- 岗位要求
- 1. 2026/2027届本科及以上学历，计算机、软件工程、人工智能、数据科学等相关专业优先。
- 2. 熟悉至少一门编程语言，如Python、Go、Java、TypeScript。
- 3. 具备扎实的软件工程基础，理解常见后端开发、数据库、接口设计和系统部署。
- 4. 了解 Prompt、RAG、Function Calling、Agent、Embedding、MCP协议等基础概念。
- 5. 具备较强的问题拆解能力，能把业务需求转化为工程方案。

### 小米｜AI研发工程师-智能风控方向

- **校招项目备注**：2027届校园招聘计划 / 正式
- **官方职位 / ID**：AI研发工程师-智能风控方向 / `7671289294427113737`
- **地点**：北京
- **官方职位页**：
- https://xiaomi.jobs.f.mioffice.cn/campus/position/7671289294427113737/detail

**官方职责**

- 1、参与建设面向零售、服务、整车等业务的 AI 风控工作流与应用平台，围绕风险主动发现、特征与数据分析、风险识别、策略生成与上线、监控复盘、客诉分析与处置辅助等场景，形成端到端闭环。
- 2、基于 LangGraph、LangChain、AutoGen 等 Agent 框架及工作流编排能力，设计并实现具备任务规划、工具调用、知识检索、状态管理和人工审核能力的智能风控应用，提升风险分析、策略运营和案件处置效率。
- 3、以 MCP 为核心建设风控工具生态，标准化接入数据仓库、特征与标签平台、策略平台、规则引擎、案件系统、监控告警、知识库及内部服务，保障工具调用的权限控制、审计追踪、稳定性和可维护性。
- 4、结合 RAG、结构化检索、SQL 分析及现有算法能力，建设风险知识库和分析助手，支持异常线索挖掘、风险归因、特征分析、策略效果评估和运营决策辅助。
- 5、与产品、算法、运营及业务团队协同，将实际业务问题拆解为可落地的 AI 工作流；持续优化模型调用效果、工具成功率、流程时效和人工提效，并推动应用稳定上线。

**官方要求**

- 1、计算机基础扎实，熟练使用 Python，至少掌握一门后端开发语言（Go、Java、C++、Rust 等）；熟悉 Git、Linux、数据库、接口开发及容器化部署。
- 2、有大模型应用、Agent 或工作流平台相关项目经验，熟悉 LangGraph、LangChain、AutoGen、LlamaIndex 等任一框架；理解 MCP、Function Calling、RAG、Prompt Engineering、Memory、Workflow Orchestration 等方法，并能够独立完成应用落地。
- 3、具备较好的工程化能力，能够设计和实现稳定、可扩展、可观测的服务；了解工具调用鉴权、日志审计、异常降级、评测与监控等机制。
- 4、具备数据分析与问题定位能力，熟悉 SQL、数据处理及常见检索方案；能够围绕风险线索、策略效果、工具调用链路和用户反馈提出可量化的优化方案。
- 5、对风控、反作弊、智能运营或企业级 AI 应用有兴趣；具备良好的沟通与协作能力，能够与产品、算法、运营和业务团队共同推进复杂问题落地。
- 6、有风控、反作弊、策略平台、数据平台、RAG/MCP/Agent 应用或多系统集成经验者优先。

### 小米｜AI属性工程师-汽车

- **校招项目备注**：2027届校园招聘计划 / 正式
- **官方职位 / ID**：AI属性工程师-汽车 / `7670918768222570803`
- **地点**：南京
- **官方职位页**：
- https://xiaomi.jobs.f.mioffice.cn/campus/position/7670918768222570803/detail

**官方职责**

- 负责将大模型、智能体等AI能力落地至整车研发流程，提升工程团队研发效率。具体包括：
- 1. 基于业务场景构建AI Agent，实现重复性工作的自动化接管；
- 2. 针对不同工程领域定制Prompt模板，建设可复用的Skills库；
- 3. 维护部门级AI中台底座，保障AI工具链的稳定性与持续迭代；
- 4. 识别高频事务性工作，设计并开发自动化工作流；

**官方要求**

- 1. 本科及以上学历，计算机科学、人工智能、软件工程等相关专业；
- 2. 具备LLM应用开发实战经验，熟悉Prompt Engineering、Agent框架、RAG技术；
- 3. 理解工程业务流程，能够将业务需求转化为技术方案；
- 4. 具备数据处理与分析能力，包括数据清洗、可视化、报表生成；
- 5. 具备快速学习能力，能跟进AI前沿技术并评估落地可行性；


### 阿里巴巴｜AI应用研发工程师

- **校招项目备注**：阿里巴巴官方 2027 校招批次
- **官方职位 / ID**：AI应用研发工程师 / `199907620013`
- **官方职位页**：https://campus-talent.alibaba.com/campus/position/199907620013?deptCodes=

**官方 JD 要点**

- 面向真实业务设计 AI Native 系统，将 Agent 的记忆、推理、工具编排、RAG 与现有业务系统连接；
- 落地意图识别、任务拆解、反思纠错、SDK/API 与 Agent 可观测体系；
- 建设自动评测 / 回测、Case 分析和高并发稳定性治理，推动 AI 从单点验证走向规模化应用；
- 要求具备扎实的软件工程能力，理解 Context / Prompt Engineering、Agent、Tool / Function Calling，并能使用主流编程语言完成生产级开发。

### 小红书｜Product Engineer（社区内容 AI Native）

- **校招项目备注**：小红书官方 2027 校园招聘 / REDstar
- **官方职位 / ID**：Product Engineer-产品工程师-社区内容方向 / `21861`
- **官方职位页**：https://job.xiaohongshu.com/campus/position/21861

**官方 JD 要点**

- 在创作发布、评论互动等核心内容场景建设 Agent 系统，负责 Context、Tool Use、Workflow、Memory / State、Eval 与 Observability；
- 探索生成式 UI、AI 原生内容分发 / 消费以及端到端 AI 应用架构；
- 强调全栈工程、复杂系统交付和 AI Native 产品从原型到规模化上线的能力。

### 小红书｜搜广推 × AI 应用工程师

- **校招项目备注**：小红书官方 2027 校园招聘 / REDstar
- **官方职位 / ID**：搜广推 × AI 应用工程师 / `21820`
- **官方职位页**：https://job.xiaohongshu.com/campus/position/21820

**官方 JD 要点**

- 负责搜索、推荐、广告、电商引擎与业务架构，并将 LLM / 多模态能力工程化为 AI 原生应用；
- 承担 AI 应用服务开发、链路性能优化和公共底层能力沉淀；
- 要求 Java / C++ 等工程能力，以及 RAG、Agent、Prompt / AI 链路系统化落地经验。

### 商汤科技｜FDE 工程师（企业级 AI 应用）

- **校招项目备注**：官方职位标题明确“27届校招”
- **官方职位 / ID**：FDE工程师-亚太业务事业群 / `7659254488749951258`、`7659255237010508078`
- **官方职位页**：
  - https://hr-jobs.sensetime.com/edu/position/7659254488749951258/detail
  - https://hr-jobs.sensetime.com/edu/position/7659255237010508078/detail

> 两个 Requisition 职责高度一致，按一个 Role Family 计数。

**官方 JD 要点**

- 面向客户项目开发和交付企业级 AI 应用，完成后端服务、系统集成、部署和问题排查；
- 集成大模型服务、RAG、Agent、知识库与 Workflow，并沉淀可复用工程组件；
- 要求 Python / Java / Go 等后端开发能力，熟悉 Web、数据库、缓存、Linux / Docker；Agent / RAG 实践为加分项。

## 6. Agent / 智能体研发｜当前校招 Active 官方 JD

### 快手｜AI Agent 全栈工程师-Agent 应用研发方向

- **校招项目备注**：快手官方2027项目 20271779425607
- **官方职位 / ID**：AI Agent 全栈工程师-Agent 应用研发方向 / `13836`
- **地点**：北京
- **官方职位页**：
- https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/13836?code=0f93d69bcf1143aaaaff2f6de0a769ec&recruitSubProjectCodes=20271779425607

**官方职责**

- 参与面向风控业务的 AI Agent 应用研发建设，覆盖智能研判、AI 排障、运营变更管控、研发提效等场景。在导师指导下，将复杂的安全治理 SOP 梳理为可执行的 Agent 工作流，参与构建 Agent 能力闭环。
- 1、Agent 应用研发：参与 AI Agent 的设计、开发与迭代，包括任务编排、Prompt 设计、工具调用、前后端联调及功能交付；支撑研判 Agent、网页自动化 Agent、AI-Oncall 等方向的业务落地；
- 2、工具链封装与集成：协助将风控平台、研判系统、变更管控、监控告警等平台能力封装为 Agent 可调用的 Tool / MCP / Skill，推进自动化工作流落地；
- 3、知识库建设：参与安全治理与风控领域知识库的搭建与优化，包括 SOP 文档处理、向量检索、混合检索、重排序及检索效果分析；
- 4、效果评估与迭代：协助构建评测集和评估链路，分析 Agent 的准确率、召回率、响应延迟和成本，并推动持续优化；
- 5、工程质量与稳定性：参与上下文管理、模型路由、异常兜底、日志监控等工程能力建设，保障服务的可用性与可维护性；
- 6、Harness 工程体系：参与前端 AI 研发范式（Harness Engineering）的落地与沉淀，探索 AI Native 架构下代码生成、需求描述、审查评估的最佳实践；
- 7、技术探索：跟踪 AI Agent、MCP、RAG、Browser Automation 等方向的技术进展，探索 AI 在安全治理工作流自动化中的创新应用，并沉淀实践经验。

**官方要求**

- 1、本科及以上学历，计算机、软件、信息等相关专业；
- 2、具备扎实的编程基础，熟悉至少一种主流开发语言，如 Python、Java、Go、JavaScript / TypeScript 等；
- 3、对 AI Agent、大语言模型应用或生成式 AI 有浓厚兴趣，有课程项目、个人项目、竞赛或开源实践者优先；
- 4、熟悉常见 AI 编程工具的使用，能够借助工具学习并解决实际工程问题；
- 5、了解 Harness、Loop Engineering、结构化输出、Function Calling / Tool Use 等基本概念，有相关实践更佳；
- 6、具备良好的学习能力、问题分析能力和沟通协作意识，能保证稳定的实习投入时间。
- 加分项：
- 1、有 LangChain、LangGraph、AutoGen 或其他 Agent 框架的实践经验；

### 快手｜AI Agent 全栈工程师-音视频方向

- **校招项目备注**：快手官方2027项目 20271779425607
- **官方职位 / ID**：AI Agent 全栈工程师-音视频方向 / `13145`
- **地点**：北京
- **官方职位页**：
- https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/13145?code=7746933f8afa43bb9708bc47f621ae3d&recruitSubProjectCodes=20271779425607

**官方职责**

- 参与面向音视频业务的 AI Agent 研发，覆盖智能排障、成本管控、体验优化、研发提效等场景。在导师指导下，将复杂的音视频处理 SOP 梳理为可执行的 Agent 工作流，参与构建从“能问”到“能干”的 Agent 能力闭环。
- 1. Agent 应用研发：参与 AI Agent 的设计、开发与迭代，包括任务编排、Prompt 设计、工具调用、前后端联调及功能交付；
- 2. 工具链封装与集成：协助将排障、转码、调度、监控等平台能力封装为 Agent 可调用的 Tool / MCP / Skill，推进自动化工作流落地；
- 3. 知识库建设：参与音视频领域知识库的搭建与优化，包括文档处理、向量检索、混合检索、重排序及检索效果分析；
- 4. 效果评估与迭代：协助构建评测集和评估链路，分析 Agent 的准确率、召回率、响应延迟和成本，并推动持续优化；
- 5. 工程质量与稳定性：参与上下文管理、模型路由、异常兜底、日志监控等工程能力建设，保障服务的可用性与可维护性；
- 6. 技术探索：跟踪 AI Agent、MCP、RAG 等方向的技术进展，探索 AI 在音视频工作流自动化中的创新应用，并沉淀实践经验。

**官方要求**

- 1. 本科及以上学历，计算机、软件、信息等相关专业；
- 2. 具备扎实的编程基础，熟悉至少一种主流开发语言，如 Python、Java、Go、JavaScript / TypeScript 等；
- 3. 对 AI Agent、大语言模型应用或生成式 AI 有浓厚兴趣，有课程项目、个人项目、竞赛或开源实践者优先；
- 4. 熟悉常见 AI 编程工具的使用，能够借助工具学习并解决实际工程问题；
- 5. 了解Harness、Loop Engineering、结构化输出、Function Calling / Tool Use 等基本概念，有相关实践更佳；
- 6. 具备良好的学习能力、问题分析能力和沟通协作意识，能保证稳定的实习投入时间。
- 加分项：
- 1. 有 LangChain、LangGraph、AutoGen 或其他 Agent 框架的实践经验；

### 快手｜【快Star】Data Agent研发工程师

- **校招项目备注**：快手官方2027项目 20271779425607
- **官方职位 / ID**：【快Star】Data Agent研发工程师 / `12829`
- **地点**：北京
- **官方职位页**：
- https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/12829?code=d30d1acd84a84251811134eb72139c33&recruitSubProjectCodes=20271779425607

**官方职责**

- 大模型正在重塑企业数据的使用方式。快手数据平台自研的企业级大数据智能体 DataAgent，每天服务数千名内部分析师、工程师和产品同学——他们用一句自然语言，就能完成数据查询、SQL 生成、看板分析、AB 实验解读等工作。这不是PPT，是一个真实落地、高频使用、持续迭代的AI产品。我们正处在 AI Agent 技术爆发的窗口期，企业级落地的挑战比 Demo 复杂 100 倍：如何让多个 Agent 协作不"幻觉"？如何构建真正理解业务的知识体系？如何在亿级用户的数据场景下做到可靠、可观测？这是你毕业后就能参与解答的问题。
- 作为团队成员，你将深度参与：
- 1、Multi-Agent 框架的工程研发，探索 Agent + Skill 多智能体协作的边界；
- 2、多模态知识构建与服务，面对百万级海量数据资产，探索让 AI 能够"看懂"的数据世界；
- 3、智能评测与可观测平台建设，让 AI 系统的每一次行为都可测量、可追溯，构建效果提升的飞轮；
- 4、利用 RAG、知识图谱、上下文压缩与记忆管理、模型微调与强化学习等前沿 LLM 技术，不断突破 DataAgent 的能力天花板；
- 5、以微服务、容器化（沙箱）等工程手段，构建高可用、高扩展的 AI 服务底座。

**官方要求**

- 1、本科及以上学历，计算机相关专业，应届或 Gap year 均欢迎；
- 2、扎实的 Java 后端开发基础，熟悉 Spring 等主流框架，代码整洁、有工程规范意识；
- 3、对 LLM 技术有基本认知（Prompt Engineering、RAG、Function Calling 等），或在校期间有相关课程/项目经历；
- 4、我们更看重的特质：
- 动手派：有想法就立刻写代码验证，不停留在"想想就好"；
- 学习欲强：AI 技术迭代极快，你能从容面对"上周学的今天就过时"；
- 善于表达：能把复杂的技术问题说清楚、讲明白；
- 乐于协作：在快速迭代的团队中找到自己的节奏。

### 快手｜大模型 AI Agent 开发工程师

- **校招项目备注**：快手官方2027项目 20271779425607
- **官方职位 / ID**：大模型 AI Agent 开发工程师 / `13091`
- **地点**：杭州 / 北京
- **官方职位页**：
- https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/13091?code=029b10e68bec40d190d0379d40223c5f&recruitSubProjectCodes=20271779425607

**官方职责**

- 1、参与 Agent 核心运行时的各项能力建设，包括任务规划、工具调用、记忆管理、多智能体协同等关键模块；
- 2、参与 OpenClaw 等开源 Agent 产品在快手内部的工程化落地与能力增强，包括电商、直播、短视频等业务场景；
- 3、参与 Agent 系统的可观测、评测、稳定性与部署体系建设，提升复杂 AI 系统的线上可用性；
- 4、跟踪并验证前沿 Agent / AI Infra 技术演进，推动从技术探索到业务落地的闭环。

**官方要求**

- 1、本科及以上学历，计算机相关专业，有扎实的计算机基础知识以及 Java 或 Python 编程功底；
- 2、对大模型、Agent、RAG 等方向有较强兴趣，理解 LLM 的基本原理、上下文机制、Prompt 作用方式及常见能力边界；
- 3、有强烈的好奇心，对前沿技术充满热情，具有良好的沟通能力、学习能力和团队合作精神。
- 加分项
- 1、有 LangChain、LlamaIndex、LangGraph、AutoGen、CrewAI 等 Agent 框架实战经验；
- 2、理解 ReAct、CoT、ToT、Reflection、Multi-Agent 等常见 Agent 推理与协作模式；
- 3、有 RAG 系统开发经验，熟悉向量检索、重排序、Hybrid Search、知识库构建等能力；
- 4、熟悉 Docker、Kubernetes、服务化开发或 AI 系统部署运维，对 Infra / 平台方向有兴趣；

### 百度｜2027AIDU-Agent应用全栈工程师(J99974)

- **校招项目备注**：百度当前校园招聘=2027届
- **官方职位 / ID**：2027AIDU-Agent应用全栈工程师(J99974) / `40a5d02a-6805-44c7-9d78-1cc943f11652`
- **地点**：北京市
- **官方职位页**：
- https://talent.baidu.com/jobs/detail/GRADUATE/40a5d02a-6805-44c7-9d78-1cc943f11652

**官方职责**

- 1. 构建下一代基于大模型的 Autonomous Agent 系统，让 AI 从“对话工具”进化为“可执行任务的智能体”；
- 2. 设计复杂任务的  规划（Planning）—执行（Acting）—反思（Reflection）闭环，提升 Agent 的自主决策能力；
- 3.搭建 Agent 的核心能力体系，包括： Tool / API  调用（函数调用体系）、长短期记忆（Memory）机制、多轮推理与状态管理（Reasoning & State）；
- 4. 探索并落地 多Agent协作（Multi-Agent  Systems），解决复杂业务问题（如自动化流程、复杂决策、智能运营等）；
- 5. 深度参与 RAG（检索增强生成）+ Agent  融合架构设计，构建具备知识理解与行动能力的系统，推动 Agent 在真实场景中的应用落地（如搜索、医疗、企业服务、数据分析、自动化办公等）参与 Agent  系统的评测体系建设（Eval），优化智能体的：成功率 / 稳定性、成本（Token / 调用）、延迟与用户体验；
- 5. 持续跟踪前沿方向（如 Tool  Learning、Self-Improvement、长期记忆、World Model、多模态 Agent），并进行工程化落地。

**官方要求**

- 不满足于“调用 API”，而是想重新定义软件如何被构建（Software 2.0 / Agent-first）
- 对“让 AI 像人一样完成复杂任务”这件事有执念
- 喜欢动手做实验、快速迭代，而不是只停留在论文或概念
- 愿意在一个高速变化、没有标准答案的领域中探索
- 深度使用过大模型（如 GPT / Claude / Gemini 等），理解其能力边界与局限性
- 做过 AI Agent / 自动化工具 / 智能助手相关项目（课程 / 自发项目均可）
- 使用过任一 Agent 框架（如 LangChain / LlamaIndex /  AutoGen / CrewAI 等）
- 对“如何让 AI 完成复杂任务”有强烈兴趣，甚至有自己的方法论或实验

### 百度｜Agent Harness 研发工程师

- **校招项目备注**：百度当前校园招聘=2027届
- **官方职位 / ID**：上海-Agent Harness 研发工程师(J100779) / `700dac2e-46ca-49a6-bfec-f5a228c16b3d`；北京-Agent Harness 研发工程师(J100815) / `78a17315-aef5-47f8-b9c8-31ccca2669bd`
- **地点**：上海市 / 北京市
- **官方职位页**：
- https://talent.baidu.com/jobs/detail/GRADUATE/700dac2e-46ca-49a6-bfec-f5a228c16b3d
- https://talent.baidu.com/jobs/detail/GRADUATE/78a17315-aef5-47f8-b9c8-31ccca2669bd

**官方职责**

- -作为 Agent Harness 核心构建者，参与设计与开发 Agent Harness 产品技术架构，打造支撑 LLM 能力在真实业务场景稳定释放的核心交互范式与系统底座
- -搭建 Agent 可读、可控、可验证的系统支撑体系，涵盖状态管理、沙箱环境设计、反馈闭环、执行约束、上下文交接与关键信息 compaction 优化，保障 Agent 长时间高复杂度执行的稳定性与可控性
- -深度参与 LLM 与 Harness 的联合优化，从 Harness 视角实现模型能力的最大化适配，分析并验证不同 Harness 设计对模型行为的真实影响
- -设计并实现 Agent 与人类的协作机制与反馈闭环，沉淀用户反馈并驱动产品持续迭代，在数亿用户规模的真实产品中，通过“人-模-体”协同进化探索智能上限

**官方要求**

- -本科及以上学历，计算机、人工智能、软件工程等相关专业，技术功底扎实，学习能力突出，可在 AI 辅助下完成跨领域高质量任务交付
- -深入理解 AI Agent 底层机制和 ReAct、CoT、Plan-and-Execute 等主流 Agent 原理，熟练使用 PyTorch、LangChain、AutoGen等框架，具备 Agent 系统从算法设计到工程落地的完整能力
- -Agent 重度用户与实践者，熟悉主流 Agent 框架的优劣差异，能清晰分析其在复杂文件读写、环境反馈、长任务执行等场景下的不足，并提出改良方案
- -良好的沟通协作能力和技术品味，能与模型研究员、产品经理紧密配合，共同推进 Harness 领域的前沿创新与产品落地，具备快速将学术成果落地为商业化产品的实战能力
- -加分项：有 AI Agent 相关开源项目贡献或 Harness 工程落地经验，智能体产品早期搭建经历，知名开源项目核心贡献、顶级会议论文发表或高水平技术竞赛获奖经历者优先

### 百度｜AI Coding / Agent Workflow 全栈开发工程师

- **校招项目备注**：百度当前校园招聘=2027届
- **官方职位 / ID**：北京-全栈开发工程师(J103963) / `885a47cc-edc7-483f-817c-73340a4444da`；深圳-全栈开发工程师(J103964) / `5ea78d8e-0f9e-40f7-898e-94861224f066`
- **地点**：北京市 / 深圳市
- **官方职位页**：
- https://talent.baidu.com/jobs/detail/GRADUATE/885a47cc-edc7-483f-817c-73340a4444da
- https://talent.baidu.com/jobs/detail/GRADUATE/5ea78d8e-0f9e-40f7-898e-94861224f066

**官方职责**

- -负责前端和服务端的业务开发工作，覆盖业务全链路，按业务需求统筹各端开发优先级，打破端侧壁垒，实现业务功能高效落地
- -深度运用AI Coding工具，开发并维护基于MCP、CLI、Skills等的各类工具，参与Al研发基础设施与Agent工作流建设，对接公司内部系统与模型，打造一体化AI研发体验
- -立足全栈发展趋势，推动并沉淀Vibe Coding、SpecCoding等新型Al研发范式在团队内的落地与最佳实践，参与业务全流程开发，推动业务从需求到上线的闭环落地
- -负责前沿技术探索与范式推广，持续跟进AI/LLM(包含底层大模型)的最新进展，提供创新的交互解决方案，并推动技术的迭代和升级
- -配合团队完成技术方案讨论、架构优化、代码评审等工作，助力团队形成"按业务分工、AI+全栈协同"的开发模式，适配未来1~2年全栈发展导向

**官方要求**

- -本科及以上学历，计算机、通信和电子信息科学、数学等相关专业
- -具备良好的计算机基础（数据结构、算法、计算机网络、操作系统等)，并熟练使用至少一门编程语言
- -熟练使用HTML5/CSS3/JavaScript/TypeScript/Vue/React等前端技术完成页面布局和交互开发，有全栈开发经验者优先
- -熟练使用TRAE、Claude Code、Codex、Cursor等任一Al Coding工具，维护过Rules、MCP、Skills并了解底层机制与技术细节的同学优先
- -认可Al Coder定位，明确自身长期全栈发展规划，具备较强的学习能力和适应能力，能快速上手新领域技术，适配业务驱动的开发模式
- -积极乐观，责任心强，具备良好的沟通协作能力、逻辑思维能力以及服务意识

### OPPO｜AI Agent 研发工程师（研发效能方向）

- **校招项目备注**：2027届应届生校园招聘
- **官方职位 / ID**：AI Agent 研发工程师（研发效能方向） / `1850`
- **地点**：深圳市
- **官方职位页**：
- https://careers.oppo.com/university/oppo/campus/post/1850

**官方职责**

- 1. 参与软件工程场景中 Coding Agent/测试类Agent 的架构设计与开发，探索任务规划、多智能体协同。
- 2. 设计并实现基于 MCP/CLI 的工具链，丰富 Agent 的 Skill 生态，优化上下文提取与注入方案。
- 3. 参与平台前后端开发，包括人机协同交互界面、任务编排引擎以及相关平台服务建设。
- 4. 参与构建 Agent 自动化评测体系，设计回归评测集，追踪并分析 Agent 执行 Trace 链路，调优执行效率与稳定性。

**官方要求**

- 1. 本科及以上学历，计算机、软件工程、人工智能等相关专业，计算机基础知识扎实。
- 2. 熟练掌握 TypeScript、Python、Go、Java 等至少两种语言，具备全栈工程开发经验。
- 3. 必须熟练且高频使用 Claude Code、Codex、Cursor 等至少一种 AI Coding 工具。
- 4. 具备优秀的快速学习能力与极客精神，能够流畅阅读英文技术文档与前沿 AI 论文。
- 5. 理解 Harness Engineering，对研发流程治理有一定认知。
- 6. 深度参与过 AI Agent 相关项目的开发，有个人开源贡献，熟练使用 GitHub。

### OPPO｜AI工程师（AI Agent方向）

- **校招项目备注**：2027届应届生校园招聘
- **官方职位 / ID**：AI工程师（AI Agent方向） / `1821`
- **地点**：成都市,深圳市
- **官方职位页**：
- https://careers.oppo.com/university/oppo/campus/post/1821

**官方职责**

- 负责系统级AI agent产品的研发落地和实施。构建高并发/高性能/高可用服务端架构和系统，支撑海量级用户产品的迭代和体验优化

**官方要求**

- 1. 具备AI 深度应用能力，有不错的产品sense，日常高频深度使用 AI 工具和应用；
- 2. 具备自驱、好奇心与学习能力，对新技术有激情、愿意分享，不设限地解决问题，良好的结果导向和抗压能力；
- 3. 熟悉Java/C/C++/golang/python等一种或多种编程语言，语言基础扎实；
- 4. 了解Linux操作系统常用操作，Shell开发，能熟练使用各种研发工具；
- 5. 专注于技术，精益求精，并对业界的最新技术发展动态有比较密切的关注；

### 美团｜【北斗】Agent 系统研发工程师

- **校招项目备注**：美团官方当前校园招聘正式岗（届别需主库复核）
- **官方职位 / ID**：【北斗】Agent 系统研发工程师 / `4530632100`
- **地点**：北京市
- **官方职位页**：
- https://zhaopin.meituan.com/web/position/detail?jobUnionId=4530632100&highlightType=campus

**官方职责**

- 【愿景】
- 负责面向算法研发、业务建模与系统构建场景的 AutoResearch Harness、Agent Swarm 与 AI Builder 能力建设，探索大模型驱动复杂问题分析、方案生成、实验验证和系统搭建的新范式。
- 【你将参与】
- 1.设计 AutoResearch Harness：建设任务分解、实验编排、工具调用、结果评   估、失败恢复、知识沉淀等核心模块，让 Agent 能稳定完成长程、开放式研发任务；
- 2.构建 Agent Swarm 协作体系：研究多 Agent 之间的角色分工、上下文共享、协同决策、互评纠错和成本控制机制，提升复杂任务中的可靠性与可扩展性；
- 3.建设上下文与记忆系   统：围绕 context compression、memory selection、状态追踪、项目知识库和跨轮学习，提升 Agent 在长链路任务中的连续性和可控性；
- 4.打造 AI Builder 原型系统：面向真实业务快速交付可用工具，将自然语言需求转化为可执行流程、实验方案、分析报告或业   务系统原型，并沉淀评测闭环与工程最佳实践。

**官方要求**

- 【任职资格】
- 1.2027届计算机、人工智能、软件工程、数学等相关专业本科及以上，硕士/博士优先。
- 2.具备扎实的工程实现能力，熟练掌握 Python/TypeScript/Go/Java 中至少一种，能独立完成从问题定义、系统设计、原型开发到评测迭代的端到端交付。
- 3.熟悉 LLM、Tool Use、   Planning、RAG/Memory、Multi-Agent、Context Engineering 等 Agent 基本机制，对 AutoResearch、AI Builder、Agent Swarm、AI Scientist/AIDE 类方向有实践或深入思考。
- 4.关注 Claude Code、Codex、OpenClaw、Cursor 等工具背后的 Harness 设计，但不限于   coding 场景。
- 5.自驱、动手快，能在开放问题中快速验证假设并推动落地。
- 【为什么是我们】
- 这里关注的是通往通用智能的 Agent 基础设施，而不是单点 Demo。你将参与 AutoResearch Harness、Agent Swarm、AI Builder、记忆与上下文系统建设，在真实业务和复杂研发场景中验证 AI 自动完成高价值任务的能力边界。

### 顺丰｜AI开发工程师（顺丰科技）

- **校招项目备注**：顺丰官方校园招聘（届别待复核）
- **官方职位 / ID**：AI开发工程师（顺丰科技） / `2239`
- **地点**：武汉市,深圳市
- **官方职位页**：
- https://campus.sf-express.com/#/postDetail/2239

**官方职责**

- 1、参与多智能体（Multi-Agent）系统设计与开发，学习Agent间协作与任务分解机制，协助构建可扩展、低耦合的智能体协作架构。
- 2、结合物流业务场景及数据，在导师指导下参与设计并构建具备业务感知与决策支持的智能体系统。
- 3、与产品、算法、业务团队紧密协作，学习大模型推理优化与部署流程，参与智能体系统在物流场景的落地、迭代与效果验证。
- 4、掌握分布式推理、GPU调度优化等前沿技术，有机会参与大规模企业级AI基础设施的规划与建设。

**官方要求**

- 1、2027届本科及以上学历毕业生，计算机、软件工程、人工智能等相关专业优先，熟练掌握Java、Python、Go至少一种编程语言，有良好的编程基础。
- 2、了解大模型基本原理与智能体应用架构，对Claude Agent SDK、DIFY、LangGraph、Spring AI等主流框架有一定了解或学习经历，了解Agent2Agent、MCP等协议，对多智能体系统有浓厚兴趣。
- 3、了解企业知识库与RAG系统基本概念，对向量数据库、检索优化与大模型集成模式有学习或项目实践经历。
- 4、了解Docker/K8s等容器化技术，对大模型服务部署与推理优化有基本认知，具备高并发、高可用系统设计的学习意识。
- 5、对flink、kafka、hive等大数据组件有基本了解，或在课程学习、项目实践中接触过相关技术。
- 6、对物流、供应链等相关业务有了解或兴趣，具备快速学习能力和业务理解能力，能将业务场景转化为技术方案。
- 7、具备良好的沟通协作能力、学习能力和创新意识，有相关项目经历、竞赛获奖或开源贡献者优先。

### 小米｜AI Agent开发工程师-Java方向

- **校招项目备注**：2027届校园招聘计划 / 正式
- **官方职位 / ID**：AI Agent开发工程师-Java方向 / `7670885684991281471`
- **地点**：北京 / 深圳
- **官方职位页**：
- https://xiaomi.jobs.f.mioffice.cn/campus/position/7670885684991281471/detail

**官方职责**

- 主要负责AGOP相关的Agent开发,包括但不限AGOP服务、知识库、AACE.
- 负责已有Agent的运维。

**官方要求**

- 有强烈的责任心,遇到问题能够一查到底,知其然并知其所以然 ；
- 扎实的编程能力,熟悉算法、数据结构、人工智能；
- 勤于思考,善于总结,乐观自信,不断追求进步 ；
- 有AI工程经验者优先；

### 小米｜Agent Harness 开发工程师

- **校招项目备注**：2027届校园招聘计划 / 正式
- **官方职位 / ID**：Agent Harness 开发工程师 / `7678147882801678602`
- **地点**：北京
- **官方职位页**：
- https://xiaomi.jobs.f.mioffice.cn/campus/position/7678147882801678602/detail

**官方职责**

- 1、参与小爱服务端核心系统的研发与维护，支持多业务场景需求，持续提升系统的迭代效率、稳定性与性能。
- 2、参与下一代小爱服务端架构升级，设计并建设面向文本大模型、多模态模型及 Agent 的 Harness 能力，支撑算法流程的快速编排、灰度验证与持续演进。
- 3、参与服务端关键技术问题攻关，围绕高并发、低延迟、稳定性、可观测性等方向持续优化系统能力。

**官方要求**

- 1、2027届本科及以上学历，计算机、软件工程、人工智能或相关专业。
- 2、熟练掌握至少一门后端编程语言（java/rust/c++/c#/golang 均可）。
- 3、掌握常用数据结构与算法，了解常见设计模式，具备良好的代码设计与工程实践能力。
- 4、了解分布式系统基础，熟悉缓存、消息队列、数据库、分布式存储或计算框架中的一种或多种。
- 5、对大模型、Agent、多模态等方向有兴趣或相关项目经历者优先。
- 6、具备良好的学习能力、主动性与协作意识，愿意面对复杂问题并持续追求技术卓越。

### 小米｜Agent Harness 研发工程师

- **校招项目备注**：2027届校园招聘计划 / 正式
- **官方职位 / ID**：Agent Harness 研发工程师 / `7671284471720020243`
- **地点**：武汉 / 北京
- **官方职位页**：
- https://xiaomi.jobs.f.mioffice.cn/campus/position/7671284471720020243/detail

**官方职责**

- 1、自研 Harness 框架：参与设计和开发面向行业场景的 Agent Harness 产品技术架构，包括 Agent Loop、工具系统、上下文管理、记忆与状态管理等核心模块
- 2、行业 Agent 落地：基于自研 Harness 框架，实现零售、客服、研发、供应链、办公等行业 Agent，将通用模型能力适配到垂直业务场景
- 3、算法与工程联合优化：从算法角度和工程角度联合优化，从 Context Engineering、Harness Engineering 等角度持续优化 Agent 的任务完成率与用户体验
- 4、模型+Harness 协同进化：以行业真实任务为反馈源，推动模型能力与 Harness 架构的双向迭代，实现 1+1>2 的效果
- 5、前沿技术追踪与落地：跟踪 Agent 领域前沿进展（MCP、A2A、Multi-Agent、Sub-agent 等），快速验证并在产品中落地

**官方要求**

- 必须项：
- 1、熟悉大模型基本原理与技术机制，包括但不限于：Transformer 架构、注意力机制、KV Cache、推理优化（Reasoning）、Tokenization 等
- 2、熟悉 Agent 核心概念与技术栈：Agent Loop、Tool Use、Planning、Skills、MCP（Model Context Protocol）、Memory、Sub-agent、Multi-Agent
- 3、深度使用过主流 Agent / Harness 产品（如 Claude Code、Codex、OpenCode、OpenClaw、Hermes 等），对 Agent 产品有品味和判断力
- 4、了解大模型的训练过程，包括预训练/后训练，熟悉开源大模型技术报告的模型与训练细节
- 5、对 Prompt Engineering、Context Engineering、Harness Engineering 有实践理解和浓厚兴趣
- 6、熟练使用 AI Agent 工具进行软件开发，具备在 AI 辅助下快速上手陌生技术栈的能力
- 7、扎实的编程基础，至少精通 Python / TypeScript / Go 中的一种语言

### 小米｜Agent工程师

- **校招项目备注**：2027届校园招聘计划 / 正式
- **官方职位 / ID**：Agent工程师 / `7670928909127223588`
- **地点**：武汉 / 北京
- **官方职位页**：
- https://xiaomi.jobs.f.mioffice.cn/campus/position/7670928909127223588/detail

**官方职责**

- 1、参与 AI Agent 平台的架构设计与核心模块研发，负责智能体运行时、编排引擎、Skill 框架等基础设施的技术方案设计与实现
- 2、深入业务场景（办公协同、流程自动化、知识管理等），识别 AI Agent 赋能机会，将产品需求转化为技术方案并落地交付
- 3、与算法团队协作，将大模型、Agent 框架、MCP 协议等 AI 能力工程化落地，构建可复用的 Agent 能力底座
- 4、保障系统工程质量与稳定性，建立技术指标体系（响应延迟、成功率、幻觉率等），数据驱动持续优化
- 5、跨域协同：联动产品、算法、数据、运维等多团队，确保系统高质量交付与稳定运行

**官方要求**

- 1、2027届应届毕业生，硕士及以上学历（博士优先），985高校或QS世界排名前100院校，计算机科学、人工智能、软件工程等相关专业
- 2、对大模型（LLM）、NLP、机器学习、Agent 系统等 AI 技术有基本认知，理解技术边界与工程化落地路径
- 3、具备扎实的工程能力，熟练掌握 Python/Java/Go 等至少一门语言，有微服务架构、状态机设计、消息队列等实践经验者优先
- 4、优秀的跨团队沟通能力，能高效协作推动技术方案从设计到上线
- 加分项
- 1、有 AI Agent、大模型应用、LLM 平台工程相关实习或项目经验
- 2、熟悉 Prompt Engineering、RAG、Agent 工作流、MCP 协议等技术实践
- 3、头部互联网公司技术实习经历（AI/Agent/平台工程方向优先），AI 相关科研项目或论文成果

### 小米｜AIOS 开发工程师

- **校招项目备注**：2027届校园招聘计划 / 正式
- **官方职位 / ID**：AIOS 开发工程师 / `7670892428991269146`
- **地点**：南京
- **官方职位页**：
- https://xiaomi.jobs.f.mioffice.cn/campus/position/7670892428991269146/detail

**官方职责**

- 1. A²UI DSL 协议设计与实现：设计 LLM 输出与原生 UI 之间的轻量级中间表示语言,支持流式增量更新、Token 经济性优化及跨框架适配（Flutter/Compose/SwiftUI）
- 2. 流式渲染引擎开发：构建从 JSON DSL 到原生 Widget 的流式解析与渲染管线,实现基于 Token 粒度的边生成边渲染（AST Streaming）,确保首屏渲染延迟 < 100ms、帧率稳定 120Hz
- 3. 端侧意图路由与多 Agent 编排：部署和优化端侧轻量意图分类模型（< 50M 参数）,设计多 Agent 协作编排策略与 Surface 显示优先级仲裁算法
- 4. 端云协同推理方案：设计端侧 SLM 预判 + 云端大模型异步填充的协同架构,实现离线降级兜底与 OS 级组件预热缓存
- 5. OS 级系统集成：在跨进程共享内存通信、UI 状态机生命周期接管、NPU/GPU 硬件加速等系统层面进行深度工程实践,将生成式 UI 能力注入 OS 渲染中枢

**官方要求**

- 基础要求：
- - 2027届本科及以上学历,计算机科学、软件工程、人工智能等相关专业
- - 扎实的编程基础,精通 C/C++ 或 Rust,理解内存管理与系统编程
- - 理解操作系统原理（进程调度、内存管理、IPC 机制）
- - 至少熟悉一个声明式 UI 框架（Flutter / Jetpack Compose / SwiftUI）的渲染管线原理
- 优先项（满足其一即可）：
- - 了解 Transformer 架构与大模型基本原理,有端侧模型部署经验（TFLite / ONNX / MNN）
- - 有编译原理基础,了解 DSL 设计、Parser、AST 构建等概念


### 阿里巴巴｜Agent Infra工程师

- **校招项目备注**：阿里巴巴官方 2027 校招批次
- **官方职位 / ID**：Agent Infra工程师 / `199907640058`
- **官方职位页**：https://campus-talent.alibaba.com/campus/position/199907640058?deptCodes=

**官方 JD 要点**

- 建设 Agent 全生命周期基础设施，包括沙箱、容器编排、任务调度、状态管理、长任务恢复与多租户安全；
- 提供 Context / Retrieval、SDK/API、CLI / Skills、可观测和 AgentOps 等平台能力；
- 要求扎实的 OS / Network / DB / Distributed Systems 基础，熟悉 Go / Python / Java / C++ / Rust / TypeScript、云原生与 Agent 框架。

### 小红书｜大模型 Agent 开发工程师（AI Coding）

- **校招项目备注**：小红书官方 2027 校园招聘 / REDstar
- **官方职位 / ID**：大模型 Agent 开发工程师（AI Coding方向） / `20960`
- **官方职位页**：https://job.xiaohongshu.com/campus/position/20960

**官方 JD 要点**

- 建设客户端 Coding Harness、Agent 编排、Context Engineering、Loop Engine 与工程级代码上下文；
- 打通 Coding Agent 在真实构建 / 测试环境中的执行—验证—修正闭环；
- 建设复杂工程代码质量 Eval，要求优秀的软件工程、程序分析和大型代码库处理能力。

### 小红书｜AI Agent 工程师（AI Coding / 质效研发）

- **校招项目备注**：小红书官方 2027 校园招聘 / REDstar
- **官方职位 / ID**：AI Agent 工程师（大模型 AI Coding方向）-质效研发 / `21828`
- **官方职位页**：https://job.xiaohongshu.com/campus/position/21828

**官方 JD 要点**

- 建设公司级 AI Agent / Coding Agent / AI 个人助理，使 Agent 能完成规划、编码、测试、发布和诊断；
- 核心方向包括 Agent Harness、代码与业务 Context、Tool / Skill、Memory、Eval 与数据飞轮；
- 强调生产级工程、MCP / Function Calling / 流式交互、Agent Harness 与高并发系统能力。

### 小红书｜点点 Agent研发工程师

- **校招项目备注**：小红书官方 2027 校园招聘 / REDstar
- **官方职位 / ID**：点点 Agent研发工程师 / `21822`
- **官方职位页**：https://job.xiaohongshu.com/campus/position/21822

**官方 JD 要点**

- 负责任务理解 / 拆解、Planning、Multi-turn Context、长期 Memory、Tool 选择执行、State 与 Failure Recovery；
- 连接小红书内容与结构化信息，持续优化 Tool Retrieval、多工具协同与真实任务成功率；
- 建设端到端 Agent Eval、专项评测和真实 Tool 实验环境，并探索 Generative UI。

### 小红书｜AI Agent Infra 工程师

- **校招项目备注**：小红书官方 2027 校园招聘 / REDstar
- **官方职位 / ID**：AI Agent Infra 工程师 / `21899`
- **官方职位页**：https://job.xiaohongshu.com/campus/position/21899

**官方 JD 要点**

- 建设 AgentSphere 生产与进化基础设施，覆盖 Harness Kernel、Managed Runtime、Context / Memory、Tool / Sandbox、Control Plane、Eval / Evolution；
- 解决长任务可靠执行、状态恢复、异构 Agent 治理、工具安全、非确定性系统评测等生产级问题；
- 要求 Python / C++ / Rust / Go 等系统工程能力，并理解 Runtime / Execution Environment / Control Plane / Data Plane 等架构边界。

### 商汤科技｜Agent开发工程师

- **校招项目备注**：官方职位标题明确“27届校招”
- **官方职位 / ID**：Agent开发工程师 / `7659330461617178916`
- **官方职位页**：https://hr-jobs.sensetime.com/edu/position/7659330461617178916/detail

**官方 JD 要点**

- 开发 Tool Calling、Workflow、Memory 等 Agent 核心模块；
- 设计 Multi-Agent 协同与调度，并把 Agent 能力封装成 SDK / API；
- 建设 Prompt 管理、效果评测和工程文档；要求 Python 与实际 Agent 框架 / 项目经验。

### 商汤科技｜Agent全栈开发工程师（大装置）

- **校招项目备注**：官方职位标题明确“27届校招”
- **官方职位 / ID**：Agent全栈开发工程师-大装置 / `7659616422645369139`
- **官方职位页**：https://hr-jobs.sensetime.com/edu/position/7659616422645369139/detail

**官方 JD 要点**

- 基于主流大模型建设可复用 AI Agent 应用与服务；
- 负责 Planning、Tool/API Calling、Memory / RAG、结果校验、Single / Multi-Agent Workflow；
- 将 Agent 封装为 API / Service，并在效果、成本与时延之间做工程权衡。

### 商汤科技｜智能体研发（亚太业务事业群）

- **校招项目备注**：官方职位标题明确“27届校招”
- **官方职位 / ID**：智能体研发-亚太业务事业群 / `7659253281403078975`
- **官方职位页**：https://hr-jobs.sensetime.com/edu/position/7659253281403078975/detail

**官方 JD 要点**

- 建设 Planning、Tool Calling、Workflow、Knowledge Retrieval、Memory 等智能体平台能力；
- 落地 RAG、Function Calling、MCP、Tools / Skills，并从 Demo 推到产品化；
- 建设 Prompt / Retrieval / Tool 调优、异常分析、效果评测和复用组件。

### MiniMax｜AGI产品研发工程师（应届生 TOP Talent）

- **校招项目备注**：MiniMax 官方 Careers 明确 2027 届校园招聘
- **官方职位 / ID**：AGI产品研发工程师-应届生-TOP Talent / `7546180826527893810`
- **官方职位页**：https://vrfi1sk8a0.jobs.feishu.cn/379481/position/7546180826527893810/detail

**官方 JD 要点**

- 负责 AI 产品 / Agent 的创新研发，参与 Agent Environment / Runtime / Infra 的定义、实现和优化；
- 将 Agent 作为模型与用户交互、行动和反馈的真实环境，联合产品体验与系统能力持续迭代；
- 要求优秀的代码、系统设计和跨技术栈复杂问题解决能力，Agent 实践 / 开源贡献为加分项。

## 7. 相关工程岗 / 边界岗 / 待届别确认

| 公司 | 官方岗位/通道 | 为什么不计核心 | 官方入口 |
|---|---|---|---|
| 腾讯 | Agent开发工程师 / AI应用工程师 / AI全栈工程师 | 当前官方 campus 已发现，但 2027 届别未闭环 | https://join.qq.com/ |
| 联想 | AI Agent开发工程师 / AI应用开发工程师 | 官方应届生 AI开发类已发现，2027 届别/完整 JD 待闭环 | https://talent.lenovo.com.cn/position?jobTypeName=AI%E5%BC%80%E5%8F%91%E7%B1%BB&projectType=1 |
| 京东 | 技术方向-全栈开发（可定岗 Agent 开发） | 2027 毕业窗口明确，但岗位是宽口径技术通道，不计核心 Agent JD | https://campus.jd.com/#/details?type=present&id=9197 |
| 顺丰 | AI全栈研发工程师（顺丰科技） | 2027 明确，但职责主体为全栈 + AI Coding，不计核心 Agent/AI应用系统 JD | https://campus.sf-express.com/#/postDetail/2246 |
| 快手 | AI测试开发工程师 | 2027 明确，包含测试 Agent / Agent Eval，但主责是测试 | https://campus.kuaishou.cn/recruit/campus/e/#/campus/job-info/13046?recruitSubProjectCodes=20271779425607 |
| OPPO | AI系统工程师（AI工程化方向） | 2027 明确，但岗位多方向混合算法 / AIOS Agent，避免算法主体混入核心 | https://careers.oppo.com/university/oppo/campus/post/1843 |
| 小米 | AI Agent开发工程师-汽车 | 2027 明确，但 JD 同时要求大模型训练 / Megatron / DeepSpeed，属于 Agent工程 + 模型训练混合边界 | https://xiaomi.jobs.f.mioffice.cn/campus/position/7670914994071046451/detail |
| 小米 | AI 数据基础架构 / 自动化测试架构 / 应用安全等 | 2027 明确且含 Agent，但主责分别是数据底座、测试、安全等，不计核心 | https://hr.xiaomi.com/website/opportunities.html?project=%E6%A0%A1%E6%8B%9B&q=agent |

## 8. 明确排除

- 算法工程师、研究员、预训练/后训练/SFT/DPO/RLHF/RL、模型训练为主；
- “Agent”只是研究/训练对象，岗位主体仍是模型算法；
- 测试/安全/数据/芯片/传统 Infra 等岗位仅局部使用 Agent，而不是 Agent / AI应用工程主责；
- 产品、运营、市场、销售；
- 日常实习、社招（本主库只统计当前有效正式校招）。

## 9. 可重复官方发现

- [官方 2027 公司源注册表](official-2027-campus-sources.json)
- [官方动态站发现结果](official-2027-agent-jobs.generated.md)
- [统一同步器](../../tools/sync_official_2027_agent_jobs.py)
- [小米 ATSX Node 适配器](../../tools/fetch_xiaomi_2027.mjs)
- [字节 ATSX Node 适配器](../../tools/fetch_bytedance_2027.mjs)

```text
逐公司确认 2027 官方项目
→ 官方项目/API全量枚举
→ Agent/AI应用多关键词 + JD正文召回
→ 算法/非目标岗排除
→ 2027届别复核
→ Role Family 去重
→ 正式库
```

## 10. 维护日志

- **2026-09-19｜固定职位页模型收口**：42 家公司全部维护 `official_root + job_list_url`；日常采集统一从固定官方职位列表页穷举，专用 API/ATS 仅作为加速器。
- **2026-09-19｜官方 JD 扩容**：从已经保存的官方招聘页面/XHR 中新增阿里巴巴 2、小红书 6、商汤科技 4、MiniMax 1，共 13 个非算法 2027 Role Family；正式库由 25 增至 38。

- **2026-09-19**：正式切换为“2027 校招 + 第一手官方 + 非算法工程”专库。
- **2026-09-19**：修复“动态站抓不到就误判无岗位”的采集缺陷；快手、百度、OPPO、美团、京东、顺丰、腾讯、联想等官方招聘接口进入自动枚举链路。
- **2026-09-19**：小米 ATSX Node 适配器跑通，官方 campus 正式岗池获取 785 岗位、34 个 Agent/AI 工程候选，二次筛选 7 个核心 Role Family。
- **2026-09-19**：正式核心库更新为 25 个 Role Family；候选池与正式库分离，边界岗不污染核心统计。
