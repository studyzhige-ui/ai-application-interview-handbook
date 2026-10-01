# 09｜认证、授权与租户：让访问范围可信

[← 上一章](08-WebSocket与EventProtocol.md) · [模块主页](../README.md) · [下一章 →](10-ExternalResourceIntegration.md)

用户甲把地址里的笔记编号从 1 改成 2，竟然读到了用户乙的内容。接口的数据类型可能完全正确，漏洞仍然存在。因为“编号是整数”和“这个人有权读这条记录”不是同一个问题。

这一章把身份、权限和访问范围接到已学过的依赖系统上。例子只使用公开的教学口令，不实现生产登录系统；目标是让允许与拒绝的规则可以被亲手验证。

## 1. 先分别回答“是谁”和“能做什么”

**认证（Authentication）** 确认请求对应哪个身份。**授权（Authorization）** 决定这个身份能否对某项资源执行某种操作。

一个令牌格式正确，不代表令牌可信；令牌可信，也不代表它持有者可以读取所有笔记。实际步骤是：提取凭证、验证凭证、建立身份，再根据身份和目标资源检查权限。

`HTTPBearer` 能帮你读取 `Authorization: Bearer ...`。**它本身不会替你验证任意 JWT 的签名、有效期、签发方或受众，也不会自动查出用户拥有哪些资源。** [FastAPI 安全教程](https://fastapi.tiangolo.com/tutorial/security/first-steps/)解释了安全依赖与 OpenAPI 的关系。

### 1.1 Bearer 是凭证使用方式，JWT 是一种凭证格式

`Authorization: Bearer <token>` 的关键是“持有这份 token 的一方能够代表它的权限使用它”。攻击者若拿到有效 token，也可能冒用，所以需要 HTTPS、有限有效期和不记录原文的日志策略。Bearer token 可以是随机、不透明的会话标识，也可以采用 JWT；两者不是同义词。

常见**签名 JWT 的紧凑格式**分为三段：

```text
base64url(header) . base64url(payload) . base64url(signature)
header：类型、算法与密钥标识等说明
payload：sub、iss、aud、exp 等 claims（声明）
signature：对前两段形成的签名或消息认证码
```

Base64url 是编码，不是加密；拿到 token 的人通常能读出 payload。签名用于检测内容被修改及验证来源，不负责保密；JWT 也存在加密形式，不能把“三段”泛化为所有 JWT。服务应按自己的可信配置选择允许算法和验证密钥，不能让来路不明的 header 决定任意算法或密钥地址。[JWT 规范](https://www.rfc-editor.org/rfc/rfc7519.html) · [JWT 安全实践](https://www.rfc-editor.org/rfc/rfc8725.html)

### 1.2 从 token 到 Principal，中间必须有验证

**Principal（已验证主体）** 是应用认可的身份，例如用户 u1 及其可信访问范围。下面是一条状态过程，不是可以直接复制的密码学实现：

```text
收到 Bearer token
→ 从受信任配置选择验证器，验证签名和允许算法
→ 验证 iss（谁签发）、aud（给谁用）、exp（是否到期）、必要的 nbf 等声明
→ 验证本应用要求的字段存在且类型正确
→ 将 sub 对应到当前有效用户，检查停用/撤销及成员关系
→ 得到 Principal(user=u1, tenant=team-a)
→ 检查这次动作和目标资源是否允许
```

签名正确却 aud 指向另一个服务，仍不能用于当前 API；签名正确且尚未到期，也可能因用户已停用或权限变更而需要拒绝。不要先解码 payload 就信任其中的 `tenant_id`。成熟库负责密码学验证，应用仍负责声明规则、可信密钥来源和用户状态。

过期只限制 token 的自然寿命，不自动实现提前撤销。需要即时撤销时，可以检查会话/撤销记录或用户版本；短期 access token 配合受控刷新流程则限制失窃后的时间窗口。JWT 不是天然“无状态又即时撤销”的双重保证。密码登录入口还应使用专门密码哈希算法验证密码、限制尝试频率；不是把明文密码直接用作长期 API token。

### 1.3 Session、Cookie 与 token 不在同一层

| 概念 | 负责什么 | 状态位置与代价 |
|---|---|---|
| 服务端 Session | 保存登录会话及当前状态 | 客户端携带不透明会话 ID，服务端查询，可集中撤销 |
| 签名 token | 携带可验证声明 | 可在本地验证，权限更新与撤销仍需额外策略 |
| Cookie | 浏览器保存并按范围自动发送值 | 可以承载会话 ID，也可以承载 token；不是认证算法 |

所以“Cookie 还是 JWT”不是完整二选一：JWT 也能放 Cookie 中，Session ID 也能放 Authorization 中。选择时要同时说明凭证格式、保存位置、发送方式、有效期与撤销。Backend 将进一步展开[认证与会话](../../05-backend-engineering/docs/15-AuthSession与TenantBoundary.md)；这里先把身份如何进入 FastAPI 的依赖链讲清楚。


## 2. 让身份成为函数的显式输入

下面用一个很小的字典模拟认证服务。两个字符串都是公开测试数据，不能用于真实系统。

```python
# example: auth_app
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from pydantic import BaseModel

app = FastAPI()
bearer = HTTPBearer(auto_error=False)

class User(BaseModel):
    id: str
    tenant_id: str

USERS = {
    "demo-alice": User(id="alice", tenant_id="team-a"),
    "demo-bob": User(id="bob", tenant_id="team-b"),
}
NOTES = {
    1: {"tenant_id": "team-a", "text": "甲团队的笔记"},
    2: {"tenant_id": "team-b", "text": "乙团队的笔记"},
}

def current_user(
    credentials: Annotated[HTTPAuthorizationCredentials | None, Depends(bearer)],
) -> User:
    user = USERS.get(credentials.credentials) if credentials else None
    if user is None:
        raise HTTPException(401, "需要有效凭证", headers={"WWW-Authenticate": "Bearer"})
    return user

CurrentUser = Annotated[User, Depends(current_user)]

@app.get("/notes/{note_id}")
def read_note(note_id: int, user: CurrentUser):
    note = NOTES.get(note_id)
    if note is None or note["tenant_id"] != user.tenant_id:
        raise HTTPException(404, "笔记不存在或不可访问")
    return {"id": note_id, "text": note["text"]}
```

`HTTPBearer` 提取请求头后，把凭证对象传给 current_user。`credentials.credentials` 是实际的 token 文字；USERS 用它查找教学身份。`auto_error=False` 让缺少凭证的情况也交给 current_user，统一返回本例的 401。

| 请求条件 | 预期结果 | 解释 |
|---|---|---|
| 没有 Authorization | 401 | 尚未获得可信身份 |
| `Bearer wrong` | 401 | 教学认证源不接受该口令 |
| `Bearer demo-alice`，读取 1 | 200 | 同一团队，允许读取 |
| `Bearer demo-alice`，读取 2 | 404 | 本例不向其他团队暴露资源是否存在 |
| `Bearer demo-bob`，读取 2 | 200 | 同一团队，允许读取 |

可以在 `/docs` 中使用 Authorize，填入教学 token 后调用；也可以在测试中发送请求头。选择 404 是本例的资源隐藏策略，不是所有禁止访问都必须返回 404。明确存在、但不允许执行的操作也常使用 403。

## 3. 租户范围必须来自可信关系

租户可以理解为拥有相对独立数据范围的团队或组织。这个例子只允许用户读取所属团队的数据。

客户端即使发送 `X-Tenant-ID: team-b`，也不应因此变成 team-b 成员。可信范围来自通过验证的身份与后端成员关系；多团队用户选择目标团队时，还需要验证其成员资格。

身份继续传到服务和数据访问层：

```text
验证凭证 → User / TenantContext
                  ↓
         检查当前资源与动作
                  ↓
         带可信范围读取数据
                  ↓
         过滤输出，返回允许内容
```

> ⚠️ 不要把 `current_user` 或 `current_tenant` 放到应用全局变量中。两个请求交错执行时可能读到对方的身份。请求范围的数据通过参数、依赖结果或 request.state 传递；共享客户端才适合应用范围。

## 4. 结构校验和权限检查谁先做

它们共同组成边界，但不必硬背一个所有请求通用的总顺序。路由匹配、参数解析和依赖求值有框架执行关系；业务上必须保证的是：**在访问受限内容或产生副作用之前，身份和授权已经完成。**

不能先把另一租户的材料发送给模型，再在输出页面隐藏它。缓存和向量索引也不例外：键里带租户前缀有帮助，但调用者仍必须无法伪造访问范围。

### 4.1 有权访问，不等于有权替用户确认高风险动作

用户可能有权阅读笔记，但删除整组资料还需要更强权限，甚至需要再次确认。这里要分别核对**身份、动作权限和本次操作意图**。只有业务风险要求时才引入额外确认，不是所有写请求都要弹窗。

例如应用决定批量删除前必须确认，页面应展示将删除哪些资料。确认结果由服务端绑定到用户、目标集合、动作和有效期；执行时再次核对。用户确认删除 A 后，不能把同一确认拿来删除 B。目标或关键参数变化，就应使旧确认失效。[OWASP 事务授权建议](https://cheatsheetseries.owasp.org/cheatsheets/Transaction_Authorization_Cheat_Sheet.html)说明了授权与具体操作绑定的必要性。

FastAPI 可以承接请求、身份依赖和确认结果，但不能让模型自己生成一个 `confirmed=true` 就绕过后端检查。需要审计或跨重启恢复时，确认记录与任务执行要由持久状态共同承载。

## 5. CORS 管什么，不管什么

浏览器页面所在的来源由协议、主机和端口共同决定。例如 `http://localhost:5173` 与 `http://localhost:8000` 是不同来源。CORS 让服务器声明哪些来源的浏览器脚本可以读取跨源响应。

```python
# example: cors_app
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["Authorization", "Content-Type"],
)

@app.get("/hello")
def hello():
    return {"message": "hello"}
```

这不是给 `hello` 增加登录要求。没有浏览器 CORS 约束的 HTTP 客户端仍可以请求它。CORS 也不能替代 Cookie 身份下的 CSRF 防护。

某些跨源请求会先发送 **OPTIONS 预检**。例如前端要带 Authorization 发 POST，浏览器先询问：“这个来源能用 POST 和这个请求头吗？”允许后才继续原请求。

测试预检时要提供 `Origin`、`Access-Control-Request-Method` 以及所需的请求头声明，才是在模拟这个询问；普通空 OPTIONS 不是同一件事。

> ⚠️ 启用凭据的跨域交互应明确列出允许的来源、方法和请求头，不直接复制通配配置。`localhost` 与 `127.0.0.1` 也不是同一个主机名，配置必须匹配实际前端地址。

### 浏览器自动带 Cookie，为什么会出现 CSRF

设用户已经登录笔记网站，浏览器保存了它的认证 Cookie。之后用户打开恶意页面，页面诱导浏览器向笔记网站发送一次修改请求；在满足 Cookie 发送规则的情况下，浏览器会自动附带凭证。服务器若只看到“有 Cookie”就执行，会把第三方页面触发的动作误当成用户本意。这就是跨站请求伪造（CSRF）的核心因果。

防护需要验证请求来源和操作意图：状态改变不使用 GET；按实际跨站需求配置 SameSite；校验 Origin/必要时 Referer；使用服务端验证、攻击页面不能取得或伪造的 CSRF token。SameSite 是重要的纵深防护，但 site 与 origin 不同：同为 HTTPS 的 app.example.com 与 api.example.com 可属于同一 site，却因主机不同而不同源。不能把 SameSite 独自当成覆盖所有情形的防线。HttpOnly 限制脚本读取 Cookie，Secure 限制通过 HTTPS 发送，都不证明这次请求由用户主动发起。[OWASP CSRF 防护](https://cheatsheetseries.owasp.org/cheatsheets/Cross-Site_Request_Forgery_Prevention_Cheat_Sheet.html)

CORS 主要控制跨源脚本能否读取响应，不能仅因恶意页面读不到响应，就推断修改请求一定没有发生。显式 Authorization 请求头通常不会被浏览器自动附到跨站表单，因此与自动 Cookie 的 CSRF 暴露面不同；但凭证若被脚本窃取，又是另一类问题。WebSocket 握手也需核对身份和允许的 Origin，不能用普通 CORS 中间件代替。


## 6. 不可信输入与秘密应在哪一层处理

安全不止登录。需要把风险落实到具体边界：

- 请求结构：限制长度、数量、字段和文件大小，拒绝不合法输入。
- 数据访问：检查资源所属范围和动作权限，必要时在查询中再限制范围。
- 外部调用：不要把用户提供的任意地址直接作为服务器请求目标。
- 日志与响应：不输出 Authorization、密码、私钥和带秘密的连接字符串。

排错时可以记录 request_id、错误类别和经过筛选的上下文，而不是默认记录全部正文。发生凭证泄露时应吊销或轮换；仅删除最新文件不能消除已泄露的历史。

## 7. 用拒绝实验检查设计是否真实生效

成功请求只能说明存在一条可用路径。权限实验必须主动交换身份和资源：Alice 读取 Bob 的资源、伪造租户请求头、使用无效 token、取消身份凭证、访问不存在的对象。

**身份输出例子：** `/me` 可以直接依赖 CurrentUser 并返回 `{"id": user.id, "tenant_id": user.tenant_id}`。缺凭证时依赖先给出 401；身份有效时只公开 ID 与团队，不把原始 token 放入响应。token 是凭证，不是应公开的用户资料。

---

## 本章小结

认证建立可信身份，授权决定具体动作的访问范围。类型校验、CORS 和输出过滤都很重要，但不能相互替代。安全规则必须通过允许与拒绝的请求共同验证。

## 🎯 面试怎么回答

**HTTPBearer 是否已经完成 JWT 校验？**

> 没有，它主要提取 Bearer 凭证并参与接口声明。具体签名、有效期、签发方、受众及身份关系需要验证器负责。

**多租户接口怎样防止用户修改 tenant_id 越权？**

> 从已验证身份确定成员关系，检查资源与动作，向数据和服务层传递可信范围。客户端选择的 tenant_id 不能直接成为授权依据。

## ⚠️ 易错点

> ⚠️ 认证通过不等于授权通过；读取和删除同一对象也可能需要不同权限。

> ⚠️ CORS 是浏览器跨源访问机制，不是接口的登录防线，也不阻止普通服务端客户端。

> ⚠️ 测试 token 是公开教学输入，不能复制成部署用的硬编码密钥。

## 本章自测

先回答，再展开核对。结合正文例子，说出预期结果及原因即可。

<details>
<summary>1. Alice 为什么读笔记 2 得到 404 而不是 200 后隐藏正文？</summary>

服务端在交付受限内容前拒绝，并用 404 降低资源存在性泄露；拒绝策略应明确且一致。

</details>

<details>
<summary>2. 配置 CORSMiddleware 后是否可以删除 current_user？</summary>

不可以，两者解决不同问题。

</details>

<details>
<summary>3. 缓存键带 tenant_id 就一定不会越权吗？</summary>

不一定。若 tenant_id 可以任意伪造，前缀仍会导向其他团队数据；可信身份与范围检查必须存在。

</details>

## 知识回看与权威资料

- [安全依赖](https://fastapi.tiangolo.com/tutorial/security/first-steps/)：了解凭证提取和 OpenAPI 安全声明。
- [CORS](https://fastapi.tiangolo.com/tutorial/cors/)：核对来源、预检、凭据和允许项。
- [安全工具参考](https://fastapi.tiangolo.com/reference/security/)：核对 auto_error 和凭证对象。

真人问题回看：[S288 的读写权限与用户确认](../../../market/interviews/batch-29.md)、[S294 的 CORS](../../../market/interviews/batch-33.md)。这些问题加深的是已有访问边界，不需要另外增加一套安全术语课程。
