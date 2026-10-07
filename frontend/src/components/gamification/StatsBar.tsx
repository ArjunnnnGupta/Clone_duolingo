"use client";

import { useState } from "react";
import { Dropdown } from "@/components/ui/Dropdown";
import { Skeleton } from "@/components/ui/Skeleton";
import { useMe } from "@/lib/queries";
import { CourseFlag } from "./CourseFlag";
import { GemsBadge } from "./GemsBadge";
import { HeartsBadge } from "./HeartsBadge";
import { HeartsPanel } from "./HeartsPanel";
import { StreakBadge } from "./StreakBadge";
import { StreakPanel } from "./StreakPanel";
import { XpPill } from "./XpPill";

type OpenPanel = "hearts" | "streak" | null;

// Every number is rendered exactly as the server sent it.
export function StatsBar() {
  const { data: me, isError, dataUpdatedAt } = useMe();
  const [openPanel, setOpenPanel] = useState<OpenPanel>(null);

  if (isError) {
    return <p className="text-sm text-text-muted">Could not load your stats.</p>;
  }
  if (!me) {
    return <Skeleton className="h-8 w-full" />;
  }

  const { stats } = me;
  const toggle = (panel: Exclude<OpenPanel, null>) =>
    setOpenPanel((current) => (current === panel ? null : panel));

  return (
    <div className="relative w-full">
      {/* z-50 keeps the badges above the Dropdown's click-away layer so they still toggle. */}
      <div className="relative z-50 flex items-center justify-between gap-1">
        <CourseFlag />
        <StreakBadge
          days={stats.current_streak}
          isActiveToday={stats.streak_active_today}
          isOpen={openPanel === "streak"}
          onClick={() => toggle("streak")}
        />
        <XpPill totalXp={stats.total_xp} />
        <GemsBadge gems={stats.gems} />
        <HeartsBadge
          hearts={stats.hearts}
          isOpen={openPanel === "hearts"}
          onClick={() => toggle("hearts")}
        />
      </div>
      <Dropdown isOpen={openPanel === "hearts"} onClose={() => setOpenPanel(null)}>
        <HeartsPanel stats={stats} receivedAt={dataUpdatedAt} />
      </Dropdown>
      <Dropdown isOpen={openPanel === "streak"} onClose={() => setOpenPanel(null)}>
        <StreakPanel stats={stats} days={me.recent_days} />
      </Dropdown>
    </div>
  );
}
