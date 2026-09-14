import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";
import rehypeSlug from "rehype-slug";
import rehypeSanitize, { defaultSchema } from "rehype-sanitize";
import { resolveMarkdownHref } from "@/lib/kb";

const schema = {
  ...defaultSchema,
  tagNames: [...new Set([...(defaultSchema.tagNames || []), "details", "summary"])],
  attributes: {
    ...defaultSchema.attributes,
    code: [...(defaultSchema.attributes?.code || []), ["className"]],
  },
};

export default function MarkdownArticle({ doc }) {
  return (
    <div className="doc-layout">
      <article className="markdown-body">
        <div className="doc-meta">
          <span>{doc.module}</span><span>·</span><span>{doc.kind}</span><span>·</span><code>{doc.path}</code>
        </div>
        <ReactMarkdown
          remarkPlugins={[remarkGfm]}
          rehypePlugins={[rehypeRaw, [rehypeSanitize, schema], rehypeSlug]}
          components={{
            a({ href = "", children, ...props }) {
              const resolved = resolveMarkdownHref(doc.path, href);
              const external = /^https?:\/\//i.test(resolved || "");
              return <a href={resolved} target={external ? "_blank" : undefined} rel={external ? "noreferrer" : undefined} {...props}>{children}</a>;
            },
          }}
        >
          {doc.markdown}
        </ReactMarkdown>
      </article>
      <aside className="toc">
        <p className="toc-title">本页目录</p>
        <nav>
          {doc.headings.slice(0, 28).map((heading) => (
            <a className={`toc-level-${heading.level}`} key={`${heading.anchor}-${heading.text}`} href={`#${heading.anchor}`}>{heading.text}</a>
          ))}
        </nav>
      </aside>
    </div>
  );
}
