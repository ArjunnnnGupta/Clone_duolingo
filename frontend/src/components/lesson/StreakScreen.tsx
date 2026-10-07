"use client";

import { motion } from "framer-motion";
import { Mascot } from "@/components/mascot/Mascot";
import { Icon } from "@/components/ui/Icon";
import { WeekStrip } from "@/components/gamification/WeekStrip";
import { useMe } from "@/lib/queries";
import type { AttemptResult } from "@/lib/types";
import { CelebrationLayout } from "./CelebrationLayout";

// The streak count is the server's, from the finalized lesson. The week strip comes from /me,
// which the completing answer already refreshed.
export function StreakScreen({
  streak,
  onContinue,
}: {
  streak: AttemptResult["streak"];
  onContinue: () => void;
}) {
  const { data: me } = useMe();

  return (
    <CelebrationLayout onContinue={onContinue}>
      <div className="flex items-end">
        <Mascot className="h-28 w-28" pose="happy" />
        <motion.div
          initial={{ scale: 0, rotate: -15 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ type: "spring", stiffness: 160, damping: 12 }}
        >
          <Icon name="flame" className="h-36 w-36 text-orange" />
        </motion.div>
      </div>
      <h1 className="text-3xl font-extrabold text-orange">{streak.count} day streak!</h1>
      {me && (
        <div className="w-full max-w-[420px]">
          <WeekStrip days={me.recent_days} />
        </div>
      )}
      <p className="text-[17px] text-text-muted">Practice tomorrow to keep it going.</p>
    </CelebrationLayout>
  );
}
