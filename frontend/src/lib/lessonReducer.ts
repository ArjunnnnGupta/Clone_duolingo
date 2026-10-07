import type {
  AnswerResponse,
  AttemptResponse,
  AttemptResult,
  ExerciseAnswer,
  LessonExercise,
} from "./types";

export type LessonPhase =
  | "answering"
  | "checking"
  | "feedback"
  | "reviewIntro"
  | "failed"
  | "complete"
  | "ended";

export interface LessonState {
  phase: LessonPhase;
  exercises: LessonExercise[];
  // Exercise ids still to be answered correctly; the head is the one on screen.
  queue: number[];
  correctIds: number[];
  // Every exercise answered wrong at least once in this attempt; it never shrinks.
  everMissedIds: number[];
  hasShownReviewIntro: boolean;
  answer: ExerciseAnswer | null;
  feedback: AnswerResponse | null;
  hearts: number;
  result: AttemptResult | null;
  errorMessage: string | null;
  // Bumped on every screen change so an exercise re-asked back-to-back starts fresh.
  step: number;
}

export type LessonAction =
  | { type: "SET_ANSWER"; answer: ExerciseAnswer | null }
  | { type: "CHECK_START" }
  | { type: "CHECK_RESULT"; response: AnswerResponse }
  | { type: "CHECK_ERROR"; message: string }
  | { type: "CONTINUE" }
  // The server closed the attempt (e.g. a lesson was started in another tab).
  | { type: "LESSON_CLOSED" }
  // A gem refill reopened a failed attempt on the server; hearts come from its response.
  | { type: "REFILLED"; hearts: number };

// The server keeps no queue, only the answer log. Rebuild it: untouched exercises in lesson
// order, then the ones answered wrong and not yet right.
export function createInitialState(attempt: AttemptResponse): LessonState {
  const correctIds = new Set(
    attempt.answered.filter((answer) => answer.is_correct).map((answer) => answer.exercise_id),
  );
  const answeredIds = new Set(attempt.answered.map((answer) => answer.exercise_id));
  const everMissedIds = [
    ...new Set(
      attempt.answered.filter((answer) => !answer.is_correct).map((answer) => answer.exercise_id),
    ),
  ];
  const untouchedIds = attempt.exercises
    .map((exercise) => exercise.id)
    .filter((id) => !answeredIds.has(id));
  const stillMissedIds = everMissedIds.filter((id) => !correctIds.has(id));
  const queue = [...untouchedIds, ...stillMissedIds];

  return {
    phase: initialPhase(attempt, stillMissedIds.includes(queue[0])),
    exercises: attempt.exercises,
    queue,
    correctIds: [...correctIds],
    everMissedIds,
    hasShownReviewIntro: false,
    answer: null,
    feedback: null,
    hearts: attempt.hearts,
    result: attempt.result,
    errorMessage: null,
    step: 0,
  };
}

function initialPhase(attempt: AttemptResponse, isHeadMissed: boolean): LessonPhase {
  if (attempt.status === "completed") return "complete";
  if (attempt.status === "failed") return "failed";
  if (attempt.status === "abandoned") return "ended";
  return isHeadMissed ? "reviewIntro" : "answering";
}

export function lessonReducer(state: LessonState, action: LessonAction): LessonState {
  switch (action.type) {
    case "SET_ANSWER":
      return state.phase === "answering" ? { ...state, answer: action.answer } : state;
    case "CHECK_START":
      return state.phase === "answering" ? { ...state, phase: "checking", errorMessage: null } : state;
    case "CHECK_RESULT":
      return state.phase === "checking" ? applyCheckResult(state, action.response) : state;
    case "CHECK_ERROR":
      return { ...state, phase: "answering", errorMessage: action.message };
    case "CONTINUE":
      return applyContinue(state);
    case "LESSON_CLOSED":
      return { ...state, phase: "ended" };
    case "REFILLED":
      return state.phase === "failed" ? resumeAfterRefill(state, action.hearts) : state;
  }
}

// Hearts, status and result are copied from the response; nothing here computes a game value.
// The queue itself only moves on CONTINUE so the answered exercise stays on screen under the feedback.
function applyCheckResult(state: LessonState, response: AnswerResponse): LessonState {
  const answeredId = state.queue[0];
  return {
    ...state,
    phase: "feedback",
    feedback: response,
    hearts: response.hearts,
    result: response.result,
    correctIds: response.correct ? [...state.correctIds, answeredId] : state.correctIds,
    everMissedIds:
      response.correct || state.everMissedIds.includes(answeredId)
        ? state.everMissedIds
        : [...state.everMissedIds, answeredId],
  };
}

function resumeAfterRefill(state: LessonState, hearts: number): LessonState {
  const isReviewStart = !state.hasShownReviewIntro && state.everMissedIds.includes(state.queue[0]);
  return {
    ...state,
    hearts,
    phase: isReviewStart ? "reviewIntro" : "answering",
    step: state.step + 1,
  };
}

function applyContinue(state: LessonState): LessonState {
  if (state.phase === "reviewIntro") {
    return { ...state, phase: "answering", hasShownReviewIntro: true, step: state.step + 1 };
  }
  if (state.phase !== "feedback" || state.feedback === null) {
    return state;
  }
  const [answeredId, ...rest] = state.queue;
  const queue = state.feedback.correct ? rest : [...rest, answeredId];
  const next = { ...state, queue, answer: null, feedback: null, step: state.step + 1 };

  if (state.result) return { ...next, phase: "complete" };
  if (state.feedback.status === "failed") return { ...next, phase: "failed" };
  const isReviewStart = !state.hasShownReviewIntro && state.everMissedIds.includes(queue[0]);
  return { ...next, phase: isReviewStart ? "reviewIntro" : "answering" };
}

// What Enter should do right now; match pairs has no CHECK button, so Enter never checks it.
export function enterKeyAction(
  state: LessonState,
  isSubmittedOnComplete: boolean,
): "check" | "continue" | null {
  if (state.phase === "answering" && state.answer && !isSubmittedOnComplete) return "check";
  if (state.phase === "feedback" || state.phase === "reviewIntro") return "continue";
  return null;
}
