# FastAPI｜可执行例子与回归

[← 模块主页](../README.md) · [测试章](../docs/13-Testing.md)

正文中的 `# example: ...` 标记把完整程序与其余片段分开。测试直接读取这些代码块，不维护另一份容易漂移的手写实现。部分块是明确的练习测试或多文件组件，不是独立启动程序。

## 运行目标版本验证

从仓库根目录执行：

```bash
python -m pip install -r curriculum/02-fastapi/examples/requirements.txt
python -m pytest curriculum/02-fastapi/examples/test_course.py -q
```

默认要求FastAPI恰为0.141.1；不满足时失败退出。安装完成后应保存 `python -m pip freeze` 与测试输出。requirements固定直接依赖，不是所有平台的完整锁文件。

网络或环境受限时，可明确运行兼容性检查：

```bash
python -m pytest curriculum/02-fastapi/examples/test_course.py --allow-compat -q -rs
```

非目标版本会跳过原生SSE、原生JSON Lines和严格Content-Type专用检查。这种结果不得表述成0.141.1全量通过。语法检查也不能代替框架执行。

## 取出一个程序自己练习

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
