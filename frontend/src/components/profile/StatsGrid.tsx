import type { ProfileResponse } from "@/lib/types";
import { StatTile } from "./StatTile";

// Each tile shows a field exactly as the server sent it.
export function StatsGrid({ profile }: { profile: ProfileResponse }) {
  const { stats, course_progress: progress } = profile;
  return (
    <div className="grid grid-cols-2 gap-3">
      <StatTile icon="flame" iconClassName="text-orange" value={String(stats.current_streak)} label="Day streak" />
      <StatTile icon="bolt" iconClassName="text-gold" value={stats.total_xp.toLocaleString()} label="Total XP" />
      <StatTile icon="flame" iconClassName="text-text-subtle" value={String(stats.longest_streak)} label="Longest streak" />
      <StatTile
        icon="check"
        iconClassName="text-green"
        value={`${progress.skills_completed} / ${progress.skills_total}`}
        label="Skills completed"
      />
    </div>
  );
}
