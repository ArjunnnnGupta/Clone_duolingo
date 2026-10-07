"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";

const STATE_CLASSES = {
  default: "border-border bg-surface hover:bg-surface-subtle",
  selected: "border-blue bg-blue/10 text-blue",
  correct: "border-green bg-green/10 text-green",
  wrong: "border-red bg-red/10 text-red",
  matched: "pointer-events-none border-border bg-surface-subtle text-text-subtle opacity-50",
} as const;

// A right answer pulses; a wrong one shakes sideways.
const STATE_ANIMATIONS = {
  correct: { scale: [1, 1.04, 1], transition: { duration: 0.35 } },
  wrong: { x: [0, -8, 8, -6, 6, 0], transition: { duration: 0.4 } },
};

export type OptionCardState = keyof typeof STATE_CLASSES;

interface OptionCardProps {
  state?: OptionCardState;
  keyHint?: string;
  isDisabled?: boolean;
  onClick: () => void;
  children: ReactNode;
}

// White 3D card shared by multiple choice, fill-blank and match pairs.
export function OptionCard({
  state = "default",
  keyHint,
  isDisabled = false,
  onClick,
  children,
}: OptionCardProps) {
  return (
    <motion.button
      disabled={isDisabled}
      onClick={onClick}
      animate={state === "correct" || state === "wrong" ? STATE_ANIMATIONS[state] : undefined}
      className={`flex w-full items-center gap-4 rounded-2xl border-2 border-b-4 px-4 py-3 text-left text-[17px] font-bold active:translate-y-0.5 active:border-b-2 disabled:cursor-default ${STATE_CLASSES[state]}`}
    >
      {keyHint && (
        <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border-2 border-current text-sm opacity-60">
          {keyHint}
        </span>
      )}
      <span className="flex flex-1 items-center justify-center gap-3">{children}</span>
    </motion.button>
  );
}

// The selected option's look: blue while choosing, then green or red once checked.
export function selectedState(verdict: "correct" | "wrong" | null): OptionCardState {
  return verdict ?? "selected";
}
