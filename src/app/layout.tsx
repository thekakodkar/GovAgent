import type { Metadata } from "next";
import "./globals.css"; // Imports your clean dark theme styles natively

export const metadata: Metadata = {
  title: "govAgent Control Plane",
  description: "Sovereign AI Governance Control Plane & Telemetry Dashboard",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className="antialiased bg-slate-950 text-slate-100">
        {children} {/* This dynamically injects your custom page.tsx chat canvas */}
      </body>
    </html>
  );
}