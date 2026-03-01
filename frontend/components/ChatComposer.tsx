"use client";
import { motion } from "framer-motion";

export default function ChatComposer({
  value, onChange, onSend, disabled
}:{ value:string; onChange:(v:string)=>void; onSend:()=>void; disabled?:boolean }) {
  return (
    <div className="glass rounded-2xl p-2 flex gap-2 items-center shadow-soft">
      <input
        value={value}
        onChange={(e)=>onChange(e.target.value)}
        onKeyDown={(e)=> e.key==="Enter" && !e.shiftKey && onSend()}
        placeholder="Ask about APR vs APY, debt avalanche, credit utilization…"
        className="flex-1 bg-transparent rounded-xl px-3 py-2 outline-none placeholder:text-zinc-500 focus:ring-0"
        aria-label="Your finance question"
      />
      <motion.button
        whileTap={{ scale: 0.96 }}
        whileHover={{ y: -1 }}
        onClick={onSend}
        disabled={disabled}
        className="rounded-xl bg-emerald-600 hover:bg-emerald-500 px-5 py-2.5 font-medium disabled:opacity-60 shadow-[0_10px_20px_rgba(16,185,129,.25)]"
      >
        Ask
      </motion.button>
    </div>
  );
}
