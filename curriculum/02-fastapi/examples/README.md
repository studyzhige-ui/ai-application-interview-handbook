# FastAPI｜可执行例子与回归

[← 模块主页](../README.md) · [测试章](../docs/13-Testing.md)

正文中的 `# example: ...` 标记把完整程序与其余片段分开。测试直接读取这些代码块，不维护另一份容易漂移的手写实现。部分块是明确的对照测试或多文件组件，不是独立启动程序。

## 按需运行目标版本回归

从仓库根目录执行：

```bash
python -m pytest curriculum/02-fastapi/examples/test_course.py -q
```

默认已有代码环境。此维护回归要求 FastAPI 恰为 0.141.1，用于避免把其他版本的结果误报为目标版本；它不是读者继续阅读的门槛。requirements.txt 记录直接依赖基线，不是所有平台的完整锁文件。维护者记录实际依赖版本与测试输出。

网络或环境受限时，可明确运行兼容性检查：

```bash
python -m pytest curriculum/02-fastapi/examples/test_course.py --allow-compat -q -rs
```

非目标版本会跳过原生SSE、原生JSON Lines和严格Content-Type专用检查。这种结果不得表述成0.141.1全量通过。语法检查也不能代替框架执行。

## 按需取出一份解释程序

从仓库根目录执行，例如提取第一章程序：

```bash
python tools/export_fastapi_example.py hello_app --output /tmp/hello_app.py
```

Windows可把输出改成自己创建的练习目录中的 `main.py`。工具默认不覆盖已有文件，文件存在时应换一个名字或明确加 `--overwrite`。普通教学服务用 `python -m uvicorn main:app --reload` 启动；脚本型例子直接运行；测试块按正文的文件组合使用。

## 验证边界

TestClient检查路由、类型、依赖、权限、资源和协议；本地Uvicorn实验检查真实套接字上的增量到达。MockTransport不验证真实模型或网络连接池。测试没有访问生产数据、收费模型或远端Git仓库。

第16章内存任务示例不承诺持久、跨进程和幂等创建；相应测试专门保留这些边界。真实代理、供应商取消和数据库事务需要另外的集成环境。


## 实现对照与维护测试

正文中的较长实现放在相关问题旁，仍进入示例回归检查。场景选择和失败边界留在主线，不因某段代码折叠就免于学习。初次范围取舍见[核心范围复核](../../../guide/project/fastapi-core-scope-review-2026-09-26.md)，后续面经校验与本轮验证见[面经校验记录](../../../guide/project/fastapi-interview-alignment-2026-09-26.md)。完整程序继续由正文导出，避免形成无人验证的另一套代码。

本轮目标版本回归：CPython 3.12.14、FastAPI 0.141.1、Pydantic 2.13.4、pytest 9.0.2，共 121 项通过；使用 requirements.txt 固定的全部直接依赖（Uvicorn 0.48.0、HTTPX 0.28.1、python-multipart 0.0.29、websockets 16.0）。包含新增的必填/可空、嵌套别名与独立默认列表、PATCH 省略/清空、日期/十进制序列化、响应/Cookie 和异步生命周期对照；保留原有真实本地套接字增量检查。回归有一条 Starlette 关于 TestClient 使用 HTTPX 的弃用提示；依赖未全量锁定，后续升级应结合框架支持核对。这不是部署代理、真实认证签发/撤销或生产数据库的集成证明。
