"use client";

import { useSyncExternalStore } from "react";
import { applyTheme, readTheme, subscribeToTheme, type Theme } from "@/lib/theme";

const OPTIONS: { theme: Theme; label: string }[] = [
  { theme: "light", label: "Light" },
  { theme: "dark", label: "Dark" },
];

export function ThemeToggle() {
  // The server always renders light; the browser reads what the <head> script applied.
  const current = useSyncExternalStore(subscribeToTheme, readTheme, () => "light" as Theme);

  return (
    <div className="grid grid-cols-2 gap-3" role="radiogroup" aria-label="Theme">
      {OPTIONS.map(({ theme, label }) => {
        const isSelected = current === theme;
        return (
          <button
            key={theme}
            role="radio"
            aria-checked={isSelected}
            onClick={() => applyTheme(theme)}
            className={`rounded-2xl border-2 border-b-4 px-4 py-3 text-[17px] font-bold ${
              isSelected ? "border-blue bg-blue/10 text-blue" : "border-border hover:bg-surface-subtle"
            }`}
          >
            {label}
          </button>
        );
      })}
    </div>
  );
}
