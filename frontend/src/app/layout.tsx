import type { Metadata } from "next";
import { Nunito } from "next/font/google";
import "./globals.css";

// Duolingo text is almost never regular weight, so only bold and extra-bold are loaded.
const nunito = Nunito({
  variable: "--font-nunito",
  subsets: ["latin"],
  weight: ["700", "800"],
});

export const metadata: Metadata = {
  title: "Duolingo Clone",
  description: "A language-learning app with a server-owned lesson engine.",
};

export default function RootLayout({ children }: LayoutProps<"/">) {
  return (
    <html lang="en" className={`${nunito.variable} h-full antialiased`}>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
