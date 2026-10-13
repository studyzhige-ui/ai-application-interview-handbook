# FastAPI｜把 Python 能力变成可校验、可观测的网络接口

[← Python](../01-python/README.md) · [课程目录](../README.md) · [Handbook](../../README.md) · [MySQL →](../03-mysql/README.md)

从第一个请求开始，依次学习路由、数据契约、依赖、资源、流式交付、访问控制、测试与部署。

## 学习前提与目标

先掌握 Python 函数、异常、类型标注、生成器与 async/await。

学完后应能把 Python 能力变成可校验、可观测的网络接口。

## 学习顺序

1. [01｜从一个可访问的接口理解请求与响应](docs/01-FastAPI职责与ASGI请求链路.md)
2. [02｜路由与参数：请求怎样变成函数输入](docs/02-Routing与APIContract.md)
3. [03｜数据契约：校验输入、限制输出、解释错误](docs/03-Pydantic与数据契约.md)
4. [04｜依赖与中间件：复用前提，不隐藏执行过程](docs/04-Dependency与Middleware.md)
5. [05｜资源生命周期：何时取得，何时归还](docs/05-ResourceLifecycle.md)
6. [06｜异步与并发：等待时谁在继续工作](docs/06-AsyncExecution与BlockingBoundary.md)
7. [07｜流式响应：逐步交付结果与 SSE 事件](docs/07-Streaming与SSE.md)
8. [08｜WebSocket：让双方在连接中持续交流](docs/08-WebSocket与EventProtocol.md)
9. [09｜认证、授权与租户：让访问范围可信](docs/09-Security与TenantContext.md)
10. [10｜连接外部服务：客户端、业务与协议适配](docs/10-ExternalResourceIntegration.md)
11. [11｜上传与后台任务：接收完成不等于处理完成](docs/11-BackgroundTask与Upload.md)
12. [12｜超时、断开与取消：请求结束之后发生什么](docs/12-TimeoutCancellation与Disconnect.md)
13. [13｜测试：让成功、拒绝与失败都有证据](docs/13-Testing.md)
14. [14｜观测与性能：把慢请求拆成可定位的时间](docs/14-Observability与Performance.md)
15. [15｜部署与退出：从一个进程到多个实例](docs/15-Deployment与GracefulShutdown.md)
16. [16｜综合实作：把问答与执行任务接成可验证 API](docs/16-AIServicePatterns.md)

## 正文与复习

首次学习沿 docs 的完整主线理解输入、状态变化、结果与失败边界，再用章末自测检查能否独立解释。第二遍使用 [Review](review/README.md)重建关系，并改变条件验证结论。

面试准备集中在 [本知识域](../../interview/02-fastapi/README.md)：[高频面试题](../../interview/02-fastapi/01-高频面试题.md)、[易混易错点](../../interview/02-fastapi/02-易混易错点.md)与[面试速查](../../interview/02-fastapi/03-面试速查.md)。正文负责完整模型，面试材料负责回答、追问与快速回忆。

## 版本与验证边界

课程目标版本为 FastAPI 0.141.1，示例以 Python 3.11+ 为入口；版本目标不代表所有环境均已执行验证。

技术事实以正文引用的官方资料及适用范围为依据；[Market](../../market/README.md)中的真实岗位与面试材料用于校准学习深度，不能代替技术证明。
