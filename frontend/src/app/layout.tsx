import type { Metadata } from "next";
import { Nunito } from "next/font/google";
import "./globals.css";
import { APPLY_SAVED_THEME_SCRIPT } from "@/lib/theme";
import { Providers } from "./providers";

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
    <html
      lang="en"
      data-theme="light"
      // The inline script may switch data-theme to "dark" before React hydrates.
      suppressHydrationWarning
      className={`${nunito.variable} h-full antialiased`}
    >
      <head>
        <script dangerouslySetInnerHTML={{ __html: APPLY_SAVED_THEME_SCRIPT }} />
      </head>
      <body className="min-h-full flex flex-col">
        <Providers>{children}</Providers>
      </body>
    </html>
  );
}
