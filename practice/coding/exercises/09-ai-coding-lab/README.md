# 分页修复练习｜从失败测试到最小修改

[← 第 09 章](../../docs/09-ai-coding.md) · [Coding 首页](../../README.md)

本目录是无第三方依赖的 Python 工程练习。pagination.py 提供**故意有缺陷的初始实现**，test_pagination.py 提供验收测试。初始测试失败是预期状态，不能把该实现当作产品代码使用。

## 任务契约

实现 paginate(items, page=1, page_size=2)。items 是列表，page 必须为正整数，page_size 必须为 1～5 的整数；布尔值、浮点数、字符串和 None 不算合法整数参数。非法参数抛 ValueError。按从 1 开始的页码返回相应的新列表，超过末尾或空数据返回 []，不得修改原列表；不要求递归深拷贝内部对象。

例如 items=[10,20,30]，默认调用得到 [10,20]，page=2 得到 [30]，page=3 得到 []，page_size=0 抛 ValueError。

## 实践流程

在此目录执行 `python -m unittest discover -v`，保存原先失败的测试名和信息。读实现，说明失败原因，限定修改范围，再修复并重跑。保留测试，不用删除断言或吞异常的方式变绿。使用 AI 时先让它调查并解释，再让它按已确定计划修改，最后检查真实差异。

完成后说明第一页下标怎么计算、校验为什么放在切片之前、切片如何满足空结果和原输入不变，以及哪些边界仍未验证。

<details>
<summary>查看参考实现：先完成自己的修复再展开</summary>

<!-- solution:pagination -->
```python
def paginate(items, page=1, page_size=2):
    if type(page) is not int or page < 1:
        raise ValueError("page must be a positive integer")
    if type(page_size) is not int or not 1 <= page_size <= 5:
        raise ValueError("page_size must be an integer from 1 to 5")
    start = (page - 1) * page_size
    return items[start:start + page_size]
```

页码从 1 开始，列表下标从 0 开始。错误类型先被拒绝，后续比较与计算才有明确前提。切片返回新外层列表，越过结尾会得到空结果；这不等于深拷贝。

</details>
