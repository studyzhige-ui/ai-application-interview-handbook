# JD 自动采集状态

最近扫描：2026-10-20T05:48:16Z。登记入口 **69** 个，本次收到 **69** 个来源结果。

自动化只负责官方来源采集、身份/正文指纹比较和待审队列；不会凭关键词把岗位写入正式 JD 库，也不会因一次失败自动删除正式岗位。

本次新事件：新增 **258**、正文/字段变化 **145**、完整扫描中可能消失 **26**。
等待 GPT 筛选：**1124** 条。

| 来源 | 公司 | 状态 | 本次观察 | 基线身份 | 新事件 | 处理 |
| --- | --- | --- | ---: | ---: | ---: | --- |
| official-001 | 小米 | OK | 796 | 796 | 28 | 完整扫描，可判断消失 |
| official-002 | 快手 | COLLECTED_UNREVIEWED | 266 | 280 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-003 | 百度 | COLLECTED_UNREVIEWED | 159 | 160 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-004 | 腾讯 | COLLECTED_UNREVIEWED | 909 | 917 | 12 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-005 | 美团 | COLLECTED_UNREVIEWED | 196 | 197 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-006 | 网易 | COLLECTED_UNREVIEWED | 2706 | 2876 | 90 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-007 | 哔哩哔哩 | COLLECTED_UNREVIEWED | 89 | 91 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-008 | 滴滴 | OK | 107 | 107 | 2 | 完整扫描，可判断消失 |
| official-009 | 拼多多 | COLLECTED_UNREVIEWED | 34 | 37 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-010 | 华为 | INCOMPLETE | 102 | 102 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-011 | 小红书 | COLLECTED_UNREVIEWED | 54 | 55 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-012 | 字节跳动 | INCOMPLETE | 8 | 18 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-013 | 阿里巴巴 | COLLECTED_UNREVIEWED | 457 | 471 | 3 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-014 | 蚂蚁集团 | COLLECTED_UNREVIEWED | 459 | 473 | 21 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-015 | 京东 | COLLECTED_UNREVIEWED | 245 | 245 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-016 | OPPO | COLLECTED_UNREVIEWED | 243 | 244 | 2 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-017 | vivo | COLLECTED_UNREVIEWED | 36 | 165 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-018 | 金山办公/WPS | OK | 49 | 49 | 0 | 完整扫描，可判断消失 |
| official-019 | 荣耀 | COLLECTED_UNREVIEWED | 15 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-020 | 科大讯飞 | COLLECTED_UNREVIEWED | 885 | 900 | 5 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-021 | 携程 | COLLECTED_UNREVIEWED | 10 | 70 | 10 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-022 | 360 | COLLECTED_UNREVIEWED | 101 | 109 | 2 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-023 | 得物 | INCOMPLETE | 11 | 174 | 11 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-024 | DeepSeek | OK | 36 | 36 | 3 | 完整扫描，可判断消失 |
| official-025 | 月之暗面/Kimi | OK | 96 | 96 | 3 | 完整扫描，可判断消失 |
| official-026 | MiniMax | OK | 31 | 31 | 0 | 完整扫描，可判断消失 |
| official-027 | 智谱/Z.ai | OK | 26 | 26 | 4 | 完整扫描，可判断消失 |
| official-028 | 阶跃星辰 | OK | 130 | 130 | 1 | 完整扫描，可判断消失 |
| official-029 | 百川智能 | INCOMPLETE | 1 | 7 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-030 | 零一万物/01.AI | OK | 51 | 51 | 1 | 完整扫描，可判断消失 |
| official-031 | 商汤科技 | OK | 143 | 143 | 7 | 完整扫描，可判断消失 |
| official-032 | 生数科技 | OK | 0 | 0 | 0 | 完整扫描，可判断消失 |
| official-033 | 硅基流动 | OK | 25 | 25 | 1 | 完整扫描，可判断消失 |
| official-034 | 面壁智能 | INCOMPLETE | 5 | 69 | 5 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-035 | Manus | OK | 21 | 21 | 1 | 完整扫描，可判断消失 |
| official-036 | 无问芯穹/Infini-AI | INCOMPLETE | 16 | 18 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-037 | 昆仑万维/天工 | INCOMPLETE | 66 | 66 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-038 | Shopee | OK | 50 | 50 | 0 | 完整扫描，可判断消失 |
| official-039 | 联想 | COLLECTED_UNREVIEWED | 86 | 87 | 10 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-040 | 蔚来 | OK | 875 | 875 | 14 | 完整扫描，可判断消失 |
| official-041 | 顺丰 | COLLECTED_UNREVIEWED | 150 | 150 | 2 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-042 | 米哈游 | COLLECTED_UNREVIEWED | 271 | 277 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-043 | 大疆 DJI | OK | 142 | 142 | 0 | 完整扫描，可判断消失 |
| official-044 | 度小满 | OK | 35 | 35 | 0 | 完整扫描，可判断消失 |
| official-045 | 海康威视 | COLLECTED_UNREVIEWED | 11 | 11 | 2 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-046 | 中兴通讯 | INCOMPLETE | 2 | 39 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-047 | 深信服 | INCOMPLETE | 10 | 11 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-048 | 金蝶 | OK | 219 | 219 | 10 | 完整扫描，可判断消失 |
| official-049 | 用友 | INCOMPLETE | 8 | 14 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-050 | 美图 | COLLECTED_UNREVIEWED | 8 | 13 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-051 | SHEIN | INCOMPLETE | 10 | 22 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-052 | 安克创新 | OK | 494 | 494 | 8 | 完整扫描，可判断消失 |
| official-053 | 大华股份 | INCOMPLETE | 2 | 2 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-054 | 吉利控股 | TIMEOUT | 224 | 389 | 114 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-055 | 小鹏集团 | INCOMPLETE | 15 | 628 | 15 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-056 | 理想汽车 | INCOMPLETE | 592 | 609 | 7 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-057 | 海尔集团 | INCOMPLETE | 114 | 125 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-058 | 美的集团 | COLLECTED_UNREVIEWED | 169 | 169 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-059 | 比亚迪 | COLLECTED_UNREVIEWED | 1497 | 1555 | 11 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-060 | 同花顺 | INCOMPLETE | 116 | 126 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-061 | 麒麟软件 | COLLECTED_UNREVIEWED | 96 | 96 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-062 | 普渡机器人 | COLLECTED_UNREVIEWED | 281 | 282 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-063 | 广联达 | OK | 32 | 32 | 2 | 完整扫描，可判断消失 |
| official-064 | 挚文集团/陌陌 | INCOMPLETE | 1 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-065 | BOSS直聘/看准科技 | INCOMPLETE | 3 | 3 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-066 | 作业帮 | OK | 46 | 46 | 1 | 完整扫描，可判断消失 |
| official-067 | 影石 Insta360 | OK | 355 | 355 | 7 | 完整扫描，可判断消失 |
| official-068 | 神州数码/神州信息 | COLLECTED_UNREVIEWED | 435 | 435 | 3 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-069 | 合合信息 | COLLECTED_UNREVIEWED | 87 | 90 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |

待审原始内容见 ../01-data/automation/review-queue.json；扫描基线见 ../01-data/automation/scan-state.json。
首次为某来源建立基线时不会把已有职位批量标记成新增。只有后续身份新增、指纹变化，或一次被确认完整的扫描中身份消失，才生成事件。
