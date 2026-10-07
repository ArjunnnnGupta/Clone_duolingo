"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";

interface PopoverCardProps {
  cardClassName: string;
  tailClassName: string;
  // Horizontal offset of the node it points at, so the tail stays under the zig-zagged node.
  tailOffset: number;
  children: ReactNode;
}

export function PopoverCard({ cardClassName, tailClassName, tailOffset, children }: PopoverCardProps) {
  // Starts 8px up so the card tucks under the node's 3D edge; z-50 keeps it above the click-away
  // layer. Width caps at 300px but leaves a 16px gutter each side on phones.
  return (
    <div className="absolute inset-x-0 top-[calc(100%-8px)] z-50 flex justify-center">
      <motion.div
        initial={{ opacity: 0, y: -8 }}
        animate={{ opacity: 1, y: 0 }}
        className={`relative mt-3 w-[min(300px,calc(100vw-32px))] rounded-2xl p-4 ${cardClassName}`}
      >
        <span
          className={`absolute -top-2 h-4 w-4 rotate-45 ${tailClassName}`}
          style={{ left: `calc(50% + ${tailOffset}px - 8px)` }}
        />
        {children}
      </motion.div>
    </div>
  );
}
