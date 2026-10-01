# Learning Path｜从基础到 AI 应用的可选路线

[← Handbook](../README.md) · [课程目录](../curriculum/README.md) · [知识地图](knowledge-map.md) · [实践](../practice/README.md) · [Products](../products/README.md)

这是一份阅读建议。默认读者已有可用的代码环境；正文中的代码和计算用于解释概念，不以安装、搭建项目或提交作品作为继续阅读的条件。已经熟悉的知识可以按需回看。

## 一条连续的基础课程

[Python](../curriculum/01-python/README.md) → [FastAPI](../curriculum/02-fastapi/README.md) → [MySQL](../curriculum/03-mysql/README.md) → [Redis](../curriculum/04-redis/README.md) → [Backend](../curriculum/05-backend-engineering/README.md) → [LLM](../curriculum/06-llm-foundation/README.md) → [Vector DB](../curriculum/07-vector-db/README.md) → [RAG](../curriculum/08-rag/README.md) → [Agent](../curriculum/09-agent/README.md) → [System Design](../curriculum/10-system-design/README.md)

目录编号、模块目录中的章节顺序、上一章与下一章导航遵循同一条路线。每个模块先建立整体问题和关系，再逐步解释其中的概念、机制与边界。

- Python 建立数据、对象、函数和执行的语言基础；FastAPI 接着说明这些程序怎样接收请求、验证数据并交付响应
- MySQL 建立持久数据、事务与并发修改；Redis 建立缓存、短期状态和原子命令。Backend 再组合这些已知行为，解释幂等、消息、可靠任务和跨系统协作
- LLM 先解释 Token、模型计算、生成与 Embedding。Vector DB 接着解释怎样比较、索引和维护这些向量，避免为了读检索章节而先跳读后面的模型知识
- RAG 将资料、检索、证据与回答连起来；Agent 在此基础上解释判断、行动、观察和继续执行。System Design 最后从完整需求出发，连接容量、状态、可靠性、质量和成本

FastAPI 的数据库示例只先说明接口与外部存储的角色；事务和存储内部机制由后面的 MySQL、Redis 展开。某个例子需要的少量前置会在当地解释，不要求提前学完整个后续模块。

## 怎样使用正文与回顾

首次阅读可以沿正文顺序建立模型：为什么有这个问题，过程怎样发生，结果为什么成立，在哪些条件下会失效。遇到代码先看输入和输出，再沿状态变化理解每一步；是否亲自运行由需要决定。

章末小结帮助收束关系，面试表达帮助组织解释，易错点帮助区分相近概念，自测帮助发现遗漏。它们从不同角度巩固理解。模块 Review 用于整体回看，Interview 用于口述与追问，均可按需要使用，没有固定周数、分数或结业门槛。

市场与真人面经可以提示复习重点；高频标签说明出现频率，主责标签说明哪个模块负责完整解释，都不意味着低频知识可以省略。冻结的能力统计与来源范围由 [Interview](../interview/README.md)维护。

## Python 与 Coding 分别顺读

Python 课程完整解释语言本身；[Coding](../practice/coding/README.md)独立解释怎样把问题变成程序，按它自己的章节顺序阅读。两条线无需穿插到指定章数才能继续，也不互相承担缺失前置。

[实践入口](../practice/README.md)把 Python 高频基础操作、数据库基础操作与 Coding 分开。已有练习是理解遇到疑问时的辅助，不是基础课程的额外负担。Hot100 是 Coding 方法的延伸练习，Git 和多文件 AI Coding 是可选参考。

## 什么时候看产品源码

理解 Agent 等相关通用机制后，可按兴趣选择一个 [Products](../products/README.md) 模块，沿该产品的一次真实任务阅读：如何接收输入、执行、调用工具、处理权限、保存状态和交付结果。产品章负责解释自身实现，代码位置用于核对依据。

公共产品的研读依据记录在对应模块的固定提交与核验日期中；Claude Code 使用获授权的私人快照，并注明其来源和覆盖范围。源码会演进，理解时需区分该版本的具体做法与可以迁移的共同原理。

<!-- learning-inventory:start -->
## 章节与配套入口

按[学习顺序配置](learning-order.json)和实际正文同步，当前合计 175 篇。目录编号、正文顺序与前后导航保持一致；冻结统计不随导航改变。

[学习资源索引](navigation-index.md)列出每个模块的正文、回顾、面试和实验入口；分组与章节内顺序以各模块 README 为准。
<!-- learning-inventory:end -->
