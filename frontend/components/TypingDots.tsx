"use client";
import { motion } from "framer-motion";

export default function TypingDots() {
  return (
    <div className="flex items-center gap-1 text-zinc-400">
      {[0,1,2].map(i=>(
        <motion.span
          key={i}
          initial={{ opacity: .3, y: 0 }}
          animate={{ opacity: 1, y: -2 }}
          transition={{ repeat: Infinity, repeatType: "reverse", duration: .6, delay: i * 0.15 }}
          className="inline-block h-2 w-2 rounded-full bg-zinc-400"
        />
      ))}
      <span className="ml-2 text-sm">Thinking…</span>
    </div>
  );
}
