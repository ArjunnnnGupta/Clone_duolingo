import type { ComponentType } from "react";
import type { ExerciseType, LessonExercise } from "@/lib/types";
import { FillBlankExercise } from "./FillBlankExercise";
import { MatchPairsExercise } from "./MatchPairsExercise";
import { MultipleChoiceExercise } from "./MultipleChoiceExercise";
import { TranslateExercise } from "./TranslateExercise";
import { TypeAnswerExercise } from "./TypeAnswerExercise";
import type { ExerciseProps } from "./types";

interface RegistryEntry<E extends LessonExercise> {
  component: ComponentType<ExerciseProps<E>>;
  // True when the exercise has no CHECK button: it submits as soon as the answer is complete.
  isSubmittedOnComplete: boolean;
}

// The only place that knows which component renders which exercise type. Adding a sixth type
// is one entry here (plus its payload type, component and the backend grader).
export const EXERCISE_REGISTRY: { [T in ExerciseType]: RegistryEntry<Extract<LessonExercise, { type: T }>> } = {
  multiple_choice: { component: MultipleChoiceExercise, isSubmittedOnComplete: false },
  translate: { component: TranslateExercise, isSubmittedOnComplete: false },
  match_pairs: { component: MatchPairsExercise, isSubmittedOnComplete: true },
  fill_blank: { component: FillBlankExercise, isSubmittedOnComplete: false },
  type_answer: { component: TypeAnswerExercise, isSubmittedOnComplete: false },
};

// TypeScript cannot correlate "this exercise's type" with "that type's component" across a
// lookup, so the widening cast lives here once; the registry's own typing keeps entries honest.
// Safe only when indexed by the type of the very exercise being rendered, which is the one
// thing ExerciseRenderer does. Do not look up a component and pass it a different exercise.
export const EXERCISE_COMPONENTS = Object.fromEntries(
  Object.entries(EXERCISE_REGISTRY).map(([type, entry]) => [type, entry.component]),
) as unknown as Record<ExerciseType, ComponentType<ExerciseProps>>;
