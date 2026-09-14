import "./globals.css";
import AppShell from "@/components/AppShell";

export const metadata = {
  title: {
    default: "AI Application Knowledge Base",
    template: "%s · AI Application KB",
  },
  description: "Personal knowledge base UI for the AI Application Interview Handbook.",
};

export default function RootLayout({ children }) {
  return (
    <html lang="zh-CN" suppressHydrationWarning>
      <body><AppShell>{children}</AppShell></body>
    </html>
  );
}
