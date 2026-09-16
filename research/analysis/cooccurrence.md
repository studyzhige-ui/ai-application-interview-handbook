# Canonical Co-occurrence Analysis

更新日期：2026-09-11

> 共现 = 两道 Canonical 出现在同一个独立 HUMAN-A 招聘流程中。它能帮助发现常见追问组合，但**没有顺序信息**，不能直接宣称为面试官的固定 Follow-up Chain。真正追问链需要回到原始 Batch 人工核验。

## Module pair co-occurrence

| Module A | Module B | Shared Source Flows |
|---|---|---:|
| RAG | Agent | 59 |
| AI Backend Engineering | Agent | 54 |
| AI Backend Engineering | Redis | 53 |
| AI Backend Engineering | MySQL | 46 |
| LLM Foundation（应用工程深度） | Agent | 45 |
| AI Backend Engineering | System Design | 39 |
| Agent | System Design | 37 |
| LLM Foundation（应用工程深度） | RAG | 35 |
| Redis | Agent | 32 |
| AI Backend Engineering | LLM Foundation（应用工程深度） | 31 |
| AI Backend Engineering | RAG | 30 |
| Vector DB | RAG | 28 |
| MySQL | Redis | 25 |
| Redis | System Design | 22 |
| MySQL | Agent | 19 |
| MySQL | System Design | 19 |
| Vector DB | LLM Foundation（应用工程深度） | 17 |
| Vector DB | Agent | 17 |
| LLM Foundation（应用工程深度） | System Design | 17 |
| AI Backend Engineering | Vector DB | 16 |
| Redis | RAG | 16 |
| RAG | System Design | 16 |
| Redis | LLM Foundation（应用工程深度） | 14 |
| MySQL | RAG | 14 |
| MySQL | LLM Foundation（应用工程深度） | 12 |
| Python | Agent | 11 |
| Python | LLM Foundation（应用工程深度） | 8 |
| Vector DB | System Design | 7 |
| Python | RAG | 6 |
| Python | Vector DB | 5 |
| Python | AI Backend Engineering | 5 |
| Redis | Vector DB | 5 |
| MySQL | Vector DB | 5 |
| FastAPI | Agent | 3 |
| Python | System Design | 2 |
| Python | FastAPI | 2 |
| FastAPI | LLM Foundation（应用工程深度） | 2 |
| Python | Redis | 2 |
| FastAPI | AI Backend Engineering | 2 |
| FastAPI | RAG | 2 |
| FastAPI | Vector DB | 1 |

## Top Canonical pairs

| QID A | QID B | Shared Sources | Pair |
|---|---|---:|---|
| `AGENT-009` | `AGENT-014` | 21 | Context Compaction ↔ Memory Architecture |
| `RAG-002` | `RAG-007` | 17 | End-to-end Pipeline ↔ Chunk Strategy |
| `AGENT-003` | `AGENT-009` | 16 | Agent Loop ↔ Context Compaction |
| `RAG-002` | `RAG-013` | 16 | End-to-end Pipeline ↔ Hybrid Retrieval |
| `AGENT-009` | `AGENT-030` | 15 | Context Compaction ↔ Multi-Agent Architecture |
| `AGENT-009` | `AGENT-010` | 15 | Context Compaction ↔ Compaction Correctness |
| `RAG-002` | `RAG-015` | 15 | End-to-end Pipeline ↔ Reranking |
| `AGENT-003` | `AGENT-034` | 15 | Agent Loop ↔ Agent Evaluation |
| `AGENT-001` | `AGENT-024` | 15 | Agent Boundary ↔ Capability Abstraction Boundary |
| `AGENT-001` | `AGENT-003` | 14 | Agent Boundary ↔ Agent Loop |
| `AGENT-001` | `AGENT-009` | 14 | Agent Boundary ↔ Context Compaction |
| `AGENT-003` | `AGENT-005` | 14 | Agent Loop ↔ Agent Paradigm |
| `AGENT-005` | `AGENT-009` | 14 | Agent Paradigm ↔ Context Compaction |
| `AGENT-005` | `AGENT-030` | 14 | Agent Paradigm ↔ Multi-Agent Architecture |
| `RAG-006` | `RAG-007` | 14 | Chunking Principles ↔ Chunk Strategy |
| `AGENT-018` | `AGENT-024` | 14 | Tool Calling Protocol ↔ Capability Abstraction Boundary |
| `REDIS-012` | `REDIS-013` | 14 | Distributed Lock Basics ↔ Distributed Lock Correctness |
| `RAG-012` | `RAG-013` | 14 | Dense vs Sparse / BM25 ↔ Hybrid Retrieval |
| `RAG-007` | `RAG-013` | 14 | Chunk Strategy ↔ Hybrid Retrieval |
| `AGENT-001` | `AGENT-014` | 14 | Agent Boundary ↔ Memory Architecture |
| `AGENT-003` | `AGENT-018` | 14 | Agent Loop ↔ Tool Calling Protocol |
| `AGENT-005` | `AGENT-014` | 14 | Agent Paradigm ↔ Memory Architecture |
| `AGENT-014` | `AGENT-030` | 14 | Memory Architecture ↔ Multi-Agent Architecture |
| `AGENT-001` | `AGENT-005` | 13 | Agent Boundary ↔ Agent Paradigm |
| `RAG-007` | `RAG-021` | 13 | Chunk Strategy ↔ RAG Evaluation |
| `RAG-013` | `RAG-015` | 13 | Hybrid Retrieval ↔ Reranking |
| `AGENT-003` | `AGENT-014` | 13 | Agent Loop ↔ Memory Architecture |
| `AGENT-009` | `AGENT-020` | 13 | Context Compaction ↔ Tool Call Failure Semantics |
| `AGENT-008` | `AGENT-009` | 12 | Context Assembly ↔ Context Compaction |
| `RAG-020` | `RAG-021` | 12 | Retrieval Metrics ↔ RAG Evaluation |
| `AGENT-018` | `AGENT-023` | 12 | Tool Calling Protocol ↔ MCP Protocol |
| `AGENT-003` | `AGENT-024` | 12 | Agent Loop ↔ Capability Abstraction Boundary |
| `AGENT-005` | `AGENT-024` | 12 | Agent Paradigm ↔ Capability Abstraction Boundary |
| `AGENT-009` | `AGENT-034` | 12 | Context Compaction ↔ Agent Evaluation |
| `AGENT-020` | `AGENT-030` | 12 | Tool Call Failure Semantics ↔ Multi-Agent Architecture |
| `AGENT-021` | `AGENT-024` | 12 | Tool Discovery / Progressive Loading ↔ Capability Abstraction Boundary |
| `AGENT-034` | `AGENT-035` | 12 | Agent Evaluation ↔ Benchmark Engineering |
| `RAG-007` | `RAG-015` | 11 | Chunk Strategy ↔ Reranking |
| `RAG-002` | `RAG-021` | 11 | End-to-end Pipeline ↔ RAG Evaluation |
| `RAG-004` | `RAG-007` | 11 | Parsing / OCR / Layout ↔ Chunk Strategy |
| `RAG-013` | `RAG-021` | 11 | Hybrid Retrieval ↔ RAG Evaluation |
| `REDIS-007` | `REDIS-012` | 11 | Cache Failure Patterns ↔ Distributed Lock Basics |
| `AGENT-003` | `AGENT-020` | 11 | Agent Loop ↔ Tool Call Failure Semantics |
| `AGENT-018` | `AGENT-020` | 11 | Tool Calling Protocol ↔ Tool Call Failure Semantics |
| `AGENT-002` | `AGENT-003` | 11 | Harness / Runtime Boundary ↔ Agent Loop |
| `AGENT-014` | `AGENT-020` | 11 | Memory Architecture ↔ Tool Call Failure Semantics |
| `AGENT-034` | `AGENT-036` | 11 | Agent Evaluation ↔ Code Verification |
| `RAG-002` | `RAG-010` | 11 | End-to-end Pipeline ↔ Query Transformation |
| `RAG-019` | `RAG-021` | 11 | Bad Case Attribution ↔ RAG Evaluation |
| `AGENT-036` | `AGENT-048` | 11 | Code Verification ↔ AI-assisted Development Workflow |
| `AGENT-003` | `AGENT-030` | 10 | Agent Loop ↔ Multi-Agent Architecture |
| `AGENT-009` | `RAG-002` | 10 | Context Compaction ↔ End-to-end Pipeline |
| `AGENT-023` | `AGENT-024` | 10 | MCP Protocol ↔ Capability Abstraction Boundary |
| `AGENT-014` | `AGENT-018` | 10 | Memory Architecture ↔ Tool Calling Protocol |
| `AGENT-014` | `AGENT-024` | 10 | Memory Architecture ↔ Capability Abstraction Boundary |
| `RAG-006` | `RAG-008` | 10 | Chunking Principles ↔ Chunk Parameters |
| `RAG-007` | `RAG-008` | 10 | Chunk Strategy ↔ Chunk Parameters |
| `AGENT-002` | `AGENT-009` | 10 | Harness / Runtime Boundary ↔ Context Compaction |
| `RAG-002` | `VDB-009` | 10 | End-to-end Pipeline ↔ Vector Storage / Product / Architecture Selection |
| `RAG-007` | `RAG-020` | 10 | Chunk Strategy ↔ Retrieval Metrics |
| `RAG-015` | `RAG-021` | 10 | Reranking ↔ RAG Evaluation |
| `AGENT-006` | `AGENT-020` | 10 | Termination / Loop Detection ↔ Tool Call Failure Semantics |
| `AGENT-002` | `AGENT-034` | 10 | Harness / Runtime Boundary ↔ Agent Evaluation |
| `AGENT-003` | `AGENT-021` | 10 | Agent Loop ↔ Tool Discovery / Progressive Loading |
| `AGENT-009` | `AGENT-021` | 10 | Context Compaction ↔ Tool Discovery / Progressive Loading |
| `AGENT-009` | `AGENT-024` | 10 | Context Compaction ↔ Capability Abstraction Boundary |
| `AGENT-021` | `AGENT-025` | 10 | Tool Discovery / Progressive Loading ↔ Skill Progressive Disclosure |
| `RAG-010` | `RAG-013` | 10 | Query Transformation ↔ Hybrid Retrieval |
| `AIBE-020` | `REDIS-012` | 10 | Data Consistency / Cache Architecture ↔ Distributed Lock Basics |
| `AGENT-001` | `AGENT-030` | 9 | Agent Boundary ↔ Multi-Agent Architecture |
| `AGENT-009` | `RAG-007` | 9 | Context Compaction ↔ Chunk Strategy |
| `RAG-007` | `VDB-009` | 9 | Chunk Strategy ↔ Vector Storage / Product / Architecture Selection |
| `RAG-015` | `VDB-009` | 9 | Reranking ↔ Vector Storage / Product / Architecture Selection |
| `VDB-004` | `VDB-005` | 9 | Index Selection ↔ HNSW |
| `VDB-005` | `VDB-007` | 9 | HNSW ↔ HNSW vs IVF |
| `AGENT-003` | `AGENT-036` | 9 | Agent Loop ↔ Code Verification |
| `AGENT-009` | `AGENT-011` | 9 | Context Compaction ↔ Large Tool Result / Context Offloading |
| `AIBE-004` | `AIBE-005` | 9 | TCP / UDP ↔ TCP Reliability |
| `RAG-002` | `RAG-012` | 9 | End-to-end Pipeline ↔ Dense vs Sparse / BM25 |
| `RAG-002` | `RAG-020` | 9 | End-to-end Pipeline ↔ Retrieval Metrics |
| `RAG-007` | `RAG-012` | 9 | Chunk Strategy ↔ Dense vs Sparse / BM25 |
| `RAG-013` | `RAG-020` | 9 | Hybrid Retrieval ↔ Retrieval Metrics |
| `RAG-015` | `RAG-016` | 9 | Reranking ↔ Top-K |
| `RAG-015` | `RAG-020` | 9 | Reranking ↔ Retrieval Metrics |
| `LLM-023` | `RAG-002` | 9 | Prompt Engineering ↔ End-to-end Pipeline |
| `AGENT-005` | `AGENT-020` | 9 | Agent Paradigm ↔ Tool Call Failure Semantics |
| `AGENT-020` | `AGENT-023` | 9 | Tool Call Failure Semantics ↔ MCP Protocol |
| `AGENT-009` | `AGENT-038` | 9 | Context Compaction ↔ Agent Runtime Resilience Policy |
| `AGENT-018` | `AGENT-021` | 9 | Tool Calling Protocol ↔ Tool Discovery / Progressive Loading |
| `AGENT-020` | `AGENT-028` | 9 | Tool Call Failure Semantics ↔ Permission / Approval / Sandbox |
| `AGENT-020` | `AGENT-038` | 9 | Tool Call Failure Semantics ↔ Agent Runtime Resilience Policy |
| `AGENT-028` | `AGENT-030` | 9 | Permission / Approval / Sandbox ↔ Multi-Agent Architecture |
| `RAG-004` | `RAG-005` | 9 | Parsing / OCR / Layout ↔ Multimodal / Table Parsing |
| `RAG-007` | `RAG-010` | 9 | Chunk Strategy ↔ Query Transformation |
| `RAG-007` | `RAG-019` | 9 | Chunk Strategy ↔ Bad Case Attribution |
| `RAG-013` | `RAG-019` | 9 | Hybrid Retrieval ↔ Bad Case Attribution |
| `AGENT-003` | `AGENT-008` | 8 | Agent Loop ↔ Context Assembly |
| `AGENT-008` | `AGENT-030` | 8 | Context Assembly ↔ Multi-Agent Architecture |
| `AGENT-030` | `RAG-007` | 8 | Multi-Agent Architecture ↔ Chunk Strategy |
| `AGENT-018` | `RAG-007` | 8 | Tool Calling Protocol ↔ Chunk Strategy |
| `VDB-004` | `VDB-007` | 8 | Index Selection ↔ HNSW vs IVF |
| `VDB-004` | `VDB-009` | 8 | Index Selection ↔ Vector Storage / Product / Architecture Selection |
| `VDB-005` | `VDB-009` | 8 | HNSW ↔ Vector Storage / Product / Architecture Selection |
| `RAG-002` | `RAG-014` | 8 | End-to-end Pipeline ↔ Fusion / RRF |
| `AGENT-009` | `AGENT-018` | 8 | Context Compaction ↔ Tool Calling Protocol |
| `AGENT-018` | `AGENT-030` | 8 | Tool Calling Protocol ↔ Multi-Agent Architecture |
| `RAG-002` | `RAG-004` | 8 | End-to-end Pipeline ↔ Parsing / OCR / Layout |
| `RAG-002` | `RAG-016` | 8 | End-to-end Pipeline ↔ Top-K |
| `RAG-007` | `RAG-016` | 8 | Chunk Strategy ↔ Top-K |
| `AGENT-009` | `RAG-013` | 8 | Context Compaction ↔ Hybrid Retrieval |
| `REDIS-002` | `REDIS-012` | 8 | Data Structures ↔ Distributed Lock Basics |
| `AGENT-003` | `AGENT-023` | 8 | Agent Loop ↔ MCP Protocol |
| `AGENT-005` | `AGENT-006` | 8 | Agent Paradigm ↔ Termination / Loop Detection |
| `AGENT-005` | `AGENT-018` | 8 | Agent Paradigm ↔ Tool Calling Protocol |
| `AGENT-020` | `RAG-002` | 8 | Tool Call Failure Semantics ↔ End-to-end Pipeline |
| `AGENT-006` | `AGENT-014` | 8 | Termination / Loop Detection ↔ Memory Architecture |
| `AGENT-006` | `AGENT-030` | 8 | Termination / Loop Detection ↔ Multi-Agent Architecture |
| `AGENT-008` | `AGENT-014` | 8 | Context Assembly ↔ Memory Architecture |
| `AGENT-008` | `AGENT-020` | 8 | Context Assembly ↔ Tool Call Failure Semantics |
| `AGENT-010` | `AGENT-014` | 8 | Compaction Correctness ↔ Memory Architecture |
