"use client";
import { useState } from "react";
import { AnimatePresence, motion } from "framer-motion";

export default function SourcesPanel({ sources }:{
  sources: { source: string; score?: number }[];
}) {
  const [open, setOpen] = useState(false);
  if (!sources?.length) return null;

  return (
    <div className="mt-2">
      <button
        onClick={() => setOpen(s => !s)}
        className="text-xs text-emerald-300 hover:text-emerald-200 underline underline-offset-4"
      >
        {open ? "Hide details" : "Why this answer?"}
      </button>

      <AnimatePresence initial={false}>
        {open && (
          <motion.div
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ type: "spring", stiffness: 140, damping: 18 }}
            className="overflow-hidden rounded-xl border border-white/10 bg-black/40 p-3 mt-2"
          >
            <ul className="grid gap-2">
              {sources.map((s, i) => (
                <li key={i} className="flex items-center justify-between bg-white/5 rounded-lg px-3 py-2">
                  <span className="font-mono text-xs">{s.source}</span>
                  {typeof s.score === "number" && (
                    <span className="text-[11px] text-zinc-400">score {s.score.toFixed(2)}</span>
                  )}
                </li>
              ))}
            </ul>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
