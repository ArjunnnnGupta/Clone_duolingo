"use client";

import { usePath } from "@/lib/queries";

// Original badge standing in for the course flag; the course name comes from the server.
export function CourseFlag() {
  const { data: path } = usePath();

  return (
    <span
      className="flex h-8 w-10 items-center justify-center rounded-lg border-2 border-border bg-surface-subtle"
      title={path?.course.title}
    >
      <span className="h-3.5 w-3.5 rounded-full bg-red" />
    </span>
  );
}
