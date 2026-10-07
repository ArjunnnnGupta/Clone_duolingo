"use client";

import { Skeleton } from "@/components/ui/Skeleton";
import { useMe } from "@/lib/queries";
import { CourseFlag } from "./CourseFlag";
import { GemsBadge } from "./GemsBadge";
import { HeartsBadge } from "./HeartsBadge";
import { StreakBadge } from "./StreakBadge";
import { XpPill } from "./XpPill";

// Every number is rendered exactly as the server sent it.
export function StatsBar() {
  const { data: me, isError } = useMe();

  if (isError) {
    return <p className="text-sm text-text-muted">Could not load your stats.</p>;
  }
  if (!me) {
    return <Skeleton className="h-8 w-full" />;
  }

  const { stats } = me;
  return (
    <div className="flex w-full items-center justify-between gap-3">
      <CourseFlag />
      <StreakBadge days={stats.current_streak} isActiveToday={stats.streak_active_today} />
      <XpPill totalXp={stats.total_xp} />
      <GemsBadge gems={stats.gems} />
      <HeartsBadge hearts={stats.hearts} />
    </div>
  );
}
