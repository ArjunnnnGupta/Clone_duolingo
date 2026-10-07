"use client";

import Link from "next/link";
import { use } from "react";

// Placeholder until Phase 6 builds the lesson player.
export default function LessonPage({ params }: PageProps<"/lesson/[attemptId]">) {
  const { attemptId } = use(params);
  return (
    <main className="mx-auto mt-24 max-w-xl px-4 text-center">
      <h1 className="text-2xl font-extrabold">Lesson attempt #{attemptId}</h1>
      <p className="mt-2 text-text-muted">The lesson player arrives in Phase 6.</p>
      <Link href="/learn" className="mt-6 inline-block font-extrabold uppercase text-blue">
        Back to path
      </Link>
    </main>
  );
}
