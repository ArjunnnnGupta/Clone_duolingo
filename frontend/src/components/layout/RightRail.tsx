import { StatsBar } from "@/components/gamification/StatsBar";
import { DailyGoalCard } from "@/components/rail/DailyGoalCard";
import { LeaderboardCard } from "@/components/rail/LeaderboardCard";

// Desktop only (below 1024px the stats move to the top bar and the cards are not shown).
export function RightRail() {
  return (
    <aside className="sticky top-0 hidden h-screen w-[368px] shrink-0 flex-col gap-4 px-6 py-5 lg:flex">
      <StatsBar />
      <LeaderboardCard />
      <DailyGoalCard />
    </aside>
  );
}
