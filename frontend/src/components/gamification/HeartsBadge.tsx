import { Icon } from "@/components/ui/Icon";

interface HeartsBadgeProps {
  hearts: number;
  isOpen: boolean;
  onClick: () => void;
}

export function HeartsBadge({ hearts, isOpen, onClick }: HeartsBadgeProps) {
  return (
    <button
      onClick={onClick}
      className={`flex items-center gap-1.5 rounded-xl px-2 py-1 font-extrabold text-red hover:bg-surface-subtle ${isOpen ? "bg-surface-subtle" : ""}`}
      title="Hearts"
    >
      <Icon name="heart" className="h-7 w-7" />
      {hearts}
    </button>
  );
}
