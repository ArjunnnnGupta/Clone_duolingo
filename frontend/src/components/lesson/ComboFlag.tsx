"use client";

import { AnimatePresence, motion } from "framer-motion";

// "N IN A ROW" over the progress bar from 3 correct answers in a row; it pops on every new one.
export function ComboFlag({ combo }: { combo: number }) {
  return (
    <AnimatePresence>
      {combo >= 3 && (
        <motion.span
          key={combo}
          initial={{ opacity: 0, y: 6, scale: 0.8 }}
          animate={{ opacity: 1, y: 0, scale: 1 }}
          exit={{ opacity: 0 }}
          className="absolute -top-5 left-2 text-xs font-extrabold uppercase tracking-[0.8px] text-orange"
        >
          {combo} in a row
        </motion.span>
      )}
    </AnimatePresence>
  );
}
