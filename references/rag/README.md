# RAG｜按问题查技术依据

[← References](../README.md) · [RAG 正文](../../curriculum/08-rag/README.md)

这份索引帮助核对机制、实现边界与版本，不用于计算面试频率。正文将资料放在需要支持的结论附近；下表用于按问题回查。官方事实与教材推导要分开：虚构政策、候选排名、预算和费用是教学假设，不是论文实验或生产测量。

## 通用机制与具体实现

| 要核对的问题 | 第一手资料 | 使用范围 |
|---|---|---|
| 检索材料如何与生成结合 | [RAG 原始论文](https://arxiv.org/abs/2005.11401) | 概念来源；应用主线不要求复现论文联合训练 |
| 假设文档为什么只能作线索 | [HyDE 原始论文](https://arxiv.org/abs/2212.10496) | 生成假设文档可能含虚假细节，实际证据应来自检索材料 |
| PDF 为何存在阅读顺序问题 | [PyMuPDF 文本抽取](https://pymupdf.readthedocs.io/en/latest/recipes-text.html) | 文字层、块位置和顺序整理；不代表所有文档都能准确恢复 |
| 哪些页面需要 OCR | [PyMuPDF OCR](https://pymupdf.readthedocs.io/en/latest/recipes-ocr.html) | 按页面需要选择、复用识别结果；依赖具体环境与配置 |
| 多格式统一表示应保留什么 | [Docling 文档模型](https://docling-project.github.io/docling/concepts/docling_document/) | 文本、表格、图片、层次和来源表示；不是解析质量保证 |
| 字符切分与 Token 切分如何区分 | [LangChain 递归字符切分说明](https://docs.langchain.com/oss/python/integrations/splitters/recursive_text_splitter) | 长度函数、分隔符与目标重叠；不将一个库的默认当通用定义 |
| BM25 如何处理 IDF、词频和长度 | [Lucene 10.3.1 BM25Similarity](https://lucene.apache.org/core/10_3_1/core/org/apache/lucene/search/similarities/BM25Similarity.html) | 固定实现的参数参照；第 07 章复算通用公式，不等同实际 Lucene 分数 API |
| RRF 的排名贡献与实现参数 | [Elasticsearch RRF](https://www.elastic.co/docs/reference/elasticsearch/rest-apis/reciprocal-rank-fusion) | 公式与该产品参数；教学常数 60 不构成最优性证明 |
| 两阶段检索为何需要重排 | [Sentence Transformers Retrieve & Re-Rank](https://sbert.net/examples/sentence_transformer/applications/retrieve_rerank/README.html) | 双编码召回与交叉编码精排的分工；示例候选数不是标准配置 |
| 排名评测的理想排序与折扣 | [Stanford IR：排序结果评测](https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-ranked-retrieval-results-1.html) | 指标解释与 NDCG；实际分母、无答案口径要另外声明 |
| LLM Judge 有哪些偏差 | [MT-Bench / Chatbot Arena 研究](https://arxiv.org/abs/2306.05685) | 判断器偏差与校准动机；不把单一研究结论当所有任务保证 |
| 文档中的指令为何不可信 | [OWASP 提示注入防护](https://cheatsheetseries.owasp.org/cheatsheets/LLM_Prompt_Injection_Prevention_Cheat_Sheet.html) | 多层防御、工具与数据边界；提示分隔不能代替授权 |
| 索引切换的原子性到哪里为止 | [Elasticsearch aliases](https://www.elastic.co/docs/manage-data/data-store/aliases) | 单服务别名操作；不能推出跨数据库、正文、缓存的全局原子性 |
| 实体中心查询怎样组织上下文 | [Microsoft GraphRAG Local Search](https://microsoft.github.io/graphrag/query/local_search/) | 相关实体、图上下文与原始文本的组合 |
| 跨主题问题怎样汇总 | [Microsoft GraphRAG Global Search](https://microsoft.github.io/graphrag/query/global_search/) | 社区报告分批形成中间要点，再筛选汇总；不自动证明事件频率或来源完整 |
| Local、Global、DRIFT 的范围 | [查询概览](https://microsoft.github.io/graphrag/query/overview/) | 具体项目查询方式，与泛指图增强检索区分 |
| Retry-After 表示什么 | [RFC 9110](https://www.rfc-editor.org/rfc/rfc9110.html#name-retry-after) | 服务端等待提示；应用仍需结合总截止时间和幂等边界 |

## 课程与运行版本

核验日期：2026-09-27。RAG 没有统一的“最新协议版本”，本模块讲通用机制，不能用一个框架版本代表整条链路。选用具体产品时，分别记录服务端、客户端、模型、输入协议与数据处理配置。

| 对象 | 核验与采用口径 | 实际运行情况 |
|---|---|---|
| 通用 RAG 机制 | 区分来源、查询、候选、上下文、生成、更新与授权；不绑定 SDK | 仅运行确定性公式与状态实验 |
| Python 机制实验 | CPython 3.13+ 标准库；原课程记录了 [3.14.7 正式发布](https://www.python.org/downloads/release/python-3147/) | 本次精修实际使用 CPython 3.13.5；未运行其他 Python 版本 |
| Microsoft GraphRAG | 保留课程采用的 [3.2.0 发布参照](https://github.com/microsoft/graphrag/releases/tag/v3.2.0) | 未安装、未运行；查询机制按上表官方资料核对，不将参照版本称为所有部署的最新版本 |
| Lucene BM25 | 10.3.1 固定文档参考 | 未运行 Lucene / Elasticsearch；补充实验只是公式复算 |
| PyMuPDF、Docling、LangChain 等 | 官方资料解释能力与限制，没有构造未经运行的版本绑定 API | 未执行解析、OCR、模型推理或框架集成 |

正式部署需要固定依赖，并按相应版本验证默认值、截断、异常、并发、资源释放和持久状态。课程未运行的版本与服务不计为验证通过。

## 技术结论与业务选择

RRF、窗口、指标与状态转换可通过 [机制实验](../../curriculum/08-rag/examples/README.md)核对。来源优先级、支持检查项、风险门槛、预算与降级属于业务选择，不能写成官方默认。

第 09 章的条件表是线上检查策略，不是自动真值判断器；第 12 章的有序日志、暂停派发和控制记录是明确前提下的一种交接设计，不是 Elasticsearch 自动提供的跨系统协议。社区报告例子也不冒充 Microsoft GraphRAG 的实测结果。

原正式面经回读范围见 [课程修订记录](../../guide/project/rag-reader-revision.md)；本次讲解、实验与显示检查范围见 [精修验收](../../guide/audits/rag-clarity-refinement-2026-09-27.md)。历史记录不随当前精修改写。
