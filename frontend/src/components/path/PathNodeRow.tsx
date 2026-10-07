"use client";

import { useEffect, useRef, useState } from "react";
import { MascotFlourish } from "@/components/mascot/MascotFlourish";
import { getNodeOffset } from "@/lib/pathLayout";
import { getUnitColorClasses } from "@/lib/unitColors";
import type { PathSkill } from "@/lib/types";
import { LockedTooltip } from "./LockedTooltip";
import { NodePopover } from "./NodePopover";
import { SkillNode } from "./SkillNode";
import { StartBubble } from "./StartBubble";

// The mascot sits beside every 4th node, on the side the path has swung away from.
const FLOURISH_EVERY = 4;

interface PathNodeRowProps {
  skill: PathSkill;
  unitColor: string;
  nodeIndex: number;
  isSelected: boolean;
  onToggle: (skillId: number) => void;
}

export function PathNodeRow({ skill, unitColor, nodeIndex, isSelected, onToggle }: PathNodeRowProps) {
  const rowRef = useRef<HTMLDivElement>(null);
  const [shakeCount, setShakeCount] = useState(0);
  const offset = getNodeOffset(nodeIndex);
  const isActive = skill.state === "active";
  const isLocked = skill.state === "locked";
  const hasFlourish = nodeIndex % FLOURISH_EVERY === FLOURISH_EVERY - 1;

  useEffect(() => {
    if (isActive) {
      rowRef.current?.scrollIntoView({ block: "center" });
    }
  }, [isActive]);

  function handleNodeClick() {
    if (isLocked) {
      setShakeCount((count) => count + 1);
    }
    onToggle(skill.id);
  }

  // mt-12 reserves room for the START bubble that floats above the active node.
  return (
    <div ref={rowRef} className={`relative flex flex-col items-center ${isActive ? "mt-12" : ""}`}>
      {/* Click-away layer (z-40) covers the sticky banners and mobile bars so any outside tap closes. */}
      {isSelected && (
        <button
          aria-hidden="true"
          tabIndex={-1}
          className="fixed inset-0 z-40 cursor-default"
          onClick={() => onToggle(skill.id)}
        />
      )}
      <div className="relative" style={{ transform: `translateX(${offset}px)` }}>
        {isActive && !isSelected && (
          <StartBubble textClassName={getUnitColorClasses(unitColor).text} />
        )}
        <SkillNode
          skill={skill}
          unitColor={unitColor}
          shakeCount={shakeCount}
          onClick={handleNodeClick}
        />
      </div>
      {isSelected &&
        (isLocked ? (
          <LockedTooltip skill={skill} tailOffset={offset} />
        ) : (
          <NodePopover skill={skill} unitColor={unitColor} tailOffset={offset} />
        ))}
      {hasFlourish && <MascotFlourish side={offset > 0 ? "left" : "right"} />}
    </div>
  );
}
