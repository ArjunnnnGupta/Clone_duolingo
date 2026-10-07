import { Button } from "@/components/ui/Button";
import type { PathSkill } from "@/lib/types";
import { PopoverCard } from "./PopoverCard";

export function LockedTooltip({ skill, tailOffset }: { skill: PathSkill; tailOffset: number }) {
  return (
    <PopoverCard
      cardClassName="border-2 border-border bg-surface"
      tailClassName="border-l-2 border-t-2 border-border bg-surface"
      tailOffset={tailOffset}
    >
      <p className="text-[17px] font-extrabold text-text-subtle">{skill.title}</p>
      <p className="mt-1 mb-4 text-[15px] text-text-subtle">
        Complete all levels above to unlock this!
      </p>
      <Button variant="locked" disabled>
        Locked
      </Button>
    </PopoverCard>
  );
}
