"use client";

import { useToast } from "@/components/ui/ToastProvider";
import { useMe, useUpdateSettings } from "@/lib/queries";

// Mirrors the server's DAILY_GOAL_OPTIONS; the server still rejects anything else.
const GOAL_OPTIONS = [
  { xp: 10, label: "Casual" },
  { xp: 20, label: "Regular" },
  { xp: 30, label: "Serious" },
  { xp: 50, label: "Intense" },
] as const;

export function GoalPicker() {
  const { data: me } = useMe();
  const updateSettings = useUpdateSettings();
  const showToast = useToast();

  function choose(goalXp: number) {
    updateSettings.mutate(
      { daily_goal_xp: goalXp },
      {
        onSuccess: () => showToast("Settings saved"),
        onError: (error) => showToast(error.message),
      },
    );
  }

  return (
    <div className="flex flex-col gap-3">
      {GOAL_OPTIONS.map(({ xp, label }) => {
        const isSelected = me?.user.daily_goal_xp === xp;
        return (
          <button
            key={xp}
            disabled={!me || updateSettings.isPending}
            onClick={() => choose(xp)}
            className={`flex items-center justify-between rounded-2xl border-2 border-b-4 px-4 py-3 text-[17px] font-bold ${
              isSelected ? "border-blue bg-blue/10 text-blue" : "border-border hover:bg-surface-subtle"
            }`}
          >
            <span>{label}</span>
            <span>{xp} XP / day</span>
          </button>
        );
      })}
    </div>
  );
}
