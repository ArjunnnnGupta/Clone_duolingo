import { Icon } from "@/components/ui/Icon";
import { ProgressBar } from "@/components/ui/ProgressBar";
import { HeartsCounter } from "./HeartsCounter";

interface LessonHeaderProps {
  progressFraction: number;
  hearts: number;
  isQuitDisabled: boolean;
  onQuit: () => void;
}

export function LessonHeader({ progressFraction, hearts, isQuitDisabled, onQuit }: LessonHeaderProps) {
  return (
    <header className="mx-auto flex w-full max-w-[1000px] items-center gap-4 px-4 py-4">
      <button
        aria-label="Quit lesson"
        disabled={isQuitDisabled}
        onClick={onQuit}
        className="text-text-subtle hover:text-text-muted disabled:cursor-not-allowed disabled:opacity-50"
      >
        <Icon name="close" className="h-7 w-7" />
      </button>
      <ProgressBar fraction={progressFraction} />
      <HeartsCounter hearts={hearts} />
    </header>
  );
}
