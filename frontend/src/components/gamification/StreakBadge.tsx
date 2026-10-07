import { Icon } from "@/components/ui/Icon";

interface StreakBadgeProps {
  days: number;
  isActiveToday: boolean;
  isOpen: boolean;
  onClick: () => void;
}

export function StreakBadge({ days, isActiveToday, isOpen, onClick }: StreakBadgeProps) {
  const colorClass = isActiveToday ? "text-orange" : "text-text-subtle";
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-1.5 rounded-xl px-2 py-1 font-extrabold hover:bg-surface-subtle ${isOpen ? "bg-surface-subtle" : ""} ${colorClass}`}
      title="Day streak"
    >
      <Icon name="flame" className="h-7 w-7" />
      {days}
    </button>
  );
}
