"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import { useAttempt, useQuitAttempt } from "@/lib/queries";
import type { AttemptResponse } from "@/lib/types";
import { Skeleton } from "@/components/ui/Skeleton";
import { ExerciseRenderer } from "./ExerciseRenderer";
import { FeedbackBanner } from "./FeedbackBanner";
import { LessonCelebration } from "./LessonCelebration";
import { LessonFooter } from "./LessonFooter";
import { LessonHeader } from "./LessonHeader";
import { LessonMessageScreen } from "./LessonMessageScreen";
import { OutOfHeartsModal } from "./OutOfHeartsModal";
import { QuitConfirmModal } from "./QuitConfirmModal";
import { EncouragementScreen } from "./EncouragementScreen";
import { ReviewIntro } from "./ReviewIntro";
import { useLessonPlayer } from "./useLessonPlayer";

export function LessonPlayer({ attemptId }: { attemptId: number }) {
  const { data: attempt, isError, error } = useAttempt(attemptId);

  if (isError) {
    return <LessonMessageScreen title="We couldn't open this lesson" message={error.message} />;
  }
  if (!attempt) {
    return <Skeleton className="m-4 h-4" />;
  }
  return <ActiveLesson attempt={attempt} />;
}

function ActiveLesson({ attempt }: { attempt: AttemptResponse }) {
  const router = useRouter();
  const [isQuitOpen, setIsQuitOpen] = useState(false);
  const { state, currentExercise, setAnswer, checkCurrentAnswer, continueLesson, resumeAfterRefill } =
    useLessonPlayer(attempt, isQuitOpen);
  const quitAttempt = useQuitAttempt(attempt.attempt_id);

  if (state.phase === "complete" && state.result) {
    return <LessonCelebration result={state.result} />;
  }
  if (state.phase === "ended") {
    return <LessonMessageScreen title="This lesson has ended" message="Start it again from the path." />;
  }

  // Interstitial screens (review intro, encouragement) have only a CONTINUE button.
  const isInterstitial = state.phase === "reviewIntro" || state.phase === "encouragement";
  const verdict = state.phase === "feedback" && state.feedback ? (state.feedback.correct ? "correct" : "wrong") : null;
  // Once the server has finalized the lesson there is no progress left to lose, so X just leaves.
  const handleQuit = () => (state.result ? router.push("/learn") : setIsQuitOpen(true));

  return (
    <div className="flex min-h-screen flex-col">
      <LessonHeader
        progressFraction={state.correctIds.length / state.exercises.length}
        hearts={state.hearts}
        combo={state.combo}
        isQuitDisabled={state.phase === "checking" || state.phase === "failed"}
        onQuit={handleQuit}
      />
      <main className="mx-auto flex w-full max-w-[600px] flex-1 flex-col justify-center px-4 py-6">
        {state.phase === "reviewIntro" && <ReviewIntro />}
        {state.phase === "encouragement" && <EncouragementScreen />}
        {!isInterstitial && currentExercise && (
          <ExerciseRenderer
            key={`${currentExercise.id}-${state.step}`}
            exercise={currentExercise}
            isLocked={state.phase !== "answering" || isQuitOpen}
            verdict={verdict}
            onAnswerChange={setAnswer}
          />
        )}
        {state.errorMessage && <p className="mt-4 text-center text-red">{state.errorMessage}</p>}
      </main>
      {state.phase === "feedback" && state.feedback ? (
        <FeedbackBanner feedback={state.feedback} onContinue={continueLesson} />
      ) : (
        <LessonFooter
          label={isInterstitial ? "Continue" : "Check"}
          isEnabled={isInterstitial || (state.phase === "answering" && state.answer !== null)}
          onPress={isInterstitial ? continueLesson : checkCurrentAnswer}
        />
      )}
      <OutOfHeartsModal
        isOpen={state.phase === "failed"}
        onRefilled={resumeAfterRefill}
        onDecline={() => router.push("/learn")}
        isDismissible={false}
      />
      <QuitConfirmModal
        isOpen={isQuitOpen}
        isQuitting={quitAttempt.isPending}
        errorMessage={quitAttempt.error?.message ?? null}
        onKeepLearning={() => setIsQuitOpen(false)}
        onEndSession={() => quitAttempt.mutate()}
      />
    </div>
  );
}
