import Link from "next/link";
import SearchPalette from "@/components/SearchPalette";
import ThemeToggle from "@/components/ThemeToggle";
import { EXTRA_AREAS, PRIMARY_MODULES } from "@/lib/config";

export default function AppShell({ children }) {
  return (
    <div className="app-shell">
      <aside className="sidebar">
        <Link className="brand" href="/">
          <span className="brand-mark">KB</span>
          <span><strong>AI Application</strong><small>Personal Knowledge Base</small></span>
        </Link>
        <nav className="side-nav">
          <p className="nav-label">学习主线</p>
          {PRIMARY_MODULES.map((item, index) => (
            <Link key={item.slug} href={item.href || `/docs/${item.slug}/README`}>
              <span className="nav-index">{String(index + 1).padStart(2, "0")}</span>
              <span>{item.short}</span>
            </Link>
          ))}
          <p className="nav-label nav-label-spaced">研究与路线</p>
          {EXTRA_AREAS.map((item) => (
            <Link key={item.slug} href={item.href || `/docs/${item.slug}/README`}>
              <span className="nav-index">·</span><span>{item.label}</span>
            </Link>
          ))}
        </nav>
        <div className="sidebar-footer">
          <Link href="/ask">✦ Ask KB</Link>
          <Link href="/search">⌕ Full Search</Link>
        </div>
      </aside>

      <div className="workspace">
        <header className="topbar">
          <SearchPalette />
          <div className="topbar-actions">
            <Link className="ask-link" href="/ask">✦ Ask</Link>
            <ThemeToggle />
          </div>
        </header>
        <main className="main-content">{children}</main>
      </div>
    </div>
  );
}
