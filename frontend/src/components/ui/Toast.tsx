"use client";

import { AnimatePresence, motion } from "framer-motion";

// Top-centre pill; ToastProvider decides when it appears and disappears.
export function Toast({ message }: { message: string | null }) {
  return (
    <AnimatePresence>
      {message && (
        <motion.p
          key={message}
          role="status"
          initial={{ opacity: 0, y: -16 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -16 }}
          className="pointer-events-none fixed left-1/2 top-4 z-[60] -translate-x-1/2 rounded-full bg-text px-5 py-3 text-[15px] font-extrabold text-surface"
        >
          {message}
        </motion.p>
      )}
    </AnimatePresence>
  );
}
