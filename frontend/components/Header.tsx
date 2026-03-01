"use client";
import { motion } from "framer-motion";

export default function Header() {
  return (
    <motion.header
      initial={{ y: -20, opacity: 0 }}
      animate={{ y: 0, opacity: 1 }}
      transition={{ type: "spring", stiffness: 120, damping: 18 }}
      className="sticky top-0 z-20 glass"
    >
      <div className="mx-auto max-w-4xl px-5 py-3 flex items-center justify-between">
        <div className="flex items-center gap-2">
          <span className="inline-block h-2 w-2 rounded-full bg-emerald-400 shadow-[0_0_10px_2px_rgba(16,185,129,.7)]" />
          <span className="font-semibold tracking-tight">FinChat</span>
          <span className="text-emerald-300/80">✦</span>
        </div>
        <p className="text-xs text-zinc-400">Finance you can finally trust</p>
      </div>
    </motion.header>
  );
}
