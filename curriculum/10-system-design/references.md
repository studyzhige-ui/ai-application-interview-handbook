# System Design｜按问题查阅技术依据

[← 模块入口](README.md) · [综合回顾](review/README.md)

本页区分三类信息：协议与产品文档支持具体技术语义；正文负责解释过程、选择与推导；业务阈值、负载、价格和故障排列是明确标注的教学假设。真人面经用于确认被问到的条件，不证明技术答案正确。

## 问题索引

| 需要核对的问题 | 课程位置 | 官方依据 | 使用边界 |
|---|---|---|---|
| 从具体工作负载推导方案 | 01、03 | [Google SRE，Non-Abstract Large System Design](https://sre.google/workbook/non-abstract-design/) | 设计方法，不提供本课程虚构业务的真实容量数据。 |
| SLI、SLO、统计窗口与误差预算 | 02 | [Google SRE Workbook，Implementing SLOs](https://sre.google/workbook/implementing-slos/) | 先定义事件、分母和窗口；本课程数值目标为教学选择。 |
| HTTP 受理与幂等方法 | 04、05、08 | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html) | 202 不等于应用已实现可靠任务；方法幂等语义不保证每次响应相同。 |
| 缓存读取、更新与失效 | 06 | [Azure Architecture Center，Cache-Aside](https://learn.microsoft.com/en-us/azure/architecture/patterns/cache-aside) | 缓存与源状态不自动保持一致；具体回填竞态按正文时序推导。 |
| Bloom Filter 的误判边界 | 06、15 | [Redis，Bloom filter](https://redis.io/docs/latest/develop/data-types/probabilistic/bloom-filter/) | 概率筛选不替代精确去重、业务状态或权限判断。 |
| 本地修改与可靠通知 | 05、08 | [AWS Prescriptive Guidance，Transactional outbox](https://docs.aws.amazon.com/prescriptive-guidance/latest/cloud-design-patterns/transactional-outbox.html) | 同事务保存待发事件；派发仍可能重复，外部系统不自动加入本地事务。 |
| 业务操作身份与安全重试 | 08、13 | [AWS Builders’ Library，Making retries safe with idempotent APIs](https://aws.amazon.com/builders-library/making-retries-safe-with-idempotent-APIs/) | 区别同一次操作与新意图，不把参数相似当作同一操作的完整证明。 |
| 供应商幂等的保留和结果规则 | 08、16 | [Stripe API，Idempotent requests](https://docs.stripe.com/api/idempotent_requests) | 产品实例，不把一家供应商的窗口和错误复用规则写成通则。 |
| 发布确认与消费确认 | 09 | [RabbitMQ 4.3 文档，Consumer Acknowledgements and Publisher Confirms](https://www.rabbitmq.com/docs/confirms) | 两种确认对应不同边界；未在 RabbitMQ 上运行本课程实验。 |
| 过载与级联故障 | 03、09、10 | [Google SRE，Handling Overload / Addressing Cascading Failures](https://sre.google/sre-book/handling-overload/) | 配合[级联故障章节](https://sre.google/sre-book/addressing-cascading-failures/)理解重试放大和资源隔离。 |
| 每次访问的授权检查 | 11 | [OWASP Authorization Cheat Sheet](https://cheatsheetseries.owasp.org/cheatsheets/Authorization_Cheat_Sheet.html) | 认证与授权分开；工具、对象、任务恢复和缓存返回都要遵守业务访问规则。 |
| 观察服务与安全发布 | 12 | [Google SRE，Monitoring Distributed Systems](https://sre.google/sre-book/monitoring-distributed-systems/) | 配合[Canarying Releases](https://sre.google/workbook/canarying-releases/)；指标、灰度和质量门的阈值须按业务验证。 |
| Refresh Token 轮换与重复使用风险 | 13 | [RFC 9700，OAuth 2.0 Security Best Current Practice](https://www.rfc-editor.org/rfc/rfc9700.html) | 轮换可使旧令牌失效；刷新结果未知时不能假定旧令牌总能安全重试。 |
| SSE 断线后的事件身份 | 14 | [HTML Living Standard，Server-sent events](https://html.spec.whatwg.org/multipage/server-sent-events.html) | Last-Event-ID 支持发送恢复位置；服务端日志保留和补发协议仍需应用实现。 |
| 行式与列式的数据访问范围 | 15 | [Amazon Redshift，Columnar storage](https://docs.aws.amazon.com/redshift/latest/dg/c_columnar_storage_disk_mem_mgmnt.html) | 支持按列读取相关数据块的解释；三行教学表不是实测性能，覆盖索引等也会影响读取成本。 |
| 大对象分块上传与校验 | 15 | [Amazon S3，Multipart upload overview](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html) | 分块对象 ETag 不一定是完整对象的 MD5；上传完成也不等于后续处理成功。 |
| 流式结果与用量记录 | 16 | [OpenAI API，Chat resource reference](https://developers.openai.com/api/reference/resources/chat) | 该接口 include_usage 的最终统计块可能因断线缺失；不能把缺失记为零费用或套用到所有供应商。 |

## 目标资料与实际运行

协议依据使用 RFC 9110、RFC 9700；SSE 依据 HTML Living Standard。产品文档是核对时的在线资料，RabbitMQ 页面显示 4.3；其他未固定版本的在线指南不被描述成某一安装版本的实机保证。OpenAI API 仅用于说明一个流式用量边界，不要求读者采用它搭建整个系统。

课程机制实验目标为 Python 3.13 标准库；运行版本和日期以[审查记录](../../guide/audits/system-design-reader-first-2026-09-28.md)为准。没有安装、运行或联调 MySQL、Redis、RabbitMQ、S3、模型供应商和 OAuth 服务，不能据此宣布这些真实服务已验证。

需要学习底层实现时，回到 [Backend](../05-backend-engineering/README.md)、[MySQL](../03-mysql/README.md)、[Redis](../04-redis/README.md)、[Vector DB](../07-vector-db/README.md)、[RAG](../08-rag/README.md)与 [Agent](../09-agent/README.md)。跨模块链接指向主讲范围，不表示本模块已替它们完成全部审查。
