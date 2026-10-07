"use client";

import { motion } from "framer-motion";

interface WordTileProps {
  tileId: string;
  text: string;
  isDisabled: boolean;
  onClick: () => void;
}

// The shared layoutId lets one tile fly between the word bank and the answer line.
export function WordTile({ tileId, text, isDisabled, onClick }: WordTileProps) {
  return (
    <motion.button
      layout
      layoutId={tileId}
      disabled={isDisabled}
      onClick={onClick}
      className="rounded-2xl border-2 border-b-4 border-border bg-surface px-4 py-3 text-[17px] font-bold disabled:cursor-default"
    >
      {text}
    </motion.button>
  );
}
