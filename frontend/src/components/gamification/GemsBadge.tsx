import { Icon } from "@/components/ui/Icon";

export function GemsBadge({ gems }: { gems: number }) {
  return (
    <span className="flex items-center gap-1.5 font-extrabold text-blue" title="Gems">
      <Icon name="gem" className="h-7 w-7" />
      {gems.toLocaleString()}
    </span>
  );
}
