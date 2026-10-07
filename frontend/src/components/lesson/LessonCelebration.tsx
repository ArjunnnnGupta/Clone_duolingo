"use client";

import { useRouter } from "next/navigation";
import { useState } from "react";
import type { AttemptResult } from "@/lib/types";
import { DailyGoalScreen } from "./DailyGoalScreen";
import { LessonCompleteScreen } from "./LessonCompleteScreen";
import { StreakScreen } from "./StreakScreen";

type Step = "complete" | "streak" | "dailyGoal";

// Lesson complete, then the streak screen if the server extended the streak, then the daily-goal
// screen if the server says the goal was just met, then back to the path.
export function LessonCelebration({ result }: { result: AttemptResult }) {
  const router = useRouter();
  const steps: Step[] = [
    "complete",
    ...(result.streak.extended ? (["streak"] as const) : []),
    ...(result.daily_goal.just_met ? (["dailyGoal"] as const) : []),
  ];
  const [stepIndex, setStepIndex] = useState(0);

  function next() {
    if (stepIndex + 1 < steps.length) {
      setStepIndex(stepIndex + 1);
    } else {
      router.push("/learn");
    }
  }

  switch (steps[stepIndex]) {
    case "complete":
      return <LessonCompleteScreen result={result} onContinue={next} />;
    case "streak":
      return <StreakScreen streak={result.streak} onContinue={next} />;
    case "dailyGoal":
      return <DailyGoalScreen dailyGoal={result.daily_goal} onContinue={next} />;
  }
}
