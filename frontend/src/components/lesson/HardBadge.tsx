import { Icon } from "@/components/ui/Icon";

export function HardBadge() {
  return (
    <p className="mb-2 flex items-center gap-2 text-sm font-extrabold uppercase tracking-[0.8px] text-red">
      <Icon name="bolt" className="h-5 w-5" />
      Hard exercise
    </p>
  );
}
