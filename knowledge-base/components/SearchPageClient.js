"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { KIND_LABELS, PRIMARY_MODULES } from "@/lib/config";

export default function SearchPageClient({ initialQuery = "" }) {
  const [query, setQuery] = useState(initialQuery);
  const [module, setModule] = useState("all");
  const [kind, setKind] = useState("all");
  const [results, setResults] = useState([]);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    const controller = new AbortController();
    const timer = setTimeout(async () => {
      setLoading(true);
      try {
        const params = new URLSearchParams({ q: query, module, kind, limit: "50" });
        const response = await fetch(`/api/search?${params}`, { signal: controller.signal });
        if (response.ok) setResults((await response.json()).results ?? []);
      } finally {
        setLoading(false);
      }
    }, 160);
    return () => {
      clearTimeout(timer);
      controller.abort();
    };
  }, [query, module, kind]);

  return (
    <section className="page-wrap">
      <div className="page-heading">
        <span className="eyebrow">FULL-TEXT SEARCH</span>
        <h1>搜索整个知识库</h1>
        <p>标题、正文、中文术语、代码名、Review、Interview 和真人面经都进入同一套索引。</p>
      </div>

      <div className="search-console">
        <input autoFocus value={query} onChange={(event) => setQuery(event.target.value)} placeholder="例如：缓存击穿、context compaction、MVCC…" />
        <div className="filter-row">
          <select value={module} onChange={(event) => setModule(event.target.value)}>
            <option value="all">全部模块</option>
            {PRIMARY_MODULES.map((item) => <option key={item.slug} value={item.slug}>{item.short}</option>)}
            <option value="research">Research</option><option value="roadmap">Roadmap</option>
          </select>
          <select value={kind} onChange={(event) => setKind(event.target.value)}>
            <option value="all">全部内容类型</option>
            {Object.entries(KIND_LABELS).map(([value, label]) => <option key={value} value={value}>{label}</option>)}
          </select>
          <span className="result-count">{loading ? "检索中…" : `${results.length} 个结果`}</span>
        </div>
      </div>

      <div className="search-results-list">
        {query.trim() && results.length === 0 && !loading && <div className="empty-panel">没有找到匹配内容。试试更短的术语或英文关键词。</div>}
        {results.map((result) => (
          <Link className="search-result-card" href={result.href} key={result.id}>
            <div className="result-topline"><span>{result.module}</span><span>{KIND_LABELS[result.kind] || result.kind}</span><code>{result.path}</code></div>
            <h2>{result.title}</h2><h3>{result.heading}</h3><p>{result.snippet}</p>
          </Link>
        ))}
      </div>
    </section>
  );
}
