import { StatsBar } from "@/components/gamification/StatsBar";

// Desktop only. Phase 8 adds the daily-quest and league cards below the stats.
export function RightRail() {
  return (
    <aside className="sticky top-0 hidden h-screen w-[368px] shrink-0 px-6 py-5 lg:block">
      <StatsBar />
    </aside>
  );
}
