import fs from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

class LocalSlugger {
  constructor() { this.seen = new Map(); }
  slug(value) {
    const base = String(value)
      .trim()
      .toLowerCase()
      .replace(/<[^>]+>/g, "")
      .replace(/[\s]+/g, "-")
      .replace(/[\u0000-\u001f\u007f!\"#$%&'()*+,./:;<=>?@[\\\]^`{|}~]/g, "")
      .replace(/-+/g, "-");
    const count = this.seen.get(base) || 0;
    this.seen.set(base, count + 1);
    return count === 0 ? base : `${base}-${count}`;
  }
}

const HERE = path.dirname(fileURLToPath(import.meta.url));
const APP_ROOT = path.resolve(HERE, "..");
const REPO_ROOT = path.resolve(process.env.KB_REPO_ROOT || path.join(APP_ROOT, ".."));
const OUT_DIR = path.join(APP_ROOT, "generated");
const OUT_FILE = path.join(OUT_DIR, "index.json");

const MODULE_ORDER = new Map([
  ["root", 0], ["python", 10], ["fastapi", 20], ["backend-engineering", 30],
  ["mysql", 40], ["redis", 50], ["vector-db", 60], ["llm-foundation", 70],
  ["rag", 80], ["agent-harness", 90], ["system-design", 100], ["roadmap", 110], ["research", 120],
]);

const SKIP_DIRS = new Set([".git", ".next", "node_modules", "knowledge-base"]);

async function walk(dir) {
  const entries = await fs.readdir(dir, { withFileTypes: true });
  const files = [];
  for (const entry of entries) {
    if (entry.isDirectory() && SKIP_DIRS.has(entry.name)) continue;
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) files.push(...await walk(full));
    else if (entry.isFile() && entry.name.toLowerCase().endsWith(".md")) files.push(full);
  }
  return files;
}

function relativeRepoPath(file) {
  return path.relative(REPO_ROOT, file).split(path.sep).join("/");
}

function getModule(repoPath) {
  const [first] = repoPath.split("/");
  return MODULE_ORDER.has(first) ? first : "root";
}

function getKind(repoPath) {
  if (repoPath.startsWith("research/interviews/")) return "interview-source";
  if (repoPath.startsWith("research/questions/")) return "canonical";
  if (repoPath.startsWith("research/")) return "research";
  if (repoPath.startsWith("roadmap/")) return "roadmap";
  if (repoPath.includes("/docs/")) return "curriculum";
  if (repoPath.includes("/review/")) return "review";
  if (repoPath.includes("/interview/")) return "interview";
  if (repoPath.endsWith("README.md")) return "index";
  return "other";
}

function cleanInline(value) {
  return value.replace(/<[^>]+>/g, "").replace(/\[([^\]]+)\]\([^\)]+\)/g, "$1").replace(/[*_~`]/g, "").trim();
}

function titleFromMarkdown(markdown, repoPath) {
  const match = markdown.match(/^#\s+(.+)$/m);
  return match ? cleanInline(match[1]) : path.posix.basename(repoPath, ".md");
}

function stripMarkdown(markdown) {
  return markdown
    .replace(/```[\s\S]*?```/g, (block) => block.replace(/```[^\n]*\n?|```/g, " "))
    .replace(/<details>|<\/details>|<summary>|<\/summary>/gi, " ")
    .replace(/<[^>]+>/g, " ")
    .replace(/!\[([^\]]*)\]\([^\)]+\)/g, "$1")
    .replace(/\[([^\]]+)\]\([^\)]+\)/g, "$1")
    .replace(/^#{1,6}\s+/gm, "").replace(/^>\s?/gm, "").replace(/^[-*+]\s+/gm, "")
    .replace(/^\d+\.\s+/gm, "").replace(/[|]/g, " ").replace(/[*_~`]/g, "")
    .replace(/\s+/g, " ").trim();
}

function headingTree(markdown) {
  const slugger = new LocalSlugger();
  const headings = [];
  for (const line of markdown.split(/\r?\n/)) {
    const match = line.match(/^(#{1,4})\s+(.+)$/);
    if (!match) continue;
    const text = cleanInline(match[2]);
    headings.push({ level: match[1].length, text, anchor: slugger.slug(text) });
  }
  return headings;
}

function splitIntoSections(markdown, title) {
  const slugger = new LocalSlugger();
  const lines = markdown.split(/\r?\n/);
  const sections = [];
  let current = { heading: title, anchor: "", level: 1, lines: [] };
  const flush = () => {
    const text = stripMarkdown(current.lines.join("\n"));
    if (text) sections.push({ ...current, text });
  };
  for (const line of lines) {
    const match = line.match(/^(#{1,4})\s+(.+)$/);
    if (match) {
      flush();
      const heading = cleanInline(match[2]);
      current = { heading, anchor: slugger.slug(heading), level: match[1].length, lines: [] };
    } else current.lines.push(line);
  }
  flush();
  return sections;
}

function splitLongText(text, target = 1500, overlap = 180) {
  if (text.length <= target) return [text];
  const chunks = [];
  let start = 0;
  while (start < text.length) {
    let end = Math.min(start + target, text.length);
    if (end < text.length) {
      const sentenceEnd = Math.max(text.lastIndexOf("。", end), text.lastIndexOf("！", end), text.lastIndexOf("？", end), text.lastIndexOf(". ", end));
      if (sentenceEnd > start + Math.floor(target * 0.6)) end = sentenceEnd + 1;
    }
    chunks.push(text.slice(start, end).trim());
    if (end >= text.length) break;
    start = Math.max(end - overlap, start + 1);
  }
  return chunks.filter(Boolean);
}

const files = await walk(REPO_ROOT);
const documents = [];
const chunks = [];

for (const file of files) {
  const repoPath = relativeRepoPath(file);
  const markdown = await fs.readFile(file, "utf8");
  const title = titleFromMarkdown(markdown, repoPath);
  const module = getModule(repoPath);
  const kind = getKind(repoPath);
  const headings = headingTree(markdown).filter((heading) => heading.level >= 2 && heading.level <= 3);
  const plainText = stripMarkdown(markdown);
  documents.push({ path: repoPath, title, module, kind, headings, markdown, excerpt: plainText.slice(0, 260), characters: plainText.length });

  for (const section of splitIntoSections(markdown, title)) {
    splitLongText(section.text).forEach((piece, index) => {
      chunks.push({
        id: `${repoPath}::${section.anchor || "top"}::${index}`,
        path: repoPath, title, module, kind, heading: section.heading, anchor: section.anchor, text: piece,
      });
    });
  }
}

documents.sort((a, b) => {
  const moduleDiff = (MODULE_ORDER.get(a.module) ?? 999) - (MODULE_ORDER.get(b.module) ?? 999);
  return moduleDiff || a.path.localeCompare(b.path, "zh-CN", { numeric: true });
});

const stats = {
  documents: documents.length,
  chunks: chunks.length,
  characters: documents.reduce((sum, doc) => sum + doc.characters, 0),
  modules: [...new Set(documents.map((doc) => doc.module))].length,
};

await fs.mkdir(OUT_DIR, { recursive: true });
await fs.writeFile(OUT_FILE, JSON.stringify({ builtAt: new Date().toISOString(), repoRoot: path.basename(REPO_ROOT), stats, documents, chunks }, null, 2));
console.log(`Knowledge index built: ${stats.documents} docs / ${stats.chunks} chunks -> ${OUT_FILE}`);
