# 17. Tombstone、Compaction 与 Index Maintenance

上一章知道了 Delete / Update 可能不会立即重写整个 ANN Index，这一章继续回答：

> **那些已经失效、删除、被替换的向量，最后怎么真正清掉？索引为什么需要维护？**

---

## 1. Tombstone 是什么

一种常见思路：

```text
Delete Request
→ 标记 deleted / tombstone
→ Query 跳过
→ 后台再做物理清理
```

好处：

```text
前台 Delete 快
不必每次重构大索引
```

代价：

```text
旧数据暂时仍占空间
Index 内可能积累无效节点
```

---

# 2. 为什么不能无限积累 Tombstone

假设：

```text
总 1 亿条
其中 3000 万已 tombstone
```

即使 Query 不返回它们，仍可能造成：

```text
存储浪费
内存浪费
ANN 导航遇到无效节点
Segment 变碎
Compaction Debt
```

所以系统需要 Maintenance。

---

# 3. Compaction 在做什么

可以把 Compaction 理解成：

```text
把有效数据重新整理
→ 丢掉 tombstone / stale version
→ 合并小 segment
→ 回收空间
→ 生成更干净的索引结构
```

不同产品实现差异很大，但核心目标类似：

> **把在线增删改造成的碎片重新整理。**

---

# 4. Segment 是什么

许多 Vector DB 不会把所有数据看成一个无限大的单文件索引，而会形成：

```text
Segment 1
Segment 2
Segment 3
...
```

新写入可能先进入：

```text
mutable / growing segment
```

达到一定条件后：

```text
seal / build index
```

后台再合并和整理。

具体术语依产品而异，但“分段写入 + 后台索引维护”是很常见的存储引擎思想。

---

# 5. Compaction 为什么可能影响性能

Compaction 会消耗：

```text
CPU
Disk I/O
Memory
Network
Index Build Resource
```

如果后台任务太激进：

```text
Query P99 抖动
写入变慢
```

如果太保守：

```text
空间膨胀
旧版本堆积
查询路径变长
```

所以它是典型 Background Maintenance Trade-off。

---

# 6. Index Maintenance 不只等于 Compaction

Production 还可能需要：

```text
Rebuild
Rebalance
Replica Repair
Segment Merge
Statistics Refresh
Index Warmup
Cache Warmup
```

这些任务都应该：

```text
可观测
可限速
可取消 / 重试
可判断进度
```

它们和 AI Backend Engineering 中的长任务治理思想相通。

---

# 7. 更新频率会影响 Index 选择

如果数据：

```text
几乎静态
```

可以接受：

```text
昂贵离线 Build
```

如果：

```text
每秒大量 Upsert / Delete
```

就必须关心：

```text
Mutable Index Capability
Compaction Cost
Rebuild Frequency
Write Amplification
```

这也是 Index Selection 的重要输入。

---

# 8. “Deleted” 与“不可检索”要区分

用户要求删除数据时，通常希望：

```text
立刻不可查询
```

但物理空间回收可以晚一些。

因此可以区分：

```text
Logical Visibility Boundary
vs
Physical Reclamation Boundary
```

对于安全 / 合规删除，还要确保：

```text
Replica
Backup
Cache
Old Index Generation
```

都在生命周期设计中被处理。

---

# 9. 怎样监控 Maintenance Debt

可以关注：

```text
Deleted Ratio
Stale Version Count
Segment Count
Small Segment Count
Index Build Queue
Compaction Queue
Disk Amplification
Memory Growth
Query Latency Drift
```

如果数据量没变，但：

```text
Index Size 一直涨
P99 一直变差
```

就应该检查 Maintenance。

---

# 10. 面试怎么答

## Q：Vector DB 删除数据后为什么还需要 Compaction？

🎯 **建议回答**：

> ANN Index 维护成本较高，所以 Delete 常先以 logical tombstone 让记录立即不可见，再由后台 compaction / rebuild 真正清理无效节点和旧版本。这样前台删除更快，但如果 tombstone 长期堆积，会带来存储、内存和查询开销，因此要监控 deleted ratio、segment 数、compaction queue 和 index size，并在后台资源与前台 SLA 之间做平衡。

---

# 11. 高频易错点

⚠️ **Logical Delete 和 Physical Reclaim 是同一时刻。** 不一定。

⚠️ **Compaction 只是节省磁盘，不影响 Query。** 索引碎片和无效节点也可能影响查询。

⚠️ **Vector DB 是只读索引，不需要后台维护。** Production 显然不是。

---

# 12. 本章自测

<details><summary>1. Tombstone 的价值是什么？</summary>

先快速让记录逻辑不可见，避免每次删除都同步重构大型 ANN Index，把昂贵物理清理延迟到后台完成。
</details>

<details><summary>2. 为什么 Compaction 不能无限激进？</summary>

因为它会消耗 CPU、I/O、内存和索引构建资源，可能影响前台 Query / Write 的 P99 SLA。
</details>