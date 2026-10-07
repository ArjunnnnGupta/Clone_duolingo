"use client";

import { useEffect, useRef } from "react";
import { Mascot } from "@/components/mascot/Mascot";
import { celebrate } from "@/lib/confetti";
import type { AttemptResult } from "@/lib/types";
import { CelebrationLayout } from "./CelebrationLayout";
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
      <Mascot className="h-40 w-40" />
      <h1 className="text-3xl font-extrabold text-gold-shade">Lesson Complete!</h1>
      <div className="flex gap-4">
        <StatCard tone="gold" label="Total XP" value={String(result.xp_earned)} icon="bolt" />
        <StatCard tone="green" label="Accuracy" value={`${result.accuracy}%`} icon="check" />
      </div>
    </CelebrationLayout>
  );
}
