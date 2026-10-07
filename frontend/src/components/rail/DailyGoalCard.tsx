"use client";

import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Icon } from "@/components/ui/Icon";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { Skeleton } from "@/components/ui/Skeleton";
import { useMe } from "@/lib/queries";

// Today's XP and the goal are the server's; the bar is just their ratio, drawn.
export function DailyGoalCard() {
  const { data: me } = useMe();
  if (!me) {
    return <Skeleton className="h-36 w-full" />;
  }
  const { goal_xp: goalXp, today_xp: todayXp } = me.daily;

  return (
    <Card>
      <div className="mb-4 flex items-center justify-between">
        <h2 className="text-xl font-extrabold">Daily goal</h2>
        <Link href="/settings" className="text-sm font-extrabold uppercase tracking-[0.8px] text-blue">
          Edit goal
        </Link>
      </div>
      <div className="flex items-center gap-4">
        <Icon name="bolt" className="h-10 w-10 shrink-0 text-gold" />
        <div className="flex-1">
          <p className="mb-2 text-[17px] font-extrabold">Earn {goalXp} XP</p>
          <ProgressBar fraction={goalXp > 0 ? Math.min(todayXp / goalXp, 1) : 0} fillClassName="bg-gold" />
          <p className="mt-1 text-sm font-extrabold text-text-muted">
            {todayXp} / {goalXp}
          </p>
        </div>
      </div>
    </Card>
  );
}
