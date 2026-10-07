import { Icon } from "@/components/ui/Icon";

export function XpPill({ totalXp }: { totalXp: number }) {
  return (
    <span className="flex items-center gap-1.5 font-extrabold text-gold-shade" title="Total XP">
      <Icon name="bolt" className="h-7 w-7 text-gold" />
      {totalXp.toLocaleString()}
    </span>
  );
}
