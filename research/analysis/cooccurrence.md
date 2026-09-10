# Canonical Co-occurrence Analysis

更新日期：2026-09-11

> 共现 = 两道 Canonical 出现在同一个独立 HUMAN-A 招聘流程中。它能帮助发现常见追问组合，但**没有顺序信息**，不能直接宣称为面试官的固定 Follow-up Chain。真正追问链需要回到原始 Batch 人工核验。

## Module pair co-occurrence

| Module A | Module B | Shared Source Flows |
|---|---|---:|
| AI Backend Engineering | Redis | 52 |
| AI Backend Engineering | MySQL | 46 |
| RAG | Agent Harness / Runtime | 41 |
| AI Backend Engineering | System Design | 37 |
| AI Backend Engineering | Agent Harness / Runtime | 32 |
| AI Backend Engineering | RAG | 27 |
| Vector DB | RAG | 26 |
| AI Backend Engineering | LLM Foundation（应用工程深度） | 26 |
| MySQL | Redis | 25 |
| LLM Foundation（应用工程深度） | RAG | 23 |
| Redis | Agent Harness / Runtime | 22 |
| Redis | System Design | 22 |
| Agent Harness / Runtime | System Design | 21 |
| MySQL | System Design | 19 |
| LLM Foundation（应用工程深度） | Agent Harness / Runtime | 16 |
| Redis | RAG | 16 |
| AI Backend Engineering | Vector DB | 14 |
| MySQL | RAG | 14 |
| RAG | System Design | 14 |
| Vector DB | LLM Foundation（应用工程深度） | 13 |
| MySQL | Agent Harness / Runtime | 13 |
| MySQL | LLM Foundation（应用工程深度） | 12 |
| Vector DB | Agent Harness / Runtime | 11 |
| LLM Foundation（应用工程深度） | System Design | 11 |
| Python | Agent Harness / Runtime | 10 |
| Redis | LLM Foundation（应用工程深度） | 10 |
| Python | RAG | 6 |
| Python | LLM Foundation（应用工程深度） | 6 |
| Vector DB | System Design | 6 |
| Python | Vector DB | 5 |
| Python | AI Backend Engineering | 5 |
| Redis | Vector DB | 5 |
| MySQL | Vector DB | 5 |
| FastAPI | Agent Harness / Runtime | 3 |
| Python | System Design | 2 |
| Python | FastAPI | 2 |
| Python | Redis | 2 |
| FastAPI | AI Backend Engineering | 2 |
| FastAPI | RAG | 2 |
| FastAPI | Vector DB | 1 |
| FastAPI | LLM Foundation（应用工程深度） | 1 |

## Top Canonical pairs

| QID A | QID B | Shared Sources | Pair |
|---|---|---:|---|
| `RAG-002` | `RAG-007` | 17 | End-to-end Pipeline ↔ Chunk Strategy |
| `AGENT-009` | `AGENT-014` | 17 | Context Compaction ↔ Memory Architecture |
| `RAG-002` | `RAG-013` | 16 | End-to-end Pipeline ↔ Hybrid Retrieval |
| `RAG-002` | `RAG-015` | 15 | End-to-end Pipeline ↔ Reranking |
| `RAG-006` | `RAG-007` | 14 | Chunking Principles ↔ Chunk Strategy |
| `AGENT-018` | `AGENT-024` | 14 | Tool Calling Protocol ↔ Capability Abstraction Boundary |
| `REDIS-012` | `REDIS-013` | 14 | Distributed Lock Basics ↔ Distributed Lock Correctness |
| `RAG-012` | `RAG-013` | 14 | Dense vs Sparse / BM25 ↔ Hybrid Retrieval |
| `RAG-007` | `RAG-013` | 14 | Chunk Strategy ↔ Hybrid Retrieval |
| `AGENT-003` | `AGENT-018` | 14 | Agent Loop ↔ Tool Calling Protocol |
| `AGENT-009` | `AGENT-010` | 13 | Context Compaction ↔ Compaction Correctness |
| `RAG-007` | `RAG-021` | 13 | Chunk Strategy ↔ RAG Evaluation |
| `RAG-013` | `RAG-015` | 13 | Hybrid Retrieval ↔ Reranking |
| `AGENT-009` | `AGENT-020` | 13 | Context Compaction ↔ Tool Call Failure Semantics |
| `AGENT-001` | `AGENT-024` | 13 | Agent Boundary ↔ Capability Abstraction Boundary |
| `AGENT-001` | `AGENT-009` | 12 | Agent Boundary ↔ Context Compaction |
| `AGENT-009` | `AGENT-030` | 12 | Context Compaction ↔ Multi-Agent Architecture |
| `RAG-020` | `RAG-021` | 12 | Retrieval Metrics ↔ RAG Evaluation |
| `AGENT-018` | `AGENT-023` | 12 | Tool Calling Protocol ↔ MCP Protocol |
| `AGENT-001` | `AGENT-003` | 11 | Agent Boundary ↔ Agent Loop |
| `AGENT-003` | `AGENT-009` | 11 | Agent Loop ↔ Context Compaction |
| `RAG-007` | `RAG-015` | 11 | Chunk Strategy ↔ Reranking |
| `RAG-002` | `RAG-021` | 11 | End-to-end Pipeline ↔ RAG Evaluation |
| `RAG-004` | `RAG-007` | 11 | Parsing / OCR / Layout ↔ Chunk Strategy |
| `RAG-013` | `RAG-021` | 11 | Hybrid Retrieval ↔ RAG Evaluation |
| `AGENT-001` | `AGENT-014` | 11 | Agent Boundary ↔ Memory Architecture |
| `REDIS-007` | `REDIS-012` | 11 | Cache Failure Patterns ↔ Distributed Lock Basics |
| `AGENT-014` | `AGENT-030` | 11 | Memory Architecture ↔ Multi-Agent Architecture |
| `AGENT-021` | `AGENT-024` | 11 | Tool Discovery / Progressive Loading ↔ Capability Abstraction Boundary |
| `RAG-019` | `RAG-021` | 11 | Bad Case Attribution ↔ RAG Evaluation |
| `AGENT-008` | `AGENT-009` | 10 | Context Assembly ↔ Context Compaction |
| `AGENT-023` | `AGENT-024` | 10 | MCP Protocol ↔ Capability Abstraction Boundary |
| `RAG-006` | `RAG-008` | 10 | Chunking Principles ↔ Chunk Parameters |
| `RAG-007` | `RAG-008` | 10 | Chunk Strategy ↔ Chunk Parameters |
| `RAG-007` | `RAG-020` | 10 | Chunk Strategy ↔ Retrieval Metrics |
| `RAG-015` | `RAG-021` | 10 | Reranking ↔ RAG Evaluation |
| `AGENT-003` | `AGENT-014` | 10 | Agent Loop ↔ Memory Architecture |
| `AGENT-018` | `AGENT-020` | 10 | Tool Calling Protocol ↔ Tool Call Failure Semantics |
| `AGENT-005` | `AGENT-014` | 10 | Agent Paradigm ↔ Memory Architecture |
| `AGENT-014` | `AGENT-020` | 10 | Memory Architecture ↔ Tool Call Failure Semantics |
| `RAG-010` | `RAG-013` | 10 | Query Transformation ↔ Hybrid Retrieval |
| `RAG-002` | `RAG-010` | 10 | End-to-end Pipeline ↔ Query Transformation |
| `AIBE-020` | `REDIS-012` | 10 | Data Consistency / Cache Architecture ↔ Distributed Lock Basics |
| `AGENT-001` | `AGENT-005` | 9 | Agent Boundary ↔ Agent Paradigm |
| `AGENT-005` | `AGENT-009` | 9 | Agent Paradigm ↔ Context Compaction |
| `AGENT-009` | `RAG-007` | 9 | Context Compaction ↔ Chunk Strategy |
| `AGENT-014` | `AGENT-018` | 9 | Memory Architecture ↔ Tool Calling Protocol |
| `RAG-007` | `VDB-009` | 9 | Chunk Strategy ↔ Vector Storage / Product / Architecture Selection |
| `RAG-015` | `VDB-009` | 9 | Reranking ↔ Vector Storage / Product / Architecture Selection |
| `VDB-004` | `VDB-005` | 9 | Index Selection ↔ HNSW |
| `VDB-005` | `VDB-007` | 9 | HNSW ↔ HNSW vs IVF |
| `AGENT-009` | `AGENT-011` | 9 | Context Compaction ↔ Large Tool Result / Context Offloading |
| `AIBE-004` | `AIBE-005` | 9 | TCP / UDP ↔ TCP Reliability |
| `RAG-002` | `RAG-012` | 9 | End-to-end Pipeline ↔ Dense vs Sparse / BM25 |
| `RAG-002` | `VDB-009` | 9 | End-to-end Pipeline ↔ Vector Storage / Product / Architecture Selection |
| `RAG-007` | `RAG-012` | 9 | Chunk Strategy ↔ Dense vs Sparse / BM25 |
| `RAG-013` | `RAG-020` | 9 | Hybrid Retrieval ↔ Retrieval Metrics |
| `RAG-015` | `RAG-016` | 9 | Reranking ↔ Top-K |
| `RAG-015` | `RAG-020` | 9 | Reranking ↔ Retrieval Metrics |
| `AGENT-003` | `AGENT-020` | 9 | Agent Loop ↔ Tool Call Failure Semantics |
| `AGENT-006` | `AGENT-020` | 9 | Termination / Loop Detection ↔ Tool Call Failure Semantics |
| `AGENT-003` | `AGENT-024` | 9 | Agent Loop ↔ Capability Abstraction Boundary |
| `AGENT-009` | `AGENT-021` | 9 | Context Compaction ↔ Tool Discovery / Progressive Loading |
| `AGENT-009` | `AGENT-034` | 9 | Context Compaction ↔ Agent Evaluation |
| `AGENT-018` | `AGENT-021` | 9 | Tool Calling Protocol ↔ Tool Discovery / Progressive Loading |
| `AGENT-020` | `AGENT-038` | 9 | Tool Call Failure Semantics ↔ Agent Runtime Resilience Policy |
| `AGENT-021` | `AGENT-025` | 9 | Tool Discovery / Progressive Loading ↔ Skill Progressive Disclosure |
| `AGENT-034` | `AGENT-035` | 9 | Agent Evaluation ↔ Benchmark Engineering |
| `RAG-004` | `RAG-005` | 9 | Parsing / OCR / Layout ↔ Multimodal / Table Parsing |
| `RAG-007` | `RAG-010` | 9 | Chunk Strategy ↔ Query Transformation |
| `RAG-007` | `RAG-019` | 9 | Chunk Strategy ↔ Bad Case Attribution |
| `AGENT-003` | `AGENT-005` | 8 | Agent Loop ↔ Agent Paradigm |
| `AGENT-005` | `AGENT-030` | 8 | Agent Paradigm ↔ Multi-Agent Architecture |
| `AGENT-009` | `RAG-002` | 8 | Context Compaction ↔ End-to-end Pipeline |
| `AGENT-030` | `RAG-007` | 8 | Multi-Agent Architecture ↔ Chunk Strategy |
| `AGENT-014` | `AGENT-024` | 8 | Memory Architecture ↔ Capability Abstraction Boundary |
| `AGENT-018` | `RAG-007` | 8 | Tool Calling Protocol ↔ Chunk Strategy |
| `VDB-004` | `VDB-007` | 8 | Index Selection ↔ HNSW vs IVF |
| `VDB-004` | `VDB-009` | 8 | Index Selection ↔ Vector Storage / Product / Architecture Selection |
| `VDB-005` | `VDB-009` | 8 | HNSW ↔ Vector Storage / Product / Architecture Selection |
| `RAG-002` | `RAG-014` | 8 | End-to-end Pipeline ↔ Fusion / RRF |
| `AGENT-009` | `AGENT-018` | 8 | Context Compaction ↔ Tool Calling Protocol |
| `RAG-002` | `RAG-004` | 8 | End-to-end Pipeline ↔ Parsing / OCR / Layout |
| `RAG-002` | `RAG-020` | 8 | End-to-end Pipeline ↔ Retrieval Metrics |
| `RAG-007` | `RAG-016` | 8 | Chunk Strategy ↔ Top-K |
| `AGENT-009` | `RAG-013` | 8 | Context Compaction ↔ Hybrid Retrieval |
| `REDIS-002` | `REDIS-012` | 8 | Data Structures ↔ Distributed Lock Basics |
| `AGENT-003` | `AGENT-021` | 8 | Agent Loop ↔ Tool Discovery / Progressive Loading |
| `AGENT-005` | `AGENT-024` | 8 | Agent Paradigm ↔ Capability Abstraction Boundary |
| `AGENT-009` | `AGENT-024` | 8 | Context Compaction ↔ Capability Abstraction Boundary |
| `AGENT-009` | `AGENT-038` | 8 | Context Compaction ↔ Agent Runtime Resilience Policy |
| `AGENT-010` | `AGENT-014` | 8 | Compaction Correctness ↔ Memory Architecture |
| `AGENT-010` | `AGENT-020` | 8 | Compaction Correctness ↔ Tool Call Failure Semantics |
| `AGENT-014` | `AGENT-015` | 8 | Memory Architecture ↔ Memory Lifecycle |
| `AGENT-024` | `AGENT-025` | 8 | Capability Abstraction Boundary ↔ Skill Progressive Disclosure |
| `AGENT-034` | `AGENT-036` | 8 | Agent Evaluation ↔ Code Verification |
| `RAG-002` | `RAG-024` | 8 | End-to-end Pipeline ↔ Incremental Update / Freshness |
| `RAG-005` | `RAG-007` | 8 | Multimodal / Table Parsing ↔ Chunk Strategy |
| `RAG-007` | `RAG-024` | 8 | Chunk Strategy ↔ Incremental Update / Freshness |
| `RAG-010` | `RAG-015` | 8 | Query Transformation ↔ Reranking |
| `RAG-013` | `RAG-019` | 8 | Hybrid Retrieval ↔ Bad Case Attribution |
| `RAG-019` | `RAG-020` | 8 | Bad Case Attribution ↔ Retrieval Metrics |
| `RAG-021` | `RAG-022` | 8 | RAG Evaluation ↔ Evaluation Dataset / Judge |
| `AIBE-020` | `REDIS-013` | 8 | Data Consistency / Cache Architecture ↔ Distributed Lock Correctness |
| `RAG-024` | `VDB-020` | 8 | Incremental Update / Freshness ↔ Index Lifecycle / Freshness |
| `AIBE-020` | `SD-001` | 8 | Data Consistency / Cache Architecture ↔ Flash Sale / Inventory |
| `AGENT-001` | `RAG-007` | 7 | Agent Boundary ↔ Chunk Strategy |
| `AGENT-003` | `AGENT-008` | 7 | Agent Loop ↔ Context Assembly |
| `RAG-002` | `RAG-006` | 7 | End-to-end Pipeline ↔ Chunking Principles |
| `AGENT-009` | `AGENT-032` | 7 | Context Compaction ↔ Model Routing / Runtime Adapter |
| `AGENT-010` | `AGENT-011` | 7 | Compaction Correctness ↔ Large Tool Result / Context Offloading |
| `RAG-013` | `RAG-014` | 7 | Hybrid Retrieval ↔ Fusion / RRF |
| `AGENT-018` | `AGENT-030` | 7 | Tool Calling Protocol ↔ Multi-Agent Architecture |
| `RAG-002` | `RAG-016` | 7 | End-to-end Pipeline ↔ Top-K |
| `RAG-004` | `RAG-021` | 7 | Parsing / OCR / Layout ↔ RAG Evaluation |
| `RAG-013` | `RAG-016` | 7 | Hybrid Retrieval ↔ Top-K |
| `RAG-021` | `VDB-009` | 7 | RAG Evaluation ↔ Vector Storage / Product / Architecture Selection |
| `AGENT-014` | `AGENT-027` | 7 | Memory Architecture ↔ Checkpoint / Resume |
| `RAG-014` | `RAG-015` | 7 | Fusion / RRF ↔ Reranking |
| `MYSQL-012` | `MYSQL-013` | 7 | Isolation Levels ↔ MVCC / ReadView |
