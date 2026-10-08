# 面经策略与配置

[← 面经业务](../README.md)

- [来源质量准入](source-quality-policy.md)：HUMAN-A 与可核验一手证据
- [岗位范围准入](role-scope-policy.md)：AI 应用 / Agent 岗位范围
- [规范化与频率口径](normalization-policy.md)：排除、题族、去重和统计
- [语料契约](corpus-contract.json)：获批来源 ID 与不可变批次校验值
- [题族规则](question-families.json)：可审阅的语义概念与问法归组规则
- [规则正例回归样本](matching-fixtures.json)：每条规则至少一个正例，测试控制样本不进入数据或频率
- [记录复核决定](record-decisions.json)：明确理由和来源定位

新采集仍需通过准入及全历史流程去重，保留完整问法、日期缺失与不确定性。增加新批次后应显式更新语料契约并重建，不回到旧 235 / 279 冻结口径。
