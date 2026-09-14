import { NextResponse } from "next/server";
import { searchKnowledge } from "@/lib/search";

export const runtime = "nodejs";

export async function GET(request) {
  const { searchParams } = new URL(request.url);
  const q = (searchParams.get("q") || "").slice(0, 300);
  const module = searchParams.get("module") || "all";
  const kind = searchParams.get("kind") || "all";
  const requestedLimit = Number(searchParams.get("limit") || 20);
  const limit = Number.isFinite(requestedLimit) ? Math.min(Math.max(requestedLimit, 1), 50) : 20;

  const results = searchKnowledge(q, { module, kind, limit });
  return NextResponse.json({ query: q, results });
}
