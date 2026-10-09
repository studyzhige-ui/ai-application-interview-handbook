# 模型整理与复核状态

[← 面经业务](../README.md) · [完整原始材料](../01-data/README.md)

当前状态：全量模型语义复核待完成。没有全量模型标签、语义归一题库或可信题频结论。

## 已有的有限断言

[prior-reviewed-assertions.json](prior-reviewed-assertions.json)完整保存原 record-decisions.json 的九条决定、理由及原文件哈希，并补齐稳定记录 ID、原文位置、引文和区块哈希。原作者身份未记录，不声称由人或某个模型审核。它们仅覆盖这九条记录。

原决定中的 suppressed_family_ids 只是退役规则的历史上下文，不再执行，也不生成新标签或频率。它们和全量模型复核进度分开计算。

## 后续模型复核

[model-review.json](model-review.json)当前为 pending，reviews 为空；不为未读材料批量填充猜测标签。[JSON Schema](model-review.schema.json)描述可选的逐记录复核格式。

模型实际读完原记录、续文及来源上下文后，可写入稳定 occurrence_id、可核验 reference、原文 quote、明确 label、reason、真实 model 标识和含时区的 reviewed_at。不确定时使用 needs_review，label 为 null；不能把歧义、占位或缺失题面补造成新问题。

校验器只验证字段、引用和计数，不替模型评价理由或真实性。reviewed 才贡献明确标签计数；同标签的来源数取 source_id 集合。计数仅描述已复核子集，不把未复核记录当作负例，也不外推市场比例。完整状态仅在当前所有结构记录都有 reviewed 记录时成立。

后续分析应保留多轮上下文、复合问法与真实不确定性；是否同义、怎样分组、什么值得准备，由有来源依据的模型整理决定。结果写回本目录，备考回答留在根目录 [interview](../../../interview/README.md)。
