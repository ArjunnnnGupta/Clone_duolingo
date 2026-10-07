"use client";

import { use } from "react";
import { LessonPlayer } from "@/components/lesson/LessonPlayer";

export default function LessonPage({ params }: PageProps<"/lesson/[attemptId]">) {
  const { attemptId } = use(params);
  return <LessonPlayer attemptId={Number(attemptId)} />;
}
