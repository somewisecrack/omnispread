import type { Metadata } from "next";
import { Inter, JetBrains_Mono } from "next/font/google";
import "./globals.css";

const inter = Inter({
  variable: "--font-inter",
  subsets: ["latin"],
  display: "swap",
});

const jetbrainsMono = JetBrains_Mono({
  variable: "--font-jetbrains",
  subsets: ["latin"],
  display: "swap",
});

export const metadata: Metadata = {
  title: "OMNISPREAD | Statistical Pairs Trading Scanner",
  description:
    "Scan equities for cointegration-based mean-reversion trading signals using Kalman-filtered spreads, Monte Carlo simulations, and advanced statistical tests.",
  keywords: ["pairs trading", "cointegration", "mean reversion", "statistical arbitrage", "quantitative trading"],
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body
        className={`${inter.variable} ${jetbrainsMono.variable}`}
        suppressHydrationWarning
        style={{
          fontFamily: "var(--font-inter), var(--font-sans)",
          minHeight: "100vh",
          background: "radial-gradient(ellipse at 50% 0%, rgba(99,102,241,0.08) 0%, transparent 60%), var(--color-bg-primary)",
        }}
      >
        {children}
      </body>
    </html>
  );
}
