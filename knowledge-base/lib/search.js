import { getIndex, docHref } from "@/lib/kb";

function normalize(value = "") {
  return value.toLowerCase().normalize("NFKC").replace(/\s+/g, " ").trim();
}

function queryTokens(query) {
  const normalized = normalize(query);
  const tokens = new Set();
  if (normalized.length >= 2) tokens.add(normalized);

  for (const word of normalized.match(/[a-z0-9_+.#/-]{2,}/g) ?? []) tokens.add(word);
  for (const sequence of normalized.match(/[\p{Script=Han}]{2,}/gu) ?? []) {
    tokens.add(sequence);
    if (sequence.length > 2) {
      for (let i = 0; i < sequence.length - 1; i += 1) tokens.add(sequence.slice(i, i + 2));
    }
  }

  return [...tokens].sort((a, b) => b.length - a.length).slice(0, 24);
}

function scoreText(haystack, needle, weight) {
  if (!needle || !haystack.includes(needle)) return 0;
  const first = haystack.indexOf(needle);
  const count = Math.min(4, haystack.split(needle).length - 1);
  return weight * count + Math.max(0, 3 - Math.floor(first / 300));
}

function scoreChunk(chunk, normalizedQuery, tokens) {
  const title = normalize(chunk.title);
  const heading = normalize(chunk.heading);
  const text = normalize(chunk.text);
  let score = 0;

  score += scoreText(title, normalizedQuery, 36);
  score += scoreText(heading, normalizedQuery, 28);
  score += scoreText(text, normalizedQuery, 12);

  for (const token of tokens) {
    score += scoreText(title, token, 9);
    score += scoreText(heading, token, 7);
    score += scoreText(text, token, token.length <= 2 ? 1.2 : 2.4);
  }

  if (chunk.kind === "curriculum") score += 1.5;
  if (chunk.kind === "review") score += 0.5;
  return score;
}

function makeSnippet(text, query, maxLength = 260) {
  const normalizedText = normalize(text);
  const normalizedQuery = normalize(query);
  let position = normalizedText.indexOf(normalizedQuery);

  if (position < 0) {
    const token = queryTokens(query).find((item) => normalizedText.includes(item));
    position = token ? normalizedText.indexOf(token) : 0;
  }

  const start = Math.max(0, position - 80);
  const end = Math.min(text.length, start + maxLength);
  const prefix = start > 0 ? "…" : "";
  const suffix = end < text.length ? "…" : "";
  return `${prefix}${text.slice(start, end).trim()}${suffix}`;
}

export function searchKnowledge(query, options = {}) {
  const normalizedQuery = normalize(query);
  if (!normalizedQuery) return [];

  const { module, kind, limit = 20, diversify = false } = options;
  const tokens = queryTokens(query);
  const scored = [];

  for (const chunk of getIndex().chunks) {
    if (module && module !== "all" && chunk.module !== module) continue;
    if (kind && kind !== "all" && chunk.kind !== kind) continue;
    const score = scoreChunk(chunk, normalizedQuery, tokens);
    if (score <= 0) continue;
    scored.push({ chunk, score });
  }

  scored.sort((a, b) => b.score - a.score);
  const results = [];
  const perDoc = new Map();

  for (const { chunk, score } of scored) {
    if (diversify) {
      const count = perDoc.get(chunk.path) ?? 0;
      if (count >= 2) continue;
      perDoc.set(chunk.path, count + 1);
    }
    results.push({
      ...chunk,
      score: Math.round(score * 100) / 100,
      href: docHref(chunk.path, chunk.anchor),
      snippet: makeSnippet(chunk.text, query),
    });
    if (results.length >= limit) break;
  }

  return results;
}
