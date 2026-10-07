"use client";

import { useEffect, useState } from "react";
import type { PathUnit } from "@/lib/types";
import { PathNodeRow } from "./PathNodeRow";
import { UnitHeader } from "./UnitHeader";

export function PathColumn({ units }: { units: PathUnit[] }) {
  const [selectedSkillId, setSelectedSkillId] = useState<number | null>(null);

  useEffect(() => {
    if (selectedSkillId === null) {
      return;
    }
    function closeOnEscape(event: KeyboardEvent) {
      if (event.key === "Escape") {
        setSelectedSkillId(null);
      }
    }
    window.addEventListener("keydown", closeOnEscape);
    return () => window.removeEventListener("keydown", closeOnEscape);
  }, [selectedSkillId]);

  // Zig-zag continues across units, so each unit starts at the global index of its first skill.
  const firstNodeIndexes: number[] = [];
  let nodesSoFar = 0;
  for (const unit of units) {
    firstNodeIndexes.push(nodesSoFar);
    nodesSoFar += unit.skills.length;
  }

  function toggleSkill(skillId: number) {
    setSelectedSkillId((current) => (current === skillId ? null : skillId));
  }

  return (
    <div className="flex flex-col gap-14 pb-40 pt-4">
      {units.map((unit, unitIndex) => (
        <section key={unit.id} className="flex flex-col gap-5">
          <UnitHeader unit={unit} />
          {unit.skills.map((skill, skillIndex) => (
            <PathNodeRow
              key={skill.id}
              skill={skill}
              unitColor={unit.color}
              nodeIndex={firstNodeIndexes[unitIndex] + skillIndex}
              isSelected={selectedSkillId === skill.id}
              onToggle={toggleSkill}
            />
          ))}
        </section>
      ))}
    </div>
  );
}
