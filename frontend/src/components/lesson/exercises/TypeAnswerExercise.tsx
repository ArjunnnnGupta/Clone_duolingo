"use client";

import { useState } from "react";
import type { TypeAnswerExercise as TypeAnswerData } from "@/lib/types";
import { ExercisePrompt } from "./ExercisePrompt";
import { PromptBubble } from "./PromptBubble";
import type { ExerciseProps } from "./types";

const VERDICT_INPUT_CLASSES = {
  none: "border-border",
  correct: "border-green text-green",
  wrong: "border-red text-red",
};

export function TypeAnswerExercise({
  exercise,
  isLocked,
  verdict,
  onAnswerChange,
}: ExerciseProps<TypeAnswerData>) {
  const [text, setText] = useState("");

  function handleChange(nextText: string) {
    setText(nextText);
    onAnswerChange(nextText.trim() ? { text: nextText } : null);
  }

  return (
    <>
      <ExercisePrompt>{exercise.prompt}</ExercisePrompt>
      <PromptBubble text={exercise.payload.source_text} />
      <input
        autoFocus
        value={text}
        disabled={isLocked}
        onChange={(event) => handleChange(event.target.value)}
        lang={exercise.payload.input_language}
        placeholder="Type your answer"
        autoCapitalize="off"
        autoComplete="off"
        spellCheck={false}
        className={`w-full rounded-2xl border-2 bg-surface-subtle px-4 py-4 ${VERDICT_INPUT_CLASSES[verdict ?? "none"]} text-[17px] font-bold outline-none placeholder:text-text-subtle focus:border-blue`}
      />
    </>
  );
}
