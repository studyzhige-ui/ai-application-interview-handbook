# JD 自动采集状态

最近扫描：2026-10-12T10:20:31Z。登记入口 **69** 个，本次收到 **69** 个来源结果。

自动化只负责官方来源采集、身份/正文指纹比较和待审队列；不会凭关键词把岗位写入正式 JD 库，也不会因一次失败自动删除正式岗位。

本次新事件：新增 **894**、正文/字段变化 **22**、完整扫描中可能消失 **72**。
累计待审：**2780**（高优先 397 / 中优先 311 / 低优先 2072）。

| 来源 | 公司 | 状态 | 本次观察 | 基线身份 | 新事件 | 处理 |
| --- | --- | --- | ---: | ---: | ---: | --- |
| official-001 | 小米 | OK | 782 | 782 | 825 | 完整扫描，可判断消失 |
| official-002 | 快手 | COLLECTED_UNREVIEWED | 279 | 279 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-003 | 百度 | COLLECTED_UNREVIEWED | 159 | 159 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-004 | 腾讯 | COLLECTED_UNREVIEWED | 905 | 906 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-005 | 美团 | COLLECTED_UNREVIEWED | 195 | 196 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-006 | 网易 | COLLECTED_UNREVIEWED | 2698 | 2701 | 3 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-007 | 哔哩哔哩 | COLLECTED_UNREVIEWED | 90 | 90 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-008 | 滴滴 | OK | 117 | 117 | 0 | 完整扫描，可判断消失 |
| official-009 | 拼多多 | COLLECTED_UNREVIEWED | 36 | 36 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-010 | 华为 | INCOMPLETE | 102 | 102 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-011 | 小红书 | COLLECTED_UNREVIEWED | 55 | 55 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-012 | 字节跳动 | INCOMPLETE | 8 | 8 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-013 | 阿里巴巴 | COLLECTED_UNREVIEWED | 469 | 469 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-014 | 蚂蚁集团 | COLLECTED_UNREVIEWED | 457 | 459 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-015 | 京东 | COLLECTED_UNREVIEWED | 244 | 244 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-016 | OPPO | COLLECTED_UNREVIEWED | 237 | 237 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-017 | vivo | COLLECTED_UNREVIEWED | 164 | 164 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-018 | 金山办公/WPS | OK | 46 | 46 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-019 | 荣耀 | COLLECTED_UNREVIEWED | 15 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-020 | 科大讯飞 | COLLECTED_UNREVIEWED | 884 | 884 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-021 | 携程 | COLLECTED_UNREVIEWED | 10 | 20 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-022 | 360 | COLLECTED_UNREVIEWED | 102 | 102 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-023 | 得物 | OK | 161 | 161 | 36 | 完整扫描，可判断消失 |
| official-024 | DeepSeek | OK | 37 | 37 | 0 | 完整扫描，可判断消失 |
| official-025 | 月之暗面/Kimi | OK | 94 | 94 | 0 | 完整扫描，可判断消失 |
| official-026 | MiniMax | OK | 100 | 100 | 106 | 完整扫描，可判断消失 |
| official-027 | 智谱/Z.ai | INCOMPLETE | 0 | 24 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-028 | 阶跃星辰 | OK | 129 | 129 | 1 | 完整扫描，可判断消失 |
| official-029 | 百川智能 | OK | 18 | 18 | 0 | 完整扫描，可判断消失 |
| official-030 | 零一万物/01.AI | OK | 51 | 51 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-031 | 商汤科技 | OK | 143 | 143 | 0 | 完整扫描，可判断消失 |
| official-032 | 生数科技 | OK | 0 | 0 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-033 | 硅基流动 | OK | 25 | 25 | 0 | 完整扫描，可判断消失 |
| official-034 | 面壁智能 | INCOMPLETE | 5 | 65 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-035 | Manus | OK | 20 | 20 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-036 | 无问芯穹/Infini-AI | INCOMPLETE | 17 | 17 | 2 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-037 | 昆仑万维/天工 | INCOMPLETE | 34 | 65 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-038 | Shopee | OK | 49 | 49 | 0 | 完整扫描，可判断消失 |
| official-039 | 联想 | COLLECTED_UNREVIEWED | 87 | 87 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-040 | 蔚来 | OK | 881 | 881 | 1 | 完整扫描，可判断消失 |
| official-041 | 顺丰 | COLLECTED_UNREVIEWED | 149 | 149 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-042 | 米哈游 | COLLECTED_UNREVIEWED | 267 | 267 | 4 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-043 | 大疆 DJI | INCOMPLETE | 0 | 140 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-044 | 度小满 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-045 | 海康威视 | COLLECTED_UNREVIEWED | 11 | 11 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-046 | 中兴通讯 | INCOMPLETE | 39 | 39 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-047 | 深信服 | INCOMPLETE | 10 | 11 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-048 | 金蝶 | INCOMPLETE | 0 | 231 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-049 | 用友 | INCOMPLETE | 6 | 12 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-050 | 美图 | PARTIAL | 13 | 13 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-051 | SHEIN | INCOMPLETE | 20 | 21 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-052 | 安克创新 | OK | 495 | 495 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-053 | 大华股份 | INCOMPLETE | 2 | 2 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-054 | 吉利控股 | TIMEOUT | 282 | 282 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-055 | 小鹏集团 | OK | 606 | 606 | 1 | 完整扫描，可判断消失 |
| official-056 | 理想汽车 | INCOMPLETE | 581 | 581 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-057 | 海尔集团 | INCOMPLETE | 115 | 115 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-058 | 美的集团 | COLLECTED_UNREVIEWED | 169 | 169 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-059 | 比亚迪 | COLLECTED_UNREVIEWED | 1544 | 1544 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-060 | 同花顺 | INCOMPLETE | 9 | 126 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-061 | 麒麟软件 | COLLECTED_UNREVIEWED | 96 | 96 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-062 | 普渡机器人 | COLLECTED_UNREVIEWED | 280 | 280 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-063 | 广联达 | OK | 32 | 32 | 1 | 完整扫描，可判断消失 |
| official-064 | 挚文集团/陌陌 | INCOMPLETE | 15 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-065 | BOSS直聘/看准科技 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-066 | 作业帮 | OK | 46 | 46 | 0 | 完整扫描，可判断消失 |
| official-067 | 影石 Insta360 | OK | 347 | 347 | 2 | 完整扫描，可判断消失 |
| official-068 | 神州数码/神州信息 | COLLECTED_UNREVIEWED | 429 | 429 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-069 | 合合信息 | COLLECTED_UNREVIEWED | 89 | 89 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |

待审原始内容见 ../01-data/automation/review-queue.json；扫描基线见 ../01-data/automation/scan-state.json。
首次为某来源建立基线时不会把已有职位批量标记成新增。只有后续身份新增、指纹变化，或一次被确认完整的扫描中身份消失，才生成事件。
