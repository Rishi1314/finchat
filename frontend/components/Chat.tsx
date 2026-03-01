"use client";
import { useState } from "react";
import { ask, AskRes } from "@/lib/api";
import MessageBubble from "./MessageBubble";
import SourcesPanel from "./SourcesPanel";
import ChatComposer from "./ChatComposer";
import TypingDots from "./TypingDots";
import { motion, AnimatePresence } from "framer-motion";

type Msg = { role:"user"|"assistant"; text:string; sources?:AskRes["sources"]; confidence?:string; latency_ms?:number };

const list = { hidden: {}, show: { transition: { staggerChildren: .05 } } };

export default function Chat() {
  const [q, setQ] = useState("");
  const [loading, setLoading] = useState(false);
  const [msgs, setMsgs] = useState<Msg[]>([
    { role:"assistant", text:"Hi! Ask me a finance question (e.g., APR vs APY, debt avalanche vs snowball)." }
  ]);

  async function onSend() {
    const prompt = q.trim(); if (!prompt) return;
    setMsgs(m => [...m, { role:"user", text:prompt }]);
    setQ(""); setLoading(true);
    try {
      const res = await ask(prompt);
      setMsgs(m => [...m, { role:"assistant", text:res.answer, sources:res.sources, confidence:res.confidence, latency_ms:res.latency_ms }]);
    } catch {
      setMsgs(m => [...m, { role:"assistant", text:"Sorry—network hiccup. Please try again." }]);
    } finally { setLoading(false); }
  }

  return (
    <div className="mx-auto max-w-4xl px-5 py-6">
      <motion.div variants={list} initial="hidden" animate="show" className="space-y-4 pb-36" aria-live="polite">
        {msgs.map((m, i) => (
          <div key={i}>
            <MessageBubble role={m.role} text={m.text}/>
            {m.role==="assistant" && (
              <>
                <div className="mt-1 text-[11px] text-zinc-400">
                  {m.confidence && <>Confidence: {m.confidence}</>}
                  {typeof m.latency_ms==="number" && <> • {m.latency_ms} ms</>}
                </div>
                {m.sources && <SourcesPanel sources={m.sources} />}
              </>
            )}
          </div>
        ))}

        <AnimatePresence>
          {loading && (
            <motion.div
              initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
              className="mr-auto"
            >
              <div className="glass rounded-2xl px-4 py-3">
                <TypingDots />
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </motion.div>

      {/* floating dock */}
      <div className="fixed bottom-4 left-1/2 -translate-x-1/2 w-full px-4">
        <div className="mx-auto max-w-3xl">
          <ChatComposer value={q} onChange={setQ} onSend={onSend} disabled={loading}/>
          <p className="pt-2 text-[11px] text-zinc-400 text-center">Educational only — not financial advice.</p>
        </div>
      </div>
    </div>
  );
}
