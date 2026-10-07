"use client";

import { Button } from "@/components/ui/Button";
import { useToast } from "@/components/ui/ToastProvider";
import { ApiError } from "@/lib/api";
import { useAdvanceDay, useResetDemo } from "@/lib/queries";

// Demo helpers; the server only mounts these routes when ENABLE_DEV_TOOLS is on.
export function DevToolsPanel() {
  const advanceDay = useAdvanceDay();
  const resetDemo = useResetDemo();
  const showToast = useToast();

  const reportError = (error: Error) =>
    showToast(
      error instanceof ApiError && error.status === 404
        ? "Dev tools are off on this server"
        : error.message,
    );

  return (
    <div className="flex flex-col gap-3">
      <p className="text-text-muted">
        Move the clock forward to see streaks and hearts change without waiting.
      </p>
      <Button
        variant="secondary"
        disabled={advanceDay.isPending}
        onClick={() =>
          advanceDay.mutate(undefined, {
            onSuccess: () => showToast("Advanced one day"),
            onError: reportError,
          })
        }
      >
        Advance day
      </Button>
      <Button
        variant="ghost"
        disabled={resetDemo.isPending}
        onClick={() =>
          resetDemo.mutate(undefined, {
            onSuccess: () => showToast("Demo learner reset"),
            onError: reportError,
          })
        }
      >
        Reset demo
      </Button>
    </div>
  );
}
