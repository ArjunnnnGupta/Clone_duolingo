import { useReducer, type Dispatch } from "react";
import { ApiError } from "@/lib/api";
import {
  createInitialState,
  enterKeyAction,
  lessonReducer,
  type LessonAction,
} from "@/lib/lessonReducer";
import { useSubmitAnswer } from "@/lib/queries";
import type { AttemptResponse, ExerciseAnswer } from "@/lib/types";
import { EXERCISE_REGISTRY } from "./exercises/registry";
import { useEnterKey } from "./useEnterKey";

// Wires the pure reducer to the answer request and the Enter shortcut.
// Shortcuts pause while something (the quit modal) covers the lesson.
export function useLessonPlayer(attempt: AttemptResponse, areShortcutsPaused: boolean) {
  const [state, dispatch] = useReducer(lessonReducer, attempt, createInitialState);
  const submit = useAnswerSubmission(attempt.attempt_id, dispatch);

  const currentExercise = state.exercises.find((exercise) => exercise.id === state.queue[0]) ?? null;
  const isSubmittedOnComplete =
    currentExercise !== null && EXERCISE_REGISTRY[currentExercise.type].isSubmittedOnComplete;

  function check(answer: ExerciseAnswer) {
    if (currentExercise && state.phase === "answering") {
      submit(currentExercise.id, answer);
    }
  }

  function checkCurrentAnswer() {
    if (state.answer) {
      check(state.answer);
    }
  }

  const continueLesson = () => dispatch({ type: "CONTINUE" });

  function setAnswer(answer: ExerciseAnswer | null) {
    dispatch({ type: "SET_ANSWER", answer });
    if (answer && isSubmittedOnComplete) {
      check(answer);
    }
  }

  useEnterKey(() => {
    const action = enterKeyAction(state, isSubmittedOnComplete);
    if (action === "check") checkCurrentAnswer();
    if (action === "continue") continueLesson();
    return action !== null;
  }, areShortcutsPaused);

  return { state, currentExercise, checkCurrentAnswer, setAnswer, continueLesson };
}

// Sends one answer and turns the response (or error) into reducer actions.
function useAnswerSubmission(attemptId: number, dispatch: Dispatch<LessonAction>) {
  const submitAnswer = useSubmitAnswer(attemptId);

  return (exerciseId: number, answer: ExerciseAnswer) => {
    dispatch({ type: "CHECK_START" });
    submitAnswer.mutate(
      { exerciseId, answer },
      {
        onSuccess: (response) => dispatch({ type: "CHECK_RESULT", response }),
        // Another tab started a lesson, which closed this attempt on the server.
        onError: (error) =>
          error instanceof ApiError && error.code === "ATTEMPT_CLOSED"
            ? dispatch({ type: "LESSON_CLOSED" })
            : dispatch({ type: "CHECK_ERROR", message: error.message }),
      },
    );
  };
}
