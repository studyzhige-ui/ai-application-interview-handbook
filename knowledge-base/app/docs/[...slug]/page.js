import { notFound } from "next/navigation";
import MarkdownArticle from "@/components/MarkdownArticle";
import { getAllDocuments, getDocumentBySlug } from "@/lib/kb";

export const dynamicParams = false;

export function generateStaticParams() {
  return getAllDocuments().map((doc) => ({ slug: doc.path.replace(/\.md$/i, "").split("/") }));
}

export async function generateMetadata({ params }) {
  const { slug } = await params;
  const doc = getDocumentBySlug(slug);
  return doc ? { title: doc.title, description: doc.excerpt } : {};
}

export default async function DocumentPage({ params }) {
  const { slug } = await params;
  const doc = getDocumentBySlug(slug);
  if (!doc) notFound();
  return <MarkdownArticle doc={doc} />;
}
