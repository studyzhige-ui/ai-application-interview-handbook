# 12｜Side Effect、Concurrency Safety 与 Destructive Tool

## 1. Tool 风险不是二元的

可以按副作用分层：

```text
Pure / Read-only
Idempotent Write
Reversible Write
Irreversible / External Side Effect
```

例如：

- grep：read-only；
- set cache key：通常可覆盖；
- git commit：可追踪但影响 workspace；
- transfer_money：外部不可随便重放。

Claude Code `Tool.ts` 直接区分 read-only、destructive 和 concurrency-safe，这类 metadata 是成熟 Runtime 的重要输入。

## 2. Concurrency Safety

两个 Tool 能不能并行，不只是“都是 async”：

```text
Read file A + Read file B      通常安全
Write file A + Write file A    冲突
Run tests + modify same repo    结果可能不稳定
```

Runtime 需要资源层信息，而不是只看函数名。

## 3. Side Effect Ledger

对于高风险动作，可以记录：

```text
intent
idempotency_key
status
external_resource_id
started_at
completed_at
```

这样 Checkpoint 恢复时不会凭 message 猜动作是否已完成。

## 4. Destructive ≠ 一律禁止

正确策略往往是：

```text
classify risk
→ stronger approval
→ narrower sandbox / credential
→ verify result
```

## 🎯 面试

我会给 Tool 明确 side-effect 和 concurrency metadata。只读、幂等写、可逆写、外部不可逆动作的 retry/approval 完全不同；并发执行还要按 workspace/resource 冲突判断，而不是看到 async 就 `gather`。

<details><summary>自测：两个不同 Tool 为什么也可能不并发安全？</summary>

它们可能写同一个文件、数据库行、浏览器 session 或外部资源。并发安全取决于共享资源，不取决于函数是否同名。
</details>
