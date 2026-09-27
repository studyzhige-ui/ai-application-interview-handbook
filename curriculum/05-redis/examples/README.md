# Redis 实验入口｜任选客户端，先预测再运行

[← Redis 首页](../README.md) · [按章节进入实验](labs.md)

正文讲模型、过程与取舍，这里负责准备和复现实验。阅读课程不要求会 Python 或 Java；Redis 命令是一套服务端接口，不同语言的客户端都在与这套接口交互。

## 1. 先建立独立、可丢弃的环境

本课程固定 Redis Open Source **8.10.2**，不使用会移动的 latest 标签。已有 Docker 的环境，可以在系统终端运行：

```bash
docker run -d --name redis-reader-lab -p 127.0.0.1:16379:6379 redis:8.10.2 sh -c "exec redis-server --save '' --appendonly no"
docker exec redis-reader-lab redis-server --version
docker exec -it redis-reader-lab redis-cli
```

第一条启动学习容器，第二条确认版本，第三条打开客户端。提示符通常为 `127.0.0.1:6379>`；实验中的 Redis 命令输入在这里，不直接输入系统终端。

16379 是宿主机端口，6379 是容器内服务端口；docker exec 内的客户端连接容器内端口。关闭客户端用 exit，关闭学习容器用 `docker stop redis-reader-lab`。需要保留快照时不要删除容器。

> ⚠️ 配置关闭自动快照和 AOF，只用于可丢弃数据。只发布到本机地址，不连接生产网络，不挂载生产目录，不向实例放真实用户资料或密钥。同名容器已存在时先核对归属，不直接删除。

没有 Docker 时，通过[官方安装入口](https://redis.io/docs/latest/operate/oss_and_stack/install/)选择适合平台的方法。应用项目可以选各自语言的成熟客户端，不需要为了学习 Redis 转换开发语言。

## 2. 每次只完成与当前问题对应的一组

进入[实验目录](labs.md)，先看适用条件和初始状态，再预测回复。执行之后分别检查返回结果与保存的状态；它们不是一回事。需要多个连接或同一 Stream 的实验有顺序要求，不把整页一次性发送到未知服务器。

大量命令与长脚本不再穿插在正文推导中，但仍作为可检查的统一源。不要另行维护一套手写答案。

## 3. 以下是维护者的验证工具，不是读者语言前置

工具使用 Python 3.10+ 标准库；这里用 Python 是为了维护本仓库的检查器，不限制用户业务语言。进入本目录运行：

```bash
python -m unittest test_offline -v
```

它检查章节结构、内部链接、命令预期的形式、有限 RESP2 解析器，以及正文明确假设的算术和状态模型。**没有启动 Redis，不证明命令或 Lua 已实际执行。**

`reader.py` 同时读取 docs 中的最小例子与 labs.md 中的连续实验，脚本和预期仍在同一个来源。需要导出时调用 reader.export，并使用新目录；导出器会拒绝覆盖内容不同的文件。

## 4. 目标版本实机验证有单独入口

在独立 Linux 开发或 CI 环境准备 Redis 8.10.2 服务程序后执行：

```bash
python run_live.py --server /absolute/path/to/redis-server --report redis-live-report.json
```

工具核对精确版本，自建临时目录和仅本机监听的进程，并验证进程 PID 后才发送命令。结束后关闭自己拥有的进程，不接受现成远程地址。没有服务程序或版本不同，返回未执行，不会静默跳过后显示全部通过。

> ⚠️ 实机套件含快照和关闭服务的测试，仅针对自身拥有的临时实例。它不验证生产掉电、Sentinel/Cluster 故障转移，也不验证任何业务语言客户端的连接池、TLS 或返回值转换。protocol.py 是有限测试驱动，不是可直接使用的生产客户端。

报告分别记录目标版本、实际版本、执行范围、通过项及未执行项。预期结果写进 JSON，只代表要检查什么，不代表检查已经发生。
