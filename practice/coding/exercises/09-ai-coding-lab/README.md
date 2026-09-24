# 分页修复练习｜从失败测试到最小修改

[← 第 09 章](../../docs/09-ai-coding.md) · [Coding 首页](../../README.md)

本目录是无第三方依赖的 Python 工程练习。`pagination.py` 提供初始实现，`test_pagination.py` 提供验收测试。

> ⚠️ 初始实现故意有缺陷，测试失败是练习起点。不要把这份缺陷实现当作产品代码使用。

## 任务契约

实现 `paginate(items, page=1, page_size=2)`，遵守以下约定：

- `items` 是列表。
- `page` 是从 1 开始的页码，必须为正整数。
- `page_size` 是每页数量，只允许 1～5 的整数。
- 非法参数抛出 `ValueError`。布尔值、浮点数、字符串和 `None` 都不算合法整数参数。
- 返回对应页面的新列表，不修改原列表。空数据或超过末页时返回 `[]`。

> ⚠️ 只要求创建新的外层列表，不要求递归深拷贝里面的对象。

对于 `items = [10, 20, 30]`：

| 调用方式 | 预期结果 |
|---|---|
| 默认调用 | [10, 20] |
| `page=2` | [30] |
| `page=3` | [] |
| `page_size=0` | 抛出 ValueError |

## 实践流程

1. 在此目录运行 `python -m unittest discover -v`，记录失败测试和信息。
2. 沿具体输入阅读实现，说明偏离要求的第一步。
3. 按契约修复，重跑测试，检查实际代码差异。
4. 使用 AI 时，先要求调查与解释，再按已确定的任务修改。

> ⚠️ 保留原测试。删除断言或吞掉异常，不是修复正确性的证据。

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

1. 先拒绝非法类型和范围，避免错误参数进入偏移运算。
2. 页码从 1 开始，因此跳过的项目数是 `(page - 1) * page_size`。
3. 切片返回新的外层列表。起点达到或超过结尾时，返回 `[]`。

> ⚠️ 新外层列表不等于深拷贝，内部对象仍可能共享引用。

</details>
