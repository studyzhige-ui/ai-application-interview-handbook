import Link from "next/link";
import { getIndex } from "@/lib/kb";
import { PRIMARY_MODULES } from "@/lib/config";

export const metadata = { title: "Knowledge Home" };

export default function HomePage() {
  const index = getIndex();
  const stats = index.stats;

  return (
    <section className="home-page page-wrap">
      <div className="hero">
        <span className="eyebrow">YOUR SOURCE OF TRUTH</span>
        <h1>把面试手册变成<br /><em>可搜索、可追溯、可问答</em>的知识系统。</h1>
        <p>原始 Markdown 不动。这里负责阅读体验、跨模块全文检索，以及基于仓库证据回答问题的 RAG 层。</p>
        <div className="hero-actions">
          <Link className="primary-button" href="/docs/roadmap/learning-path">继续学习 →</Link>
          <Link className="secondary-button" href="/ask">✦ Ask your KB</Link>
        </div>
      </div>

      <div className="stat-strip">
        <div><strong>{stats.documents}</strong><span>Markdown 文档</span></div>
        <div><strong>{stats.chunks}</strong><span>可检索知识片段</span></div>
        <div><strong>{Math.round(stats.characters / 1000) / 10} 万</strong><span>正文字符</span></div>
        <div><strong>10</strong><span>正式学习模块</span></div>
      </div>

      <div className="section-heading-row">
        <div><span className="eyebrow">CURRICULUM</span><h2>十模块知识地图</h2></div>
        <Link href="/docs/roadmap/knowledge-map">打开完整 Knowledge Map →</Link>
      </div>

      <div className="module-grid">
        {PRIMARY_MODULES.map((module, index) => (
          <Link className="module-card" href={`/docs/${module.slug}/README`} key={module.slug}>
            <span className="module-number">{String(index + 1).padStart(2, "0")}</span>
            <small>{module.layer}</small><h3>{module.label}</h3><p>进入模块正文、Review、Interview 与相关证据。</p><span className="card-arrow">↗</span>
          </Link>
        ))}
      </div>

      <div className="feature-grid">
        <Link href="/search" className="feature-card"><span>⌕</span><h3>全文搜索</h3><p>中文、英文、代码术语和真人面经统一检索，不再靠目录逐层翻。</p></Link>
        <Link href="/ask" className="feature-card"><span>✦</span><h3>RAG 问答</h3><p>先检索你的知识片段，再回答，并把证据链接回原章节。</p></Link>
        <Link href="/docs/research/README" className="feature-card"><span>◎</span><h3>Evidence Layer</h3><p>课程知识和 HUMAN-A 真人面经保持分层，但能在同一界面里联查。</p></Link>
      </div>
    </section>
  );
}
