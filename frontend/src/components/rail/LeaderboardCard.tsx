"use client";

import Link from "next/link";
import { Card } from "@/components/ui/Card";
import { Skeleton } from "@/components/ui/Skeleton";
import { useLeaderboard } from "@/lib/queries";

// Rank and weekly XP come from the leaderboard's own "is me" entry.
export function LeaderboardCard() {
  const { data: board } = useLeaderboard();
  if (!board) {
    return <Skeleton className="h-32 w-full" />;
  }
  const me = board.entries.find((entry) => entry.is_me);
  if (!me) {
    return null;
  }

  return (
    <Card>
      <div className="mb-3 flex items-center justify-between">
        <h2 className="text-xl font-extrabold">Weekly leaderboard</h2>
        <Link href="/leaderboard" className="text-sm font-extrabold uppercase tracking-[0.8px] text-blue">
          View
        </Link>
      </div>
      <p className="text-[17px] font-extrabold">
        You&apos;re ranked <span className="text-green">#{me.rank}</span>
      </p>
      <p className="text-text-muted">You&apos;ve earned {me.xp} XP this week</p>
    </Card>
  );
}
