# 25｜Fork、Branch 与 Replay

## 1. 为什么 Agent 需要 Fork

有些任务希望从同一状态尝试不同方案：

```text
Checkpoint C
├─ branch A：方案 A
└─ branch B：方案 B
```

或者 spawn subagent 时继承一部分 parent context。

## 2. Fork 到底继承什么

必须明确：

```text
instructions snapshot?
conversation history?
working state?
credentials?
permission decisions?
memory?
workspace?
budget?
```

不能简单 `deepcopy(session)`。

Codex 固定 commit 的 ThreadInstructionsProvider 变更甚至专门区分 live fork / subagent 对 applied snapshot 与 source provider 的继承，这非常能说明继承语义必须显式设计。

## 3. Replay

Replay 不是简单重发 messages：

- 外部 Tool 不应默认再次真实执行；
- 时间 / 网络结果会变化；
- nondeterministic model 会变化。

因此常见两类：

```text
Event Replay   重建 Runtime State
Eval Replay    固定/Mock Tool Evidence 重新跑模型
```

## 4. Branch Merge

Multi-Agent 或探索分支最终需要汇总，但不要把两个完整 histories 全拼回主 Context。应汇总 artifact / result / evidence。

## 🎯 面试

Fork 要定义 state、instruction、workspace、permission、budget 的继承规则；Replay 要区分“重建状态”和“重新执行副作用”。如果没有这些协议，分支和恢复会产生难以发现的重复动作。

<details><summary>自测：为什么 Fork 不该继承所有 permission decision？</summary>

因为授权可能只针对 parent run 的具体动作或环境；跨 branch 自动继承会扩大权限范围。
</details>
