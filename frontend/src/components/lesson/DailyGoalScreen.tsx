import { Icon } from "@/components/ui/Icon";
import { ProgressBar } from "@/components/ui/ProgressBar";
import type { AttemptResult } from "@/lib/types";
import { CelebrationLayout } from "./CelebrationLayout";

// Only shown when the server says this lesson is the one that met the goal, so the bar is full.
export function DailyGoalScreen({
  dailyGoal,
  onContinue,
}: {
  dailyGoal: AttemptResult["daily_goal"];
  onContinue: () => void;
}) {
  return (
    <CelebrationLayout onContinue={onContinue}>
      <Icon name="bolt" className="h-32 w-32 text-gold" />
      <h1 className="text-3xl font-extrabold text-gold-shade">Daily goal reached!</h1>
      <div className="w-full max-w-[420px]">
        <ProgressBar fraction={1} />
        <p className="mt-3 text-[17px] text-text-muted">
          {dailyGoal.today_xp} / {dailyGoal.goal_xp} XP today
        </p>
      </div>
    </CelebrationLayout>
  );
}
