# 02｜数据类型与容器：给数据选一个合适的组织方式

[← 上一章：程序基础](01-programming-fundamentals.md) · [Coding 首页](../README.md) · [下一章：基础练习 →](03-basic-exercises.md)

只有一个成绩时，写 `score = 90` 就够了。如果有全班同学的成绩呢？如果还要通过姓名查成绩，或者只问“这个人是否已经签到”，同一种保存方式还方便吗？

**容器不是要背的一排名词，而是几种组织数据的办法。** 顺序重要时用列表，固定的一组值可以放进元组，文字用字符串，名字到成绩的关系用字典，只关心有没有出现则用集合。

这一章围绕这些常见任务，练习后续编程中反复要用的操作。每种容器先学清楚自己最重要的用法，再把它们组合起来解决两数之和、移动零和分组问题。目标是见到数据就知道如何下手，不是记完 Python 的方法目录。

## 1. 读一行操作时，分开看“改了什么”和“得到什么”

上一章已经区分过 `print` 与 `return`。操作容器也有类似的区别：有的操作修改原来的数据，有的操作返回一个新结果，也有的两件事都做。

例如，`len(nums)` 问“有几个元素”，不会改变 nums；`nums.append(3)` 把一个新元素加到原列表末尾，却不返回新的列表。不能看到一行代码就只问“输出是多少”，因为这行可能根本没有打印。

调用形状也可以先认一认：`len(nums)` 是把 nums 传给**函数**；`nums.append(3)` 是通过对象调用它的**方法**。但有没有点号，并不决定操作会不会修改原数据，仍要看这个操作本身的含义。

下面每个例子都给出初始数据。代码右侧的注释会说明返回值或执行后的状态；真正要在屏幕上看到它，仍需要 `print`。

<a id="list"></a>
## 2. list：把一组数据按顺序放好

假设三次练习的得分依次是 10、20、30。你既关心分数，也关心它们出现的顺序，就可以用列表保存：

```python
nums = [10, 20, 30]
print(len(nums))    # 3：一共有三个元素
print(nums[0])      # 10：第一个元素
print(nums[1])      # 20：第二个元素
print(nums[-1])     # 30：最后一个元素
print(20 in nums)  # True：值 20 在列表里
```

方括号里放各个元素，逗号负责分开它们。**下标从 0 开始**，所以长度为 3 的列表，合法非负下标是 0、1、2；访问 `nums[3]` 就会越界。

`in` 检查的是值是否出现，不是在问下标是否合法。空列表写成 `[]`；在条件中，空列表按假处理，非空列表按真处理。即使是 `[0]`，也因为有一个元素而不是空列表。

### 2.1 要一个元素，还是要连续的一段

下标取得一个元素，**切片**取得一段位置上的元素，组成新列表：

```python
nums = [10, 20, 30, 40]
print(nums[1:3])   # [20, 30]：包含位置 1，不包含位置 3
print(nums[:2])    # [10, 20]：从开头取到位置 2 之前
print(nums[2:])    # [30, 40]：从位置 2 取到末尾
print(nums[::-1])  # [40, 30, 20, 10]：反向构造新列表
```

可以把 `nums[1:3]` 想成“从位置 1 开始，在到达位置 3 前停下”。左边包含、右边不包含，与 `range` 的终点规则相呼应。

完整形式是 `nums[start:stop:step]`，例如 `nums[::2]` 每隔一个位置取一项；`[::-1]` 的步长是 -1。切片不修改原列表，还可能得到空列表。它与单个下标的边界行为不同：切片超过末尾会截到边界，单个下标越界则报错。

### 2.2 改一个值、添一个值、取走一个值

假设第二次成绩录错了，需要改成 99；又完成一次练习，追加 40；随后发现这次不计入统计，要把它取走。

```python
nums = [10, 20, 30]
nums[1] = 99           # nums 变成 [10, 99, 30]
result = nums.append(40) # nums 变成 [10, 99, 30, 40]
print(result)          # None：append 不返回列表
last = nums.pop()      # last = 40；nums 变回 [10, 99, 30]
print(last, nums)      # 40 [10, 99, 30]
```

这三行分别是替换、追加和删除。`append` 修改原对象，返回 `None`；`pop` 不仅删除，还把取走的值返回。因此不要写 `nums = nums.append(40)`，否则名字 nums 最后会关联到 None，而不是追加后的列表。

删除时还要分清“按位置”与“按值”：

```python
nums = [10, 20, 30, 20]
first = nums.pop(0)  # 返回 10，nums 变成 [20, 30, 20]
nums.remove(20)      # 删除第一个值为 20 的元素，nums 变成 [30, 20]
print(first, nums)   # 10 [30, 20]
```

空列表不能 `pop()`，`remove` 找不到值也会报错。过滤数据时，先构造一个新列表通常更好理解；边遍历原列表边删除，后续位置会变化，容易跳过元素。

一次加入多个元素时，另一个常用区别是“整体加入”还是“逐项加入”：

```python
a = [1]
a.append([2, 3])  # [1, [2, 3]]：把整个列表当成一个元素
b = [1]
b.extend([2, 3])  # [1, 2, 3]：把来源里的元素逐个加到末尾
print(a, b)       # [1, [2, 3]] [1, 2, 3]
```

### 2.3 遍历：要值、要下标，还是两者都要

如果只是逐个处理分数，直接取得元素值最自然：

```python
nums = [10, 20, 30]
for x in nums:
    print(x)             # 10、20、30，各一行
for i in range(len(nums)):
    print(i, nums[i])     # 0 10、1 20、2 30，各一行
```

第一种的 x 是值，第二种的 i 是下标。名字本身没有决定作用：写 `for i in nums`，i 仍然接收 10、20、30，而不是 0、1、2。

同时需要下标和值时，可以使用 `enumerate`。不过先看懂一对数据怎样分给两个名字，这个动作叫**解包**：

```python
i, x = [0, 10]  # 第一项交给 i，第二项交给 x
print(i, x)     # 0 10

nums = [10, 20, 30]
for i, x in enumerate(nums):
    print(i, x) # 0 10、1 20、2 30，各一行
```

`enumerate` 每次提供一对“编号、元素值”，循环头再把它们分别交给 i 和 x。默认编号从 0 开始，正好对应列表下标。先理解“提供一对”和“拆给两个名字”这两个动作，后面就不会把双变量循环看成新的魔法。

### 2.4 排序：拿一份新结果，还是改变原顺序

把分数从小到大排好时，先问：原来的时间顺序还需要保留吗？

```python
nums = [3, 1, 2]
ordered = sorted(nums)   # 返回新列表 [1, 2, 3]
print(nums, ordered)     # [3, 1, 2] [1, 2, 3]
returned = nums.sort()   # 原列表变成 [1, 2, 3]
print(nums, returned)    # [1, 2, 3] None
```

`sorted` 返回新的排序结果；`.sort()` 改变原列表，返回 None。两者都能用 `reverse=True` 指定降序。

反转则是另一个动作：只把前后顺序倒过来，不按大小重新排列。汇总操作也不会改动列表：

```python
nums = [3, 1, 2]
nums.reverse()          # nums 变成 [2, 1, 3]，不是降序排序
print(nums)             # [2, 1, 3]
print(sorted(nums, reverse=True)) # [3, 2, 1]
print(sum(nums))        # 6：求和
print(min(nums), max(nums)) # 1 3：最小值与最大值
```

空列表求和为 0，但没有指定默认值时，`min([])` 和 `max([])` 都没有可返回的极值，会报错。还不能默认任意混合类型都能比较，例如整数与字符串无法直接按大小排序。

当“排序依据”不是元素本身时，`key` 可以接收一个函数。下面按绝对值排，比较依据依次是 3、1、2，但结果保留原来的数字：

```python
nums = [-3, 1, -2]
print(sorted(nums, key=abs))  # [1, -2, -3]
```

传 `abs` 而不是 `abs()`，因为要交给排序操作一个“对每项求比较依据”的函数，而不是提前调用一次。这样理解后，按区间起点、字符串长度排序，就只是换一种比较依据。

### 2.5 构造结果：先会循环，再看推导式

从 `[1,2,3,4]` 里挑偶数，并把它们平方，最直白的过程是：取出一个值，判断，符合要求才加入结果。

```python
nums = [1, 2, 3, 4]
result = []
for x in nums:
    if x % 2 == 0:
        result.append(x * x)
print(result)  # [4, 16]
```

把同一个过程压在一行，就是列表推导式：

```python
nums = [1, 2, 3, 4]
result = [x * x for x in nums if x % 2 == 0]
print(result)  # [4, 16]
```

阅读时仍先看中间的 for，再看 if，最后看最前面的 `x * x` 放进结果。**写得短不会改变执行逻辑。** 如果一行让你看不清过程，就保留普通循环；这比强记紧凑写法更有用。

### 2.6 复制与二维列表：为什么两处会一起变

前一章改变量 x，并不会把 old 一起改掉。但两个名字指向同一个列表时，修改列表会被它们共同观察到：

```python
nums = [1, 2]
alias = nums        # 不是复制，只是另一个名字指向同一列表
saved = nums.copy() # 新建一个外层列表
alias.append(3)
print(nums)         # [1, 2, 3]
print(saved)        # [1, 2]
```

`alias = nums` 与 `nums.copy()` 的目的不同。前者共享对象，后者得到新的外层列表；后者叫浅拷贝，因为里面的对象并不一定继续复制。`==` 比较内容，`is` 比较是不是同一个对象。

矩阵就是“列表里面还有列表”，两个下标分别取行和列：

```python
grid = [[1, 2, 3], [4, 5, 6]]
print(grid[0])     # [1, 2, 3]：第一行
print(grid[0][1])  # 2：第一行的第二个元素
```

初始化矩阵时，有一个与共享对象直接相关的坑，值得在这里弄懂：

```python
bad = [[0, 0]] * 2          # 两个位置引用的是同一行
bad[0][0] = 9
print(bad)                  # [[9, 0], [9, 0]]
good = [[0, 0] for _ in range(2)] # 每轮新建一行；_ 表示不用的循环变量
good[0][0] = 9
print(good)                 # [[9, 0], [0, 0]]
```

`[0] * 3` 适合得到三个零；但把一个**可变的行列表**重复放进去，不会复制出独立的三行。需要每行独立，就在每轮真正创建一行。

<a id="tuple"></a>
## 3. tuple：把几个位置的含义固定下来

坐标中的 3 表示行、5 表示列。它们是一个整体，却不是准备不断追加成绩的列表。这样的固定组合可以用元组表示：

```python
point = (3, 5)
print(point[0], point[1])  # 3 5
row, col = point          # row=3，col=5：与列表一样按位置解包
print(row, col)           # 3 5
single = (3,)             # 只有一项也要有逗号；(3) 只是整数 3
print(type(single))       # <class 'tuple'>
```

元组也能使用 `len`、下标、切片、`in` 和普通 for，含义与列表相通。关键区别是**元组不可变**：不能替换某个位置，也没有 append。无需为了对齐列表的目录，重新背一套相同的读取操作。

解包也常见于交换变量和函数返回多个结果：

```python
a, b = 2, 5
a, b = b, a              # 先得到右侧两个旧值，再分别写到左侧
print(a, b)              # 5 2

def bounds(nums):
    return min(nums), max(nums) # 返回一对结果

low, high = bounds([3, 1, 5])
print(low, high)         # 1 5
```

如果先写 `a = b` 再写 `b = a`，原来的 a 已经丢了；多目标赋值先取得右侧全部旧值，才避免这个问题。普通解包两边项数不匹配会报错。

在需要转换时，`list(point)` 得到新列表，`tuple([3,5])` 得到元组。不可变约束的是元组各位置的绑定，不保证内部每个对象都不可变；例如元组里包含一个列表，那个列表仍然可能被修改。

<a id="str"></a>
## 4. str：按顺序读文字，再构造需要的文字

字符串也有顺序，因此已经学会的下标、切片和遍历，不必重新理解一遍。只是每次取出的不是分数，而是一个字符。

```python
text = "hello"
print(len(text))      # 5
print(text[0])        # h
print(text[1:4])      # ell
print(text[::-1])     # olleh
print("ell" in text) # True：这里检查一段子串是否出现
for ch in text:
    print(ch)         # h、e、l、l、o，各一行
```

空字符串写作 `""`。字符串不可变，不能通过 `text[0] = "H"` 修改它。要把 hello 变成 Hello，应当构造新字符串：

```python
text = "hello"
changed = "H" + text[1:] # 用 H 接上后面的 ello
print(changed)           # Hello
print(text)              # hello：原字符串没有改变
```

这就是字符串与列表在“修改”上的区别。`+` 用于拼接新文字，而不是修改某个字符的位置。

### 4.1 split：一整行怎样变成几项

输入常常是一行文字 `"10 20 30"`，但你想逐个处理其中的数。`split` 先负责拆分，**不会顺便完成数值转换**。

```python
line = "10 20 30"
parts = line.split()
print(parts)             # ['10', '20', '30']
print(type(parts[0]))    # <class 'str'>
print("red,blue".split(",")) # ['red', 'blue']：明确用逗号拆分
```

无参数的 `.split()` 按空白拆分，连续的空格或换行会作为分隔；明确传入分隔符时，则按那个分隔符拆。后续需要整数，再逐项调用 `int`。先认清拆分前后是什么类型，复杂的输入写法就容易拆开。

### 4.2 join：几项文字怎样重新连成一项

反过来，已经有多个字符串，想连接成一段文字，可以使用 `分隔符.join(各项文字)`：

```python
words = ["AI", "coding"]
print(" ".join(words))  # AI coding：中间放一个空格
print("-".join(words))  # AI-coding
print("".join(words))   # AIcoding：不放分隔符
```

注意点号前面不是 words，而是**要放在两项之间的分隔符**。空字符串 `""` 也能调用方法，它表示“中间不要加入任何字符”。每项必须是字符串；整数要先转成文字，join 不会替你自动转换。

如果想把一个单词的字符按顺序整理，也可以组合排序与拼接：

```python
chars = sorted("tea") # ['a', 'e', 't']：sorted 返回列表
key = "".join(chars)  # 'aet'
print(key)            # aet
```

这里发生了两步类型变化：字符串经过 sorted 得到字符列表，join 再把它变回字符串。这正是后面分组时 `"".join(sorted(word))` 的来历，不必把长表达式整体背下来。

<a id="dict"></a>
## 5. dict：通过一个键找到对应的信息

名单与成绩若分别放在两个列表里，你还得先找姓名的位置。字典可以直接表达“姓名对应成绩”：

```python
scores = {"Alice": 90, "Bob": 85}
print(scores["Alice"])   # 90
print("Alice" in scores) # True：检查键，不是检查成绩
scores["Bob"] = 88       # 修改 Bob 的值
scores["Carol"] = 95     # 新增一个键及其值
print(scores["Bob"])     # 88
```

冒号左边是**键 key**，右边是**值 value**。一个键只对应一个值，所以再次给 Bob 赋值是在覆盖原成绩，而不是增加第二个 Bob。空字典写成 `{}`。

基础题里常用整数和字符串作键。元素都可哈希的元组也能作键，列表则不能；“可哈希”的机制可以在知识课程继续学习。值可以是列表等容器，这样就能表达“一个特征对应一组单词”。

### 5.1 可能没有这个键时，怎样读取

直接读取 `scores["Dan"]` 会因为缺失键而报 KeyError。但统计频次时，“还没见过这个数字”很正常，可以用 get 提供默认值：

```python
scores = {"Alice": 90}
print(scores.get("Alice", 0)) # 90：存在就取原值
print(scores.get("Dan", 0))   # 0：缺失时使用默认值
print("Dan" in scores)       # False：get 没有新增这个键
```

`get` 是读取，不是写入。这里返回 0，也不表示字典里已经存了 `"Dan": 0`。若任务认为缺失就是错误，也不要随意用默认值把问题掩盖掉。

不再需要一条记录时，可以按键删除：

```python
scores = {"Alice": 90, "Bob": 85}
del scores["Bob"]       # 删除 Bob 这一条；不是把成绩改为 0
print(scores)           # {'Alice': 90}
```

`del` 是删除语句，键必须存在。

### 5.2 遍历：只要键、只要值，还是键值都要

```python
scores = {"Alice": 90, "Bob": 85}
print(list(scores.keys()))   # ['Alice', 'Bob']
print(list(scores.values())) # [90, 85]
print(list(scores.items()))  # [('Alice', 90), ('Bob', 85)]
```

这三行是同一份字典的三种观察方式。`keys` 看名字，`values` 看成绩，`items` 看一对对的“名字、成绩”。外面的 list 把各项收集成列表，便于显示；这些方法本身返回的不是可直接用下标取第一个元素的普通列表。

```python
scores = {"Alice": 90, "Bob": 85}
for name in scores:
    print(name)          # Alice、Bob，各一行：默认遍历键
for value in scores.values():
    print(value)         # 90、85，各一行
for name, value in scores.items():
    print(name, value)   # Alice 90、Bob 85，各一行
```

最后一种不是新语法：items 提供一对，循环头解包，再把两项交给 name 和 value。字典保留插入顺序，但不会自动按键或值排序；遍历过程中也不应随意增删键。

### 5.3 计数：让每个字符对应“见过几次”

现在把“姓名 → 成绩”换成“字符 → 次数”，字典就可以统计 banana 中每个字符出现几次。

```python
text = "banana"
count = {}
for ch in text:
    old = count.get(ch, 0) # 以前没见过，就当作 0 次
    count[ch] = old + 1    # 增加一次，再写回
print(count)              # {'b': 1, 'a': 3, 'n': 2}
```

第一次读到 b，字典还为空，因此取到默认 0，写入 b:1。第一次读到 a 也是如此。第二次读到 a 时，旧次数已经是 1，于是覆盖成 2。**新增和更新并不是两套算法：都是取得旧次数，再把新次数写回。**

把循环体的两行合起来，就是常见的 `count[ch] = count.get(ch, 0) + 1`。阅读仍从右侧开始，不能把它误解为“字典自动加一”。

字典还能存位置，关键在于你给值赋予什么含义：

```python
nums = [5, 8, 5]
position = {}
for i, x in enumerate(nums):
    position[x] = i
print(position)  # {5: 2, 8: 1}：这里保存最后一次出现的位置
```

若想保存首次位置，就先检查 x 是否已经是键，已经有了便不要覆盖。写代码之前先说清楚“值代表次数还是下标”，比记住某段模板重要。

<a id="set"></a>
## 6. set：只问“有没有见过”

检查签到是否重复时，不一定需要知道每个人出现多少次，也不一定需要保存位置。集合只记录成员是否存在：

```python
seen = set()       # 创建空集合；{} 创建的是空字典
seen.add(10)       # 加入成员 10
seen.add(20)       # 加入成员 20
seen.add(10)       # 重复加入，不会多出一份 10
print(len(seen))   # 2
print(10 in seen)  # True
print(99 in seen)  # False
```

set 不保存重复次数，也不保证遍历顺序，没有“第几个成员”的下标。`set([3,1,3])` 可以得到只有 3 和 1 的集合，但不能据此保证“保留第一次出现的顺序”。成员和字典键一样需要可哈希，列表不能直接作为成员。

需要把一个成员移出去时，常用 remove 或 discard：

```python
seen = {10, 20}
seen.remove(10)    # 现在只剩成员 20；10 必须存在
seen.discard(99)   # 99 不存在也不报错
print(20 in seen) # True
```

它们的区别是**成员不存在时怎么办**。算法已经保证成员在集合里时可以用 remove；不存在也允许时用 discard。集合遍历仍使用普通 for，只是不要把某次观察到的顺序当作保证。

把这些操作组合起来，就能判断是否有重复：

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

必须先查询再加入。否则刚把 x 放进去，又问 x 在不在，就会把每个元素都判成重复。这里 seen 的含义始终是“**这轮之前**已经出现的成员”。

## 7. 跨容器组合：把已经会的操作接起来

### 7.1 两列数据一一对应时，用 zip 配对

姓名与成绩来自两列，想逐个一起处理，不需要自己同时维护两个下标：

```python
names = ["Alice", "Bob"]
scores = [90, 85]
pairs = list(zip(names, scores))
print(pairs)  # [('Alice', 90), ('Bob', 85)]
for name, score in pairs:
    print(name, score) # Alice 90、Bob 85，各一行
```

zip 负责把相同位置的项配成一对，解包负责把一对分给两个名字。默认会在较短的一组结束时停止；任务要求两组一一对应时，要先确认长度一致，不能让数据悄悄丢失。

### 7.2 把列表交给函数：改原来的，还是返回新的

```python
def doubled(nums):
    return [x * 2 for x in nums]

def add_zero(nums):
    nums.append(0)

original = [1, 2]
answer = doubled(original)
print(answer, original) # [2, 4] [1, 2]
returned = add_zero(original)
print(original, returned) # [1, 2, 0] None
```

第一个函数构造新列表并返回，第二个函数修改传入的原列表。参数名也是名字，因此通过它修改共享对象，调用方会看见；但在函数内写 `nums = []` 只是让局部名字指向新列表，不会替调用方重新赋值。

做题前先确认要求的是哪一种。**“函数没有返回值”不等于“函数没有改变数据”。**

## 8. 两数之和：我真正需要找的是什么

给定 `nums=[2,7,11,15]` 与 `target=9`，返回两个不同下标，使对应的数相加等于 9，结果应为 `[0,1]`。本练习保证存在时只有一组答案，无解时扩展约定返回 `[]`。

最直接的办法是逐对检查。两层循环没有新语法，只是把上一章的编号配对换成通过下标读取数值：

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

但站在当前数字 x 的位置看，我并不需要尝试所有数字。我知道要找的是 `target - x`，缺的只是“它以前出现在哪里”。这个问题恰好适合字典。

```python
def two_sum(nums, target):
    seen = {}                      # 数字 → 此前出现的下标
    for i, x in enumerate(nums):
        need = target - x
        if need in seen:
            return [seen[need], i]
        seen[x] = i
    return []

assert two_sum([2, 7, 11, 15], 9) == [0, 1]
assert two_sum([3, 3], 6) == [0, 1]
assert two_sum([3], 6) == []
```

| 当前值 | 需要的值 | 查询前的 seen | 接下来做什么 |
|---:|---:|---|---|
| 2 | 7 | {} | 没有 7，记下 2 在位置 0 |
| 7 | 2 | {2: 0} | 找到了 2，返回它的位置 0 与当前位置 1 |

先查再记录，保证只和此前的位置配对；不能拿当前位置使用两次。这个顺序与集合判重相似，但字典还保存了答案需要的下标。

## 9. 移动零：同一个结果，两种交付方式

把 `[0,1,0,3,12]` 中的零放到末尾，非零数字保持原相对顺序，应得到 `[1,3,12,0,0]`。先不追求最省空间，只用熟悉的循环和列表操作完成它。

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

for 遇到零就跳过，依次收集出 `[1]`、`[1,3]`、`[1,3,12]`。原来一共五项，现在只有三项，所以 while 再补两个零。条件依赖的长度会在每次 append 后增加，因此它能结束。

如果要求修改原列表，而不是返回新列表，应该把收集到的值写回去：

```python
def move_zeroes_inplace_basic(nums):
    non_zero = []
    for x in nums:
        if x != 0:
            non_zero.append(x)
    k = len(non_zero)
    for i in range(k):
        nums[i] = non_zero[i]
    for i in range(k, len(nums)):
        nums[i] = 0

nums = [0, 1, 0, 3, 12]
assert move_zeroes_inplace_basic(nums) is None
assert nums == [1, 3, 12, 0, 0]
```

先覆盖前 k 个位置，剩余位置填零，调用方才会观察到原对象变化。不过我们仍创建了额外列表。**修改原对象与只用常数额外空间是两个不同要求。** 双指针可以进一步用原列表中的位置保存进度，从而省掉这份随输入增长的中间结果；理解它之前，这个版本已足够练熟基础操作。

## 10. 字母异位词：先找出“同一组”的共同特征

`eat`、`tea`、`ate` 顺序不同，却使用相同的字母。要给单词分组，先问：能不能给同组单词算出一个相同的标记？

把字符排序再拼回字符串，这三个词都会变成 `aet`。于是字典可以保存“标记 → 这一组的单词列表”。下面先限定小写英文字母：

```python
words = ["eat", "tea", "tan", "ate", "nat", "bat"]
groups = {}
for word in words:
    chars = sorted(word)     # 'tea' → ['a', 'e', 't']
    key = "".join(chars)     # → 'aet'
    if key not in groups:
        groups[key] = []     # 第一次遇到这一组，先准备空列表
    groups[key].append(word) # 把原单词加到这一组，不是加入排序后的 key
answer = list(groups.values())
print(answer) # [['eat', 'tea', 'ate'], ['tan', 'nat'], ['bat']]
```

第一次遇到 eat，先建立 `groups["aet"]`，里面放入 eat。遇到 tea 时不再创建组，而是取出已经存在的列表，追加 tea。最后只需要各组，不需要标记，所以取 `.values()`，再收集成列表。

这几步仍是已学过的排序、拼接、字典查询与列表追加。真正新增的是一种解题思路：**给同类数据构造相同的特征，再按特征聚在一起。**

## 11. 本章小结与面试怎么答

列表记顺序，元组记固定组合，字符串记文字，字典记对应关系，集合记成员。选容器之前先问“下一步最常需要知道什么”，操作时再区分原对象变化、返回值和输出。

两数之和从逐对尝试变成字典查询，也给复杂度一个直观入口：长度为 n 时，逐对检查约有 n(n-1)/2 对，按 O(n²) 增长；一次扫描配合平均 O(1) 的字典查询，平均时间可按 O(n) 估算，但额外保存了 O(n) 的历史信息。这里是常见成本模型，不是承诺任意字典操作都绝对常数时间。

**问：怎样选择 list、dict 和 set？**

> 🎯 需要按顺序或位置组织数据，用 list；需要通过键取得关联信息，用 dict；只关心成员是否存在，用 set。比如保序去重需要同时满足存在性和顺序，可以用 set 判断、list 收集，而不是直接把 set 转回 list。

**问：sorted(nums) 与 nums.sort() 有什么区别？**

> 🎯 sorted 返回新的排序列表，原列表保持不变；sort 修改原列表并返回 None。先确认是否允许改变输入，再选择用法。

## 12. ⚠️ 容易混淆的地方

- 下标和值是两种信息。`for x in nums` 已经取得值，不能再不加判断地拿它当下标。
- `.append()`、`.sort()` 返回 None；`.pop()` 返回取出的值。不要把所有修改方法的返回值都当作新容器。
- `{}` 是空字典，`set()` 才是空集合；集合不保证保留首次出现顺序。
- `get` 只读取；`count[x] = ...` 才写入。一个字典的值是次数还是下标，必须由任务明确。
- 浅拷贝只让外层独立。二维列表和回溯路径等场景，要检查内部可变对象是否仍在共享。

## 13. 章节自测

<details>
<summary>1. 为什么 append([2,3]) 和 extend([2,3]) 的结果不同？</summary>

append 把参数作为一个元素放进去，因此新增元素本身是列表；extend 逐项读取来源，把 2 和 3 分别加入。先问“我想加一项，还是加来源中的每一项”。

</details>

<details>
<summary>2. for name, score in scores.items() 中，items 与解包分别做什么？</summary>

items 每轮提供一对键和值；解包把第一项交给 name，第二项交给 score。字典遍历与多变量赋值是两个配合的动作，不是一个无法拆开的语法。

</details>

<details>
<summary>3. 为什么 groups[key].append(word) 不需要再把列表赋回 groups[key]？</summary>

通过 groups[key] 取得的就是那个组所关联的列表对象，append 已经修改了它，不是先修改一份独立副本。因此无需重新绑定这个键。

</details>

**动手验收：** 对 `[3,1,3,2,1]` 分别写出频次表 `{3:2,1:2,2:1}` 和保序去重结果 `[3,1,2]`。先说明为什么一个任务只要字典，另一个需要集合与列表配合，再到[基础练习](03-basic-exercises.md)或[Notebook](../exercises/03-basic-exercises.ipynb)独立完成。

## 14. 知识课程回看

想深入理解容器的对象性质与查找成本，看 [Python：核心数据类型与容器](../../../curriculum/01-python/docs/02-核心数据类型与容器.md)；对“明明复制了，为什么内部还一起变化”有疑问，看 [Python：可变对象与深浅拷贝](../../../curriculum/01-python/docs/03-可变对象-对象身份-深浅拷贝.md)。它们承载更完整的语言机制，这里优先把核心操作练熟。

语义依据：[数据结构教程](https://docs.python.org/3/tutorial/datastructures.html)、[内置类型](https://docs.python.org/3/library/stdtypes.html)、[内置函数](https://docs.python.org/3/library/functions.html)。
