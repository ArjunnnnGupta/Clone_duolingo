import { Icon } from "@/components/ui/Icon";

interface StreakBadgeProps {
  days: number;
  isActiveToday: boolean;
}

export function StreakBadge({ days, isActiveToday }: StreakBadgeProps) {
  const colorClass = isActiveToday ? "text-orange" : "text-text-subtle";
  return (
    <span className={`flex items-center gap-1.5 font-extrabold ${colorClass}`} title="Day streak">
      <Icon name="flame" className="h-7 w-7" />
      {days}
    </span>
  );
}
