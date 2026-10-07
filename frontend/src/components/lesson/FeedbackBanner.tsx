"use client";

import { motion } from "framer-motion";
import { Button } from "@/components/ui/Button";
import { Icon } from "@/components/ui/Icon";
import type { AnswerResponse } from "@/lib/types";

interface FeedbackBannerProps {
  feedback: AnswerResponse;
  onContinue: () => void;
}

// Everything shown here is text the server sent: the verdict, the solution and any note.
export function FeedbackBanner({ feedback, onContinue }: FeedbackBannerProps) {
  const toneClasses = feedback.correct
    ? "bg-correct-bg text-correct-text"
    : "bg-wrong-bg text-wrong-text";

  return (
    <motion.div
      initial={{ y: "100%" }}
      animate={{ y: 0 }}
      transition={{ type: "spring", duration: 0.2, bounce: 0.1 }}
      className={toneClasses}
    >
      <div className="mx-auto flex w-full max-w-[1000px] items-center gap-4 px-4 py-6">
        <span className="flex h-14 w-14 shrink-0 items-center justify-center rounded-full bg-surface">
          <Icon name={feedback.correct ? "check" : "close"} className="h-8 w-8" />
        </span>
        <div className="flex-1 text-[17px] font-bold">
          <p className="text-2xl font-extrabold">
            {feedback.correct ? "Nice!" : "Correct solution:"}
          </p>
          {feedback.feedback_note && <p>{feedback.feedback_note}</p>}
          {feedback.correct_solution && <p>{feedback.correct_solution}</p>}
        </div>
        <div className="w-40 shrink-0">
          <Button variant={feedback.correct ? "primary" : "danger"} onClick={onContinue}>
            Continue
          </Button>
        </div>
      </div>
    </motion.div>
  );
}
