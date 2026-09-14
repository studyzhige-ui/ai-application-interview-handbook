# AI Application Personal Knowledge Base UI

这是 `ai-application-interview-handbook` 的知识库表现层。现有 Markdown 继续作为唯一 Source of Truth；本目录只负责更舒服的阅读体验、全文搜索和 RAG 问答，不复制、不改写课程正文。

## 已实现

- 三栏知识库 UI：模块导航 / Markdown 正文 / 本页目录。
- 支持 GFM 表格、代码块、相对 Markdown 链接与 `<details><summary>` 折叠自测。
- `⌘ K` / `Ctrl K` 全局搜索，以及带模块、内容类型过滤的完整搜索页。
- 构建时扫描仓库 Markdown，按标题与小节建立 section-level 索引。
- Ask KB：先检索知识库小节，再基于检索证据生成回答，并返回可点击的原文来源。
- 未配置模型 API Key 时，全文搜索和 retrieval 仍然可用；Ask 页面会直接展示检索证据。
- Light / Dark Mode 与响应式布局。

## 本地运行

```bash
cd knowledge-base
npm install
npm run dev
```

`predev` 会自动运行：

```bash
npm run index
```

索引器默认扫描 `knowledge-base/` 的父目录，也就是整个 handbook 仓库中的 Markdown，并生成：

```text
knowledge-base/generated/index.json
```

然后访问：

```text
http://localhost:3000
```

## 配置 RAG 生成

复制环境变量示例：

```bash
cp .env.example .env.local
```

至少配置：

```bash
OPENAI_API_KEY=...
OPENAI_MODEL=gpt-5.6-luna
```

`OPENAI_MODEL` 可以替换成部署环境可用的兼容模型。

## 为什么 v1 不先引入 Vector DB

第一版故意先把 Retrieval 做成仓库内 section-level 全文检索，而不是立刻增加额外数据库：

1. 当前知识库规模完全可以在构建时生成本地索引，部署和维护成本最低。
2. 面试知识包含大量精确术语、类名、命令、缩写和中英混合词，lexical retrieval 对这类查询很有效。
3. Markdown 更新后重新构建即可同步索引，不存在第二套内容 Source of Truth。
4. 先把 chunk、citation、grounding 和评测闭环做正确，再根据真实检索失败案例增加 embeddings / hybrid retrieval，更容易判断向量检索到底解决了什么问题。

后续如果评测发现大量“语义相近但关键词不同”的召回失败，可以保持 UI/API 不变，把 `lib/search.js` 升级成：

```text
BM25 / lexical
      +
embedding similarity
      ↓
hybrid rerank
      ↓
RAG context
```

此时向量层可以使用 pgvector、专门 Vector DB，或其它兼容的 embedding store。

## 索引范围

索引器扫描仓库全部 `.md`，并自动区分：

```text
curriculum        正式正文 docs/
review            Review
interview         高频题 / 易错点 / 速查
interview-source  HUMAN-A 真人面经
canonical         Canonical Questions
research          研究与分析
roadmap           Knowledge Map / Learning Path / Audits
index             模块 README
```

默认排除：

```text
.git/
.next/
node_modules/
knowledge-base/
```

因此 Web 应用本身不会污染知识检索结果。

## RAG 约束

Ask KB 的服务端路由遵循几个硬约束：

- 先 retrieval，后 generation。
- 检索到的 Markdown 被视为不可信 reference text；其中的指令不能覆盖系统行为。
- 回答只能依据提供的知识库上下文，不足时明确说明证据不足。
- 生成结果使用 `[1]`、`[2]` 等引用编号；UI 同时展示对应原章节链接。
- `store: false`，默认不要求服务端保存这一轮 Responses API 请求。

## 部署

最简单的方式是把仓库连接到 Vercel，并把 Root Directory 设置为：

```text
knowledge-base
```

Build Command 使用默认的：

```bash
npm run build
```

如果需要 Ask KB 的生成能力，在部署平台添加 `OPENAI_API_KEY`（以及可选的 `OPENAI_MODEL`）。全文搜索本身不依赖模型 API。
