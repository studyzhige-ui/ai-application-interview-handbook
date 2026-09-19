# 2027 校招｜官方 Agent / AI 应用工程岗位自动发现结果

> Generated: **2026-09-19 07:05 UTC**
>
> 仅调用公司官方招聘接口 / 官方招聘入口。该文件是 discovery layer；最终 Active JD 仍需确认岗位属于 2027 校招且职责主体不是算法/模型训练。

## 官方源执行状态

| 公司 | 模式 | 状态 | 拉取岗位 | Agent相关非算法候选 | 官方入口 |
|---|---|---:|---:|---:|---|
| 360 | portal_only | PORTAL_ONLY | 0 | 0 | https://hr.360.cn/ |
| DeepSeek | portal_only | PORTAL_ONLY | 0 | 0 | https://talent.deepseek.com/ |
| LiblibAI | portal_only | PORTAL_ONLY | 0 | 0 | https://www.liblib.art/us/joinus |
| Manus | portal_only | PORTAL_ONLY | 0 | 0 | https://manus.im/ |
| MiniMax | portal_only | PORTAL_ONLY | 0 | 0 | https://www.minimax.cn/careers |
| OPPO | portal_only | PORTAL_ONLY | 0 | 0 | https://careers.oppo.com/university/oppo/campus/post?recruitType=Graduate |
| Shopee | portal_only | PORTAL_ONLY | 0 | 0 | https://careers.shopee.cn/ |
| vivo | portal_only | PORTAL_ONLY | 0 | 0 | https://hr.vivo.com/ |
| 京东 | portal_only | PORTAL_ONLY | 0 | 0 | https://campus.jd.com/ |
| 华为 | huawei_api | ERROR；HTTPError: 404 Client Error:  for url: https://career.huawei.com/reccampportal/portal5/position/api/position/queryPositions \| discovered: https://www.hwht.com/#/zh/jobs | 0 | 0 | https://career.huawei.com/cn/ |
| 哔哩哔哩 | bilibili_api | ERROR；HTTPError: 404 Client Error: Not Found for url: https://jobs.bilibili.com/api/positions?page=1&pageSize=100 \| discovered: /api/campus/position/cityList ; /api/campus/position/detail ; /api/campus/position/positionList ; /api/campus/position/postCodeList ; /api/rts/position/query ; /api/rts/position/query/list ; /api/srs/position/cityList ; /api/srs/position/detail | 0 | 0 | https://jobs.bilibili.com/campus/positions |
| 商汤科技 | portal_only | PORTAL_ONLY | 0 | 0 | https://www.sensetime.com/cn/join-us |
| 字节跳动 | portal_only | PORTAL_ONLY | 0 | 0 | https://jobs.bytedance.com/campus/position |
| 小米 | xiaomi_api | ERROR；HTTPError: 404 Client Error: Not Found for url: https://hr.xiaomi.com/api/position/list?pageNum=1&pageSize=100 \| discovered: https://career.mi.com/jobs ; https://info-app-webfile.cnbj1.mi-fds.com/info-app-webfile/recruitment-website/opportunities/Overseas.jpg ; https://info-app-webfile.cnbj1.mi-fds.com/info-app-webfile/recruitment-website/opportunities/beijing.jpg ; https://info-app-webfile.cnbj1.mi-fds.com/info-app-webfile/recruitment-website/opportunities/nanjing.jpg ; https://info-app-webfile.cnbj1.mi-fds.com/info-app-webfile/recruitment-website/opportunities/opportunities-hero4.jpg ; https://info-app-webfile.cnbj1.mi-fds.com/info-app-webfile/recruitment-website/opportunities/shanghai.jpg ; https://info-app-webfile.cnbj1.mi-fds.com/info-app-webfile/recruitment-website/opportunities/shenzhen.jpg ; https://info-app-webfile.cnbj1.mi-fds.com/info-app-webfile/recruitment-website/opportunities/wuhan.jpg | 0 | 0 | https://hr.xiaomi.com/website/opportunities.html?project=%E6%A0%A1%E6%8B%9B&q=agent |
| 小红书 | portal_only | PORTAL_ONLY | 0 | 0 | https://job.xiaohongshu.com/campus |
| 得物 | portal_only | PORTAL_ONLY | 0 | 0 | https://www.dewu.com/ |
| 快手 | kuaishou_api | ERROR；HTTPError: 404 Client Error: Not Found for url: https://zhaopin.kuaishou.cn/recruit/api/job/list?page=1&pageSize=50&workCity=&jobType=&recruitSubProjectCodes=20271779425607 \| discovered: /api/v1/external/position/collect/add ; /api/v1/external/position/collect/cancel ; /api/v1/external/position/collect/list ; /api/v1/open/position/poster/detail ; /api/v1/open/position/poster/list ; /api/v1/open/position/poster/template ; /api/v1/open/positions/check/city ; /api/v1/open/positions/find | 0 | 0 | https://campus.kuaishou.cn/recruit/campus/e/#/campus/jobs?recruitSubProjectCodes=20271779425607 |
| 拼多多 | pdd_api | ERROR；HTTPError: 403 Client Error: Forbidden for url: https://careers.pinduoduo.com/api/position/list?page=1&pageSize=100 \| discovered: api/recruit/position/queryPosition ; api/recruit/position/querySecondPosition ; api/recruit/qa/common/list ; api/recruit/qa/list ; api/recruit/queryByShortLink ; api/recruit/resume/checkModify ; api/recruit/site/query ; api/recruit/sys/secret/set | 0 | 0 | https://careers.pinduoduo.com/campus |
| 携程 | portal_only | PORTAL_ONLY | 0 | 0 | https://campus.ctrip.com/ |
| 无问芯穹/Infini-AI | portal_only | PORTAL_ONLY | 0 | 0 | https://www.infini-ai.com/ |
| 昆仑万维/天工 | portal_only | PORTAL_ONLY | 0 | 0 | https://www.kunlun.com/ |
| 智谱/Z.ai | portal_only | PORTAL_ONLY | 0 | 0 | https://www.zhipuai.cn/zh/joinus |
| 月之暗面/Kimi | portal_only | PORTAL_ONLY | 0 | 0 | https://careers.kimi.com/ |
| 滴滴 | didi_api | ERROR；HTTPError: 404 Client Error:  for url: https://talent.didiglobal.com/api/jobList?page=1&pageSize=100&language=zh \| discovered: /api/get_job_apply_form/ ; /api/outer/ats-apply/website/group-by-job ; /api/outer/ats-apply/website/job ; /api/outer/ats-apply/website/jobs/departments/flat ; /api/outer/ats-apply/website/jobs/departments/structure ; /api/outer/ats-apply/website/jobs/module ; /api/outer/ats-apply/website/jobs/recent ; /api/outer/ats-apply/website/jobs/v2 | 0 | 0 | https://campus.didiglobal.com/ |
| 生数科技 | portal_only | PORTAL_ONLY | 0 | 0 | https://www.shengshu-ai.com/ |
| 百川智能 | portal_only | PORTAL_ONLY | 0 | 0 | https://www.baichuan-ai.com/ |
| 百度 | baidu_api | OK | 0 | 0 | https://talent.baidu.com/jobs/list?projectType=1 |
| 硅基流动 | portal_only | PORTAL_ONLY | 0 | 0 | https://siliconflow.cn/ |
| 科大讯飞 | portal_only | PORTAL_ONLY | 0 | 0 | https://campus.iflytek.com/official-pc/jobList |
| 网易 | netease_api | OK | 2666 | 0 | https://campus.163.com/ |
| 美团 | meituan_api | OK | 0 | 0 | https://zhaopin.meituan.com/web/campus |
| 联想 | portal_only | PORTAL_ONLY | 0 | 0 | https://talent.lenovo.com.cn/ |
| 腾讯 | portal_only | PORTAL_ONLY | 0 | 0 | https://join.qq.com/ |
| 荣耀 | portal_only | PORTAL_ONLY | 0 | 0 | https://career.hihonor.com/ |
| 蔚来 | portal_only | PORTAL_ONLY | 0 | 0 | https://www.nio.cn/careers |
| 蚂蚁集团 | portal_only | PORTAL_ONLY | 0 | 0 | https://talent.antgroup.com/campus-full-list |
| 金山办公/WPS | portal_only | PORTAL_ONLY | 0 | 0 | https://join.wps.cn/ |
| 阶跃星辰 | portal_only | PORTAL_ONLY | 0 | 0 | https://www.stepfun.com/ |
| 阿里巴巴 | portal_only | PORTAL_ONLY | 0 | 0 | https://talent.alibaba.com/campus/position-list |
| 零一万物/01.AI | portal_only | PORTAL_ONLY | 0 | 0 | https://www.01.ai/ |
| 面壁智能 | portal_only | PORTAL_ONLY | 0 | 0 | https://www.modelbest.cn/ |
| 顺丰 | portal_only | PORTAL_ONLY | 0 | 0 | https://hr.sf-express.com/ |

## 自动发现候选

> 本轮官方 API 未返回匹配候选；请查看上方 ERROR / PORTAL_ONLY 状态，并继续从官方校园招聘入口人工核验。
