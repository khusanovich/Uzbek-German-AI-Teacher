import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Sprachassistent - German Tutor",
  description: "AI tutor for learning German (Uzbek speakers)",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className="antialiased bg-gray-50">{children}</body>
    </html>
  );
}
