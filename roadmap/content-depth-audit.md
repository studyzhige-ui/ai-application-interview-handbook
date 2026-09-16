# Curriculum Content Depth Audit｜正文深度最终口径

> **2026-09-16更新：** Agent为16章分层增强版，全仓库177篇正文；本轮已完成机制迁移、通用推导示例、细粒度训练与结构验证，范围和限制见文末。旧全仓库终审仍是历史记录。


[← Handbook 总目录](../README.md) · [Knowledge Map](knowledge-map.md) · [Granularity Audit](curriculum-granularity-audit.md)

> 当前十个一级模块共 **177 个正文知识块**。本文件统一记录完成状态；文件大小只用于发现异常，不作为质量结论。

## 验收标准

一个知识块应覆盖其主题所需要的大部分：

```text
为什么需要
→ 准确定义 / Mental Model
→ 机制 / 数据流 / 算法
→ Failure / Trade-off
→ Production / AI Application 场景
→ 模块边界
→ 面试表达 / 易错点 / 深挖
→ 折叠自测
```

窄主题可以较短；大型 Production 子系统如果只有概览则不能通过。

## 当前状态

| 模块 | Blocks | Numbering | Quality Status |
|---|---:|---|---|
| [Python Foundation](../python/README.md) | 13 | ✅ `01–13` | ✅ PASS |
| [FastAPI](../fastapi/README.md) | 16 | ✅ `01–16` | ✅ PASS |
| [AI Backend Engineering](../backend-engineering/README.md) | 22 | ✅ `01–22` | ✅ PASS |
| [MySQL](../mysql/README.md) | 23 | ✅ `01–23` | ✅ PASS |
| [Redis](../redis/README.md) | 24 | ✅ `01–24` | ✅ PASS |
| [Vector Database](../vector-db/README.md) | 16 | ✅ `01–16` | ✅ PASS |
| [LLM Foundation（应用工程深度）](../llm-foundation/README.md) | 14 | ✅ `01–14` | ✅ PASS |
| [RAG](../rag/README.md) | 14 | ✅ `01–14` | ✅ PASS |
| [Agent](../agent/README.md) | 16 | ✅ `01–16` | 分层增强与机制/训练迁移复核完成；范围见文末 |
| [System Design](../system-design/README.md) | 19 | ✅ `01–19` | ✅ PASS |

**当前正文总量：177 blocks。**

## 验收历史说明

- Python：保留 v1 主干后做 Canonical Coverage / Depth Remediation；
- FastAPI / AIBE / System Design：首版即按当前粒度和深度标准建设；
- Redis / Vector DB / LLM / RAG：完成旧结构颗粒度整改后重新做深度复核；
- MySQL：原 23-block 结构本身健康，机制与 correctness 边界审阅通过；
- Agent 历史版本：47→23 时完成旧短稿深写与证据验收；当前16章分层重构的检查范围见顶部更新说明。

## 后续规则

```text
先定认知闭环 → 写正文 → QA 找异常 → 人工复核 → 再标记完成
```

自动检查只负责发现异常，不能代替人工判断。


## 2026-09-16｜Agent 分层增强：吸收 main 的机制与训练优势

对照来源：main `0266cbfa131ff4157cad9f4c18b75fe153c0b846`；增强前分支 `2fbd42e65940b961e6c2edb17bc87940feb028ff`。保留任务→四层→治理16章主线，不恢复旧23章目录或另一套架构课程。

| main旧章 | 当前主责 | 处理结果 |
|---|---|---|
| 01–02 | 01–04 | 契约/控制权推导、Model与Harness边界；不恢复另一套八平面总纲 |
| 03 | 04、07 | Loop/事件/状态保留；纠正通用Run/Turn树，替换为可运行教学Loop |
| 04–05 | 10 | Contract、schema/语义、Registry/曝光、发现/版本与源码对照 |
| 06–07 | 11 | 结果投影、错误、并发/取消、迟到回执与具体实现线索 |
| 08 | 04 | Planning、ReAct、停止、预算、Steering全部沿控制循环组织 |
| 09–10 | 05 | 组装/预算/外部化/压缩/正确性；补回源码阶段、澄清缓存类型 |
| 11 | 06 | Memory生命周期、纠错、来源与索引失效 |
| 12–13 | 07、13 | 状态、检查点、恢复、操作核对、Fork与环境引用 |
| 14–15 | 13–14 | 执行隔离、审批绑定、注入/凭证/外传与威胁边界 |
| 16 | 12 | MCP/Skill/Hook、目录/版本与渐进加载；安全门不可仅靠可选Hook |
| 17 | 03、09 | 意图路由与模型能力策略/供应商适配分开 |
| 18 | 08 | 交接、预算、取消、A2A、共享工作区与证据汇聚 |
| 19–20 | 15 | Trace、三种Replay、评分、回归与持续改进；补具体测试矩阵 |
| 21 | 12、13、16 | 资源搜索、工作区/patch、测试/diff/交付验证 |
| 22–23 | 16 | Gateway/持久层职责、部署/成本、框架选型/迁移与实现对照 |

人工复核与修改依据：对23章旧正文和16章新正文做分节/段落保留候选扫描，再审阅差异；扫描只帮助定位，不把文本命中率当作语义覆盖率。核心机制已保留的段落不重复搬运；重点补回实现对照、最小循环与具体练习。前两章新增通用任务的完整推导；每章增加有边界的阅读提示与情景自测；16章长文按章节内部责任分段，而不是继续拆文件。

**不照搬的内容：** 旧八平面不作为第二套架构；旧Session→Run→Turn树不当通用标准；旧示意代码不作为可运行证明，本轮另提供经执行验证的教学Loop；Tool Execution不是天然跨系统事务；Prompt Cache不等于缓存最终回答。教学补充和既有固定源码阅读记录分别标明；不声称本轮重新遍历全部产品源码。

**训练迁移：** 旧main高频练习56/56保留能力范围并配具体追问与掌握标准，新增8道教学推导题，共64题；旧易错辨析实际86条（不是此前聊天里的90条）整合到同一面试入口；速查按新主线重组。44个ACTIVE Canonical映射保持一致；自拟追问不冒充Verified Follow-up Chains。

**实际检查：** 16章连续、177篇全仓库正文计数；每章阅读提示和至少4个折叠自测；56个旧练习标识完整、64题和86辨析计数；旧目录/平行架构课程不存在；相对文件链接与Agent显式锚点；研究问题、面经、统计与固定源码索引本轮逐文件摘要不变。第04章唯一标记的纯Python教学Loop实际执行5个断言场景通过（正常、越界、未读引用、预算、未知决策）。

**范围限制：** 这是一轮教材结构/机制迁移、例子与训练质量复核，不等于177篇逐句事实重审，也不等于真实模型、外部工具、沙箱或多worker生产故障测试。其余代码明确作为骨架/伪代码，产品版本细节仍按引用快照与官方资料核验。
