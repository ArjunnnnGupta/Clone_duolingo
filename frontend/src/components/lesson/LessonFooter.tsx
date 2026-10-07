import { Button } from "@/components/ui/Button";

interface LessonFooterProps {
  label: "Check" | "Continue";
  isEnabled: boolean;
  onPress: () => void;
}

// Plain bottom bar with a single action; feedback replaces it with FeedbackBanner.
export function LessonFooter({ label, isEnabled, onPress }: LessonFooterProps) {
  return (
    <div className="border-t-2 border-border">
      <div className="mx-auto flex w-full max-w-[1000px] justify-end px-4 py-6">
        <div className="w-full sm:w-40">
          <Button
            variant={isEnabled ? "primary" : "locked"}
            disabled={!isEnabled}
            onClick={onPress}
          >
            {label}
          </Button>
        </div>
      </div>
    </div>
  );
}
