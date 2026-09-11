#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

CALLOUTS = {
    "system-design/docs/06-Cache与HotPath.md": """> **本章定位：System Design 组合层。** 这里训练的是“何时把 Cache 放进架构、Read/Write Path 怎样组合、Hot Path 与降级怎样决策”。Redis 的 Cache/TTL/击穿/雪崩机制回到 [Redis Cache Design](../../redis/docs/09-Cache设计与缓存故障.md)；跨 MySQL + Redis 的一致性机制回到 [AIBE Consistency & Compensation](../../backend-engineering/docs/13-Consistency与Compensation.md)。\n""",
    "system-design/docs/07-PartitionRouting与Fanout.md": """> **本章定位：System Design 组合层。** 这里关注“什么时候分片、按什么 Key 路由、Fan-out 与 Rebalance 如何影响系统”。具体存储内部机制分别回到 [MySQL Sharding](../../mysql/docs/19-Sharding.md)、[Redis Cluster](../../redis/docs/14-Cluster与HashSlot.md) 与 [Distributed Vector DB](../../vector-db/docs/13-分布式VectorDB.md)。\n""",
    "system-design/docs/08-Consistency与Idempotency.md": """> **本章定位：System Design 组合层。** 这里从业务 Invariant 出发选择 Transaction / CAS / Idempotency / Compensation。通用 Side-effect Safety 与跨系统一致性机制回到 [AIBE Idempotency](../../backend-engineering/docs/09-APIIdempotency与SideEffect.md) 和 [AIBE Consistency](../../backend-engineering/docs/13-Consistency与Compensation.md)；数据库事务内部机制回到 [MySQL](../../mysql/README.md)，Agent Tool 恢复语义回到 [Agent Checkpoint / Resume](../../agent-harness/docs/13-CheckpointResumeReliability.md)。\n""",
    "system-design/docs/09-QueueBackpressure与LongRunningTask.md": """> **本章定位：System Design 组合层。** 这里训练 Queue / Worker / Long-running Task 怎样进入整体架构。Backpressure、MQ Delivery 与 Durable Task 的完整机制分别回到 [AIBE Backpressure](../../backend-engineering/docs/06-Backpressure与RateLimit.md)、[AIBE MQ](../../backend-engineering/docs/10-MQ与DeliverySemantics.md) 和 [AIBE Reliable Async Task](../../backend-engineering/docs/12-ReliableAsyncTask.md)。\n""",
    "system-design/docs/10-Reliability与Overload.md": """> **本章定位：System Design 组合层。** 这里把 Deadline、Retry、Failover、Degradation、Load Shedding 组合成系统级 Failure Strategy；这些 Primitive 的完整机制与错误语义回到 [AIBE Timeout / Deadline](../../backend-engineering/docs/07-TimeoutDeadline与ErrorTaxonomy.md) 和 [AIBE Retry / Circuit Breaker / Failover](../../backend-engineering/docs/08-RetryCircuitBreaker与Failover.md)。\n""",
    "system-design/docs/11-MultiTenancy与Security.md": """> **本章定位：System Design 组合层。** 这里关注 Tenant / Permission / Security 怎样贯穿 State、Cache、Queue、Trace 与 Tool。HTTP/API 身份上下文回到 [FastAPI Security](../../fastapi/docs/09-Security与TenantContext.md)，通用 Auth / Backend Security 回到 [AIBE Auth](../../backend-engineering/docs/15-AuthSession与TenantBoundary.md) 与 [AIBE Security](../../backend-engineering/docs/21-BackendSecurity.md)，Agent 高风险动作回到 [Permission / Sandbox](../../agent-harness/docs/14-PermissionApprovalSandbox.md) 和 [Prompt Injection / Containment](../../agent-harness/docs/15-GuardrailsInjectionContainment.md)。\n""",
    "system-design/docs/12-ObservabilityEvaluation与Evolution.md": """> **本章定位：System Design 组合层。** 这里负责把 Observability、Evaluation、Cost 与 Evolution 组合成系统闭环。通用 Metrics/Logs/Trace 回到 [AIBE Observability](../../backend-engineering/docs/17-Observability与PerformanceDiagnosis.md)；Retrieval / End-to-end Quality 回到 [RAG Evaluation](../../rag/docs/10-RetrievalEvaluation.md) 与 [RAG Quality Engineering](../../rag/docs/11-EndToEndQualityEngineering.md)；Agent Trace / Eval 回到 [Agent Trace](../../agent-harness/docs/19-TraceReplayObservability.md) 与 [Agent Evaluation](../../agent-harness/docs/20-AgentEvaluationBenchmark.md)。\n""",
}

for rel, callout in CALLOUTS.items():
    path = ROOT / rel
    text = path.read_text(encoding="utf-8")
    if "**本章定位：System Design 组合层。**" in text:
        continue
    lines = text.splitlines()
    if not lines or not lines[0].startswith("# "):
        raise RuntimeError(f"missing H1: {rel}")
    new = lines[0] + "\n\n" + callout.rstrip() + "\n\n" + "\n".join(lines[1:]).lstrip("\n")
    path.write_text(new.rstrip() + "\n", encoding="utf-8")

print(f"updated {len(CALLOUTS)} System Design synthesis chapters")
