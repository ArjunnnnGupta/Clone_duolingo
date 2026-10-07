import { Icon, type IconName } from "@/components/ui/Icon";

interface StatTileProps {
  icon: IconName;
  iconClassName: string;
  value: string;
  label: string;
}

export function StatTile({ icon, iconClassName, value, label }: StatTileProps) {
  return (
    <div className="flex items-center gap-3 rounded-2xl border-2 border-border px-4 py-3">
      <Icon name={icon} className={`h-8 w-8 shrink-0 ${iconClassName}`} />
      <div>
        <p className="text-xl font-extrabold">{value}</p>
        <p className="text-text-muted">{label}</p>
      </div>
    </div>
  );
}
