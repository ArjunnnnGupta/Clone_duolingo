"use client";

import { animate, motion, useMotionValue, useTransform } from "framer-motion";
import { useEffect } from "react";

// Counts from 0 up to the server's number; the last frame is always exactly `to`.
export function CountUp({ to, durationS = 0.8 }: { to: number; durationS?: number }) {
  const value = useMotionValue(0);
  const rounded = useTransform(value, (latest) => Math.round(latest));

  useEffect(() => {
    const controls = animate(value, to, { duration: durationS, ease: "easeOut", delay: 0.3 });
    return () => controls.stop();
  }, [value, to, durationS]);

  return <motion.span>{rounded}</motion.span>;
}
