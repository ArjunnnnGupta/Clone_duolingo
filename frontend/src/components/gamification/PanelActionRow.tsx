import { Icon, type IconName } from "@/components/ui/Icon";

interface PanelActionRowProps {
  label: string;
  icon: IconName;
  detail?: string;
  detailIcon?: IconName;
  isBusy: boolean;
  onClick: () => void;
}

export function PanelActionRow({
  label,
  icon,
  detail,
  detailIcon,
  isBusy,
  onClick,
}: PanelActionRowProps) {
  return (
    <button
      disabled={isBusy}
      onClick={onClick}
      className="flex items-center gap-3 rounded-2xl border-2 border-b-4 border-border px-4 py-3 text-left text-[15px] font-extrabold uppercase tracking-[0.8px] hover:bg-surface-subtle active:translate-y-0.5 active:border-b-2 disabled:cursor-wait disabled:opacity-60"
    >
      <Icon name={icon} className="h-6 w-6 text-red" />
      <span className="flex-1">{label}</span>
      {detail && (
        <span className="flex items-center gap-1 text-blue">
          {detailIcon && <Icon name={detailIcon} className="h-5 w-5" />}
          {detail}
        </span>
      )}
    </button>
  );
}
