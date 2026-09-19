# Python Reader Revision｜读者可理解性与课程重组记录

[← Project Records](README.md) · [← Python Foundation](../../curriculum/01-python/README.md) · [↑ Handbook](../../README.md)

> 本文件记录 Python Foundation 的历史重组、知识点迁移与验证范围。它用于保留项目演进证据，不作为 Python 模块的正式入口定义。

## 知识点迁移索引

本轮重组的是教学顺序，不以减少知识点换取篇幅。以下按旧主题给出新的主责位置；同一机制在应用处可以简要回顾，完整解释仍集中维护。

| 原有主题 | 新版主责位置与处理 |
|---|---|
| 对象身份、动态／强类型、type／isinstance、真值／None、索引／切片／解包、语言选型 | 01：先定义与代码入门，再比较与取值，最后语言选型；原有 AI／Java／Go 取舍保留 |
| list／tuple／str、append／extend、hash／equality、dict 碰撞／删除／扩容、set、切片成本 | 02：序列 → 哈希前置知识 → dict 完整机制 → set → 切片与选型 |
| 可变性、赋值、浅／深拷贝、函数共享传参、可变默认参数 | 03：统一通过对象引用图推导；补充深拷贝共享关系与重复行列表 |
| 函数对象、参数、星号、仅位置／仅关键字、默认值、LEGB、global／nonlocal、闭包 | 04：从一次调用开始，作用域与晚绑定有独立正反实验 |
| lambda、各类推导式、enumerate／zip、sorted／sort、map／filter／reduce、any／all、极值 | 05：按处理任务分组；补求值时机、输入形状与空输入边界 |
| 可迭代对象、迭代器协议、for、生成器、yield、惰性与耗尽、手写 Counter | 06 讲使用与机制；Counter 的完整类实现移到 08，不删除 |
| 装饰器参数／叠加／wraps、计时、with、contextmanager、手写 MyContext | 07 讲函数包装与生命周期；MyContext 的完整类实现移到 08，不删除 |
| 类／实例／self、四类面向对象思想、属性／方法、new／init、MRO、property、slots、Duck Typing／Protocol／ABC／可替换性、魔术方法 | 08：先对象基础，再行为契约，再实际实现迭代与资源协议 |
| 异常结构、raise／因果链、自定义异常、assert、文件、文本／字节、大文件、pathlib、模块／包／main／import／循环导入 | 09：按失败处理 → 资源操作 → 模块生命周期组织；修正导入初始化顺序 |
| JSON、结构／业务校验、TypedDict／dataclass／Pydantic、修复／重试／拒绝、eval 风险、SearchPlan | 10：按信任边界分层；保留原示例主题，补严格校验、错误分类与资源边界 |
| 引用计数、del、循环 GC、可达性、业务内存增长、GIL、I/O／CPU／本地库、线程安全 | 11：区分语言、实现、业务三层；补充自由线程构建的适用前提 |
| Thread／Process／Coroutine、Lock／RLock／Semaphore、事件循环、await／Task、gather／as_completed、超时／取消／fallback、线程池／进程池、可靠任务边界 | 12：先执行模型，再同步与容量，再结果与退出；聚合示例补等待取消收尾 |
| 复杂度、动态数组、链表、栈／队列、哈希表、树／BST、遍历、堆与 Top K、AI 应用选择 | 13：从操作需要推导结构；补全 BFS 子节点入队与 Top K 边界 |


## 修订验证范围

**本轮完成范围：** 重写 `docs/01–13` 的教学结构、正文、例子与衔接，同步模块主页和 Review 入口；原有章节路径、集中复习与面试资料入口保留。没有新增一套与正文并行的“新版补充教材”。

**知识与形式：** 原有主题按上面的索引保留或迁移；37 道原有章末自测保留，继续默认折叠。🎯 回答保持可见，⚠️ 后补正确解释。章节编号随正文分组调整，不沿用旧的小节编号制造错觉。

**代码核验：** 在 CPython 3.13.5、Pydantic 2.13.4 环境对代表性示例做了 27 组检查，包含引用／拷贝、闭包、装饰器、上下文清理、模块缓存、结构校验、DFS／BFS、Top K 等；另外检查聚合的早停、超时、单源失败、空输入、并发上限、外部取消，并验证 spawn 方式的进程入口与进程池桥接。Top K 还与排序结果进行了 200 组随机输入对照。

这些检查不是全部教学代码逐段执行，也不构成跨所有 Python 版本／平台的证明；模拟取消与清理不等于对真实下游服务副作用的保证。

**仍待验收：** 初学者连续阅读时是否还存在术语跳跃、隐含前提、解释不足或重复负担，需要实际再次通读验证。本页不将这一项预先标为完成。

> 正式课程结构、学习顺序和模块边界以 [Python Foundation README](../../curriculum/01-python/README.md) 为准。
