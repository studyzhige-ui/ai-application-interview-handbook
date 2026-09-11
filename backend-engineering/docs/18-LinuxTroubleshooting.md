# 18. Linux Process / CPU / Memory / Disk / Port Troubleshooting

> 线上排障最重要的不是背命令，而是形成：**症状 → 资源 → 进程 → 依赖 → 最近变更 → 验证** 的顺序。

## 1. 先确认问题范围

用户说：

> 服务挂了。

先问：

```text
单实例？全部实例？
单接口？全部接口？
单 Tenant？全部用户？
单 Region？全局？
刚发布？突然流量？
```

范围决定排障方向。

---

## 2. 先看进程还活着吗

常用：

```bash
ps aux
ps -ef
pgrep -af myservice
```

如果进程不在：

- crash；
- OOMKilled；
- supervisor restart；
- deployment replacement。

如果进程在，也不代表能服务请求。

---

## 3. CPU 高怎么办

先看：

```bash
top
htop
ps -eo pid,ppid,cmd,%mem,%cpu --sort=-%cpu
```

然后区分：

```text
user CPU
system CPU
iowait
load average
```

CPU 高可能是：

- busy loop；
- parsing；
- compression；
- GC；
- excessive serialization；
- too many context switches；
- logging。

不要看到 CPU 100% 就直接扩机器。

---

## 4. Load Average

Load 不等于 CPU Usage。

它可以包含：

- 正在运行；
- 等待 CPU；
- 某些不可中断等待。

所以：

```text
high load + low CPU
```

也可能是 I/O 等待等问题。

---

## 5. Memory 高

常用：

```bash
free -h
ps aux --sort=-%mem
cat /proc/<pid>/status
```

关注：

- RSS；
- virtual memory；
- swap；
- page cache；
- container limit。

Linux `free` 里“used”不能简单理解成应用泄漏，因为 Page Cache 也会占内存。

---

## 6. OOM

Linux / Container 内存耗尽时可能触发 OOM Kill。

检查：

```bash
dmesg
journalctl
kubectl describe pod
```

典型 AI Backend 原因：

- 大文件一次性读内存；
- Queue 无限增长；
- Agent Context / result retained；
- per-worker client/model duplication；
- memory leak；
- request body / stream buffer。

---

## 7. Memory Leak vs High Working Set

### Leak

```text
traffic stable
memory continuously grows
never returns
```

### High Working Set

```text
traffic increases
memory increases
traffic falls
memory partly stabilizes/reuses
```

Python Allocator / GC / libc 还可能让 RSS 不立即下降。

所以不能只看“一次没降”就断言 Leak。

---

## 8. Disk 问题

常用：

```bash
df -h
du -sh *
iostat
```

典型：

- log 打满磁盘；
- temp file；
- Docker image / layer；
- Kafka / DB data；
- inode exhausted。

`df` 看 filesystem 使用；`du` 看目录文件大小，两者可能因 deleted-but-open file 等原因不一致。

---

## 9. Deleted but Open File

进程打开一个大日志文件后，文件被 `rm`：

```text
目录看不到
但进程 fd 仍持有 inode
```

磁盘空间不会立即释放。

可用：

```bash
lsof +L1
```

排查。

---

## 10. Port / Connection

常用：

```bash
ss -lntp
ss -ant
lsof -i :8000
```

问题：

- port not listening；
- too many connections；
- TIME_WAIT；
- SYN backlog；
- FD exhaustion。

AI Streaming 服务长连接多，更容易积累 Socket / FD。

---

## 11. File Descriptor

查看：

```bash
ulimit -n
ls /proc/<pid>/fd | wc -l
lsof -p <pid>
```

FD 用于：

- socket；
- file；
- pipe；
- event mechanism。

如果 Client/Response 没正确关闭，可能 FD Leak。

---

## 12. Network 排查

基础：

```bash
curl -v
ping
traceroute
ss
nslookup / dig
```

但不同环境可能禁 Ping，网络路径也可能经过 LB / Proxy / Mesh。

要区分：

```text
DNS
connect
TLS
server processing
read
```

这和 Timeout 章节的分层一致。

---

## 13. Process / Thread 数异常

```bash
ps -T -p <pid>
```

如果 Thread 持续增长：

- Thread leak；
- unbounded executor；
- SDK 每次创建 pool；
- blocking requests pile up。

Thread 数多也可能带来：

- memory stack；
- context switch；
- scheduler overhead。

---

## 14. Container 里的“机器资源”

容器看到的资源受到 cgroup 限制。

Host 有 64GB，不代表 Pod 可以用 64GB。

要看：

```text
requests / limits
cgroup CPU quota
memory limit
OOMKilled
throttling
```

所以排障时必须确认运行边界。

---

## 15. 最近变更优先

Production Regression 高概率和 Change 有关：

```text
new deploy
config change
model version
traffic shift
dependency change
schema migration
```

排障时一定要对齐 Timeline。

---

## 16. AI 场景：P99 突然升高

推荐链：

```text
P99 up
↓
QPS / errors changed?
↓
queue / pool wait?
↓
CPU / memory / FD?
↓
DB / Redis / Provider / Model latency?
↓
new release / config?
↓
trace slow samples
```

不要直接 SSH 上去 `top` 一顿看，没有 Hypothesis。

---

## 17. 常见命令不是知识点本身

你可以不会所有参数，但要知道：

| 问题 | 工具方向 |
|---|---|
| Process | ps / top |
| CPU | top / pidstat / perf（进阶） |
| Memory | free / proc / smem |
| Disk | df / du / iostat / lsof |
| Network | ss / curl / dig |
| Log | journalctl / app logs |
| Container | docker / kubectl / cgroup metrics |

---

## 18. 🎯 面试怎么答

**问：Linux 线上服务 CPU 100% 怎么排查？**

可以回答：

> 先确认影响范围和最近变更，再用 top/ps 定位进程与线程，区分 user/system/iowait 和 load。然后结合应用 Trace 看是不是某个接口、解析任务、GC 或 busy loop。还要检查流量是否突增、Thread/Queue 是否异常以及下游是否导致 spin/retry。定位后通过 Profile/日志/版本对比验证，而不是直接重启。

---

## 19. ⚠️ 易错点

- Load Average ≠ CPU Usage；
- Linux used memory ≠ 全部应用泄漏；
- 进程活着 ≠ 服务 Ready；
- `rm` 大日志 ≠ 磁盘立即释放；
- Host Resource ≠ Container 可用 Resource；
- 重启能恢复 ≠ 找到 Root Cause。

---

## 20. 本章自测

<details>
<summary>1. `df` 很满但 `du` 找不到大文件，可能是什么？</summary>

可能是文件已删除但仍被某进程打开，inode/blocks 仍被 FD 引用。可用 `lsof +L1` 排查。

</details>

<details>
<summary>2. 为什么 Container 里的 OOM 不能只看 Host 还有多少内存？</summary>

容器受 cgroup memory limit 约束，即使 Host 有空闲内存，Pod/Container 超过自己的限制仍可能 OOMKilled。

</details>

<details>
<summary>3. 为什么排障要先看最近变更？</summary>

很多 Regression 与新版本、配置、模型、依赖或流量变化直接相关。Change Timeline 能快速缩小 Hypothesis 空间。

</details>