import type { ExerciseAnswer, LessonExercise } from "@/lib/types";

// Every exercise component keeps its own selection state and reports a serializable answer
// (or null while the learner has nothing to check yet).
export interface ExerciseProps<E extends LessonExercise = LessonExercise> {
  exercise: E;
  isLocked: boolean;
  onAnswerChange: (answer: ExerciseAnswer | null) => void;
}
