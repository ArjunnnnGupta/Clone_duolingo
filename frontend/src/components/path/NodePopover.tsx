"use client";

import { useState } from "react";
import { OutOfHeartsModal } from "@/components/lesson/OutOfHeartsModal";
import { Button } from "@/components/ui/Button";
import { ApiError } from "@/lib/api";
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
  const [isOutOfHeartsOpen, setIsOutOfHeartsOpen] = useState(false);

  function start() {
    startLesson.mutate(skill.id, {
      // The server refuses to start a lesson at 0 hearts; offer the refill instead of an error.
      onError: (error) => {
        if (error instanceof ApiError && error.code === "NO_HEARTS") {
          setIsOutOfHeartsOpen(true);
        }
      },
    });
  }

  // Progress is shown exactly as the server reports it; which lesson starts next is the
  // server's decision (a completed skill starts a practice lesson).
  const subtitle = isCompleted
    ? "Practice to keep this skill sharp"
    : `${skill.lessons_completed} of ${skill.lesson_count} lessons complete`;

  return (
    <PopoverCard cardClassName={colors.fill} tailClassName={colors.fill} tailOffset={tailOffset}>
      <p className="text-[17px] font-extrabold text-on-color">{skill.title}</p>
      <p className="mt-1 mb-4 text-[15px] text-on-color/80">{subtitle}</p>
      <Button
        variant="white"
        className={colors.text}
        // Stays disabled after success too: a second tap before navigation would open another attempt.
        disabled={startLesson.isPending || startLesson.isSuccess}
        onClick={start}
      >
        {isCompleted ? "Practice" : "Start"}
      </Button>
      {startLesson.isError && !isOutOfHeartsOpen && (
        <p className="mt-3 text-center text-sm text-on-color">{startLesson.error.message}</p>
      )}
      <OutOfHeartsModal
        isOpen={isOutOfHeartsOpen}
        onRefilled={() => {
          setIsOutOfHeartsOpen(false);
          start();
        }}
        onDecline={() => setIsOutOfHeartsOpen(false)}
        isDismissible
      />
    </PopoverCard>
  );
}
