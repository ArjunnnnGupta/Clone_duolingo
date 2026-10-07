import type { ReactNode } from "react";
import { LessonFooter } from "./LessonFooter";

// Centered content above a single CONTINUE bar; shared by the three post-lesson screens.
export function CelebrationLayout({
  children,
  onContinue,
}: {
  children: ReactNode;
  onContinue: () => void;
}) {
  return (
    <div className="flex min-h-screen flex-col">
      <div className="flex flex-1 flex-col items-center justify-center gap-6 px-4 text-center">
        {children}
      </div>
      <LessonFooter label="Continue" isEnabled onPress={onContinue} />
    </div>
  );
}
