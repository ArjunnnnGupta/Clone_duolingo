"use client";

import { PathColumn } from "@/components/path/PathColumn";
import { Skeleton } from "@/components/ui/Skeleton";
import { usePath } from "@/lib/queries";

export default function LearnPage() {
  const { data: path, isError, error } = usePath();

  if (isError) {
    return <p className="mt-10 text-center text-text-muted">Could not load the path: {error.message}</p>;
  }
  if (!path) {
    return (
      <div className="mt-4 flex flex-col items-center gap-6">
        <Skeleton className="h-24 w-full" />
        <Skeleton className="h-[70px] w-[70px] rounded-full" />
        <Skeleton className="h-[70px] w-[70px] rounded-full" />
      </div>
    );
  }
  return <PathColumn units={path.units} />;
}
