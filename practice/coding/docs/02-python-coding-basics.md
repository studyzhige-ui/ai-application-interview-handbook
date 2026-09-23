# 02｜数据类型与容器：先完整掌握一种数据，再组合解决问题

[← 上一章：程序基础](01-programming-fundamentals.md) · [Coding 首页](../README.md) · [下一章：基础练习 →](03-basic-exercises.md)

> 本章先按容器建立完整操作模型，再组合算法。每个独立代码块都准备自己的数据；代码后的注释说明结果或状态变化，不代表该行自动打印。前置知识是第 01 章的变量、循环、函数和断言。

## 1. 容器选择与操作的两个结果

`list` 保存可修改的顺序，`tuple` 保存固定位置的组合，`str` 保存文字，`dict` 保存键到值的映射，`set` 只保存不重复的成员。选择容器取决于数据关系，不是哪个名字更熟悉。

每个操作都要分别看：**原对象有没有变，表达式返回了什么**。例如 `len(nums)` 是函数调用，把对象传给函数；`nums.append(3)` 是方法调用，通过对象取得操作再调用。方法不一定修改对象，函数也不一定没有副作用，不能只靠有没有点号判断。

数值与布尔运算归第 01 章。这里的顺序是列表、元组、字符串、字典、集合，之后再学习跨容器组合。需要底层对象模型时可回到 [Python Foundation](../../../curriculum/01-python/README.md)，但本章练习所需的基础操作不依赖先去别处补课。

<a id="list"></a>
## 2. list：保留顺序，允许增删替换

### 2.1 创建、读取与查询

```python
nums = [10, 20, 30]
empty = []
print(len(nums))          # 3：元素数量
print(nums[0])            # 10：下标从 0 开始
print(nums[-1])           # 30：最后一个元素
print(20 in nums)         # True：查询值是否出现
print(nums.index(20))     # 1：第一次出现的下标
print(nums.count(20))     # 1：出现次数
print(bool(empty))        # False：空容器在条件中按假处理
print(bool([0]))          # True：非空容器为真，和其中的值是不是 0 无关
```

`in` 问有没有，`index` 问在哪里，`count` 问多少个。index 找不到会报 ValueError；单个下标越界会报 IndexError。布尔转换 `bool(data)` 显式显示条件判断会使用的真值。

### 2.2 切片：一段位置构成新列表

```python
nums = [10, 20, 30, 40]
print(nums[1:3])          # [20, 30]：包含左端，不包含右端
print(nums[:2])           # [10, 20]：省略起点
print(nums[2:])           # [30, 40]：省略终点
print(nums[::2])          # [10, 30]：步长为 2
print(nums[::-1])         # [40, 30, 20, 10]：反向构造新列表
print(nums[2:100])        # [30, 40]：切片截到边界，不同于单下标访问
print(nums[3:1])          # []：正步长不能向更小的终点走
```

通用形式是 `data[start:stop:step]`，步长不能为 0。切片可以得到空结果；原列表不变。索引与切片不是同一种边界行为。

### 2.3 新增与替换：一个元素还是多个元素

```python
nums = [10, 20, 30]
nums[1] = 99             # nums = [10, 99, 30]
returned = nums.append(40)  # nums = [10, 99, 30, 40]
print(returned)          # None：append 修改列表，不返回列表
nums.extend([50, 60])    # nums = [10, 99, 30, 40, 50, 60]
nums.insert(1, 15)       # nums = [10, 15, 99, 30, 40, 50, 60]
nums[1:3] = [7, 8]       # nums = [10, 7, 8, 30, 40, 50, 60]
print(nums)              # [10, 7, 8, 30, 40, 50, 60]
```

append 把参数整体放进去，extend 把来源里的各项逐个加入。普通连续切片赋值可以改变列表长度；带非单位步长的切片替换要求数量匹配。先用等长替换追踪位置，再处理长度变化。

```python
a = [1]
a.append([2, 3])         # a = [1, [2, 3]]，第二项本身是一个列表
b = [1]
b.extend([2, 3])         # b = [1, 2, 3]
print(a, b)              # [1, [2, 3]] [1, 2, 3]
print([1, 2] + [3])       # [1, 2, 3]：构造新列表
print([0] * 3)           # [0, 0, 0]：重复三次
```

### 2.4 删除、清空与返回被删除的值

```python
nums = [10, 20, 30, 20]
last = nums.pop()         # last = 20；nums = [10, 20, 30]
first = nums.pop(0)       # first = 10；nums = [20, 30]
nums.remove(20)           # nums = [30]：只删第一个匹配的值
nums.extend([40, 50])    # nums = [30, 40, 50]
del nums[1]             # nums = [30, 50]：del 是语句，不返回被删值
nums.clear()             # nums = []
print(last, first, nums) # 20 10 []
```

空列表 pop 或指定位置越界会报 IndexError；remove 找不到值会报 ValueError。需要取出被删值用 pop。遍历原列表时随意删除会改变后续位置，容易跳过元素；过滤任务优先构造新列表。

### 2.5 排序、反转与汇总

```python
nums = [3, 1, 2]
new_nums = sorted(nums)  # [1, 2, 3]；nums 不变
print(nums, new_nums)    # [3, 1, 2] [1, 2, 3]
returned = nums.sort()   # nums = [1, 2, 3]
print(returned)          # None，不是排序结果
nums.sort(reverse=True) # nums = [3, 2, 1]
nums.reverse()           # nums = [1, 2, 3]：只反转顺序，不按大小排序
print(list(reversed(nums)))  # [3, 2, 1]：反向遍历结果收集成新列表
print(sum(nums))         # 6
print(min(nums), max(nums))  # 1 3
```

`list(source)` 把可逐项读取的来源收集成列表。reversed 提供反向遍历，不修改原对象。sum([]) 为 0，未指定默认值的 min([])/max([]) 会报 ValueError。混合类型不一定可比较，不能默认整数与字符串可以直接排序。

排序的 key 参数接收函数，表示按每项的哪个特征排列，不是立刻调用该函数一次。

```python
nums = [-3, 1, -2]
print(sorted(nums, key=abs))  # [1, -2, -3]：按绝对值排序
assert nums == [-3, 1, -2]
```

sorted 和 list.sort 都支持 key、reverse；排序键相同的元素保持原相对顺序。具体成本在第 05 章讨论。

### 2.6 遍历、解包与 enumerate

```python
nums = [10, 20, 30]
for x in nums:
    print(x)             # 10、20、30，各一行；取得的是元素值
for i in range(len(nums)):
    print(i, nums[i])     # 0 10、1 20、2 30，各一行；i 是下标
```

需要两种信息时先学解包：把右侧多项按位置分别交给左侧多个变量。解包不只用于元组，也能用于列表等可迭代对象。

```python
i, x = [0, 10]          # i=0，x=10
print(i, x)              # 0 10
nums = [10, 20, 30]
for i, x in enumerate(nums):
    print(i, x)          # 0 10、1 20、2 30，各一行
```

enumerate 每次给一对“编号、元素值”，循环头再解包。默认编号从 0 开始，正好可作下标；`enumerate(nums, start=1)` 则是从 1 编号，不能直接拿编号访问同一位置。普通解包两边数量不匹配会报 ValueError。

### 2.7 推导式：压缩已经理解的循环

```python
nums = [1, 2, 3, 4]
result = []
for x in nums:
    if x % 2 == 0:
        result.append(x * x)
compact = [x * x for x in nums if x % 2 == 0]
assert result == compact == [4, 16]
```

读推导式时先执行 for 取得 x，再判断 if，最后计算开头的 x*x 放进新列表。不修改原列表。看不清时就使用普通循环，不以行数少作为质量目标。

### 2.8 复制、共享对象与二维列表

```python
nums = [1, 2]
alias = nums             # 两个名字指向同一对象
copied = nums.copy()    # 新的外层列表
alias.append(3)
print(nums, copied)      # [1, 2, 3] [1, 2]
print(alias is nums)     # True
print(copied is nums)    # False
```

copy、完整切片和 list(nums) 都是浅拷贝：只新建外层，内部对象仍可能共享。== 比内容，is 比对象身份。

```python
bad = [[0, 0]] * 2       # 两个位置引用同一行
bad[0][0] = 9
print(bad)               # [[9, 0], [9, 0]]
good = [[0, 0] for _ in range(2)]  # 每轮新建一行；_ 表示不用的循环变量
good[0][0] = 9
print(good)              # [[9, 0], [0, 0]]
print(good[0][1])        # 0：先取行，再取该行的一列
```

矩阵就是列表里再放列表。深层对象是否也应复制取决于任务，不把浅拷贝当成全层级独立保证。

**自测：** 原输入不变，得到降序列表，应该使用哪种操作？

<details><summary>查看参考答案</summary>

```python
nums = [3, 1, 2]
answer = sorted(nums, reverse=True)
assert answer == [3, 2, 1] and nums == [3, 1, 2]
```

不能把 nums.sort() 的 None 返回值当成排序结果。

</details>

<a id="tuple"></a>
## 3. tuple：固定位置的组合，不支持增删替换

### 3.1 创建、访问、查询与遍历

```python
point = (3, 5)
empty = ()
single = (3,)            # 单元素需要逗号；(3) 只是整数 3
print(type(single))     # <class 'tuple'>
print(len(point))       # 2
print(point[0], point[-1])  # 3 5
print(point[:1])         # (3,)
print(3 in point)        # True
print(point.count(3))    # 1
print(point.index(5))    # 1
for value in point:
    print(value)         # 3、5，各一行
```

索引、切片、len、in、count、index 的含义与列表一致，越界与找不到的边界也相同。但 tuple 没有 append/remove/sort，也不能写 point[0]=...。这些不是漏教的方法，而是该类型不支持的操作。

### 3.2 解包、转换与构造新值

元组也能比较或生成排序结果。按位置逐项比较，遇到第一个不同项就决定大小；元素本身仍需可比较。sorted 返回列表，不是原地排序元组。

```python
point = (3, 5)
print(point == (3, 5))          # True
print((1, 9) < (2, 0))         # True：先比较第一项
print((1, 3) < (1, 5))         # True：第一项相同，再比较第二项
print(sorted((3, 1, 2)))       # [1, 2, 3]
print(bool(()))                # False：空元组为假
```


```python
point = (3, 5)
row, col = point         # row=3，col=5：复用刚学过的解包
print(row, col)          # 3 5
print(point + (7,))      # (3, 5, 7)：新元组
print(point * 2)         # (3, 5, 3, 5)
mutable = list(point)   # [3, 5]：新的可修改容器
mutable[0] = 9
new_point = tuple(mutable)
print(point, new_point) # (3, 5) (9, 5)
```

多目标赋值先计算右侧全部旧值，再依次写到左侧，因此可以交换，而不需要手工先覆盖一个变量：

```python
a, b = 2, 5
a, b = b, a
print(a, b)                    # 5 2
nums = [10, 20]
nums[0], nums[1] = nums[1], nums[0]
assert nums == [20, 10]
```

不可变约束的是元组位置不能重新绑定，不代表内部每个对象不可变。`([1],2)` 中的列表仍能修改；元组能否作字典键，要看元素是否都可哈希。

```python
def bounds(nums):
    return min(nums), max(nums)  # 把两个结果打包为元组

low, high = bounds([3, 1, 5])   # 调用后解包
print(low, high)                # 1 5
```

**自测：** (3,) 与 (3) 有何不同？

<details><summary>查看参考答案</summary>

前者是单元素元组，后者是加括号的整数表达式。逗号才决定这里的打包；转换成 list 后修改的是新容器，不是把元组“解锁”。

</details>

<a id="str"></a>
## 4. str：文字序列，修改得到新字符串

### 4.1 创建、读取、切片与遍历

```python
text = "hello"
print(len(text))         # 5
print(text[0], text[-1]) # h o
print(text[1:4])         # ell
print(text[::-1])        # olleh
print("ell" in text)     # True：可查询子串
for ch in "hi":
    print(ch)            # h、i，各一行
print(list("hi"))        # ['h', 'i']
```

单个下标越界会报 IndexError；`text[0]="H"` 会报 TypeError。Python 字符串按 Unicode 码点处理，不等于字节数；某些屏幕上的字符可由多个码点组成。普通算法题以题目规定的字符集为准。

### 4.2 查找、计数和内容判断

```python
text = "banana"
print(text.find("na"))       # 2：第一次位置
print(text.find("x"))        # -1：没找到
print(text.index("na"))      # 2：找不到则报 ValueError
print(text.count("na"))      # 2：不重叠出现次数
print(text.startswith("ban")) # True
print(text.endswith("na"))   # True
print("abc".isalpha())        # True：字母
print("123".isdecimal())      # True：十进制数字字符
print("123".isdigit())        # True：数字字符，范围比 isdecimal 更宽
print("a1".isalnum())         # True：字母或数字
print(" \t".isspace())        # True：空白字符
```

这些内容判断对空字符串返回 False。isdigit 为真不保证 int 能转换，例如某些上标数字；带正负号的整数文字也不满足纯数字字符判断。输入解析应遵循明确格式，而不是靠方法名字猜。

### 4.3 去两端字符、替换与大小写

```python
text = "  Hello World  "
trimmed = text.strip()       # 'Hello World'
print(repr(text))            # '  Hello World  '：原对象不变
print(repr(trimmed))         # 'Hello World'
print(repr(text.lstrip()))   # 'Hello World  '
print(repr(text.rstrip()))   # '  Hello World'
print(trimmed.lower())       # hello world
print(trimmed.upper())       # HELLO WORLD
print(trimmed.replace("World", "Python"))  # Hello Python
print("banana".replace("a", "A", 1))       # bAnana：只替换一次
print("pre_name".removeprefix("pre_"))     # name
print("report.txt".removesuffix(".txt"))   # report
```

strip(chars) 的参数是一组可从两端反复去掉的字符，不是完整前后缀；精确前后缀使用 removeprefix/removesuffix。想让变量保留结果，需写 `text=text.strip()`。没有重新赋值，原变量仍关联原文字。

### 4.4 split 与 join：拆开后是什么，拼接要求什么

```python
text = "  10   20\t30  "
parts = text.split()
print(parts)                    # ['10', '20', '30']：合并连续空白、忽略两端空白
print("a,,b".split(","))         # ['a', '', 'b']：指定分隔符时可保留空段
print("a b c".split(" ", 1))    # ['a', 'b c']：最多拆一次
print("a\nb".splitlines())       # ['a', 'b']：按行拆分
print("-".join(["a", "b"]))      # a-b：分隔符放在相邻项之间
print("".join(["a", "b"]))       # ab：空分隔符
```

split 返回字符串列表，不会转换成整数。join 要求各项都是字符串，`" ".join([1,2])` 会报 TypeError。

```python
nums = [10, 20, 30]
parts = [str(x) for x in nums]   # ['10', '20', '30']
print(" ".join(parts))          # 10 20 30
chars = sorted("tea")           # ['a', 'e', 't']：sorted 已在列表部分讲过
key = "".join(chars)            # 'aet'
print(key)                       # aet
```

因此 `"".join(sorted(word))` 只是把后两步写到一行，并不是新语法。第一次组合时保留中间变量，更容易追踪类型与结果。

### 4.5 构造、比较与格式化

```python
print("Py" + "thon")             # Python：新字符串
print("ha" * 3)                  # hahaha
print("abc" == "abc")            # True
print("10" < "2")                # True：按字符顺序比较，不是数字大小
name = "Alice"
score = 3.14159
print(f"{name}: {score:.2f}")     # Alice: 3.14
print("{}: {:.2f}".format(name, score))  # Alice: 3.14
```

f 前缀允许在大括号中放表达式，`.2f` 指定显示两位小数，不改变 score 本身。大量拼接优先先收集片段再 join，避免反复复制越来越长的字符串。

### 4.6 bytes：文字编码后得到字节，不是另一种 str

文本进入文件、网络或二进制输入流时，需要编码。str 保存文字，bytes 保存 0～255 的字节值。编码 encode 将文字转字节，解码 decode 按同一种编码解释回文字。

```python
text = "你好"
data = text.encode("utf-8")
print(type(data))              # <class 'bytes'>
print(len(text), len(data))    # 2 6：文字长度与编码后字节数不同
print(data.decode("utf-8"))    # 你好
raw = b"10 20"                # ASCII 内容可以直接用 b 前缀
print(raw[0], raw[:2])         # 49 b'10'：单下标得到整数，切片仍是 bytes
print(raw.split())             # [b'10', b'20']
print(b"10" in raw)           # True
print(b"-".join(raw.split())) # b'10-20'
print(int(b"10"))             # 10：符合格式的字节可以转整数
```

bytes 不可变，不能给 raw[0] 赋值；拼接、替换等得到新对象，不能直接混合 str 与 bytes。二进制输入不保证全是合法 UTF-8，解码失败应检查实际编码与数据。第 04 章只在大量整数输入中使用 bytes，不展开本课程用不到的二进制协议。

**自测：** 把 `"  eat tea  "` 变为 `"eat-tea"`，且原字符串不变。

<details><summary>查看参考答案</summary>

```python
text = "  eat tea  "
answer = "-".join(text.split())
assert answer == "eat-tea" and text == "  eat tea  "
```

split 在这里已处理两端空白，无需为了形式完整再重复 strip。

</details>

<a id="dict"></a>
## 5. dict：每个键关联一个值

### 5.1 创建、查值与缺失处理

```python
score = {"Alice": 90, "Bob": 85}
empty = {}
print(len(score))                # 2：键值对数
print(score["Alice"])            # 90
print("Alice" in score)          # True：检查的是键，不是值
print(score.get("Bob", 0))       # 85
print(score.get("Carol", 0))     # 0：缺失的默认值
print(score.get("Carol"))        # None：未指定默认值
print("Carol" in score)          # False：get 不会新增键
```

直接读取缺失键会报 KeyError。缺失是正常情况可用 get；缺失代表违约时，不应随意默认成 0 掩盖问题。键必须可哈希：常用整数、字符串、元素都可哈希的元组可以，列表、字典、集合不可以直接作键；值没有这项要求。字典按插入顺序遍历，不会自动按键排序。

### 5.2 新增、覆盖和批量更新

```python
score = {"Alice": 90}
score["Bob"] = 85                  # 新增
score["Alice"] = 95                # 覆盖旧值，不新增第二个同名键
score.update({"Bob": 88, "Carol": 80})
print(score)                       # {'Alice': 95, 'Bob': 88, 'Carol': 80}
value = score.setdefault("Dan", 0) # 缺失才写入默认值，value=0
again = score.setdefault("Dan", 99)# 已有就返回已有值，again=0
print(value, again)                # 0 0
print(dict([("a", 1), ("b", 2)]))  # {'a': 1, 'b': 2}：从键值对序列创建
```

setdefault 与 get 都可提供默认值，但前者缺失时写入，后者不写。初学时也可以展开为 `if key not in d: d[key]=...`，不必追求压成一行。

### 5.3 keys、values、items 与遍历

```python
score = {"Alice": 90, "Bob": 85}
print(list(score.keys()))          # ['Alice', 'Bob']
print(list(score.values()))        # [90, 85]
print(list(score.items()))         # [('Alice', 90), ('Bob', 85)]
for name in score:
    print(name)                    # Alice、Bob，各一行
for value in score.values():
    print(value)                   # 90、85，各一行
for name, value in score.items():
    print(name, value)             # Alice 90、Bob 85，各一行
```

items 每轮给一个二元组，再由循环头解包。keys/values/items 返回的是视图，会反映之后的字典变化，不是普通列表；list 把当时各项收集成列表，便于展示或保留外层快照，不能直接写 `score.values()[0]`。

### 5.4 删除、清空、复制和排序展示

```python
score = {"Alice": 90, "Bob": 85}
saved = score.copy()               # 浅拷贝，内部可变值仍可能共享
removed = score.pop("Bob")         # 85；score = {'Alice': 90}
missing = score.pop("Nobody", -1)  # -1：缺失默认值
score["Carol"] = 80
pair = score.popitem()              # ('Carol', 80)：最后插入的一对
del score["Alice"]                 # score = {}
score.clear()                      # 清空；这里原本已为空
print(removed, missing, pair)      # 85 -1 ('Carol', 80)
print(saved)                       # {'Alice': 90, 'Bob': 85}
print(sorted(saved))               # ['Alice', 'Bob']：排序键，得到列表
```

无默认值的 pop、del 遇到缺失键会报 KeyError，空字典 popitem 也会报错。字典没有 sort 方法，需对它的键、值或键值对生成另一个排序序列。遍历时增删键可能报 RuntimeError，不能把修改遍历结构当作普通过滤。

```python
score = {"Alice": 90, "Bob": 85}
def by_score(pair):
    return pair[1]
print(sorted(score.items(), key=by_score))  # [('Bob', 85), ('Alice', 90)]
squares = {x: x * x for x in [1, 2, 3]}     # 字典推导式，每轮产生 key:value
print(squares)                              # {1: 1, 2: 4, 3: 9}
```

### 5.5 容器内的小应用：计数与位置

```python
text = "banana"
count = {}
for ch in text:
    old = count.get(ch, 0)         # 先取旧次数，缺失当 0
    count[ch] = old + 1            # 增加后写回
print(count)                       # {'b': 1, 'a': 3, 'n': 2}
```

`count[ch]=count.get(ch,0)+1` 与循环中的两行等价。右侧先得到旧次数，再加一，最后左侧赋值才写入。首次 b 是“默认 0 → 1 → 新增 b:1”，之后重复字符是覆盖旧次数。

```python
nums = [5, 8, 5]
position = {}
for i, x in enumerate(nums):
    position[x] = i
print(position)                    # {5: 2, 8: 1}：保存最后出现位置
```

需要首次位置时，要先检查键是否存在。键值含义来自任务，不能把“计次数”和“记下标”当成同一段模板。

**自测：** 读取缺失 b 时得到 0，但不得新增键，选 get 还是 setdefault？

<details><summary>查看参考答案</summary>

```python
d = {"a": 2}
value = d.get("b", 0)
assert value == 0 and d == {"a": 2}
```

setdefault 会在缺失时新增键，不符合要求。

</details>

<a id="set"></a>
## 6. set：只保存成员，不保存位置和重复次数

### 6.1 创建、成员查询与遍历

```python
seen = set()                       # 空集合；{} 是空字典
values = {3, 1, 3}                 # 只有成员 1、3
from_list = set([3, 1, 3, 2])
print(len(values))                 # 2
print(3 in values)                 # True
print(9 not in values)             # True
print(sorted(from_list))           # [1, 2, 3]：显示顺序来自 sorted
for x in sorted(values):
    print(x)                        # 1、3，各一行
```

set 不保证遍历顺序，没有下标、切片、index，也不能保存重复次数。成员必须可哈希，规则与字典键相同。去重之后无法据此还原重复次数，不能承诺保留首次出现顺序。

### 6.2 增删、清空与复制

```python
seen = {10}
seen.add(20)                       # 成员 10、20
seen.add(20)                       # 重复添加不变
seen.update([20, 30])              # 成员 10、20、30
seen.remove(10)                    # 成员 20、30；缺失会报 KeyError
seen.discard(999)                  # 缺失也不报错
copied = seen.copy()
removed = seen.pop()               # 删除并返回任意成员，不是最小值或第一个
assert removed in {20, 30} and len(seen) == 1
seen.clear()
print(sorted(copied), seen)        # [20, 30] set()
```

空集合 pop 会报 KeyError。测试集合应比较内容或排序后的列表，不能依赖某次偶然打印顺序。add 把参数当一个成员，update 逐个读取来源成员；成员不可哈希时仍会报错。

### 6.3 集合运算、包含关系与不可变集合

```python
a = {1, 2, 3}
b = {3, 4}
print(sorted(a | b))              # [1, 2, 3, 4]：并集，a.union(b)
print(sorted(a & b))              # [3]：交集，a.intersection(b)
print(sorted(a - b))              # [1, 2]：差集，a.difference(b)
print(sorted(a ^ b))              # [1, 2, 4]：对称差，a.symmetric_difference(b)
print({1, 2} <= a)                # True：子集，issubset
print(a >= {1})                   # True：超集，issuperset
print(a.isdisjoint({8, 9}))        # True：没有共同成员
print(a == {3, 2, 1})             # True：内容相同，与书写顺序无关
```

上面的四种运算都产生新集合；对应的 update、intersection_update、difference_update、symmetric_difference_update 修改原集合，返回 None。

```python
a = {1, 2, 3}
returned = a.intersection_update({2, 3, 4})
print(sorted(a), returned)         # [2, 3] None
squares = {x * x for x in [-2, 2, 3]}
print(sorted(squares))             # [4, 9]：集合推导式自动去重
fixed = frozenset({1, 2})           # 不可变集合，没有 add/remove
print(fixed == {1, 2})             # True
```

frozenset 本身可哈希，成员同样必须可哈希，可以作为字典键。这个例子解释“需要不可变成员集合”时怎样表达，不要求基础题强行使用。

### 6.4 容器内的小应用：有没有重复

```python
def has_duplicate(nums):
    seen = set()
    for x in nums:
        if x in seen:
            return True
        seen.add(x)
    return False

assert has_duplicate([3, 1, 3]) is True
assert has_duplicate([3, 1]) is False
assert has_duplicate([]) is False
```

seen 保存此前已经处理的成员，所以先查询再加入。反过来会把每个元素都当成重复。

**自测：** 为什么 `list(set([3,1,3,2]))` 不能保证得到 `[3,1,2]`？

<details><summary>查看参考答案</summary>

集合只表达成员，不表达首次出现顺序。需要一个 set 判重，再用一个 list 按读取顺序收集；完整练习见第 03 章。

</details>

## 7. 跨容器组合：新增的是任务，不是基础 API

### 7.1 zip 配对，循环头解包

```python
names = ["Alice", "Bob"]
scores = [90, 85]
pairs = list(zip(names, scores))
print(pairs)                       # [('Alice', 90), ('Bob', 85)]
for name, score in pairs:
    print(name, score)             # Alice 90、Bob 85，各一行
print(list(zip([1, 2], [3])))       # [(1, 3)]：默认到较短来源结束
```

zip 负责按位置配对，解包负责把一对分给两个名字。zip 自身是一次性迭代结果，需要复用时先收集成列表。任务要求两组等长时，先验证长度；支持的环境也可使用 strict=True 拒绝截断，不能默默丢数据。

### 7.2 函数接收列表：返回新结果与修改原对象

```python
def doubled(nums):
    return [x * 2 for x in nums]

def add_zero(nums):
    nums.append(0)

original = [1, 2]
assert doubled(original) == [2, 4] and original == [1, 2]
assert add_zero(original) is None
assert original == [1, 2, 0]
```

参数名也只是名字。通过它修改同一个列表，调用方会观察到变化；函数内部 `nums=[]` 则只是重新绑定局部名字，不会把调用方名字重新绑定。

可变默认参数在函数定义时创建，会被多次调用共享。需要每次新列表时使用 None 作标记：

```python
def collect(value, items=None):
    if items is None:
        items = []
    items.append(value)
    return items

assert collect(1) == [1]
assert collect(2) == [2]
```

## 8. 两数之和：从逐对尝试到保存历史位置

**练习契约：** 给整数列表与目标和，返回两个不同下标。存在时本例保证唯一答案；无解扩展约定返回 []。nums=[2,7,11,15]、target=9，结果为 [0,1]。

```python
def two_sum_brute(nums, target):
    for i in range(len(nums)):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return [i, j]
    return []

assert two_sum_brute([2, 7, 11, 15], 9) == [0, 1]
assert two_sum_brute([3, 3], 6) == [0, 1]
```

外层固定一个位置，内层只检查之后的位置。对于当前数字 x，真正需要的是 target-x 以前在哪个位置出现；字典正好保存这种关系。

```python
def two_sum(nums, target):
    seen = {}                      # 数字 → 已处理位置
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i                # 先查再记录，排除同位置复用
    return []

assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([3], 6) == []
```

| i | x | need | 查询前 seen | 动作 |
|---:|---:|---:|---|---|
| 0 | 2 | 7 | {} | 没找到，记录 2:0 |
| 1 | 7 | 2 | {2:0} | 找到，返回 [0,1] |

优化减少的是重复找补数的工作，不是看到数组就猜哈希模板。

## 9. 移动零：先返回新列表，再修改原列表

**任务：** nums=[0,1,0,3,12]，非零数字保持相对顺序，零放到后面，得到 [1,3,12,0,0]。先允许额外列表，不声称这是满足原题空间要求的最优解。

```python
def move_zeroes_copy(nums):
    result = []
    for x in nums:
        if x != 0:
            result.append(x)
    while len(result) < len(nums):
        result.append(0)
    return result

nums = [0, 1, 0, 3, 12]
assert move_zeroes_copy(nums) == [1, 3, 12, 0, 0]
assert nums == [0, 1, 0, 3, 12]
```

第一段依次得到 []、[1]、[1,3]、[1,3,12]，跳过零；第二段补到原长度 5。改变输入为全零、全非零、空列表，再追踪执行次数。

```python
def move_zeroes_inplace_basic(nums):
    non_zero = [x for x in nums if x != 0]
    k = len(non_zero)
    for i in range(k):
        nums[i] = non_zero[i]
    for i in range(k, len(nums)):
        nums[i] = 0

nums = [0, 1, 0, 3, 12]
assert move_zeroes_inplace_basic(nums) is None
assert nums == [1, 3, 12, 0, 0]
```

这里确实修改原对象，但仍有额外列表。原地修改与 O(1) 额外空间不是同一句话，第 06 章再消除额外数组。

## 10. 字母异位词分组：特征到同组单词

**任务：** 把 ['eat','tea','tan','ate','nat','bat'] 按字母组成分组，组间顺序不影响语义。先限定小写英文字母，不额外引入文字归一化问题。

```python
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
groups = {}
for word in words:
    chars = sorted(word)           # 'tea' → ['a', 'e', 't']
    key = "".join(chars)           # → 'aet'
    if key not in groups:
        groups[key] = []
    groups[key].append(word)      # 修改该键关联的列表
answer = list(groups.values())
print(answer)                     # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

eat、tea、ate 都得到 aet，于是进入同组。sorted、join、查询、append、values 每一步都已在所属容器部分学过；新增的是“用标准形式表示同类”的思路。

## 11. 复杂度入门与章节验收

长度为 n 的单次遍历做 n 次，记作 O(n)；检查所有不同位置组合约有 n(n-1)/2 次，按平方增长，记作 O(n²)。字典和集合的查询通常按平均 O(1) 估算，所以两数之和字典版平均 O(n) 时间、O(n) 额外空间。不是所有两层缩进都一定平方，也不是字典在任何情况下都绝对常数；第 05、06 章展开。

闭卷解释：append 为什么返回 None，pop 为什么返回被删元素？get 是否写入？tuple 为什么没有 append？split 得到什么类型？items 与解包分别做什么？set 为什么不能保留首次顺序？能回答后再完成[第 03 章练习](03-basic-exercises.md)和[Notebook](../exercises/03-basic-exercises.ipynb)。

本章覆盖主线需要的常用基础操作，不声称穷举标准库全部 API；后续若新增基础操作，应先补到这里的所属容器小节，而不是散落在某道算法题后面。

语义依据：[数据结构教程](https://docs.python.org/3/tutorial/datastructures.html)、[内置类型](https://docs.python.org/3/library/stdtypes.html)、[内置函数](https://docs.python.org/3/library/functions.html)。
