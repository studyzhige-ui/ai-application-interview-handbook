"use client";

import { useState } from "react";
import Link from "next/link";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import { PRIMARY_MODULES } from "@/lib/config";

const SUGGESTIONS = [
  "为什么 Agent 项目里同时需要 MySQL 和 Redis？",
  "RAG 的 chunking、retrieval 和 evaluation 怎么串起来？",
  "Agent checkpoint 和普通 session state 有什么区别？",
  "面试里如何解释 Python async / await 的运行机制？",
];

export default function AskClient() {
  const [question, setQuestion] = useState("");
  const [scope, setScope] = useState("all");
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");

  async function submit(value = question) {
    const finalQuestion = value.trim();
    if (!finalQuestion) return;
    setQuestion(finalQuestion);
    setLoading(true);
    setError("");
    setResult(null);
    try {
      const response = await fetch("/api/ask", {
        method: "POST",
        headers: { "content-type": "application/json" },
        body: JSON.stringify({ question: finalQuestion, scope }),
      });
      const data = await response.json();
      if (!response.ok) throw new Error(data.error || "Ask KB 请求失败");
      setResult(data);
    } catch (err) {
      setError(err.message || "Ask KB 请求失败");
    } finally {
      setLoading(false);
    }
  }

  return (
    <section className="page-wrap ask-page">
      <div className="page-heading ask-heading">
        <span className="eyebrow">RETRIEVAL-AUGMENTED GENERATION</span>
        <h1>Ask your knowledge base</h1>
        <p>先从你自己的 Markdown 小节检索证据，再生成回答；回答不应该脱离知识库凭空补事实。</p>
      </div>

      <div className="ask-box">
        <textarea value={question} onChange={(event) => setQuestion(event.target.value)} onKeyDown={(event) => {
          if ((event.metaKey || event.ctrlKey) && event.key === "Enter") submit();
        }} placeholder="问一个需要跨章节组织的问题…" rows={4} />
        <div className="ask-controls">
          <select value={scope} onChange={(event) => setScope(event.target.value)}>
            <option value="all">全知识库</option>
            {PRIMARY_MODULES.map((item) => <option key={item.slug} value={item.slug}>{item.short}</option>)}
            <option value="research">Research</option>
          </select>
          <button className="primary-button" disabled={loading || !question.trim()} onClick={() => submit()}>{loading ? "正在检索与组织…" : "Ask KB →"}</button>
        </div>
      </div>

      {!result && !loading && <div className="suggestion-grid">{SUGGESTIONS.map((suggestion) => <button key={suggestion} onClick={() => submit(suggestion)}>{suggestion}</button>)}</div>}
      {error && <div className="error-panel">{error}</div>}

      {result && (
        <div className="answer-grid">
          <div className="answer-panel">
            {!result.configured && <div className="config-notice"><strong>RAG 检索已经工作，但生成模型尚未配置。</strong><p>在部署环境设置 <code>OPENAI_API_KEY</code> 后，这里会基于下方证据生成带引用的完整答案。</p></div>}
            {result.answer && <ReactMarkdown remarkPlugins={[remarkGfm]}>{result.answer}</ReactMarkdown>}
          </div>
          <aside className="sources-panel">
            <h2>Retrieved sources</h2>
            {result.sources.map((source, index) => (
              <Link href={source.href} key={source.id}>
                <span>[{index + 1}] {source.heading}</span><strong>{source.title}</strong><small>{source.path}</small><p>{source.snippet}</p>
              </Link>
            ))}
          </aside>
        </div>
      )}
    </section>
  );
}
