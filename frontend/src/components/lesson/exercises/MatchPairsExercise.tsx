"use client";

import { useEffect, useState } from "react";
import type { MatchItem, MatchPairsExercise as MatchPairsData } from "@/lib/types";
import { ExercisePrompt } from "./ExercisePrompt";
import { OptionCard } from "./OptionCard";
import type { ExerciseProps } from "./types";

const MISMATCH_FLASH_MS = 400;

type Side = "left" | "right";

// Taps are validated here because each item carries its partner's pair key. A wrong tap only
// flashes red and is counted; the server never charges a heart for this exercise type.
export function MatchPairsExercise({
  exercise,
  isLocked,
  onAnswerChange,
}: ExerciseProps<MatchPairsData>) {
  const { left, right } = exercise.payload;
  const [selected, setSelected] = useState<Partial<Record<Side, MatchItem>>>({});
  const [matchedPairs, setMatchedPairs] = useState<[string, string][]>([]);
  const [mismatches, setMismatches] = useState(0);
  const [flashedIds, setFlashedIds] = useState<string[]>([]);

  useEffect(() => {
    if (flashedIds.length === 0) {
      return;
    }
    const timer = setTimeout(() => setFlashedIds([]), MISMATCH_FLASH_MS);
    return () => clearTimeout(timer);
  }, [flashedIds]);

  function tap(side: Side, item: MatchItem) {
    const nextSelected = { ...selected, [side]: item };
    const { left: leftItem, right: rightItem } = nextSelected;
    if (!leftItem || !rightItem) {
      setSelected(nextSelected);
      return;
    }
    setSelected({});
    if (leftItem.pair === rightItem.pair) {
      const nextPairs: [string, string][] = [...matchedPairs, [leftItem.id, rightItem.id]];
      setMatchedPairs(nextPairs);
      if (nextPairs.length === left.length) {
        onAnswerChange({ pairs: nextPairs, mismatches });
      }
    } else {
      setMismatches((count) => count + 1);
      setFlashedIds([leftItem.id, rightItem.id]);
    }
  }

  function stateOf(item: MatchItem, side: Side) {
    if (matchedPairs.some((pair) => pair.includes(item.id))) return "matched";
    if (flashedIds.includes(item.id)) return "wrong";
    return selected[side]?.id === item.id ? "selected" : "default";
  }

  function renderColumn(items: MatchItem[], side: Side) {
    return (
      <div className="flex flex-1 flex-col gap-3">
        {items.map((item) => (
          <OptionCard
            key={item.id}
            state={stateOf(item, side)}
            isDisabled={isLocked}
            onClick={() => tap(side, item)}
          >
            {item.text}
          </OptionCard>
        ))}
      </div>
    );
  }

  return (
    <>
      <ExercisePrompt>{exercise.prompt}</ExercisePrompt>
      <div className="flex gap-4">
        {renderColumn(left, "left")}
        {renderColumn(right, "right")}
      </div>
    </>
  );
}
