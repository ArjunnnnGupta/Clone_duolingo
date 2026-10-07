import type { LessonExercise } from "@/lib/types";
import { EXERCISE_COMPONENTS } from "./exercises/registry";
import type { ExerciseProps } from "./exercises/types";

export function ExerciseRenderer(props: ExerciseProps<LessonExercise>) {
  const Component = EXERCISE_COMPONENTS[props.exercise.type];
  return <Component {...props} />;
}
