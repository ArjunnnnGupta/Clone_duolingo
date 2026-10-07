"use client";

import { motion } from "framer-motion";
import { useEffect, useRef } from "react";
import { Mascot } from "@/components/mascot/Mascot";
import { celebrate } from "@/lib/confetti";
import type { AttemptResult } from "@/lib/types";
import { CelebrationLayout } from "./CelebrationLayout";
import { CountUp } from "./CountUp";
import { StatCard } from "./StatCard";

// Read-only: XP and accuracy are the figures the server stored when it finalized the lesson.
export function LessonCompleteScreen({
  result,
  onContinue,
}: {
  result: AttemptResult;
  onContinue: () => void;
}) {
  const hasCelebrated = useRef(false);

  useEffect(() => {
    // Once per mount; development's double-invoked effects would otherwise fire two bursts.
    if (!hasCelebrated.current) {
      hasCelebrated.current = true;
      celebrate();
    }
  }, []);

  return (
    <CelebrationLayout onContinue={onContinue}>
      {/* The cat jumps twice for joy. */}
      <motion.div
        animate={{ y: [0, -28, 0] }}
        transition={{ duration: 0.5, repeat: 1, delay: 0.2, ease: "easeOut" }}
      >
        <Mascot className="h-40 w-40" pose="happy" />
      </motion.div>
      <h1 className="text-3xl font-extrabold text-gold-shade">Lesson Complete!</h1>
      {/* Cards scale in one after the other; XP counts up to the server's figure. */}
      <motion.div
        className="flex gap-4"
        initial="hidden"
        animate="shown"
        transition={{ staggerChildren: 0.15, delayChildren: 0.2 }}
      >
        <StatCard tone="gold" label="Total XP" value={<CountUp to={result.xp_earned} />} icon="bolt" />
        <StatCard tone="green" label="Accuracy" value={`${result.accuracy}%`} icon="check" />
      </motion.div>
    </CelebrationLayout>
  );
}
