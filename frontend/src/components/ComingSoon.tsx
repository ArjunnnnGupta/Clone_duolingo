"use client";

import { useRouter } from "next/navigation";
import { Mascot } from "@/components/mascot/Mascot";
import { Button } from "@/components/ui/Button";

export function ComingSoon({ title }: { title: string }) {
  const router = useRouter();

  return (
    <div className="flex flex-col items-center gap-4 pt-24 text-center">
      <Mascot className="h-32 w-32" />
      <h1 className="text-3xl font-extrabold">{title}</h1>
      <p className="text-[17px] text-text-muted">Coming soon!</p>
      <div className="w-full max-w-[240px]">
        <Button onClick={() => router.push("/learn")}>Back to learning</Button>
      </div>
    </div>
  );
}
