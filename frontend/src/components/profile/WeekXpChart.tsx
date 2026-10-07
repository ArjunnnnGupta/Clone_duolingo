import { weekdayInitial } from "@/lib/dates";
import type { DayXp } from "@/lib/types";

const CHART_HEIGHT_CLASS = "h-36";

// One thin bar per day. Heights are each day's XP as a share of the week's best day (a drawing
// ratio); the numbers themselves are the server's. Values show on hover; a hidden table repeats
// them for screen readers, so the bars themselves are not focusable.
export function WeekXpChart({ days }: { days: DayXp[] }) {
  const maxXp = Math.max(...days.map((day) => day.xp), 1);

  return (
    <div>
      <ol className={`flex items-end gap-2 border-b-2 border-border ${CHART_HEIGHT_CLASS}`}>
        {days.map((day, index) => {
          const isToday = index === days.length - 1;
          return (
            <li
              key={day.date}
              className="group relative flex h-full flex-1 flex-col items-center justify-end"
            >
              <span
                className={`mb-1 rounded-lg bg-text px-2 py-0.5 text-sm font-extrabold text-surface ${
                  isToday ? "" : "opacity-0 group-hover:opacity-100"
                }`}
              >
                {day.xp}
              </span>
              <span
                className={`w-full max-w-8 rounded-t-[4px] ${isToday ? "bg-gold" : "bg-gold/60"}`}
                style={{ height: `${Math.max((day.xp / maxXp) * 100, day.xp > 0 ? 4 : 1)}%` }}
              />
            </li>
          );
        })}
      </ol>
      <ol className="mt-2 flex gap-2">
        {days.map((day, index) => (
          <li
            key={day.date}
            className={`flex-1 text-center text-sm font-extrabold ${
              index === days.length - 1 ? "text-gold-shade" : "text-text-subtle"
            }`}
          >
            {weekdayInitial(day.date)}
          </li>
        ))}
      </ol>
      <table className="sr-only">
        <caption>XP earned in the last 7 days</caption>
        <tbody>
          {days.map((day) => (
            <tr key={day.date}>
              <th scope="row">{day.date}</th>
              <td>{day.xp} XP</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
