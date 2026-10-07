import { useEffect, useEffectEvent } from "react";

// Pressing 1..count calls onPick(index); ignored while the exercise is locked.
export function useNumberKeys(count: number, isLocked: boolean, onPick: (index: number) => void) {
  const handleKeyDown = useEffectEvent((event: KeyboardEvent) => {
    const index = Number(event.key) - 1;
    if (Number.isInteger(index) && index >= 0 && index < count) {
      onPick(index);
    }
  });

  useEffect(() => {
    if (isLocked) {
      return;
    }
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [isLocked]);
}
