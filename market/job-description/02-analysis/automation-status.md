# JD 自动采集状态

最近扫描：2026-10-27T06:04:54Z。登记入口 **69** 个，本次收到 **69** 个来源结果。

自动化只负责官方来源采集、身份/正文指纹比较和待审队列；不会凭关键词把岗位写入正式 JD 库，也不会因一次失败自动删除正式岗位。

本次新事件：新增 **388**、正文/字段变化 **241**、完整扫描中可能消失 **147**。
等待 GPT 筛选：**2173** 条。

| 来源 | 公司 | 状态 | 本次观察 | 基线身份 | 新事件 | 处理 |
| --- | --- | --- | ---: | ---: | ---: | --- |
| official-001 | 小米 | OK | 793 | 793 | 73 | 完整扫描，可判断消失 |
| official-002 | 快手 | COLLECTED_UNREVIEWED | 260 | 284 | 2 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-003 | 百度 | COLLECTED_UNREVIEWED | 159 | 160 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-004 | 腾讯 | COLLECTED_UNREVIEWED | 893 | 920 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-005 | 美团 | COLLECTED_UNREVIEWED | 196 | 197 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-006 | 网易 | COLLECTED_UNREVIEWED | 2734 | 3010 | 80 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-007 | 哔哩哔哩 | COLLECTED_UNREVIEWED | 89 | 91 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-008 | 滴滴 | OK | 96 | 96 | 4 | 完整扫描，可判断消失 |
| official-009 | 拼多多 | COLLECTED_UNREVIEWED | 34 | 37 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-010 | 华为 | INCOMPLETE | 102 | 103 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-011 | 小红书 | COLLECTED_UNREVIEWED | 54 | 55 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-012 | 字节跳动 | INCOMPLETE | 8 | 18 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-013 | 阿里巴巴 | COLLECTED_UNREVIEWED | 447 | 476 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-014 | 蚂蚁集团 | COLLECTED_UNREVIEWED | 463 | 485 | 2 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-015 | 京东 | COLLECTED_UNREVIEWED | 251 | 254 | 7 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-016 | OPPO | COLLECTED_UNREVIEWED | 245 | 246 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-017 | vivo | COLLECTED_UNREVIEWED | 36 | 165 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-018 | 金山办公/WPS | OK | 49 | 49 | 0 | 完整扫描，可判断消失 |
| official-019 | 荣耀 | COLLECTED_UNREVIEWED | 15 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-020 | 科大讯飞 | COLLECTED_UNREVIEWED | 887 | 910 | 8 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-021 | 携程 | COLLECTED_UNREVIEWED | 10 | 90 | 10 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-022 | 360 | COLLECTED_UNREVIEWED | 99 | 112 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-023 | 得物 | OK | 162 | 162 | 3 | 完整扫描，可判断消失 |
| official-024 | DeepSeek | INCOMPLETE | 0 | 36 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-025 | 月之暗面/Kimi | INCOMPLETE | 1 | 97 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-026 | MiniMax | OK | 32 | 32 | 2 | 完整扫描，可判断消失 |
| official-027 | 智谱/Z.ai | OK | 26 | 26 | 1 | 完整扫描，可判断消失 |
| official-028 | 阶跃星辰 | OK | 130 | 130 | 0 | 完整扫描，可判断消失 |
| official-029 | 百川智能 | OK | 5 | 5 | 1 | 完整扫描，可判断消失 |
| official-030 | 零一万物/01.AI | OK | 54 | 54 | 2 | 完整扫描，可判断消失 |
| official-031 | 商汤科技 | INCOMPLETE | 139 | 150 | 9 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-032 | 生数科技 | OK | 0 | 0 | 0 | 完整扫描，可判断消失 |
| official-033 | 硅基流动 | OK | 26 | 26 | 1 | 完整扫描，可判断消失 |
| official-034 | 面壁智能 | OK | 59 | 59 | 25 | 完整扫描，可判断消失 |
| official-035 | Manus | OK | 24 | 24 | 1 | 完整扫描，可判断消失 |
| official-036 | 无问芯穹/Infini-AI | INCOMPLETE | 17 | 19 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-037 | 昆仑万维/天工 | INCOMPLETE | 66 | 66 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-038 | Shopee | OK | 50 | 50 | 0 | 完整扫描，可判断消失 |
| official-039 | 联想 | COLLECTED_UNREVIEWED | 83 | 87 | 6 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-040 | 蔚来 | INCOMPLETE | 161 | 1029 | 161 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-041 | 顺丰 | COLLECTED_UNREVIEWED | 153 | 154 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-042 | 米哈游 | COLLECTED_UNREVIEWED | 266 | 286 | 2 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-043 | 大疆 DJI | OK | 142 | 142 | 0 | 完整扫描，可判断消失 |
| official-044 | 度小满 | OK | 35 | 35 | 0 | 完整扫描，可判断消失 |
| official-045 | 海康威视 | COLLECTED_UNREVIEWED | 10 | 11 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-046 | 中兴通讯 | INCOMPLETE | 2 | 39 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-047 | 深信服 | INCOMPLETE | 10 | 11 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-048 | 金蝶 | OK | 226 | 226 | 17 | 完整扫描，可判断消失 |
| official-049 | 用友 | INCOMPLETE | 8 | 14 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-050 | 美图 | COLLECTED_UNREVIEWED | 8 | 13 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-051 | SHEIN | INCOMPLETE | 10 | 23 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-052 | 安克创新 | OK | 494 | 494 | 17 | 完整扫描，可判断消失 |
| official-053 | 大华股份 | INCOMPLETE | 2 | 2 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-054 | 吉利控股 | TIMEOUT | 270 | 440 | 102 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-055 | 小鹏集团 | OK | 627 | 627 | 171 | 完整扫描，可判断消失 |
| official-056 | 理想汽车 | INCOMPLETE | 608 | 636 | 26 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-057 | 海尔集团 | INCOMPLETE | 123 | 138 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-058 | 美的集团 | COLLECTED_UNREVIEWED | 171 | 171 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-059 | 比亚迪 | COLLECTED_UNREVIEWED | 1562 | 1629 | 7 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-060 | 同花顺 | INCOMPLETE | 118 | 128 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-061 | 麒麟软件 | COLLECTED_UNREVIEWED | 88 | 97 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-062 | 普渡机器人 | COLLECTED_UNREVIEWED | 287 | 290 | 11 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-063 | 广联达 | INCOMPLETE | 1 | 31 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-064 | 挚文集团/陌陌 | INCOMPLETE | 1 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-065 | BOSS直聘/看准科技 | INCOMPLETE | 3 | 3 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-066 | 作业帮 | INCOMPLETE | 1 | 47 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-067 | 影石 Insta360 | OK | 359 | 359 | 9 | 完整扫描，可判断消失 |
| official-068 | 神州数码/神州信息 | COLLECTED_UNREVIEWED | 439 | 439 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-069 | 合合信息 | COLLECTED_UNREVIEWED | 84 | 90 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |

待审原始内容见 ../01-data/automation/review-queue.json；扫描基线见 ../01-data/automation/scan-state.json。
首次为某来源建立基线时不会把已有职位批量标记成新增。只有后续身份新增、指纹变化，或一次被确认完整的扫描中身份消失，才生成事件。
