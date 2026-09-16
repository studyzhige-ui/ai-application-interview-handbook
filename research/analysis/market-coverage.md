# Market Coverage — Company / Role / Round

更新日期：2026-09-11

> 本文件只统计冻结 `S001–S279` 的来源标题元数据。`Sxxx` 已在采集层把同一候选人同一公司同一招聘流程的多轮合并，因此公司 / 岗位的基本单位仍是独立招聘流程。Round tag 是一个流程是否包含该轮次，允许一条多轮流程同时命中多个 Round tag。

## 总覆盖

- 正式 HUMAN-A 来源：**279**
- 至少映射到 1 道 Canonical 的来源：**278**
- 未映射到 Canonical 的来源：**1**
- 规范化公司 / 组织标签：**71**
- 原始公司标题标签：**110**

## Company Group 覆盖

| Company Group | Source Flows |
|---|---:|
| 字节跳动 | 51 |
| 阿里巴巴 | 45 |
| 腾讯 | 25 |
| 快手 | 17 |
| 小红书 | 16 |
| 美团 | 15 |
| 百度 | 10 |
| 蚂蚁集团 | 8 |
| 京东 | 8 |
| OPPO | 5 |
| 拼多多 | 4 |
| 滴滴 | 4 |
| 哔哩哔哩 | 4 |
| Shopee | 4 |
| 深信服 | 2 |
| 携程 | 2 |
| 联想 | 2 |
| 同花顺 | 2 |
| 科大讯飞 | 2 |
| 要务科技 | 2 |
| 影石创新 | 1 |
| 唯品会 | 1 |
| 启云方 | 1 |
| 小鹏汽车 | 1 |
| 360 | 1 |
| 多益网络 | 1 |
| 超参 | 1 |
| 原力健康 | 1 |
| 名创优品 | 1 |
| 法本信息 | 1 |
| FOSHO | 1 |
| 机械星球（要务科技） | 1 |
| 中兴通讯 | 1 |
| 点点互动 | 1 |
| 平安 | 1 |
| MiniMax | 1 |
| 钉钉 | 1 |
| 懂车帝 | 1 |
| 成都晓多科技 | 1 |
| 商汤 SenseTime | 1 |
| 嘉为科技 | 1 |
| 米哈游 | 1 |
| 汇川技术 | 1 |
| 深圳 Tuitti / 视界之外 | 1 |
| 奇虎 360 | 1 |
| CVTE | 1 |
| 小米 | 1 |
| 第四范式 | 1 |
| Moka | 1 |
| 钉学科技 | 1 |
| 金山办公 | 1 |
| 曹操出行 | 1 |
| Insta360 | 1 |
| 大疆 | 1 |
| 大麦 | 1 |
| 广州某小厂 | 1 |
| 猎豹移动 | 1 |
| 亚信安全 | 1 |
| 上海某独角兽小厂 | 1 |
| 文远知行 | 1 |
| 九号公司 | 1 |
| 某小厂 | 1 |
| 元石科技 | 1 |
| 匿名游戏公司（1000–9999 人） | 1 |
| 某中型 AI 设备研发公司 | 1 |
| 华为 | 1 |
| 成都某中厂（网络安全 / 自研 Agent 产品） | 1 |
| 杭州某小厂 | 1 |
| 匿名 B 端小公司 | 1 |
| 北京 B 端 AI 小公司 | 1 |
| 佰聆数据 | 1 |

## Primary Role 覆盖

> Role Primary 是按来源标题做的确定性归一化；`role_raw` 永久保留在 `source-metadata.csv`，避免关键词归类覆盖原始岗位语义。

| Primary Role | Source Flows |
|---|---:|
| Agent Development | 131 |
| AI Application | 55 |
| AI Full-stack | 34 |
| AI Backend | 32 |
| Coding Agent / Agent Infra | 14 |
| LLM Application | 7 |
| Other AI Engineering | 5 |
| FDE / Applied AI | 1 |

## Role Tag 覆盖（非互斥）

| Role Tag | Source Flows |
|---|---:|
| Agent Development | 151 |
| AI Application | 72 |
| AI Full-stack | 34 |
| AI Backend | 33 |
| Coding Agent / Agent Infra | 14 |
| LLM Application | 11 |
| Other AI Engineering | 5 |
| FDE / Applied AI | 1 |
| RAG / Knowledge | 1 |

## Round / Stage 覆盖（非互斥）

| Round Tag | Source Flows containing tag |
|---|---:|
| R1 / 一面 | 218 |
| R2 / 二面 | 71 |
| Technical / 未编号技术面 | 14 |
| R3 / 三面 | 9 |
| HR | 6 |
| Unspecified | 4 |
| Leader / 主管 / 交叉 | 4 |
| AI Coding / Vibe Coding | 2 |

## Top Company × Module：出现过该模块问题的独立流程数

| Company | Python | FastAPI | AI Backend Engineering | MySQL | Redis | Vector DB | LLM Foundation（应用工程深度） | RAG | Agent | System Design |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 字节跳动 | 5 | 1 | 28 | 13 | 10 | 8 | 21 | 16 | 27 | 9 |
| 阿里巴巴 | 1 | 1 | 18 | 6 | 6 | 6 | 13 | 17 | 29 | 10 |
| 腾讯 | 0 | 0 | 15 | 6 | 6 | 3 | 8 | 12 | 11 | 4 |
| 快手 | 1 | 0 | 6 | 0 | 6 | 2 | 5 | 6 | 14 | 3 |
| 小红书 | 0 | 0 | 8 | 5 | 9 | 2 | 4 | 5 | 10 | 5 |
| 美团 | 1 | 0 | 6 | 4 | 5 | 2 | 6 | 5 | 8 | 4 |
| 百度 | 2 | 0 | 2 | 3 | 0 | 2 | 3 | 4 | 8 | 3 |
| 蚂蚁集团 | 0 | 0 | 3 | 1 | 3 | 0 | 1 | 4 | 6 | 2 |
| 京东 | 0 | 0 | 7 | 3 | 5 | 1 | 0 | 2 | 3 | 2 |
| OPPO | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 1 | 3 | 1 |
| 拼多多 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 4 | 0 |
| 滴滴 | 0 | 0 | 3 | 3 | 2 | 0 | 0 | 1 | 2 | 2 |
| 哔哩哔哩 | 1 | 0 | 0 | 0 | 1 | 0 | 1 | 0 | 3 | 1 |
| Shopee | 0 | 0 | 2 | 2 | 2 | 0 | 0 | 1 | 2 | 2 |
| 深信服 | 0 | 0 | 1 | 0 | 1 | 0 | 0 | 0 | 2 | 0 |

## Primary Role × Module：出现过该模块问题的独立流程数

| Role | Python | FastAPI | AI Backend Engineering | MySQL | Redis | Vector DB | LLM Foundation（应用工程深度） | RAG | Agent | System Design |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Agent Development | 7 | 1 | 49 | 19 | 30 | 11 | 42 | 44 | 88 | 37 |
| AI Application | 3 | 1 | 24 | 5 | 8 | 11 | 15 | 21 | 35 | 8 |
| AI Full-stack | 1 | 0 | 15 | 12 | 7 | 7 | 7 | 9 | 17 | 9 |
| AI Backend | 0 | 0 | 24 | 13 | 15 | 3 | 10 | 8 | 8 | 9 |
| Coding Agent / Agent Infra | 2 | 0 | 3 | 4 | 2 | 1 | 4 | 1 | 10 | 5 |
| LLM Application | 2 | 1 | 5 | 0 | 3 | 4 | 3 | 4 | 4 | 2 |
| Other AI Engineering | 0 | 0 | 5 | 2 | 4 | 0 | 1 | 1 | 3 | 1 |
| FDE / Applied AI | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

## 未映射来源

`S271`
