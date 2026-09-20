# 官方 AI / Agent 工程岗位覆盖审计

> 公司扫描覆盖、当前目标岗位存在性、自动抓取 Runtime 三者分开。公司当前 0 岗不会被移出长期扫描池；抓取失败也不能解释为 0 岗。

## 扫描池覆盖

- 固定长期扫描公司：**69/69**
- 第一方官方招聘 / 校招入口 READY：**69/69**
- 当前有目标岗位：**49**
- 完整枚举后确认当前 0 个目标岗位：**11**
- 仍需完成本轮枚举：**9**
- Role Family：**366**
- 第一方完整 JD：**333**

## Runtime 诊断

- ENUMERATED：**41/69**
- LIST_REACHABLE：**3**
- BLOCKED：**25**
- Browser cache fresh：**YES**
- Feishu cache fresh：**YES**
- Moka cache fresh：**YES**

## 逐公司

| 公司 | 主要业务 | 官方职位池 | 当前目标岗 | Runtime | 代表岗位 |
|---|---|---|---|---|---|
| 小米 | 智能手机、IoT、操作系统、智能汽车与 AI | https://xiaomi.jobs.f.mioffice.cn/campus/ | HAS_TARGET_JDS | BLOCKED | Agent Harness 研发工程师 |
| 快手 | 短视频、直播、电商、广告与 AI | https://campus.kuaishou.cn/recruit/campus/e/ | HAS_TARGET_JDS | ENUMERATED | AI Agent 全栈工程师-Agent 应用研发方向 |
| 百度 | 搜索、生成式 AI、智能云与自动驾驶 | https://talent.baidu.com/jobs/list?projectType=1 | HAS_TARGET_JDS | ENUMERATED | 2027AIDU-Agent应用全栈工程师(J99974) |
| 腾讯 | 社交、游戏、内容、云计算、金融科技与 AI | https://join.qq.com/post.html | HAS_TARGET_JDS | ENUMERATED | 面向 Agent 应用开发的易用 API 抽象与平台化建设 |
| 美团 | 本地生活、外卖、即时零售、旅游与配送科技 | https://zhaopin.meituan.com/web/campus | HAS_TARGET_JDS | ENUMERATED | 【北斗】CodeAgent AI工程师 |
| 网易 | 游戏、音乐、教育、内容与互联网服务 | https://campus.163.com/ | HAS_TARGET_JDS | ENUMERATED | AI全栈开发工程师（暴雪） |
| 哔哩哔哩 | 视频社区、直播、游戏与内容生态 | https://jobs.bilibili.com/campus/positions | HAS_TARGET_JDS | ENUMERATED | AI Native 基础架构工程师【2027届】 |
| 滴滴 | 网约车、出行平台、自动驾驶与物流 | https://campus.didiglobal.com/campus_apply/didiglobal/96064#/jobs | ZERO_TARGET_JDS | ENUMERATED |  |
| 拼多多 | 电商、Temu、供应链与平台技术 | https://careers.pddglobalhr.com/campus/grad | ZERO_TARGET_JDS | ENUMERATED |  |
| 华为 | 通信设备、云、终端、计算、汽车 ICT 与 AI | https://career.huawei.com/cn/campus-recruitment | ZERO_TARGET_JDS | ENUMERATED |  |
| 小红书 | 内容社区、生活方式、电商与广告 | https://job.xiaohongshu.com/campus/position | HAS_TARGET_JDS | ENUMERATED | 【REDstar】AI Agent Infra 工程师 |
| 字节跳动 | 抖音/TikTok、内容平台、云与大模型 AI | https://jobs.bytedance.com/campus/position | HAS_TARGET_JDS | BLOCKED | AI Agent开发工程师 - 抖音研发 |
| 阿里巴巴 | 电商、云计算、本地生活、物流与企业 AI | https://campus-talent.alibaba.com/campus/position?batchId=100000760001 | HAS_TARGET_JDS | ENUMERATED | AI Agent 应用研发&系统架构-阿里星/A Star |
| 蚂蚁集团 | 支付、金融科技、企业科技与 AI | https://talent.antgroup.com/campus-full-list | HAS_TARGET_JDS | ENUMERATED | FDE-前线部署工程师 |
| 京东 | 电商、物流、零售科技、云与企业服务 | https://campus.jd.com/ | HAS_TARGET_JDS | ENUMERATED | 多智能体强化学习驱动的物流决策系统研发 |
| OPPO | 智能手机、IoT、操作系统与端侧 AI | https://careers.oppo.com/university/oppo/campus/post?recruitType=Graduate | HAS_TARGET_JDS | ENUMERATED | AI全栈工程师 |
| vivo | 智能手机、操作系统、IoT 与端侧 AI | https://hr-campus.vivo.com/campus/jobs | HAS_TARGET_JDS | ENUMERATED | Agent技术工程师-27届秋招 |
| 金山办公/WPS | 办公软件、协同办公与办公 AI | https://join.wps.cn/ | HAS_TARGET_JDS | BLOCKED | AI应用开发工程师 |
| 荣耀 | 智能手机、PC、IoT 与 AI OS | https://career.honor.com/SU60eea919bef57c1023f6fe78/pb/school.html | ZERO_TARGET_JDS | ENUMERATED |  |
| 科大讯飞 | 语音 AI、大模型、教育、医疗与企业 AI | https://iflytek.zhiye.com/5/jobs | HAS_TARGET_JDS | ENUMERATED | 【星火X计划】面向通用大模型智能体强化学习的Infra工程(J13988) |
| 携程 | 在线旅游、酒店机票与旅行 AI | https://careers.ctrip.com/#/campus | HAS_TARGET_JDS | ENUMERATED | 云原生研发工程师（AI Agent方向）（2027届秋招）(MJ036678) |
| 360 | 网络安全、搜索/浏览器、AI 助手与企业安全 | https://360campus.zhiye.com/campus/jobs | HAS_TARGET_JDS | ENUMERATED | 27秋招-AI应用开发工程师（AIOps）（北京）-5389(J12461) |
| 得物 | 潮流电商、社区、鉴别与交易服务 | https://poizon.jobs.feishu.cn/578078/ | ZERO_TARGET_JDS | ENUMERATED |  |
| DeepSeek | 基础大模型、推理模型与模型服务 | https://app.mokahr.com/social-recruitment/high-flyer/140576#/ | ZERO_TARGET_JDS | ENUMERATED |  |
| 月之暗面/Kimi | 大模型、Kimi AI 助手与 Agent | https://app.mokahr.com/campus-recruitment/moonshot/148507 | HAS_TARGET_JDS | BLOCKED | Agent Development Engineer（实习） |
| MiniMax | 多模态大模型、AI 产品与 Agent | https://vrfi1sk8a0.jobs.feishu.cn/379481/?project=7495675705720965415 | HAS_TARGET_JDS | BLOCKED | AGI产品研发工程师-应届生-TOP Talent |
| 智谱/Z.ai | GLM 大模型、模型 API 与 Agent 平台 | https://app.mokahr.com/campus-recruitment/zphz/148984 | HAS_TARGET_JDS | ENUMERATED | 26届春招-大模型应用开发工程师（Java） |
| 阶跃星辰 | 多模态基础模型、AI 平台与应用 | https://app.mokahr.com/campus-recruitment/step/94905 | HAS_TARGET_JDS | BLOCKED | Coding Agent 全栈工程师 |
| 百川智能 | 大模型与企业/行业 AI 应用 | https://cq6qe6bvfr6.jobs.feishu.cn/646926/?project=7676396828845639987 | HAS_TARGET_JDS | BLOCKED | 【源点顶尖人才计划】AI Infra工程师-推理方向实习生 |
| 零一万物/01.AI | 大模型、企业 AI 与 AI 应用 | https://01ai.jobs.feishu.cn/index/ | HAS_TARGET_JDS | BLOCKED | AI 测试工程师 |
| 商汤科技 | 大模型、计算机视觉、AI 基础设施与行业应用 | https://hr-jobs.sensetime.com/edu/ | HAS_TARGET_JDS | BLOCKED | 【27届校招】Agent开发工程师 |
| 生数科技 | 视频生成、多模态生成模型与 Vidu | https://shengshu.jobs.feishu.cn/index/ | HAS_TARGET_JDS | BLOCKED | Agent平台开发工程师 (YH) |
| 硅基流动 | 模型推理云、模型 API 与 AI Infra | https://app.mokahr.com/su/Idzsq | HAS_TARGET_JDS | BLOCKED | 端侧AI Agent工程师(A24765) |
| 面壁智能 | 端侧大模型、小模型与 Agent | https://modelbest.jobs.feishu.cn/campus/position/list?spread=NEDQRTH | HAS_TARGET_JDS | BLOCKED | Agentic Engineering |
| Manus | 通用 AI Agent | https://jobs.ashbyhq.com/manusai | NEEDS_ENUMERATION | LIST_REACHABLE |  |
| 无问芯穹/Infini-AI | AI Infra、异构算力与训练/推理平台 | https://infinigence.jobs.feishu.cn/088717 | HAS_TARGET_JDS | BLOCKED | 推理框架开发工程师 |
| 昆仑万维/天工 | 大模型、天工 AI、互联网与海外业务 | https://jobs.kunlun.com/459522/position/list | HAS_TARGET_JDS | BLOCKED | Agent框架工程师 |
| Shopee | 东南亚电商、金融科技、物流与 AI | https://app.mokahr.com/campus_apply/shopee/2962#/jobs | HAS_TARGET_JDS | BLOCKED | Agent开发工程师 |
| 联想 | PC、智能设备、服务器、企业基础设施与 AI | https://talent.lenovo.com.cn/position?jobTypeName=AI%E5%BC%80%E5%8F%91%E7%B1%BB&projectType=1 | HAS_TARGET_JDS | ENUMERATED | AI Agent开发工程师 |
| 蔚来 | 智能电动车、智能驾驶、能源服务与 AI | https://nio.jobs.feishu.cn/campus/ | HAS_TARGET_JDS | BLOCKED | Super Sparks-校招-车端智能体框架和应用工程师 |
| 顺丰 | 快递、物流、供应链科技与 AI | https://campus.sf-express.com/positionList | HAS_TARGET_JDS | ENUMERATED | AI全栈研发工程师（顺丰科技） |
| 米哈游 | 游戏、IP、互动娱乐、游戏研发技术与 AI | https://jobs.mihoyo.com/#/campus | NEEDS_ENUMERATION | BLOCKED |  |
| 大疆 DJI | 无人机、影像设备、行业机器人与智能硬件 | https://careers.dji.com/zh-CN/campus/hot-jobs?source=campus_hotjobs | HAS_TARGET_JDS | ENUMERATED | AI DevOps 工程师 |
| 度小满 | 消费金融、财富管理、支付与金融科技 | https://campus.duxiaoman.com/ | HAS_TARGET_JDS | BLOCKED | AI全栈研发工程师-大数据引擎/云原生方向 |
| 海康威视 | 智慧物联、视频技术、企业数字化与 AIoT | https://mcampus.hikvision.com/#/position?activeTab=0 | NEEDS_ENUMERATION | BLOCKED |  |
| 中兴通讯 | 通信网络、算力、云、终端、企业数字化与 AI | https://job.zte.com.cn/cn/campus-recruitment/Recruitment_positions/freshstudent.html | HAS_TARGET_JDS | ENUMERATED | AI应用开发资深专家 |
| 深信服 | 网络安全、云计算、企业 IT 与 AI | https://hr.sangfor.com/schoolRecruitment | NEEDS_ENUMERATION | BLOCKED |  |
| 金蝶 | ERP、企业云 SaaS、企业管理软件与企业 AI | https://app.mokahr.com/campus-recruitment/kingdeehr/166565?locale=zh-CN | HAS_TARGET_JDS | ENUMERATED | 应用开发工程师-FDE（深圳） |
| 用友 | ERP、BIP、企业软件与企业级 AI | https://career.yonyou.com/SU67ac41886202cc7916ae3029/pb/school.html | ZERO_TARGET_JDS | ENUMERATED |  |
| 美图 | 图像/视频应用、AI 影像、内容生成与设计工具 | https://hr.meitu.com/ | ZERO_TARGET_JDS | ENUMERATED |  |
| SHEIN | 全球时尚电商、供应链平台与电商技术 | https://careers.shein.cn/Students | NEEDS_ENUMERATION | LIST_REACHABLE |  |
| 安克创新 | 充电、影音、智能家居、安防与储能消费电子 | https://career.anker.com.cn/universities/recruitment/new/ | ZERO_TARGET_JDS | ENUMERATED |  |
| 大华股份 | 智慧物联、视频 AI、智慧城市与企业数字化 | https://job.dahuatech.com/ | HAS_TARGET_JDS | ENUMERATED | 【研发中心】2027届大数据工程师（Agent方向）(J24380) |
| 吉利控股 | 汽车、智能电动车、智能座舱与汽车 AI | https://campus.geely.com/campus-recruitment/geely/78436/?locale=zh-CN#/jobs?commitment%5B0%5D=%E5%85%A8%E8%81%8C&page=1&anchorName=jobsList | NEEDS_ENUMERATION | BLOCKED |  |
| 小鹏集团 | 智能电动车、Physical AI、机器人与飞行汽车 | https://xiaopeng.jobs.feishu.cn/campus | NEEDS_ENUMERATION | BLOCKED |  |
| 理想汽车 | 智能电动车、智能驾驶、具身智能与智能硬件 | https://www.lixiang.com/employ/campus/list.html?fromJob=1&employchannelcode=H56UNDK&job_mode=1 | HAS_TARGET_JDS | ENUMERATED | 智能体应用软件研发工程师 |
| 海尔集团 | 智慧家庭、工业互联网、医疗健康与工业 AI | https://maker.haier.net/client/campus/activityindex.html | HAS_TARGET_JDS | ENUMERATED | FDE工程师（AI前线部署工程师） |
| 美的集团 | 智能家居、工业技术、楼宇、机器人与新能源 | https://newpower.midea.com/ | ZERO_TARGET_JDS | ENUMERATED |  |
| 比亚迪 | 新能源汽车、电池、新能源、电子与轨道交通 | https://job.byd.com/ | NEEDS_ENUMERATION | LIST_REACHABLE |  |
| 同花顺 | 金融信息服务、证券软件、金融数据与金融 AI | https://campus.10jqka.com.cn/ | HAS_TARGET_JDS | ENUMERATED | 金融 Agent 开发工程师（AIME项目） |
| 麒麟软件 | 国产操作系统、服务器/桌面 OS 与 AI OS | https://kylinos.zhiye.com/campus/jobs | ZERO_TARGET_JDS | ENUMERATED |  |
| 普渡机器人 | 商用服务机器人、具身智能与机器人软件 | https://pudutech.zhiye.com/campus/jobs | HAS_TARGET_JDS | ENUMERATED | Agent开发工程师(J12678) |
| 广联达 | BIM、数字建筑、工程软件与建筑产业 AI | https://app.mokahr.com/campus-recruitment/glodon/91966 | HAS_TARGET_JDS | BLOCKED | 27届校招-AI Agent开发工程师 |
| 挚文集团/陌陌 | 移动社交、直播与泛娱乐 | https://campus.hellogroup.com/ | HAS_TARGET_JDS | ENUMERATED | 【2027校招正式批】Agent开发工程师 |
| BOSS直聘/看准科技 | 在线招聘、人力资源平台与招聘科技 | https://m.zhipin.com/zhaopin/8d0140fe120765a01nF_2Ni8EQ~~/ | HAS_TARGET_JDS | BLOCKED | 大模型应用工程师（校招） |
| 作业帮 | 教育科技、学习工具、智能硬件与教育 AI | https://app.mokahr.com/campus-recruitment/zuoyebang/144908?locale=zh-CN | HAS_TARGET_JDS | ENUMERATED | AI全栈开发工程师（海外新业务）-27秋招 |
| 影石 Insta360 | 全景相机、运动相机、智能影像与 AI 影像软件 | https://arashivision.jobs.feishu.cn/campus/position/list | NEEDS_ENUMERATION | BLOCKED |  |
| 神州数码/神州信息 | IT 基础设施、金融科技、云服务与企业数字化 | https://dcits.zhiye.com/campus/jobs | HAS_TARGET_JDS | ENUMERATED | 2027届-AI大模型工程师（政企方向）北京(J22570) |
| 合合信息 | OCR/文档 AI、扫描全能王、数据智能与企业服务 | https://intsig.zhiye.com/campus/jobs | HAS_TARGET_JDS | ENUMERATED | 【27校招】AI Agent研发工程师(J14439) |

## 验收规则

- 69/69 公司必须始终保留固定第一方职位池；公司扫描覆盖是硬失败条件。
- HAS_TARGET_JDS 表示已有符合非算法 AI/Agent 工程范围的岗位；ZERO_TARGET_JDS 只允许在完整枚举后产生。
- NEEDS_ENUMERATION 表示自动维护链路尚未完成该公司的本轮完整分页/关键词穷举，不等价于无岗位。
- Runtime ENUMERATED 与岗位存在性分开；任何一次 WAF/API/browser 失败不得删除历史 VERIFIED_ROLE。
- 正式 JD 继续只接受第一方公司官网或公司官方 ATS 正文。
