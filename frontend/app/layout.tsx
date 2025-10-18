import "./globals.css";
import { Plus_Jakarta_Sans } from "next/font/google";

const font = Plus_Jakarta_Sans({ subsets: ["latin"], weight: ["400","600","700"] });

export const metadata = { title: "FinChat", description: "Finance you can finally trust" };

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body className={`${font.className} min-h-screen antialiased bg-[#07090c] text-zinc-100`}>
        {/* animated radial + grid background */}
        <div className="fixed inset-0 -z-10 overflow-hidden">
          <div className="pointer-events-none absolute inset-0 bg-[radial-gradient(1200px_600px_at_50%_-20%,rgba(16,185,129,0.18),transparent_60%)]" />
          <div className="pointer-events-none absolute inset-0 bg-[linear-gradient(transparent,transparent),radial-gradient(circle_at_20%_20%,rgba(59,130,246,0.15),transparent_30%),radial-gradient(circle_at_80%_30%,rgba(16,185,129,0.12),transparent_35%)]" />
          <div className="absolute inset-0 opacity-[0.08] [background:linear-gradient(#fff_1px,transparent_1px),linear-gradient(90deg,#fff_1px,transparent_1px)] bg-[size:28px_28px]" />
        </div>
        {children}
      </body>
    </html>
  );
}
