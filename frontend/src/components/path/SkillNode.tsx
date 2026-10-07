"use client";

import { motion, useAnimationControls } from "framer-motion";
import { useEffect } from "react";
import { Icon, toIconName } from "@/components/ui/Icon";
import { getUnitColorClasses } from "@/lib/unitColors";
import type { PathSkill } from "@/lib/types";
import { ProgressRing } from "./ProgressRing";

interface SkillNodeProps {
  skill: PathSkill;
  unitColor: string;
  shakeCount: number;
  onClick: () => void;
}

export function SkillNode({ skill, unitColor, shakeCount, onClick }: SkillNodeProps) {
  const colors = getUnitColorClasses(unitColor);
  const controls = useAnimationControls();

  useEffect(() => {
    if (shakeCount > 0) {
      controls.start({ x: [0, -6, 6, -4, 4, 0], transition: { duration: 0.4 } });
    }
  }, [shakeCount, controls]);

  const faceClasses = {
    locked: "bg-border text-text-subtle shadow-node-locked",
    active: `${colors.fill} text-on-color ${colors.nodeShadow}`,
    completed: "bg-gold text-on-color shadow-node-gold",
  }[skill.state];

  return (
    <motion.button
      animate={controls}
      onClick={onClick}
      aria-label={`${skill.title}, ${skill.state}`}
      className="group relative flex h-[100px] w-[100px] items-center justify-center"
    >
      {skill.state === "active" && (
        <ProgressRing
          fraction={skill.lesson_count > 0 ? skill.lessons_completed / skill.lesson_count : 0}
          strokeClassName={colors.stroke}
        />
      )}
      <span
        className={`flex h-[70px] w-[70px] items-center justify-center rounded-full group-active:translate-y-2 group-active:shadow-none ${faceClasses}`}
      >
        {/* Completed skills show a check; the others show their own glyph (dimmed while locked). */}
        <Icon
          name={skill.state === "completed" ? "check" : toIconName(skill.icon)}
          className="h-9 w-9"
        />
      </span>
    </motion.button>
  );
}
