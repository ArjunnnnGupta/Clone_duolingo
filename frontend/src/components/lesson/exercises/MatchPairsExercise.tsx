"use client";

import { useEffect, useState } from "react";
import type { MatchItem, MatchPairsExercise as MatchPairsData } from "@/lib/types";
import { ExercisePrompt } from "./ExercisePrompt";
import { OptionCard, type OptionCardState } from "./OptionCard";
import { useNumberKeys } from "./useNumberKeys";
import type { ExerciseProps } from "./types";

// A wrong pair flashes red and a right pair flashes green for this long; the right pair then greys out.
const FLASH_MS = 400;

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
  const [flash, setFlash] = useState<{ ids: string[]; state: "correct" | "wrong" } | null>(null);

  useEffect(() => {
    if (flash === null) {
      return;
    }
    const timer = setTimeout(() => setFlash(null), FLASH_MS);
    return () => clearTimeout(timer);
  }, [flash]);

  function tap(side: Side, item: MatchItem) {
    const nextSelected = { ...selected, [side]: item };
    const { left: leftItem, right: rightItem } = nextSelected;
    if (!leftItem || !rightItem) {
      setSelected(nextSelected);
      return;
    }
    setSelected({});
    const ids = [leftItem.id, rightItem.id];
    if (leftItem.pair !== rightItem.pair) {
      setMismatches((count) => count + 1);
      setFlash({ ids, state: "wrong" });
      return;
    }
    const nextPairs: [string, string][] = [...matchedPairs, [leftItem.id, rightItem.id]];
    setMatchedPairs(nextPairs);
    setFlash({ ids, state: "correct" });
    if (nextPairs.length === left.length) {
      onAnswerChange({ pairs: nextPairs, mismatches });
    }
  }

  // Keys follow the badges: left column 1..n, right column continues (…9, 0).
  const columns: [Side, MatchItem[]][] = [["left", left], ["right", right]];
  const keyed = columns.flatMap(([side, items]) => items.map((item) => ({ side, item })));
  const keys = keyed.map((_, index) => String((index + 1) % 10));
  useNumberKeys(keyed.length, isLocked, (index) => tap(keyed[index].side, keyed[index].item), keys);

  function stateOf(item: MatchItem, side: Side): OptionCardState {
    if (flash?.ids.includes(item.id)) return flash.state;
    if (matchedPairs.some((pair) => pair.includes(item.id))) return "matched";
    return selected[side]?.id === item.id ? "selected" : "default";
  }

  return (
    <>
      <ExercisePrompt>{exercise.prompt}</ExercisePrompt>
      <div className="flex gap-4">
        {columns.map(([side, items]) => (
          <div key={side} className="flex flex-1 flex-col gap-3">
            {items.map((item) => (
              <OptionCard
                key={item.id}
                state={stateOf(item, side)}
                keyHint={keys[keyed.findIndex((entry) => entry.item.id === item.id)]}
                isDisabled={isLocked}
                onClick={() => tap(side, item)}
              >
                {item.text}
              </OptionCard>
            ))}
          </div>
        ))}
      </div>
    </>
  );
}
