import type { LessonExercise } from "@/lib/types";
import { EXERCISE_COMPONENTS, isHardExercise } from "./exercises/registry";
import type { ExerciseProps } from "./exercises/types";
import { HardBadge } from "./HardBadge";

export function ExerciseRenderer(props: ExerciseProps<LessonExercise>) {
  const Component = EXERCISE_COMPONENTS[props.exercise.type];
  return (
    <>
      {isHardExercise(props.exercise) && <HardBadge />}
      <Component {...props} />
    </>
  );
}
