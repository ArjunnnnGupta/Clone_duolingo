import { useEffect, useEffectEvent } from "react";

// Pressing the key at keys[i] calls onPick(i); ignored while the exercise is locked.
// Defaults to "1".."count", like the number badges on option cards.
export function useNumberKeys(
  count: number,
  isLocked: boolean,
  onPick: (index: number) => void,
  keys: string[] = Array.from({ length: count }, (_, index) => String(index + 1)),
) {
  const handleKeyDown = useEffectEvent((event: KeyboardEvent) => {
    const index = keys.indexOf(event.key);
    if (index >= 0) {
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
