# 历史 JD 待复核专项处置（2026-10-15）

按照历史八份审计分片的原始职位、职责与任职要求，对 **63 条** `needs_review` 按事件 ID 单独复核：**22 条纳入、8 条排除、33 条证据不足保留待补证**。机器可读的逐条结论保存在 [复核决定](../01-data/automation/backlog-audit/followup-decisions-2026-10-15.json)。证据不足者不纳入正式库，也不伪装成已明确排除。

小米 [2027届校园招聘计划](https://hr.xiaomi.com/website/campus.html) 与 [官方校招职位列表](https://xiaomi.jobs.f.mioffice.cn/campus/m/position/list) 将“校招”“正式”“2027届校园招聘计划”同时标示：这里“正式”是全职职位性质而非社招资格。纳入决策结合官方校园招聘详情、职位计划与完整工程职责，仍以实际投递时的具体官方详情为准。

## 确认纳入（22）

| 公司 / 岗位 | 事件 ID | 完整 JD 工程证据 |
| --- | --- | --- |
| 小米 · [嵌入式测试开发与AI应用工程师-汽车](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670915178993256713/detail) | `4572d4cb9c74b43623a5eb01e1ea1f6c` | 2、负责编写自动化测试脚本，包括：操作系统、资源、时序、通信、驱动、系统服务等模块 |
| 小米 · [AI研发工程师-手机](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670891457062127881/detail) | `aa207b0f4d9099129aa22b98a8af6269` | 2. 负责模型端侧落地部署,适配NPU（如Intel平台）,涉及模型量化、精度验证、性能调优等 |
| 小米 · [AI算法工程师-AICoding/Agents方向](https://xiaomi.jobs.f.mioffice.cn/campus/position/7671291137243629878/detail) | `fae49a1d4128bc757d44c7389208d616` | 1、负责代码智能体（Coding Agent）系统全流程研发：数据构建（代码语料清洗、代码/对话/工具轨迹标注）、预训练/持续预训练、指令微调（SFT）与后训练（DPO/ORPO/RLHF/RLAIF |
| 小米 · [AI Agent多模态算法工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7671129633626540331/detail) | `bd9a4c95aa9fd353f7718b9b19c07a86` | 负责 AI Agent 智能体系统研发，探索并优化多模态大模型（MLLM）在图像质量评价（IQA）业务场景中的高效微调和推理技术，满足多样化业务需求（拍照、视频等），实现模型在AI Agent工作流中 |
| 小米 · [体系AI工程师-汽车](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670918570079652123/detail) | `12f6555c9e4617f801e847ea74896ffa` | 1. 参与完成AI在电动汽车智造领域的关键技术预研、业务开发工作 |
| 小米 · [AI属性工程师-汽车](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670918768222570803/detail) | `7d49443ead2f56358ecf4348f46fcc94` | 负责将大模型、智能体等AI能力落地至整车研发流程，提升工程团队研发效率 |
| 小米 · [自动化测试架构开发工程师-汽车](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670918384100788507/detail) | `7857b88922e4d83aec44220cd56c3afa` | 1、负责软件自动化测试平台、测试工具、框架的开发与维护，建立标准化测试流程 |
| 小米 · [软件开发工程师-影像方向](https://xiaomi.jobs.f.mioffice.cn/campus/position/7671129598676125993/detail) | `4f1df23f826dc841ed4476d8c140a86c` | 4. 负责影像与AI结合的Agent业务设计与软件架构，熟悉Agent的运作原理，有影像智慧化经验优先 |
| 小米 · [大模型网关服务端开发工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7676005513680030006/detail) | `568aa88e22f15eca62dae721b75a4f9b` | 1. 负责大模型网关的架构设计与核心代码编写，支撑高并发、低延迟的AI请求调度 |
| 小米 · [AI 数据基础架构工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670924132817750318/detail) | `e1496096f0a387131ffb9a86a356ba4c` | 参与支撑数亿设备、PB 级数据规模的湖仓一体架构研发，主导 AI Agent 在大数据全链路的落地，作为 Apache 顶级开源项目贡献者，和全球开发者一起定义下一代数据基础设施 |
| 小米 · [芯片物理设计工程师（AI方向）](https://xiaomi.jobs.f.mioffice.cn/campus/position/7671129267694897427/detail) | `1bbb4817617a010afbbd91dce327b12b` | 2、聚焦IC设计流程智能化升级，将机器学习、强化学习、大模型Agent技术落地到COT中后端核心场景，通过AI自主探索替代传统人工经验与数据模仿模式，优化逻辑综合、UPF/SDC产生、STA分析、布局 |
| 小米 · [大模型算法工程师-Data Agent方向](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670923368716011830/detail) | `4e7a9b92274347e8c15e3ba82eb75fdc` | 1. 参与分析 Agent（Text-to-SQL / Data Agent）核心能力的研究与研发，探索大模型在企业数据分析场景下规模化、生产级落地的技术路径 |
| 小米 · [AI Agent开发工程师-Java方向](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670885684991281471/detail) | `4118847a205b66ab04525791231bdfc6` | 主要负责AGOP相关的Agent开发,包括但不限AGOP服务、知识库、AACE. |
| 小米 · [AI Agent开发工程师-汽车](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670914994071046451/detail) | `16c020f96ab4916d9d16549e42597fc2` | 1、参与面向真实业务场景的AI Agent应用研发，涵盖需求分析、原型验证、功能实现与上线维护 |
| 小米 · [服务端工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670923490631239974/detail) | `c3261fef482828186fe7796fd5298d95` | 1.负责大模型网关核心研发与架构设计，完成需求分析、功能开发、迭代优化，搭建高可用、高性能、可扩展的大模型统一接入管控平台，支撑业务侧模型稳定调用 |
| 小米 · [大模型agent算法工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670924118350465321/detail) | `dbf05fe7bb5d6c9ec04219a571508d50` | 探索 Agent Harness 研究与应用的前沿技术，构建可进化的 Agent Harness 技术底座，定义可持续学习 Agent 的基础范式，包括但不限于： |
| 小米 · [服务端工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670935018218932543/detail) | `af08ad9dfd204c612cfa5c98c6e88b49` | 1.负责大模型网关核心研发与架构设计，完成需求分析、功能开发、迭代优化，搭建高可用、高性能、可扩展的大模型统一接入管控平台，支撑业务侧模型稳定调用 |
| 小米 · [Agent Harness 研发工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7671284471720020243/detail) | `c84f8e1ffa3d1a479852a62a93eb83d6` | 1、自研 Harness 框架：参与设计和开发面向行业场景的 Agent Harness 产品技术架构，包括 Agent Loop、工具系统、上下文管理、记忆与状态管理等核心模块 |
| 小米 · [AI研发工程师-智能风控方向](https://xiaomi.jobs.f.mioffice.cn/campus/position/7671289294427113737/detail) | `7e286e177c3d75238ca7b7a157b1d9c1` | 1、参与建设面向零售、服务、整车等业务的 AI 风控工作流与应用平台，围绕风险主动发现、特征与数据分析、风险识别、策略生成与上线、监控复盘、客诉分析与处置辅助等场景，形成端到端闭环 |
| 小米 · [云计算开发工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670923711373281572/detail) | `5cbb341449017891ac8d58eef80bc70b` | 2. AI Native研发范式建设：落地智能编码、AI评审、智能测试等AI原生应用，推动研发模式从“工具辅助”向“AI驱动”升级，提升代码质量与交付效率 |
| 小米 · [客户端工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670885167280900393/detail) | `9d1adb42eb35c443f267fb5cd64dc7c0` | 1、参与 AI 多模态应用客户端长期架构建设，优化架构设计以提升整体迭代效率与运行性能 |
| 小米 · [大模型智能体算法工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670923797172586795/detail) | `4aefe2427b861271e685e42ab39de2bc` | 1、Agent Memory：设计快慢双系统记忆架构，优化记忆管理机制、召回策略与压缩方法，统一存储和检索文本、图像、视频、代码等多模态数据 |

## 确认排除（8）

依据职位实际工作而非AI关键词、职位标题作出排除。

| 公司 / 岗位 | 事件 ID | 原因 |
| --- | --- | --- |
| 蔚来 · [校招-涂装数字化助理工程师](https://nio.jobs.feishu.cn/campus/position/7673026850814691622/detail) | `9d7bebe522bde0900c2450064b094e11` | 核心职责为涂装生产数据与MES数字化，LLM仅属于探索，未明确AI应用系统的工程交付。 |
| 蔚来 · [实习-安全产品开发（AI方向）](https://nio.jobs.feishu.cn/campus/position/7633336911108884772/detail) | `723ca2d362e450b74f7439d43c67edb7` | 主体是车联网安全、身份治理系统与微服务开发，LLM只作探索，AI应用模块职责不足。 |
| 小米 · [互联框架研发工程师-汽车](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670924719398471979/detail) | `e2e9a4ff216fe17611f8222ed013025f` | 主责为汽车互联框架、CarIoT及移动端性能优化，CarClaw未披露Agent研发职责，AI只是能力加分项。 |
| 影石 Insta360 · [南京实习基地-AI开发实习生-大模型方向](https://arashivision.jobs.feishu.cn/campus/position/7665663614732765491/detail) | `bf1c1ae66a85b011dc04cbb4b1c3f210` | 主要是模型量化、剪枝、算子融合和推理框架预研，不属于目标Agent应用或AI评测工程。 |
| 小米 · [可观测性平台研发工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670923711374248228/detail) | `5fa01b3bba6782dcd0c37e7a5cccb35c` | 通用日志指标追踪、告警平台是主责，AI问答和故障辅助定位仅为探索条款而非主要工程交付。 |
| 蔚来 · [校招-后端AI工程师](https://nio.jobs.feishu.cn/campus/position/7678158229625784619/detail) | `e42d5dce722951fc351f9fd239f73939` | 主体是Java后端与使用AI编程工具，Agent在导师指导下探索且交付范围不明，不符合核心Agent工程定位。 |
| 小米 · [模型优化工程师](https://xiaomi.jobs.f.mioffice.cn/campus/position/7670910643553863962/detail) | `db9330c69658f65dbc5ab1c726fb2110` | 主要为模型量化/剪枝/蒸馏/推理优化及芯片适配，不属于目标AI应用、Agent或AI评测平台产品开发。 |
| 蔚来 · [蔚来AGI超星计划-敢想敢研，自成课题](https://nio.jobs.feishu.cn/campus/position/7638947328871450890/detail) | `afa239c13efc128396cb365c521c7146` | 这是一条自由申报AI研究课题的开放通道，缺乏确定工程岗位职责与可交付边界。 |

## 保留待补证（33）

这 33 条尚无最终可支撑纳入或排除的证据。必须补采完整岗位职责和要求，或核对该具体岗位的官方校招/实习计划信息；维持 `review_state: needs_review` 并且不计入正式岗位库。后续通过 followup 决策补证，不能覆盖已确认的历史结论。

| 公司 / 岗位 | 事件 ID | 需要补证的事项 |
| --- | --- | --- |
| 联想 · [投后财务分析师](https://talent.lenovo.com.cn/position/detail?id=2414) | `fe6bf9c207aff92759a601df97718e9a` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| MiniMax · 运营 | `a447744650d6877abd3a679c728fcd02` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 理想汽车 · 功率模块工艺开发工程师 | `16561115553f9927dd5c6e1bf58d49d7` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 理想汽车 · 功率模块封装开发工程师 | `41de2c7a60a2868144b156838f596c10` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 吉利控股 · [财务BP 发布于 2026-10-07 全职 全职 不限 不限 浙江·宁波市 浙江·宁波市 允许1个月内投递4个职位，请选择适合的职位进行投递 立即投递](https://campus.geely.com/campus-recruitment/geely/78436/?locale=zh-CN#/job/77aea072-4de5-4e09-98d1-b4b21d84ad3e) | `0c909fcec9c59d89b4aa1fcde71773be` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 商汤科技 · 新界 | `00a911b56e9afd2704fc9ac34cd26094` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 商汤科技 · 北京 | `747c3ecf87787d57fec0cafed3388b25` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 海康威视 · [职位](https://mcampus.hikvision.com/#/position?activeTab=0) | `0488d29fbec30ec4b512f954bf2b7221` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 无问芯穹/Infini-AI · 研发 | `b113e4edb8c7aa15d44caf5e2c56445f` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| MiniMax · 职能 / 支持 | `0e4271cbae9a72bae02821601cf87d6f` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 商汤科技 · 成都 | `82f2112aa4def82dcf27313d4ff860df` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 昆仑万维/天工 · [AI视频 - NLP算法工程师](https://jobs.kunlun.com/459522/position/7516920796661434650/detail) | `9fb9136e4e5d09d2d23ad1993d7c9d72` | 已有完整职责但尚未确认该具体岗位属于校招/实习的官方计划或届次；不得凭“正式”或某个门户路径猜测。 |
| 无问芯穹/Infini-AI · [强化学习训练框架研发工程师](https://infinigence.jobs.feishu.cn/088717/position/7680449713766615346/detail) | `eb39602ccabf44f651a3d73e71631ea1` | 已有完整职责但尚未确认该具体岗位属于校招/实习的官方计划或届次；不得凭“正式”或某个门户路径猜测。 |
| 联想 · [算法工程师](https://talent.lenovo.com.cn/position/detail?id=2335) | `cd2e504ba6bfa1d786bff3351de27e60` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| MiniMax · 产品 / 策划 / 项目 | `c1acb3d7571d497fe8845b114791c394` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| MiniMax · 市场 | `8d18c8b86150dc934b486ea35cd77066` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 商汤科技 · 上海 | `6e90bbdafc1f43a733e8e64ab2bbd466` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 联想 · [AI应用开发工程师](https://talent.lenovo.com.cn/position/detail?id=2351) | `751081f2ac21398502cb65ea883cd167` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 商汤科技 · 新加坡 | `e8f2efd6ecb66e20e3e903ba67c503fa` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 理想汽车 · AI芯片算法工程师-上海 | `cb5943c89bc8a73e701adaf45f8e21a9` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 昆仑万维/天工 · [AI视频 - AI infra 算法工程师](https://jobs.kunlun.com/459522/position/7516919311517255974/detail) | `c98a98b3e2f5954be6750e230ba41800` | 已有完整职责但尚未确认该具体岗位属于校招/实习的官方计划或届次；不得凭“正式”或某个门户路径猜测。 |
| 商汤科技 · [多模态交互产品实习生（小语种方向）](https://hr-jobs.sensetime.com/edu/position/7683462187561552170/detail) | `216ffa0842fdb7cf2e8a6077c278e6f3` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 百川智能 · 北京 | `01f00927438d9c4b4045817ae25cb09a` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 商汤科技 · 杭州 | `f8381edb97e1f4a484e8c9e3707761ea` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 吉利控股 · [急 营销管培生 发布于 2026-10-13 全职 全职 硕士 硕士 浙江·杭州市 浙江·杭州市 允许1个月内投递4个职位，请选择适合的职位进行投递 立即投递](https://campus.geely.com/campus-recruitment/geely/78436/?locale=zh-CN#/job/ba78b62f-c108-42ef-8197-71bb54079fca) | `116973b1b7a0d649c6dbcbcc64fd7130` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 联想 · [AI知识管理工程师](https://talent.lenovo.com.cn/position/detail?id=2343) | `6ea332db27c987cd78747bd144a9bea2` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| MiniMax · 研发 | `b532878a7e58705fbc8d0d4093b2690b` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 理想汽车 · AI芯片算法工程师-杭州 | `b9033f1b2353f458328dbed52fa7516c` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 无问芯穹/Infini-AI · [推理框架开发工程师](https://infinigence.jobs.feishu.cn/088717/position/7547565996359715126/detail) | `e37404a0b9fafe25a98163c0694e4d12` | 已有完整职责但尚未确认该具体岗位属于校招/实习的官方计划或届次；不得凭“正式”或某个门户路径猜测。 |
| 小鹏集团 · [压铸顶岗实习生-广州压铸厂](https://xiaopeng.jobs.feishu.cn/campus/position/7589451831748151579/detail) | `e3c6dfc570ce87510aa911c7a57a05da` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 无问芯穹/Infini-AI · 设计 | `f31849b357f510c4971ae9c1a5bb4be0` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| MiniMax · 设计 | `39dcd9bdeedd618efe5c2bcdb09b1757` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |
| 商汤科技 · 深圳 | `3939ae7f6955487f18f80b0de477bf4d` | 尚未取得该具体岗位可用的完整职责和任职要求，采集内容可能只有地点、栏目或标题；需补采官方JD后再审。 |

## 处理约束

专项文件使用 `followup_for: needs_review`。审核桥只允许后续复核此前为 `needs_review` 的原事件；未有新官方证据时不强行纳入或排除。有效纳入须保留原文职责、学历要求、官方招聘类型依据与逐字的工程交付证据，并通过 `jd.py check`。
