import confetti from "canvas-confetti";

// One celebratory burst; skipped for learners who ask their system for reduced motion.
export function celebrate() {
  confetti({ particleCount: 120, spread: 80, origin: { y: 0.6 }, disableForReducedMotion: true });
}
