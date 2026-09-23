# 01｜程序基础：先读懂执行，再写出函数

[← Coding 首页](../README.md) · [下一章：数据类型与容器 →](02-python-coding-basics.md)

> 本章从零开始解释值、赋值、输入输出、判断、循环、函数、验证和错误。容器的完整操作在第 02 章学习；Hot100 的组合例子在容器之后出现，不把尚未教学的列表操作当作本章前提。

## 1. 代码、执行与表达式

把代码保存为 `main.py`，在文件所在目录运行 `python main.py`；有些环境命令是 `python3`，应确认使用 Python 3。`#` 后面是给人看的注释，不参与执行。

```python
x = 2
other = 3
answer = x + other       # 先算右侧，再让 answer 关联整数 5
print(answer)            # 5
```

`print(answer)` 把 answer 的值作为参数交给 Python 提供的 print 函数，让它显示结果。函数调用先按“把数据交给一个操作”理解，第 8 节再学习自己定义函数。

文件里的文字是源代码，解释器执行它们才是一次运行。这里从上往下执行，第三行不是数学等式，而是“求右边的值，再赋给左边”。`2 + 3` 是表达式，会得到 5；在普通文件中单写表达式不会自动打印，交互环境显示结果是额外提供的便利。

逐行读代码时，始终问：读了什么值，做了什么操作，哪些状态改变，有没有输出，下一步去哪里。后面的判断、循环、函数只是改变了这条执行路线。

## 2. 数值类型：操作、结果和边界

`int` 是整数，`float` 是浮点数。`type(value)` 返回对象类型；小数不一定能用浮点数精确表示，因此不要把小数显示误当成十进制绝对精确。

```python
print(type(18))          # <class 'int'>
print(type(2.5))         # <class 'float'>
print(7 + 2)            # 9
print(7 - 2)            # 5
print(7 * 2)            # 14
print(7 / 2)            # 3.5：除法
print(7 // 2)           # 3：向下取整除法
print(-7 // 2)          # -4：向负无穷取整，不是直接删除小数
print(7 % 2)            # 1：余数；整数 x % 2 == 0 表示偶数
print(2 ** 3)           # 8：乘方
print(abs(-7))          # 7：绝对值
print(round(3.14159, 2)) # 3.14：数值舍入，不等于固定显示两位小数
```

乘除先于加减；不确定时用括号表达意图。除数为零会报 `ZeroDivisionError`。Python 整数不受固定 32 位上限约束，但大整数仍然消耗计算时间和内存。位运算也属于整数操作，集中在本节末尾介绍；第 07 章只讨论这些操作怎样解决具体问题。

引号里的内容属于字符串 `str`，也就是文字。这里先区分数字与数字的文字表示；字符串全部常用操作归第 02 章。

```python
text = "18"
number = int(text)      # number=18；text 仍为字符串 "18"
print(number + 1)      # 19
print(float("2.5"))    # 2.5
print(int(2.9))        # 2：向零截断，不是四舍五入
print(str(18))         # 18：得到字符串，打印时不显示两边引号
```

`int("hello")`、`int("2.5")` 会报 `ValueError`；类型转换需要输入内容符合格式，不会替你猜想要的含义。

### 2.1 整数的位运算：工具在这里，算法应用在第 07 章

二进制每一位只有 0 或 1，`0b` 前缀表示二进制整数；`bin` 把整数显示成二进制文字。初次阅读先知道每种操作的含义，不要求立即把它用到算法里。

```python
print(bin(5))             # 0b101
print(int("101", 2))     # 5：按二进制解释文字
print(5 & 3)              # 1：逐位同时为 1 才为 1
print(5 | 3)              # 7：逐位至少一项为 1 就为 1
print(5 ^ 3)              # 6：逐位不同才为 1，^ 不是乘方
print(5 << 1)             # 10：左移一位
print(5 >> 1)             # 2：右移一位
print(~5)                 # -6：Python 整数取反满足 ~x = -x-1
```

5 的二进制是 101，3 是 011；按相同位置做运算就得到上面结果。Python 整数位运算不受固定 8/32 位截断约束，因此不要把 ~5 误算成某个无符号小整数。`answer ^= x` 与整数场景的 `answer = answer ^ x` 对应。布尔判断使用后面条件部分会学的 and/or/not，不用位运算代替。

## 3. 变量名不等于对象

```python
x = 10
old = x               # old 也关联整数 10
x = x + 1             # 用旧 x 计算 11，再重新绑定 x
print(x, old)         # 11 10
x += 1                # 对本例整数，相当于 x = x + 1
print(x)              # 12
```

名字是到对象的关联，不是对象本身。重新绑定 x 不会同时重新绑定 old。第 02 章会说明另一种情况：两个名字关联同一个可变列表时，修改列表对象会被两边同时观察到。

`=` 赋值，`==` 比较值。名字先定义才能读取；拼错名字或超出作用域会导致 `NameError`。读代码要恢复运行时的状态，而不是假定一个变量永远代表同一个值。

## 4. 输入与输出：让类型可观察

下面程序运行时输入 `18` 并回车。`input()` 读取一行并去掉行末换行，正常返回字符串，不会自动识别数字。

<!-- run: {"stdin":"18\n","stdout":"18\n<class 'str'>\n'18'\n<class 'int'>\n19\n"} -->
```python
age_text = input()
print(age_text)          # 18
print(type(age_text))    # <class 'str'>
print(repr(age_text))    # '18'：repr 展示便于诊断的表示，包括引号
age = int(age_text)
print(type(age))         # <class 'int'>
print(age + 1)           # 19
```

`int(input())` 是先调用里面的 input，再把返回值传给 int。屏幕显示相同，不代表类型相同。输入源结束而没有数据时会报 `EOFError`；第 04 章学习完整输入协议。

```python
print(2, 3)             # 2 3：默认空格分隔，末尾换行
print(2, 3, sep=",")    # 2,3：sep 指定分隔符
print("A", end="")      # A 后面不换行
print("B")              # 与上一行合起来显示 AB
```

`sep=...`、`end=...` 是按名字传参数。变量变化和注释不会自动产生输出。后面的笔试里只能输出题目要求的内容，不能夹带“请输入”等提示文字。

## 5. 布尔值、条件与缩进

`bool` 的两个值是 `True/False`，分别为真和假。比较运算 `== != < <= > >=` 得到布尔值。条件链从上往下检查，只执行第一个满足的分支。

```python
age = 16
print(age >= 18)         # False
if age >= 18:
    print("adult")
elif age >= 13:
    print("teen")       # 本例输出 teen
else:
    print("child")
```

冒号表示后面有代码块；同一块使用一致缩进，通常四个空格。`else` 没有自己的条件，表示前面都不满足。缩进错不仅是排版问题，也会改变执行逻辑或直接报错。

```python
age = 20
has_ticket = True
print(age >= 18 and has_ticket)  # True：两个条件都满足
print(age < 18 or has_ticket)    # True：至少一个条件满足
print(not has_ticket)           # False：取反
```

布尔转换 `bool(value)` 显式得到条件判断使用的真或假；0、0.0、None 按假处理，非零数按真处理。第 02 章在各容器的语境中说明空容器与非空容器。

```python
print(bool(0), bool(2))      # False True
print(bool(None))           # False
```

`and/or` 会短路：结果确定时不再计算右侧。这里操作数是布尔值；对一般对象使用 and/or 不保证返回 bool，先用清楚的 if 表达业务。`None` 表示没有结果或未提供值，不是数字 0；函数部分马上使用。

## 6. for：数据来源负责提供下一项

```python
for x in range(1, 4):
    print(x)             # 1、2、3，各一行
print("done")            # done
```

`range(1,4)` 表示从 1 开始、到 4 之前的整数范围。每轮 for 取得下一项，把它赋给 x，再执行缩进块；取不到下一项时结束。x 没有魔法，换成 number 也一样。以后遍历列表时，取得的是列表元素，不会自动取得下标。

### 6.1 range 的三个参数

`range(stop)` 默认从 0 开始；`range(start,stop)` 指定起点；`range(start,stop,step)` 再指定步长。终点始终不包含，步长默认 1，不能是 0。

```python
for i in range(3):
    print(i)             # 0、1、2
for i in range(2, 5):
    print(i)             # 2、3、4
for i in range(5, 0, -2):
    print(i)             # 5、3、1
```

`range(5,0)` 是空范围，因为正步长无法走向更小的终点。range 是可反复遍历的范围对象，不需要事先存下所有整数，也不是一次性迭代器。给循环变量重新赋值，不会改变来源下一次提供的值。

### 6.2 累积状态与追踪表

```python
total = 0
for x in range(1, 4):
    total += x
print(total)             # 6
```

| 轮次 | x | 更新前 total | 更新后 total |
|---:|---:|---:|---:|
| 1 | 1 | 0 | 1 |
| 2 | 2 | 1 | 3 |
| 3 | 3 | 3 | 6 |

这里 total 表示已处理数字之和，所以初始化必须在循环外。先定义状态含义，更新语句才有理由存在。

## 7. while：每次回到顶部重新判断

```python
x = 1
while x <= 3:
    print(x)             # 1、2、3
    x += 1
print(x)                 # 4：下一次判断为 False，循环退出
```

执行路线是“判断 → 为真进入 → 执行一轮 → 回顶部”。条件最初为假时一次都不执行。对这种靠条件终止的循环，要说明条件依赖哪些状态、每轮如何推进、为什么最终越过边界。

状态可以由循环体直接赋值，也可以由其中调用的函数间接修改；不是只能使用某一种更新语句。但写在循环后面的语句，不能帮助一个始终不退出的循环改变条件，因为程序还到不了那里。

### 7.1 break 与 continue

```python
x = 0
while True:
    x += 1
    if x == 4:
        break            # 退出最近一层循环，即使条件仍为 True
    if x == 2:
        continue         # 跳过本轮剩余语句，回到下一次判断
    print(x)             # 输出 1、3
print("end")             # end
```

所以“while 必须把条件变为 False 才能结束”并不准确。break 可以结束循环，函数内 return 可以结束函数，未处理异常也会中断正常路径。使用 continue 时要检查更新是否被跳过；有意持续运行的循环也需要取消或退出机制。

## 8. 函数：定义、调用、返回是三个时刻

```python
def add(a, b):
    result = a + b
    return result

first = add(2, 3)
second = add(10, 20)
print(first, second)      # 5 30
```

执行 def 时建立函数，还没有执行函数体。调用 add(2,3) 时，形参 a 接收实参 2，b 接收 3，局部变量 result 得到 5；return 把 5 交回调用位置，first 接住它，然后继续后面的语句。每次调用有自己的局部状态，result 不会自动出现在函数外。

### 8.1 print 不等于 return

```python
def show_double(x):
    print(x * 2)

def get_double(x):
    return x * 2

value = show_double(3)    # 函数内部打印 6
print(value)             # None：没有显式返回值
answer = get_double(3)   # 返回 6，本行不打印
print(answer + 1)        # 7
```

return 立即结束本次函数调用，print 只输出，函数还会继续。走到函数末尾或执行不带值的 return 都得到 None。判断缺少结果常写 `value is None`；is 比对象身份，不替代一般数值的 ==。

### 8.2 默认参数与提前返回

```python
def can_enter(age, minimum=18):
    if age < minimum:
        return False
    return True

assert can_enter(16) is False
assert can_enter(16, minimum=16) is True
```

这里 minimum 的默认值是整数。容器作为参数、原地修改、可变默认参数的陷阱在第 02 章结合对象操作学习。参数数量或名字不匹配会报 TypeError；return 不能出现在函数外。

`assert 条件` 是断言：为真就继续，为假抛 AssertionError。它用于本地测试，不替代生产输入校验，因为优化运行选项可能关闭断言。样例通过只证明覆盖到的行为，不是所有输入的证明。

## 9. 两层循环怎样衔接

```python
for i in range(3):
    for j in range(i + 1, 3):
        print(i, j)      # 依次输出 0 1、0 2、1 2
```

i=0 时，内层完整走完 j=1,2；再到 i=1，内层重新开始只取得 j=2；i=2 时内层为空。j 从 i+1 开始避免同位置和倒序重复配对。第 02 章学会列表按位置取值后，再用这个过程完成两数之和，而不是在这里提前要求容器知识。

## 10. Traceback：从异常位置追到错误状态的来源

下面是故意出错的完整程序，保存为 main.py 后运行。

<!-- run: {"error":"ZeroDivisionError"} -->
```python
count = 0
average = 10 / count
```

典型输出：

```text
Traceback (most recent call last):
  File "main.py", line 2, in <module>
    average = 10 / count
ZeroDivisionError: division by zero
```

第一行表示下面列调用轨迹，最近的一层在后面。`File` 后是文件路径，`line` 后是行号，`in <module>` 表示文件顶层；如果显示函数名，就是当时所在的函数。缩进的源码行帮你对照现场。末行冒号前是异常类型，后面是异常信息。不同版本可能增加箭头、波浪线、颜色，不影响基本读法。

先读发生了什么异常，再定位直接失败的表达式，最后恢复变量状态。本例 count=0 导致除零；抛错的位置不自动等于应该修改的位置。

### 10.1 多文件调用链

下面是一段用于读栈的日志示意，不是三份需要独立运行的源码：

```text
Traceback (most recent call last):
  File "main.py", line 8, in <module>
    run()
  File "service.py", line 12, in run
    average = calculate(10, 0)
  File "math_ops.py", line 3, in calculate
    return total / count
ZeroDivisionError: division by zero
```

从上往下是 main 调用 run，再调用 calculate；从下往上调查，是先发现 count 为零，再追问上游为什么传零。最下面可能是第三方库，也不能据此判断库有错。看完直接失败层之后，应检查自己与库之间的参数、输入契约和数据来源，不是机械地只改最后一个文件。

长日志出现 `During handling ...` 或 `direct cause ...` 时，可能有多个异常块。每块分别读，再理解前一个异常为何引出后一个，不能当成一条普通调用链。

### 10.2 异常类型告诉你从哪里查

| 类型 | 首先调查 |
|---|---|
| SyntaxError / IndentationError | 冒号、括号、缩进；语法错误不一定有完整运行调用栈 |
| NameError | 名字是否定义、拼写、作用域 |
| TypeError | 运算与类型是否匹配、函数参数是否传对 |
| ValueError | 类型可以接受，但内容是否合法，例如数字转换 |
| IndexError / KeyError | 下标或键是否存在；第 02 章结合容器学习 |
| AssertionError | 哪条预期不成立，实际值是什么 |

修复流程是复现最小失败、检查现场、修改、重跑失败用例和正常用例。不能把吞掉异常当成修好了问题。

## 11. 章节自测与验收

**任务：** 实现 sum_to(n)，返回 1 到非负整数 n 的总和，不使用 sum；n=3 返回 6，n=0 返回 0。先手工追踪，再写函数。

<details>
<summary>查看参考答案与验证</summary>

```python
def sum_to(n):
    total = 0
    for x in range(1, n + 1):
        total += x
    return total

assert sum_to(3) == 6
assert sum_to(0) == 0
assert sum_to(5) == 15
```

终点不包含，所以写 n+1；return 在循环外。若把 return 缩进循环内，n=3 第一次就返回 1，n=0 则没有进入循环，函数最终返回 None。

</details>

**口述自测：** 为什么循环变量会变？while True 为什么也能结束？屏幕出现 6 为什么不代表函数返回 6？

<details>
<summary>查看参考答案</summary>

for 每轮从来源取下一项并赋给循环变量。while 可以通过 break 或所在函数的 return 退出，异常也可能中止正常路径。print 产生输出，return 决定交给调用者的值，两者独立。

</details>

能预测变量追踪表、独立写并调用函数、区分打印与返回、从错误信息恢复关键状态后，再进入数据类型与容器。

语义依据：[Python 控制流](https://docs.python.org/3/tutorial/controlflow.html)、[内置函数](https://docs.python.org/3/library/functions.html)、[错误与异常](https://docs.python.org/3/tutorial/errors.html)。
