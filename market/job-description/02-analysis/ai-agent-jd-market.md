# 当前校招｜AI 应用开发 & Agent / 智能体研发官方 JD 市场库

> **正式口径：69 家长期目标公司扫描池 + 第一方招聘/校招入口 + 非算法 AI/Agent 工程岗位。公司是否当前有目标岗是扫描结果，不是进入扫描池的前置条件。**
>
> 自动抓取失败不再等价于“公司没有岗位”。岗位存在性由持久化核验索引维护；第一方 API / ATS 自动化负责刷新、扩充和补全文，不负责在失败时删除已核验事实。

## 3. 当前快照｜2026-09-20

- **长期扫描公司：69 家。**
- **第一方招聘 / 校招入口：69/69 已登记。**
- **原 41 家已核验目标工程岗位事实全部保留；新增 28 家进入首次完整枚举。**
- **公司状态与岗位状态分离：允许 HAS_TARGET_JDS / ZERO_TARGET_JDS / NEEDS_ENUMERATION。**
- **严格 Role Family：230。**
- **第一方完整 JD：190 个 Role Family。**
- **第一方仅标题：7 个；当前岗位已核验、待补第一方正文：33 个。**
- 旧抓取器的 0 命中已废止为岗位结论：它只能表示“本次自动枚举没有抓到”，不能表示“公司没有相关岗位”。

## 4. 已核验目标岗位公司（长期扫描池共 69 家）

| 公司 | 官方招聘 / 校招入口 | 已核验代表岗位 | 招聘类型 | JD / 证据状态 |
|---|---|---|---|---|
| 小米 | https://xiaomi.jobs.f.mioffice.cn/campus/ | Agent Harness 研发工程师 | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 快手 | https://campus.kuaishou.cn/recruit/campus/e/ | AI应用开发工程师 | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 百度 | https://talent.baidu.com/jobs/list?projectType=1 | 2027AIDU-Agent应用全栈工程师(J99974) | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 腾讯 | https://join.qq.com/post.html | Agent开发工程师 | 2027校园招聘 | ROLE_VERIFIED |
| 美团 | https://zhaopin.meituan.com/web/campus | AI应用开发工程师 | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 网易 | https://campus.163.com/ | AI Agent 应用开发工程师 | 2027校园招聘 | ROLE_VERIFIED |
| 哔哩哔哩 | https://jobs.bilibili.com/campus/positions | 【B-UP】多模态智能体工程师（校招） | 当前校园招聘 | TITLE_ONLY_FIRST_PARTY |
| 滴滴 | https://campus.didiglobal.com/campus_apply/didiglobal/96064#/jobs | 27届秋招-自动驾驶-AI Agent工程师 | 2027校园招聘 | ROLE_VERIFIED |
| 拼多多 | https://careers.pddglobalhr.com/campus/grad | AI Agent研发工程师 | 2027校园招聘 | JD_VERIFIED_EXTERNAL_OR_FIRST_PARTY |
| 华为 | https://career.huawei.com/cn/campus-recruitment | AI应用平台开发工程师 | 2027校园招聘 | JD_VERIFIED_EXTERNAL_OR_FIRST_PARTY |
| 小红书 | https://job.xiaohongshu.com/campus/position | 【REDstar】AI Agent Infra 工程师 | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 字节跳动 | https://jobs.bytedance.com/campus/position | AI Agent开发工程师 - 抖音研发 | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 阿里巴巴 | https://campus-talent.alibaba.com/campus/position?batchId=100000760001 | AI Agent应用开发工程师 | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 蚂蚁集团 | https://talent.antgroup.com/campus-full-list | Agent研发工程师 | 2027届实习 / 校园人才池 | JD_VERIFIED_EXTERNAL_OR_FIRST_PARTY |
| 京东 | https://campus.jd.com/ | Agent开发工程师 | 当前官方招聘 | FULL_FIRST_PARTY_JD |
| OPPO | https://careers.oppo.com/university/oppo/campus/post?recruitType=Graduate | AI Agent 研发工程师（研发效能方向） | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| vivo | https://hr-campus.vivo.com/campus/jobs | Agent技术工程师-27届秋招 | 2027校园招聘 | ROLE_VERIFIED |
| 金山办公/WPS | https://join.wps.cn/ | AI应用开发工程师 | 当前官方招聘 / 2027校招池 | JD_VERIFIED_EXTERNAL_OR_FIRST_PARTY |
| 荣耀 | https://career.honor.com/SU60eea919bef57c1023f6fe78/pb/school.html | AI软件开发工程师 （AI Coding / Agent方向） | 当前校园招聘 | TITLE_ONLY_FIRST_PARTY |
| 科大讯飞 | https://iflytek.zhiye.com/5/jobs | Agent研发工程师-Harness方向 | 2027秋季校园招聘 | ROLE_VERIFIED |
| 携程 | https://careers.ctrip.com/#/campus | Agent开发工程师（2027届秋招） | 2027秋季校园招聘 | JD_VERIFIED_EXTERNAL_OR_FIRST_PARTY |
| 360 | https://360campus.zhiye.com/campus/jobs | AI应用工程师——AI系统软件 | 2027届实习招聘 | ROLE_VERIFIED |
| 得物 | https://poizon.jobs.feishu.cn/578078/ | 【27届校招】中间件AI开发工程师（Golang方向） | 2027秋季校园招聘 | JD_VERIFIED_EXTERNAL_OR_FIRST_PARTY |
| DeepSeek | https://app.mokahr.com/social-recruitment/high-flyer/140576#/ | Agent Harness 研发工程师 | 当前官方招聘 | ROLE_VERIFIED |
| 月之暗面/Kimi | https://app.mokahr.com/campus-recruitment/moonshot/148507 | Agent Development Engineer（实习） | 2027/2028校园招聘与实习 | ROLE_VERIFIED |
| MiniMax | https://vrfi1sk8a0.jobs.feishu.cn/379481/?project=7495675705720965415 | AGI产品研发工程师-应届生-TOP Talent | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 智谱/Z.ai | https://app.mokahr.com/campus-recruitment/zphz/148984 | AI研发工程师-Agent Tools/大模型应用方向 | 当前官方招聘（非算法工程） | ROLE_VERIFIED |
| 阶跃星辰 | https://app.mokahr.com/campus-recruitment/step/94905 | Coding Agent 全栈工程师 | 当前官方招聘；公司同时开放2027校园招聘 | ROLE_VERIFIED |
| 百川智能 | https://cq6qe6bvfr6.jobs.feishu.cn/646926/?project=7676396828845639987 | 【源点顶尖人才计划】AI Infra工程师-推理方向实习生 | 2027及以后在校生/可转正 | JD_VERIFIED_EXTERNAL_OR_FIRST_PARTY |
| 零一万物/01.AI | https://01ai.jobs.feishu.cn/index/ | AI 测试工程师 | 当前官方招聘 | FULL_FIRST_PARTY_JD |
| 商汤科技 | https://hr-jobs.sensetime.com/edu/ | 【27届校招】Agent开发工程师 | 当前校园招聘 | FULL_FIRST_PARTY_JD |
| 生数科技 | https://shengshu.jobs.feishu.cn/index/ | 流式视频 Agent 工程师 | 当前官方招聘（正式/实习） | ROLE_VERIFIED |
| 硅基流动 | https://app.mokahr.com/su/Idzsq | 端侧AI Agent工程师(A24765) | 当前官方招聘 | ROLE_VERIFIED |
| 面壁智能 | https://modelbest.jobs.feishu.cn/campus/position/list?spread=NEDQRTH | Agentic Engineering | 2027/2028/2029顶尖人才实习 | ROLE_VERIFIED |
| Manus | https://jobs.ashbyhq.com/manusai | AI Agent Engineer | 当前官方招聘 | FULL_FIRST_PARTY_JD |
| 无问芯穹/Infini-AI | https://infinigence.jobs.feishu.cn/088717 | 推理框架开发工程师 | 2027秋季校园招聘 | ROLE_VERIFIED |
| 昆仑万维/天工 | https://jobs.kunlun.com/459522/position/list | Agent框架工程师 | 当前官方招聘 | ROLE_VERIFIED |
| Shopee | https://app.mokahr.com/campus_apply/shopee/2962#/jobs | Agent开发工程师 | 2027秋季校园招聘 | ROLE_VERIFIED |
| 联想 | https://talent.lenovo.com.cn/position?jobTypeName=AI%E5%BC%80%E5%8F%91%E7%B1%BB&projectType=1 | AI Agent开发工程师 | 当前校园招聘 | TITLE_ONLY_FIRST_PARTY |
| 蔚来 | https://nio.jobs.feishu.cn/campus/ | Super Sparks-校招-车端智能体框架和应用工程师 | 2027校园招聘 | JD_VERIFIED_EXTERNAL_OR_FIRST_PARTY |
| 顺丰 | https://campus.sf-express.com/positionList | AI开发工程师（顺丰科技） | 当前校园招聘 | FULL_FIRST_PARTY_JD |

> 这张表只展示当前已有持久化岗位事实的公司；完整 69 家公司及其第一方职位入口见 [company-scan-pool.md](company-scan-pool.md)。完整职位族和 JD 见 [official-2027-agent-jobs.generated.md](../01-data/official-2027-agent-jobs.generated.md)。

## 5. 第一方材料与采集记录

[人工核验岗位正文](../01-data/curated-official-jds.md) · [采集策略](../03-strategy/collection-policy.md) · [采集日志](../05-logs/collection-history.md)
