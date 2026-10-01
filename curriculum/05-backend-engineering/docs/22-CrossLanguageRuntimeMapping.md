# 把通用机制映射到 Java、Spring 与 Go

[← 配置和版本怎样安全改变](21-ConfigRelease与ServiceEvolution.md) · [模块主页](../README.md)

你已经知道连接为什么要释放、共享状态为什么要保护、任务为什么不能只放内存。换成 Java、Spring 或 Go，问题仍然存在，只是由不同组件完成。学习迁移先认出同一个问题，再确认实现哪里不同。

本章固定采用 **Java SE 21 API、Spring Framework 7.0 文档与 Go 1.26 语境** ，不把它们统称为最新版本，也不把 Python 实验冒充 Java/Go 验证。它是按岗位选择的生态分支，不是通用 Backend 主线的隐藏前置。

<a id="11-用问题对齐生态而不是用名字替换"></a>

## 1. 先选要迁移的问题，再选语言分支

| 通用问题 | Python / FastAPI 常见载体 | Java / Spring 常见载体 | Go 常见载体 |
|---|---|---|---|
| 谁创建和关闭依赖 | 显式装配、依赖与 Lifespan | Bean 容器、作用域 | 显式启动与关闭 |
| 谁保存请求上下文 | contextvars、依赖作用域 | ThreadLocal、请求作用域 | context.Context |
| 谁协调共享修改 | 锁、信号量、队列 | monitor、Lock、并发集合 | Mutex、Channel 等 |
| 谁执行并发工作 | 事件循环、线程或进程池 | 线程及执行框架 | goroutine 与运行时 |
| 谁回收内存 | 具体 Python 实现 | JVM 回收器 | Go 回收器 |

这些是问题的对应，不是 API 等价表。每一行都要继续问作用域、阻塞、取消、清理和进程退出后剩下什么。

目标是 Java/Spring 时读[第 2 节](#java-path)，按依赖、共享修改、上下文与内存推进；目标是 Go 时读[第 3 节](#go-path)，先理解调度，再看通道与取消。暂未使用的生态可留作查询，不要求一次记住所有名称。

<a id="java-path"></a>

## 2. Java / Spring：从受管理对象到线程与内存

<a id="1-依赖注入管理的是对象关系与生命周期"></a>

### 2.1 依赖注入：谁创建、交付和关闭对象

**Dependency Injection（依赖注入）** 让组件声明所需对象，由外部提供实例，而不是每个方法临时创建。Spring 管理的对象称为 **Bean** ，容器负责按定义创建、注入，并在相应阶段初始化或销毁。[Spring IoC 容器](https://docs.spring.io/spring-framework/reference/core/beans.html)

例如文档服务需要数据库客户端：若它服务整个应用，应在使用前初始化，在应用结束时关闭；若某个字段存的是每次请求的用户，就不能不加区分地放入所有请求共享的单例。

Spring singleton 是容器中的单例作用域，不是全世界只能有一个对象，也不自动线程安全。prototype 等作用域的销毁责任不同，持有资源的一方需核对生命周期。[Bean 作用域](https://docs.spring.io/spring-framework/reference/core/beans/factory-scopes.html)

可先理解为定义、实例化、注入、初始化和相应后处理，再交付使用；代理和回调的精确时序取决于处理器。A 需要 B、B 又需要尚未建好的 A 时形成循环依赖，应先检查职责，而不是因框架可处理部分情况就主动制造循环。

<a id="2-aop-的效果取决于调用是否经过代理"></a>

### 2.2 AOP：这次调用有没有经过代理

**AOP（面向切面编程）** 把事务、日志等共同逻辑放在方法调用边界。Spring 常用代理拦截：调用先进入代理，再到真实目标。

```text
外部调用者 → 代理（例如开启事务）→ 目标方法
目标 this.otherMethod() → 目标自身，不重新经过该代理
```

同对象自调用可能绕过期望的事务、重试或日志增强。结论针对代理模式，字节码织入等机制不能直接套用。可让职责清晰的另一组件经受管理代理调用，或显式组织事务，不宜到处读取代理上下文。[代理与自调用](https://docs.spring.io/spring-framework/reference/core/aop/proxying.html)

FastAPI 依赖、装饰器、中间件与 AOP 可以解决部分相似问题，进入位置和生命周期仍需分别确认。

<a id="3-互斥可重入与-cas-如何保护状态"></a>

### 2.3 共享修改：保护一整次状态转换

两个线程都读余额 10，再各减 1 写成 9，会丢失一次修改。需保护“读、判断、写”的组合，不只保护某个字段访问。

Java `synchronized` 使用监视器语义提供互斥与相应可见性；`ReentrantLock` 是显式锁 API，还提供可中断获取、条件等待等控制。 **可重入** 表示同一线程持锁时可再次进入，按匹配次数释放，不允许其他线程同时进入。[ReentrantLock](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/ReentrantLock.html)

成功拿锁后应在 `finally` 中释放；持锁调用慢服务会扩大等待，多把锁还需一致获取顺序等规则避免死锁。

**CAS（Compare-And-Set，比较并设置）** 把预期值检查和更新合成原子操作。预期 10，别人先改成 9，CAS 应失败并重新判断。它仍有竞争和重试成本；A 变 B 又变 A 时，仅比较值看不见中间变化，必要时增加版本等机制。

<a id="4-aqs-组织等待不替你决定业务条件"></a>

<details>
<summary>追到同步器实现时再看：AQS 怎样组织等待</summary>

**AbstractQueuedSynchronizer（AQS，抽象队列同步器）** 提供同步状态、等待队列和获取/释放框架。实现者定义什么状态可以获取，框架协助排队、阻塞和唤醒。[AQS API](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/locks/AbstractQueuedSynchronizer.html)

锁可用状态表达占用，信号量可表达剩余许可，含义不同但都要协调竞争。队列不保证业务状态正确，使用 CAS 也不表示绝无阻塞。公平、取消和中断按具体同步器核对；这里不要求先实现一个 AQS 同步器才理解互斥。

</details>

<a id="5-哈希映射快速定位不等于没有冲突"></a>

### 2.4 哈希容器：单次原子与多步原子不同

`HashMap` 用哈希定位桶，冲突后仍需比较键。装载程度上升会影响查找，扩容重新分配位置，以空间换较低冲突；某些桶可用树形结构改善严重冲突。平均接近常数时间有条件，不是所有输入都无条件 O(1)。[HashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/HashMap.html)

Java 的桶、链表、树化不是 Python dict 的实现说明，具体阈值也不属于跨语言不变量。

`ConcurrentHashMap` 支持并发，但 `containsKey` 后 `put` 是两个操作，中间可被其他线程改变。按需要选 `putIfAbsent`、`compute` 等相应原子操作；修改映射再发外部通知，仍跨越更大业务边界。[ConcurrentHashMap](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/util/concurrent/ConcurrentHashMap.html)

不要把早期 Segment 数量套用所有版本，也不能把某时刻的 size 当多步决策已锁定。

<a id="6-threadlocal-的寿命是线程不是一次请求"></a>

### 2.5 ThreadLocal：线程复用后是谁的上下文

**ThreadLocal（线程局部变量）** 让每个线程保存独立值。线程 T 处理 Alice 后没清理，随后处理 Bob，就可能仍读到 Alice 的身份。[ThreadLocal](https://docs.oracle.com/en/java/javase/21/docs/api/java.base/java/lang/ThreadLocal.html)

下面是连续片段，不是完整 Java 程序；`currentUser` 已声明为 ThreadLocal，`handle` 是业务方法：

```java
currentUser.set(user);
try {
    handle();
} finally {
    currentUser.remove();
}
```

清理的是该线程保存的引用，不是销毁 user 的全部引用；异常也要清理。换线程执行时，还要明确捕获、安装和恢复规则。Python contextvars、Go context 可承载部分相似职责，但不自动等价。

<a id="7-jvm-内存区域决定到哪里找-oom"></a>

### 2.6 JVM：内存不足先定位区域

**JVM（Java 虚拟机）** 执行字节码并管理运行数据。堆主要承载对象，每线程栈保存调用帧和局部执行状态；类元数据另有存放区域，HotSpot 的 **Metaspace（元空间）** 是相关实现。直接缓冲、原生内存和线程栈也占进程资源。[JVM 运行数据区](https://docs.oracle.com/javase/specs/jvms/se21/html/jvms-2.html)

类需经过加载、相应连接与初始化；对象创建还涉及分配、默认初始化和构造逻辑。语言对象模型、 **JIT（即时编译）** 优化后的实际分配及操作系统 RSS 不应混成同一层。

因此 OOM 不只代表堆满，StackOverflow（栈溢出）也不是所有内存不足的通用名称。应根据错误区域检查存活对象、分配速率、直接内存、线程数和容器限制。

<a id="8-gc-回收不可达对象不撤销业务引用"></a>

### 2.7 GC：业务用完，不等于对象不可达

**GC（垃圾回收）** 依据可达性等规则识别可回收对象，再组织回收、搬移或压缩。对象仍被全局缓存或线程上下文引用，即使业务不再需要，也可能无法回收。

回收器在吞吐、暂停、内存与并发工作间取舍。ZGC 面向低延迟，但不是零成本或零暂停，也不能修复无限保存引用。分代能力与默认行为需按 JDK 版本确认，不应沿用“ZGC 永远不分代”。[OpenJDK ZGC](https://wiki.openjdk.org/spaces/zgc/pages/34668579/Main)

排障把 GC 日志与请求延迟、分配率、堆和容器内存对齐。Heap Dump（堆转储）查看对象引用，线程转储查看等待，Profiler（剖析器）定位分配或执行热点。采集可能暂停程序、占磁盘或泄露数据，应控制范围。

<a id="go-path"></a>

## 3. Go：从调度资源到通信与取消

<a id="9-go-的-gmp-分别是什么"></a>

### 3.1 G、M、P 分别承担什么

**Goroutine** 是 Go 运行时调度的并发执行单元。G 表示它及相关状态；M 是操作系统线程；P 是执行 Go 代码需要的调度资源。调度器把可运行 G 交给持有 P 的 M，并用本地、全局队列等组织工作。[运行时开发说明](https://go.dev/src/runtime/HACKING)

网络等待期间可让其他任务继续。某些阻塞系统调用会占住 M，运行时可安排其他线程接手执行资源。因此 `GOMAXPROCS` 约束 Go 代码并行执行资源，不是操作系统线程总数上限。[Go runtime](https://pkg.go.dev/runtime)

相应现代版本的默认行为会考虑 CPU 亲和性和 Linux cgroup 配额，并可能动态调整；显式配置及兼容选项会改变行为，不能永远当作宿主 CPU 数。

Python asyncio 通常在事件循环线程经 await 协作挂起，Go 可把 goroutine 调度到多个线程并行。两者都消耗内存与下游资源，轻量不等于可无限创建。

<a id="10-channel-和-context-不提供分布式任务持久性"></a>

### 3.2 Channel 与 context：协调并不等于持久

**Channel（通道）** 在 goroutine 之间传值并同步。无缓冲通道的发送需有接收方配合；有缓冲通道满后也会等。关闭表示不再发送，向已关闭通道发送会 panic；接收方可在缓冲耗尽后通过返回状态识别关闭。[通道规范](https://go.dev/ref/spec#Channel_types)

共享计数器可用 Mutex（互斥锁），流水线和所有权交接可用通道，不能说通道天然比锁高级。Channel 也不是持久 MQ，进程退出后不能把缓冲内容当 Kafka 日志重放。

`context.Context` 传递截止、取消和请求相关值。取消需要操作方观察并配合退出；创建派生 context 后，应按 API 约定调用取消函数释放资源。它不能强制杀死 goroutine 或撤销远端副作用。[Go context](https://pkg.go.dev/context)

## 本章小结

先保持工程问题不变，再按所用语言核对实现。Spring 管对象与调用边界，Java 同步、容器和上下文各有范围；JVM 回收不能解除业务引用。Go 调度器分配执行资源，通道与 context 协调进程内工作，不替代任务持久化。

## 🎯 面试怎么答

**Spring 同对象自调用为什么可能使事务增强失效？**

> 在代理模式下，增强由经过代理的调用触发。this.otherMethod() 直接调用目标自身，不会重新经过该代理。应明确组件与事务边界，让需要增强的调用走受管理代理；这个结论不机械套用其他织入机制。

**Python asyncio 与 Go goroutine 有什么区别？**

> asyncio 通常在事件循环线程协作挂起，阻塞调用会占住该线程；Go 运行时通过 G/M/P 将 goroutine 调度到线程，可以并行。两者仍需资源限额与取消配合，进程内任务也不能直接当作持久队列。

## ⚠️ 易错点

> ⚠️ 名称和用途相似，不表示作用域、传播与清理规则相同。

> ⚠️ 并发容器单次操作原子，不代表组合操作或外部副作用也原子。

> ⚠️ GOMAXPROCS 不是线程总数上限，Channel 不是持久消息系统。

## 本章自测

按已选语言分支作答；Java/Spring 看 1、2，Go 看 3。

### 1. Java：线程 T 处理 Alice 时设置 ThreadLocal，异常后没 remove，随后处理 Bob。风险与修复在哪？

<details>
<summary>参考答案与解释</summary>

可能把 Alice 上下文带给 Bob，产生错误权限与引用保留。原任务 finally 中清理；跨线程另设传播和恢复规则，不能依赖碰巧换线程。

</details>

### 2. Java：用 putIfAbsent 代替 containsKey 后 put，能顺便保证之后的邮件只发一次吗？

<details>
<summary>参考答案与解释</summary>

不能。容器争抢与邮件是两个边界，进程重启和外部结果未知仍需持久幂等、查询或核对协议。

</details>

### 3. Go：取消 context 后，goroutine 仍在调用外部服务，可以立刻登记“对方没有执行”吗？

<details>
<summary>参考答案与解释</summary>

不能。取消是通知，需要被调用方配合；即使本地退出，远端也可能已执行。副作用仍按稳定操作身份核对。

</details>

## 知识回看与权威资料

- [并发与 Future](05-Concurrency与ThreadPool.md)：先理解执行、等待、终结，再比较不同运行时。
- [Linux 资源诊断](19-LinuxTroubleshooting.md)：把运行时对象和堆，与整个进程的资源占用区分。
- [技术资料索引](../../../references/backend-engineering/README.md)：按目标语言进入官方 API，不把概念映射当成已完成语言实作。
