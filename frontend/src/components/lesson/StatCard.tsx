"use client";

import { motion } from "framer-motion";
import type { ReactNode } from "react";
import { Icon, type IconName } from "@/components/ui/Icon";

const TONE_CLASSES = {
  gold: { header: "bg-gold", border: "border-gold", text: "text-gold-shade" },
  green: { header: "bg-green", border: "border-green", text: "text-green" },
} as const;

// Scale-in used by LessonCompleteScreen's staggered entrance.
export const STAT_CARD_ENTRANCE = {
  hidden: { opacity: 0, scale: 0.6 },
  shown: { opacity: 1, scale: 1, transition: { type: "spring" as const, stiffness: 260, damping: 18 } },
};

interface StatCardProps {
  tone: keyof typeof TONE_CLASSES;
  label: string;
  value: ReactNode;
  icon: IconName;
}

export function StatCard({ tone, label, value, icon }: StatCardProps) {
  const classes = TONE_CLASSES[tone];
  return (
    <motion.div
      variants={STAT_CARD_ENTRANCE}
      className={`w-36 overflow-hidden rounded-2xl border-2 ${classes.border}`}
    >
      <p className={`py-1 text-center text-xs font-extrabold uppercase text-on-color ${classes.header}`}>
        {label}
      </p>
      <p className={`flex items-center justify-center gap-2 py-4 text-2xl font-extrabold ${classes.text}`}>
        <Icon name={icon} className="h-6 w-6" />
        {value}
      </p>
    </motion.div>
  );
}
