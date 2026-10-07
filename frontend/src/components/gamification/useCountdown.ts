import { useEffect, useEffectEvent, useRef, useState } from "react";

const TICK_MS = 250;

// Whole seconds left until deadlineMs (a browser timestamp). The deadline is anchored to when
// the server's value arrived, not to when this component mounted, so a panel opened minutes
// after the fetch still shows the true remaining time. At zero it calls onElapsed once so the
// caller can ask the server again; it never decides what happens to the hearts itself.
export function useCountdown(deadlineMs: number, onElapsed: () => void): number {
  const [now, setNow] = useState(() => Date.now());
  const hasElapsed = useRef(false);
  const handleElapsed = useEffectEvent(onElapsed);
  const remaining = Math.max(0, Math.ceil((deadlineMs - now) / 1000));

  useEffect(() => {
    const timer = setInterval(() => setNow(Date.now()), TICK_MS);
    return () => clearInterval(timer);
  }, []);

  useEffect(() => {
    if (remaining === 0 && !hasElapsed.current) {
      hasElapsed.current = true;
      handleElapsed();
    }
  }, [remaining]);

  return remaining;
}
