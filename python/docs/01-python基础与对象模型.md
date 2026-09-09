# 01. Python 基础与对象模型

## 1. 先理解一个核心：Python 里的“变量”更像标签

💡 **新手理解**：Python 变量不是一个固定的盒子，而更像“贴在对象上的名字”。

```python
a = 10
b = a
```

这里可以理解为：整数对象 `10` 被名字 `a` 引用，随后 `b` 也引用同一个对象。

```python
a = [1, 2]
b = a
b.append(3)
print(a)  # [1, 2, 3]
```

原因不是“b 把值传回给 a”，而是 `a` 和 `b` 本来就引用同一个列表对象。

## 2. 对象的三个重要属性

在面试中可以把 Python 对象理解为有三类核心信息：

| 属性 | 含义 | 常用方式 |
|---|---|---|
| identity | 对象身份，是否为同一个对象 | `id(obj)`、`is` |
| type | 对象类型 | `type(obj)`、`isinstance()` |
| value | 对象所表示的值 | `==` 常用于比较 |

```python
a = [1, 2]
b = [1, 2]

print(a == b)  # True：值相等
print(a is b)  # False：不是同一个对象
```

⚠️ `is` 的准确说法是比较**对象身份**，而不是简单背成“比较内存地址”。`id()` 在 CPython 中通常与内存地址有关，但“identity”才是语言层面更准确的概念。

## 3. 动态类型

Python 是动态类型语言：**类型属于对象，不属于变量名本身。**

```python
x = 10
x = "hello"
x = [1, 2, 3]
```

同一个变量名可以先后引用不同类型的对象。

这不等于“Python 没有类型”。恰恰相反，每个对象都有明确的类型，只是变量不需要提前声明类型。

## 4. 常见基本类型

```python
age = 22            # int
price = 9.9         # float
name = "Tom"        # str
ok = True           # bool
nothing = None      # NoneType
```

查看类型：

```python
print(type(age))
print(isinstance(age, int))
```

通常在真实代码中，判断类型更推荐 `isinstance()`，因为它考虑继承关系。

## 5. 真值判断 Truthy / Falsy

Python 中很多对象都可以直接放进 `if`。

常见假值：

- `False`
- `None`
- 数字 `0`、`0.0`
- 空字符串 `""`
- 空容器 `[]`、`()`, `{}`, `set()`

```python
items = []
if not items:
    print("列表为空")
```

比 `if len(items) == 0:` 更 Pythonic。

## 6. `None` 应该怎么比较

推荐：

```python
if value is None:
    ...
```

不推荐：

```python
if value == None:
    ...
```

因为 `None` 是单例对象，判断对象身份更清晰，也符合 Python 风格。

## 7. 序列的索引与切片

字符串、列表、元组等都支持索引。

```python
nums = [10, 20, 30, 40, 50]
print(nums[0])      # 10
print(nums[-1])     # 50
print(nums[1:4])    # [20, 30, 40]
print(nums[::-1])   # 反转
```

切片基本格式：

```text
sequence[start:stop:step]
```

- `start`：包含
- `stop`：不包含
- `step`：步长

## 8. 解包

```python
a, b = 1, 2

a, b = b, a  # Python 中交换变量
```

扩展解包：

```python
first, *middle, last = [1, 2, 3, 4, 5]
print(first)   # 1
print(middle)  # [2, 3, 4]
print(last)    # 5
```

## 9. 面试怎么答：Python 是动态类型还是强类型？

🎯 **推荐回答**：

Python 是**动态类型、强类型**语言。动态类型指变量不需要提前声明类型，变量名可以在运行过程中引用不同类型对象；强类型指 Python 不会随意在不兼容类型之间进行隐式转换，例如字符串和整数不能直接相加。

```python
"1" + 1  # TypeError
```

## 10. 本章高频追问

1. 变量、对象、引用分别是什么？
2. `type()` 和 `isinstance()` 有什么区别？
3. `is` 和 `==` 有什么区别？
4. 为什么判断 `None` 推荐用 `is`？
5. Python 为什么说是动态类型但又是强类型？
6. `a = b` 是复制对象吗？

下一章：[02. 核心数据类型与容器](02-核心数据类型与容器.md)
