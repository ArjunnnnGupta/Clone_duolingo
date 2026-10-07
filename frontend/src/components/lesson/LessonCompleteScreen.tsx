"use client";

import { useRouter } from "next/navigation";
import { Mascot } from "@/components/mascot/Mascot";
import { Button } from "@/components/ui/Button";
import type { AttemptResult } from "@/lib/types";
import { StatCard } from "./StatCard";

// Read-only: XP and accuracy are the figures the server stored when it finalized the lesson.
export function LessonCompleteScreen({ result }: { result: AttemptResult }) {
  const router = useRouter();

  return (
    <div className="flex min-h-screen flex-col">
      <div className="flex flex-1 flex-col items-center justify-center gap-6 px-4">
        <Mascot className="h-40 w-40" />
        <h1 className="text-3xl font-extrabold text-gold-shade">Lesson Complete!</h1>
        <div className="flex gap-4">
          <StatCard tone="gold" label="Total XP" value={String(result.xp_earned)} icon="bolt" />
          <StatCard tone="green" label="Accuracy" value={`${result.accuracy}%`} icon="check" />
        </div>
      </div>
      <div className="border-t-2 border-border">
        <div className="mx-auto flex w-full max-w-[1000px] justify-end px-4 py-6">
          <div className="w-full sm:w-40">
            <Button onClick={() => router.push("/learn")}>Continue</Button>
          </div>
        </div>
      </div>
    </div>
  );
}
