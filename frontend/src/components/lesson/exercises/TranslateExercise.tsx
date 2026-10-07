"use client";

import { useState } from "react";
import type { TranslateExercise as TranslateData } from "@/lib/types";
import { ExercisePrompt } from "./ExercisePrompt";
import { PromptBubble } from "./PromptBubble";
import { WordTile } from "./WordTile";
import type { ExerciseProps } from "./types";

// The answer line takes the verdict's colour once the answer is checked.
const VERDICT_LINE_CLASSES = { none: "border-border", correct: "border-green", wrong: "border-red" };

export function TranslateExercise({
  exercise,
  isLocked,
  verdict,
  onAnswerChange,
}: ExerciseProps<TranslateData>) {
  const [placedIds, setPlacedIds] = useState<string[]>([]);
  const { source_text: sourceText, tiles } = exercise.payload;
  const tileById = new Map(tiles.map((tile) => [tile.id, tile]));

  function updatePlaced(nextPlacedIds: string[]) {
    setPlacedIds(nextPlacedIds);
    const texts = nextPlacedIds.map((id) => tileById.get(id)?.text ?? "");
    onAnswerChange(texts.length > 0 ? { tiles: texts } : null);
  }

  return (
    <>
      <ExercisePrompt>{exercise.prompt}</ExercisePrompt>
      <PromptBubble text={sourceText} />
      <div className={`flex min-h-[72px] flex-wrap gap-2 border-y-2 py-3 ${VERDICT_LINE_CLASSES[verdict ?? "none"]}`}>
        {placedIds.map((id) => (
          <WordTile
            key={id}
            tileId={id}
            text={tileById.get(id)?.text ?? ""}
            isDisabled={isLocked}
            onClick={() => updatePlaced(placedIds.filter((placedId) => placedId !== id))}
          />
        ))}
      </div>
      <div className="mt-6 flex flex-wrap justify-center gap-2">
        {tiles.map((tile) =>
          placedIds.includes(tile.id) ? (
            // Grey slot the same size as the tile, so the bank does not reflow while it is placed.
            <span
              key={tile.id}
              aria-hidden="true"
              className="rounded-2xl border-2 border-b-4 border-transparent bg-border px-4 py-3 text-[17px] font-bold text-transparent"
            >
              {tile.text}
            </span>
          ) : (
            <WordTile
              key={tile.id}
              tileId={tile.id}
              text={tile.text}
              isDisabled={isLocked}
              onClick={() => updatePlaced([...placedIds, tile.id])}
            />
          ),
        )}
      </div>
    </>
  );
}
