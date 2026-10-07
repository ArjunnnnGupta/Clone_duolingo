import { Mascot } from "@/components/mascot/Mascot";

export function ReviewIntro() {
  return (
    <div className="flex flex-1 items-center justify-center gap-3">
      <Mascot className="h-32 w-32 shrink-0" />
      <p className="relative rounded-2xl border-2 border-border px-4 py-3 text-[17px] font-bold">
        <span className="absolute -left-2 top-1/2 h-3 w-3 -translate-y-1/2 rotate-45 border-b-2 border-l-2 border-border bg-surface" />
        Let&apos;s review the ones you missed!
      </p>
    </div>
  );
}
