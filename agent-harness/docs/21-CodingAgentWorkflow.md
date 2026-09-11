# 21. Coding Agent：Repo Understanding → Patch → Test → Verify

Coding Agent 不是：

> “让 LLM 写代码。”

真正的工程闭环是：

```text
Understand Repository
→ Understand Task
→ Locate Relevant Code
→ Plan Minimal Change
→ Edit / Patch
→ Run Test / Lint / Typecheck
→ Inspect Diff
→ Fix Regression
→ Verify Acceptance Criteria
→ Deliver
```

HUMAN-A 中 `AGENT-048 AI-assisted Development Workflow` 有 37 个独立来源，说明企业已经把“AI Coding 怎么真正进入研发流程”当成核心能力，而不只是 Copilot 使用技巧。

---

## 1. Coding Agent 最大的问题不是生成，而是理解和验证

模型很容易生成：

```text
看起来合理的 patch
```

但它可能：

```text
改错文件
漏掉调用方
破坏接口
测试没跑
只修表面症状
```

所以 Harness 要提供的不只是 `edit_file`，还要有：

```text
repo discovery
search
navigation
workspace state
command execution
diff
test
verification
```

---

# 2. Repository Understanding 不等于 Vector RAG

HUMAN-A `AGENT-037` 直接比较：

```text
Vector RAG
AST / LSP
ripgrep / Filesystem Search
Dependency Graph
```

它们解决不同问题。

## ripgrep / Text Search

适合：

```text
符号名
错误字符串
配置项
调用痕迹
```

优点：快、精确、成本低。

## Filesystem Navigation

适合：

```text
项目结构
模块边界
配置文件位置
```

## AST / LSP

适合：

```text
definition
reference
type
symbol relationship
```

## Vector / Semantic Search

适合：

```text
不知道具体关键词
按语义找相关实现
```

## Dependency Graph

适合：

```text
impact analysis
跨模块依赖
```

成熟 Coding Agent 通常组合，而不是只靠一种检索。

---

# 3. Repo Understanding 的搜索漏斗

建议：

```text
1. Read task / issue
2. Inspect repo tree
3. Exact text / symbol search
4. Read local neighborhood
5. Follow references / dependency
6. Semantic search only when useful
7. Build small working set
```

不要一开始：

```text
把整个 repo 全塞 Context
```

Context Engineering 原则同样适用。

---

# 4. Patch 应尽量小

目标：

```text
minimal sufficient change
```

而不是：

```text
顺手重构全项目
```

小 Patch 的优势：

- Review 容易；
- Regression Surface 小；
- 失败更容易归因；
- Rollback 简单；
- Test 范围更明确。

Planning 时可以显式限制：

```text
Non-goal: 不做无关重构
```

---

# 5. Workspace State 必须可控

Coding Agent 需要知道：

```text
base commit
current branch
modified files
untracked files
running processes
```

如果没有清晰 workspace boundary：

```text
上一次任务残留修改
→ 被下一次任务误认为原始代码
```

所以每个 Run 最好有：

```text
workspace identity / snapshot
```

---

# 6. Patch Application 要有前置版本

如果 Agent 读到：

```text
file version A
```

准备 Patch。

但期间文件变成 B：

```text
直接覆盖
→ Lost Update
```

更安全：

```text
base hash / line context
→ apply patch
→ conflict if base changed
```

Multi-Agent 场景尤其重要。

---

# 7. Test 是 Outcome Verification，不是装饰

HUMAN-A `AGENT-036 Code Verification` 有 24 个独立来源。

最低验证层：

```text
syntax / compile
unit test
typecheck
lint
integration test
```

具体跑哪些取决于 Repository。

Agent 不能只说：

> “修改应该能工作。”

必须尽量执行可以独立验证的检查。

---

# 8. Test Failure 怎么处理

不是：

```text
Test fail
→ 修改到 test 变绿
```

因为 Agent 可能“修测试”来掩盖 bug。

需要先分类：

```text
existing failure?
caused by patch?
flaky?
environment issue?
expectation changed legitimately?
```

如果要修改 Test：

```text
必须说明为什么 expectation 应改变
```

---

# 9. Diff Review 是另一道防线

Tests 全过也可能出现：

```text
删除日志
放宽权限
绕过验证
加入 hardcoded secret
```

所以最终要：

```text
git diff
→ inspect changed files
→ check scope
→ check unexpected deletion
→ check security
```

Human Review 可以建立在 Diff 上，而不是重新读整个仓库。

---

# 10. Acceptance Criteria 必须独立于 Agent 自评

例如 Issue：

```text
修复 retry 时重复扣款
```

完成标准应该是：

```text
new regression test reproduces old bug
patch makes test pass
existing tests pass
no duplicate external call
```

而不是：

```text
Agent: “我已解决重复扣款问题。”
```

SWE-bench 的重要启发正是：

> 用真实 repository environment 和测试结果判断问题是否真正解决。

---

# 11. Verification Pyramid

可以从便宜到贵：

```text
Parse / Compile
→ Static Analysis / Typecheck
→ Targeted Unit Test
→ Related Test Suite
→ Integration / E2E
→ Full Regression
```

不是每次都跑完整 E2E，但高风险修改应该逐层提高验证强度。

---

# 12. Command Execution 的风险

Coding Agent 需要 shell：

```text
pytest
npm test
git diff
```

但 shell 也是高风险 Tool。

必须结合：

```text
Permission
Sandbox
Network Policy
Timeout
Output Offloading
```

例如不允许测试脚本：

```text
访问 production DB
```

---

# 13. AI-assisted Development 中人的责任

健康流程：

```text
Human owns requirement / acceptance / risk
Agent accelerates discovery / patch / test
Runtime records evidence
Human reviews high-impact decision
```

不是：

```text
Agent 写代码
→ Human 只点 Merge
```

也不是：

```text
Agent 只能补全几行代码
```

责任边界取决于可验证性和风险。

---

# 14. Rollback / Delivery

交付前至少保留：

```text
base commit
final diff
test evidence
run trace
artifact / patch id
```

如果上线后有问题：

```text
能定位这次 Agent 修改
→ revert / rollback
```

这也是 Agent Trace 与普通开发审计连接的地方。

---

# 15. Claude Code / Codex 为什么是重要实现参考

这两个产品本身就是成熟 Coding Agent，因此我们从源码索引中抽象：

```text
filesystem / search / tool runtime
workspace / session
permission / sandbox
cancellation
trace
context management
```

但课程不复制某一产品 UI 或类名。

真正要学的是：

> **一个 Coding Agent 要完成可交付代码修改，Runtime 必须提供哪些闭环能力。**

---

# 16. Coding Agent Failure Timeline

```text
T0  Agent 搜到相似函数 A
T1  未继续查真实调用方 B
T2  修改 A
T3  只跑了单个 unit test
T4  Test pass
T5  上线后 B 仍走另一条路径
T6  Bug 仍存在
```

根因：

```text
Repo Understanding + Acceptance Verification 不完整
```

不是“模型代码能力差”。

---

# 17. HUMAN-A 信号

本章主要承接：

- `AGENT-036` Code Verification：24 个来源；
- `AGENT-037` Repository Understanding：9 个；
- `AGENT-048` AI-assisted Development Workflow：37 个。

真实面试很可能直接问：

```text
你用 AI Coding 怎么保证代码质量？
为什么不用纯 Vector RAG 理解 Repo？
AI 写完代码你怎么验收？
```

---

# 18. 面试怎么答

## Q：AI Coding 怎么保证质量？

🎯 **30 秒回答**：

> 我把 Coding Agent 看成完整工程循环，不是代码生成器。先通过 tree/ripgrep/symbol/AST/LSP/语义搜索建立最小相关工作集；Patch 尽量小并绑定 base version；修改后跑 compile/typecheck/targeted tests，再看 diff 和影响范围，必要时跑 integration/regression；最终按独立 Acceptance Criteria 验证，而不是相信 Agent 说“完成”。高风险命令还必须经过 sandbox/permission，所有 test/diff 证据进入 trace 方便 review 和 rollback。

---

# 19. 高频易错点

⚠️ **Repo Understanding = Vector RAG。** 代码有强 symbol / dependency / filesystem 结构。

⚠️ **Test 过了就一定正确。** Test coverage 可能不足，还要看 Diff / Acceptance。

⚠️ **Agent 可以直接改测试让它通过。** 必须验证 expectation 是否合理变化。

⚠️ **AI-assisted Development = 人不再 Review。** 责任边界没有消失。

---

# 20. 本章自测

<details><summary>1. 为什么 Coding Agent 不应该一开始把全仓库塞进 Context？</summary>

成本和噪声都高，而且代码导航有更强的结构化信号。应先用 tree、exact search、symbol/reference 等缩小工作集，再按需读文件。
</details>

<details><summary>2. 为什么 Test 和 Diff 都需要？</summary>

Test 验证行为，Diff 验证修改范围与潜在风险；两者能发现不同类型问题。
</details>

<details><summary>3. SWE-bench 对 Coding Agent Evaluation 最大启发是什么？</summary>

最终应该在真实 repository environment 中验证 issue 是否被解决，而不是只评价生成代码文本看起来是否合理。
</details>
