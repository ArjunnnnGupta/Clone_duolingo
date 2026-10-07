"use client";

import { motion, useAnimationControls } from "framer-motion";
import { useEffect, useRef } from "react";
import { Icon } from "@/components/ui/Icon";

// Shows the server's heart count; it only shakes when that count drops.
export function HeartsCounter({ hearts }: { hearts: number }) {
  const controls = useAnimationControls();
  const previousHearts = useRef(hearts);

  useEffect(() => {
    if (hearts < previousHearts.current) {
      controls.start({ scale: [1.3, 1], x: [0, -4, 4, -2, 0], transition: { duration: 0.4 } });
    }
    previousHearts.current = hearts;
  }, [hearts, controls]);

  return (
    <motion.span animate={controls} className="flex items-center gap-1.5 font-extrabold text-red">
      <Icon name="heart" className="h-7 w-7" />
      {hearts}
    </motion.span>
  );
}
