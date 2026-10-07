"use client";

import { LeaderboardRow } from "@/components/leaderboard/LeaderboardRow";
import { LeagueHeader } from "@/components/leaderboard/LeagueHeader";
import { Skeleton } from "@/components/ui/Skeleton";
import { useLeaderboard } from "@/lib/queries";

export default function LeaderboardPage() {
  const { data: board, isError, error } = useLeaderboard();

  if (isError) {
    return <p className="mt-10 text-center text-text-muted">Could not load the leaderboard: {error.message}</p>;
  }
  if (!board) {
    return (
      <div className="flex flex-col gap-3 pt-6">
        <Skeleton className="h-20 w-full" />
        <Skeleton className="h-64 w-full" />
      </div>
    );
  }
  return (
    <div className="pb-10 pt-6">
      <LeagueHeader periodStart={board.period_start} periodEnd={board.period_end} />
      <ol className="flex flex-col gap-1">
        {board.entries.map((entry) => (
          <LeaderboardRow key={entry.user_id} entry={entry} />
        ))}
      </ol>
    </div>
  );
}
