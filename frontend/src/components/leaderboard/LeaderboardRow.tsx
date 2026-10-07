"use client";

import { useEffect, useRef } from "react";
import { Avatar } from "@/components/ui/Avatar";
import type { LeaderboardEntry } from "@/lib/types";

// Rank, name and XP are the server's; the current learner's row is highlighted and scrolled into view.
export function LeaderboardRow({ entry }: { entry: LeaderboardEntry }) {
  const rowRef = useRef<HTMLLIElement>(null);

  useEffect(() => {
    if (entry.is_me) {
      rowRef.current?.scrollIntoView({ block: "center" });
    }
  }, [entry.is_me]);

  return (
    <li
      ref={rowRef}
      aria-current={entry.is_me ? "true" : undefined}
      className={`flex items-center gap-4 rounded-2xl border-2 px-4 py-3 ${
        entry.is_me ? "border-blue bg-blue/10" : "border-transparent"
      }`}
    >
      <span className="w-8 text-center text-[17px] font-extrabold text-text-muted">{entry.rank}</span>
      <Avatar name={entry.display_name} color={entry.avatar_color} />
      <span className="min-w-0 flex-1 truncate text-[17px] font-extrabold">{entry.display_name}</span>
      <span className="shrink-0 text-text-muted">{entry.xp} XP</span>
    </li>
  );
}
