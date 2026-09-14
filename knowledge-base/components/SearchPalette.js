"use client";

import { useEffect, useRef, useState } from "react";
import { useRouter } from "next/navigation";

export default function SearchPalette() {
  const router = useRouter();
  const inputRef = useRef(null);
  const [open, setOpen] = useState(false);
  const [query, setQuery] = useState("");
  const [results, setResults] = useState([]);

  useEffect(() => {
    function onKeyDown(event) {
      if ((event.metaKey || event.ctrlKey) && event.key.toLowerCase() === "k") {
        event.preventDefault();
        setOpen(true);
      }
      if (event.key === "Escape") setOpen(false);
    }
    window.addEventListener("keydown", onKeyDown);
    return () => window.removeEventListener("keydown", onKeyDown);
  }, []);

  useEffect(() => {
    if (open) setTimeout(() => inputRef.current?.focus(), 0);
  }, [open]);

  useEffect(() => {
    if (!query.trim()) {
      setResults([]);
      return;
    }
    const controller = new AbortController();
    const timer = setTimeout(async () => {
      const response = await fetch(`/api/search?q=${encodeURIComponent(query)}&limit=8`, { signal: controller.signal });
      if (response.ok) setResults((await response.json()).results ?? []);
    }, 160);
    return () => {
      clearTimeout(timer);
      controller.abort();
    };
  }, [query]);

  function go(href) {
    setOpen(false);
    setQuery("");
    router.push(href);
  }

  return (
    <>
      <button className="search-trigger" onClick={() => setOpen(true)}>
        <span>⌕&nbsp; 搜索知识库</span><kbd>⌘ K</kbd>
      </button>
      {open && (
        <div className="palette-backdrop" onMouseDown={() => setOpen(false)}>
          <div className="palette" onMouseDown={(event) => event.stopPropagation()}>
            <div className="palette-input-row">
              <span className="palette-icon">⌕</span>
              <input ref={inputRef} value={query} onChange={(event) => setQuery(event.target.value)} placeholder="搜索 Redis、RAG、Agent checkpoint…" />
              <button className="esc-button" onClick={() => setOpen(false)}>ESC</button>
            </div>
            <div className="palette-results">
              {!query.trim() && <p className="empty-state">支持中文、英文、代码术语和章节标题全文搜索。</p>}
              {query.trim() && results.length === 0 && <p className="empty-state">没有找到匹配内容。</p>}
              {results.map((result) => (
                <button className="palette-result" key={result.id} onClick={() => go(result.href)}>
                  <div><strong>{result.title}</strong><span>{result.heading}</span></div>
                  <p>{result.snippet}</p>
                </button>
              ))}
            </div>
            <div className="palette-footer">
              <button onClick={() => go(`/search?q=${encodeURIComponent(query)}`)}>打开完整搜索 →</button>
            </div>
          </div>
        </div>
      )}
    </>
  );
}
