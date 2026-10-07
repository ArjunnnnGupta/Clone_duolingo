import type { ReactNode } from "react";

export function SettingsSection({ title, children }: { title: string; children: ReactNode }) {
  return (
    <section className="mt-8">
      <h2 className="mb-4 text-xl font-extrabold">{title}</h2>
      {children}
    </section>
  );
}
