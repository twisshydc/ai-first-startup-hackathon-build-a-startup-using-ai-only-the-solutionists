import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Solutionists — NZ → India Honey Trade Intelligence",
  description:
    "Trade intelligence and operations platform for New Zealand honey companies entering India.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>{children}</body>
    </html>
  );
}
