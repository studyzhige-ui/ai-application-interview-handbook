import SearchPageClient from "@/components/SearchPageClient";

export const metadata = { title: "Full Search" };

export default async function SearchPage({ searchParams }) {
  const params = await searchParams;
  return <SearchPageClient initialQuery={params?.q ?? ""} />;
}
