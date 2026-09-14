import fs from "node:fs";
import path from "node:path";
import { fileURLToPath } from "node:url";

const HERE = path.dirname(fileURLToPath(import.meta.url));
const INDEX_FILE = path.resolve(HERE, "../generated/index.json");
let cache;

export function getIndex() {
  if (!cache) {
    cache = JSON.parse(fs.readFileSync(INDEX_FILE, "utf8"));
  }
  return cache;
}

export function getAllDocuments() {
  return getIndex().documents;
}

export function getDocumentByPath(repoPath) {
  return getIndex().documents.find((doc) => doc.path === repoPath) ?? null;
}

export function getDocumentBySlug(slug = []) {
  const parts = Array.isArray(slug) ? slug : [slug];
  const decoded = parts.map((part) => {
    try { return decodeURIComponent(part); } catch { return part; }
  });
  const repoPath = `${decoded.join("/")}.md`;
  return getDocumentByPath(repoPath);
}

export function docHref(repoPath, anchor = "") {
  const withoutExtension = repoPath.replace(/\.md$/i, "");
  const encoded = withoutExtension
    .split("/")
    .map((segment) => encodeURIComponent(segment))
    .join("/");
  return `/docs/${encoded}${anchor ? `#${anchor}` : ""}`;
}

export function resolveMarkdownHref(currentPath, href) {
  if (!href || /^(https?:|mailto:|tel:|#)/i.test(href)) return href;
  const [target, hash = ""] = href.split("#");
  if (!target.toLowerCase().endsWith(".md")) return href;
  const resolved = path.posix.normalize(path.posix.join(path.posix.dirname(currentPath), target));
  return docHref(resolved, hash);
}
