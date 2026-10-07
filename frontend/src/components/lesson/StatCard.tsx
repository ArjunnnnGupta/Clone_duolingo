import { Icon, type IconName } from "@/components/ui/Icon";

const TONE_CLASSES = {
  gold: { header: "bg-gold", border: "border-gold", text: "text-gold-shade" },
  green: { header: "bg-green", border: "border-green", text: "text-green" },
} as const;

interface StatCardProps {
  tone: keyof typeof TONE_CLASSES;
  label: string;
  value: string;
  icon: IconName;
}

export function StatCard({ tone, label, value, icon }: StatCardProps) {
  const classes = TONE_CLASSES[tone];
  return (
    <div className={`w-36 overflow-hidden rounded-2xl border-2 ${classes.border}`}>
      <p className={`py-1 text-center text-xs font-extrabold uppercase text-surface ${classes.header}`}>
        {label}
      </p>
      <p className={`flex items-center justify-center gap-2 py-4 text-2xl font-extrabold ${classes.text}`}>
        <Icon name={icon} className="h-6 w-6" />
        {value}
      </p>
    </div>
  );
}
