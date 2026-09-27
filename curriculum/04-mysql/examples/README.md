# MySQL 实验｜固定小数据与双会话验证

[返回课程](../README.md) · [第 02 章：创建第一张表](../docs/02-单表查询与增删改.md)

这里为正文提供统一数据，不是另一份需要先读完的教材。第 01 章先建立概念，第 02 章完成第一张表；从第 03 章起加载本目录的 `seed.sql`。它会重置课程表，使每次实验有同样的起点。

## 1. 目标环境与实际验证分开

目标为MySQL Community **9.7 LTS、InnoDB**。通用服务器基线9.7.2；本地容器使用官方9.7.3镜像，其发布说明是Docker镜像安全补丁。MySQL 8.4等其他版本可以比较部分机制，但不能直接作为9.7验证结果；MariaDB、SQLite及Python模型也不是本课程的MySQL执行替代品。

**验证状态：真实MySQL测试尚未执行。** 正文给出规则推导的预期，运行脚本准备好供目标环境验证；实际环境及具体范围见[验证记录](../../../guide/project/mysql-reader-revision-2026-09-27.md)。

## 2. 选择一个数据库客户端

没有安装服务器时，按[MySQL 官方安装入口](https://dev.mysql.com/doc/refman/9.7/en/installing.html)选择操作系统对应的 Community Server 安装方式，再创建仅供练习的数据库与账号。客户端可以是你已经熟悉的图形工具或 mysql 命令行；知道如何连接、打开 SQL 编辑区、执行选中语句和查看结果即可，不要求掌握应用语言。

下面两条路径任选一种：已有本地 MySQL 就直接连接；已有 Docker 环境可以使用下一节的容器方式。两者都不是另一个编程语言教程。

## 3. 使用已有本地 MySQL

建立专用练习数据库`handbook_mysql_lab`，使用仅能访问它的练习账号。连接后检查`SELECT VERSION()`、`SELECT DATABASE()`与`SELECT @@session.transaction_isolation`。

终端示例：

```bash
mysql --host=127.0.0.1 --port=3306 --user=course -p --default-character-set=utf8mb4 handbook_mysql_lab
```

密码交互输入，不放进命令行。不同客户端创建的窗口是否共享连接要确认；锁与隔离实验需要两个真正独立的连接。

## 4. 使用已有 Docker 环境

本节不要求为学习SQL额外先学容器平台；已有Docker时，可在此目录操作：

1. 将`.env.example`复制为`.env`，填写两份仅用于本地练习的密码。`.env`已被本目录忽略。
2. 执行`docker compose up -d`，等待初始化完成。检查`docker compose logs mysql`，不要把“容器已创建”当成数据库已准备好。
3. 主机客户端使用`127.0.0.1:3307`、用户`course`连接；这与容器内部的3306端口不同。

没有主机`mysql`客户端时，可以在两个终端分别执行：

```bash
docker exec -it mysql-reader-lab mysql -u course -p --default-character-set=utf8mb4 handbook_mysql_lab
```

完成后`docker compose stop`停止实例并保留数据。`docker compose down -v`会删除课程卷，只有确实要清空练习数据时才使用；不要拿其他项目的Compose文件执行清理。

> ⚠️ 镜像标签与实际环境要在运行时核对，联网拉取和Docker启动尚未在本交付环境实测。镜像不可用时明确报告，不静默换成另一个数据库产品。

## 5. 初始化与重置

`seed.sql`只操作明确命名的`handbook_mysql_lab`中的课程表，不删除数据库，也不包含任何生产配置变更。执行前结束A、B两个连接中的旧事务，确认不再需要当前练习修改。

主机客户端可以在MySQL提示符内执行：

```sql
SOURCE /你的实际仓库路径/curriculum/04-mysql/examples/seed.sql;
```

Windows路径可用正斜杠。使用容器客户端时，先在终端复制文件：

```bash
docker cp seed.sql mysql-reader-lab:/tmp/mysql-course-seed.sql
```

然后在容器的MySQL提示符中执行`SOURCE /tmp/mysql-course-seed.sql;`。`SOURCE`是mysql客户端命令；使用图形工具时打开SQL文件并执行内容。

初始化得到：

| 表 | 内容 | 用途 |
|---|---|---|
| members | 3名成员，团队10和20 | JOIN、EXISTS |
| tasks | 6项任务，日期固定 | 查询、索引、分页 |
| accounts | 两个账户各100，version为0 | 事务、MVCC、并发 |
| credit_events | 空表 | 扣减与流水 |
| lock_numbers | 主键10、20、30 | 范围锁实验 |

第 02 章的 `first_tasks`独立，不由此文件重置。要重复第 02 章，在确认是练习库之后单独删除那张表，再执行该章建表语句。

## 6. 怎样执行单章实验

[配套实验](experiments.md)按正在学习的问题选择。正文中标为同一过程的代码块按顺序执行。不同章节开始时，按正文要求重置；不要带着上一轮余额70去核对下一章“初始余额100”的输出。

索引计划没有固定答案：六行表可能选择全表扫描。测试检查查询结果及计划能否生成，不硬编码某版本必须选择哪个索引、花多少毫秒。

双会话实验先执行A的一步，再执行B的一步，遇到“等待”时去另一边释放锁或制造下一条等待边。一次复制整篇SQL，无法验证并发时间线。

## 7. 可选的维护工具

到这里已经具备全部人工练习前提。以下脚本供维护者自动核对，**不作为阅读、手工执行 SQL 或完成自测的前置**。学习者使用 Java 或其他语言也不需要先学会这些脚本。

### 从正文和实验页导出 SQL

在仓库根目录运行：

```bash
python tools/export_mysql_example.py --list
python tools/export_mysql_example.py filter_tasks
```

命令只输出标记的SQL，不连接数据库、不执行、不自动初始化。程序输出后仍需根据所属章节准备数据和会话。每个命名块在正文或对应实验页维护一份，导出和测试读取同一份内容。

### 自动运行目标数据库检查

自动检查会反复重置本目录拥有的练习表。不要连真实业务数据库。在仓库根目录运行 `python -m pip install -r curriculum/04-mysql/examples/requirements.txt`。其中 `rsa` 依赖用于现代密码认证；不要为运行课程把服务器改成旧认证模式。安装完成后设置：

```text
MYSQL_COURSE_HOST=127.0.0.1
MYSQL_COURSE_PORT=3307
MYSQL_COURSE_USER=course
MYSQL_COURSE_PASSWORD=你在本地设置的练习密码
```

这些变量在自己的终端配置，不写回仓库。运行：

```bash
python curriculum/04-mysql/examples/mysql_runtime_checks.py --confirm-reset handbook_mysql_lab
```

脚本仅允许连接本机，并核对服务器是MySQL 9.7.2或同系列更新维护版。数据与查询测试、双连接锁测试分别执行，报告服务器版本、测试数和失败项。没有PyMySQL、没有服务器、版本不符合或未确认重置时都会失败退出，**不会用跳过全部测试制造成功结果**。

测试不覆盖实际主从拓扑、断电、Binlog恢复、CDC平台和在线分片迁移；这些内容的正文时间线属于机制推演，真实部署需独立验收。
