# 面经处理脚本

[← 面经业务](../README.md) · [统计口径](../03-strategy/normalization-policy.md)

使用 Python 标准库，无网络、无第三方依赖、无抓取行为。

```sh
python market/interview-experience/04-scripts/build_interview_analysis.py
python market/interview-experience/04-scripts/build_interview_analysis.py --check
python -m unittest discover -s market/interview-experience/04-scripts -p 'test_*.py'
```

重建正式来源、所有问法记录、字面去重、语义问题族、主题与域频率、排除登记和顺序追溯。--check 逐一比对全部派生文件并以非零状态报告陈旧结果，不写文件。

根目录面试成品中明确的 evidence 标记区由此脚本同步当前域内前五问题族及原始问法；标记之外的备考正文不会更改。没有标记的成品会显式报错，防止覆盖人工内容。

采集由现有独立采集任务继续执行，其日志保存在 05-logs；本脚本只处理已准入的正式材料，不自动扩大权限或重新采集。
