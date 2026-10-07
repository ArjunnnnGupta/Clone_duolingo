"use client";

import { motion } from "framer-motion";

interface ProgressBarProps {
  // 0 to 1; the caller decides what it measures.
  fraction: number;
  fillClassName?: string;
}

export function ProgressBar({ fraction, fillClassName = "bg-green" }: ProgressBarProps) {
  return (
    <div
      role="progressbar"
      aria-valuenow={Math.round(fraction * 100)}
      className="relative h-4 w-full overflow-hidden rounded-full bg-border"
    >
      <motion.div
        className={`relative h-full rounded-full ${fillClassName}`}
        initial={false}
        animate={{ width: `${fraction * 100}%` }}
        transition={{ type: "spring", stiffness: 120, damping: 20 }}
      >
        <span className="absolute inset-x-2 top-1 h-1 rounded-full bg-surface/30" />
      </motion.div>
    </div>
  );
}
