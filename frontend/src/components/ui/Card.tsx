import type { ReactNode } from "react";

export function Card({ className = "", children }: { className?: string; children: ReactNode }) {
  return (
    <section className={`rounded-2xl border-2 border-border bg-surface p-4 ${className}`}>
      {children}
    </section>
  );
}
