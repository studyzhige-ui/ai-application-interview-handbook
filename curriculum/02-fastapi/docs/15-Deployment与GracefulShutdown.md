# 15｜部署与退出：从一个进程到多个实例

[← 上一章](14-Observability与Performance.md) · [模块主页](../README.md) · [下一章 →](16-AIServicePatterns.md)

一个终端里能访问 `/hello`，不等于服务已经可以长期承接用户。上线后进程会重启、流量会分配到不同实例，长连接也可能在发布时仍未结束。部署需要回答：**由谁运行，能承受多少，什么时候接流量，怎样退出。**

这一章不要求先学会 Kubernetes；先理解单个进程，再理解多个进程与平台配合的边界。

## 1. 开发重载与生产运行分开

开发时使用：

```bash
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8000
```

重载便于修改代码后重启服务；生产不应把它当成进程可靠性机制。一个简单的生产启动形态可以是：

```bash
python -m uvicorn main:app --host 0.0.0.0 --port 8000 --workers 2
```

`0.0.0.0` 表示监听各网络接口，不是用户应在浏览器输入的目标地址。需要根据网络、防火墙与代理安排实际访问入口。`--reload` 与多 worker 是不同运行方式，不要一起作为默认命令复制。

本课程使用 Uvicorn 明确展示入口，安装 `fastapi[standard]` 时也可使用官方 CLI 的 `fastapi dev`、`fastapi run`。它们是启动方式，不改变应用的 HTTP 契约。

## 2. 一个 worker 拥有一份自己的内存

多个 worker 通常是多个进程，各自导入应用、运行 lifespan、拥有自己的客户端与连接池。普通全局 dict 不会自动同步。

```text
请求1 → worker A → 内存里写入任务7
请求2 → worker B → 自己的内存里没有任务7
```

这个问题不会因为变量名字叫 `global_tasks` 而消失。需要跨请求、跨实例、跨重启可靠存在的业务状态，应由合适的外部状态系统管理。

多 worker 有助于利用多核和隔离部分进程级故障，但并不保证吞吐按数量线性增长。

## 3. 连接池与内存按实例一起估算

假设 2 个副本，每副本 3 个 worker，每个 worker 最多 20 个数据库连接，单按这个配置上限就可能达到：

```text
2 × 3 × 20 = 120 个连接
```

实际连接数还受惰性建立、驱动和负载影响，但数据库侧必须能承受设计允许的总量。模型对象、Tokenizer 和其他大资源同样可能按进程复制，不能只看“单进程占用”。

增加 worker 之前先看 CPU、内存、连接与下游配额，确认瓶颈在哪。若下游已经饱和，更多入口可能只是放大排队。

## 4. 存活与就绪是两种决策

**存活探测（Liveness）** 帮助平台判断实例是否出现需要重启的故障。**就绪探测（Readiness）** 帮助平台判断当前是否应该把流量发给它。

应用活着但尚未完成必要初始化时，不应接业务流量。某个共享下游短暂故障时，是否重启所有实例、是否摘除流量也要根据实际恢复策略决定，不能把每次下游波动都变成重启风暴。

```python
# example: health_app
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Request

@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.ready = False
    # 教学中初始化轻量目录；真实资源失败应阻止应用错误宣告就绪。
    app.state.catalog = {1: "可用"}
    app.state.ready = True
    try:
        yield
    finally:
        app.state.ready = False
        app.state.catalog.clear()

app = FastAPI(lifespan=lifespan)

@app.get("/live")
def live():
    return {"alive": True}

@app.get("/ready")
def ready(request: Request):
    if not getattr(request.app.state, "ready", False):
        raise HTTPException(503, "尚未就绪")
    return {"ready": True}
```

这个应用演示状态含义。ASGI 服务器通常会等启动完成再承接请求，因此不能期待启动中的同一应用一定能对外响应 503。就绪接口、平台探测和发布摘流需要一起设计。

> ⚠️ 把 ready=False 写在 lifespan 退出部分，不等于已经在退出前完成了负载均衡摘流。平台何时停止发新请求、Uvicorn 等待多久、最终何时强制终止，都不是这个布尔值单独决定的。

## 5. 优雅退出需要一条有时限的流程

```text
接到退出或发布信号
        ↓
平台与服务器协调停止接收新工作
        ↓
在预算内等待已有请求，处理长连接
        ↓
取消可取消工作，保留持久任务的可恢复状态
        ↓
关闭应用共享资源
        ↓
退出；超出平台预算时可能被强制终止
```

SSE 和 WebSocket 可能长期不自然结束，所以不能无限等待。可发送终止提示时发送，让客户端按约定重连；无法发送时，客户端也必须能识别中断。

适当配置服务器的优雅退出超时，并确保平台的终止窗口留有协调与清理余量。不要假设仅写 finally 就可以对抗任何终止。

## 6. 容器、副本和代理各做什么

容器是部署封装，不等于单个 Python 进程。平台可以每容器一个 worker、以多个副本扩展，也可以有其他进程安排；选择应结合资源限制、启动成本和发布粒度。

HTTPS、转发头和路径前缀通常由代理参与。应用信任转发头时必须限制可信代理来源，否则外部客户端可能伪造协议或地址。若代理把 `/api` 前缀去掉再转给应用，生成文档和 URL 时才需要了解 `root_path` 的具体配置。[代理文档](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)提供了具体边界。

### 6.1 一次带前缀的 HTTPS 请求怎样变化

假设公开入口是 `https://notes.example/api/hello`，代理与应用部署在同一机器，代理终止 TLS 并剥掉 `/api`：

```text
浏览器：HTTPS /api/hello，Host=notes.example
→ 可信代理：解密，移除 /api 前缀
→ 内部网络请求：HTTP /hello → 127.0.0.1:8000
→ 应用：匹配 /hello，知道公开部署前缀 root_path=/api
→ 文档与生成的公开 URL：仍要表达外部的 HTTPS、主机和 /api
```

这三个信息来自不同责任：代理转发外部 Host，受信任的 `X-Forwarded-Proto` 等头提供外部协议/来源，root_path 描述挂载前缀。例如这个“只有同机代理能到达应用”的配置形态：

```bash
python -m uvicorn main:app --host 127.0.0.1 --port 8000 --proxy-headers --forwarded-allow-ips 127.0.0.1 --root-path /api
```

`--forwarded-allow-ips` 限制哪些直接连接者可以提供可信转发头；不应在可被公网直连的应用上随意信任 `*`。root_path 不负责配置代理，也不是自动给全部业务路由再加一次 `/api`。若前缀剥除、路由前缀与 root_path 重复或漏配，常见结果是文档页面打开了，却去错误位置取 OpenAPI，或重定向生成内部 HTTP 地址。需要沿实际入口逐跳核对。[代理与 root_path](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)

### 6.2 信号、等待窗口与清理是不同阶段

进程管理器通常通过 SIGTERM 请求退出；Uvicorn 停止接收新连接，并在配置窗口内等待正在进行的请求/任务，然后推进关闭。`--timeout-graceful-shutdown` 限制服务器优雅等待，不是保证所有远端副作用在这个时间内撤销。平台最终强杀窗口还要留出摘流传播和应用清理余量；具体总顺序由部署平台与服务器共同决定。

例如平台总窗口 30 秒，摘流传播预计 5 秒，在途请求等待分配 15 秒，其余留给资源关闭与调度余量。长 SSE/WebSocket 不能默认自然结束，应有终止/重连策略；持久任务的恢复不能依赖最后一刻还来得及写内存。这个算例说明预算分配，不是推荐所有系统照抄同一组秒数。[Uvicorn 退出设置](https://www.uvicorn.org/settings/)


## 7. 部署之前真正需要验证什么

1. 冷启动时必要资源能初始化；初始化失败不会误报成功。
2. 多进程请求不依赖进程内共享业务状态。
3. 并发增加时连接、内存和下游使用没有越过预算。
4. 发布中已有短请求、流式连接与持久任务按各自规则处理。
5. 经实际代理的流不会意外缓冲，身份与转发配置正确。

这组检查不是 Kubernetes 专用知识。即使部署在一台虚拟机上，同样需要进程管理、日志、失败重启与有限退出预算。

**生命周期证据：** health_app 在 TestClient 上下文内 ready 为 True，退出后为 False 且 catalog 为空，说明该应用的进入/退出逻辑被执行。它没有平台摘流、真实多进程或强杀路径，不能拿这条绿色测试代替那些证据。

---

## 本章小结

部署把应用放进真实的进程与平台生命周期。每个 worker 有独立资源，健康信号服务于不同决策，退出必须有预算。无状态 API 不是没有任何状态，而是关键事实不依赖某个进程内存长期存活。

## 🎯 面试怎么回答

**为什么增加 worker 会压垮数据库？**

> 每个 worker 通常各自持有连接池，总上限随副本与进程数量增长。扩容入口前应同时检查数据库和下游容量。

**Lifespan 能自动完成全部优雅退出吗？**

> 不能。它负责应用内初始化和清理；流量摘除、等待在途请求、退出超时和强杀由服务器与平台共同决定。

## ⚠️ 易错点

> ⚠️ 生产不用 reload 代替进程管理；reload 与 worker 扩展不是同一目的。

> ⚠️ 全局 dict 在多 worker 间不自动共享。

> ⚠️ 轻量 live 响应不证明所有下游健康，也不应让每次存活探测都真实调用模型。

## 本章自测

先回答，再展开核对。结合正文例子，说出预期结果及原因即可。

<details>
<summary>1. 2 副本、3worker、每池 20 连接，为什么要考虑 120 而不是 20？</summary>

因为池通常属于每个进程，多个副本中各自有独立池。

</details>

<details>
<summary>2. ready=False 是否自动让代理停止发请求？</summary>

不会，代理或平台必须读取并使用该信号，且要考虑传播时序。

</details>

<details>
<summary>3. 为什么长 SSE 连接会影响退出？</summary>

若无限等待自然结束，发布可能无法完成；需要有限 drain、终止或重连策略。

</details>

## 知识回看与权威资料

- [多 worker](https://fastapi.tiangolo.com/deployment/server-workers/)：核对进程内存与启动方式。
- [容器部署](https://fastapi.tiangolo.com/deployment/docker/)：理解进程、副本和启动步骤。
- [代理边界](https://fastapi.tiangolo.com/advanced/behind-a-proxy/)：核对可信转发头与路径前缀。
- [Uvicorn 设置](https://www.uvicorn.org/settings/)：核对 worker、reload 与退出超时。
