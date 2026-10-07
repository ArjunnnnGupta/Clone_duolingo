import { Icon } from "@/components/ui/Icon";
import type { DayActivity, MeStats } from "@/lib/types";
import { WeekStrip } from "./WeekStrip";

interface StreakPanelProps {
  stats: MeStats;
  days: DayActivity[];
}

// The streak count, "extended today" flag and week strip are all server values.
export function StreakPanel({ stats, days }: StreakPanelProps) {
  const message = stats.streak_active_today
    ? "You extended your streak today!"
    : "Finish a lesson today to keep your streak going.";

  return (
    <div className="flex flex-col gap-4">
      <div className="flex items-center justify-between rounded-2xl bg-orange p-4 text-on-color">
        <div>
          <h2 className="text-2xl font-extrabold">{stats.current_streak} day streak</h2>
          <p className="text-[15px]">{message}</p>
        </div>
        <Icon name="flame" className="h-14 w-14 shrink-0" />
      </div>
      <WeekStrip days={days} />
    </div>
  );
}
