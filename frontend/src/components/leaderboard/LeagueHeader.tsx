import { formatMonthDay } from "@/lib/dates";

export function LeagueHeader({ periodStart, periodEnd }: { periodStart: string; periodEnd: string }) {
  return (
    <header className="mb-6 border-b-2 border-border pb-6 text-center">
      <h1 className="text-3xl font-extrabold">Weekly leaderboard</h1>
      <p className="mt-1 text-[17px] text-text-muted">
        {formatMonthDay(periodStart)} – {formatMonthDay(periodEnd)}
      </p>
    </header>
  );
}
