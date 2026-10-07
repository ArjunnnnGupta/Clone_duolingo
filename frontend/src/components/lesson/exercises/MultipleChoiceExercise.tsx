"use client";

import { useState } from "react";
import type { MultipleChoiceExercise as MultipleChoiceData } from "@/lib/types";
import { ExercisePrompt } from "./ExercisePrompt";
import { OptionCard } from "./OptionCard";
import { useNumberKeys } from "./useNumberKeys";
import type { ExerciseProps } from "./types";

export function MultipleChoiceExercise({
  exercise,
  isLocked,
  onAnswerChange,
}: ExerciseProps<MultipleChoiceData>) {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const { options } = exercise.payload;

  function select(optionId: string) {
    setSelectedId(optionId);
    onAnswerChange({ option_id: optionId });
  }

  useNumberKeys(options.length, isLocked, (index) => select(options[index].id));

  return (
    <>
      <ExercisePrompt>{exercise.prompt}</ExercisePrompt>
      <div className="flex flex-col gap-3">
        {options.map((option, index) => (
          <OptionCard
            key={option.id}
            keyHint={String(index + 1)}
            state={selectedId === option.id ? "selected" : "default"}
            isDisabled={isLocked}
            onClick={() => select(option.id)}
          >
            {option.emoji && <span className="text-3xl">{option.emoji}</span>}
            {option.text}
          </OptionCard>
        ))}
      </div>
    </>
  );
}
