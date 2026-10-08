# 面经数据

[← 面经业务](../README.md) · [当前分析](../02-analysis/README.md)

## 原始材料

raw/batch-01.md 至 raw/batch-38.md 保存该批次完整的正式一手来源区块，以及原有采集日期等必要元数据。[当前文件清单](raw-manifest.json)记录文件 SHA-256；[来源区块保全凭证](source-provenance.json)逐项记录 399 个流程与 S288 扩展共 400 个区块的原始位置、当前位置及逐字节摘要。

迁移只清理区块外的研究观察、冻结分析和课程计划。真实采集、排除和去重事实转入[批次采集记录](../05-logs/batch-collection-records.md)。正式来源区块内部的所有文字、题序、追问、作者回答、日期不确定性与排除边界原样保留。原始完整批次另有迁移前核验快照用于逐区块对照，没有以旧统计驱动新分析。

[语料契约](../03-strategy/corpus-contract.json)同时校验当前文件与原始来源区块摘要。区块外的采集日志不参与问题提取，批次观察不会错误归给最后一名候选人。

## 结构化接口

- [sources.json](sources.json)：sources 数组；每个 source_id 是一个独立流程。原始标题、公司、岗位、轮次、日期文本、URL、元数据行与完整 source section text 均保留
- [question-occurrences.json](question-occurrences.json)：occurrences 数组；一条是一个实际存档记录，未拆分复合问法。保留原列表标记、原文本、缩进续文、小节、文件行号、顺序、显式追问标签和分类理由。续文中的明确原追问用 follow_up_texts 索引，保留行号；原文边界/作者解释不当作追问。题族证据可来自主问或明确追问，不拆增原始记录数
- [normalized-questions.json](normalized-questions.json)：保守字面规范化组。只做 Unicode/空白处理与编辑序号剥离，保留代码运算符、大小写和题面语义
- [question-families.json](question-families.json)：细粒度问题族及其实际来源集合。语义关系由公开规则定义；不是把所有同域问题合为一道题

occurrence_id 由 source_id、批次和迁移前原文件行组成，保持来源记录身份；line_start / line_end 指向当前文件，original_line_start / original_line_end 指向保全凭证中的原位置。normalized question ID 由保守字面键的 SHA-256 前缀产生。来源顺序以完整存档顺序为准，轮次以原小节为准；相邻记录不自动推断为因果追问。

S391 原稿使用无编号项目符号，这 21 条原始记录正常进入分类；S387 未披露的 2–10、1–24、1–9 等范围各保留一条占位，不按范围生成新题。
