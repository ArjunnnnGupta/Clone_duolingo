"use client";

import { useRefreshMe } from "@/lib/queries";
import { useCountdown } from "./useCountdown";

function formatClock(totalSeconds: number): string {
  const [hours, minutes, seconds] = [
    Math.floor(totalSeconds / 3600),
    Math.floor((totalSeconds % 3600) / 60),
    totalSeconds % 60,
  ].map((part) => String(part).padStart(2, "0"));
  return `${hours}:${minutes}:${seconds}`;
}

interface NextHeartCountdownProps {
  serverSeconds: number;
  // When the browser received serverSeconds (React Query's dataUpdatedAt).
  receivedAt: number;
}

// The parent remounts this on every /me fetch (keyed by receivedAt), so each server answer
// starts a fresh countdown even when it repeats the same number of seconds.
export function NextHeartCountdown({ serverSeconds, receivedAt }: NextHeartCountdownProps) {
  const refreshMe = useRefreshMe();
  const remaining = useCountdown(receivedAt + serverSeconds * 1000, refreshMe);
  return <span>Next heart in {formatClock(remaining)}</span>;
}
