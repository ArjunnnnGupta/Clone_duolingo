import { StatsBar } from "@/components/gamification/StatsBar";

// Stands in for the right rail wherever the rail is hidden (below 1024px).
// Its h-14 is the sticky offset UnitHeader uses (top-14); change both together.
export function MobileTopBar() {
  return (
    <header className="sticky top-0 z-30 flex h-14 items-center bg-surface lg:hidden">
      <StatsBar />
    </header>
  );
}
