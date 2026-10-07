import { useEffect, useEffectEvent } from "react";

// Calls onEnter when Enter is pressed outside a button; onEnter returns true if it acted.
export function useEnterKey(onEnter: () => boolean, isPaused: boolean) {
  // An effect event always sees the latest state, so the listener is attached once
  // instead of being re-attached on every render to avoid stale values.
  const handleKeyDown = useEffectEvent((event: KeyboardEvent) => {
    // A focused button already turns Enter into a click; handling it here too would fire twice.
    if (event.key !== "Enter" || event.repeat || event.target instanceof HTMLButtonElement) {
      return;
    }
    if (onEnter()) {
      event.preventDefault();
    }
  });

  useEffect(() => {
    if (isPaused) {
      return;
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isPaused]);
}
