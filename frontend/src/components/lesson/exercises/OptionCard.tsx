import type { ReactNode } from "react";

const STATE_CLASSES = {
  default: "border-border bg-surface hover:bg-surface-subtle",
  selected: "border-blue bg-blue/10 text-blue",
  wrong: "border-red bg-red/10 text-red",
  matched: "pointer-events-none border-border bg-surface-subtle text-text-subtle opacity-50",
} as const;

interface OptionCardProps {
  state?: keyof typeof STATE_CLASSES;
  keyHint?: string;
  isDisabled?: boolean;
  onClick: () => void;
  children: ReactNode;
}

// White 3D card shared by multiple choice, fill-blank and match pairs.
export function OptionCard({
  state = "default",
  keyHint,
  isDisabled = false,
  onClick,
  children,
}: OptionCardProps) {
  return (
    <button
      disabled={isDisabled}
      onClick={onClick}
      className={`flex w-full items-center gap-4 rounded-2xl border-2 border-b-4 px-4 py-3 text-left text-[17px] font-bold active:translate-y-0.5 active:border-b-2 disabled:cursor-default ${STATE_CLASSES[state]}`}
    >
      {keyHint && (
        <span className="flex h-7 w-7 shrink-0 items-center justify-center rounded-lg border-2 border-border text-sm text-text-muted">
          {keyHint}
        </span>
      )}
      <span className="flex flex-1 items-center justify-center gap-3">{children}</span>
    </button>
  );
}
