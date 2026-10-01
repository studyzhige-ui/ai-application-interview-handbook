# FastAPI｜Review总图与综合自测

[← 模块主页](../README.md) · [面试题](../interview/高频面试题.md) · [练习](../examples/README.md)

这一页用于第二遍。先遮住答案，画出请求与资源的路线；哪里说不清，再回对应正文。不要把短答案当作首次学习的完整解释。

## 总图1｜从请求到响应

```text
客户端 → ASGI服务器 → 应用中间件与路由
                         ↓
                   输入和依赖边界
                         ↓
                    业务服务/适配
                         ↓
                     输出与发送
```

指出FastAPI、Uvicorn、Starlette、Pydantic各自的职责。再找出一条422路径、一条权限拒绝路径和一条下游失败路径。

## 总图2｜资源什么时候结束

```text
应用启动：创建共享客户端/资源
  │
  ├─ 请求A：取得依赖 → 调用处理函数 → 发送响应 → 对应清理
  ├─ 请求B：取得依赖 → 拒绝/异常 → 对应清理
  │
应用退出：平台与服务器协调停止工作，关闭共享资源
```

在图中单独标出function与request作用域。不要把函数返回、响应体发完和客户端显示当成同一时刻。

## 总图3｜同步、异步与容量

```text
框架调用同步路由/依赖 → 线程执行
框架调用async路由    → 事件循环推进
async中直接调用同步函数 → 不会自动转交

在途限制 + 有界输入/队列 + 下游容量 + 等待预算
```

能解释为什么两个Semaphore许可不等于每秒两次请求，也不等于所有worker合计最多两次。

## 总图4｜事件、任务与连接

```text
短请求：一个请求 → 一个结果
流式交付：开始 → 内容/进度 → 成功或失败终态
双向交互：建立连接 ↔ 消息 ↔ 消息 → 断开清理
持久任务：接受 → 状态记录 → 独立执行 → 查询/事件/取消
```

流断开、任务取消与执行停止分开验证。知道事件ID不足以自动恢复，202不足以自动持久。

## 总图5｜诊断与部署

```text
定位慢：排队 → 连接 → 下游 → 发送 → 客户端
部署：实例 × worker × 每进程资源
退出：停止接流量 → 有限等待/取消 → 关闭资源
```

说明日志、指标、Trace分别解决什么；不要用每请求ID作为无限标签，不让每次健康检查真实调用全部外部服务。

## 综合自测

按课程主题重建规则和判断依据，包括为什么选择某种通信方式、失败后保留什么状态。具体实现对照可以稍后重做；题目中的场景判断不是可省略的边界。

<details>
<summary>1. FastAPI、Starlette、Uvicorn、Pydantic分别做什么？</summary>

Uvicorn承接网络并调用ASGI应用；Starlette提供Web基础；FastAPI组织类型驱动的路由、依赖、契约与文档；Pydantic校验和序列化数据。

回看：[01｜从一个可访问的接口理解请求与响应](../docs/01-FastAPI职责与ASGI请求链路.md)。

</details>

<details>
<summary>2. ASGI是什么？</summary>

服务器与应用之间的接口规范，通过scope、receive、send以及生命周期事件表达交互；它不是asyncio的别名。

回看：[01｜从一个可访问的接口理解请求与响应](../docs/01-FastAPI职责与ASGI请求链路.md)。

</details>

<details>
<summary>3. 一个请求怎样到达路由函数？【FASTAPI-001】</summary>

服务器把网络数据转换成ASGI交互，应用匹配路由、解析校验输入并求值所需依赖，再调用处理函数，最后将结果编码为响应。具体嵌套与失败路径不能压成每次都完全相同的串行顺序。

回看：[01｜从一个可访问的接口理解请求与响应](../docs/01-FastAPI职责与ASGI请求链路.md)。

</details>

<details>
<summary>4. FastAPI为什么适合AI应用接口？</summary>

它把Python、类型契约、异步I/O和流式交付接在一起；但检索质量、工具执行和持久任务仍由业务及执行系统负责。

回看：[01｜从一个可访问的接口理解请求与响应](../docs/01-FastAPI职责与ASGI请求链路.md)。

</details>

<details>
<summary>5. 中间件与依赖的区别？【FASTAPI-002】</summary>

中间件包装应用处理过程，适合请求关联和通用响应处理；依赖声明具体路由所需输入、身份或资源，可组成依赖图并在测试中替换。

回看：[04｜依赖与中间件：复用前提，不隐藏执行过程](../docs/04-Dependency与Middleware.md)。

</details>

<details>
<summary>6. 多个中间件怎样执行？</summary>

对示例所添加的中间件，后加的在外层。请求先过外层再到内层，响应沿嵌套返回；流体发送的终点要另行测量。

回看：[04｜依赖与中间件：复用前提，不隐藏执行过程](../docs/04-Dependency与Middleware.md)。

</details>

<details>
<summary>7. yield依赖解决什么？</summary>

把资源交给调用方使用，并在相应作用域退出时清理。通常通过try/finally处理正常与异常，不把finally当作断电保证。

回看：[05｜资源生命周期：何时取得，何时归还](../docs/05-ResourceLifecycle.md)。

</details>

<details>
<summary>8. function与request作用域有何区别？</summary>

function在处理函数结束后、响应发送前清理；yield依赖默认request作用域覆盖响应周期，流继续使用资源时要匹配其生命周期。

回看：[05｜资源生命周期：何时取得，何时归还](../docs/05-ResourceLifecycle.md)。

</details>

<details>
<summary>9. lifespan与依赖怎么分？</summary>

lifespan管理每个应用实例的启动与退出资源；依赖承接具体请求或操作的输入与资源。一个共享客户端不应被单次请求结束关闭。

回看：[05｜资源生命周期：何时取得，何时归还](../docs/05-ResourceLifecycle.md)。

</details>

<details>
<summary>10. HTTP模型客户端为什么通常复用？</summary>

它可以管理可复用连接，减少每次创建和建连成本。仍需设有限连接、超时和明确关闭范围。

回看：[10｜连接外部服务：客户端、业务与协议适配](../docs/10-ExternalResourceIntegration.md)。

</details>

<details>
<summary>11. async def一定更快吗？</summary>

不是。可协作等待I/O时能让事件循环推进其他任务；同步阻塞和长CPU计算不会因函数声明改变而消失。

回看：[06｜异步与并发：等待时谁在继续工作](../docs/06-AsyncExecution与BlockingBoundary.md)。

</details>

<details>
<summary>12. 框架怎样执行普通def路由？</summary>

FastAPI对自己调用的同步路由与依赖使用线程执行；线程容量与下游资源仍有限。

回看：[06｜异步与并发：等待时谁在继续工作](../docs/06-AsyncExecution与BlockingBoundary.md)。

</details>

<details>
<summary>13. async路由里普通helper会自动进线程池吗？</summary>

不会，那是当前线程普通调用。必要时显式转交或使用异步接口。

回看：[06｜异步与并发：等待时谁在继续工作](../docs/06-AsyncExecution与BlockingBoundary.md)。

</details>

<details>
<summary>14. gather会自动限流吗？</summary>

不会。它组织并发结果，不控制总任务数或全局速率。Semaphore也只限制相应实例中的在途量。

回看：[06｜异步与并发：等待时谁在继续工作](../docs/06-AsyncExecution与BlockingBoundary.md)。

</details>

<details>
<summary>15. 请求、数据库和响应模型应共用吗？</summary>

不应默认共用。输入允许的字段、持久结构与公开结果服务不同边界；小项目可以简化但要明确过滤与责任。

回看：[03｜数据契约：校验输入、限制输出、解释错误](../docs/03-Pydantic与数据契约.md)。

</details>

<details>
<summary>16. response_model有什么作用？</summary>

参与输出校验、序列化、字段过滤与文档。返回直接构造的Response时，需要理解绕开相应处理的边界。

回看：[03｜数据契约：校验输入、限制输出、解释错误](../docs/03-Pydantic与数据契约.md)。

</details>

<details>
<summary>17. 字段、跨字段规则和业务授权怎样分开？</summary>

字段校验检查单项类型和范围；跨字段规则检查输入之间的关系，例如起始页不能晚于结束页。实际页数、资源归属和动作权限还需要可信业务事实，不能仅从输入合法推出允许执行。

回看：[03｜数据契约：校验输入、限制输出、解释错误](../docs/03-Pydantic与数据契约.md)。

</details>

<details>
<summary>18. 怎样通过SSE推运行中事件？【FASTAPI-004】</summary>

运行系统产生明确事件，API适配成SSE。客户端识别内容、错误和终止；重连需游标与历史，不能仅靠事件ID自动获得恢复。

回看：[07｜流式响应：逐步交付结果与 SSE 事件](../docs/07-Streaming与SSE.md)。

</details>

<details>
<summary>19. SSE只能GET吗？</summary>

服务端可在POST返回SSE；浏览器原生EventSource主要使用GET，不能随意设置POST体或自定义认证头。需要区分服务能力与客户端限制。

回看：[07｜流式响应：逐步交付结果与 SSE 事件](../docs/07-Streaming与SSE.md)。

</details>

<details>
<summary>20. 流发出200后失败怎么办？</summary>

不能改已发出的状态；能继续发送时用错误与终止事件，断开时客户端也要识别未收到终态。

回看：[07｜流式响应：逐步交付结果与 SSE 事件](../docs/07-Streaming与SSE.md)。

</details>

<details>
<summary>21. 轮询、SSE与WebSocket怎样选？</summary>

允许一定刷新延迟、只需要当前状态时可先评估轮询；服务端持续交付适合SSE；持续双向消息适合WebSocket。断开后要区分重新取得最新快照与补齐全部事件，身份、游标和缓冲仍由应用负责。

回看：[08｜WebSocket：让双方在连接中持续交流](../docs/08-WebSocket与EventProtocol.md)。

</details>

<details>
<summary>22. 客户端断开意味着后端停止吗？</summary>

不一定。连接资源应清理，临时工作可以取消，持久任务可以继续；远端动作是否停止取决于其真实协议。

回看：[12｜超时、断开与取消：请求结束之后发生什么](../docs/12-TimeoutCancellation与Disconnect.md)。

</details>

<details>
<summary>23. BackgroundTasks能代替可靠任务队列吗？</summary>

不能。它是在当前应用进程中响应后的工作。是否适用还要看任务丢失是否可接受，重要小任务也可能需要持久保证。

回看：[11｜上传与后台任务：接收完成不等于处理完成](../docs/11-BackgroundTask与Upload.md)。

</details>

<details>
<summary>24. bytes与UploadFile怎样选？</summary>

bytes把完整内容交给函数；UploadFile提供临时文件接口，适合分块。路由内分块并不保护之前的表单解析与网络入口，需配合上传限额。

回看：[11｜上传与后台任务：接收完成不等于处理完成](../docs/11-BackgroundTask与Upload.md)。

</details>

<details>
<summary>25. 大型文档处理API怎样设计？</summary>

区分文件已接收、任务已接受与执行成功。分块读取只改善内存使用；续传还需要上传标识、已存部分和完整性校验。任务应有独立状态，失败不发布半成品，清理由明确的任务所有者负责。

回看：[11｜上传与后台任务：接收完成不等于处理完成](../docs/11-BackgroundTask与Upload.md)。

</details>

<details>
<summary>26. 测试怎样替换身份或数据库依赖？</summary>

将原依赖函数映射到测试依赖，并在finally或fixture收尾时恢复原覆盖。不要只模拟整个HTTP结果。

回看：[13｜测试：让成功、拒绝与失败都有证据](../docs/13-Testing.md)。

</details>

<details>
<summary>27. SQL已经优化，为什么接口仍慢？</summary>

先核对端到端与SQL的测量范围，再测连接等待、其他下游、序列化、发送和代理。某一阶段快16倍不代表全程快16倍；并发Span还不能简单相加，优化应针对实际瓶颈。

回看：[14｜观测与性能：把慢请求拆成可定位的时间](../docs/14-Observability与Performance.md)。

</details>

<details>
<summary>28. 多worker为什么不共享全局dict？</summary>

worker通常是独立进程，各自持有内存与连接池。全局是进程内的全局，不是所有机器的全局。

回看：[15｜部署与退出：从一个进程到多个实例](../docs/15-Deployment与GracefulShutdown.md)。

</details>

<details>
<summary>29. 只会GET和POST为什么不足以构建完整服务？【FASTAPI-005】</summary>

还要定义身份、契约、资源、执行方式、事件、取消与任务状态，配合测试、观测和部署。路由入口不是整个运行系统。

回看：[16｜接口模式：把问答、任务与运行边界连起来](../docs/16-AIServicePatterns.md)。

</details>

<details>
<summary>30. FastAPI与Agent Runtime边界是什么？</summary>

API负责Web访问和交付边界，Runtime负责动态循环、工具、上下文、记忆与恢复。两者配合，不能互相推诿身份、取消和验证责任。

回看：[16｜接口模式：把问答、任务与运行边界连起来](../docs/16-AIServicePatterns.md)。

</details>

<details>
<summary>31. JSON没有Content-Type时为什么旧代码和课程版本行为不同？</summary>

0.132.0引入默认严格JSON Content-Type检查。应修正客户端声明，而不是默认关闭全局安全行为。

回看：[03｜数据契约：校验输入、限制输出、解释错误](../docs/03-Pydantic与数据契约.md)。

</details>

<details>
<summary>32. JSON Lines返回一个JSON数组吗？</summary>

不是，每行一个完整JSON值。课程原生接口默认媒体类型application/jsonl，需要逐行解析。

回看：[07｜流式响应：逐步交付结果与 SSE 事件](../docs/07-Streaming与SSE.md)。

</details>

<details>
<summary>33. except Exception是否捕获CancelledError？</summary>

现代asyncio中不捕获，CancelledError继承BaseException。显式捕获后通常仍应继续抛出。

回看：[12｜超时、断开与取消：请求结束之后发生什么](../docs/12-TimeoutCancellation与Disconnect.md)。

</details>

<details>
<summary>34. HTTPX的ASGITransport会自动执行lifespan吗？</summary>

不会，需要显式管理。TestClient用上下文管理器可执行生命周期。

回看：[13｜测试：让成功、拒绝与失败都有证据](../docs/13-Testing.md)。

</details>

<details>
<summary>35. Liveness和Readiness分别触发什么决策？</summary>

前者用于判断实例是否需要重启等恢复动作，后者判断是否应接流量；具体阈值与探测方式由平台设计。

回看：[15｜部署与退出：从一个进程到多个实例](../docs/15-Deployment与GracefulShutdown.md)。

</details>

<details>
<summary>36. 后台任务可以复用请求结束时释放的会话吗？</summary>

不应依赖这样的寿命。任务应拿稳定标识，并建立自己拥有的资源范围。

回看：[05｜资源生命周期：何时取得，何时归还](../docs/05-ResourceLifecycle.md)。

</details>

## 契约与身份的交叉自测

<details><summary>str | None 没默认值时，为什么 {} 失败而 {"name": null} 可以通过？PATCH 又为什么用 exclude_unset？</summary>

前者缺少必填字段，后者提供了允许的空值。PATCH 需要区分省略与明确清空，exclude_unset 保留实际提供的字段；exclude_none 会丢掉明确清空。回看[第 03 章](../docs/03-Pydantic与数据契约.md)。

</details>

<details><summary>解码出 JWT 的 tenant_id，为什么还不能建立可信租户身份？</summary>

编码可读取不代表可信。先验证签名、允许算法、签发方、受众、有效期及所需声明，再检查当前身份与成员关系，最后授权具体动作。签名不加密 payload，也不自动撤销旧权限。回看[第 09 章](../docs/09-Security与TenantContext.md)。

</details>

<details><summary>为什么 Cookie、Session、JWT 与 CORS 不是同一层的选择？</summary>

Cookie 是浏览器自动保存/发送的载体，Session 是会话状态，JWT 是声明格式，CORS 控制浏览器跨源读取。自动携带认证 Cookie 的写操作还要考虑 CSRF，不能用“读不到响应”证明动作没发生。

</details>

## 请求链综合回看

以第 16 章的同一条任务为例，依次解释路由、输入、身份、公开输出及取消状态。再对照测试章判断每份证据覆盖了哪一层：进程内行为不等于真实网络，真实网络也不等于部署代理。这里用于阅读后重建关系，不要求另写项目作为通关条件。
