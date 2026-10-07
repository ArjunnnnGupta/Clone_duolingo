import { Mascot } from "@/components/mascot/Mascot";

// The mascot "says" the text to translate, like the speech bubbles in the real app.
export function PromptBubble({ text }: { text: string }) {
  return (
    <div className="mb-6 flex items-center gap-3">
      <Mascot className="h-28 w-28 shrink-0" />
      <p className="relative rounded-2xl border-2 border-border px-4 py-3 text-[17px] font-bold">
        <span className="absolute -left-2 top-1/2 h-3 w-3 -translate-y-1/2 rotate-45 border-b-2 border-l-2 border-border bg-surface" />
        {text}
      </p>
    </div>
  );
}
