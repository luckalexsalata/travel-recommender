import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Travel Recommender - AI Travel Recommendations",
  description: "Отримай персональні туристичні рекомендації з штучним інтелектом",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="uk">
      <body className="antialiased">
        {children}
      </body>
    </html>
  );
}
