import { Mascot } from "@/components/mascot/Mascot";

// Shown once, before the first hard exercise, when the learner has made no mistakes so far.
export function EncouragementScreen() {
  return (
    <div className="flex flex-1 flex-col items-center justify-center gap-3">
      <p className="relative rounded-2xl border-2 border-border px-4 py-3 text-[17px] font-bold">
        Great work! Let&apos;s make this a bit harder…
        <span className="absolute -bottom-2 left-1/2 h-3 w-3 -translate-x-1/2 rotate-45 border-b-2 border-r-2 border-border bg-surface" />
      </p>
      <Mascot className="h-36 w-36" pose="happy" />
    </div>
  );
}
