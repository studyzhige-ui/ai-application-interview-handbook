# 面经原始数据

[← 面经业务](../README.md)

- [raw/](raw/)：完整正式来源与同流程扩展，逐字节保留
- [questions.json](questions.json)：模型归并的共同回答任务及边界；逐记录支持保存在[模型复核结果](../02-analysis/model-review.json)
- [sources.json](sources.json)：来源 ID、原始标题、区块位置、原始 URL 与结构记录数
- [source-provenance.json](source-provenance.json)：每个正式区块的原位置、当前位置及 SHA-256
- [raw-manifest.json](raw-manifest.json)：批次文件大小及 SHA-256
- [语料契约](../03-strategy/corpus-contract.json)：获批来源集合、文件/区块哈希及无编号记录位置

raw 是内容依据；索引不复制全文，不含自动语义标签。结构记录 ID 沿用“来源 ID:批次:L原始行号”，物理行号移动时仍可借助保全凭证追溯。编号范围只保留原行，不展开成多条问题；缩进续文保持原样，也不推断提问角色。

编号行按格式定位；原始无编号列表由契约显式列出位置，不靠关键词判断它是不是问题。索引里的记录数只反映这种结构口径。查看某条记录可用 [核验脚本](../04-scripts/README.md) 的 --record 参数。

当前审阅分支正式来源为 **S001–S405、S408–S421，共419个来源ID、45批**；此前五日增量见[Batch40](raw/batch-40.md)、[Batch41](raw/batch-41.md)、[Batch42](raw/batch-42.md)、[Batch43](raw/batch-43.md)、[Batch44](raw/batch-44.md)，本日S421平安银行真人一面及作者补问见[Batch45](raw/batch-45.md)。旧未发布S406/S407原件缺失，保留空号且不计正式来源；下一编号S422。403来源模型分析快照不变，未合并前不声称main已包含本日增量。
