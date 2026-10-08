# 面经保全与引用核验

[← 面经业务](../README.md)

只用 Python 标准库，离线运行。默认只读，不联网、不分类、不生成语义归一/频率文件，不改根目录 interview。

在仓库根目录执行：

```sh
python3 market/interview-experience/04-scripts/verify_interview_data.py --check
python3 -m unittest discover -s market/interview-experience/04-scripts -p 'test_*.py'
```

不加参数同样只读。查看稳定记录的原文与当前/原始位置：

```sh
python3 market/interview-experience/04-scripts/verify_interview_data.py --record S388:batch-38:L00298
```

获批新增材料后，更新 raw、source-provenance.json 和 corpus-contract.json。契约列出 source_ids、raw_sha256、source_section_sha256；若新增原始无编号记录，另更新 unnumbered_record_ids。保留旧区块原文与 original_line_start/end，填写真实当前位置。再显式刷新两个结构文件：

```sh
python3 market/interview-experience/04-scripts/verify_interview_data.py --write-index
python3 market/interview-experience/04-scripts/verify_interview_data.py --check
```

--write-index 只写 sources.json 与 raw-manifest.json，不修改契约、原文、复核断言或模型标签。校验器不内置来源总数；后续增加批次或流程不需要修改 Python。

测试仅覆盖保全、结构 ID、链接、计数与复核引用。可选模型复核格式见 [分析入口](../02-analysis/README.md)；只有实际提供的 reviewed 标签参与计数。
