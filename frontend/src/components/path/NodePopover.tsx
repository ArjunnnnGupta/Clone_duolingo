"use client";

import { Button } from "@/components/ui/Button";
import { useStartLesson } from "@/lib/queries";
import { getUnitColorClasses } from "@/lib/unitColors";
import type { PathSkill } from "@/lib/types";
import { PopoverCard } from "./PopoverCard";

interface NodePopoverProps {
  skill: PathSkill;
  unitColor: string;
  tailOffset: number;
}

export function NodePopover({ skill, unitColor, tailOffset }: NodePopoverProps) {
  const colors = getUnitColorClasses(unitColor);
  const startLesson = useStartLesson();
  const isCompleted = skill.state === "completed";

  // Progress is shown exactly as the server reports it; which lesson starts next is the
  // server's decision (a completed skill starts a practice lesson).
  const subtitle = isCompleted
    ? "Practice to keep this skill sharp"
    : `${skill.lessons_completed} of ${skill.lesson_count} lessons complete`;

  return (
    <PopoverCard cardClassName={colors.fill} tailClassName={colors.fill} tailOffset={tailOffset}>
      <p className="text-[17px] font-extrabold text-surface">{skill.title}</p>
      <p className="mt-1 mb-4 text-[15px] text-surface/80">{subtitle}</p>
      <Button
        variant="white"
        className={colors.text}
        // Stays disabled after success too: a second tap before navigation would open another attempt.
        disabled={startLesson.isPending || startLesson.isSuccess}
        onClick={() => startLesson.mutate(skill.id)}
      >
        {isCompleted ? "Practice" : "Start"}
      </Button>
      {startLesson.isError && (
        <p className="mt-3 text-center text-sm text-surface">{startLesson.error.message}</p>
      )}
    </PopoverCard>
  );
}
