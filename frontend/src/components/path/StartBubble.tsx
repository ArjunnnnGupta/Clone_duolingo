"use client";

import { motion } from "framer-motion";

// -mb-3 lets the bubble overlap the top of the progress ring so its tail touches the node.
export function StartBubble({ textClassName }: { textClassName: string }) {
  return (
    <motion.div
      animate={{ y: [0, -4, 0] }}
      transition={{ duration: 1.2, repeat: Infinity, ease: "easeInOut" }}
      className="pointer-events-none absolute bottom-full left-1/2 -mb-3 -translate-x-1/2"
    >
      <span
        className={`relative block rounded-xl border-2 border-border bg-surface px-4 py-2 text-[15px] font-extrabold uppercase tracking-[0.8px] ${textClassName}`}
      >
        Start
        <span className="absolute -bottom-[7px] left-1/2 h-3 w-3 -translate-x-1/2 rotate-45 border-b-2 border-r-2 border-border bg-surface" />
      </span>
    </motion.div>
  );
}
