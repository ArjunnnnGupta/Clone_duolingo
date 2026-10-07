"use client";

import { Icon } from "@/components/ui/Icon";
import { usePracticeForHeart, useRefillHearts } from "@/lib/queries";
import type { MeStats } from "@/lib/types";
import { NextHeartCountdown } from "./NextHeartCountdown";
import { PanelActionRow } from "./PanelActionRow";

// Every figure here is the server's: the filled hearts, the countdown, the refill price, and
// any error. The client never checks whether a refill is affordable or hearts are full.
interface HeartsPanelProps {
  stats: MeStats;
  // When /me last arrived; the countdown is anchored to it.
  receivedAt: number;
}

export function HeartsPanel({ stats, receivedAt }: HeartsPanelProps) {
  const refill = useRefillHearts();
  const practice = usePracticeForHeart();
  const errorMessage = refill.error?.message ?? practice.error?.message;

  return (
    <div className="flex flex-col gap-4 text-center">
      <h2 className="text-2xl font-extrabold">Hearts</h2>
      <div className="flex justify-center gap-2" aria-label={`${stats.hearts} hearts`}>
        {Array.from({ length: stats.max_hearts }, (_, index) => (
          <Icon
            key={index}
            name="heart"
            className={`h-8 w-8 ${index < stats.hearts ? "text-red" : "text-border"}`}
          />
        ))}
      </div>
      <div className="text-[17px]">
        {stats.seconds_until_next_heart === null ? (
          <>
            <p className="font-extrabold">You have full hearts</p>
            <p className="text-text-muted">Keep on learning</p>
          </>
        ) : (
          <p className="font-extrabold">
            <NextHeartCountdown
              key={receivedAt}
              serverSeconds={stats.seconds_until_next_heart}
              receivedAt={receivedAt}
            />
          </p>
        )}
      </div>
      <div className="flex flex-col gap-2">
        <PanelActionRow
          label="Refill hearts"
          icon="heart"
          detail={String(stats.refill_cost_gems)}
          detailIcon="gem"
          isBusy={refill.isPending}
          onClick={() => {
            practice.reset();
            refill.mutate();
          }}
        />
        <PanelActionRow
          label="Practice to earn hearts"
          icon="heart"
          isBusy={practice.isPending}
          onClick={() => {
            refill.reset();
            practice.mutate();
          }}
        />
      </div>
      {errorMessage && <p className="text-sm text-red">{errorMessage}</p>}
    </div>
  );
}
