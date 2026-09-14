export const PRIMARY_MODULES = [
  { slug: "python", label: "Python Foundation", short: "Python", layer: "Foundation" },
  { slug: "fastapi", label: "FastAPI", short: "FastAPI", layer: "Foundation" },
  { slug: "backend-engineering", label: "AI Backend Engineering", short: "Backend", layer: "Foundation" },
  { slug: "mysql", label: "MySQL", short: "MySQL", layer: "Data" },
  { slug: "redis", label: "Redis", short: "Redis", layer: "Data" },
  { slug: "vector-db", label: "Vector Database", short: "Vector DB", layer: "Data" },
  { slug: "llm-foundation", label: "LLM Foundation", short: "LLM", layer: "Model" },
  { slug: "rag", label: "RAG", short: "RAG", layer: "AI Application" },
  { slug: "agent-harness", label: "Agent Harness / Runtime", short: "Agent", layer: "Agent Runtime" },
  { slug: "system-design", label: "System Design", short: "System Design", layer: "Integration" },
];

export const EXTRA_AREAS = [
  { slug: "research", label: "真人面经研究库", href: "/docs/research/README" },
  { slug: "roadmap", label: "Roadmap / Audits", href: "/docs/roadmap/knowledge-map" },
];

export const KIND_LABELS = {
  curriculum: "系统正文",
  review: "复习",
  interview: "面试",
  "interview-source": "真人面经",
  canonical: "Canonical Questions",
  research: "研究",
  roadmap: "路线 / 审计",
  index: "模块入口",
  other: "其他",
};

export function moduleLabel(slug) {
  return PRIMARY_MODULES.find((item) => item.slug === slug)?.label
    ?? EXTRA_AREAS.find((item) => item.slug === slug)?.label
    ?? (slug === "root" ? "Knowledge Base" : slug);
}
