# JD 自动采集状态

最近扫描：2026-10-30T06:54:07Z。登记入口 **69** 个，本次收到 **69** 个来源结果。

自动化只负责官方来源采集、身份/正文指纹比较和待审队列；不会凭关键词把岗位写入正式 JD 库，也不会因一次失败自动删除正式岗位。

本次新事件：新增 **272**、正文/字段变化 **171**、完整扫描中可能消失 **253**。
等待 GPT 筛选：**2550** 条。

| 来源 | 公司 | 状态 | 本次观察 | 基线身份 | 新事件 | 处理 |
| --- | --- | --- | ---: | ---: | ---: | --- |
| official-001 | 小米 | INCOMPLETE | 42 | 835 | 42 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-002 | 快手 | COLLECTED_UNREVIEWED | 260 | 285 | 5 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-003 | 百度 | COLLECTED_UNREVIEWED | 159 | 160 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-004 | 腾讯 | COLLECTED_UNREVIEWED | 888 | 923 | 9 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-005 | 美团 | PARTIAL | 0 | 197 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-006 | 网易 | COLLECTED_UNREVIEWED | 2728 | 3071 | 87 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-007 | 哔哩哔哩 | PARTIAL | 0 | 91 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-008 | 滴滴 | OK | 79 | 79 | 17 | 完整扫描，可判断消失 |
| official-009 | 拼多多 | COLLECTED_UNREVIEWED | 34 | 37 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-010 | 华为 | INCOMPLETE | 102 | 103 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-011 | 小红书 | COLLECTED_UNREVIEWED | 54 | 55 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-012 | 字节跳动 | INCOMPLETE | 8 | 18 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-013 | 阿里巴巴 | COLLECTED_UNREVIEWED | 446 | 480 | 8 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-014 | 蚂蚁集团 | COLLECTED_UNREVIEWED | 464 | 488 | 21 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-015 | 京东 | COLLECTED_UNREVIEWED | 254 | 258 | 9 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-016 | OPPO | COLLECTED_UNREVIEWED | 244 | 246 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-017 | vivo | COLLECTED_UNREVIEWED | 33 | 172 | 7 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-018 | 金山办公/WPS | OK | 49 | 49 | 0 | 完整扫描，可判断消失 |
| official-019 | 荣耀 | COLLECTED_UNREVIEWED | 15 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-020 | 科大讯飞 | COLLECTED_UNREVIEWED | 889 | 913 | 6 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-021 | 携程 | COLLECTED_UNREVIEWED | 10 | 100 | 10 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-022 | 360 | COLLECTED_UNREVIEWED | 99 | 113 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-023 | 得物 | OK | 154 | 154 | 9 | 完整扫描，可判断消失 |
| official-024 | DeepSeek | OK | 36 | 36 | 1 | 完整扫描，可判断消失 |
| official-025 | 月之暗面/Kimi | OK | 94 | 94 | 15 | 完整扫描，可判断消失 |
| official-026 | MiniMax | INCOMPLETE | 6 | 38 | 6 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-027 | 智谱/Z.ai | OK | 28 | 28 | 5 | 完整扫描，可判断消失 |
| official-028 | 阶跃星辰 | INCOMPLETE | 1 | 131 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-029 | 百川智能 | OK | 5 | 5 | 0 | 完整扫描，可判断消失 |
| official-030 | 零一万物/01.AI | OK | 54 | 54 | 4 | 完整扫描，可判断消失 |
| official-031 | 商汤科技 | OK | 144 | 144 | 23 | 完整扫描，可判断消失 |
| official-032 | 生数科技 | OK | 0 | 0 | 0 | 完整扫描，可判断消失 |
| official-033 | 硅基流动 | OK | 27 | 27 | 1 | 完整扫描，可判断消失 |
| official-034 | 面壁智能 | OK | 59 | 59 | 5 | 完整扫描，可判断消失 |
| official-035 | Manus | OK | 23 | 23 | 6 | 完整扫描，可判断消失 |
| official-036 | 无问芯穹/Infini-AI | INCOMPLETE | 23 | 26 | 7 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-037 | 昆仑万维/天工 | INCOMPLETE | 64 | 66 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-038 | Shopee | OK | 47 | 47 | 3 | 完整扫描，可判断消失 |
| official-039 | 联想 | COLLECTED_UNREVIEWED | 82 | 87 | 5 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-040 | 蔚来 | OK | 858 | 858 | 215 | 完整扫描，可判断消失 |
| official-041 | 顺丰 | COLLECTED_UNREVIEWED | 153 | 154 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-042 | 米哈游 | COLLECTED_UNREVIEWED | 252 | 288 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-043 | 大疆 DJI | OK | 142 | 142 | 2 | 完整扫描，可判断消失 |
| official-044 | 度小满 | OK | 35 | 35 | 0 | 完整扫描，可判断消失 |
| official-045 | 海康威视 | COLLECTED_UNREVIEWED | 10 | 11 | 3 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-046 | 中兴通讯 | INCOMPLETE | 2 | 39 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-047 | 深信服 | INCOMPLETE | 10 | 11 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-048 | 金蝶 | OK | 227 | 227 | 1 | 完整扫描，可判断消失 |
| official-049 | 用友 | INCOMPLETE | 8 | 14 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-050 | 美图 | COLLECTED_UNREVIEWED | 20 | 25 | 12 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-051 | SHEIN | INCOMPLETE | 10 | 23 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-052 | 安克创新 | OK | 495 | 495 | 17 | 完整扫描，可判断消失 |
| official-053 | 大华股份 | INCOMPLETE | 2 | 2 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-054 | 吉利控股 | TIMEOUT | 256 | 443 | 48 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-055 | 小鹏集团 | INCOMPLETE | 17 | 644 | 17 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-056 | 理想汽车 | INCOMPLETE | 608 | 639 | 3 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-057 | 海尔集团 | INCOMPLETE | 124 | 139 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-058 | 美的集团 | COLLECTED_UNREVIEWED | 171 | 171 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-059 | 比亚迪 | COLLECTED_UNREVIEWED | 1581 | 1650 | 27 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-060 | 同花顺 | INCOMPLETE | 117 | 128 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-061 | 麒麟软件 | COLLECTED_UNREVIEWED | 87 | 97 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-062 | 普渡机器人 | COLLECTED_UNREVIEWED | 288 | 292 | 3 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-063 | 广联达 | OK | 30 | 30 | 1 | 完整扫描，可判断消失 |
| official-064 | 挚文集团/陌陌 | INCOMPLETE | 1 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-065 | BOSS直聘/看准科技 | INCOMPLETE | 3 | 3 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-066 | 作业帮 | OK | 49 | 49 | 13 | 完整扫描，可判断消失 |
| official-067 | 影石 Insta360 | OK | 363 | 363 | 5 | 完整扫描，可判断消失 |
| official-068 | 神州数码/神州信息 | COLLECTED_UNREVIEWED | 443 | 443 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-069 | 合合信息 | COLLECTED_UNREVIEWED | 82 | 90 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |

待审原始内容见 ../01-data/automation/review-queue.json；扫描基线见 ../01-data/automation/scan-state.json。
首次为某来源建立基线时不会把已有职位批量标记成新增。只有后续身份新增、指纹变化，或一次被确认完整的扫描中身份消失，才生成事件。
