# JD 自动采集状态

最近扫描：2026-10-12T08:40:17Z。登记入口 **69** 个，本次收到 **69** 个来源结果。

自动化只负责官方来源采集、身份/正文指纹比较和待审队列；不会凭关键词把岗位写入正式 JD 库，也不会因一次失败自动删除正式岗位。

本次新事件：新增 **92**、正文/字段变化 **1**、完整扫描中可能消失 **0**。
累计待审：**93**（高优先 36 / 中优先 10 / 低优先 47）。

| 来源 | 公司 | 状态 | 本次观察 | 基线身份 | 新事件 | 处理 |
| --- | --- | --- | ---: | ---: | ---: | --- |
| official-001 | 小米 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-002 | 快手 | COLLECTED_UNREVIEWED | 279 | 279 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-003 | 百度 | COLLECTED_UNREVIEWED | 159 | 159 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-004 | 腾讯 | COLLECTED_UNREVIEWED | 905 | 906 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-005 | 美团 | COLLECTED_UNREVIEWED | 196 | 196 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-006 | 网易 | COLLECTED_UNREVIEWED | 2696 | 2697 | 12 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-007 | 哔哩哔哩 | COLLECTED_UNREVIEWED | 90 | 90 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-008 | 滴滴 | OK | 117 | 117 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-009 | 拼多多 | COLLECTED_UNREVIEWED | 36 | 36 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-010 | 华为 | COLLECTED_UNREVIEWED | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-011 | 小红书 | COLLECTED_UNREVIEWED | 55 | 55 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-012 | 字节跳动 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-013 | 阿里巴巴 | COLLECTED_UNREVIEWED | 469 | 469 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-014 | 蚂蚁集团 | COLLECTED_UNREVIEWED | 459 | 459 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-015 | 京东 | COLLECTED_UNREVIEWED | 244 | 244 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-016 | OPPO | COLLECTED_UNREVIEWED | 237 | 237 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-017 | vivo | COLLECTED_UNREVIEWED | 164 | 164 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-018 | 金山办公/WPS | BLOCKED | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-019 | 荣耀 | COLLECTED_UNREVIEWED | 15 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-020 | 科大讯飞 | PARTIAL | 800 | 884 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-021 | 携程 | COLLECTED_UNREVIEWED | 10 | 10 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-022 | 360 | COLLECTED_UNREVIEWED | 102 | 102 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-023 | 得物 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-024 | DeepSeek | OK | 37 | 37 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-025 | 月之暗面/Kimi | OK | 94 | 94 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-026 | MiniMax | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-027 | 智谱/Z.ai | OK | 24 | 24 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-028 | 阶跃星辰 | OK | 128 | 128 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-029 | 百川智能 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-030 | 零一万物/01.AI | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-031 | 商汤科技 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-032 | 生数科技 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-033 | 硅基流动 | OK | 25 | 25 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-034 | 面壁智能 | INCOMPLETE | 65 | 65 | 60 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-035 | Manus | COLLECTED_UNREVIEWED | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-036 | 无问芯穹/Infini-AI | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-037 | 昆仑万维/天工 | INCOMPLETE | 16 | 26 | 10 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-038 | Shopee | OK | 49 | 49 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-039 | 联想 | COLLECTED_UNREVIEWED | 87 | 87 | 1 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-040 | 蔚来 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-041 | 顺丰 | COLLECTED_UNREVIEWED | 149 | 149 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-042 | 米哈游 | COLLECTED_UNREVIEWED | 263 | 263 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-043 | 大疆 DJI | OK | 140 | 140 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-044 | 度小满 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-045 | 海康威视 | COLLECTED_UNREVIEWED | 11 | 11 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-046 | 中兴通讯 | INCOMPLETE | 39 | 39 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-047 | 深信服 | INCOMPLETE | 11 | 11 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-048 | 金蝶 | OK | 231 | 231 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-049 | 用友 | INCOMPLETE | 12 | 12 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-050 | 美图 | COLLECTED_UNREVIEWED | 13 | 13 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-051 | SHEIN | INCOMPLETE | 20 | 20 | 10 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-052 | 安克创新 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-053 | 大华股份 | INCOMPLETE | 2 | 2 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-054 | 吉利控股 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-055 | 小鹏集团 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-056 | 理想汽车 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-057 | 海尔集团 | INCOMPLETE | 115 | 115 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-058 | 美的集团 | COLLECTED_UNREVIEWED | 169 | 169 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-059 | 比亚迪 | COLLECTED_UNREVIEWED | 1544 | 1544 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-060 | 同花顺 | INCOMPLETE | 126 | 126 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-061 | 麒麟软件 | COLLECTED_UNREVIEWED | 96 | 96 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-062 | 普渡机器人 | COLLECTED_UNREVIEWED | 280 | 280 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-063 | 广联达 | OK | 32 | 32 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-064 | 挚文集团/陌陌 | INCOMPLETE | 15 | 15 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-065 | BOSS直聘/看准科技 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-066 | 作业帮 | OK | 46 | 46 | 0 | 首次基线建立，不产生历史岗位新增事件 |
| official-067 | 影石 Insta360 | INCOMPLETE | 0 | 0 | 0 | 本次未取得可用岗位观察；等待后续成功扫描建立基线 |
| official-068 | 神州数码/神州信息 | COLLECTED_UNREVIEWED | 429 | 429 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |
| official-069 | 合合信息 | COLLECTED_UNREVIEWED | 89 | 89 | 0 | 非完整扫描；仅合并已观察新增/变化，不判断消失 |

待审原始内容见 ../01-data/automation/review-queue.json；扫描基线见 ../01-data/automation/scan-state.json。
首次为某来源建立基线时不会把已有职位批量标记成新增。只有后续身份新增、指纹变化，或一次被确认完整的扫描中身份消失，才生成事件。
