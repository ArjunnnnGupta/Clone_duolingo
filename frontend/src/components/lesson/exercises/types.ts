import type { ExerciseAnswer, LessonExercise } from "@/lib/types";

export type Verdict = "correct" | "wrong";

// Every exercise component keeps its own selection state and reports a serializable answer
// (or null while the learner has nothing to check yet).
export interface ExerciseProps<E extends LessonExercise = LessonExercise> {
  exercise: E;
  isLocked: boolean;
  // Set while the feedback footer is up, so the exercise can colour the learner's answer.
  verdict: Verdict | null;
  onAnswerChange: (answer: ExerciseAnswer | null) => void;
}
