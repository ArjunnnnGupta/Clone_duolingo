"use client";

import { useRouter } from "next/navigation";
import { Mascot } from "@/components/mascot/Mascot";
import { Button } from "@/components/ui/Button";

interface LessonMessageScreenProps {
  title: string;
  message: string;
}

// Used when a lesson cannot continue (out of hearts, already ended, failed to load).
export function LessonMessageScreen({ title, message }: LessonMessageScreenProps) {
  const router = useRouter();

  return (
    <div className="flex min-h-screen flex-col items-center justify-center gap-4 px-4 text-center">
      <Mascot className="h-32 w-32" />
      <h1 className="text-2xl font-extrabold">{title}</h1>
      <p className="text-text-muted">{message}</p>
      <div className="w-full max-w-[240px]">
        <Button onClick={() => router.push("/learn")}>Back to path</Button>
      </div>
    </div>
  );
}
