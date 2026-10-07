"use client";

import { useState } from "react";
import type { FillBlankExercise as FillBlankData } from "@/lib/types";
import { ExercisePrompt } from "./ExercisePrompt";
import { OptionCard, selectedState } from "./OptionCard";
import { useNumberKeys } from "./useNumberKeys";
import type { ExerciseProps } from "./types";

export function FillBlankExercise({
  exercise,
  isLocked,
  verdict,
  onAnswerChange,
}: ExerciseProps<FillBlankData>) {
  const [selectedWord, setSelectedWord] = useState<string | null>(null);
  const { before, after, options } = exercise.payload;

  function select(word: string) {
    setSelectedWord(word);
    onAnswerChange({ text: word });
  }

  useNumberKeys(options.length, isLocked, (index) => select(options[index]));

  return (
    <>
      <ExercisePrompt>{exercise.prompt}</ExercisePrompt>
      <p className="mb-6 text-xl font-extrabold">
        {before}{" "}
        <span className="inline-block min-w-24 border-b-2 border-border text-center text-blue">
          {selectedWord ?? " "}
        </span>{" "}
        {after}
      </p>
      <div className="flex flex-col gap-3">
        {options.map((word, index) => (
          <OptionCard
            key={word}
            keyHint={String(index + 1)}
            state={selectedWord === word ? selectedState(verdict) : "default"}
            isDisabled={isLocked}
            onClick={() => select(word)}
          >
            {word}
          </OptionCard>
        ))}
      </div>
    </>
  );
}
