import { Icon } from "@/components/ui/Icon";

export function HeartsBadge({ hearts }: { hearts: number }) {
  return (
    <span className="flex items-center gap-1.5 font-extrabold text-red" title="Hearts">
      <Icon name="heart" className="h-7 w-7" />
      {hearts}
    </span>
  );
}
