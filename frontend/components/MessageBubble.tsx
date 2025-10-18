"use client";
import { motion } from "framer-motion";

export default function MessageBubble({
  role, text, time
}: { role: "user" | "assistant"; text: string; time?: string }) {
  const isUser = role === "user";

  return (
    <motion.div
      initial={{ opacity: 0, y: 10, scale: 0.98 }}
      animate={{ opacity: 1, y: 0, scale: 1 }}
      transition={{ type: "spring", stiffness: 220, damping: 18 }}
      className={`relative max-w-[82%] rounded-2xl p-[1px] ${
        isUser
          ? "bg-gradient-to-br from-sky-500/35 via-sky-400/10 to-transparent"
          : "bg-gradient-to-br from-emerald-500/40 via-emerald-400/10 to-transparent"
      } ${isUser ? "ml-auto" : "mr-auto"}`}
    >
      <div className={`glass rounded-2xl px-4 py-3 shadow-soft`}>
        <div className="text-[10px] tracking-wider uppercase text-zinc-400 mb-1">
          {role}{time ? ` • ${time}` : ""}
        </div>
        <div className="whitespace-pre-wrap leading-relaxed text-[15px]">
          {text}
        </div>
      </div>
    </motion.div>
  );
}
