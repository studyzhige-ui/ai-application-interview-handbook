# 官方招聘岗位源全覆盖审计

> 本文件同时记录“当前严格 JD 结果是否闭环”和“自动维护链路是否已经由完整运行重新证明”。这两件事分开验收，避免再次出现配置有 URL 就显示全绿。

## 当前结果闭环

- 固定公司：**41**
- 可枚举固定路径：**41/41**
- 严格结果闭环：**41/41**
- 命中目标岗位公司：**15**
- 严格 Role Family：**196**
- 第一方完整 JD：**189**
- 第一方仅标题：**7**

## 自动维护运行证明

- 已有完整枚举证明：**16/41**
- 固定职位池可达、待新版完整穷举重跑：**24**
- 自动链路仍 BLOCKED：**1**

> 当前 41 家已经都有明确严格结果；但 GitHub Actions 当前未能进入任何执行 step，因此新的 41/41 Runtime Certification 尚不能伪造为完成。自动任务恢复后，审计必须跑到 41/41 ENUMERATED 才会通过。

## 逐公司

| 公司 | 招聘池范围 | 当前严格结果 | Role Family | 完整 JD | 仅标题 | Runtime | 固定职位池 |
|---|---|---|---:|---:|---:|---|---|
| 小米 | campus | HAS_TARGET_JDS | 7 | 7 | 0 | ENUMERATED | https://xiaomi.jobs.f.mioffice.cn/campus/ |
| 快手 | campus | HAS_TARGET_JDS | 8 | 8 | 0 | ENUMERATED | https://campus.kuaishou.cn/recruit/campus/e/ |
| 百度 | campus | HAS_TARGET_JDS | 5 | 5 | 0 | ENUMERATED | https://talent.baidu.com/jobs/list?projectType=1 |
| 腾讯 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | ENUMERATED | https://join.qq.com/post.html |
| 美团 | campus | HAS_TARGET_JDS | 2 | 2 | 0 | ENUMERATED | https://zhaopin.meituan.com/web/campus |
| 网易 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | ENUMERATED | https://campus.163.com/ |
| 哔哩哔哩 | campus | HAS_TARGET_JDS | 1 | 0 | 1 | ENUMERATED | https://jobs.bilibili.com/campus/positions |
| 滴滴 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | ENUMERATED | https://campus.didiglobal.com/campus_apply/didiglobal/96064#/jobs |
| 拼多多 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | ENUMERATED | https://careers.pddglobalhr.com/campus/grad |
| 华为 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://career.huawei.com/cn/campus-recruitment |
| 小红书 | campus | HAS_TARGET_JDS | 6 | 6 | 0 | LIST_REACHABLE | https://job.xiaohongshu.com/campus/position |
| 字节跳动 | campus | HAS_TARGET_JDS | 130 | 130 | 0 | ENUMERATED | https://jobs.bytedance.com/campus/position |
| 阿里巴巴 | campus | HAS_TARGET_JDS | 18 | 18 | 0 | ENUMERATED | https://campus-talent.alibaba.com/campus/position?batchId=100000760001 |
| 蚂蚁集团 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://talent.antgroup.com/campus-full-list |
| 京东 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | ENUMERATED | https://campus.jd.com/ |
| OPPO | campus | HAS_TARGET_JDS | 5 | 5 | 0 | ENUMERATED | https://careers.oppo.com/university/oppo/campus/post?recruitType=Graduate |
| vivo | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://hr-campus.vivo.com/campus/jobs |
| 金山办公/WPS | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | ENUMERATED | https://join.wps.cn/ |
| 荣耀 | campus | HAS_TARGET_JDS | 3 | 0 | 3 | LIST_REACHABLE | https://career.honor.com/SU60eea919bef57c1023f6fe78/pb/school.html |
| 科大讯飞 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://iflytek.zhiye.com/5/jobs |
| 携程 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://careers.ctrip.com/#/campus |
| 360 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://360campus.zhiye.com/campus/jobs |
| 得物 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://poizon.jobs.feishu.cn/578078/ |
| DeepSeek | official_recruiting | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://app.mokahr.com/social-recruitment/high-flyer/140576#/ |
| 月之暗面/Kimi | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://app.mokahr.com/campus-recruitment/moonshot/148507 |
| MiniMax | campus | HAS_TARGET_JDS | 1 | 1 | 0 | LIST_REACHABLE | https://vrfi1sk8a0.jobs.feishu.cn/379481/?project=7495675705720965415 |
| 智谱/Z.ai | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://app.mokahr.com/campus-recruitment/zphz/148984 |
| 阶跃星辰 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://app.mokahr.com/campus-recruitment/step/94905 |
| 百川智能 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://cq6qe6bvfr6.jobs.feishu.cn/646926/?project=7676396828845639987 |
| 零一万物/01.AI | official_recruiting | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://01ai.jobs.feishu.cn/index/ |
| 商汤科技 | campus | HAS_TARGET_JDS | 5 | 5 | 0 | LIST_REACHABLE | https://hr-jobs.sensetime.com/edu/ |
| 生数科技 | official_recruiting | ZERO_TARGET_JDS | 0 | 0 | 0 | BLOCKED | https://shengshu.jobs.feishu.cn/index/ |
| 硅基流动 | official_recruiting | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://app.mokahr.com/su/Idzsq |
| 面壁智能 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://modelbest.jobs.feishu.cn/campus/position/list?spread=NEDQRTH |
| Manus | official_recruiting | HAS_TARGET_JDS | 1 | 1 | 0 | LIST_REACHABLE | https://jobs.ashbyhq.com/manusai |
| 无问芯穹/Infini-AI | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://infinigence.jobs.feishu.cn/088717 |
| 昆仑万维/天工 | official_recruiting | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://jobs.kunlun.com/459522/position/list |
| Shopee | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://app.mokahr.com/campus_apply/shopee/2962#/jobs |
| 联想 | campus | HAS_TARGET_JDS | 3 | 0 | 3 | ENUMERATED | https://talent.lenovo.com.cn/position?jobTypeName=AI%E5%BC%80%E5%8F%91%E7%B1%BB&projectType=1 |
| 蔚来 | campus | ZERO_TARGET_JDS | 0 | 0 | 0 | LIST_REACHABLE | https://nio.jobs.feishu.cn/campus/ |
| 顺丰 | campus | HAS_TARGET_JDS | 1 | 1 | 0 | ENUMERATED | https://campus.sf-express.com/positionList |

## 状态解释

- `HAS_TARGET_JDS`：当前第一方招聘池中存在严格非算法 AI 应用 / Agent 工程岗位。
- `ZERO_TARGET_JDS`：公司仍在官方搜索矩阵中，但本轮严格 Gate 后没有岗位进入正式库；不代表公司没有其他招聘。
- `FULL_JD`：已经保存第一方职责 / 任职要求正文；`TITLE_ONLY_OFFICIAL`：只从第一方当前职位列表确认标题，不用二手来源补写。
- `ENUMERATED`：已有一次完整分页/官方 API 枚举证明；`LIST_REACHABLE`：入口可达但旧快照没有完整穷举证明；`BLOCKED`：自动采集链路仍需修复。
- 当前结果库与 Runtime Certification 分离：结果可以基于同日第一方快照与官网核验闭环，但定时维护只有在 41/41 自动枚举后才允许全绿。
