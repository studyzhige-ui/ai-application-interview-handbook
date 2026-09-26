# FastAPI｜官方资料、版本与验证边界

[← FastAPI课程](../../curriculum/02-fastapi/README.md) · [References](../README.md)

资料核验日期：2026-09-25。课程目标版本是 **FastAPI 0.141.1**，发布于2026-07-29。本文依据官方发布记录、教程和依赖库文档，不将某一旧版本行为写成永久规则。HUMAN-A的冻结统计不因技术资料更新而改变。

## 1. 版本基线

[PyPI发布页](https://pypi.org/project/fastapi/0.141.1/)与[官方Release](https://github.com/fastapi/fastapi/releases/tag/0.141.1)相互核对。对应发布提交为 `95f8322ee1dcda7ceace7b1c4f6c9915b36d748f`；源码以这个版本标签为准，教程页面后续可能继续更新。

| 能力或变化 | 版本位置 | 课程处理 |
|---|---|---|
| 默认严格JSON Content-Type | 0.132.0 | 输入契约章说明客户端声明及兼容边界 |
| 原生JSON Lines流式返回 | 0.134.0 | 流式章消息格式比较旁的实现对照；先理解逐条记录与事件的差别 |
| 原生SSE | 0.135.0 | event、data、id、终态、客户端与重连 |
| 直接使用Pydantic序列化的优化 | 0.130.0起相关变化 | 序列化实现与性能资料；正文先学输入输出转换 |
| ORJSONResponse/UJSONResponse弃用提示 | 0.131.0 | 不作为新课程默认优化方案，不把弃用说成已删除 |
| APIRouter内部组织变化 | 0.137.0 | 只教学可观察的include_router行为，不把旧的克隆实现当成通用机制 |
| frontend能力与相关修复 | 0.138.0至0.141.1 | 只保留参考入口，遇到同服务前端托管需求再查 |

上述时间点以[官方发布记录](https://fastapi.tiangolo.com/release-notes/)为依据。`Latest Changes`可能包含尚未发布内容，不能用来替代稳定版本基线。

## 2. 请求、输入与输出

| 疑问 | 权威资料 |
|---|---|
| 应用如何开始工作 | [First Steps](https://fastapi.tiangolo.com/tutorial/first-steps/) |
| Body怎样映射为类型模型 | [Request Body](https://fastapi.tiangolo.com/tutorial/body/) |
| 响应模型如何限制公开字段 | [Response Model](https://fastapi.tiangolo.com/tutorial/response-model/) |
| 为什么输入错误与输出错误不同 | [Handling Errors](https://fastapi.tiangolo.com/tutorial/handling-errors/) |
| JSON请求头如何影响解析 | [Strict Content-Type](https://fastapi.tiangolo.com/advanced/strict-content-type/) |
| Pydantic解析、校验和序列化 | [Models](https://docs.pydantic.dev/latest/concepts/models/)、[Strict Mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) |

[Pydantic 模型校验器](https://docs.pydantic.dev/latest/concepts/validators/#model-validators)用于核对 after 校验器的执行位置和返回约定；它不自动替代依赖数据库事实的业务判断。

## 3. 依赖、资源与执行

[Dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/)与[Sub-dependencies](https://fastapi.tiangolo.com/tutorial/dependencies/sub-dependencies/)说明依赖图和请求内结果复用。[yield依赖](https://fastapi.tiangolo.com/tutorial/dependencies/dependencies-with-yield/)说明获取、清理、作用域与异常传播；[Lifespan](https://fastapi.tiangolo.com/advanced/events/)管理应用范围资源。

[Async说明](https://fastapi.tiangolo.com/async/)区分框架调用同步路由和普通helper调用；[Starlette线程池](https://starlette.dev/threadpool/)说明同步执行有容量边界。不要仅凭函数名含async判断真实执行位置。

## 4. 流式、WebSocket与取消

- [SSE教程](https://fastapi.tiangolo.com/tutorial/server-sent-events/)与[API参考](https://fastapi.tiangolo.com/reference/sse/)：事件数据编码、原生响应、心跳和续接线索。
- [JSON Lines](https://fastapi.tiangolo.com/tutorial/stream-json-lines/)：逐项类型声明及`application/jsonl`。
- [WebSocket](https://fastapi.tiangolo.com/advanced/websockets/)：接受、收发、断开和依赖。
- [ASGI HTTP/WebSocket规范](https://asgi.readthedocs.io/en/latest/specs/www.html)：响应开始、响应体结束和断开事件。
- [Python asyncio异常](https://docs.python.org/3/library/asyncio-exceptions.html)：CancelledError自3.8起继承BaseException。
- [Task、TaskGroup与timeout](https://docs.python.org/3/library/asyncio-task.html)：本地任务取消和等待。
- [AnyIO取消](https://anyio.readthedocs.io/en/stable/cancellation.html)：取消作用域与有限清理。
- [浏览器EventSource](https://developer.mozilla.org/en-US/docs/Web/API/EventSource)：客户端发起方式，不能与服务器支持POST混为一谈。

取消传播、最终ASGI消息发送与客户端接收是不同边界；文档与测试都应按相应责任描述。[WHATWG EventSource 规范](https://html.spec.whatwg.org/multipage/server-sent-events.html#the-last-event-id-header)用于核对 Last-Event-ID；传输层的续接线索不能写成业务已持久处理的确认。

## 5. 外部资源、安全与上传

[HTTPX异步客户端](https://www.python-httpx.org/async/)、[超时](https://www.python-httpx.org/advanced/timeouts/)、[传输适配](https://www.python-httpx.org/advanced/transports/)用于核对客户端复用与模拟的边界。MockTransport不测试真实网络与池容量。

[FastAPI安全](https://fastapi.tiangolo.com/tutorial/security/first-steps/)和[CORS](https://fastapi.tiangolo.com/tutorial/cors/)分别说明身份工具与浏览器跨源机制。[文件上传](https://fastapi.tiangolo.com/tutorial/request-files/)说明bytes与UploadFile；[后台任务](https://fastapi.tiangolo.com/tutorial/background-tasks/)与[Starlette后台执行](https://starlette.dev/background/)说明任务顺序、异常和进程边界。

补充资料核验日期：2026-09-26。

- [HTTP 502／504 规范](https://www.rfc-editor.org/rfc/rfc9110.html#section-15.6.3)：核对网关角色、无效响应与未及时响应的区别，不把全部上游错误硬映射为 502。
- [OWASP 事务授权](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html)：核对确认结果如何绑定具体动作，防止确认后换目标或参数。
- [S3 分段上传](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)：作为可续传协议的具体实现参照，区分上传标识、部分记录、完成和清理；不把它当作 HTTP 表单上传的通用行为。

## 6. 验证、观测与部署

[测试教程](https://fastapi.tiangolo.com/tutorial/testing/)、[依赖替换](https://fastapi.tiangolo.com/advanced/testing-dependencies/)、[异步测试](https://fastapi.tiangolo.com/advanced/async-tests/)与[WebSocket测试](https://fastapi.tiangolo.com/advanced/testing-websockets/)分别负责各类测试入口。HTTPX ASGITransport不自动启动lifespan，测试客户端也不代替真实代理。

[Starlette中间件](https://starlette.dev/middleware/)与ASGI规范用于核对计时终点。[worker](https://fastapi.tiangolo.com/deployment/server-workers/)、[容器](https://fastapi.tiangolo.com/deployment/docker/)、[代理](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)、[Uvicorn设置](https://www.uvicorn.org/settings/)用于进程、容量和退出边界。可选[前端托管](https://fastapi.tiangolo.com/tutorial/frontend/)不替代这些运行责任。

## 7. 如何阅读验证记录

课程示例的目标版本与本次实际可运行版本须分别记录。初次修订结果见[修订与验证记录](../../guide/project/fastapi-reader-revision-2026-09-25.md)，本轮修改与重跑范围见[面经校验记录](../../guide/project/fastapi-interview-alignment-2026-09-26.md)。官方文档核对不等于全部代码已在目标版本运行；本地通过也不等于跨平台、代理、数据库和供应商集成通过。
