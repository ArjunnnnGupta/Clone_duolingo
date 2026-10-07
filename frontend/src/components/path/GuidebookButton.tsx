"use client";

import { Icon } from "@/components/ui/Icon";
import { useToast } from "@/components/ui/ToastProvider";

// The guidebook is out of scope; the button exists so the banner matches the real app.
export function GuidebookButton() {
  const showToast = useToast();

  return (
    <button
      onClick={() => showToast("Coming soon!")}
      aria-label="Guidebook"
      className="flex items-center gap-2 rounded-xl border-2 border-on-color/30 bg-on-color/10 px-3 py-2 text-sm font-extrabold uppercase tracking-[0.8px] hover:bg-on-color/20"
    >
      <Icon name="notebook" className="h-6 w-6" />
      <span className="hidden sm:inline">Guidebook</span>
    </button>
  );
}
