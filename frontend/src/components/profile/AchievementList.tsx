import type { AchievementOut } from "@/lib/types";
import { AchievementCard } from "./AchievementCard";

export function AchievementList({ achievements }: { achievements: AchievementOut[] }) {
  // Earned first, then the rest; each group keeps the server's order.
  const unlocked = achievements.filter((achievement) => achievement.unlocked_at !== null);
  const locked = achievements.filter((achievement) => achievement.unlocked_at === null);
  const sorted = [...unlocked, ...locked];
  return (
    <ul className="flex flex-col gap-3">
      {sorted.map((achievement) => (
        <AchievementCard key={achievement.code} achievement={achievement} />
      ))}
    </ul>
  );
}
