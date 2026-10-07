import { Icon } from "@/components/ui/Icon";
import { weekdayInitial } from "@/lib/dates";
import type { DayActivity } from "@/lib/types";

// One circle per day as the server reported it; the last day is today.
export function WeekStrip({ days }: { days: DayActivity[] }) {
  return (
    <ol className="flex justify-between rounded-2xl border-2 border-border bg-surface px-3 py-3">
      {days.map((day, index) => {
        const isToday = index === days.length - 1;
        return (
          <li key={day.date} className="flex flex-col items-center gap-1">
            <span className={`text-sm font-extrabold ${isToday ? "text-orange" : "text-text-subtle"}`}>
              {weekdayInitial(day.date)}
            </span>
            <span
              className={`flex h-8 w-8 items-center justify-center rounded-full ${
                day.is_active ? "bg-orange text-surface" : "bg-border"
              }`}
            >
              {day.is_active && <Icon name="check" className="h-5 w-5" />}
            </span>
          </li>
        );
      })}
    </ol>
  );
}
