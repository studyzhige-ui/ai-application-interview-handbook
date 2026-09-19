# 04. 为什么 InnoDB 使用 B+Tree

`MYSQL-004` 在冻结 HUMAN-A 中有 **13 个独立来源**，是 MySQL 模块第二高频问题。

但面试里只回答：

> “B+Tree 是多叉平衡树，查询快。”

通常不够。

真正要解释的是：**数据库为什么需要一种“高扇出、低树高、有序、适合 Page I/O 和 Range Scan”的索引结构。**

---

## 1. 先从“磁盘 / Page 友好”理解

程序里的普通搜索树经常以“比较次数”为核心。

数据库还必须考虑：

```text
数据量很大
→ 不可能全部留在 CPU Cache / Heap
→ 数据按 Page 组织
→ 一次访问 Page 的成本远大于几个整数比较
```

所以数据库索引结构非常在意：

> **每访问一个节点，能否一次获得很多 Key，从而用很少的层级定位目标 Page。**

这就是“多叉”非常重要的原因。

---

# 2. 为什么普通 Binary Search Tree 不合适

二叉搜索树每个节点最多两个孩子：

```text
        50
       /  \
     20    80
    / \    / \
   10 30  70 90
```

理想平衡时查询大致是 `O(log₂N)`。

问题不是 Big-O 很差，而是：

> **分叉数太低，数据量极大时树可能很高。**

如果每一层都意味着需要访问另一个 Page，层级越多通常越不友好。

---

# 3. 红黑树为什么也不是数据库页索引的主选项

红黑树通过旋转等规则维持近似平衡，适合内存中的很多 Ordered Map 场景。

但它本质仍是二叉结构：

```text
一个节点
→ 最多两个孩子
```

数据库更希望一个 Page 节点里保存大量 Key / Child Pointer：

```text
             [10 | 20 | 35 | 50 | 80 | ...]
             /    |    |    |    \
            /     |    |    |     \
       child0 child1 ...             childN
```

这样一次 Page 读取可以做更多导航。

💡 **新手理解**：

> 红黑树擅长“内存对象级平衡”；B-tree/B+Tree 类结构更适合“一个节点就是一整页”的外存访问模型。

---

# 4. B-Tree 先是什么

B-Tree 是多路平衡搜索树。

一个节点可以放多个 Key：

```text
          [20 | 50]
          /   |   \
         /    |    \
 [5 10]   [30 40]   [60 70 90]
```

特点：

- 多叉；
- 保持平衡；
- 一个 Node 能容纳很多 Key；
- Tree Height 比二叉树低很多。

这已经非常适合数据库 / 文件系统。

---

# 5. B+Tree 与 B-Tree 的核心差异

面试里通常重点讲 B+Tree 的这几个特征：

## 5.1 非叶子节点主要用于导航

简化理解：

```text
Internal Node
→ Key + Child Pointer

Leaf Node
→ 真正的 Index Record
```

这样 Internal Node 不需要携带完整业务记录，可以容纳更多导航 Key，提高 Fan-out。

---

## 5.2 数据集中在 Leaf

例如：

```text
                  [30 | 60]
                /     |      \
               /      |       \
        [10 20]   [30 40 50]   [60 70 80]
           ↔           ↔            ↔
```

查一个具体 Key：

```text
Root
→ Internal Page
→ Leaf Page
```

---

## 5.3 Leaf Page 有序相连

这对 Range Query 很重要。

例如：

```sql
WHERE created_at >= '2026-09-01'
  AND created_at <  '2026-10-01'
```

B+Tree 可以先找到 Range Start，然后沿叶子页顺序扫描。

简化：

```text
找到 2026-09-01
       ↓
Leaf A ↔ Leaf B ↔ Leaf C ↔ ...
       顺序向后扫描
```

这比 Hash 结构天然更适合 Range。

---

# 6. 为什么“高扇出”非常关键

假设一个索引页能放很多：

```text
Key + Pointer
```

那么一个 Internal Page 就可以指向大量 Child Page。

抽象例子：

```text
Root:       1000 个 child
              ↓
Level 2: 1000 × 1000 个 child
              ↓
Leaf:     非常多的 records
```

这里不要死背“3 层能放多少千万行”这种固定数字，因为它受到：

- Key 长度；
- Primary Key 长度；
- Page Fill；
- Record Format；
- 数据类型；

影响。

真正应该记住的是：

> **Page 固定大小下，Internal Record 越小，Fan-out 越高，Tree Height 越低。**

这也解释了为什么“索引 Key 不要无脑做得很宽”有工程意义。

---

# 7. InnoDB Index Page

MySQL 8.4 官方文档说明：

- 除 Spatial Index 外，InnoDB Index 是 B-tree 数据结构；
- Index Record 存储在叶子 Page；
- 默认 Index Page Size 通常为 **16KB**。

学习时可以把一个树节点理解为：

```text
一个 InnoDB Page
```

因此：

```text
更高 Fan-out
→ 更低 Height
→ 更少层级 Page Access
```

⚠️ **不要推导成：树高 3 = 每次必然 3 次磁盘 I/O。**

Page 可能已经在 Buffer Pool 中，真实物理 I/O 取决于缓存状态和访问路径。

---

# 8. 为什么 B+Tree 比 Hash 更适合通用数据库 Index

对比：

| 能力 | B+Tree | Hash |
|---|---|---|
| Equal Lookup | ✅ | ✅，理想情况下很强 |
| Range Query | ✅ | ❌ 天然不擅长 |
| ORDER BY 利用顺序 | ✅ | ❌ |
| Prefix / Ordered Scan | ✅ | ❌ |
| 找相邻 Key | ✅ | ❌ |
| 通用 OLTP Index | 很适合 | 更偏特定 Equal Lookup |

例如：

```sql
SELECT id
FROM agent_runs
WHERE user_id = 10001
  AND created_at >= '2026-09-01'
ORDER BY created_at
LIMIT 20;
```

这里既有 Equal Prefix，又有 Range，又有 Order。

B+Tree 的有序结构天然适配这类访问。

---

# 9. 为什么 B+Tree 比 B-Tree 更常被用来解释 MySQL 索引

面试语境里常见回答：

```text
1. Internal Node 主要做导航
2. 同样 Page 可以放更多 Key / Pointer
3. Fan-out 高，树更矮
4. 数据集中在 Leaf
5. Leaf 有序链接，Range Scan 友好
```

这个回答方向是对的。

但需要谨慎：官方 MySQL 文档通常使用更宽泛的术语 **B-tree** 描述 InnoDB Index，而面试教材常进一步用 B+Tree 模型解释其叶子记录与页级有序扫描行为。

🎯 **更稳妥的表达**：

> InnoDB 官方把普通 Index 描述为 B-tree 数据结构；从其数据集中在叶子记录、页级有序结构和范围扫描行为看，面试中通常用 B+Tree 模型来解释。核心价值是高扇出、低树高、有序和 Range-friendly，而不是纠结术语字面。

---

# 10. Range Scan 是怎么发生的

假设 Index：

```sql
INDEX idx_created (created_at)
```

执行：

```sql
SELECT id, created_at
FROM agent_runs
WHERE created_at >= '2026-09-01 00:00:00'
  AND created_at <  '2026-09-02 00:00:00';
```

可以粗略理解：

```text
Root
  ↓
Internal Node
  ↓
定位第一个 >= 09-01 的 Leaf Record
  ↓
沿 Leaf Page 向后扫描
  ↓
直到 >= 09-02 停止
```

这就是“Index 有序”真正带来的价值之一。

---

# 11. 为什么随机插入可能导致 Page Split

如果新 Key 总是追加在右侧：

```text
1, 2, 3, 4, 5, 6, ...
```

写入位置更有局部性。

但如果 Primary Key 是完全随机值：

```text
918...
12...
700...
42...
```

新记录可能不断插到已有 B+Tree 中间位置。

当目标 Page 没有足够空间时，就可能需要 Page Split 等结构维护。

这会带来：

- 更多 Page 变动；
- 更差写局部性；
- Fragmentation；
- Buffer / Storage 压力。

这也是后面为什么会讨论：

> UUID / Random Primary Key 对 InnoDB Clustered Index 的影响。

但不要简单说“UUID 一定不能做主键”。真正结论要结合：

- UUID 形式；
- 是否有时间有序版本；
- 写吞吐；
- 分布式 ID 需求；
- Secondary Index 大小；
- 数据规模。

---

# 12. B+Tree 是“始终完美满页”吗

不是。

实际 B-tree Page 会有：

- Free Space；
- Split；
- Merge；
- 删除标记；
- Page Fill 差异。

所以不要把教科书中每个节点恰好塞满的图当作真实磁盘布局。

图是为了理解：

```text
有序
多叉
平衡
Page-oriented
Leaf Scan
```

---

# 13. 为什么主键长度会影响整个索引体系

这个问题在下一章会完整解释，这里先给结论。

InnoDB Secondary Index Leaf Record 会保存对应的 Primary Key。

于是：

```text
Primary Key 很宽
  ↓
每个 Secondary Index Record 也更宽
  ↓
一个 Page 能放的记录减少
  ↓
Index Size 增大
  ↓
Cache / I/O / Tree Fan-out 都可能受影响
```

所以主键设计不仅影响 Primary Index 自己。

---

# 14. 一道常见对比题

## B+Tree vs 红黑树

🎯 可以回答：

> 两者都能提供有序查找，但红黑树是二叉结构，更适合内存中的节点级数据结构；数据库按 Page 访问外存，B+Tree 类多路树一个节点能容纳大量 Key 和 Child Pointer，Fan-out 高、树高低，可以减少层级 Page Access，而且叶子有序，Range Scan 很自然，因此更适合通用数据库 Index。

## B+Tree vs Hash

> Hash 对等值定位很强，但没有天然排序，Range、ORDER BY 和有序扫描很弱；数据库查询大量存在范围和排序，因此 B+Tree 更通用。

## B+Tree vs B-Tree

> 面试中重点是 B+Tree 把真实索引记录集中在 Leaf，Internal Node 主要承担导航，因此同样 Page 可以保持较高 Fan-out；叶子有序相连也更适合范围扫描。

---

# 15. 面试官继续追问什么

🔍 **为什么 B+Tree 通常只有很少层？**  
从 Page Size、Internal Record 大小、Fan-out 回答，不背固定“3 层存 2000 万”。

🔍 **B+Tree 查询复杂度是多少？**  
可以从 `O(log_m N)` 抽象回答，但立即补充真实数据库性能由 Page Access、Buffer Pool、返回规模和回表决定。

🔍 **为什么叶子链表对范围查询有用？**  
找到 Lower Bound 后可以沿有序 Leaf 顺序扫描，不需要每个 Record 都重新从 Root 查。

🔍 **随机主键为什么不好？**  
继续进入 Clustered Index、Page Split、写局部性和 Secondary Index Primary Key Storage。

---

# 16. 高频易错点

⚠️ **B+Tree 的所有非叶子节点“完全不存数据”**  
面试里最好说“Internal Node 主要保存导航 Key / Pointer，真正 Index Record 集中在 Leaf”，避免把教学模型说成所有实现细节的绝对表述。

⚠️ **树高就是磁盘 I/O 次数**  
忽略 Buffer Pool。

⚠️ **Hash 查询 O(1)，所以一定比 B+Tree 好**  
忽略 Range / Order / Collision / Storage Access。

⚠️ **随机主键一定导致每次 Page Split**  
不是每次，只是更容易破坏插入局部性，并在目标 Page 空间不足时触发结构调整。

---

# 17. 本章自测

<details>
<summary>1. 数据库为什么比内存 Map 更关心树的 Fan-out？</summary>

因为数据库以 Page 为核心组织数据；一个 Page 能容纳更多导航 Key，就能指向更多 Child Page，降低 Tree Height，减少需要跨层访问的 Page 数量。

</details>

<details>
<summary>2. B+Tree 为什么适合范围查询？</summary>

它保持 Key 有序；找到范围起点后，可以沿有序叶子页持续扫描，直到超过范围终点。

</details>

<details>
<summary>3. 为什么不能说“三层 B+Tree 就是三次磁盘 I/O”？</summary>

因为索引 Page 可能已经缓存在 InnoDB Buffer Pool 中。树高代表逻辑访问层级，不等价于每层一定触发物理存储读取。

</details>

<details>
<summary>4. 为什么 Primary Key 的宽度会影响 Secondary Index？</summary>

因为 InnoDB Secondary Index Leaf Record 包含对应 Primary Key。主键越宽，Secondary Index Record 越大，整体 Index Size 和缓存压力也可能越大。

</details>

---

# 18. 官方资料

- MySQL 8.4 — InnoDB Index Physical Structure  
  <https://dev.mysql.com/doc/refman/8.4/en/innodb-physical-structure.html>
- MySQL 8.4 — InnoDB Indexes  
  <https://dev.mysql.com/doc/refman/8.4/en/innodb-indexes.html>
- MySQL 8.4 — Comparison of B-Tree and Hash Indexes  
  <https://dev.mysql.com/doc/refman/8.4/en/index-btree-hash.html>

下一章会把 B+Tree 从“抽象树”落到 InnoDB 最关键的数据组织：

> **Clustered Index 与 Secondary Index。**
