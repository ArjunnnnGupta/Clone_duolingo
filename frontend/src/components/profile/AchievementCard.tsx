import { Icon, toIconName } from "@/components/ui/Icon";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { formatMonthDay } from "@/lib/dates";
import type { AchievementOut } from "@/lib/types";

// Unlocked state, date and progress all come from the server; locked ones show how far along.
export function AchievementCard({ achievement }: { achievement: AchievementOut }) {
  const unlockedAt = achievement.unlocked_at;
  const isUnlocked = unlockedAt !== null;

  return (
    <li
      className={`flex items-center gap-4 rounded-2xl border-2 px-4 py-3 ${
        isUnlocked ? "border-gold" : "border-border"
      }`}
    >
      <span
        className={`flex h-14 w-14 shrink-0 items-center justify-center rounded-2xl ${
          isUnlocked ? "bg-gold text-surface" : "bg-border text-text-subtle"
        }`}
      >
        <Icon name={toIconName(achievement.icon)} className="h-8 w-8" />
      </span>
      <div className="min-w-0 flex-1">
        <p className="text-[17px] font-extrabold">{achievement.title}</p>
        <p className="text-text-muted">{achievement.description}</p>
        {unlockedAt !== null ? (
          <p className="text-sm font-extrabold text-gold-shade">
            Unlocked {formatMonthDay(unlockedAt.slice(0, 10))}
          </p>
        ) : (
          <div className="mt-2 flex items-center gap-3">
            <ProgressBar
              fraction={achievement.progress / achievement.threshold}
              fillClassName="bg-gold"
            />
            <span className="shrink-0 text-sm font-extrabold text-text-muted">
              {achievement.progress} / {achievement.threshold}
            </span>
          </div>
        )}
      </div>
    </li>
  );
}
