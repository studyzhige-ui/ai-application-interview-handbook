# 仓库维护工具

这里只保留跨仓库的只读检查。岗位采集与面试数据处理的业务代码在各自 market 业务的 04-scripts。

- [check_handbook.py](check_handbook.py)：检查目标目录、本地 Markdown 路径与锚点、阅读入口覆盖和未解决的合并标记。
- [test_handbook.py](test_handbook.py)：用小型独立样例验证链接解析、重复标题锚点及冲突识别。

运行：

```sh
python tools/check_handbook.py
python -m unittest discover -s tools -p 'test_*.py' -v
```

01-data/raw 下的一手快照保留原始历史引用，不作为当前导航页面检查；它们的完整性由各业务数据契约校验。其他正文与 README 仍全部接受链接检查。
