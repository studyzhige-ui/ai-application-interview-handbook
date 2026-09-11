# 02. TCP、TLS 与 HTTP/1.1 / HTTP/2 / HTTP/3

> 这一章不要求你成为网络协议工程师，而是建立 AI Backend 面试和故障排查需要的**服务通信心智模型**。

## 1. 先看一条完整链路

访问：

```text
https://api.example.com/chat
```

可以粗略展开为：

```text
DNS
↓
IP
↓
Transport Connection
↓
TLS
↓
HTTP
↓
Application
```

每层解决的问题不同。

---

## 2. DNS 解决什么

DNS 把域名解析成可访问的地址。

```text
api.example.com
→ DNS Resolve
→ IP
```

Production 中 DNS 还可能参与：

- 服务入口切换；
- Region 路由；
- Load Balancing；
- Failover。

⚠️ DNS 不是“实时强一致服务发现”。TTL、缓存、递归解析链都意味着变化传播存在时间窗口。

---

## 3. TCP vs UDP

| 维度 | TCP | UDP |
|---|---|---|
| 连接语义 | 面向连接 | 无连接 |
| 顺序 | 保证字节流顺序 | 不保证 |
| 丢包恢复 | 有 | 应用自己处理 |
| 拥塞控制 | 有 | 协议本身不提供同等语义 |
| Header/状态成本 | 更高 | 更轻 |
| 常见场景 | HTTP/1.1、HTTP/2、DB、RPC | 实时音视频、QUIC 底层等 |

不要简单说：

> UDP 快，TCP 慢。

真实 Trade-off 是：

```text
可靠性 / 顺序 / 拥塞控制 / 连接状态
vs
实时性 / 应用自定义恢复 / 协议灵活性
```

---

## 4. TCP 三次握手为什么不是两次

简化理解：双方需要确认：

```text
Client 能发
Server 能收
Server 能发
Client 能收
```

并建立双方认可的初始序列状态。

```text
Client          Server
  | SYN ----------> |
  | <------ SYN+ACK |
  | ACK ----------> |
```

面试重点不是背 Flag，而是理解：

> 连接建立需要双方确认彼此收发能力与序列状态。

---

## 5. TCP Reliable Delivery

TCP 的可靠性来自多种机制协作，例如：

- Sequence Number；
- ACK；
- Retransmission；
- Flow Control；
- Congestion Control。

### Retransmission

网络没有收到预期 ACK 时可能重传。

这说明一个重要事实：

> 网络层“可靠传输”不等于业务层“Exactly Once”。

假设客户端发送支付请求：

```text
Server 扣款成功
↓
Response 丢失
↓
Client timeout
↓
Client retry
```

TCP 并不能替你解决“是否重复扣款”。

后面仍需要业务 Idempotency。

---

## 6. 四次挥手与半关闭

TCP 双向字节流两个方向可以独立关闭，所以连接终止不是简单“一次 Goodbye”。

这也解释为什么真实服务里会出现：

- 客户端已经断开；
- 服务端仍有任务运行；
- 一侧写失败；
- 中间 Proxy 超时；
- Half-open Connection。

Streaming Service 要特别关注这种状态。

---

## 7. TLS 解决什么

HTTP 本身不提供安全通信。

HTTPS 可以理解为：

```text
HTTP
↓
TLS Secure Channel
↓
TCP / QUIC
```

TLS 主要提供：

- Confidentiality；
- Integrity；
- Peer Authentication（典型 Web 场景验证 Server）。

---

## 8. 对称加密与非对称加密怎样协作

大致思路：

```text
Certificate / Public Key Mechanism
→ 验证身份、建立共享秘密
→ Session Key
→ 大量数据使用高效对称加密
```

为什么不全程只用非对称加密？

因为对称加密更适合高吞吐数据传输。

为什么不能只有对称密钥？

因为初次安全交换密钥与认证对方身份仍需要额外机制。

---

## 9. Certificate Trust Chain

浏览器或 Client 不是看到一个证书就“自动相信”。

简化：

```text
Server Certificate
→ Intermediate CA
→ Trusted Root CA
```

Client 还会检查：

- Hostname；
- Validity；
- Signature Chain；
- Policy / Algorithm 等。

---

## 10. HTTP/1.1

典型优势：成熟、简单、兼容广。

长连接允许 Connection Reuse，避免每个请求重新建立 TCP/TLS。

但一个 Connection 上请求并发能力有限，应用常通过连接池维护多个连接。

---

## 11. HTTP/2

HTTP/2 一个核心能力是 Multiplexing：

```text
one TCP connection
├─ stream A
├─ stream B
└─ stream C
```

多个 HTTP Stream 可以并发复用一个 TCP Connection。

但底层仍是 TCP 字节流。

如果发生底层 Packet Loss，TCP 仍需要按自己的可靠传输规则恢复，因此不同 HTTP/2 Stream 仍可能共同受同一个 TCP Connection 的传输问题影响。

---

## 12. HTTP/3 / QUIC

HTTP/3 通常运行在 QUIC 之上，而 QUIC 建在 UDP 之上，但它自己实现：

- Reliable Streams；
- Congestion Control；
- Encryption integration；
- Connection migration 等能力。

所以不能说：

> “HTTP/3 用 UDP，所以不可靠。”

QUIC 在 UDP 之上提供自己的可靠传输语义。

---

## 13. AI Streaming 为什么关心 HTTP Version

长时间 Streaming Connection 常关注：

- Connection Establishment；
- Multiplexing；
- Proxy Support；
- Head-of-line Impact；
- Mobile Network Migration；
- Disconnect Detection。

但应用层仍然要自己设计：

```text
Event ID
Resume Cursor
Heartbeat
Business State
```

协议不会自动帮 Agent Run Resume。

---

## 14. Keep-Alive 的意义

如果每个 LLM Provider Request 都重新：

```text
TCP handshake
+ TLS handshake
+ request
```

会增加延迟与 CPU 成本。

所以 HTTP Client 通常通过 Connection Pool / Keep-Alive 复用连接。

这也是后面 Connection Pool 章节存在的原因。

---

## 15. Failure Timeline

假设 AI Service 调外部 Provider：

```text
DNS slow
→ TCP connect 2s
→ TLS 300ms
→ provider queue 5s
→ first byte 4s
→ stream 20s
```

如果只设置一个“30 秒 Timeout”，你很难知道到底是哪一阶段慢。

后面会拆成：

```text
connect timeout
read timeout
overall deadline
```

---

## 16. 🎯 面试怎么答

**问：HTTP/2 与 HTTP/3 核心区别？**

可以回答：

> HTTP/2 通过一个 TCP Connection 多路复用多个 Stream，但底层仍受 TCP 字节流和连接级丢包恢复影响；HTTP/3 基于 QUIC，QUIC 运行在 UDP 之上并自己实现可靠 Stream、拥塞控制和安全握手等能力，因此可以减少不同应用 Stream 之间的底层阻塞耦合。实际选型还要考虑客户端、代理、基础设施支持，而不是只看理论延迟。

---

## 17. ⚠️ 易错点

- UDP ≠ 永远更快；
- HTTP/3 基于 UDP ≠ 不可靠；
- TLS ≠ “只用非对称加密”；
- TCP Reliability ≠ Business Idempotency；
- Keep-Alive ≠ Connection 永不关闭。

---

## 18. 本章自测

<details>
<summary>1. 为什么 TCP 已经可靠，支付 API 仍然需要幂等？</summary>

TCP 只能保证连接中的字节可靠传输。Server 执行业务成功但 Response 丢失时，Client 无法知道结果，Retry 可能再次触发业务副作用，因此仍需要应用层幂等。

</details>

<details>
<summary>2. 为什么 HTTP/3 基于 UDP 仍可以可靠？</summary>

因为 UDP 只是提供 Datagram Transport，QUIC 在其上实现自己的可靠 Stream、重传、拥塞控制与安全机制。

</details>

<details>
<summary>3. AI Streaming 的 Resume 为什么不能只依赖 TCP 重连？</summary>

TCP 只恢复新的连接，不知道业务 Event 已经发送到哪里，也不知道 Agent Run 的 durable state。应用仍需 Event ID、Cursor、Run State 等业务协议。

</details>